from fastapi import APIRouter, Depends, HTTPException, Query, Request, WebSocket, WebSocketDisconnect
from sqlalchemy.orm import Session

from core.database import get_db
from core.rbac import Resource, Action, require_permission, get_client_ip
from core.security import decode_access_token
from core.audit_actions import AuditAction
from models.user import User
from models.extended import ThreatIntelligence, NetworkFlow, IOC
from services.threat_intelligence_service import ThreatIntelligenceService
from services.audit_service import AuditService
from ml.detection_engine import DetectionPipeline
from network.sensor import NetworkSensor
from datetime import datetime, timedelta
from typing import List, Dict, Any

router = APIRouter(prefix="/api/v1", tags=["advanced"])

detection_pipeline = DetectionPipeline()
network_sensor = NetworkSensor()


def _audit_meta(request: Request) -> dict:
    return {
        "ip_address": get_client_ip(request),
        "user_agent": request.headers.get("User-Agent"),
    }


MITRE_FRAMEWORK = {
    "tactics": {
        "TA0001": {"name": "Initial Access", "techniques": ["T1189", "T1190", "T1195", "T1199", "T1200"]},
        "TA0002": {"name": "Execution", "techniques": ["T1059", "T1609", "T1651", "T1559", "T1203"]},
        "TA0003": {"name": "Persistence", "techniques": ["T1098", "T1197", "T1547", "T1037", "T1554"]},
        "TA0004": {"name": "Privilege Escalation", "techniques": ["T1548", "T1547", "T1134", "T1547", "T1547"]},
        "TA0005": {"name": "Defense Evasion", "techniques": ["T1548", "T1197", "T1140", "T1197", "T1140"]},
        "TA0006": {"name": "Credential Access", "techniques": ["T1110", "T1555", "T1187", "T1040", "T1056"]},
        "TA0007": {"name": "Discovery", "techniques": ["T1087", "T1010", "T1217", "T1580", "T1526"]},
        "TA0008": {"name": "Lateral Movement", "techniques": ["T1210", "T1570", "T1570", "T1570", "T1570"]},
        "TA0009": {"name": "Collection", "techniques": ["T1557", "T1123", "T1119", "T1185", "T1115"]},
        "TA0010": {"name": "Exfiltration", "techniques": ["T1020", "T1030", "T1048", "T1041", "T1011"]},
        "TA0011": {"name": "Command and Control", "techniques": ["T1071", "T1092", "T1001", "T1008", "T1105"]},
        "TA0040": {"name": "Impact", "techniques": ["T1531", "T1561", "T1565", "T1491", "T1561"]},
    }
}


@router.get("/mitre/tactics")
def get_mitre_tactics(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_permission(Resource.THREAT_INTEL, Action.READ)),
):
    """Get MITRE ATT&CK tactics matrix."""
    return {
        "tactics": MITRE_FRAMEWORK["tactics"],
        "framework": "MITRE ATT&CK v12",
    }


@router.get("/mitre/tactic/{tactic_id}")
def get_tactic_details(
    tactic_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_permission(Resource.THREAT_INTEL, Action.READ)),
):
    """Get tactic details with mapped threats."""
    tactic = MITRE_FRAMEWORK["tactics"].get(tactic_id)
    if not tactic:
        raise HTTPException(status_code=404, detail="Tactic not found")
    threats = ThreatIntelligenceService.get_threats_by_tactic(db, tactic_id)
    return {
        "tactic_id": tactic_id,
        "tactic_name": tactic["name"],
        "techniques": tactic["techniques"],
        "mapped_threats": [{"id": t.id, "name": t.threat_name} for t in threats],
    }


@router.post("/threats/{threat_id}/mitre-map")
def map_threat_to_mitre(
    threat_id: int,
    tactic_id: str,
    technique_id: str,
    technique_name: str,
    request: Request,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_permission(Resource.THREAT_INTEL, Action.UPDATE)),
):
    """Map threat to MITRE ATT&CK framework."""
    threat = ThreatIntelligenceService.get_threat_by_id(db, threat_id)
    if not threat:
        raise HTTPException(status_code=404, detail="Threat not found")
    tactic = MITRE_FRAMEWORK["tactics"].get(tactic_id)
    if not tactic:
        raise HTTPException(status_code=404, detail="Tactic not found")
    mapping = ThreatIntelligenceService.add_mitre_mapping(
        db, threat_id, tactic_id, tactic["name"], technique_id, technique_name
    )
    AuditService.log_from_user(
        db,
        current_user,
        AuditAction.THREAT_UPDATE.value,
        entity_type="ThreatIntelligence",
        entity_id=threat_id,
        new_value={"tactic_id": tactic_id, "technique_id": technique_id},
        **_audit_meta(request),
    )
    return {
        "mapping_id": mapping.id,
        "threat_id": threat_id,
        "tactic_id": tactic_id,
        "technique_id": technique_id,
    }


@router.get("/mitre/attack-matrix")
def get_attack_matrix(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_permission(Resource.THREAT_INTEL, Action.READ)),
):
    """Get attack matrix view of all tactics and techniques."""
    matrix = {}
    for tactic_id, tactic_data in MITRE_FRAMEWORK["tactics"].items():
        matrix[tactic_id] = {
            "name": tactic_data["name"],
            "techniques": tactic_data["techniques"],
            "threat_count": len(ThreatIntelligenceService.get_threats_by_tactic(db, tactic_id)),
        }
    return {"matrix": matrix}


@router.post("/threat-hunting/search-ip")
def hunt_by_ip(
    ip: str,
    time_range_hours: int = Query(24),
    db: Session = Depends(get_db),
    current_user: User = Depends(require_permission(Resource.DETECTION, Action.EXECUTE)),
):
    """Hunt threats by IP address."""
    time_threshold = datetime.utcnow() - timedelta(hours=time_range_hours)
    flows = db.query(NetworkFlow).filter(
        (NetworkFlow.source_ip == ip) | (NetworkFlow.destination_ip == ip),
        NetworkFlow.timestamp >= time_threshold,
    ).order_by(NetworkFlow.timestamp.desc()).all()
    suspicious_flows = [f for f in flows if f.anomaly_score > 0.7 or f.risk_score > 70]
    return {
        "searched_ip": ip,
        "total_flows": len(flows),
        "suspicious_flows": len(suspicious_flows),
        "flows": [
            {
                "id": f.id,
                "source_ip": f.source_ip,
                "destination_ip": f.destination_ip,
                "protocol": f.protocol,
                "anomaly_score": f.anomaly_score,
                "risk_score": f.risk_score,
                "timestamp": f.timestamp.isoformat(),
            }
            for f in suspicious_flows[:50]
        ],
    }


@router.post("/threat-hunting/search-domain")
def hunt_by_domain(
    domain: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_permission(Resource.DETECTION, Action.EXECUTE)),
):
    """Hunt threats by domain."""
    iocs = db.query(IOC).filter(IOC.value.ilike(f"%{domain}%")).all()
    return {
        "searched_domain": domain,
        "ioc_count": len(iocs),
        "iocs": [
            {
                "id": i.id,
                "type": i.ioc_type,
                "value": i.value,
                "risk_score": i.risk_score,
                "reputation": i.reputation,
            }
            for i in iocs
        ],
    }


@router.post("/threat-hunting/search-hash")
def hunt_by_hash(
    file_hash: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_permission(Resource.DETECTION, Action.EXECUTE)),
):
    """Hunt threats by file hash."""
    ioc = db.query(IOC).filter(IOC.value == file_hash, IOC.ioc_type == "hash").first()
    if not ioc:
        return {"hash": file_hash, "found": False, "message": "Hash not in database"}
    return {
        "hash": file_hash,
        "found": True,
        "ioc_id": ioc.id,
        "description": ioc.description,
        "risk_score": ioc.risk_score,
        "reputation": ioc.reputation,
        "source": ioc.source,
    }


@router.post("/detection/analyze-flow")
def analyze_network_flow(
    flow_data: Dict[str, Any],
    request: Request,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_permission(Resource.DETECTION, Action.EXECUTE)),
):
    """Analyze network flow through detection pipeline."""
    result = detection_pipeline.process_network_flow(flow_data)
    AuditService.log_from_user(
        db,
        current_user,
        AuditAction.DETECTION_EXECUTE.value,
        entity_type="Detection",
        new_value={"flow_source": flow_data.get("source_ip")},
        **_audit_meta(request),
    )
    return result


@router.post("/detection/batch-analyze")
def batch_analyze_flows(
    flows: List[Dict[str, Any]],
    request: Request,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_permission(Resource.DETECTION, Action.EXECUTE)),
):
    """Analyze multiple flows."""
    results = [detection_pipeline.process_network_flow(flow) for flow in flows]
    AuditService.log_from_user(
        db,
        current_user,
        AuditAction.DETECTION_EXECUTE.value,
        entity_type="Detection",
        new_value={"batch_size": len(flows)},
        **_audit_meta(request),
    )
    return {"total_analyzed": len(flows), "results": results}


@router.get("/detection/sensor-stats")
def get_sensor_stats(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_permission(Resource.DETECTION, Action.READ)),
):
    """Get network sensor statistics."""
    return network_sensor.get_sensor_stats()


async def _authenticate_websocket(websocket: WebSocket, db: Session) -> User | None:
    """Validate Bearer token on WebSocket connection."""
    auth = websocket.headers.get("Authorization", "")
    token = auth[7:].strip() if auth.startswith("Bearer ") else websocket.query_params.get("token")
    if not token:
        return None
    payload = decode_access_token(token)
    if not payload or not payload.get("sub"):
        return None
    user = db.query(User).filter(User.id == int(payload["sub"])).first()
    if not user or not user.is_active:
        return None
    return user


@router.websocket("/ws/live-threats")
async def websocket_live_threats(websocket: WebSocket, db: Session = Depends(get_db)):
    """WebSocket for live threat updates (authenticated)."""
    user = await _authenticate_websocket(websocket, db)
    if not user:
        await websocket.close(code=4401)
        return
    await websocket.accept()
    try:
        import asyncio
        from models.extended import Alert, AlertPriority, AlertStatus

        while True:
            critical_alerts = db.query(Alert).filter(
                Alert.priority == AlertPriority.CRITICAL,
                Alert.status == AlertStatus.OPEN,
            ).limit(10).all()
            await websocket.send_json({
                "type": "threat_update",
                "count": len(critical_alerts),
                "alerts": [
                    {
                        "id": a.id,
                        "title": a.title,
                        "severity": a.severity,
                        "risk_score": a.risk_score,
                    }
                    for a in critical_alerts
                ],
            })
            await asyncio.sleep(5)
    except WebSocketDisconnect:
        pass


@router.websocket("/ws/live-incidents")
async def websocket_live_incidents(websocket: WebSocket, db: Session = Depends(get_db)):
    """WebSocket for live incident updates (authenticated)."""
    user = await _authenticate_websocket(websocket, db)
    if not user:
        await websocket.close(code=4401)
        return
    await websocket.accept()
    try:
        import asyncio
        from services.incident_service import IncidentService

        while True:
            active_incidents = IncidentService.get_active_incidents_count(db)
            await websocket.send_json({
                "type": "incident_update",
                "active_count": active_incidents,
            })
            await asyncio.sleep(10)
    except WebSocketDisconnect:
        pass
