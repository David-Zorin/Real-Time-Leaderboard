from fastapi import APIRouter, Depends, status
from app.schemas.auth import RegisterRequest, LoginRequest, TokenResponse
from app.services.auth_service import AuthService
from app.db.connection import get_db

router = APIRouter()

@router.post("/register", status_code=status.HTTP_201_CREATED)
def register(user_data: RegisterRequest, db = Depends(get_db)):
    """Registers a new user account."""
    return AuthService.register_user(db, user_data)

@router.post("/login", response_model=TokenResponse)
def login(login_data: LoginRequest, db = Depends(get_db)):
    """Authenticates user and returns JWT token."""
    return AuthService.authenticate_user(db, login_data)
