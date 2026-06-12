import logging
import json
import threading
from pathlib import Path
from datetime import datetime


class AuditLogger:
    """
    Singleton para Centralized Audit Logging.
    Garantiza el cumplimiento de ISO 27001 (A.8.15 Logging).
    Registra eventos en formato estructurado JSON.
    """

    _instance = None
    _lock = threading.Lock()

    def __new__(cls, log_file: str = "logs/audit.log"):
        with cls._lock:
            if cls._instance is None:
                cls._instance = super(AuditLogger, cls).__new__(cls)
                cls._instance._setup_logger(log_file)
        return cls._instance

    def _setup_logger(self, log_file: str):
        self.logger = logging.getLogger("OmniVoCAudit")
        self.logger.setLevel(logging.INFO)

        Path(log_file).parent.mkdir(parents=True, exist_ok=True)

        # Evitar añadir múltiples handlers si el singleton es llamado repetidas veces
        if not self.logger.handlers:
            handler = logging.FileHandler(log_file)
            handler.setLevel(logging.INFO)
            # Formateador simple porque el payload ya será JSON
            formatter = logging.Formatter("%(message)s")
            handler.setFormatter(formatter)
            self.logger.addHandler(handler)

    def log(
        self,
        level: str,
        module: str,
        message: str,
        contains_pii: bool = False,
        is_security_event: bool = False,
    ):
        log_entry = {
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "level": level.upper(),
            "module": module,
            "message": message,
            "contains_pii": contains_pii,
            "is_security_event": is_security_event,
        }
        log_json = json.dumps(log_entry)

        if level.upper() in ["ERROR", "CRITICAL"]:
            self.logger.error(log_json)
        elif level.upper() == "WARNING":
            self.logger.warning(log_json)
        else:
            self.logger.info(log_json)

    def info(self, module: str, message: str, **kwargs):
        self.log("INFO", module, message, **kwargs)

    def error(self, module: str, message: str, **kwargs):
        self.log("ERROR", module, message, **kwargs)

    def warning(self, module: str, message: str, **kwargs):
        self.log("WARNING", module, message, **kwargs)
