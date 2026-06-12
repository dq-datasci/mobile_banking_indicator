import json
import os
from src.core.security.audit_logger import AuditLogger


def test_audit_logger_singleton():
    logger1 = AuditLogger("logs/test_audit.log")
    logger2 = AuditLogger("logs/test_audit.log")
    assert logger1 is logger2


def test_audit_logger_writes_json():
    log_file = "logs/test_audit_write.log"
    if os.path.exists(log_file):
        os.remove(log_file)

    logger = AuditLogger(log_file)
    # Evitar arrastrar handlers del test anterior
    logger.logger.handlers.clear()
    logger._setup_logger(log_file)

    logger.info("TestModule", "Test message", contains_pii=True)

    with open(log_file, "r") as f:
        line = f.readline()
        log_entry = json.loads(line)
        assert log_entry["level"] == "INFO"
        assert log_entry["module"] == "TestModule"
        assert log_entry["message"] == "Test message"
        assert log_entry["contains_pii"] is True
        assert log_entry["is_security_event"] is False
