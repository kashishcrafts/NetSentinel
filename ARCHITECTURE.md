# NetSentinel Architecture

## System Overview

NetSentinel is designed as a distributed, scalable cyber defense platform with clear separation of concerns:

```
┌─────────────────────────────────────────────────────────────┐
│                    CLIENT LAYER                              │
│  ┌──────────────────────────────────────────────────────┐   │
│  │  React 19 Frontend (TypeScript)                       │   │
│  │  • Dashboard: Real-time threat metrics                │   │
│  │  • Alert Management: Create, escalate, assign         │   │
│  │  • Incident Response: Investigation workflows         │   │
│  │  • IOC Search: Query indicator reputation             │   │
│  │  • Threat Hunting: IP, domain, hash analysis          │   │
│  │  • MITRE Navigator: ATT&CK mapping visualization      │   │
│  └──────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
                           ↓ HTTP/WebSocket
┌─────────────────────────────────────────────────────────────┐
│                 API GATEWAY LAYER                            │
│  ┌──────────────────────────────────────────────────────┐   │
│  │  Nginx Reverse Proxy                                 │   │
│  │  • TLS termination (production)                      │   │
│  │  • Request routing (/api → Backend, /ws → WS)       │   │
│  │  • Load balancing                                    │   │
│  │  • Gzip compression                                  │   │
│  └──────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
                           ↓
┌─────────────────────────────────────────────────────────────┐
│                APPLICATION LAYER                             │
│  ┌──────────────────────────────────────────────────────┐   │
│  │  FastAPI Backend (Async Python)                      │   │
│  │  REST Endpoints:                                     │   │
│  │    /api/v1/alerts    - Alert lifecycle mgmt          │   │
│  │    /api/v1/incidents - Incident response             │   │
│  │    /api/v1/iocs      - Indicator management          │   │
│  │    /api/v1/threats   - Threat intelligence           │   │
│  │    /api/v1/mitre     - MITRE framework               │   │
│  │    /api/v1/audit-logs- Compliance audit             │   │
│  │    /api/v1/detection - ML detection pipeline         │   │
│  │  WebSocket Endpoints:                                │   │
│  │    /ws/live-threats  - Real-time threat stream       │   │
│  │    /ws/live-incidents- Active incidents stream       │   │
│  └──────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
                    ↓                   ↓
        ┌───────────────────┐  ┌──────────────────┐
        │  SERVICE LAYER    │  │   ML/DETECTION   │
        │                   │  │                  │
        │  Business Logic:  │  │  Feature Extract │
        │  • AlertService   │  │  Anomaly Detect  │
        │  • IncidentService│  │  Risk Scoring    │
        │  • IOCService     │  │  Explainability  │
        │  • ThreatService  │  │                  │
        │  • AuditService   │  │  Models:         │
        │                   │  │  • IsolationFst  │
        │                   │  │  • StdScaler     │
        │                   │  │  • [Future: LSTM]
        └───────────────────┘  └──────────────────┘
                    ↓                   ↓
        ┌───────────────────┐  ┌──────────────────┐
        │  NETWORK SENSOR   │  │  DATA LAYER      │
        │                   │  │                  │
        │  Packet Capture:  │  │  ORM Models:     │
        │  • Normalize      │  │  • Alert         │
        │  • Aggregate      │  │  • Incident      │
        │  • Buffer flows   │  │  • IOC           │
        │                   │  │  • Threat        │
        │  Flow Data:       │  │  • NetworkFlow   │
        │  • SrcIP/DstIP    │  │  • AuditLog      │
        │  • Ports/Proto    │  │  • MitreMapping  │
        │  • Byte counts    │  │                  │
        │  • Packet count   │  │  Relationships:  │
        │                   │  │  • FK references │
        │                   │  │  • JSON fields   │
        │                   │  │  • Indexes       │
        └───────────────────┘  └──────────────────┘
                    ↓                   ↓
        ┌───────────────────────────────────────────┐
        │           PERSISTENCE LAYER                │
        │                                            │
        │  PostgreSQL Database:                      │
        │  • Relational data (alerts, incidents)     │
        │  • JSON fields (metadata, tags)            │
        │  • Full-text search indexes                │
        │  • Foreign key constraints                 │
        │                                            │
        │  Redis Cache:                              │
        │  • Session storage                         │
        │  • Alert counters                          │
        │  • Rate limiting                           │
        │                                            │
        │  (Optional) Kafka:                         │
        │  • Stream network flows                    │
        │  • Event sourcing                          │
        └───────────────────────────────────────────┘
```

## Component Architecture

### Frontend (frontend/)
```
src/
├── pages/
│   ├── Login.tsx           - Authentication
│   ├── Dashboard.tsx       - Main metrics/overview
│   ├── Alerts.tsx          - Alert list + management
│   ├── Incidents.tsx       - Incident response
│   ├── IOCCenter.tsx       - Indicator search
│   ├── ThreatHunting.tsx   - Proactive hunting
│   ├── MITRECenter.tsx     - ATT&CK framework
│   ├── AuditLogs.tsx       - Compliance trail
│   ├── UserManagement.tsx  - RBAC administration
│   └── Settings.tsx        - Platform configuration
├── components/
│   ├── Sidebar.tsx         - Navigation menu
│   ├── Navbar.tsx          - Top navigation
│   ├── ProtectedRoute.tsx  - JWT guard
│   └── [...charts, tables] - UI components
├── services/
│   └── api.ts              - Axios HTTP client
├── hooks/
│   └── [custom hooks]
├── styles/
│   └── tailwind.config.js  - Cyber theme
└── App.tsx                 - Router + layout
```

### Backend (backend/)
```
├── main.py                 - FastAPI app + router setup
├── api/
│   ├── enterprise.py       - Alert, Incident, IOC, Threat endpoints
│   ├── advanced.py         - MITRE, Hunting, Detection, WebSocket
│   ├── auth.py             - Login, token endpoints
│   └── [routers]
├── services/
│   ├── alert_service.py    - Alert CRUD + lifecycle
│   ├── incident_service.py - Incident response
│   ├── ioc_service.py      - IOC management
│   ├── threat_intelligence_service.py - Threat tracking
│   └── audit_service.py    - Compliance logging
├── ml/
│   └── detection_engine.py - IsolationForest ensemble
├── network/
│   └── sensor.py           - Packet processing + flow aggregation
├── models/
│   ├── user.py             - User model
│   └── extended.py         - Alert, Incident, IOC, Threat models
├── schemas/
│   ├── user.py             - User DTOs
│   └── extended.py         - Pydantic validation schemas
└── core/
    ├── database.py         - SQLAlchemy setup + engine
    └── config.py           - Environment configuration
```

## Data Flow

### Alert Creation & Processing
```
1. Sensor/API → Packet Data
   ↓
2. Network Sensor → Normalize & Aggregate
   ↓
3. ML Detection → Feature Extraction → IsolationForest
   ↓
4. Risk Scoring → Confidence Calculation → Severity
   ↓
5. AlertService → Create Alert in DB
   ↓
6. AuditService → Log mutation
   ↓
7. WebSocket → Broadcast to connected clients
   ↓
8. Frontend → Display in Dashboard/Alerts page
```

### Threat Intelligence Enrichment
```
1. IOC Ingestion (API or external feed)
   ↓
2. IOCService → Deduplication & Storage
   ↓
3. ExternalAPI Integration (VirusTotal, AbuseIPDB)
   ↓
4. Reputation Update → Risk Score Calculation
   ↓
5. ThreatIntelligenceService → Link to threat actors
   ↓
6. MitreMapping → Link to ATT&CK techniques
   ↓
7. Alert Correlation → Find related alerts
   ↓
8. Dashboard Update → Visualization
```

## API Response Structure

All endpoints follow standardized response format:

### Success Response (200)
```json
{
  "success": true,
  "data": {...} or [{...}],
  "timestamp": "2024-01-01T12:00:00Z"
}
```

### Paginated Response
```json
{
  "success": true,
  "data": [{...}, {...}],
  "total": 150,
  "skip": 0,
  "limit": 50,
  "timestamp": "2024-01-01T12:00:00Z"
}
```

### Error Response (4xx/5xx)
```json
{
  "success": false,
  "error": "Error message",
  "code": "ERROR_CODE",
  "timestamp": "2024-01-01T12:00:00Z"
}
```

## Security Architecture

### Authentication Flow
```
1. User → POST /api/v1/auth/login (email + password)
   ↓
2. Backend → Verify credentials against bcrypt hash
   ↓
3. Backend → Generate JWT token (HS256)
   ↓
4. Client → Store token in localStorage
   ↓
5. Client → Include "Authorization: Bearer {token}" in all requests
   ↓
6. Backend → Verify token via dependency injection
   ↓
7. Extract user_id from token claims
   ↓
8. Return 401 if invalid/expired
```

### Authorization (Role-Based Access Control)
```
Roles:
- Super Admin    → Full access to all endpoints
- Admin          → Manage users, system config
- SOC Analyst    → Create/manage alerts, view all data
- Threat Hunter  → Threat hunting, IOC search
- Incident Responder → Full incident lifecycle
- Viewer         → Read-only access

Implementation:
- Middleware checks role in JWT claims
- Endpoint decorators enforce minimum role
- Field-level filtering in responses
```

## Deployment Architecture

### Development (Docker Compose)
```
Host Machine
├── Frontend Service (localhost:80)
│   └── Nginx container
├── Backend Service (localhost:8001)
│   └── FastAPI container
├── PostgreSQL (localhost:5432)
│   └── DB container
└── Redis (localhost:6379)
    └── Cache container
```

### Production (Kubernetes Ready)
```
Load Balancer
├── Frontend Pods (replicas=3)
│   └── Nginx + Static files
├── API Pods (replicas=5)
│   └── FastAPI + Workers
├── Database Pods
│   └── PostgreSQL HA + Replication
├── Cache Pods
│   └── Redis Cluster
└── Message Queue Pods
    └── Kafka Cluster
```

## Monitoring & Observability

### Metrics Exposed
- Application: Alert count, incident count, detection accuracy
- Infrastructure: CPU, memory, disk, network
- Database: Connection pool, query performance, replication lag
- API: Request rate, latency, error rate, response size

### Logging Strategy
- Application logs → stdout (container friendly)
- Access logs → Nginx access.log
- Error logs → Structured JSON logs with context
- Audit logs → Database (compliance requirement)

## Performance Considerations

### Caching Strategy
- Alert summaries cached in Redis (5min TTL)
- Threat intelligence cached (24hr TTL)
- User sessions cached
- Frequently accessed IOCs cached

### Database Optimization
- Indexes on (status, created_at, user_id, source_ip, destination_ip)
- Partitioning for large tables (alerts, network_flows)
- Connection pooling (20 connections default)
- Query optimization for common filters

### ML Model Performance
- Feature extraction: ~10ms per flow
- Anomaly detection: ~50ms batch (100 flows)
- Risk scoring: ~5ms per alert
- Ensemble voting: negligible overhead

## Scalability

### Horizontal Scaling
- Stateless API servers (load balanced)
- Shared PostgreSQL database
- Distributed Redis cache
- Message queue for async jobs

### Vertical Scaling
- Increase database connection pool
- Increase ML model batch size
- Adjust Nginx worker processes
- Increase backend uvicorn workers

### Future Enhancements
- Graph database (Neo4j) for relationship analysis
- Time-series database (InfluxDB) for metrics
- Document store (Elasticsearch) for logs
- Message queue (Kafka) for event streaming
