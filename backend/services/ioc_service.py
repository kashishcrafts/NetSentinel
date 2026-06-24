from sqlalchemy.orm import Session
from models.extended import IOC, IOCType
from schemas.extended import IOCCreate, IOCResponse
from typing import List, Optional
from datetime import datetime


class IOCService:
    @staticmethod
    def create_ioc(db: Session, ioc: IOCCreate) -> IOC:
        existing = db.query(IOC).filter(IOC.value == ioc.value).first()
        if existing:
            return existing
        
        db_ioc = IOC(
            ioc_type=ioc.ioc_type,
            value=ioc.value,
            description=ioc.description,
            reputation=ioc.reputation,
            risk_score=ioc.risk_score,
            confidence=ioc.confidence,
            source=ioc.source,
            tags=ioc.tags,
            metadata=ioc.metadata,
        )
        db.add(db_ioc)
        db.commit()
        db.refresh(db_ioc)
        return db_ioc

    @staticmethod
    def get_iocs(
        db: Session,
        skip: int = 0,
        limit: int = 100,
        ioc_type: Optional[str] = None,
        status: Optional[str] = None,
    ) -> tuple[List[IOC], int]:
        query = db.query(IOC)
        
        if ioc_type:
            query = query.filter(IOC.ioc_type == ioc_type)
        if status:
            query = query.filter(IOC.status == status)
        
        total = query.count()
        iocs = query.order_by(IOC.created_at.desc()).offset(skip).limit(limit).all()
        return iocs, total

    @staticmethod
    def get_ioc_by_value(db: Session, value: str) -> Optional[IOC]:
        return db.query(IOC).filter(IOC.value == value).first()

    @staticmethod
    def get_ioc_by_id(db: Session, ioc_id: int) -> Optional[IOC]:
        return db.query(IOC).filter(IOC.id == ioc_id).first()

    @staticmethod
    def search_iocs(db: Session, search_term: str) -> List[IOC]:
        return db.query(IOC).filter(IOC.value.ilike(f"%{search_term}%")).all()

    @staticmethod
    def get_high_risk_iocs(db: Session) -> List[IOC]:
        return db.query(IOC).filter(IOC.risk_score >= 80).all()

    @staticmethod
    def update_ioc_reputation(db: Session, ioc_id: int, reputation: float) -> Optional[IOC]:
        ioc = db.query(IOC).filter(IOC.id == ioc_id).first()
        if not ioc:
            return None
        
        ioc.reputation = reputation
        ioc.updated_at = datetime.utcnow()
        db.commit()
        db.refresh(ioc)
        return ioc

    @staticmethod
    def add_tag_to_ioc(db: Session, ioc_id: int, tag: str) -> Optional[IOC]:
        ioc = db.query(IOC).filter(IOC.id == ioc_id).first()
        if not ioc:
            return None
        
        if ioc.tags is None:
            ioc.tags = []
        if tag not in ioc.tags:
            ioc.tags.append(tag)
        
        ioc.updated_at = datetime.utcnow()
        db.commit()
        db.refresh(ioc)
        return ioc

    @staticmethod
    def get_iocs_by_tag(db: Session, tag: str) -> List[IOC]:
        iocs = db.query(IOC).all()
        return [ioc for ioc in iocs if ioc.tags and tag in ioc.tags]
