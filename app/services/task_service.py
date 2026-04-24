from sqlalchemy import select

from app.models.task import Task
from app.schemas.task import TaskResponse
from app.services.db import get_session


def get_all_tasks():
    with get_session() as session:
        tasks = session.scalars(select(Task).order_by(Task.id)).all()
        return [TaskResponse.model_validate(task) for task in tasks]


def get_unfinished_tasks():
    with get_session() as session:
        tasks = session.scalars(
            select(Task).where(Task.is_done.is_(False)).order_by(Task.id)
        ).all()
        return [TaskResponse.model_validate(task) for task in tasks]


def create_task(title):
    with get_session() as session:
        task = Task(title=title)
        session.add(task)
        session.commit()
        session.refresh(task)
        return TaskResponse.model_validate(task)


def toggle_task_status(task_id):
    with get_session() as session:
        task = session.get(Task, task_id)
        if not task:
            return None

        task.is_done = not task.is_done
        session.commit()
        session.refresh(task)
        return TaskResponse.model_validate(task)


def delete_task_by_id(task_id):
    with get_session() as session:
        task = session.get(Task, task_id)
        if not task:
            return False

        session.delete(task)
        session.commit()
        return True
