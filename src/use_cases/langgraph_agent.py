import logging
from typing import TypedDict, Annotated, List, Dict
from langgraph.graph import StateGraph, END

logger = logging.getLogger("LangGraphAgent")

class AgentState(TypedDict):
    messages: Annotated[List[Dict], "The messages in the conversation"]
    user_issue: str
    urgency: str
    department: str

class CommunityManagerAgent:
    """
    Agente de LangGraph que rutea quejas y responde a usuarios (Historia 2.3.4 - 2.3.6).
    """
    def __init__(self):
        self.graph = self._build_graph()
        
    def _build_graph(self):
        workflow = StateGraph(AgentState)
        
        workflow.add_node("triage", self.triage_node)
        workflow.add_node("responder", self.responder_node)
        
        workflow.set_entry_point("triage")
        workflow.add_edge("triage", "responder")
        workflow.add_edge("responder", END)
        
        return workflow.compile()
        
    def triage_node(self, state: AgentState):
        issue = state.get("user_issue", "")
        urgency = "Baja"
        department = "Atención al Cliente"
        
        critical_keywords = ["robo", "hack", "fraude", "estafa", "vaciaron", "bloqueada", "error", "no sirve"]
        if any(word in issue.lower() for word in critical_keywords):
            urgency = "Crítica"
            if "robo" in issue.lower() or "fraude" in issue.lower() or "hack" in issue.lower():
                department = "Seguridad / Legal"
            else:
                department = "Soporte Técnico Nivel 2"
                
        return {"urgency": urgency, "department": department}
        
    def responder_node(self, state: AgentState):
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
            "department": ""
        }
        result = self.graph.invoke(initial_state)
        return {
            "urgency": result.get("urgency"),
            "department": result.get("department"),
            "response": result.get("messages")[-1]["content"]
        }
