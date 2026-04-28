import random
from app.db.connection import get_db_connection
from app.services.auth_service import AuthService
from app.services.game_service import GameService, ScoreService
from app.schemas.auth import RegisterRequest
from app.schemas.score import GameCreate


def seed():
    print("🌱 Seeding fake data...")
    with get_db_connection() as conn:
        # 1. Create Games
        try:
            g1 = GameService.create_game(
                conn, GameCreate(title="Galactic Wars", description="Space shooter")
            )
            g2 = GameService.create_game(
                conn, GameCreate(title="Speed Racer", description="Racing game")
            )
            game_ids = [g1["id"], g2["id"]]
        except Exception as e:
            print(f"⚠️ Games might already exist, fetching existing IDs...")
            with conn.cursor() as cur:
                cur.execute("SELECT id FROM games")
                game_ids = [row[0] for row in cur.fetchall()]

        # 2. Create Users & Scores
        users = [
            ("player_one", "one@test.com"),
            ("pro_gamer", "pro@test.com"),
            ("noob_master", "noob@test.com"),
            ("pixel_king", "pixel@test.com"),
            ("fast_finger", "fast@test.com"),
        ]

        for username, email in users:
            print(f"Processing user: {username}...")
            # Try to register
            try:
                AuthService.register_user(
                    conn,
                    RegisterRequest(
                        username=username, email=email, password="password123"
                    ),
                )
                print(f"Created new user {username}")
            except Exception:
                print(f"  ℹ️ User {username} already exists")

            # Fetch the user id (needed for scores)
            with conn.cursor() as cur:
                cur.execute("SELECT id FROM users WHERE username = %s", (username,))
                row = cur.fetchone()
                if not row:
                    print(f"Error: Could not find/create user {username}")
                    continue
                user_id = row[0]

            # 3. Submit random scores
            for _ in range(3):
                score = round(random.uniform(10, 500), 1)
                game_id = random.choice(game_ids)
                try:
                    ScoreService.submit_score(conn, user_id, username, game_id, score)
                    print(f"Added {score} pts to {username}")
                except Exception as e:
                    print(f"Failed to add score for {username}: {e}")

    print("\n Seeding process finished!")


if __name__ == "__main__":
    seed()
