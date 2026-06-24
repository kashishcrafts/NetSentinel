from sqlalchemy.orm import Session
from models.threat import Threat
from schemas.threat import ThreatCreate, ThreatUpdate
from typing import Optional, List

class ThreatService:
    
    @staticmethod
    def get_threat_by_id(db: Session, threat_id: int) -> Optional[Threat]:
        return db.query(Threat).filter(Threat.id == threat_id).first()
    
    @staticmethod
    def get_all_threats(db: Session, skip: int = 0, limit: int = 100) -> List[Threat]:
        return db.query(Threat).offset(skip).limit(limit).all()
    
    @staticmethod
    def get_threats_by_severity(db: Session, severity: str, skip: int = 0, limit: int = 100) -> List[Threat]:
        return db.query(Threat).filter(Threat.severity == severity).offset(skip).limit(limit).all()
    
    @staticmethod
    def get_threats_by_type(db: Session, threat_type: str, skip: int = 0, limit: int = 100) -> List[Threat]:
        return db.query(Threat).filter(Threat.threat_type == threat_type).offset(skip).limit(limit).all()
    
    @staticmethod
    def get_unresolved_threats(db: Session, skip: int = 0, limit: int = 100) -> List[Threat]:
        return db.query(Threat).filter(Threat.is_resolved == False).offset(skip).limit(limit).all()
    
    @staticmethod
    def create_threat(db: Session, threat: ThreatCreate, created_by: int) -> Threat:
        db_threat = Threat(
            **threat.dict(),
            created_by=created_by
        )
        db.add(db_threat)
        db.commit()
        db.refresh(db_threat)
        return db_threat
    
    @staticmethod
    def update_threat(db: Session, threat_id: int, threat_update: ThreatUpdate) -> Optional[Threat]:
        db_threat = ThreatService.get_threat_by_id(db, threat_id)
        if not db_threat:
            return None
        
        update_data = threat_update.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_threat, field, value)
        
        db.add(db_threat)
        db.commit()
        db.refresh(db_threat)
        return db_threat
    
    @staticmethod
    def delete_threat(db: Session, threat_id: int) -> bool:
        db_threat = ThreatService.get_threat_by_id(db, threat_id)
        if not db_threat:
            return False
        
        db.delete(db_threat)
        db.commit()
        return True
