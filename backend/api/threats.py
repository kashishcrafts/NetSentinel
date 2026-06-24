from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from schemas.threat import ThreatCreate, ThreatResponse, ThreatUpdate
from services.threat_service import ThreatService
from core.database import get_db

router = APIRouter(prefix="/threats", tags=["Threats"])

@router.post("", response_model=ThreatResponse, status_code=status.HTTP_201_CREATED)
def create_threat(threat: ThreatCreate, created_by: int = 1, db: Session = Depends(get_db)):
    """Create a new threat."""
    new_threat = ThreatService.create_threat(db, threat, created_by)
    return new_threat

@router.get("/{threat_id}", response_model=ThreatResponse)
def get_threat(threat_id: int, db: Session = Depends(get_db)):
    """Get threat by ID."""
    threat = ThreatService.get_threat_by_id(db, threat_id)
    if not threat:
        raise HTTPException(status_code=404, detail="Threat not found")
    return threat

@router.get("", response_model=list[ThreatResponse])
def get_all_threats(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Get all threats."""
    threats = ThreatService.get_all_threats(db, skip, limit)
    return threats

@router.get("/severity/{severity}", response_model=list[ThreatResponse])
def get_threats_by_severity(severity: str, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Get threats by severity level."""
    threats = ThreatService.get_threats_by_severity(db, severity, skip, limit)
    return threats

@router.get("/type/{threat_type}", response_model=list[ThreatResponse])
def get_threats_by_type(threat_type: str, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Get threats by type."""
    threats = ThreatService.get_threats_by_type(db, threat_type, skip, limit)
    return threats

@router.get("/unresolved/list", response_model=list[ThreatResponse])
def get_unresolved_threats(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Get unresolved threats."""
    threats = ThreatService.get_unresolved_threats(db, skip, limit)
    return threats

@router.put("/{threat_id}", response_model=ThreatResponse)
def update_threat(threat_id: int, threat_update: ThreatUpdate, db: Session = Depends(get_db)):
    """Update threat by ID."""
    threat = ThreatService.update_threat(db, threat_id, threat_update)
    if not threat:
        raise HTTPException(status_code=404, detail="Threat not found")
    return threat

@router.delete("/{threat_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_threat(threat_id: int, db: Session = Depends(get_db)):
    """Delete threat by ID."""
    success = ThreatService.delete_threat(db, threat_id)
    if not success:
        raise HTTPException(status_code=404, detail="Threat not found")
    return None
