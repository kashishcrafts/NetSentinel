from sqlalchemy.orm import Session
from models.extended import Incident, IncidentStatus, IncidentComment
from schemas.extended import IncidentCreate, IncidentUpdate
from typing import List, Optional
from datetime import datetime


class IncidentService:
    @staticmethod
    def create_incident(db: Session, incident: IncidentCreate) -> Incident:
        db_incident = Incident(
            title=incident.title,
            description=incident.description,
            severity=incident.severity,
            risk_score=incident.risk_score,
            assigned_to=incident.assigned_to,
        )
        db.add(db_incident)
        db.commit()
        db.refresh(db_incident)
        return db_incident

    @staticmethod
    def get_incidents(
        db: Session,
        skip: int = 0,
        limit: int = 100,
        status: Optional[str] = None,
    ) -> tuple[List[Incident], int]:
        query = db.query(Incident)
        
        if status:
            query = query.filter(Incident.status == status)
        
        total = query.count()
        incidents = query.order_by(Incident.created_at.desc()).offset(skip).limit(limit).all()
        return incidents, total

    @staticmethod
    def get_incident_by_id(db: Session, incident_id: int) -> Optional[Incident]:
        return db.query(Incident).filter(Incident.id == incident_id).first()

    @staticmethod
    def update_incident(db: Session, incident_id: int, update: IncidentUpdate) -> Optional[Incident]:
        incident = db.query(Incident).filter(Incident.id == incident_id).first()
        if not incident:
            return None
        
        update_data = update.dict(exclude_unset=True)
        for key, value in update_data.items():
            setattr(incident, key, value)
        
        incident.updated_at = datetime.utcnow()
        db.commit()
        db.refresh(incident)
        return incident

    @staticmethod
    def add_comment(db: Session, incident_id: int, user_id: int, comment: str) -> IncidentComment:
        db_comment = IncidentComment(incident_id=incident_id, user_id=user_id, comment=comment)
        db.add(db_comment)
        db.commit()
        db.refresh(db_comment)
        return db_comment

    @staticmethod
    def get_incident_comments(db: Session, incident_id: int) -> List[IncidentComment]:
        return db.query(IncidentComment).filter(IncidentComment.incident_id == incident_id).order_by(IncidentComment.created_at).all()

    @staticmethod
    def get_active_incidents_count(db: Session) -> int:
        return db.query(Incident).filter(
            Incident.status.in_([IncidentStatus.NEW, IncidentStatus.INVESTIGATING, IncidentStatus.CONTAINMENT])
        ).count()

    @staticmethod
    def link_alert_to_incident(db: Session, incident_id: int, alert_id: int):
        from models.extended import Alert
        alert = db.query(Alert).filter(Alert.id == alert_id).first()
        if alert:
            alert.incident_id = incident_id
            db.commit()

    @staticmethod
    def unlink_alert_from_incident(db: Session, alert_id: int):
        from models.extended import Alert
        alert = db.query(Alert).filter(Alert.id == alert_id).first()
        if alert:
            alert.incident_id = None
            db.commit()
