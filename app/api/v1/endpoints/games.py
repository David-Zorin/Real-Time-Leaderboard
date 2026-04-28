from fastapi import APIRouter, Depends, status
from typing import List
from app.schemas.score import GameCreate, ScoreSubmit
from app.services.game_service import GameService, ScoreService
from app.db.connection import get_db
from app.api.deps import get_current_user

router = APIRouter()

@router.post("/", status_code=status.HTTP_201_CREATED)
def create_game(game_data: GameCreate, db = Depends(get_db), current_user = Depends(get_current_user)):
    """Only authenticated users can register a new game."""
    return GameService.create_game(db, game_data)

@router.get("/")
def list_games(db = Depends(get_db)):
    """Anyone can see the list of games."""
    return GameService.list_games(db)

@router.post("/scores", status_code=status.HTTP_201_CREATED)
def submit_score(score_data: ScoreSubmit, db = Depends(get_db), current_user = Depends(get_current_user)):
    """
    Submits a score for the current logged-in user.
    We pass both ID (for DB) and Username (for Redis leaderboard).
    """
    return ScoreService.submit_score(
        db, 
        current_user["id"], 
        current_user["username"], 
        score_data.game_id, 
        score_data.score
    )
