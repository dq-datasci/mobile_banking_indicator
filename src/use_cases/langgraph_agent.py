import logging
from typing import TypedDict, Annotated, List, Dict
from langgraph.graph import StateGraph, END
import pandas as pd
from pyspark.sql import SparkSession
import os

logger = logging.getLogger("LangGraphAgent")

class AgentState(TypedDict):
    messages: Annotated[List[Dict], "The messages in the conversation"]
    user_issue: str
    urgency: str
    department: str
    intent: str

class OmniVocMultiAgent:
    """
    Agente Multi-Rol LangGraph que maneja quejas (Triage) y Consultas Analíticas (Data Analyst).
    """
    def __init__(self):
        self.graph = self._build_graph()
        self.nps_data = self._load_data()
        
    def _load_data(self):
        try:
            spark = SparkSession.builder.getOrCreate()
            if os.path.exists("data/gold/Aggr_NPS"):
                return spark.read.format("delta").load("data/gold/Aggr_NPS").toPandas()
        except:
            pass
        return pd.DataFrame()
        
    def _build_graph(self):
        workflow = StateGraph(AgentState)
        
        workflow.add_node("intent_router", self.intent_router_node)
        workflow.add_node("triage", self.triage_node)
        workflow.add_node("analyst", self.analyst_node)
        workflow.add_node("responder", self.responder_node)
        
        workflow.set_entry_point("intent_router")
        
        def route(state):
            if state.get("intent") == "analytics":
                return "analyst"
            return "triage"
            
        workflow.add_conditional_edges("intent_router", route)
        workflow.add_edge("triage", "responder")
        workflow.add_edge("analyst", "responder")
        workflow.add_edge("responder", END)
        
        return workflow.compile()
        
    def intent_router_node(self, state: AgentState):
        issue = state.get("user_issue", "").lower()
        intent = "triage"
        analytics_keywords = ["situacion", "situación", "banco", "churn", "probabilidad", "nps", "recomienda", "mitigar", "análisis", "analisis", "rendimiento"]
        if any(word in issue for word in analytics_keywords):
            intent = "analytics"
        return {"intent": intent}

    def triage_node(self, state: AgentState):
        issue = state.get("user_issue", "")
        urgency = "Baja"
        department = "Atención al Cliente"
        
        critical_keywords = ["robo", "robaron", "robado", "robar", "hack", "fraude", "estafa", "vaciaron", "bloqueada", "error", "no sirve", "desaparecio", "desapareció"]
        if any(word in issue.lower() for word in critical_keywords):
            urgency = "Crítica"
            if any(word in issue.lower() for word in ["robo", "robar", "robado", "robaron", "fraude", "hack", "estafa", "vaciaron"]):
                department = "Seguridad / Legal"
            else:
                department = "Soporte Técnico Nivel 2"
                
        return {"urgency": urgency, "department": department}
        
    def analyst_node(self, state: AgentState):
        issue = state.get("user_issue", "").lower()
        department = "Analítica de Negocios"
        
        if self.nps_data.empty:
            msg = "Lo siento, no tengo acceso a la base de datos Gold en este momento."
            return {"department": department, "urgency": "Informativa", "messages": state.get("messages", []) + [{"role": "agent", "content": msg}]}
            
        banco_encontrado = None
        for b in self.nps_data['bank_name'].unique():
            if b.lower() in issue:
                banco_encontrado = b
                break
                
        if banco_encontrado:
            stats = self.nps_data[self.nps_data['bank_name'] == banco_encontrado].iloc[0]
            total = stats['total_reviews']
            prom = stats['promoters']
            detr = stats['detractors']
            nps = ((prom/total) - (detr/total))*100 if total > 0 else 0
            churn_prob = (detr / total) * 100 if total > 0 else 0
            
            msg = f"📊 **Análisis para {banco_encontrado}**:\n\n"
            msg += f"- **NPS Actual:** {nps:.1f} pts\n"
            msg += f"- **Volumen Analizado:** {total} reseñas\n"
            msg += f"- **Riesgo de Churn Estimado:** {churn_prob:.1f}%\n\n"
            
            if churn_prob > 30:
                msg += "🚨 **Recomendación:** La probabilidad de churn es ALTA debido a una elevada insatisfacción general. Se recomienda investigar inmediatamente el pipeline de UI/UX, lanzar retargeting agresivo y priorizar atención en canales sociales."
            else:
                msg += "✅ **Recomendación:** La retención es estable. Para subir el NPS, sugiero potenciar programas de referidos y beneficios VIP."
        else:
            msg = "🤖 No logré identificar un banco específico en tu pregunta (ej. BNB, BCP, BancoSol). Por favor, menciona el nombre de la institución para darte un reporte detallado."
            
        return {"department": department, "urgency": "Informativa", "messages": state.get("messages", []) + [{"role": "agent", "content": msg}]}

    def responder_node(self, state: AgentState):
        intent = state.get("intent")
        if intent == "analytics":
            return {}
            
        urgency = state.get("urgency")
        department = state.get("department")
        
        if urgency == "Crítica":
            msg = f"⚠️ [ALERTA] Hemos escalado tu caso inmediatamente a {department}. Por favor, NO compartas tus contraseñas por este medio. Un asesor se pondrá en contacto pronto."
        else:
            msg = "Gracias por comunicarte. Estamos revisando tu caso para mejorar nuestra app. Si necesitas ayuda adicional, contáctanos a soporte."
            
        new_msg = {"role": "agent", "content": msg}
        messages = state.get("messages", []) + [new_msg]
        return {"messages": messages}
        
    def process_issue(self, text: str) -> dict:
        initial_state = {
            "messages": [{"role": "user", "content": text}],
            "user_issue": text,
            "urgency": "",
            "department": "",
            "intent": ""
        }
        result = self.graph.invoke(initial_state)
        return {
            "urgency": result.get("urgency", "Informativa"),
            "department": result.get("department", "Asistente AI"),
            "response": result.get("messages")[-1]["content"]
        }
