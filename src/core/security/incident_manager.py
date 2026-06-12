from typing import List, Protocol
from datetime import datetime

class IncidentObserver(Protocol):
    def update(self, level: str, module: str, message: str, **kwargs) -> None:
        pass

class IncidentManager(IncidentObserver):
    """
    Gestiona y enruta incidentes críticos hacia la Mesa de Servicios (DevOps).
    Aplica el Patrón Observer suscribiéndose al AuditLogger.
    Cumple con ITIL 4 (Incident Management) e ISO 27001 (A.5.24).
    """

    def __init__(self):
        self.incident_history: List[dict] = []
        self._alert_thresholds = ["ERROR", "CRITICAL"]

    def update(self, level: str, module: str, message: str, **kwargs) -> None:
        """
        Método llamado por el Subject (AuditLogger) cuando se registra un log.
        """
        if level.upper() in self._alert_thresholds:
            self._trigger_swarming(level, module, message, **kwargs)

    def _trigger_swarming(self, level: str, module: str, message: str, **kwargs) -> None:
        """
        Simula el envío de una alerta crítica al equipo DevOps (Mesa de Servicios)
        para iniciar el protocolo de Swarming.
        """
        incident_data = {
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "level": level.upper(),
            "module": module,
            "message": message,
            "action": "INITIATE_SWARMING",
            "metadata": kwargs
        }
        self.incident_history.append(incident_data)
        
        # Aquí se conectaría con Slack, PagerDuty, o Email real.
        # Por ahora lo imprimimos como alerta en consola.
        print(f"\n[🚨 ALERTA DE MESA DE SERVICIOS - SWARMING ACTIVADO] \n"
              f"Nivel: {level.upper()} | Módulo: {module}\n"
              f"Detalle: {message}\n"
              f"--------------------------------------------------\n")

    def get_recent_incidents(self) -> List[dict]:
        return self.incident_history
