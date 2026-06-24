from fastapi import APIRouter, Depends, HTTPException, Request, status
from sqlalchemy.orm import Session

from schemas.report import ReportCreate, ReportResponse, ReportUpdate
from services.report_service import ReportService
from services.audit_service import AuditService
from core.database import get_db
from core.rbac import Resource, Action, require_permission, get_client_ip
from core.audit_actions import AuditAction
from models.user import User

router = APIRouter(prefix="/reports", tags=["Reports"])


def _audit_meta(request: Request) -> dict:
    return {
        "ip_address": get_client_ip(request),
        "user_agent": request.headers.get("User-Agent"),
    }


@router.post("", response_model=ReportResponse, status_code=status.HTTP_201_CREATED)
def create_report(
    report: ReportCreate,
    request: Request,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_permission(Resource.REPORTS, Action.CREATE)),
):
    """Create a new report."""
    new_report = ReportService.create_report(db, report, current_user.id)
    AuditService.log_from_user(
        db,
        current_user,
        AuditAction.REPORT_CREATE.value,
        entity_type="Report",
        entity_id=new_report.id,
        new_value=report.model_dump(),
        **_audit_meta(request),
    )
    return new_report


@router.get("/{report_id}", response_model=ReportResponse)
def get_report(
    report_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_permission(Resource.REPORTS, Action.READ)),
):
    """Get report by ID."""
    report = ReportService.get_report_by_id(db, report_id)
    if not report:
        raise HTTPException(status_code=404, detail="Report not found")
    return report


@router.get("", response_model=list[ReportResponse])
def get_all_reports(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_permission(Resource.REPORTS, Action.READ)),
):
    """Get all reports."""
    return ReportService.get_all_reports(db, skip, limit)


@router.get("/type/{report_type}", response_model=list[ReportResponse])
def get_reports_by_type(
    report_type: str,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_permission(Resource.REPORTS, Action.READ)),
):
    """Get reports by type."""
    return ReportService.get_reports_by_type(db, report_type, skip, limit)


@router.get("/user/{user_id}", response_model=list[ReportResponse])
def get_reports_by_user(
    user_id: int,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_permission(Resource.REPORTS, Action.READ)),
):
    """Get reports by user."""
    return ReportService.get_reports_by_user(db, user_id, skip, limit)


@router.put("/{report_id}", response_model=ReportResponse)
def update_report(
    report_id: int,
    report_update: ReportUpdate,
    request: Request,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_permission(Resource.REPORTS, Action.UPDATE)),
):
    """Update report by ID."""
    report = ReportService.update_report(db, report_id, report_update)
    if not report:
        raise HTTPException(status_code=404, detail="Report not found")
    AuditService.log_from_user(
        db,
        current_user,
        AuditAction.REPORT_UPDATE.value,
        entity_type="Report",
        entity_id=report_id,
        new_value=report_update.model_dump(exclude_unset=True),
        **_audit_meta(request),
    )
    return report


@router.delete("/{report_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_report(
    report_id: int,
    request: Request,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_permission(Resource.REPORTS, Action.DELETE)),
):
    """Delete report by ID."""
    success = ReportService.delete_report(db, report_id)
    if not success:
        raise HTTPException(status_code=404, detail="Report not found")
    AuditService.log_from_user(
        db,
        current_user,
        AuditAction.REPORT_DELETE.value,
        entity_type="Report",
        entity_id=report_id,
        **_audit_meta(request),
    )
    return None
