from fastapi import APIRouter, Depends, HTTPException, Query, Request
from sqlalchemy.orm import Session

from core.database import get_db
from core.rbac import Resource, Action, require_permission, get_client_ip
from core.audit_actions import AuditAction
from schemas.extended import (
    AlertCreate,
    AlertUpdate,
    AlertResponse,
    IncidentCreate,
    IncidentUpdate,
    IncidentResponse,
    IOCCreate,
    IOCResponse,
    ThreatIntelligenceCreate,
    ThreatIntelligenceResponse,
    AuditLogResponse,
    SystemSettingResponse,
    SystemSettingUpdate,
)
from services.alert_service import AlertService
from services.incident_service import IncidentService
from services.ioc_service import IOCService
from services.threat_intelligence_service import ThreatIntelligenceService
from services.audit_service import AuditService
from services.settings_service import SettingsService
from models.user import User

router = APIRouter(prefix="/api/v1", tags=["enterprise"])


def _audit_meta(request: Request) -> dict:
    return {
        "ip_address": get_client_ip(request),
        "user_agent": request.headers.get("User-Agent"),
    }


# =======================
# ALERT ENDPOINTS
# =======================

@router.post("/alerts", response_model=AlertResponse)
def create_alert(
    alert: AlertCreate,
    request: Request,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_permission(Resource.ALERTS, Action.CREATE)),
):
    """Create a new alert."""
    db_alert = AlertService.create_alert(db, alert)
    AuditService.log_from_user(
        db,
        current_user,
        AuditAction.ALERT_CREATE.value,
        entity_type="Alert",
        entity_id=db_alert.id,
        new_value=alert.model_dump(),
        **_audit_meta(request),
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
    current_user: User = Depends(require_permission(Resource.ALERTS, Action.READ)),
):
    """Get alerts with filtering."""
    alerts, total = AlertService.get_alerts(db, skip, limit, status, priority, severity)
    return {
        "data": [AlertResponse.model_validate(a) for a in alerts],
        "total": total,
        "skip": skip,
        "limit": limit,
    }


@router.get("/alerts/critical-count")
def get_critical_alerts_count(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_permission(Resource.ALERTS, Action.READ)),
):
    """Get count of critical open alerts."""
    count = AlertService.get_critical_alerts_count(db)
    return {"critical_alerts": count}


@router.get("/alerts/{alert_id}", response_model=AlertResponse)
def get_alert(
    alert_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_permission(Resource.ALERTS, Action.READ)),
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
    request: Request,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_permission(Resource.ALERTS, Action.UPDATE)),
):
    """Update alert."""
    alert = AlertService.update_alert(db, alert_id, update)
    if not alert:
        raise HTTPException(status_code=404, detail="Alert not found")
    AuditService.log_from_user(
        db,
        current_user,
        AuditAction.ALERT_UPDATE.value,
        entity_type="Alert",
        entity_id=alert_id,
        new_value=update.model_dump(exclude_unset=True),
        **_audit_meta(request),
    )
    return alert


@router.post("/alerts/{alert_id}/assign/{user_id}", response_model=AlertResponse)
def assign_alert(
    alert_id: int,
    user_id: int,
    request: Request,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_permission(Resource.ALERTS, Action.EXECUTE)),
):
    """Assign alert to user."""
    alert = AlertService.assign_alert(db, alert_id, user_id)
    if not alert:
        raise HTTPException(status_code=404, detail="Alert not found")
    AuditService.log_from_user(
        db,
        current_user,
        AuditAction.ALERT_ASSIGN.value,
        entity_type="Alert",
        entity_id=alert_id,
        new_value={"assigned_to": user_id},
        **_audit_meta(request),
    )
    return alert


@router.post("/alerts/{alert_id}/escalate", response_model=AlertResponse)
def escalate_alert(
    alert_id: int,
    request: Request,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_permission(Resource.ALERTS, Action.EXECUTE)),
):
    """Escalate alert to critical."""
    alert = AlertService.escalate_alert(db, alert_id)
    if not alert:
        raise HTTPException(status_code=404, detail="Alert not found")
    AuditService.log_from_user(
        db,
        current_user,
        AuditAction.ALERT_ESCALATE.value,
        entity_type="Alert",
        entity_id=alert_id,
        **_audit_meta(request),
    )
    return alert


@router.post("/alerts/{alert_id}/resolve", response_model=AlertResponse)
def resolve_alert(
    alert_id: int,
    request: Request,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_permission(Resource.ALERTS, Action.EXECUTE)),
):
    """Resolve alert."""
    alert = AlertService.resolve_alert(db, alert_id)
    if not alert:
        raise HTTPException(status_code=404, detail="Alert not found")
    AuditService.log_from_user(
        db,
        current_user,
        AuditAction.ALERT_RESOLVE.value,
        entity_type="Alert",
        entity_id=alert_id,
        **_audit_meta(request),
    )
    return alert


# =======================
# INCIDENT ENDPOINTS
# =======================

@router.post("/incidents", response_model=IncidentResponse)
def create_incident(
    incident: IncidentCreate,
    request: Request,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_permission(Resource.INCIDENTS, Action.CREATE)),
):
    """Create a new incident."""
    db_incident = IncidentService.create_incident(db, incident)
    AuditService.log_from_user(
        db,
        current_user,
        AuditAction.INCIDENT_CREATE.value,
        entity_type="Incident",
        entity_id=db_incident.id,
        new_value=incident.model_dump(),
        **_audit_meta(request),
    )
    return db_incident


@router.get("/incidents", response_model=dict)
def get_incidents(
    skip: int = Query(0),
    limit: int = Query(100),
    status: str = Query(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(require_permission(Resource.INCIDENTS, Action.READ)),
):
    """Get incidents."""
    incidents, total = IncidentService.get_incidents(db, skip, limit, status)
    return {
        "data": [IncidentResponse.model_validate(i) for i in incidents],
        "total": total,
        "skip": skip,
        "limit": limit,
    }


@router.get("/incidents/active-count")
def get_active_incidents_count(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_permission(Resource.INCIDENTS, Action.READ)),
):
    """Get count of active incidents."""
    count = IncidentService.get_active_incidents_count(db)
    return {"active_incidents": count}


@router.get("/incidents/{incident_id}", response_model=IncidentResponse)
def get_incident(
    incident_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_permission(Resource.INCIDENTS, Action.READ)),
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
    request: Request,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_permission(Resource.INCIDENTS, Action.UPDATE)),
):
    """Update incident."""
    incident = IncidentService.update_incident(db, incident_id, update)
    if not incident:
        raise HTTPException(status_code=404, detail="Incident not found")
    AuditService.log_from_user(
        db,
        current_user,
        AuditAction.INCIDENT_UPDATE.value,
        entity_type="Incident",
        entity_id=incident_id,
        new_value=update.model_dump(exclude_unset=True),
        **_audit_meta(request),
    )
    return incident


# =======================
# IOC ENDPOINTS
# =======================

@router.post("/iocs", response_model=IOCResponse)
def create_ioc(
    ioc: IOCCreate,
    request: Request,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_permission(Resource.IOCS, Action.CREATE)),
):
    """Create IOC."""
    db_ioc = IOCService.create_ioc(db, ioc)
    AuditService.log_from_user(
        db,
        current_user,
        AuditAction.IOC_CREATE.value,
        entity_type="IOC",
        entity_id=db_ioc.id,
        new_value=ioc.model_dump(),
        **_audit_meta(request),
    )
    return db_ioc


@router.get("/iocs", response_model=dict)
def get_iocs(
    skip: int = Query(0),
    limit: int = Query(100),
    ioc_type: str = Query(None),
    status: str = Query(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(require_permission(Resource.IOCS, Action.READ)),
):
    """Get IOCs."""
    iocs, total = IOCService.get_iocs(db, skip, limit, ioc_type, status)
    return {
        "data": [IOCResponse.model_validate(i) for i in iocs],
        "total": total,
        "skip": skip,
        "limit": limit,
    }


@router.get("/iocs/search", response_model=list)
def search_iocs(
    query: str = Query(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(require_permission(Resource.IOCS, Action.READ)),
):
    """Search IOCs."""
    iocs = IOCService.search_iocs(db, query)
    return [IOCResponse.model_validate(i) for i in iocs]


@router.get("/iocs/high-risk", response_model=list)
def get_high_risk_iocs(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_permission(Resource.IOCS, Action.READ)),
):
    """Get high-risk IOCs."""
    iocs = IOCService.get_high_risk_iocs(db)
    return [IOCResponse.model_validate(i) for i in iocs]


# =======================
# THREAT INTELLIGENCE ENDPOINTS
# =======================

@router.post("/threat-intelligence", response_model=ThreatIntelligenceResponse)
def create_threat_intelligence(
    threat: ThreatIntelligenceCreate,
    request: Request,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_permission(Resource.THREAT_INTEL, Action.CREATE)),
):
    """Create threat intelligence."""
    db_threat = ThreatIntelligenceService.create_threat(db, threat)
    AuditService.log_from_user(
        db,
        current_user,
        AuditAction.THREAT_INTEL_CREATE.value,
        entity_type="ThreatIntelligence",
        entity_id=db_threat.id,
        new_value=threat.model_dump(),
        **_audit_meta(request),
    )
    return db_threat


@router.get("/threat-intelligence", response_model=dict)
def get_threat_intelligence(
    skip: int = Query(0),
    limit: int = Query(100),
    severity: str = Query(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(require_permission(Resource.THREAT_INTEL, Action.READ)),
):
    """Get threat intelligence."""
    threats, total = ThreatIntelligenceService.get_threats(db, skip, limit, severity)
    return {
        "data": [ThreatIntelligenceResponse.model_validate(t) for t in threats],
        "total": total,
        "skip": skip,
        "limit": limit,
    }


@router.get("/threat-intelligence/critical", response_model=list)
def get_critical_threats(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_permission(Resource.THREAT_INTEL, Action.READ)),
):
    """Get critical threats."""
    threats = ThreatIntelligenceService.get_critical_threats(db)
    return [ThreatIntelligenceResponse.model_validate(t) for t in threats]


# =======================
# SETTINGS ENDPOINTS
# =======================

@router.get("/settings", response_model=list[SystemSettingResponse])
def get_settings(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_permission(Resource.SETTINGS, Action.READ)),
):
    """Get system settings."""
    return SettingsService.get_all_settings(db)


@router.patch("/settings/{key}", response_model=SystemSettingResponse)
def update_setting(
    key: str,
    update: SystemSettingUpdate,
    request: Request,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_permission(Resource.SETTINGS, Action.UPDATE)),
):
    """Update a system setting."""
    existing = SettingsService.get_setting(db, key)
    old_value = existing.value if existing else None
    setting = SettingsService.update_setting(
        db, key, update.value, current_user.id, update.description
    )
    AuditService.log_from_user(
        db,
        current_user,
        AuditAction.SETTINGS_UPDATE.value,
        entity_type="Settings",
        entity_id=setting.id,
        old_value={"key": key, "value": old_value},
        new_value={"key": key, "value": update.value},
        **_audit_meta(request),
    )
    return setting


# =======================
# AUDIT ENDPOINTS
# =======================

@router.get("/audit-logs", response_model=dict)
def get_audit_logs(
    skip: int = Query(0),
    limit: int = Query(100),
    user_id: int = Query(None),
    action: str = Query(None),
    entity_type: str = Query(None),
    status: str = Query(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(require_permission(Resource.AUDIT, Action.READ)),
):
    """Get audit logs."""
    logs, total = AuditService.get_audit_logs(
        db, skip, limit, user_id, action, entity_type, status
    )
    return {
        "data": [AuditLogResponse.model_validate(log) for log in logs],
        "total": total,
        "skip": skip,
        "limit": limit,
    }
