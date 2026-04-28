from pydantic import BaseModel, Field

class GameCreate(BaseModel):
    title: str = Field(..., min_length=2, max_length=100)
    description: str = ""

class ScoreSubmit(BaseModel):
    game_id: int
    score: float = Field(..., gt=-1)

class LeaderboardEntry(BaseModel):
    rank: int
    username: str
    score: float
