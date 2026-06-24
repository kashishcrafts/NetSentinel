import pytest
from schemas.extended import AlertCreate, AlertPriorityEnum


@pytest.mark.integration
def test_create_alert_endpoint(client, auth_headers):
    """Test POST /api/v1/alerts endpoint"""
    alert_data = {
        "alert_type": "network_anomaly",
        "title": "Suspicious Activity",
        "message": "Detected anomaly",
        "priority": "HIGH",
        "severity": "high",
        "anomaly_score": 0.85,
        "risk_score": 75,
        "confidence": 0.92,
        "source_ip": "192.168.1.100",
        "destination_ip": "10.0.0.1",
        "protocol": "TCP"
    }
    
    response = client.post(
        "/api/v1/alerts",
        json=alert_data,
        headers=auth_headers
    )
    
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Suspicious Activity"


@pytest.mark.integration
def test_get_alerts_endpoint(client, auth_headers):
    """Test GET /api/v1/alerts endpoint"""
    response = client.get("/api/v1/alerts", headers=auth_headers)
    
    assert response.status_code == 200
    data = response.json()
    assert "data" in data
    assert isinstance(data["data"], list)


@pytest.mark.integration
def test_escalate_alert_endpoint(client, auth_headers):
    """Test POST /api/v1/alerts/{id}/escalate endpoint"""
    # First create an alert
    alert_data = {
        "alert_type": "test",
        "title": "Test",
        "message": "Test",
        "priority": "LOW",
        "severity": "low",
        "anomaly_score": 0.3,
        "risk_score": 20,
        "confidence": 0.7,
        "source_ip": "192.168.1.1",
        "destination_ip": "10.0.0.1",
        "protocol": "TCP"
    }
    
    create_response = client.post(
        "/api/v1/alerts",
        json=alert_data,
        headers=auth_headers
    )
    
    alert_id = create_response.json()["id"]
    
    # Escalate it
    response = client.post(
        f"/api/v1/alerts/{alert_id}/escalate",
        headers=auth_headers
    )
    
    assert response.status_code == 200
    data = response.json()
    assert data["priority"] == "CRITICAL"


@pytest.mark.integration
def test_unauthorized_access(client):
    """Test unauthorized access without auth headers"""
    response = client.get("/api/v1/alerts")
    assert response.status_code == 401


@pytest.mark.integration
def test_get_critical_count_endpoint(client, auth_headers):
    """Test GET /api/v1/alerts/critical-count endpoint"""
    response = client.get(
        "/api/v1/alerts/critical-count",
        headers=auth_headers
    )
    
    assert response.status_code == 200
    data = response.json()
    assert "count" in data or isinstance(data, dict)
