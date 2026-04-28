from pydantic import BaseModel, Field

class ScoreSubmit(BaseModel):
    game_id: int
    score: float = Field(..., gt=-1)

class LeaderboardEntry(BaseModel):
    rank: int
    username: str
    score: float
