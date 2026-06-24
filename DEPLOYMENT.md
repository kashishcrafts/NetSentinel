# NetSentinel: Enterprise Cyber Defense Platform

[![Backend CI/CD](https://github.com/your-org/netsentinel/workflows/Backend%20CI%2FCD/badge.svg)](https://github.com/your-org/netsentinel/actions)
[![Frontend CI/CD](https://github.com/your-org/netsentinel/workflows/Frontend%20CI%2FCD/badge.svg)](https://github.com/your-org/netsentinel/actions)
[![Code Coverage](https://codecov.io/gh/your-org/netsentinel/branch/main/graph/badge.svg)](https://codecov.io/gh/your-org/netsentinel)

A complete enterprise-grade cyber defense platform comparable to Splunk Enterprise Security, IBM QRadar, and Microsoft Sentinel.

## Features

### Core Security Operations
- **Real-time Threat Detection**: ML-powered anomaly detection using Isolation Forest ensemble
- **Alert Management**: Full lifecycle alert management with prioritization and escalation
- **Incident Response**: Structured incident investigation and response workflows
- **Threat Intelligence**: IOC tracking, MITRE ATT&CK framework integration, threat actor intelligence
- **Audit Logging**: Comprehensive compliance and forensics audit trails

### Advanced Capabilities
- **Network Sensor**: Packet normalization, flow aggregation, real-time processing
- **ML Detection Pipeline**: Multi-stage detection with feature extraction and risk scoring
- **Threat Hunting**: Proactive search capabilities for IPs, domains, and file hashes
- **MITRE Framework**: Full ATT&CK mapping with tactic/technique/subtechnique hierarchy
- **Live Threat Streaming**: Real-time WebSocket connections for dashboard updates

### Enterprise Features
- **Role-Based Access Control**: 6 roles (Admin, Analyst, Hunter, Responder, Viewer)
- **User Management**: User provisioning and role assignment
- **API-First Architecture**: RESTful API with OpenAPI documentation
- **Containerized Deployment**: Docker + Docker Compose for rapid deployment
- **CI/CD Pipeline**: GitHub Actions for automated testing and deployment
- **Scalable Infrastructure**: Redis caching, Kafka message queues (optional)

## Tech Stack

### Backend
- **Framework**: FastAPI 0.104+ (async Python web framework)
- **Database**: PostgreSQL 15 with SQLAlchemy ORM
- **ML/Analytics**: scikit-learn, pandas, numpy, TensorFlow
- **Authentication**: JWT via python-jose
- **Real-time**: WebSockets with python-socketio

### Frontend
- **Framework**: React 19 with TypeScript 5
- **Styling**: Tailwind CSS 3.4 with custom cyber theme
- **UI Components**: Recharts for visualizations
- **Routing**: React Router DOM 6
- **HTTP Client**: Axios with JWT interceptor
- **Build**: Vite 5.4

### DevOps
- **Containerization**: Docker + Docker Compose
- **Web Server**: Nginx (reverse proxy + load balancing)
- **CI/CD**: GitHub Actions
- **Cache**: Redis 7
- **Message Queue**: Kafka (optional)

## Quick Start

### Prerequisites
- Docker & Docker Compose
- Node.js 20+ (for frontend development)
- Python 3.11+ (for backend development)
- Git

### Local Development

1. **Clone the repository**
```bash
git clone https://github.com/your-org/netsentinel.git
cd netsentinel
```

2. **Set up environment variables**
```bash
cp .env.example .env
# Edit .env with your configuration
```

3. **Start the stack with Docker Compose**
```bash
docker-compose up -d
```

4. **Initialize database**
```bash
docker-compose exec backend python -m alembic upgrade head
docker-compose exec backend python scripts/seed_data.py
```

5. **Access the application**
- Frontend: http://localhost
- Backend API: http://localhost:8001
- API Docs: http://localhost:8001/docs

### Development Setup (without Docker)

**Backend:**
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r ../requirements.txt
uvicorn main:app --reload --port 8001
```

**Frontend:**
```bash
cd frontend
npm install
npm run dev
```

## API Documentation

### Authentication
All endpoints require JWT bearer token in Authorization header:
```
Authorization: Bearer <token>
```

### Key Endpoints

#### Alerts
- `POST /api/v1/alerts` - Create alert
- `GET /api/v1/alerts` - List alerts (filterable)
- `PATCH /api/v1/alerts/{id}` - Update alert
- `POST /api/v1/alerts/{id}/escalate` - Escalate alert
- `POST /api/v1/alerts/{id}/assign/{user_id}` - Assign alert

#### Incidents
- `POST /api/v1/incidents` - Create incident
- `GET /api/v1/incidents` - List incidents
- `PATCH /api/v1/incidents/{id}` - Update incident
- `POST /api/v1/incidents/{id}/link-alert/{alert_id}` - Link alert

#### IOCs (Indicators of Compromise)
- `POST /api/v1/iocs` - Create IOC
- `GET /api/v1/iocs` - List IOCs
- `GET /api/v1/iocs/search` - Search IOCs
- `GET /api/v1/iocs/high-risk` - High risk IOCs

#### Threat Intelligence
- `POST /api/v1/threats` - Create threat
- `GET /api/v1/threats` - List threats
- `POST /api/v1/threats/{id}/mitre-map` - Map to MITRE framework

#### Detection
- `POST /api/v1/detection/analyze-flow` - Analyze single network flow
- `POST /api/v1/detection/batch-analyze` - Batch analysis
- `GET /api/v1/detection/sensor-stats` - Network sensor statistics

#### WebSockets
- `WS /ws/live-threats` - Stream critical threats
- `WS /ws/live-incidents` - Stream active incidents

### Full API Documentation
Available at `http://localhost:8001/docs` (Swagger UI)

## Database Schema

### Core Tables
- **users**: User accounts with role-based access
- **alerts**: Security alerts with full lifecycle tracking
- **incidents**: Incident response tracking
- **iocs**: Indicators of Compromise with reputation scoring
- **threats**: Threat intelligence data
- **audit_logs**: Comprehensive audit trail
- **network_flows**: Network flow data for analysis

### Relationships
- Alerts ↔ Incidents (many-to-one)
- Incidents ↔ Comments (one-to-many)
- Threats ↔ MITRE Mappings (one-to-many)
- IOCs ↔ Tags (one-to-many JSON)

## Testing

### Backend Tests
```bash
# Run all tests
pytest backend/tests -v

# Run specific test file
pytest backend/tests/test_alert_service.py -v

# Run with coverage
pytest backend/tests --cov=backend --cov-report=html
```

### Frontend Tests
```bash
cd frontend
npm run test
npm run test:coverage
```

## Deployment

### Using Docker Compose (Development)
```bash
docker-compose up -d
```

### Production Deployment
1. Set secure environment variables in `.env.production`
2. Update secrets in GitHub Actions:
   - `DOCKER_USERNAME`
   - `DOCKER_PASSWORD`
   - `DOCKER_REGISTRY`
   - `DEPLOY_HOST`
   - `DEPLOY_USER`
   - `DEPLOY_KEY`
3. Push to main branch to trigger deployment

### Database Migrations
```bash
# Inside backend container
alembic upgrade head
```

## Configuration

### Environment Variables
```
# Database
DATABASE_URL=postgresql://user:pass@localhost:5432/db
REDIS_URL=redis://localhost:6379

# Security
SECRET_KEY=your-secret-key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Server
ENVIRONMENT=development|production
DEBUG=true|false
```

## Architecture

```
┌─────────────────────────────────────────┐
│          Frontend (React/TS)            │
│  ├─ Pages (Dashboard, Alerts, etc.)     │
│  ├─ Components (Charts, Tables)         │
│  └─ Services (API client)               │
└────────┬────────────────────────────────┘
         │ HTTP/WebSocket
         ↓
┌─────────────────────────────────────────┐
│   Nginx (Reverse Proxy)                 │
│   ├─ Route /api → Backend               │
│   ├─ Route /ws → WebSocket              │
│   └─ Serve static → Frontend            │
└────────┬────────────────────────────────┘
         │
    ┌────┴─────┬──────────────────┐
    ↓          ↓                  ↓
┌────────┐ ┌───────────┐  ┌──────────────┐
│Backend │ │  Cache   │  │   Message   │
│(FastAPI)  │ (Redis)  │  │   Queue    │
│         │ └──────────┘  │  (Kafka)    │
│ Services:│              └──────────────┘
│ - Alerts │
│ - IOCs  │
│ - ML    │
│ - Network
└────┬────┘
     │
     ↓
┌──────────────────┐
│   PostgreSQL     │
│   (Database)     │
└──────────────────┘
```

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

MIT License - see LICENSE file for details

## Support

- 📧 Email: support@netsentinel.io
- 📚 Docs: https://docs.netsentinel.io
- 🐛 Issues: https://github.com/your-org/netsentinel/issues

## Roadmap

- [ ] Graph database for relationship analysis
- [ ] Advanced ML models (LSTM, Transformer)
- [ ] External threat intelligence integrations (VirusTotal, AbuseIPDB)
- [ ] Network topology visualization with D3.js
- [ ] PDF/Excel report generation
- [ ] Slack/Teams integration
- [ ] SIEM data source connectors
- [ ] Kubernetes deployment support

## Status

🟢 **Production Ready** - v2.0.0

---

Built with ❤️ for enterprise security teams
