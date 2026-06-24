from sqlalchemy.orm import Session
from models.report import Report
from schemas.report import ReportCreate, ReportUpdate
from typing import Optional, List

class ReportService:
    
    @staticmethod
    def get_report_by_id(db: Session, report_id: int) -> Optional[Report]:
        return db.query(Report).filter(Report.id == report_id).first()
    
    @staticmethod
    def get_all_reports(db: Session, skip: int = 0, limit: int = 100) -> List[Report]:
        return db.query(Report).offset(skip).limit(limit).all()
    
    @staticmethod
    def get_reports_by_type(db: Session, report_type: str, skip: int = 0, limit: int = 100) -> List[Report]:
        return db.query(Report).filter(Report.report_type == report_type).offset(skip).limit(limit).all()
    
    @staticmethod
    def get_reports_by_user(db: Session, user_id: int, skip: int = 0, limit: int = 100) -> List[Report]:
        return db.query(Report).filter(Report.generated_by == user_id).offset(skip).limit(limit).all()
    
    @staticmethod
    def create_report(db: Session, report: ReportCreate, generated_by: int) -> Report:
        db_report = Report(
            **report.dict(),
            generated_by=generated_by
        )
        db.add(db_report)
        db.commit()
        db.refresh(db_report)
        return db_report
    
    @staticmethod
    def update_report(db: Session, report_id: int, report_update: ReportUpdate) -> Optional[Report]:
        db_report = ReportService.get_report_by_id(db, report_id)
        if not db_report:
            return None
        
        update_data = report_update.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_report, field, value)
        
        db.add(db_report)
        db.commit()
        db.refresh(db_report)
        return db_report
    
    @staticmethod
    def delete_report(db: Session, report_id: int) -> bool:
        db_report = ReportService.get_report_by_id(db, report_id)
        if not db_report:
            return False
        
        db.delete(db_report)
        db.commit()
        return True
