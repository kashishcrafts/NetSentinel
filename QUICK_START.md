# NetSentinel - Quick Start Guide

## Installation (5 minutes)

### 1. Prerequisites
- Python 3.8+
- PostgreSQL 12+
- pip/poetry

### 2. Setup

```bash
# Clone and enter directory
cd NetSentinel

# Create virtual environment
python -m venv venv

# Activate (Windows: venv\Scripts\activate)
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env with your PostgreSQL credentials

# Initialize database
python init_db.py

# Start server
cd backend
python -m uvicorn main:app --reload
```

### 3. Access API
- **API**: http://localhost:8000
- **Docs**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## Default Admin Account

```
Email: admin@netsentinel.local
Password: admin123456
```

## Quick Test

### Login
```bash
curl -X POST http://localhost:8000/users/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "admin@netsentinel.local",
    "password": "admin123456"
  }'
```

### Create Threat
```bash
curl -X POST http://localhost:8000/threats \
  -H "Authorization: Bearer {YOUR_TOKEN}" \
  -H "Content-Type: application/json" \
  -d '{
    "threat_name": "Test Threat",
    "threat_type": "reconnaissance",
    "severity": "medium",
    "source_ip": "192.168.1.1",
    "destination_ip": "10.0.0.1",
    "confidence_score": 0.85,
    "detected_at": "2024-01-15T10:30:00"
  }'
```

## Docker Setup (Alternative)

```bash
docker-compose up -d
```

API will be available at http://localhost:8000

## Project Structure

```
backend/
├── api/              # Routes (users, threats, alerts, reports)
├── core/             # Config, database, security, auth
├── models/           # SQLAlchemy models
├── schemas/          # Pydantic schemas
├── services/         # Business logic
└── main.py           # App entry point
```

## Key Files

| File | Purpose |
|------|---------|
| `.env` | Environment configuration |
| `requirements.txt` | Python dependencies |
| `init_db.py` | Database initialization |
| `backend/main.py` | Application entry point |
| `Dockerfile` | Docker image |
| `docker-compose.yml` | Docker Compose setup |

## Features

✅ FastAPI + SQLAlchemy + PostgreSQL
✅ JWT Authentication
✅ Password Hashing (bcrypt)
✅ Role-Based Access Control
✅ User, Threat, Alert, Report management
✅ Comprehensive API documentation
✅ Docker ready

## API Routes

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/users/register` | Register new user |
| POST | `/users/login` | Login user |
| GET | `/threats` | List threats |
| POST | `/threats` | Create threat |
| GET | `/alerts` | List alerts |
| POST | `/alerts` | Create alert |
| GET | `/reports` | List reports |
| POST | `/reports` | Create report |

## Environment Variables

```
DATABASE_URL=postgresql://user:password@localhost:5432/netsentinel_db
SECRET_KEY=your-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
ADMIN_EMAIL=admin@netsentinel.local
ADMIN_PASSWORD=admin123456
```

## Troubleshooting

**Port 8000 already in use?**
```bash
cd backend
python -m uvicorn main:app --port 8001
```

**Database connection error?**
- Check PostgreSQL is running
- Verify DATABASE_URL in .env
- Test connection: `psql postgresql://user:password@localhost:5432/netsentinel_db`

**Import errors?**
```bash
pip install -r requirements.txt --force-reinstall
export PYTHONPATH="${PYTHONPATH}:$(pwd)/backend"
```

## Next Steps

1. ✅ Backend API running
2. ⏳ Set up frontend (React)
3. ⏳ Implement ML models
4. ⏳ Set up visualization dashboard
5. ⏳ Deploy to production

## Documentation

- [Full Documentation](./DOCUMENTATION.md)
- [API Examples](./API_EXAMPLES.md)
- [Backend README](./backend/README.md)

## Support

- Check logs: `tail -f backend.log`
- API docs: http://localhost:8000/docs
- Contact: [support email]

---

**Need help?** Check the DOCUMENTATION.md file for detailed information.
