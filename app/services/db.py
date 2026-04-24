import os
import time

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

#SQLAlch база
class Base(DeclarativeBase):
    pass

#connect
def get_database_url():
    host = os.getenv("DB_HOST", "db")
    port = os.getenv("DB_PORT", "5432")
    db_name = os.getenv("DB_NAME", "todo_db")
    user = os.getenv("DB_USER", "todo_user")
    password = os.getenv("DB_PASSWORD", "111")
    return f"postgresql+psycopg2://{user}:{password}@{host}:{port}/{db_name}"

#запросы, сессии
engine = create_engine(get_database_url(), future=True)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False, future=True)


def wait_for_db(max_retries=10, delay=3):
    for attempt in range(1, max_retries + 1):
        try:
            with engine.connect():
                return
        except Exception:
            if attempt == max_retries:
                raise
            print(f"Database is not ready yet. Retry {attempt}/{max_retries}...")
            time.sleep(delay)


def get_session():
    return SessionLocal()

# глав. запуск
def init_db():
    from app.models.task import Task  

    wait_for_db()
    Base.metadata.create_all(bind=engine)
