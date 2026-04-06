from fastapi import FastAPI, Depends
from db.connection import get_connection

app = FastAPI(title="Real-Time Leaderboard")


def get_db():
    conn = get_connection()
    try:
        yield conn
    finally:
        conn.close()


@app.get("/")
def root(db=Depends(get_db)):
    return "Server is running and db is connected"
