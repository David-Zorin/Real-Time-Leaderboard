from app.schemas.score import GameCreate
from psycopg2.extras import RealDictCursor
from fastapi import HTTPException, status

class GameService:
    @staticmethod
    def create_game(conn, game_in: GameCreate):
        """Adds a new game to the system using the Schema."""
        try:
            with conn.cursor() as cur:
                cur.execute(
                    "INSERT INTO games (title, description) VALUES (%s, %s) RETURNING id",
                    (game_in.title, game_in.description)
                )
                game_id = cur.fetchone()[0]
                conn.commit()
                return {"id": game_id, "title": game_in.title, "message": "Game created successfully"}
        except Exception as e:
            conn.rollback()
            raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

    @staticmethod
    def list_games(conn):
        """Returns all available games."""
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute("SELECT * FROM games ORDER BY created_at DESC")
            return cur.fetchall()

class ScoreService:
    @staticmethod
    def submit_score(conn, user_id: int, game_id: int, score: float):
        """
        Records a player's score. 
        In a real-time system, we'd also update Redis here (we'll do that in the next step!).
        """
        try:
            with conn.cursor() as cur:
                # 1. Verify game exists
                cur.execute("SELECT id FROM games WHERE id = %s", (game_id,))
                if not cur.fetchone():
                    raise HTTPException(status_code=404, detail="Game not found")

                # 2. Insert the score
                cur.execute(
                    "INSERT INTO scores (user_id, game_id, score) VALUES (%s, %s, %s) RETURNING id",
                    (user_id, game_id, score)
                )
                conn.commit()
                return {"message": "Score submitted successfully"}
        except Exception as e:
            conn.rollback()
            if isinstance(e, HTTPException): raise e
            raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
