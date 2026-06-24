import pytest
from services.alert_service import AlertService
from schemas.extended import AlertCreate, AlertStatusEnum, AlertPriorityEnum


@pytest.mark.unit
def test_create_alert(db_session):
    """Test alert creation"""
    alert_data = AlertCreate(
        alert_type="network_anomaly",
        title="Suspicious Network Activity",
        message="Detected unusual traffic pattern",
        priority=AlertPriorityEnum.HIGH,
        severity="high",
        anomaly_score=0.85,
        risk_score=75,
        confidence=0.92,
        source_ip="192.168.1.100",
        destination_ip="10.0.0.1",
        protocol="TCP",
        metadata={"port": 443}
    )
    
    service = AlertService()
    alert = service.create_alert(db_session, alert_data)
    
    assert alert.title == "Suspicious Network Activity"
    assert alert.priority == AlertPriorityEnum.HIGH
    assert alert.status == AlertStatusEnum.OPEN


@pytest.mark.unit
def test_get_alerts(db_session):
    """Test getting alerts with filtering"""
    service = AlertService()
    
    # Create multiple alerts
    for i in range(3):
        alert_data = AlertCreate(
            alert_type="test",
            title=f"Alert {i}",
            message=f"Test message {i}",
            priority=AlertPriorityEnum.MEDIUM,
            severity="medium",
            anomaly_score=0.5,
            risk_score=50,
            confidence=0.8,
            source_ip="192.168.1.1",
            destination_ip="10.0.0.1",
            protocol="TCP"
        )
        service.create_alert(db_session, alert_data)
    
    alerts = service.get_alerts(db_session)
    assert len(alerts) >= 3


@pytest.mark.unit
def test_escalate_alert(db_session):
    """Test alert escalation"""
    service = AlertService()
    
    alert_data = AlertCreate(
        alert_type="test",
        title="Test Alert",
        message="Test",
        priority=AlertPriorityEnum.LOW,
        severity="low",
        anomaly_score=0.3,
        risk_score=20,
        confidence=0.7,
        source_ip="192.168.1.1",
        destination_ip="10.0.0.1",
        protocol="TCP"
    )
    
    alert = service.create_alert(db_session, alert_data)
    escalated = service.escalate_alert(db_session, alert.id)
    
    assert escalated.priority == AlertPriorityEnum.CRITICAL
    assert escalated.status == AlertStatusEnum.ESCALATED


@pytest.mark.unit
def test_get_critical_alerts_count(db_session):
    """Test getting critical alerts count"""
    service = AlertService()
    
    alert_data = AlertCreate(
        alert_type="test",
        title="Critical Alert",
        message="Test",
        priority=AlertPriorityEnum.CRITICAL,
        severity="critical",
        anomaly_score=0.95,
        risk_score=95,
        confidence=0.99,
        source_ip="192.168.1.1",
        destination_ip="10.0.0.1",
        protocol="TCP"
    )
    
    service.create_alert(db_session, alert_data)
    count = service.get_critical_alerts_count(db_session)
    
    assert count >= 1
