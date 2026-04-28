from fastapi import FastAPI
from app.api.v1.api import api_router
from app.core.config import settings
from app.db.connection import close_all_connections

app = FastAPI(title=settings.PROJECT_NAME)

# Include all our modular routes
app.include_router(api_router, prefix="/api/v1")

@app.get("/")
def root():
    return {"message": "Welcome to the Real-Time Leaderboard API"}

@app.on_event("shutdown")
def shutdown_event():
    # Gracefully close DB connections when the server stops
    close_all_connections()
