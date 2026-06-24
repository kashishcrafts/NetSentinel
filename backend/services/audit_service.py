from sqlalchemy.orm import Session
from models.extended import AuditLog
from typing import List, Optional
from datetime import datetime


class AuditService:
    @staticmethod
    def log_action(
        db: Session,
        user_id: int,
        action: str,
        entity_type: str,
        entity_id: int,
        old_value: Optional[dict] = None,
        new_value: Optional[dict] = None,
        ip_address: Optional[str] = None,
        user_agent: Optional[str] = None,
    ) -> AuditLog:
        log = AuditLog(
            user_id=user_id,
            action=action,
            entity_type=entity_type,
            entity_id=entity_id,
            old_value=old_value,
            new_value=new_value,
            ip_address=ip_address,
            user_agent=user_agent,
        )
        db.add(log)
        db.commit()
        db.refresh(log)
        return log

    @staticmethod
    def get_audit_logs(
        db: Session,
        skip: int = 0,
        limit: int = 100,
        user_id: Optional[int] = None,
        action: Optional[str] = None,
        entity_type: Optional[str] = None,
    ) -> tuple[List[AuditLog], int]:
        query = db.query(AuditLog)
        
        if user_id:
            query = query.filter(AuditLog.user_id == user_id)
        if action:
            query = query.filter(AuditLog.action == action)
        if entity_type:
            query = query.filter(AuditLog.entity_type == entity_type)
        
        total = query.count()
        logs = query.order_by(AuditLog.timestamp.desc()).offset(skip).limit(limit).all()
        return logs, total

    @staticmethod
    def get_user_activity(db: Session, user_id: int, hours: int = 24) -> List[AuditLog]:
        from datetime import timedelta
        time_threshold = datetime.utcnow() - timedelta(hours=hours)
        return db.query(AuditLog).filter(
            AuditLog.user_id == user_id,
            AuditLog.timestamp >= time_threshold
        ).order_by(AuditLog.timestamp.desc()).all()

    @staticmethod
    def get_entity_audit_trail(db: Session, entity_type: str, entity_id: int) -> List[AuditLog]:
        return db.query(AuditLog).filter(
            AuditLog.entity_type == entity_type,
            AuditLog.entity_id == entity_id
        ).order_by(AuditLog.timestamp.desc()).all()

    @staticmethod
    def get_suspicious_activities(db: Session) -> List[AuditLog]:
        suspicious_actions = ["DELETE", "MODIFY_PERMISSION", "ESCALATE_PRIVILEGE"]
        return db.query(AuditLog).filter(
            AuditLog.action.in_(suspicious_actions)
        ).order_by(AuditLog.timestamp.desc()).all()
