from fastapi import APIRouter, Depends, HTTPException, Request, status
from sqlalchemy.orm import Session

from schemas.extended import AlertCreate, AlertResponse, AlertUpdate
from services.alert_service import AlertService
from services.audit_service import AuditService
from core.database import get_db
from core.rbac import Resource, Action, require_permission, get_client_ip
from core.audit_actions import AuditAction
from models.user import User

router = APIRouter(prefix="/alerts", tags=["Alerts"])


def _audit_meta(request: Request) -> dict:
    return {
        "ip_address": get_client_ip(request),
        "user_agent": request.headers.get("User-Agent"),
    }


@router.post("", response_model=AlertResponse, status_code=status.HTTP_201_CREATED)
def create_alert(
    alert: AlertCreate,
    request: Request,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_permission(Resource.ALERTS, Action.CREATE)),
):
    """Create a new alert."""
    new_alert = AlertService.create_alert(db, alert)
    AuditService.log_from_user(
        db,
        current_user,
        AuditAction.ALERT_CREATE.value,
        entity_type="Alert",
        entity_id=new_alert.id,
        new_value=alert.model_dump(),
        **_audit_meta(request),
    )
    return new_alert


@router.get("/{alert_id}", response_model=AlertResponse)
def get_alert(
    alert_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_permission(Resource.ALERTS, Action.READ)),
):
    """Get alert by ID."""
    alert = AlertService.get_alert_by_id(db, alert_id)
    if not alert:
        raise HTTPException(status_code=404, detail="Alert not found")
    return alert


@router.get("", response_model=dict)
def get_all_alerts(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_permission(Resource.ALERTS, Action.READ)),
):
    """Get all alerts."""
    alerts, total = AlertService.get_alerts(db, skip, limit)
    return {
        "data": [AlertResponse.model_validate(a) for a in alerts],
        "total": total,
        "skip": skip,
        "limit": limit,
    }


@router.put("/{alert_id}", response_model=AlertResponse)
def update_alert(
    alert_id: int,
    alert_update: AlertUpdate,
    request: Request,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_permission(Resource.ALERTS, Action.UPDATE)),
):
    """Update alert by ID."""
    alert = AlertService.update_alert(db, alert_id, alert_update)
    if not alert:
        raise HTTPException(status_code=404, detail="Alert not found")
    AuditService.log_from_user(
        db,
        current_user,
        AuditAction.ALERT_UPDATE.value,
        entity_type="Alert",
        entity_id=alert_id,
        new_value=alert_update.model_dump(exclude_unset=True),
        **_audit_meta(request),
    )
    return alert


@router.post("/{alert_id}/read", response_model=AlertResponse)
def mark_alert_as_read(
    alert_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_permission(Resource.ALERTS, Action.UPDATE)),
):
    """Mark alert as read."""
    alert = AlertService.mark_as_read(db, alert_id)
    if not alert:
        raise HTTPException(status_code=404, detail="Alert not found")
    return alert


@router.delete("/{alert_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_alert(
    alert_id: int,
    request: Request,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_permission(Resource.ALERTS, Action.DELETE)),
):
    """Delete alert by ID."""
    success = AlertService.delete_alert(db, alert_id)
    if not success:
        raise HTTPException(status_code=404, detail="Alert not found")
    AuditService.log_from_user(
        db,
        current_user,
        AuditAction.ALERT_DELETE.value,
        entity_type="Alert",
        entity_id=alert_id,
        **_audit_meta(request),
    )
    return None
