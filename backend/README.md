# NetSentinel Backend API

Enterprise-grade AI-Powered Network Intrusion & Cyber Threat Visualizer

## Features

- **FastAPI** - Modern, fast web framework for building APIs
- **SQLAlchemy** - SQL toolkit and Object-Relational Mapping
- **PostgreSQL** - Powerful, open-source relational database
- **JWT Authentication** - Secure token-based authentication
- **Password Hashing** - Bcrypt-based password hashing with passlib
- **Role-Based Access Control (RBAC)** - Fine-grained permission management
- **Comprehensive API** - Full CRUD operations for Threats, Alerts, Reports, and Users

## Project Structure

```
backend/
├── api/                  # API routers
│   ├── users.py         # User management endpoints
│   ├── threats.py       # Threat management endpoints
│   ├── alerts.py        # Alert management endpoints
│   └── reports.py       # Report management endpoints
├── core/                # Core functionality
│   ├── config.py        # Configuration from environment
│   ├── database.py      # Database setup and session management
│   ├── security.py      # JWT and password utilities
│   ├── rbac.py          # Role-based access control
│   └── auth_middleware.py # Authentication middleware
├── models/              # SQLAlchemy ORM models
│   ├── user.py          # User model
│   ├── threat.py        # Threat model
│   ├── alert.py         # Alert model
│   └── report.py        # Report model
├── schemas/             # Pydantic validation schemas
│   ├── user.py          # User schemas
│   ├── threat.py        # Threat schemas
│   ├── alert.py         # Alert schemas
│   └── report.py        # Report schemas
├── services/            # Business logic layer
│   ├── user_service.py      # User business logic
│   ├── threat_service.py    # Threat business logic
│   ├── alert_service.py     # Alert business logic
│   └── report_service.py    # Report business logic
└── main.py              # Application entry point
```

## Installation

### Prerequisites

- Python 3.8+
- PostgreSQL 12+
- pip or poetry

### Setup

1. **Clone the repository**

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r ../requirements.txt
   ```

4. **Configure environment**
   ```bash
   cp ../.env.example ../.env
   # Edit .env with your database credentials
   ```

5. **Initialize database**
   ```bash
   python ../init_db.py
   ```

6. **Run the application**
   ```bash
   python -m uvicorn main:app --reload
   ```

   The API will be available at `http://localhost:8000`

## API Endpoints

### Authentication
- `POST /users/register` - Register new user
- `POST /users/login` - Login and get access token

### Users
- `GET /users` - Get all users
- `GET /users/{user_id}` - Get user by ID
- `GET /users/me` - Get current user profile
- `PUT /users/{user_id}` - Update user
- `DELETE /users/{user_id}` - Delete user

### Threats
- `GET /threats` - Get all threats
- `GET /threats/{threat_id}` - Get threat by ID
- `GET /threats/severity/{severity}` - Get threats by severity
- `GET /threats/type/{threat_type}` - Get threats by type
- `GET /threats/unresolved/list` - Get unresolved threats
- `POST /threats` - Create threat
- `PUT /threats/{threat_id}` - Update threat
- `DELETE /threats/{threat_id}` - Delete threat

### Alerts
- `GET /alerts` - Get all alerts
- `GET /alerts/{alert_id}` - Get alert by ID
- `GET /alerts/status/{status}` - Get alerts by status
- `GET /alerts/threat/{threat_id}` - Get alerts by threat
- `GET /alerts/unread/list` - Get unread alerts
- `POST /alerts` - Create alert
- `PUT /alerts/{alert_id}` - Update alert
- `POST /alerts/{alert_id}/read` - Mark alert as read
- `DELETE /alerts/{alert_id}` - Delete alert

### Reports
- `GET /reports` - Get all reports
- `GET /reports/{report_id}` - Get report by ID
- `GET /reports/type/{report_type}` - Get reports by type
- `GET /reports/user/{user_id}` - Get reports by user
- `POST /reports` - Create report
- `PUT /reports/{report_id}` - Update report
- `DELETE /reports/{report_id}` - Delete report

## User Roles

- **admin** - Full system access
- **analyst** - Read, create, update threats and alerts
- **operator** - Read and update alerts
- **viewer** - Read-only access

## API Documentation

Once the server is running, visit:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## Environment Variables

```
DATABASE_URL=postgresql://user:password@localhost:5432/netsentinel_db
SECRET_KEY=your-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
ADMIN_EMAIL=admin@netsentinel.local
ADMIN_PASSWORD=admin123456
```

## Development

### Running Tests
```bash
pytest
```

### Code Quality
```bash
flake8 .
black .
mypy .
```

## License

MIT
