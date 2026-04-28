from app.db.connection import redis_client
from app.schemas.score import LeaderboardEntry
from typing import List

class LeaderboardService:
    LEADERBOARD_KEY = "global_leaderboard"

    @classmethod
    def increment_score(cls, username: str, score: float):
        """
        Adds points to a user's total score in the real-time leaderboard.
        """
        redis_client.zincrby(cls.LEADERBOARD_KEY, score, username)

    @classmethod
    def get_top_players(cls, limit: int = 10) -> List[LeaderboardEntry]:
        """
        Retrieves the top N players from Redis.
        ZREVRANGE gives us the highest scores first.
        """
        raw_data = redis_client.zrevrange(
            cls.LEADERBOARD_KEY, 0, limit - 1, withscores=True
        )
        
        leaderboard = []
        for rank, (username, score) in enumerate(raw_data, start=1):
            leaderboard.append(
                LeaderboardEntry(
                    rank=rank,
                    username=username,
                    score=score
                )
            )
        return leaderboard

    @classmethod
    def get_user_rank(cls, username: str):
        """Gets the specific rank and score for a user."""
        score = redis_client.zscore(cls.LEADERBOARD_KEY, username)
        if score is None:
            return None
        
        # zrevrank is 0-indexed, so we add 1
        rank = redis_client.zrevrank(cls.LEADERBOARD_KEY, username)
        return {"username": username, "score": score, "rank": rank + 1}
