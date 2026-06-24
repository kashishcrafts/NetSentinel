from sqlalchemy import Column, Integer, String, DateTime, Float, ForeignKey, JSON, Boolean
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from core.database import Base

class Threat(Base):
    __tablename__ = "threats"

    id = Column(Integer, primary_key=True, index=True)
    threat_name = Column(String(255), nullable=False, index=True)
    threat_type = Column(String(100), nullable=False)
    severity = Column(String(50), nullable=False)  # critical, high, medium, low
    description = Column(String, nullable=True)
    source_ip = Column(String(45), nullable=True)
    destination_ip = Column(String(45), nullable=True)
    source_port = Column(Integer, nullable=True)
    destination_port = Column(Integer, nullable=True)
    protocol = Column(String(20), nullable=True)
    confidence_score = Column(Float, default=0.0, nullable=False)
    detected_at = Column(DateTime, nullable=False)
    created_by = Column(Integer, ForeignKey("users.id"), nullable=False)
    threat_metadata = Column(JSON, nullable=True)
    is_resolved = Column(Boolean, default=False, nullable=False)
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)
    
    creator = relationship("User", foreign_keys=[created_by])
