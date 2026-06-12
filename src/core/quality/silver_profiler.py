import pandas as pd
from pathlib import Path
from src.core.security.audit_logger import AuditLogger

try:
    from ydata_profiling import ProfileReport
except ImportError:
    ProfileReport = None


class SilverProfilerFacade:
    """
    Facade para el análisis exploratorio automático (EDA) sobre la capa Silver.
    Cumple con SRP: encapsula toda la complejidad de generar reportes de calidad.
    """
    
    def __init__(self, output_dir: str = "reports/profiling"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.logger = AuditLogger()
        self.logger.info("SilverProfilerFacade", "Inicializado el generador de reportes de perfilamiento.")

    def generate_report(self, df: pd.DataFrame, report_name: str = "silver_profile.html") -> str:
        """
        Genera un reporte HTML usando ydata-profiling.
        Aplica Degradación Elegante (Fail Safe) si falla por memoria o dependencias.
        """
        output_path = self.output_dir / report_name
        
        try:
            if ProfileReport is None:
                raise ImportError("ydata-profiling no está instalado correctamente.")
                
            self.logger.info("SilverProfilerFacade", f"Iniciando perfilamiento completo para {report_name}")
            
            # minimal=True para evitar cuellos de botella en memoria (Fail Safe / Resiliencia)
            profile = ProfileReport(df, title="OmniVoC Silver Layer Profiling Report", minimal=True)
            profile.to_file(output_path)
            
            self.logger.info("SilverProfilerFacade", f"Reporte generado exitosamente en {output_path}")
            return str(output_path)
            
        except Exception as e:
            # Fallback en caso de OutOfMemory u otro error
            self.logger.warning(
                "SilverProfilerFacade", 
                f"Falla en ydata-profiling: {str(e)}. Aplicando fallback a Pandas Describe."
            )
            fallback_path = self.output_dir / report_name.replace(".html", "_fallback.html")
            self._generate_fallback_report(df, fallback_path)
            return str(fallback_path)
            
    def _generate_fallback_report(self, df: pd.DataFrame, output_path: Path):
        """
        Genera un reporte básico usando pandas en caso de que ydata-profiling falle.
        Cumple con el patrón Fallback (Degradación Elegante).
        """
        try:
            description = df.describe(include='all').to_html()
            info = pd.DataFrame({"Data Types": df.dtypes, "Non-Null Count": df.notnull().sum()}).to_html()
            
            html_content = f"""
            <html>
            <head><title>Fallback Silver Profile</title></head>
            <body>
                <h2>Basic Data Info</h2>
                {info}
                <h2>Basic Descriptive Statistics</h2>
                {description}
            </body>
            </html>
            """
            
            with open(output_path, "w", encoding="utf-8") as f:
                f.write(html_content)
                
            self.logger.info("SilverProfilerFacade", f"Fallback reporte generado en {output_path}")
        except Exception as e:
            self.logger.error("SilverProfilerFacade", f"Fallo crítico en Fallback Profiling: {str(e)}")
