import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from core.database import engine, Base
from models.user import User
from models.threat import Threat
from models.alert import Alert
from models.report import Report
from models.extended import (
    Alert as ExtendedAlert,
    Incident,
    IOC,
    ThreatIntelligence,
    AuditLog,
    NetworkFlow,
    ModelVersion,
    MitreMapping,
)
from api import users, threats, alerts, reports, enterprise, advanced

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="NetSentinel Enterprise API",
    version="2.0.0",
    description="Enterprise-grade AI-Powered Network Intrusion Detection, Threat Intelligence & Incident Response Platform",
    docs_url="/docs",
    openapi_url="/openapi.json",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(users.router)
app.include_router(threats.router)
app.include_router(alerts.router)
app.include_router(reports.router)
app.include_router(enterprise.router)
app.include_router(advanced.router)

@app.get("/")
def root():
    return {
        "message": "NetSentinel API Running",
        "version": "1.0.0",
        "status": "active"
    }

@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "database": "connected"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)