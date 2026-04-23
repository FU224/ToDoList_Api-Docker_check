import os
import time

import psycopg2
from psycopg2.extras import RealDictCursor


def get_connection(max_retries=10, delay=3):
    db_config = {
        "host": os.getenv("DB_HOST", "db"),
        "port": os.getenv("DB_PORT", "5432"),
        "dbname": os.getenv("DB_NAME", "todo_db"),
        "user": os.getenv("DB_USER", "todo_user"),
        "password": os.getenv("DB_PASSWORD", "todo_password"),
    }

    for attempt in range(1, max_retries + 1):
        try:
            return psycopg2.connect(cursor_factory=RealDictCursor, **db_config)
        except psycopg2.OperationalError:
            if attempt == max_retries:
                raise
            print(f"Database is not ready yet. Retry {attempt}/{max_retries}...")
            time.sleep(delay)


def init_db():
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                CREATE TABLE IF NOT EXISTS tasks (
                    id SERIAL PRIMARY KEY,
                    title VARCHAR(255) NOT NULL,
                    is_done BOOLEAN NOT NULL DEFAULT FALSE
                )
                """
            )
        conn.commit()
