# Quick Start Guide

Get NetSentinel running in 5 minutes!

## Option 1: Docker Compose (Recommended)

### Prerequisites
- Docker Desktop (includes Docker and Docker Compose)
- 4GB RAM minimum, 8GB recommended

### Steps

1. **Clone and setup**
```bash
git clone https://github.com/your-org/netsentinel.git
cd netsentinel
cp .env.example .env
```

2. **Start all services**
```bash
docker-compose up -d
```

Wait 30-60 seconds for all services to start and become healthy.

3. **Initialize database**
```bash
docker-compose exec backend python scripts/seed_data.py
```

4. **Access the platform**
- **Frontend**: http://localhost
- **API Docs**: http://localhost:8001/docs
- **Database**: postgres://localhost:5432 (credentials in .env)

5. **Login with sample credentials**
```
Email: admin@netsentinel.io
Password: admin123
```

### Verify Everything Works

```bash
# Check all containers are running
docker-compose ps

# View backend logs
docker-compose logs -f backend

# Test API
curl http://localhost:8001/health
```

### Stop services
```bash
docker-compose down
```

---

## Option 2: Local Development

### Prerequisites
- Python 3.11+
- Node.js 20+
- PostgreSQL 15 (or use Docker for just DB)
- Git

### Backend Setup

1. **Create Python virtual environment**
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. **Install dependencies**
```bash
cd ..
pip install -r requirements.txt
```

3. **Setup database**
```bash
# Create PostgreSQL database
createdb netsentinel_db

# Run migrations
cd backend
alembic upgrade head

# Seed sample data
python scripts/seed_data.py
```

4. **Start backend server**
```bash
uvicorn main:app --reload --port 8001
```

Backend running at: http://localhost:8001

### Frontend Setup

In a new terminal:

```bash
cd frontend
npm install
npm run dev
```

Frontend running at: http://localhost:5173

---

## Common Tasks

### Add a New User
```bash
# Via API
curl -X POST http://localhost:8001/api/v1/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "newuser@example.com",
    "password": "password123",
    "username": "newuser",
    "role": "SOC Analyst"
  }'
```

### View API Documentation
```
http://localhost:8001/docs
```
Interactive Swagger UI with all endpoints and models.

### Run Tests
```bash
# Backend tests
cd backend
pytest tests -v

# Frontend tests
cd frontend
npm run test
```

### View Logs
```bash
# Docker logs
docker-compose logs backend
docker-compose logs frontend

# Or follow in real-time
docker-compose logs -f
```

### Reset Database
```bash
# Docker Compose
docker-compose down -v
docker-compose up -d
docker-compose exec backend python scripts/seed_data.py
```

---

## Troubleshooting

### Port Already in Use
```bash
# Find process using port
lsof -i :8001      # backend
lsof -i :3000      # frontend
lsof -i :5432      # database
lsof -i :6379      # redis

# Kill process
kill -9 <PID>
```

### Database Connection Error
```bash
# Check PostgreSQL is running
docker-compose ps postgres

# Or for local PostgreSQL
psql -U netsentinel -d netsentinel_db
```

### Frontend can't reach backend
- Ensure backend is running: `curl http://localhost:8001/health`
- Check CORS settings in backend/main.py
- Clear browser cache and restart dev server

### Module not found errors
```bash
# Reinstall dependencies
pip install -r requirements.txt --force-reinstall

# Or for frontend
cd frontend && npm install
```

---

## What's Next?

1. **Explore the Dashboard**: http://localhost
2. **Review API Docs**: http://localhost:8001/docs
3. **Create some test alerts**: Use Dashboard or API
4. **Read ARCHITECTURE.md**: Understand the system design
5. **Check DEPLOYMENT.md**: Production deployment options

---

## Architecture Overview

```
┌─────────────────────┐
│  React Frontend     │  http://localhost
├─────────────────────┤
│  FastAPI Backend    │  http://localhost:8001
├─────────────────────┤
│  PostgreSQL DB      │  localhost:5432
└─────────────────────┘
```

---

## Support

- 📖 Full Documentation: See DEPLOYMENT.md and ARCHITECTURE.md
- 🐛 Report Issues: GitHub Issues
- 💬 Community: GitHub Discussions
- 📧 Email: support@netsentinel.io

---

Happy threat hunting! 🛡️
