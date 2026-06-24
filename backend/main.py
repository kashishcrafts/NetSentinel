import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException

from core.database import engine, Base, SessionLocal
from core.auth_middleware import SecurityHeadersMiddleware, AuthContextMiddleware
from core.exceptions import (
    http_exception_handler,
    validation_exception_handler,
    generic_exception_handler,
)
from core.config import ADMIN_EMAIL, ADMIN_PASSWORD
from core.security import hash_password
from core.rbac import Role
from models.user import User
from models.threat import Threat
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
    SystemSetting,
)
from api import users, threats, alerts, reports, enterprise, advanced
from services.settings_service import SettingsService

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="NetSentinel Enterprise API",
    version="2.0.0",
    description="Enterprise-grade AI-Powered Network Intrusion Detection, Threat Intelligence & Incident Response Platform",
    docs_url="/docs",
    openapi_url="/openapi.json",
)

app.add_middleware(SecurityHeadersMiddleware)
app.add_middleware(AuthContextMiddleware)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_exception_handler(Exception, generic_exception_handler)
app.add_exception_handler(RequestValidationError, validation_exception_handler)
app.add_exception_handler(StarletteHTTPException, http_exception_handler)

app.include_router(users.router)
app.include_router(threats.router)
app.include_router(alerts.router)
app.include_router(reports.router)
app.include_router(enterprise.router)
app.include_router(advanced.router)


def bootstrap_default_admin() -> None:
    """Ensure default SuperAdmin exists for first-run deployments."""
    db = SessionLocal()
    try:
        admin = db.query(User).filter(User.email == ADMIN_EMAIL).first()
        if not admin:
            admin = User(
                name="System Administrator",
                email=ADMIN_EMAIL,
                hashed_password=hash_password(ADMIN_PASSWORD),
                role=Role.SUPERADMIN.value,
                is_active=True,
                is_verified=True,
            )
            db.add(admin)
            db.commit()
        SettingsService.ensure_defaults(db)
    finally:
        db.close()


@app.on_event("startup")
def on_startup():
    if os.getenv("TESTING") != "1":
        bootstrap_default_admin()


@app.get("/")
def root():
    return {
        "message": "NetSentinel API Running",
        "version": "2.0.0",
        "status": "active",
    }


@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "database": "connected",
    }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
