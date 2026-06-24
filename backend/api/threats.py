from fastapi import APIRouter, Depends, HTTPException, Request, status
from sqlalchemy.orm import Session

from schemas.threat import ThreatCreate, ThreatResponse, ThreatUpdate
from services.threat_service import ThreatService
from services.audit_service import AuditService
from core.database import get_db
from core.rbac import Resource, Action, require_permission, get_client_ip
from core.audit_actions import AuditAction
from models.user import User

router = APIRouter(prefix="/threats", tags=["Threats"])


def _audit_meta(request: Request) -> dict:
    return {
        "ip_address": get_client_ip(request),
        "user_agent": request.headers.get("User-Agent"),
    }


@router.post("", response_model=ThreatResponse, status_code=status.HTTP_201_CREATED)
def create_threat(
    threat: ThreatCreate,
    request: Request,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_permission(Resource.THREATS, Action.CREATE)),
):
    """Create a new threat."""
    new_threat = ThreatService.create_threat(db, threat, current_user.id)
    AuditService.log_from_user(
        db,
        current_user,
        AuditAction.THREAT_CREATE.value,
        entity_type="Threat",
        entity_id=new_threat.id,
        new_value=threat.model_dump(),
        **_audit_meta(request),
    )
    return new_threat


@router.get("/{threat_id}", response_model=ThreatResponse)
def get_threat(
    threat_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_permission(Resource.THREATS, Action.READ)),
):
    """Get threat by ID."""
    threat = ThreatService.get_threat_by_id(db, threat_id)
    if not threat:
        raise HTTPException(status_code=404, detail="Threat not found")
    return threat


@router.get("", response_model=list[ThreatResponse])
def get_all_threats(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_permission(Resource.THREATS, Action.READ)),
):
    """Get all threats."""
    return ThreatService.get_all_threats(db, skip, limit)


@router.get("/severity/{severity}", response_model=list[ThreatResponse])
def get_threats_by_severity(
    severity: str,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_permission(Resource.THREATS, Action.READ)),
):
    """Get threats by severity level."""
    return ThreatService.get_threats_by_severity(db, severity, skip, limit)


@router.get("/type/{threat_type}", response_model=list[ThreatResponse])
def get_threats_by_type(
    threat_type: str,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_permission(Resource.THREATS, Action.READ)),
):
    """Get threats by type."""
    return ThreatService.get_threats_by_type(db, threat_type, skip, limit)


@router.get("/unresolved/list", response_model=list[ThreatResponse])
def get_unresolved_threats(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_permission(Resource.THREATS, Action.READ)),
):
    """Get unresolved threats."""
    return ThreatService.get_unresolved_threats(db, skip, limit)


@router.put("/{threat_id}", response_model=ThreatResponse)
def update_threat(
    threat_id: int,
    threat_update: ThreatUpdate,
    request: Request,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_permission(Resource.THREATS, Action.UPDATE)),
):
    """Update threat by ID."""
    threat = ThreatService.update_threat(db, threat_id, threat_update)
    if not threat:
        raise HTTPException(status_code=404, detail="Threat not found")
    AuditService.log_from_user(
        db,
        current_user,
        AuditAction.THREAT_UPDATE.value,
        entity_type="Threat",
        entity_id=threat_id,
        new_value=threat_update.model_dump(exclude_unset=True),
        **_audit_meta(request),
    )
    return threat


@router.delete("/{threat_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_threat(
    threat_id: int,
    request: Request,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_permission(Resource.THREATS, Action.DELETE)),
):
    """Delete threat by ID."""
    success = ThreatService.delete_threat(db, threat_id)
    if not success:
        raise HTTPException(status_code=404, detail="Threat not found")
    AuditService.log_from_user(
        db,
        current_user,
        AuditAction.THREAT_DELETE.value,
        entity_type="Threat",
        entity_id=threat_id,
        **_audit_meta(request),
    )
    return None
