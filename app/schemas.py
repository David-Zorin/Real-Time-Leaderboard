from pydantic import BaseModel, EmailStr, Field


# --- Auth ---
class RegisterRequest(BaseModel):
    username: str = Field(..., min_lenght=4)
    email: EmailStr
    password: str = Field(..., min_length=6)


class LoginRequest(BaseModel):
    username: str
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


# --- Scores ---
class ScoreSubmit(BaseModel):
    game_id: int
    score: float = Field(..., gt=-1)


# --- Leaderboard ---
class LeaderboardEntry(BaseModel):
    rank: int
    username: str
    score: float
