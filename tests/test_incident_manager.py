from src.core.security.audit_logger import AuditLogger
from src.core.security.incident_manager import IncidentManager

def test_incident_manager_receives_critical_alert():
    # Setup
    logger = AuditLogger("logs/test_audit_incidents.log")
    manager = IncidentManager()
    logger.attach(manager)
    
    # Action
    logger.error("TestModule", "Database connection lost")
    logger.info("TestModule", "This should not trigger an incident")
    
    # Assert
    incidents = manager.get_recent_incidents()
    assert len(incidents) == 1
    assert incidents[0]["level"] == "ERROR"
    assert incidents[0]["module"] == "TestModule"
    
    # Cleanup
    logger.detach(manager)
