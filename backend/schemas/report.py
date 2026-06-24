from pydantic import BaseModel
from typing import Optional, Dict, Any
from datetime import datetime

class ReportBase(BaseModel):
    title: str
    description: Optional[str] = None
    report_type: str
    content: Dict[str, Any]
    period_start: datetime
    period_end: datetime

class ReportCreate(ReportBase):
    pass

class ReportUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    content: Optional[Dict[str, Any]] = None
    is_confidential: Optional[bool] = None

class ReportResponse(ReportBase):
    id: int
    generated_by: int
    threats_count: int
    alerts_count: int
    is_confidential: bool
    format: str
    file_path: Optional[str] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
