import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient
import os

from main import app
from core.database import Base, get_db


@pytest.fixture(scope="session")
def db_engine():
    """Create test database engine"""
    database_url = os.getenv("TEST_DATABASE_URL", "sqlite:///:memory:")
    if "sqlite" in database_url:
        engine = create_engine(database_url, connect_args={"check_same_thread": False})
    else:
        engine = create_engine(database_url)
    
    Base.metadata.create_all(bind=engine)
    yield engine
    Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function")
def db_session(db_engine):
    """Create database session for tests"""
    connection = db_engine.connect()
    transaction = connection.begin()
    Session = sessionmaker(bind=connection)
    session = Session()
    
    yield session
    
    session.close()
    transaction.rollback()
    connection.close()


@pytest.fixture
def client(db_session):
    """FastAPI test client"""
    def override_get_db():
        yield db_session
    
    app.dependency_overrides[get_db] = override_get_db
    
    with TestClient(app) as test_client:
        yield test_client
    
    app.dependency_overrides.clear()


@pytest.fixture
def auth_headers(client, db_session):
    """Generate authentication headers for tests"""
    from models.user import User
    from passlib.context import CryptContext
    
    pwd_context = CryptContext(schemes=["bcrypt"])
    
    test_user = User(
        email="test@example.com",
        username="testuser",
        hashed_password=pwd_context.hash("password123"),
        role="admin"
    )
    db_session.add(test_user)
    db_session.commit()
    
    response = client.post("/api/v1/auth/login", json={
        "email": "test@example.com",
        "password": "password123"
    })
    
    token = response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}
