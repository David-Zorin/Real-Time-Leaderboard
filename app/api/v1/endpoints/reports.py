from fastapi import APIRouter, Depends, Query
from app.services.report_service import ReportService
from app.db.connection import get_db

router = APIRouter()

@router.get("/top-players")
def get_periodic_report(days: int = Query(7, gt=0, le=30), db = Depends(get_db)):
    """
    Generate a report of the top players from the last X days.
    Default is 7 days, max is 30.
    """
    return ReportService.get_top_players_report(db, days)
