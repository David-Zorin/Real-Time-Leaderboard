import os
from dotenv import load_dotenv

load_dotenv()


class Settings:
    PROJECT_NAME: str = "Real-Time Leaderboard"
    DATABASE_URL: str = os.getenv(
        "DATABASE_URL",
        "postgresql://leaderboard_user:leaderboard_pass@localhost:5432/leaderboard_db",
    )
    REDIS_URL: str = os.getenv("REDIS_URL", "redis://localhost:6379/0")
    SECRET_KEY: str = os.getenv("SECRET_KEY", "my-secret-key-for-jwt-generation")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24  # expire time - 1 day


settings = Settings()
