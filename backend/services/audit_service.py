from sqlalchemy.orm import Session
from models.extended import AuditLog
from core.audit_actions import AuditAction, AuditStatus
from typing import List, Optional
from datetime import datetime, timedelta


class AuditService:
    @staticmethod
    def log_event(
        db: Session,
        action: str,
        *,
        user_id: Optional[int] = None,
        username: Optional[str] = None,
        role: Optional[str] = None,
        entity_type: Optional[str] = None,
        entity_id: Optional[int] = None,
        status: str = AuditStatus.SUCCESS.value,
        old_value: Optional[dict] = None,
        new_value: Optional[dict] = None,
        ip_address: Optional[str] = None,
        user_agent: Optional[str] = None,
    ) -> AuditLog:
        """Record an enterprise audit log entry."""
        log = AuditLog(
            user_id=user_id,
            username=username,
            role=role,
            action=action,
            entity_type=entity_type,
            entity_id=entity_id,
            status=status,
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
        username: Optional[str] = None,
        role: Optional[str] = None,
        status: str = AuditStatus.SUCCESS.value,
    ) -> AuditLog:
        """Backward-compatible audit logging wrapper."""
        return AuditService.log_event(
            db,
            action,
            user_id=user_id,
            username=username,
            role=role,
            entity_type=entity_type,
            entity_id=entity_id,
            status=status,
            old_value=old_value,
            new_value=new_value,
            ip_address=ip_address,
            user_agent=user_agent,
        )

    @staticmethod
    def log_from_user(
        db: Session,
        user,
        action: str,
        *,
        entity_type: Optional[str] = None,
        entity_id: Optional[int] = None,
        status: str = AuditStatus.SUCCESS.value,
        old_value: Optional[dict] = None,
        new_value: Optional[dict] = None,
        ip_address: Optional[str] = None,
        user_agent: Optional[str] = None,
    ) -> AuditLog:
        """Log an action using an authenticated user object."""
        return AuditService.log_event(
            db,
            action,
            user_id=user.id if user else None,
            username=user.name if user else None,
            role=user.role if user else None,
            entity_type=entity_type,
            entity_id=entity_id,
            status=status,
            old_value=old_value,
            new_value=new_value,
            ip_address=ip_address,
            user_agent=user_agent,
        )

    @staticmethod
    def get_audit_logs(
        db: Session,
        skip: int = 0,
        limit: int = 100,
        user_id: Optional[int] = None,
        action: Optional[str] = None,
        entity_type: Optional[str] = None,
        status: Optional[str] = None,
    ) -> tuple[List[AuditLog], int]:
        query = db.query(AuditLog)

        if user_id:
            query = query.filter(AuditLog.user_id == user_id)
        if action:
            query = query.filter(AuditLog.action == action)
        if entity_type:
            query = query.filter(AuditLog.entity_type == entity_type)
        if status:
            query = query.filter(AuditLog.status == status)

        total = query.count()
        logs = query.order_by(AuditLog.timestamp.desc()).offset(skip).limit(limit).all()
        return logs, total

    @staticmethod
    def get_user_activity(db: Session, user_id: int, hours: int = 24) -> List[AuditLog]:
        time_threshold = datetime.utcnow() - timedelta(hours=hours)
        return db.query(AuditLog).filter(
            AuditLog.user_id == user_id,
            AuditLog.timestamp >= time_threshold,
        ).order_by(AuditLog.timestamp.desc()).all()

    @staticmethod
    def get_entity_audit_trail(db: Session, entity_type: str, entity_id: int) -> List[AuditLog]:
        return db.query(AuditLog).filter(
            AuditLog.entity_type == entity_type,
            AuditLog.entity_id == entity_id,
        ).order_by(AuditLog.timestamp.desc()).all()

    @staticmethod
    def get_suspicious_activities(db: Session) -> List[AuditLog]:
        suspicious_actions = [
            AuditAction.USER_DELETE.value,
            AuditAction.ROLE_CHANGE.value,
            AuditAction.LOGIN_FAILED.value,
            "DELETE",
            "MODIFY_PERMISSION",
            "ESCALATE_PRIVILEGE",
        ]
        return db.query(AuditLog).filter(
            AuditLog.action.in_(suspicious_actions)
        ).order_by(AuditLog.timestamp.desc()).all()
