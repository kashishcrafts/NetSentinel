from pydantic import BaseModel
from typing import Optional, Dict, Any
from datetime import datetime

class AlertBase(BaseModel):
    alert_type: str
    message: str
    priority: int = 0
    details: Optional[Dict[str, Any]] = None

class AlertCreate(AlertBase):
    threat_id: int

class AlertUpdate(BaseModel):
    status: Optional[str] = None
    priority: Optional[int] = None
    message: Optional[str] = None
    assigned_to: Optional[int] = None
    is_read: Optional[bool] = None
    details: Optional[Dict[str, Any]] = None

class AlertResponse(AlertBase):
    id: int
    threat_id: int
    status: str
    assigned_to: Optional[int] = None
    is_read: bool
    created_by: int
    created_at: datetime
    updated_at: datetime
    resolved_at: Optional[datetime] = None

    class Config:
        from_attributes = True
