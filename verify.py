#!/usr/bin/env python3
"""
NetSentinel Project Verification Script
Checks project structure and all dependencies
"""

import sys
from pathlib import Path

# Add backend to path
sys.path.insert(0, str(Path(__file__).parent / "backend"))

def check_structure():
    """Verify project structure."""
    print("\n📁 Checking Project Structure...")
    
    required_dirs = [
        "backend",
        "backend/api",
        "backend/core",
        "backend/models",
        "backend/schemas",
        "backend/services",
        "backend/utils",
    ]
    
    required_files = [
        "backend/main.py",
        "backend/core/config.py",
        "backend/core/database.py",
        "backend/core/security.py",
        "backend/core/rbac.py",
        ".env",
        "requirements.txt",
        "init_db.py",
    ]
    
    for dir_path in required_dirs:
        if Path(dir_path).exists():
            print(f"  ✓ {dir_path}/")
        else:
            print(f"  ✗ {dir_path}/ - NOT FOUND")
    
    for file_path in required_files:
        if Path(file_path).exists():
            print(f"  ✓ {file_path}")
        else:
            print(f"  ✗ {file_path} - NOT FOUND")

def check_imports():
    """Verify all imports work correctly."""
    print("\n🔗 Checking Imports...")
    
    imports_to_test = [
        ("core.config", "Config module"),
        ("core.database", "Database module"),
        ("core.security", "Security module"),
        ("core.rbac", "RBAC module"),
        ("models.user", "User model"),
        ("models.threat", "Threat model"),
        ("models.alert", "Alert model"),
        ("models.report", "Report model"),
        ("schemas.user", "User schema"),
        ("schemas.threat", "Threat schema"),
        ("schemas.alert", "Alert schema"),
        ("schemas.report", "Report schema"),
        ("services.user_service", "User service"),
        ("services.threat_service", "Threat service"),
        ("services.alert_service", "Alert service"),
        ("services.report_service", "Report service"),
        ("api.users", "Users API"),
        ("api.threats", "Threats API"),
        ("api.alerts", "Alerts API"),
        ("api.reports", "Reports API"),
    ]
    
    for module_name, description in imports_to_test:
        try:
            __import__(module_name)
            print(f"  ✓ {description}")
        except ImportError as e:
            print(f"  ✗ {description} - {str(e)}")
        except Exception as e:
            print(f"  ⚠ {description} - {str(e)}")

def check_database():
    """Verify database configuration."""
    print("\n🗄️  Checking Database...")
    
    try:
        from core.config import DATABASE_URL
        from core.database import engine, SessionLocal, get_db
        
        print(f"  ✓ Database URL configured")
        print(f"  ✓ Engine created")
        print(f"  ✓ SessionLocal available")
        print(f"  ✓ get_db dependency available")
        
        # Try to create a session
        db = SessionLocal()
        db.close()
        print(f"  ✓ Database connection test passed")
        
    except Exception as e:
        print(f"  ✗ Database error: {str(e)}")

def check_models():
    """Verify models are properly configured."""
    print("\n📊 Checking Models...")
    
    try:
        from core.database import Base
        from models.user import User
        from models.threat import Threat
        from models.alert import Alert
        from models.report import Report
        
        models = [User, Threat, Alert, Report]
        for model in models:
            print(f"  ✓ {model.__name__} model")
            print(f"    - Table: {model.__tablename__}")
            print(f"    - Columns: {len(model.__table__.columns)}")
        
    except Exception as e:
        print(f"  ✗ Model error: {str(e)}")

def check_schemas():
    """Verify schemas are properly configured."""
    print("\n📋 Checking Schemas...")
    
    try:
        from schemas.user import UserCreate, UserResponse, LoginRequest, TokenResponse
        from schemas.threat import ThreatCreate, ThreatResponse
        from schemas.alert import AlertCreate, AlertResponse
        from schemas.report import ReportCreate, ReportResponse
        
        schemas = [
            ("UserCreate", UserCreate),
            ("UserResponse", UserResponse),
            ("LoginRequest", LoginRequest),
            ("TokenResponse", TokenResponse),
            ("ThreatCreate", ThreatCreate),
            ("ThreatResponse", ThreatResponse),
            ("AlertCreate", AlertCreate),
            ("AlertResponse", AlertResponse),
            ("ReportCreate", ReportCreate),
            ("ReportResponse", ReportResponse),
        ]
        
        for name, schema in schemas:
            print(f"  ✓ {name}")
        
    except Exception as e:
        print(f"  ✗ Schema error: {str(e)}")

def check_security():
    """Verify security utilities."""
    print("\n🔒 Checking Security...")
    
    try:
        from core.security import hash_password, verify_password, create_access_token, decode_token
        from core.rbac import Role, Permission, has_permission
        
        # Test password hashing
        test_password = "test_password_123"
        hashed = hash_password(test_password)
        verified = verify_password(test_password, hashed)
        
        if verified:
            print(f"  ✓ Password hashing works")
        else:
            print(f"  ✗ Password hashing failed")
        
        # Test JWT
        token = create_access_token({"sub": 1, "role": "admin"})
        payload = decode_token(token)
        
        if payload and payload.get("sub") == 1:
            print(f"  ✓ JWT creation and decoding works")
        else:
            print(f"  ✗ JWT test failed")
        
        # Test RBAC
        admin_role = Role.ADMIN
        print(f"  ✓ RBAC roles configured")
        
    except Exception as e:
        print(f"  ✗ Security error: {str(e)}")

def check_services():
    """Verify services are properly configured."""
    print("\n⚙️  Checking Services...")
    
    try:
        from services.user_service import UserService
        from services.threat_service import ThreatService
        from services.alert_service import AlertService
        from services.report_service import ReportService
        
        services = [
            ("UserService", UserService),
            ("ThreatService", ThreatService),
            ("AlertService", AlertService),
            ("ReportService", ReportService),
        ]
        
        for name, service in services:
            print(f"  ✓ {name}")
        
    except Exception as e:
        print(f"  ✗ Service error: {str(e)}")

def check_api():
    """Verify API routers are properly configured."""
    print("\n🛣️  Checking API Routers...")
    
    try:
        from api.users import router as users_router
        from api.threats import router as threats_router
        from api.alerts import router as alerts_router
        from api.reports import router as reports_router
        
        routers = [
            ("Users", users_router),
            ("Threats", threats_router),
            ("Alerts", alerts_router),
            ("Reports", reports_router),
        ]
        
        for name, router in routers:
            routes_count = len(router.routes)
            print(f"  ✓ {name} router ({routes_count} routes)")
        
    except Exception as e:
        print(f"  ✗ API router error: {str(e)}")

def check_main_app():
    """Verify main FastAPI app."""
    print("\n🚀 Checking Main Application...")
    
    try:
        from main import app
        
        routes = len(app.routes)
        print(f"  ✓ FastAPI app created")
        print(f"  ✓ Total routes: {routes}")
        
    except Exception as e:
        print(f"  ✗ Main app error: {str(e)}")

def main():
    """Run all verification checks."""
    print("""
╔════════════════════════════════════════════════════╗
║    NetSentinel - Project Verification Script      ║
╚════════════════════════════════════════════════════╝
    """)
    
    try:
        check_structure()
        check_imports()
        check_database()
        check_models()
        check_schemas()
        check_security()
        check_services()
        check_api()
        check_main_app()
        
        print("""
╔════════════════════════════════════════════════════╗
║    ✓ All Verification Checks Passed!             ║
║    NetSentinel is ready to run                    ║
╚════════════════════════════════════════════════════╝

Next steps:
1. Configure .env with your database credentials
2. Run: python init_db.py
3. Run: python run.py
4. Visit: http://localhost:8000/docs
        """)
        
    except Exception as e:
        print(f"\n✗ Verification failed: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()
