from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from schemas.alert import AlertCreate, AlertResponse, AlertUpdate
from services.alert_service import AlertService
from core.database import get_db

router = APIRouter(prefix="/alerts", tags=["Alerts"])

@router.post("", response_model=AlertResponse, status_code=status.HTTP_201_CREATED)
def create_alert(alert: AlertCreate, created_by: int = 1, db: Session = Depends(get_db)):
    """Create a new alert."""
    new_alert = AlertService.create_alert(db, alert, created_by)
    return new_alert

@router.get("/{alert_id}", response_model=AlertResponse)
def get_alert(alert_id: int, db: Session = Depends(get_db)):
    """Get alert by ID."""
    alert = AlertService.get_alert_by_id(db, alert_id)
    if not alert:
        raise HTTPException(status_code=404, detail="Alert not found")
    return alert

@router.get("", response_model=list[AlertResponse])
def get_all_alerts(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Get all alerts."""
    alerts = AlertService.get_all_alerts(db, skip, limit)
    return alerts

@router.get("/status/{status}", response_model=list[AlertResponse])
def get_alerts_by_status(status: str, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Get alerts by status."""
    alerts = AlertService.get_alerts_by_status(db, status, skip, limit)
    return alerts

@router.get("/threat/{threat_id}", response_model=list[AlertResponse])
def get_alerts_by_threat(threat_id: int, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Get alerts by threat ID."""
    alerts = AlertService.get_alerts_by_threat(db, threat_id, skip, limit)
    return alerts

@router.get("/unread/list", response_model=list[AlertResponse])
def get_unread_alerts(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Get unread alerts."""
    alerts = AlertService.get_unread_alerts(db, skip, limit)
    return alerts

@router.put("/{alert_id}", response_model=AlertResponse)
def update_alert(alert_id: int, alert_update: AlertUpdate, db: Session = Depends(get_db)):
    """Update alert by ID."""
    alert = AlertService.update_alert(db, alert_id, alert_update)
    if not alert:
        raise HTTPException(status_code=404, detail="Alert not found")
    return alert

@router.post("/{alert_id}/read", response_model=AlertResponse)
def mark_alert_as_read(alert_id: int, db: Session = Depends(get_db)):
    """Mark alert as read."""
    alert = AlertService.mark_as_read(db, alert_id)
    if not alert:
        raise HTTPException(status_code=404, detail="Alert not found")
    return alert

@router.delete("/{alert_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_alert(alert_id: int, db: Session = Depends(get_db)):
    """Delete alert by ID."""
    success = AlertService.delete_alert(db, alert_id)
    if not success:
        raise HTTPException(status_code=404, detail="Alert not found")
    return None
