from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from core.database import get_db
from core.rbac import get_current_user
from schemas.extended import (
    AlertCreate, AlertUpdate, AlertResponse,
    IncidentCreate, IncidentUpdate, IncidentResponse,
    IOCCreate, IOCResponse,
    ThreatIntelligenceCreate, ThreatIntelligenceResponse,
    AuditLogResponse,
)
from services.alert_service import AlertService
from services.incident_service import IncidentService
from services.ioc_service import IOCService
from services.threat_intelligence_service import ThreatIntelligenceService
from services.audit_service import AuditService
from models.user import User
from typing import List

router = APIRouter(prefix="/api/v1", tags=["enterprise"])


# =======================
# ALERT ENDPOINTS
# =======================

@router.post("/alerts", response_model=AlertResponse)
def create_alert(
    alert: AlertCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Create a new alert."""
    db_alert = AlertService.create_alert(db, alert)
    
    # Audit log
    AuditService.log_action(
        db, current_user.id, "CREATE", "Alert", db_alert.id,
        new_value=alert.dict()
    )
    
    return db_alert


@router.get("/alerts", response_model=dict)
def get_alerts(
    skip: int = Query(0),
    limit: int = Query(100),
    status: str = Query(None),
    priority: str = Query(None),
    severity: str = Query(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Get alerts with filtering."""
    alerts, total = AlertService.get_alerts(db, skip, limit, status, priority, severity)
    return {
        "data": [AlertResponse.from_orm(a) for a in alerts],
        "total": total,
        "skip": skip,
        "limit": limit,
    }


@router.get("/alerts/{alert_id}", response_model=AlertResponse)
def get_alert(
    alert_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Get alert by ID."""
    alert = AlertService.get_alert_by_id(db, alert_id)
    if not alert:
        raise HTTPException(status_code=404, detail="Alert not found")
    
    AlertService.mark_as_read(db, alert_id)
    return alert


@router.patch("/alerts/{alert_id}", response_model=AlertResponse)
def update_alert(
    alert_id: int,
    update: AlertUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Update alert."""
    alert = AlertService.update_alert(db, alert_id, update)
    if not alert:
        raise HTTPException(status_code=404, detail="Alert not found")
    
    AuditService.log_action(
        db, current_user.id, "UPDATE", "Alert", alert_id,
        new_value=update.dict(exclude_unset=True)
    )
    
    return alert


@router.post("/alerts/{alert_id}/assign/{user_id}", response_model=AlertResponse)
def assign_alert(
    alert_id: int,
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Assign alert to user."""
    alert = AlertService.assign_alert(db, alert_id, user_id)
    if not alert:
        raise HTTPException(status_code=404, detail="Alert not found")
    
    AuditService.log_action(
        db, current_user.id, "ASSIGN", "Alert", alert_id,
        new_value={"assigned_to": user_id}
    )
    
    return alert


@router.post("/alerts/{alert_id}/escalate", response_model=AlertResponse)
def escalate_alert(
    alert_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Escalate alert to critical."""
    alert = AlertService.escalate_alert(db, alert_id)
    if not alert:
        raise HTTPException(status_code=404, detail="Alert not found")
    
    AuditService.log_action(
        db, current_user.id, "ESCALATE", "Alert", alert_id
    )
    
    return alert


@router.post("/alerts/{alert_id}/resolve", response_model=AlertResponse)
def resolve_alert(
    alert_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Resolve alert."""
    alert = AlertService.resolve_alert(db, alert_id)
    if not alert:
        raise HTTPException(status_code=404, detail="Alert not found")
    
    AuditService.log_action(
        db, current_user.id, "RESOLVE", "Alert", alert_id
    )
    
    return alert


@router.get("/alerts/critical-count")
def get_critical_alerts_count(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Get count of critical open alerts."""
    count = AlertService.get_critical_alerts_count(db)
    return {"critical_alerts": count}


# =======================
# INCIDENT ENDPOINTS
# =======================

@router.post("/incidents", response_model=IncidentResponse)
def create_incident(
    incident: IncidentCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Create a new incident."""
    db_incident = IncidentService.create_incident(db, incident)
    
    AuditService.log_action(
        db, current_user.id, "CREATE", "Incident", db_incident.id,
        new_value=incident.dict()
    )
    
    return db_incident


@router.get("/incidents", response_model=dict)
def get_incidents(
    skip: int = Query(0),
    limit: int = Query(100),
    status: str = Query(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Get incidents."""
    incidents, total = IncidentService.get_incidents(db, skip, limit, status)
    return {
        "data": [IncidentResponse.from_orm(i) for i in incidents],
        "total": total,
        "skip": skip,
        "limit": limit,
    }


@router.get("/incidents/{incident_id}", response_model=IncidentResponse)
def get_incident(
    incident_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Get incident by ID."""
    incident = IncidentService.get_incident_by_id(db, incident_id)
    if not incident:
        raise HTTPException(status_code=404, detail="Incident not found")
    
    return incident


@router.patch("/incidents/{incident_id}", response_model=IncidentResponse)
def update_incident(
    incident_id: int,
    update: IncidentUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Update incident."""
    incident = IncidentService.update_incident(db, incident_id, update)
    if not incident:
        raise HTTPException(status_code=404, detail="Incident not found")
    
    AuditService.log_action(
        db, current_user.id, "UPDATE", "Incident", incident_id,
        new_value=update.dict(exclude_unset=True)
    )
    
    return incident


@router.get("/incidents/active-count")
def get_active_incidents_count(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Get count of active incidents."""
    count = IncidentService.get_active_incidents_count(db)
    return {"active_incidents": count}


# =======================
# IOC ENDPOINTS
# =======================

@router.post("/iocs", response_model=IOCResponse)
def create_ioc(
    ioc: IOCCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Create IOC."""
    db_ioc = IOCService.create_ioc(db, ioc)
    
    AuditService.log_action(
        db, current_user.id, "CREATE", "IOC", db_ioc.id,
        new_value=ioc.dict()
    )
    
    return db_ioc


@router.get("/iocs", response_model=dict)
def get_iocs(
    skip: int = Query(0),
    limit: int = Query(100),
    ioc_type: str = Query(None),
    status: str = Query(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Get IOCs."""
    iocs, total = IOCService.get_iocs(db, skip, limit, ioc_type, status)
    return {
        "data": [IOCResponse.from_orm(i) for i in iocs],
        "total": total,
        "skip": skip,
        "limit": limit,
    }


@router.get("/iocs/search", response_model=list)
def search_iocs(
    query: str = Query(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Search IOCs."""
    iocs = IOCService.search_iocs(db, query)
    return [IOCResponse.from_orm(i) for i in iocs]


@router.get("/iocs/high-risk", response_model=list)
def get_high_risk_iocs(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Get high-risk IOCs."""
    iocs = IOCService.get_high_risk_iocs(db)
    return [IOCResponse.from_orm(i) for i in iocs]


# =======================
# THREAT INTELLIGENCE ENDPOINTS
# =======================

@router.post("/threat-intelligence", response_model=ThreatIntelligenceResponse)
def create_threat_intelligence(
    threat: ThreatIntelligenceCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Create threat intelligence."""
    db_threat = ThreatIntelligenceService.create_threat(db, threat)
    
    AuditService.log_action(
        db, current_user.id, "CREATE", "ThreatIntelligence", db_threat.id,
        new_value=threat.dict()
    )
    
    return db_threat


@router.get("/threat-intelligence", response_model=dict)
def get_threat_intelligence(
    skip: int = Query(0),
    limit: int = Query(100),
    severity: str = Query(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Get threat intelligence."""
    threats, total = ThreatIntelligenceService.get_threats(db, skip, limit, severity)
    return {
        "data": [ThreatIntelligenceResponse.from_orm(t) for t in threats],
        "total": total,
        "skip": skip,
        "limit": limit,
    }


@router.get("/threat-intelligence/critical", response_model=list)
def get_critical_threats(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Get critical threats."""
    threats = ThreatIntelligenceService.get_critical_threats(db)
    return [ThreatIntelligenceResponse.from_orm(t) for t in threats]


@router.get("/audit-logs", response_model=dict)
def get_audit_logs(
    skip: int = Query(0),
    limit: int = Query(100),
    user_id: int = Query(None),
    action: str = Query(None),
    entity_type: str = Query(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Get audit logs."""
    logs, total = AuditService.get_audit_logs(db, skip, limit, user_id, action, entity_type)
    return {
        "data": [AuditLogResponse.from_orm(l) for l in logs],
        "total": total,
        "skip": skip,
        "limit": limit,
    }
