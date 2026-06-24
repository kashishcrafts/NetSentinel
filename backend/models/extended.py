from sqlalchemy import Column, Integer, String, Float, DateTime, Text, Boolean, ForeignKey, JSON, Enum, Index
from sqlalchemy.orm import relationship
from datetime import datetime
import enum
from core.database import Base


class AlertStatus(str, enum.Enum):
    OPEN = "open"
    ASSIGNED = "assigned"
    INVESTIGATING = "investigating"
    ESCALATED = "escalated"
    RESOLVED = "resolved"
    CLOSED = "closed"


class AlertPriority(str, enum.Enum):
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


class IncidentStatus(str, enum.Enum):
    NEW = "new"
    INVESTIGATING = "investigating"
    CONTAINMENT = "containment"
    ERADICATION = "eradication"
    RECOVERY = "recovery"
    CLOSED = "closed"


class IOCType(str, enum.Enum):
    IP = "ip"
    DOMAIN = "domain"
    URL = "url"
    HASH = "hash"
    EMAIL = "email"
    FILE = "file"


class ThreatActorLevel(str, enum.Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class Alert(Base):
    __tablename__ = "alerts"
    __table_args__ = (
        Index("idx_alert_status", "status"),
        Index("idx_alert_created", "created_at"),
        Index("idx_alert_user", "assigned_to"),
    )

    id = Column(Integer, primary_key=True)
    alert_type = Column(String(255), nullable=False)
    title = Column(String(500), nullable=False)
    message = Column(Text, nullable=False)
    status = Column(Enum(AlertStatus), default=AlertStatus.OPEN)
    priority = Column(Enum(AlertPriority), default=AlertPriority.MEDIUM)
    severity = Column(String(50), nullable=False)
    anomaly_score = Column(Float, nullable=True)
    risk_score = Column(Float, nullable=True)
    confidence = Column(Float, nullable=True)
    source_ip = Column(String(45), nullable=True)
    destination_ip = Column(String(45), nullable=True)
    protocol = Column(String(50), nullable=True)
    threat_id = Column(Integer, ForeignKey("threats.id"), nullable=True)
    incident_id = Column(Integer, ForeignKey("incidents.id"), nullable=True)
    assigned_to = Column(Integer, ForeignKey("users.id"), nullable=True)
    is_read = Column(Boolean, default=False)
    metadata = Column(JSON, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    threat = relationship("Threat", back_populates="alerts")
    incident = relationship("Incident", back_populates="alerts")
    assigned_user = relationship("User", back_populates="assigned_alerts")
    comments = relationship("AlertComment", back_populates="alert", cascade="all, delete-orphan")


class AlertComment(Base):
    __tablename__ = "alert_comments"

    id = Column(Integer, primary_key=True)
    alert_id = Column(Integer, ForeignKey("alerts.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    comment = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    alert = relationship("Alert", back_populates="comments")
    user = relationship("User")


class Incident(Base):
    __tablename__ = "incidents"
    __table_args__ = (
        Index("idx_incident_status", "status"),
        Index("idx_incident_created", "created_at"),
    )

    id = Column(Integer, primary_key=True)
    title = Column(String(500), nullable=False)
    description = Column(Text, nullable=False)
    status = Column(Enum(IncidentStatus), default=IncidentStatus.NEW)
    severity = Column(String(50), nullable=False)
    risk_score = Column(Float, nullable=True)
    assigned_to = Column(Integer, ForeignKey("users.id"), nullable=True)
    threat_count = Column(Integer, default=0)
    alert_count = Column(Integer, default=0)
    evidence_count = Column(Integer, default=0)
    metadata = Column(JSON, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    assigned_user = relationship("User", back_populates="assigned_incidents")
    alerts = relationship("Alert", back_populates="incident")
    threats = relationship("Threat", back_populates="incident")
    comments = relationship("IncidentComment", back_populates="incident", cascade="all, delete-orphan")


class IncidentComment(Base):
    __tablename__ = "incident_comments"

    id = Column(Integer, primary_key=True)
    incident_id = Column(Integer, ForeignKey("incidents.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    comment = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    incident = relationship("Incident", back_populates="comments")
    user = relationship("User")


class IOC(Base):
    __tablename__ = "iocs"
    __table_args__ = (
        Index("idx_ioc_type", "ioc_type"),
        Index("idx_ioc_value", "value"),
        Index("idx_ioc_created", "created_at"),
    )

    id = Column(Integer, primary_key=True)
    ioc_type = Column(Enum(IOCType), nullable=False)
    value = Column(String(500), nullable=False, unique=True)
    description = Column(Text, nullable=True)
    reputation = Column(Float, default=0.0)
    risk_score = Column(Float, default=0.0)
    confidence = Column(Float, default=0.0)
    status = Column(String(50), default="active")
    source = Column(String(255), nullable=True)
    tags = Column(JSON, nullable=True)
    metadata = Column(JSON, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class ThreatIntelligence(Base):
    __tablename__ = "threat_intelligence"
    __table_args__ = (
        Index("idx_ti_name", "threat_name"),
        Index("idx_ti_created", "created_at"),
    )

    id = Column(Integer, primary_key=True)
    threat_name = Column(String(255), nullable=False)
    threat_actor = Column(String(255), nullable=True)
    threat_actor_level = Column(Enum(ThreatActorLevel), nullable=True)
    description = Column(Text, nullable=True)
    mitre_techniques = Column(JSON, nullable=True)
    mitre_tactics = Column(JSON, nullable=True)
    kill_chain = Column(JSON, nullable=True)
    confidence = Column(Float, default=0.0)
    severity = Column(String(50), nullable=False)
    risk_score = Column(Float, default=0.0)
    source = Column(String(255), nullable=True)
    malware_families = Column(JSON, nullable=True)
    iocs = Column(JSON, nullable=True)
    metadata = Column(JSON, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class MitreMapping(Base):
    __tablename__ = "mitre_mappings"

    id = Column(Integer, primary_key=True)
    threat_id = Column(Integer, ForeignKey("threats.id"), nullable=True)
    tactic_id = Column(String(50), nullable=False)
    tactic_name = Column(String(255), nullable=False)
    technique_id = Column(String(50), nullable=False)
    technique_name = Column(String(255), nullable=False)
    subtechnique_id = Column(String(50), nullable=True)
    subtechnique_name = Column(String(255), nullable=True)
    metadata = Column(JSON, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)


class AuditLog(Base):
    __tablename__ = "audit_logs"
    __table_args__ = (
        Index("idx_audit_user", "user_id"),
        Index("idx_audit_timestamp", "timestamp"),
        Index("idx_audit_action", "action"),
    )

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    action = Column(String(100), nullable=False)
    entity_type = Column(String(100), nullable=False)
    entity_id = Column(Integer, nullable=False)
    old_value = Column(JSON, nullable=True)
    new_value = Column(JSON, nullable=True)
    ip_address = Column(String(45), nullable=True)
    user_agent = Column(String(500), nullable=True)
    timestamp = Column(DateTime, default=datetime.utcnow)


class NetworkFlow(Base):
    __tablename__ = "network_flows"
    __table_args__ = (
        Index("idx_flow_src_dst", "source_ip", "destination_ip"),
        Index("idx_flow_timestamp", "timestamp"),
    )

    id = Column(Integer, primary_key=True)
    source_ip = Column(String(45), nullable=False)
    destination_ip = Column(String(45), nullable=False)
    source_port = Column(Integer, nullable=True)
    destination_port = Column(Integer, nullable=True)
    protocol = Column(String(50), nullable=False)
    bytes_sent = Column(Integer, default=0)
    bytes_received = Column(Integer, default=0)
    packet_count = Column(Integer, default=0)
    duration = Column(Float, default=0.0)
    anomaly_score = Column(Float, default=0.0)
    risk_score = Column(Float, default=0.0)
    timestamp = Column(DateTime, default=datetime.utcnow)
    metadata = Column(JSON, nullable=True)


class ModelVersion(Base):
    __tablename__ = "model_versions"

    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    version = Column(String(50), nullable=False)
    model_type = Column(String(100), nullable=False)
    accuracy = Column(Float, nullable=True)
    precision = Column(Float, nullable=True)
    recall = Column(Float, nullable=True)
    f1_score = Column(Float, nullable=True)
    training_timestamp = Column(DateTime, default=datetime.utcnow)
    deployment_timestamp = Column(DateTime, nullable=True)
    is_active = Column(Boolean, default=False)
    metadata = Column(JSON, nullable=True)
