from fastapi import APIRouter, Depends, Query
from typing import List, Optional
from app.schemas.score import LeaderboardEntry
from app.services.leaderboard_service import LeaderboardService
from app.api.deps import get_current_user

router = APIRouter()

@router.get("/", response_model=List[LeaderboardEntry])
def get_global_leaderboard(limit: int = Query(10, gt=0, le=100)):
    """
    Returns the top players across all games.
    Default limit is 10, max is 100.
    """
    return LeaderboardService.get_top_players(limit)

@router.get("/me")
def get_my_rank(current_user = Depends(get_current_user)):
    """
    Returns the rank and total score of the logged-in user.
    """
    stats = LeaderboardService.get_user_rank(current_user["username"])
    if not stats:
        return {"message": "No scores recorded yet", "username": current_user["username"]}
    return stats
