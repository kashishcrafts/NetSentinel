from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from schemas.report import ReportCreate, ReportResponse, ReportUpdate
from services.report_service import ReportService
from core.database import get_db

router = APIRouter(prefix="/reports", tags=["Reports"])

@router.post("", response_model=ReportResponse, status_code=status.HTTP_201_CREATED)
def create_report(report: ReportCreate, generated_by: int = 1, db: Session = Depends(get_db)):
    """Create a new report."""
    new_report = ReportService.create_report(db, report, generated_by)
    return new_report

@router.get("/{report_id}", response_model=ReportResponse)
def get_report(report_id: int, db: Session = Depends(get_db)):
    """Get report by ID."""
    report = ReportService.get_report_by_id(db, report_id)
    if not report:
        raise HTTPException(status_code=404, detail="Report not found")
    return report

@router.get("", response_model=list[ReportResponse])
def get_all_reports(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Get all reports."""
    reports = ReportService.get_all_reports(db, skip, limit)
    return reports

@router.get("/type/{report_type}", response_model=list[ReportResponse])
def get_reports_by_type(report_type: str, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Get reports by type."""
    reports = ReportService.get_reports_by_type(db, report_type, skip, limit)
    return reports

@router.get("/user/{user_id}", response_model=list[ReportResponse])
def get_reports_by_user(user_id: int, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Get reports by user."""
    reports = ReportService.get_reports_by_user(db, user_id, skip, limit)
    return reports

@router.put("/{report_id}", response_model=ReportResponse)
def update_report(report_id: int, report_update: ReportUpdate, db: Session = Depends(get_db)):
    """Update report by ID."""
    report = ReportService.update_report(db, report_id, report_update)
    if not report:
        raise HTTPException(status_code=404, detail="Report not found")
    return report

@router.delete("/{report_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_report(report_id: int, db: Session = Depends(get_db)):
    """Delete report by ID."""
    success = ReportService.delete_report(db, report_id)
    if not success:
        raise HTTPException(status_code=404, detail="Report not found")
    return None
