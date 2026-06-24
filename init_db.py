#!/usr/bin/env python3
"""Database initialization script."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent / "backend"))

from core.database import SessionLocal, engine, Base
from models.user import User
from core.security import hash_password
from core.config import ADMIN_EMAIL, ADMIN_PASSWORD

def init_db():
    """Initialize database with tables and admin user."""
    
    Base.metadata.create_all(bind=engine)
    print("✓ Database tables created successfully")
    
    db = SessionLocal()
    
    try:
        admin_user = db.query(User).filter(User.email == ADMIN_EMAIL).first()
        
        if not admin_user:
            admin_user = User(
                name="Administrator",
                email=ADMIN_EMAIL,
                hashed_password=hash_password(ADMIN_PASSWORD),
                role="admin",
                is_active=True,
                is_verified=True
            )
            db.add(admin_user)
            db.commit()
            print(f"✓ Admin user created: {ADMIN_EMAIL}")
        else:
            print(f"✓ Admin user already exists: {ADMIN_EMAIL}")
    
    except Exception as e:
        db.rollback()
        print(f"✗ Error creating admin user: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    init_db()
    print("✓ Database initialization completed")
