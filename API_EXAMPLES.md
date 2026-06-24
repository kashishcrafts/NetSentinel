# NetSentinel API Examples

## Base URL
```
http://localhost:8000
```

## Authentication

All protected endpoints require JWT token in the Authorization header:
```
Authorization: Bearer {access_token}
```

## User Management

### Register User
```bash
curl -X POST http://localhost:8000/users/register \
  -H "Content-Type: application/json" \
  -d '{
    "name": "John Analyst",
    "email": "analyst@netsentinel.local",
    "password": "secure_password_123",
    "role": "analyst"
  }'
```

### Login
```bash
curl -X POST http://localhost:8000/users/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "admin@netsentinel.local",
    "password": "admin123456"
  }'
```

Response:
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "user": {
    "id": 1,
    "name": "Administrator",
    "email": "admin@netsentinel.local",
    "role": "admin",
    "is_active": true,
    "is_verified": true,
    "created_at": "2024-01-15T10:30:00",
    "updated_at": "2024-01-15T10:30:00",
    "last_login": null
  }
}
```

### Get All Users
```bash
curl -X GET http://localhost:8000/users \
  -H "Authorization: Bearer {access_token}"
```

### Get User by ID
```bash
curl -X GET http://localhost:8000/users/1 \
  -H "Authorization: Bearer {access_token}"
```

### Update User
```bash
curl -X PUT http://localhost:8000/users/2 \
  -H "Authorization: Bearer {access_token}" \
  -H "Content-Type: application/json" \
  -d '{
    "role": "analyst",
    "is_active": true
  }'
```

## Threat Management

### Create Threat
```bash
curl -X POST http://localhost:8000/threats \
  -H "Authorization: Bearer {access_token}" \
  -H "Content-Type: application/json" \
  -d '{
    "threat_name": "SQL Injection Attack",
    "threat_type": "injection",
    "severity": "critical",
    "description": "Detected SQL injection attempt on API endpoint",
    "source_ip": "192.168.1.100",
    "destination_ip": "10.0.0.5",
    "source_port": 54321,
    "destination_port": 443,
    "protocol": "TCP",
    "confidence_score": 0.95,
    "detected_at": "2024-01-15T10:30:00",
    "metadata": {
      "payload": "SELECT * FROM users WHERE id=1 OR 1=1",
      "user_agent": "Mozilla/5.0..."
    }
  }'
```

### Get All Threats
```bash
curl -X GET http://localhost:8000/threats?skip=0&limit=10 \
  -H "Authorization: Bearer {access_token}"
```

### Get Threats by Severity
```bash
curl -X GET http://localhost:8000/threats/severity/critical \
  -H "Authorization: Bearer {access_token}"
```

### Get Unresolved Threats
```bash
curl -X GET http://localhost:8000/threats/unresolved/list \
  -H "Authorization: Bearer {access_token}"
```

### Update Threat
```bash
curl -X PUT http://localhost:8000/threats/1 \
  -H "Authorization: Bearer {access_token}" \
  -H "Content-Type: application/json" \
  -d '{
    "is_resolved": true,
    "severity": "medium"
  }'
```

## Alert Management

### Create Alert
```bash
curl -X POST http://localhost:8000/alerts \
  -H "Authorization: Bearer {access_token}" \
  -H "Content-Type: application/json" \
  -d '{
    "threat_id": 1,
    "alert_type": "security_event",
    "message": "Critical threat detected",
    "priority": 10,
    "details": {
      "action_required": true,
      "escalation": "immediate"
    }
  }'
```

### Get Unread Alerts
```bash
curl -X GET http://localhost:8000/alerts/unread/list \
  -H "Authorization: Bearer {access_token}"
```

### Get Alerts by Status
```bash
curl -X GET http://localhost:8000/alerts/status/open \
  -H "Authorization: Bearer {access_token}"
```

### Mark Alert as Read
```bash
curl -X POST http://localhost:8000/alerts/1/read \
  -H "Authorization: Bearer {access_token}"
```

### Update Alert
```bash
curl -X PUT http://localhost:8000/alerts/1 \
  -H "Authorization: Bearer {access_token}" \
  -H "Content-Type: application/json" \
  -d '{
    "status": "acknowledged",
    "assigned_to": 2
  }'
```

## Report Management

### Create Report
```bash
curl -X POST http://localhost:8000/reports \
  -H "Authorization: Bearer {access_token}" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Daily Security Report",
    "description": "Daily threat analysis report",
    "report_type": "summary",
    "content": {
      "total_threats": 42,
      "critical_threats": 5,
      "resolved": 35
    },
    "period_start": "2024-01-15T00:00:00",
    "period_end": "2024-01-15T23:59:59"
  }'
```

### Get All Reports
```bash
curl -X GET http://localhost:8000/reports \
  -H "Authorization: Bearer {access_token}"
```

### Get Reports by Type
```bash
curl -X GET http://localhost:8000/reports/type/detailed \
  -H "Authorization: Bearer {access_token}"
```

## Error Responses

### 401 Unauthorized
```json
{
  "detail": "Not authenticated"
}
```

### 403 Forbidden
```json
{
  "detail": "Insufficient permissions"
}
```

### 404 Not Found
```json
{
  "detail": "Resource not found"
}
```

### 422 Validation Error
```json
{
  "detail": [
    {
      "loc": ["body", "email"],
      "msg": "invalid email format",
      "type": "value_error.email"
    }
  ]
}
```
