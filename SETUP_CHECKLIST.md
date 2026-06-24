# NetSentinel - Setup & Deployment Checklist

## Pre-Setup Requirements

- [ ] Python 3.8+ installed
- [ ] PostgreSQL 12+ installed and running
- [ ] pip or conda package manager
- [ ] Git (optional)
- [ ] 500MB+ disk space
- [ ] Port 8000 available (or configurable)
- [ ] Port 5432 available for PostgreSQL (or configure in .env)

---

## Installation Checklist

### Step 1: Environment Setup
- [ ] Navigate to NetSentinel project directory
- [ ] Create Python virtual environment: `python -m venv venv`
- [ ] Activate virtual environment:
  - Linux/Mac: `source venv/bin/activate`
  - Windows: `venv\Scripts\activate`
- [ ] Verify Python: `python --version` (should be 3.8+)
- [ ] Upgrade pip: `pip install --upgrade pip`

### Step 2: Dependencies Installation
- [ ] Install requirements: `pip install -r requirements.txt`
- [ ] Verify installations: `pip list`
- [ ] Check for any warnings or errors

### Step 3: Environment Configuration
- [ ] Copy environment template: `cp .env.example .env`
- [ ] Edit `.env` with your configuration:
  - [ ] Set DATABASE_URL (PostgreSQL connection string)
  - [ ] Verify SECRET_KEY (or generate new one for production)
  - [ ] Set ADMIN_EMAIL (if different)
  - [ ] Set ADMIN_PASSWORD (change from default)
- [ ] Verify .env file is in project root (not in backend/)

### Step 4: Database Setup
- [ ] Start PostgreSQL service
- [ ] Verify PostgreSQL is running: `psql --version`
- [ ] Test database connection using .env credentials
- [ ] Create database (if not auto-created):
  - `psql -U postgres`
  - `CREATE DATABASE netsentinel_db;`
- [ ] Initialize database: `python init_db.py`
- [ ] Verify tables created:
  ```sql
  psql -d netsentinel_db
  \dt  -- list tables
  ```

### Step 5: Project Verification
- [ ] Run verification script: `python verify.py`
- [ ] Verify all checks pass (green ✓)
- [ ] Review verify.py output for any warnings

---

## Launch Checklist

### Step 1: Start the Application
Choose ONE method:

**Method 1: Direct Python (Recommended)**
- [ ] Navigate to project root
- [ ] Run: `python run.py`
- [ ] Wait for: "Uvicorn running on http://0.0.0.0:8000"

**Method 2: Windows Batch File**
- [ ] Double-click: `start.bat`
- [ ] Wait for server to start

**Method 3: Unix Shell Script**
- [ ] Make executable: `chmod +x start.sh`
- [ ] Run: `./start.sh`
- [ ] Wait for server to start

**Method 4: Make Command**
- [ ] Verify make installed
- [ ] Run: `make run`
- [ ] Wait for server to start

**Method 5: Docker**
- [ ] Verify Docker installed
- [ ] Run: `docker-compose up -d`
- [ ] Wait for containers to start

### Step 2: Verify Server is Running
- [ ] Check console shows: "Uvicorn running on http://0.0.0.0:8000"
- [ ] No errors in console output
- [ ] Server ready for requests

---

## Initial Testing Checklist

### Test 1: API Health Check
- [ ] Open terminal (new window/tab)
- [ ] Run: `curl http://localhost:8000/health`
- [ ] Should return: `{"status": "healthy", "database": "connected"}`
- [ ] Verify response includes "connected"

### Test 2: API Documentation
- [ ] Open browser
- [ ] Visit: `http://localhost:8000/docs`
- [ ] Verify Swagger UI loads
- [ ] See list of endpoints
- [ ] All 4 resource categories visible (Users, Threats, Alerts, Reports)

### Test 3: User Registration
- [ ] In Swagger UI, click "Users" section
- [ ] Click "POST /users/register" endpoint
- [ ] Click "Try it out"
- [ ] Enter test data:
  ```json
  {
    "name": "Test User",
    "email": "test@example.local",
    "password": "TestPassword123!",
    "role": "analyst"
  }
  ```
- [ ] Click "Execute"
- [ ] Verify: Status 201, user ID returned

### Test 4: Login
- [ ] Click "POST /users/login" endpoint
- [ ] Click "Try it out"
- [ ] Enter admin credentials:
  ```json
  {
    "email": "admin@netsentinel.local",
    "password": "admin123456"
  }
  ```
- [ ] Click "Execute"
- [ ] Verify: Status 200, access_token returned
- [ ] Copy access token

### Test 5: Authentication
- [ ] Click "GET /users" endpoint
- [ ] Click "Try it out"
- [ ] Scroll down to "Authorization"
- [ ] Click lock icon
- [ ] Paste token in "Bearer <token>" format
- [ ] Click "Authorize"
- [ ] Click "Execute"
- [ ] Verify: Status 200, users list returned

### Test 6: Create Threat
- [ ] Click "POST /threats" endpoint
- [ ] Click "Try it out"
- [ ] Authorize with bearer token
- [ ] Enter threat data:
  ```json
  {
    "threat_name": "Test SQL Injection",
    "threat_type": "injection",
    "severity": "high",
    "source_ip": "192.168.1.100",
    "destination_ip": "10.0.0.1",
    "confidence_score": 0.85,
    "detected_at": "2024-01-15T10:30:00"
  }
  ```
- [ ] Click "Execute"
- [ ] Verify: Status 201, threat ID returned

---

## Database Verification Checklist

### Check Tables Exist
- [ ] Connect to database: `psql -d netsentinel_db`
- [ ] List tables: `\dt`
- [ ] Verify tables present:
  - [ ] users
  - [ ] threats
  - [ ] alerts
  - [ ] reports
- [ ] Check users table: `SELECT * FROM users;`
- [ ] Verify admin user exists
- [ ] Exit: `\q`

### Check Data Integrity
- [ ] Verify users created during testing exist
- [ ] Verify threats/alerts created via API exist
- [ ] Check relationships (foreign keys):
  - [ ] Alert's threat_id matches threat record
  - [ ] Threat's created_by matches user record

---

## Production Preparation Checklist

### Security Hardening
- [ ] Change ADMIN_PASSWORD in .env to strong password
- [ ] Generate new SECRET_KEY:
  ```bash
  python -c "import secrets; print(secrets.token_urlsafe(32))"
  ```
- [ ] Update SECRET_KEY in .env
- [ ] Set CORS origins (change from "*" to specific domains)
- [ ] Enable SSL/TLS certificates
- [ ] Set environment variables securely (not in files)

### Performance Tuning
- [ ] Review database connection pool settings
- [ ] Configure uvicorn workers based on CPU cores
- [ ] Set up caching if needed
- [ ] Configure logging appropriately

### Deployment Options
- [ ] Choose deployment target:
  - [ ] Docker/Docker Swarm
  - [ ] Kubernetes
  - [ ] Traditional VPS (AWS, GCP, Azure)
  - [ ] Serverless (AWS Lambda, GCP Cloud Run)
- [ ] Set up CI/CD pipeline
- [ ] Configure backup strategy
- [ ] Set up monitoring and alerting

### Documentation
- [ ] Review README.md
- [ ] Update API_EXAMPLES.md with your endpoints
- [ ] Document custom configurations
- [ ] Document deployment procedures

---

## Troubleshooting Checklist

### Port Already in Use
- [ ] Verify port 8000 not in use: `netstat -an | grep 8000`
- [ ] Change PORT in .env
- [ ] Or kill process: `fuser -k 8000/tcp`
- [ ] Restart application

### Database Connection Fails
- [ ] Verify PostgreSQL running: `psql --version`
- [ ] Check DATABASE_URL in .env
- [ ] Test connection manually:
  ```bash
  psql postgresql://user:password@localhost:5432/netsentinel_db
  ```
- [ ] Verify credentials correct
- [ ] Verify database exists
- [ ] Check firewall rules

### Import Errors
- [ ] Reinstall dependencies:
  ```bash
  pip install -r requirements.txt --force-reinstall
  ```
- [ ] Verify Python path:
  ```bash
  export PYTHONPATH="${PYTHONPATH}:$(pwd)/backend"
  ```
- [ ] Check __init__.py files exist in all packages
- [ ] Run verification: `python verify.py`

### Slow Responses
- [ ] Check database queries
- [ ] Review database indexes
- [ ] Check PostgreSQL performance
- [ ] Monitor memory usage
- [ ] Check network latency

### Authentication Issues
- [ ] Verify token format: `Bearer <token>`
- [ ] Check token expiration time
- [ ] Regenerate admin user: `python init_db.py`
- [ ] Review security.py for JWT configuration

---

## Ongoing Maintenance Checklist

### Daily Tasks
- [ ] Monitor application logs
- [ ] Check database disk space
- [ ] Monitor API response times
- [ ] Check for error spikes

### Weekly Tasks
- [ ] Review security alerts
- [ ] Check backup status
- [ ] Review performance metrics
- [ ] Update threat intelligence feeds (when implemented)

### Monthly Tasks
- [ ] Security audit
- [ ] Performance optimization review
- [ ] Backup verification
- [ ] Update dependencies (if needed)

### Quarterly Tasks
- [ ] Full security assessment
- [ ] Database optimization
- [ ] Disaster recovery drill
- [ ] Load testing

---

## Success Indicators

✅ **Setup Successful When:**
- [ ] Python virtual environment activated
- [ ] All requirements installed without errors
- [ ] .env properly configured
- [ ] Database initialized with tables
- [ ] Verification script passes all checks
- [ ] Server starts without errors
- [ ] API documentation accessible
- [ ] Health check returns "connected"
- [ ] Can register and login
- [ ] Can create threats/alerts/reports
- [ ] Database contains created records

---

## Quick Reference Commands

```bash
# Activate virtual environment
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate      # Windows

# Install dependencies
pip install -r requirements.txt

# Verify installation
python verify.py

# Initialize database
python init_db.py

# Run application
python run.py

# Start with make
make setup
make run

# Start with Docker
docker-compose up -d

# Stop application
Ctrl+C  # In terminal
docker-compose down  # For Docker

# Run tests
pytest

# Format code
make format

# View logs
tail -f logs/app.log
```

---

## Support & Resources

### Documentation Files
- **QUICK_START.md** - Quick setup guide
- **DOCUMENTATION.md** - Full technical documentation
- **API_EXAMPLES.md** - API usage examples
- **PROJECT_INDEX.md** - File navigation guide

### Online Resources
- FastAPI docs: https://fastapi.tiangolo.com/
- SQLAlchemy docs: https://docs.sqlalchemy.org/
- PostgreSQL docs: https://www.postgresql.org/docs/

### Getting Help
1. Check error messages in console
2. Review DOCUMENTATION.md
3. Check API_EXAMPLES.md
4. Run `python verify.py`
5. Check application logs

---

## Final Notes

- This checklist is comprehensive but can be skipped if using Docker
- For Docker: Only complete "Pre-Setup" and "Docker" launch steps
- Always keep .env file secure and never commit to git
- Regularly backup your database
- Monitor application performance regularly
- Stay updated with security patches

---

**Version**: 1.0.0  
**Last Updated**: January 2024  
**Status**: Ready to Deploy ✅

**Good luck with your NetSentinel deployment! 🚀**
