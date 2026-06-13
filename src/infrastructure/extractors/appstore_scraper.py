import os
import re
import requests
import pandas as pd
import hashlib
from bs4 import BeautifulSoup
from typing import List, Dict, Any
from datetime import datetime
from src.core.interfaces.scraper_interface import BaseScraper


class AppStoreScraper(BaseScraper):
    """
    Scraper Híbrido para Apple App Store:
    1. Intenta extraer hasta 500 reseñas vía RSS (iTunes API).
    2. Si RSS falla o devuelve 0, hace un fallback de "Degradación Elegante" 
       extrayendo las reseñas destacadas incrustadas estáticamente en el HTML.
    """

    def __init__(self, country: str = "bo"):
        super().__init__()
        self.country = country
        self.rss_url = "https://itunes.apple.com/{country}/rss/customerreviews/page={page}/id={app_id}/sortby=mostrecent/json"
        self.html_url = "https://apps.apple.com/{country}/app/{app_name}/id{app_id}?see-all=reviews"

    def _hash_username(self, username: str) -> str:
        if not username:
            return "Anonymous"
        return hashlib.sha256(username.encode('utf-8')).hexdigest()

    def extract_reviews(
        self, app_id: str, max_reviews: int = 500
    ) -> List[Dict[str, Any]]:
        try:
            name, identifier = app_id.split(",")
        except Exception:
            raise ValueError(
                "Para App Store, app_id debe ser 'app_name,app_id' numérico. Ej: 'nequi,1302266602'"
            )

        self.logger.info(self.__class__.__name__, f"Iniciando extracción RSS App Store para {name} en {self.country}")
        
        # 1. Intentar RSS
        reviews = self._extract_via_rss(identifier, max_reviews)
        if reviews:
            self.logger.info(self.__class__.__name__, f"RSS exitoso: {len(reviews)} reviews extraídas para {name}.")
            return reviews
            
        self.logger.warning(self.__class__.__name__, f"RSS devolvió 0 reviews para {name}. Intentando fallback HTML.")
        
        # 2. Fallback HTML
        html_reviews = self._extract_via_html(name, identifier)
        self.logger.info(self.__class__.__name__, f"Fallback HTML extrajo {len(html_reviews)} reviews para {name}.")
        return html_reviews

    def _extract_via_rss(self, identifier: str, max_reviews: int) -> List[Dict[str, Any]]:
        all_reviews = []
        for page in range(1, 11):
            url = self.rss_url.format(country=self.country, page=page, app_id=identifier)
            headers = {"User-Agent": "Mozilla/5.0"}
            try:
                response = requests.get(url, headers=headers, timeout=10)
                if response.status_code != 200:
                    break
                
                data = response.json()
                entries = data.get("feed", {}).get("entry", [])
                if isinstance(entries, dict):
                    entries = [entries]
                if not entries:
                    break
                    
                for entry in entries:
                    if not entry.get("author"):
                        continue
                        
                    date_str = entry.get("updated", {}).get("label")
                    parsed_date = pd.to_datetime(date_str).to_pydatetime() if date_str else datetime.now()
                            
                    raw_user = entry.get("author", {}).get("name", {}).get("label", "Unknown")
                    
                    review = {
                        "reviewId": str(entry.get("id", {}).get("label", "")),
                        "userName": self._hash_username(raw_user),
                        "userImage": None,
                        "content": entry.get("content", {}).get("label", ""),
                        "score": int(entry.get("im:rating", {}).get("label", 0)),
                        "thumbsUpCount": int(entry.get("im:voteCount", {}).get("label", 0)),
                        "reviewCreatedVersion": entry.get("im:version", {}).get("label", ""),
                        "at": parsed_date,
                        "replyContent": None,
                        "repliedAt": None,
                        "appVersion": entry.get("im:version", {}).get("label", "")
                    }
                    all_reviews.append(review)
            except Exception as e:
                self.logger.warning(self.__class__.__name__, f"Error fetching page {page} RSS: {e}")
                break
                
            if len(all_reviews) >= max_reviews:
                break
                
        unique_reviews = {r["reviewId"]: r for r in all_reviews if r["reviewId"]}.values()
        return list(unique_reviews)[:max_reviews]

    def _extract_via_html(self, app_name: str, identifier: str) -> List[Dict[str, Any]]:
        url = self.html_url.format(country=self.country, app_name=app_name, app_id=identifier)
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
            "Accept-Language": "es-419,es;q=0.9"
        }
        
        try:
            response = requests.get(url, headers=headers, timeout=10)
            if response.status_code != 200:
                return []
                
            soup = BeautifulSoup(response.text, "html.parser")
            review_divs = soup.find_all("div", class_=re.compile(r"container.*is-detail-view"))
            
            extracted = []
            for i, r in enumerate(review_divs):
                try:
                    title_elem = r.find("h3", id=re.compile(r"review-.*-title"))
                    title = title_elem.text.strip() if title_elem else ""
                    
                    author_elem = r.find("span", class_=re.compile("author"))
                    author = author_elem.text.strip() if author_elem else f"User_{i}"
                    
                    date_elem = r.find("time")
                    date_str = date_elem.get("datetime") if date_elem else ""
                    parsed_date = pd.to_datetime(date_str).to_pydatetime() if date_str else datetime.now()
                    
                    # Apple structure puts the P tag outside the detail-view div sometimes
                    content_elem = r.parent.find("p") if r.parent else r.find("p", attrs={"data-testid": "truncate-text"})
                    content = content_elem.text.strip() if content_elem else ""
                    content = content.replace("HTML_TAG_START", "").replace("HTML_TAG_END", "").strip()
                    
                    if not content and title:
                        content = title
                        
                    ol_stars = r.find("ol", class_=re.compile("stars"))
                    rating = 0
                    if ol_stars:
                        aria = ol_stars.get("aria-label", "")
                        match = re.search(r'(\d+)', aria)
                        if match:
                            rating = int(match.group(1))
                            
                    # Si no hay contenido real ni rating, saltear (p. ej. texto de privacidad)
                    if not content and rating == 0:
                        continue
                        
                    if "El desarrollador" in content and "política de privacidad" in content:
                        continue
                        
                    review = {
                        "reviewId": f"html-{identifier}-{i}",
                        "userName": self._hash_username(author),
                        "userImage": None,
                        "content": content,
                        "score": rating,
                        "thumbsUpCount": 0,
                        "reviewCreatedVersion": None,
                        "at": parsed_date,
                        "replyContent": None,
                        "repliedAt": None,
                        "appVersion": None
                    }
                    extracted.append(review)
                except Exception:
                    continue
            return extracted
        except Exception as e:
            self.logger.error(self.__class__.__name__, f"Error fallback HTML App Store: {e}")
            return []

    def save_to_bronze(self, app_id: str, data: List[Dict[str, Any]]):
        pass

