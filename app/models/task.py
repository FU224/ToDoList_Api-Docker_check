from sqlalchemy import Boolean, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from app.services.db import Base

        #SQLAlchemy как выглядит база таблицы
class Task(Base):
    __tablename__ = "tasks"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    is_done: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
