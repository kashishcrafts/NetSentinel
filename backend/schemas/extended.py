from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime
from enum import Enum


class AlertStatusEnum(str, Enum):
    OPEN = "open"
    ASSIGNED = "assigned"
    INVESTIGATING = "investigating"
    ESCALATED = "escalated"
    RESOLVED = "resolved"
    CLOSED = "closed"


class AlertPriorityEnum(str, Enum):
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


class AlertCreate(BaseModel):
    alert_type: str
    title: str
    message: str
    priority: AlertPriorityEnum = AlertPriorityEnum.MEDIUM
    severity: str
    anomaly_score: Optional[float] = None
    risk_score: Optional[float] = None
    confidence: Optional[float] = None
    source_ip: Optional[str] = None
    destination_ip: Optional[str] = None
    protocol: Optional[str] = None
    threat_id: Optional[int] = None
    metadata: Optional[Dict[str, Any]] = None


class AlertUpdate(BaseModel):
    status: Optional[AlertStatusEnum] = None
    priority: Optional[AlertPriorityEnum] = None
    assigned_to: Optional[int] = None
    is_read: Optional[bool] = None


class AlertResponse(BaseModel):
    id: int
    alert_type: str
    title: str
    message: str
    status: str
    priority: str
    severity: str
    anomaly_score: Optional[float]
    risk_score: Optional[float]
    confidence: Optional[float]
    source_ip: Optional[str]
    destination_ip: Optional[str]
    protocol: Optional[str]
    threat_id: Optional[int]
    assigned_to: Optional[int]
    is_read: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class IncidentStatusEnum(str, Enum):
    NEW = "new"
    INVESTIGATING = "investigating"
    CONTAINMENT = "containment"
    ERADICATION = "eradication"
    RECOVERY = "recovery"
    CLOSED = "closed"


class IncidentCreate(BaseModel):
    title: str
    description: str
    severity: str
    risk_score: Optional[float] = None
    assigned_to: Optional[int] = None


class IncidentUpdate(BaseModel):
    status: Optional[IncidentStatusEnum] = None
    severity: Optional[str] = None
    assigned_to: Optional[int] = None


class IncidentResponse(BaseModel):
    id: int
    title: str
    description: str
    status: str
    severity: str
    risk_score: Optional[float]
    assigned_to: Optional[int]
    threat_count: int
    alert_count: int
    evidence_count: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class IOCTypeEnum(str, Enum):
    IP = "ip"
    DOMAIN = "domain"
    URL = "url"
    HASH = "hash"
    EMAIL = "email"
    FILE = "file"


class IOCCreate(BaseModel):
    ioc_type: IOCTypeEnum
    value: str
    description: Optional[str] = None
    reputation: float = 0.0
    risk_score: float = 0.0
    confidence: float = 0.0
    source: Optional[str] = None
    tags: Optional[List[str]] = None
    metadata: Optional[Dict[str, Any]] = None


class IOCResponse(BaseModel):
    id: int
    ioc_type: str
    value: str
    description: Optional[str]
    reputation: float
    risk_score: float
    confidence: float
    status: str
    source: Optional[str]
    tags: Optional[List[str]]
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class ThreatIntelligenceCreate(BaseModel):
    threat_name: str
    threat_actor: Optional[str] = None
    description: Optional[str] = None
    mitre_techniques: Optional[List[str]] = None
    mitre_tactics: Optional[List[str]] = None
    confidence: float = 0.0
    severity: str
    risk_score: float = 0.0
    source: Optional[str] = None
    malware_families: Optional[List[str]] = None


class ThreatIntelligenceResponse(BaseModel):
    id: int
    threat_name: str
    threat_actor: Optional[str]
    description: Optional[str]
    mitre_techniques: Optional[List[str]]
    mitre_tactics: Optional[List[str]]
    confidence: float
    severity: str
    risk_score: float
    source: Optional[str]
    malware_families: Optional[List[str]]
    created_at: datetime

    class Config:
        from_attributes = True


class AuditLogResponse(BaseModel):
    id: int
    user_id: int
    action: str
    entity_type: str
    entity_id: int
    old_value: Optional[Dict[str, Any]]
    new_value: Optional[Dict[str, Any]]
    ip_address: Optional[str]
    timestamp: datetime

    class Config:
        from_attributes = True


class NetworkFlowCreate(BaseModel):
    source_ip: str
    destination_ip: str
    source_port: Optional[int] = None
    destination_port: Optional[int] = None
    protocol: str
    bytes_sent: int = 0
    bytes_received: int = 0
    packet_count: int = 0
    duration: float = 0.0
    anomaly_score: float = 0.0
    risk_score: float = 0.0


class NetworkFlowResponse(BaseModel):
    id: int
    source_ip: str
    destination_ip: str
    source_port: Optional[int]
    destination_port: Optional[int]
    protocol: str
    bytes_sent: int
    bytes_received: int
    packet_count: int
    duration: float
    anomaly_score: float
    risk_score: float
    timestamp: datetime

    class Config:
        from_attributes = True


class DetectionResult(BaseModel):
    anomaly_score: float = Field(..., ge=0, le=1)
    risk_score: float = Field(..., ge=0, le=100)
    severity: str
    confidence: float = Field(..., ge=0, le=100)
    detection_type: str
    model_used: str
    explanation: Optional[str] = None
    features_used: Optional[Dict[str, Any]] = None
