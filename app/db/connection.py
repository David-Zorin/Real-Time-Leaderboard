from contextlib import contextmanager
import psycopg2.pool
import redis
from app.core.config import settings

# PostgreSQL Pool
try:
    db_pool = psycopg2.pool.ThreadedConnectionPool(1, 20, dsn=settings.DATABASE_URL)
    print("Database connection pool created successfully")
except Exception as e:
    print(f"Error creating connection pool: {e}")
    db_pool = None

# Redis Client
# decode_responses=True so Redis redis will return strings
redis_client = redis.from_url(settings.REDIS_URL, decode_responses=True)


@contextmanager
def get_db_connection():
    """
    Context manager to borrow a connection from the pool
    and return it automatically when finished.
    """
    conn = db_pool.getconn()
    try:
        yield conn
    finally:
        db_pool.putconn(conn)


def get_db():
    """FastAPI dependency that yields a database connection."""
    with get_db_connection() as conn:
        yield conn


def close_all_connections():
    """Gracefully shut down the pool when the server stops."""
    if db_pool:
        db_pool.closeall()
