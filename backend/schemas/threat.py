from pydantic import BaseModel
from typing import Optional, Dict, Any
from datetime import datetime

class ThreatBase(BaseModel):
    threat_name: str
    threat_type: str
    severity: str
    description: Optional[str] = None
    source_ip: Optional[str] = None
    destination_ip: Optional[str] = None
    source_port: Optional[int] = None
    destination_port: Optional[int] = None
    protocol: Optional[str] = None
    confidence_score: float = 0.0
    detected_at: datetime
    threat_metadata: Optional[Dict[str, Any]] = None

class ThreatCreate(ThreatBase):
    pass

class ThreatUpdate(BaseModel):
    threat_name: Optional[str] = None
    threat_type: Optional[str] = None
    severity: Optional[str] = None
    description: Optional[str] = None
    confidence_score: Optional[float] = None
    is_resolved: Optional[bool] = None
    threat_metadata: Optional[Dict[str, Any]] = None

class ThreatResponse(ThreatBase):
    id: int
    created_by: int
    is_resolved: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
