import os
from datetime import date
from typing import Optional

from sqlalchemy import Date, String, create_engine, select
from sqlalchemy.orm import DeclarativeBase, Mapped, Session, mapped_column

from config import DB_PATH


class Base(DeclarativeBase):
    pass


class TaskBase(Base):
    __tablename__ = "tasks"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(30))
    description: Mapped[Optional[str]] = mapped_column(String(60))
    status: Mapped[str] = mapped_column(String(15), default="Not complete")
    created_at: Mapped[date] = mapped_column(Date, default=date.today)

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "status": self.status,
            "created_at": self.created_at,
        }


DB_URL = "sqlite:///data/tasks.db"
engine = create_engine(DB_URL, echo=True)
Base.metadata.create_all(engine)


def load_tasks():
    if (
        os.path.exists(DB_PATH) and os.path.getsize(DB_PATH) > 0
    ):  # Проверка на наличие файла и его размер
        with Session(engine) as session:
            stmt = select(TaskBase)
            tasks = session.execute(stmt).scalars().all()
            return tasks
    else:
        return []


def render_page():
    with Session(engine) as session:
        stmt = select(TaskBase)
        tasks = session.execute(stmt).scalars().all()
        # print(tasks)
        return tasks


dbtasks = load_tasks()
