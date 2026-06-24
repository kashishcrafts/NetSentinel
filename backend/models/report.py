from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, JSON, Boolean
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from core.database import Base

class Report(Base):
    __tablename__ = "reports"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    description = Column(String, nullable=True)
    report_type = Column(String(100), nullable=False)  # summary, detailed, trend, incident
    content = Column(JSON, nullable=False)
    generated_by = Column(Integer, ForeignKey("users.id"), nullable=False)
    threats_count = Column(Integer, default=0, nullable=False)
    alerts_count = Column(Integer, default=0, nullable=False)
    period_start = Column(DateTime, nullable=False)
    period_end = Column(DateTime, nullable=False)
    is_confidential = Column(Boolean, default=False, nullable=False)
    format = Column(String(50), default="json", nullable=False)  # json, pdf, csv, html
    file_path = Column(String, nullable=True)
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)
    
    generator = relationship("User", foreign_keys=[generated_by])
