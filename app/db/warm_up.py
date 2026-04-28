from app.db.connection import get_db_connection, redis_client
from app.services.leaderboard_service import LeaderboardService
from psycopg2.extras import RealDictCursor


def warm_up_cache():
    print("🔥 Warming up Redis cache from PostgreSQL...")

    query = """
        SELECT u.username, SUM(s.score) as total_score
        FROM scores s
        JOIN users u ON s.user_id = u.id
        GROUP BY u.username
    """

    try:
        with get_db_connection() as conn:
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute(query)
                results = cur.fetchall()

                if not results:
                    print("ℹ️ No scores found in database to sync.")
                    return

                # Clear existing leaderboard to avoid duplicates/stale data
                redis_client.delete(LeaderboardService.LEADERBOARD_KEY)

                for row in results:
                    # Sync to Redis
                    LeaderboardService.update_score(
                        row["username"], float(row["total_score"])
                    )
                    print(f"Synced {row['username']}: {row['total_score']} pts")

        print("✨ Redis cache is now synchronized with the database!")
    except Exception as e:
        print(f"Error during cache warm-up: {e}")


if __name__ == "__main__":
    warm_up_cache()
