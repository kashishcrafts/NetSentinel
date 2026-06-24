# NetSentinel Project Documentation

## Overview

NetSentinel is an enterprise-grade AI-Powered Network Intrusion Detection & Cyber Threat Visualizer system built with modern technologies.

## Technology Stack

### Backend
- **Framework**: FastAPI 0.104.1
- **Server**: Uvicorn 0.24.0
- **Database**: PostgreSQL 15
- **ORM**: SQLAlchemy 2.0.23
- **Authentication**: JWT (python-jose)
- **Password Hashing**: bcrypt (passlib)
- **Validation**: Pydantic 2.5.0

### Frontend
- React (to be implemented)
- D3.js for threat visualization
- Redux for state management

### ML Models
- Threat detection models
- Anomaly detection
- Pattern recognition

## Project Structure

```
NetSentinel/
├── backend/                 # FastAPI Application
│   ├── api/                # API route handlers
│   ├── core/               # Core functionality
│   ├── models/             # SQLAlchemy ORM models
│   ├── schemas/            # Pydantic validation schemas
│   ├── services/           # Business logic
│   ├── utils/              # Utility functions
│   ├── main.py             # Application entry point
│   └── README.md           # Backend documentation
├── frontend/               # React Frontend (to be implemented)
├── ml_models/              # ML Models (to be implemented)
├── database/               # Database scripts
├── datasets/               # Sample data and datasets
├── docs/                   # Documentation
├── requirements.txt        # Python dependencies
├── .env                    # Environment configuration
├── .env.example            # Example environment configuration
├── .gitignore              # Git ignore rules
├── Dockerfile              # Docker configuration
├── docker-compose.yml      # Docker Compose setup
├── init_db.py              # Database initialization script
└── API_EXAMPLES.md         # API usage examples
```

## Key Features

### 1. User Management
- User registration and authentication
- JWT-based session management
- Role-based access control (RBAC)
- User profile management

### 2. Threat Detection
- Real-time threat detection
- Threat classification by type and severity
- Threat history and tracking
- Threat resolution workflow

### 3. Alert System
- Automated alert generation
- Alert prioritization
- Alert assignment to analysts
- Alert lifecycle management
- Unread alert tracking

### 4. Reporting
- Comprehensive threat reports
- Customizable report types
- Report generation and storage
- Multi-format export (JSON, PDF, CSV)

### 5. Security Features
- JWT authentication
- Password hashing with bcrypt
- Role-based access control
- Secure database connections
- CORS support

## Database Schema

### Users Table
```sql
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    hashed_password VARCHAR NOT NULL,
    role VARCHAR(50) DEFAULT 'viewer',
    is_active BOOLEAN DEFAULT TRUE,
    is_verified BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_login TIMESTAMP
);
```

### Threats Table
```sql
CREATE TABLE threats (
    id SERIAL PRIMARY KEY,
    threat_name VARCHAR(255) NOT NULL,
    threat_type VARCHAR(100) NOT NULL,
    severity VARCHAR(50) NOT NULL,
    description TEXT,
    source_ip VARCHAR(45),
    destination_ip VARCHAR(45),
    source_port INTEGER,
    destination_port INTEGER,
    protocol VARCHAR(20),
    confidence_score FLOAT DEFAULT 0.0,
    detected_at TIMESTAMP NOT NULL,
    created_by INTEGER NOT NULL REFERENCES users(id),
    metadata JSON,
    is_resolved BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### Alerts Table
```sql
CREATE TABLE alerts (
    id SERIAL PRIMARY KEY,
    threat_id INTEGER NOT NULL REFERENCES threats(id),
    alert_type VARCHAR(100) NOT NULL,
    status VARCHAR(50) DEFAULT 'open',
    priority INTEGER DEFAULT 0,
    message TEXT NOT NULL,
    details JSON,
    assigned_to INTEGER REFERENCES users(id),
    is_read BOOLEAN DEFAULT FALSE,
    created_by INTEGER NOT NULL REFERENCES users(id),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    resolved_at TIMESTAMP
);
```

### Reports Table
```sql
CREATE TABLE reports (
    id SERIAL PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    report_type VARCHAR(100) NOT NULL,
    content JSON NOT NULL,
    generated_by INTEGER NOT NULL REFERENCES users(id),
    threats_count INTEGER DEFAULT 0,
    alerts_count INTEGER DEFAULT 0,
    period_start TIMESTAMP NOT NULL,
    period_end TIMESTAMP NOT NULL,
    is_confidential BOOLEAN DEFAULT FALSE,
    format VARCHAR(50) DEFAULT 'json',
    file_path VARCHAR,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

## User Roles and Permissions

| Role | Permissions |
|------|-------------|
| Admin | CREATE, READ, UPDATE, DELETE, EXECUTE |
| Analyst | CREATE, READ, UPDATE |
| Operator | READ, UPDATE |
| Viewer | READ |

## API Endpoints Overview

### Authentication
- `POST /users/register` - Register new user
- `POST /users/login` - Authenticate user

### Users
- `GET /users` - List all users
- `GET /users/{id}` - Get user details
- `PUT /users/{id}` - Update user
- `DELETE /users/{id}` - Delete user

### Threats
- `GET /threats` - List threats
- `POST /threats` - Create threat
- `GET /threats/{id}` - Get threat details
- `PUT /threats/{id}` - Update threat
- `DELETE /threats/{id}` - Delete threat
- `GET /threats/severity/{severity}` - Filter by severity
- `GET /threats/type/{type}` - Filter by type
- `GET /threats/unresolved/list` - Get unresolved threats

### Alerts
- `GET /alerts` - List alerts
- `POST /alerts` - Create alert
- `GET /alerts/{id}` - Get alert details
- `PUT /alerts/{id}` - Update alert
- `DELETE /alerts/{id}` - Delete alert
- `GET /alerts/status/{status}` - Filter by status
- `GET /alerts/unread/list` - Get unread alerts
- `POST /alerts/{id}/read` - Mark as read

### Reports
- `GET /reports` - List reports
- `POST /reports` - Create report
- `GET /reports/{id}` - Get report details
- `PUT /reports/{id}` - Update report
- `DELETE /reports/{id}` - Delete report
- `GET /reports/type/{type}` - Filter by type

## Getting Started

### Installation
```bash
# Clone repository
git clone <repo-url>
cd NetSentinel

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Setup environment
cp .env.example .env
# Edit .env with your configuration

# Initialize database
python init_db.py

# Run application
cd backend
python -m uvicorn main:app --reload
```

### With Docker
```bash
docker-compose up -d
```

### API Documentation
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Development Guidelines

### Code Style
- Follow PEP 8
- Use type hints
- Write descriptive docstrings

### Testing
```bash
pytest
```

### Database Migrations
Handled through SQLAlchemy ORM with Base.metadata.create_all()

## Deployment

### Production Checklist
- [ ] Update SECRET_KEY in .env
- [ ] Configure DATABASE_URL for production database
- [ ] Set up SSL certificates
- [ ] Configure CORS origins
- [ ] Set up logging
- [ ] Configure monitoring
- [ ] Set up backup strategy

### Deployment Options
- Docker/Docker Compose
- Kubernetes
- AWS EC2
- GCP Compute Engine
- Azure App Service

## Security Considerations

1. **Authentication**: JWT tokens with expiration
2. **Authorization**: Role-based access control
3. **Encryption**: SSL/TLS for transport, bcrypt for passwords
4. **Database**: Connection pooling, SQL injection protection via ORM
5. **API Security**: CORS configuration, rate limiting (to be implemented)

## Future Enhancements

- [ ] WebSocket support for real-time alerts
- [ ] Machine learning-based threat detection
- [ ] Advanced visualization dashboard
- [ ] Threat intelligence integration
- [ ] Email/Slack notifications
- [ ] Two-factor authentication
- [ ] Audit logging
- [ ] API rate limiting
- [ ] GraphQL API
- [ ] Mobile app

## Troubleshooting

### Database Connection Issues
```bash
# Check PostgreSQL is running
# Verify DATABASE_URL in .env
# Check credentials
```

### Import Errors
```bash
# Reinstall dependencies
pip install -r requirements.txt --force-reinstall

# Check Python path
export PYTHONPATH="${PYTHONPATH}:/path/to/backend"
```

### Port Already in Use
```bash
# Change port in .env or use:
uvicorn main:app --port 8001
```

## Contributing

1. Create feature branch
2. Make changes
3. Run tests
4. Submit pull request

## Support

For issues and questions:
- Open GitHub issue
- Check documentation
- Review API examples

## License

MIT License - See LICENSE file for details

---

**Version**: 1.0.0  
**Last Updated**: January 2024
