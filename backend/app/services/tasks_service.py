from typing import List
from app.models.task import Task, db
from app.errors.http import CustomHTTPException


def select_tasks():
    tasks: List[Task] = Task.query.all()

    if len(tasks) == 0:
        raise CustomHTTPException(description="No tasks found", code=404)

    return tasks


def select_task_by_id(task_id: int):
    task: Task = Task.query.get(task_id)

    if task is None:
        raise CustomHTTPException(
            description="Task with the given id not found", code=404)

    return task


def insert_task(data: dict):
    task = Task(**data)

    db.session.add(task)
    db.session.commit()

    return task


def update_task(data: dict, task_id: int):
    task = select_task_by_id(task_id)

    task.title = data.get('title', task.title)
    task.body = data.get('body', task.body)
    task.status_done = data.get('status_done', task.status_done)

    db.session.commit()

    return task


def delete_task(task_id: int):
    task = select_task_by_id(task_id)

    db.session.delete(task)
    db.session.commit()

    return task
