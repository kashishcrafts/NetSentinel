from sqlalchemy.orm import Session
from models.extended import Alert, AlertStatus, AlertComment
from schemas.extended import AlertCreate, AlertUpdate, AlertResponse
from typing import List, Optional
from datetime import datetime, timedelta


class AlertService:
    @staticmethod
    def create_alert(db: Session, alert: AlertCreate) -> Alert:
        db_alert = Alert(
            alert_type=alert.alert_type,
            title=alert.title,
            message=alert.message,
            priority=alert.priority,
            severity=alert.severity,
            anomaly_score=alert.anomaly_score,
            risk_score=alert.risk_score,
            confidence=alert.confidence,
            source_ip=alert.source_ip,
            destination_ip=alert.destination_ip,
            protocol=alert.protocol,
            threat_id=alert.threat_id,
            metadata=alert.metadata,
        )
        db.add(db_alert)
        db.commit()
        db.refresh(db_alert)
        return db_alert

    @staticmethod
    def get_alerts(
        db: Session,
        skip: int = 0,
        limit: int = 100,
        status: Optional[str] = None,
        priority: Optional[str] = None,
        severity: Optional[str] = None,
    ) -> tuple[List[Alert], int]:
        query = db.query(Alert)
        
        if status:
            query = query.filter(Alert.status == status)
        if priority:
            query = query.filter(Alert.priority == priority)
        if severity:
            query = query.filter(Alert.severity == severity)
        
        total = query.count()
        alerts = query.order_by(Alert.created_at.desc()).offset(skip).limit(limit).all()
        return alerts, total

    @staticmethod
    def get_alert_by_id(db: Session, alert_id: int) -> Optional[Alert]:
        return db.query(Alert).filter(Alert.id == alert_id).first()

    @staticmethod
    def update_alert(db: Session, alert_id: int, update: AlertUpdate) -> Optional[Alert]:
        alert = db.query(Alert).filter(Alert.id == alert_id).first()
        if not alert:
            return None
        
        update_data = update.dict(exclude_unset=True)
        for key, value in update_data.items():
            setattr(alert, key, value)
        
        alert.updated_at = datetime.utcnow()
        db.commit()
        db.refresh(alert)
        return alert

    @staticmethod
    def assign_alert(db: Session, alert_id: int, user_id: int) -> Optional[Alert]:
        alert = db.query(Alert).filter(Alert.id == alert_id).first()
        if not alert:
            return None
        
        alert.assigned_to = user_id
        alert.status = AlertStatus.ASSIGNED
        alert.updated_at = datetime.utcnow()
        db.commit()
        db.refresh(alert)
        return alert

    @staticmethod
    def escalate_alert(db: Session, alert_id: int) -> Optional[Alert]:
        alert = db.query(Alert).filter(Alert.id == alert_id).first()
        if not alert:
            return None
        
        alert.status = AlertStatus.ESCALATED
        alert.priority = "critical"
        alert.updated_at = datetime.utcnow()
        db.commit()
        db.refresh(alert)
        return alert

    @staticmethod
    def resolve_alert(db: Session, alert_id: int) -> Optional[Alert]:
        alert = db.query(Alert).filter(Alert.id == alert_id).first()
        if not alert:
            return None
        
        alert.status = AlertStatus.RESOLVED
        alert.updated_at = datetime.utcnow()
        db.commit()
        db.refresh(alert)
        return alert

    @staticmethod
    def mark_as_read(db: Session, alert_id: int) -> Optional[Alert]:
        alert = db.query(Alert).filter(Alert.id == alert_id).first()
        if not alert:
            return None
        
        alert.is_read = True
        db.commit()
        db.refresh(alert)
        return alert

    @staticmethod
    def add_comment(db: Session, alert_id: int, user_id: int, comment: str) -> AlertComment:
        db_comment = AlertComment(alert_id=alert_id, user_id=user_id, comment=comment)
        db.add(db_comment)
        db.commit()
        db.refresh(db_comment)
        return db_comment

    @staticmethod
    def get_alert_comments(db: Session, alert_id: int) -> List[AlertComment]:
        return db.query(AlertComment).filter(AlertComment.alert_id == alert_id).order_by(AlertComment.created_at).all()

    @staticmethod
    def get_critical_alerts_count(db: Session) -> int:
        return db.query(Alert).filter(Alert.priority == "critical", Alert.status == AlertStatus.OPEN).count()

    @staticmethod
    def get_open_alerts_count(db: Session) -> int:
        return db.query(Alert).filter(Alert.status == AlertStatus.OPEN).count()

    @staticmethod
    def get_alerts_by_severity(db: Session, severity: str) -> List[Alert]:
        return db.query(Alert).filter(Alert.severity == severity).order_by(Alert.created_at.desc()).all()

    @staticmethod
    def get_recent_alerts(db: Session, hours: int = 24) -> List[Alert]:
        time_threshold = datetime.utcnow() - timedelta(hours=hours)
        return db.query(Alert).filter(Alert.created_at >= time_threshold).order_by(Alert.created_at.desc()).all()
        
        for field, value in update_data.items():
            setattr(db_alert, field, value)
        
        db.add(db_alert)
        db.commit()
        db.refresh(db_alert)
        return db_alert
    
    @staticmethod
    def delete_alert(db: Session, alert_id: int) -> bool:
        db_alert = AlertService.get_alert_by_id(db, alert_id)
        if not db_alert:
            return False
        
        db.delete(db_alert)
        db.commit()
        return True
    
    @staticmethod
    def mark_as_read(db: Session, alert_id: int) -> Optional[Alert]:
        db_alert = AlertService.get_alert_by_id(db, alert_id)
        if not db_alert:
            return None
        
        db_alert.is_read = True
        db.add(db_alert)
        db.commit()
        db.refresh(db_alert)
        return db_alert
