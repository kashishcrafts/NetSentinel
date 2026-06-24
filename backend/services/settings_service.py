from sqlalchemy.orm import Session
from models.extended import SystemSetting
from typing import List, Optional


class SettingsService:
    DEFAULT_SETTINGS = {
        "alert_retention_days": {"value": 90, "description": "Days to retain resolved alerts"},
        "session_timeout_minutes": {"value": 30, "description": "JWT access token lifetime hint"},
        "enable_mfa": {"value": False, "description": "Multi-factor authentication enabled"},
        "max_login_attempts": {"value": 5, "description": "Max failed login attempts before lockout"},
    }

    @staticmethod
    def ensure_defaults(db: Session) -> None:
        for key, meta in SettingsService.DEFAULT_SETTINGS.items():
            existing = db.query(SystemSetting).filter(SystemSetting.key == key).first()
            if not existing:
                db.add(SystemSetting(key=key, value=meta["value"], description=meta["description"]))
        db.commit()

    @staticmethod
    def get_all_settings(db: Session) -> List[SystemSetting]:
        SettingsService.ensure_defaults(db)
        return db.query(SystemSetting).order_by(SystemSetting.key).all()

    @staticmethod
    def get_setting(db: Session, key: str) -> Optional[SystemSetting]:
        return db.query(SystemSetting).filter(SystemSetting.key == key).first()

    @staticmethod
    def update_setting(
        db: Session,
        key: str,
        value,
        updated_by: int,
        description: Optional[str] = None,
    ) -> Optional[SystemSetting]:
        setting = db.query(SystemSetting).filter(SystemSetting.key == key).first()
        if not setting:
            setting = SystemSetting(key=key, value=value, description=description)
        else:
            setting.value = value
            if description is not None:
                setting.description = description
        setting.updated_by = updated_by
        db.add(setting)
        db.commit()
        db.refresh(setting)
        return setting
