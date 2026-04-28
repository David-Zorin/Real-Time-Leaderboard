import psycopg2
from app.core.config import settings
import os

def init_db():
    print("Initializing database...")
    try:
        conn = psycopg2.connect(settings.DATABASE_URL)
        with conn.cursor() as cur:
            # Read the schema.sql file
            schema_path = os.path.join("app", "db", "schema.sql")
            with open(schema_path, "r") as f:
                schema_sql = f.read()
            
            # Execute the SQL
            cur.execute(schema_sql)
            conn.commit()
            print("✅ Database tables created successfully!")
        conn.close()
    except Exception as e:
        print(f"❌ Error initializing database: {e}")

if __name__ == "__main__":
    init_db()
