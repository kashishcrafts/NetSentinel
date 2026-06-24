from sqlalchemy.orm import Session
from models.extended import ThreatIntelligence, MitreMapping
from schemas.extended import ThreatIntelligenceCreate
from typing import List, Optional
from datetime import datetime


class ThreatIntelligenceService:
    @staticmethod
    def create_threat(db: Session, threat: ThreatIntelligenceCreate) -> ThreatIntelligence:
        db_threat = ThreatIntelligence(
            threat_name=threat.threat_name,
            threat_actor=threat.threat_actor,
            description=threat.description,
            mitre_techniques=threat.mitre_techniques,
            mitre_tactics=threat.mitre_tactics,
            confidence=threat.confidence,
            severity=threat.severity,
            risk_score=threat.risk_score,
            source=threat.source,
            malware_families=threat.malware_families,
        )
        db.add(db_threat)
        db.commit()
        db.refresh(db_threat)
        return db_threat

    @staticmethod
    def get_threats(
        db: Session,
        skip: int = 0,
        limit: int = 100,
        severity: Optional[str] = None,
    ) -> tuple[List[ThreatIntelligence], int]:
        query = db.query(ThreatIntelligence)
        
        if severity:
            query = query.filter(ThreatIntelligence.severity == severity)
        
        total = query.count()
        threats = query.order_by(ThreatIntelligence.created_at.desc()).offset(skip).limit(limit).all()
        return threats, total

    @staticmethod
    def get_threat_by_id(db: Session, threat_id: int) -> Optional[ThreatIntelligence]:
        return db.query(ThreatIntelligence).filter(ThreatIntelligence.id == threat_id).first()

    @staticmethod
    def get_threat_by_name(db: Session, threat_name: str) -> Optional[ThreatIntelligence]:
        return db.query(ThreatIntelligence).filter(ThreatIntelligence.threat_name == threat_name).first()

    @staticmethod
    def search_threats(db: Session, search_term: str) -> List[ThreatIntelligence]:
        return db.query(ThreatIntelligence).filter(
            ThreatIntelligence.threat_name.ilike(f"%{search_term}%")
        ).all()

    @staticmethod
    def get_threats_by_actor(db: Session, actor: str) -> List[ThreatIntelligence]:
        return db.query(ThreatIntelligence).filter(
            ThreatIntelligence.threat_actor == actor
        ).all()

    @staticmethod
    def add_mitre_mapping(
        db: Session,
        threat_id: int,
        tactic_id: str,
        tactic_name: str,
        technique_id: str,
        technique_name: str,
        subtechnique_id: Optional[str] = None,
        subtechnique_name: Optional[str] = None,
    ) -> MitreMapping:
        mapping = MitreMapping(
            threat_id=threat_id,
            tactic_id=tactic_id,
            tactic_name=tactic_name,
            technique_id=technique_id,
            technique_name=technique_name,
            subtechnique_id=subtechnique_id,
            subtechnique_name=subtechnique_name,
        )
        db.add(mapping)
        db.commit()
        db.refresh(mapping)
        return mapping

    @staticmethod
    def get_threat_mitre_mappings(db: Session, threat_id: int) -> List[MitreMapping]:
        return db.query(MitreMapping).filter(MitreMapping.threat_id == threat_id).all()

    @staticmethod
    def get_threats_by_tactic(db: Session, tactic_id: str) -> List[ThreatIntelligence]:
        mappings = db.query(MitreMapping).filter(MitreMapping.tactic_id == tactic_id).all()
        threat_ids = list(set([m.threat_id for m in mappings if m.threat_id]))
        return db.query(ThreatIntelligence).filter(ThreatIntelligence.id.in_(threat_ids)).all()

    @staticmethod
    def get_critical_threats(db: Session) -> List[ThreatIntelligence]:
        return db.query(ThreatIntelligence).filter(
            ThreatIntelligence.severity == "critical"
        ).order_by(ThreatIntelligence.risk_score.desc()).all()
