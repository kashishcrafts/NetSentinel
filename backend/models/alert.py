from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey, JSON
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from core.database import Base

class Alert(Base):
    __tablename__ = "alerts"

    id = Column(Integer, primary_key=True, index=True)
    threat_id = Column(Integer, ForeignKey("threats.id"), nullable=False, index=True)
    alert_type = Column(String(100), nullable=False)
    status = Column(String(50), default="open", nullable=False)  # open, acknowledged, resolved, dismissed
    priority = Column(Integer, default=0, nullable=False)
    message = Column(String, nullable=False)
    details = Column(JSON, nullable=True)
    assigned_to = Column(Integer, ForeignKey("users.id"), nullable=True)
    is_read = Column(Boolean, default=False, nullable=False)
    created_by = Column(Integer, ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)
    resolved_at = Column(DateTime, nullable=True)
    
    threat = relationship("Threat", foreign_keys=[threat_id])
    assigned_user = relationship("User", foreign_keys=[assigned_to])
    creator = relationship("User", foreign_keys=[created_by])
