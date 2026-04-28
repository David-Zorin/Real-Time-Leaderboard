from psycopg2.extras import RealDictCursor
from datetime import datetime, timedelta

class ReportService:
    @staticmethod
    def get_top_players_report(conn, days: int = 7):
        """
        Calculates who earned the most points in the last N days.
        This uses SQL 'SUM' and 'GROUP BY'.
        """
        # Calculate the date 'N' days ago
        since_date = datetime.now() - timedelta(days=days)

        query = """
            SELECT u.username, SUM(s.score) as total_score
            FROM scores s
            JOIN users u ON s.user_id = u.id
            WHERE s.submitted_at >= %s
            GROUP BY u.username
            ORDER BY total_score DESC
            LIMIT 10
        """
        
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(query, (since_date,))
            return cur.fetchall()
