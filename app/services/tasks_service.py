from typing import List
from flask import current_app as app
from app.models.task import Task, db
from app.errors.http import CustomHTTPException


def select_tasks():
    app.logger.debug("Retrieving tasks from database")
    tasks: List[Task] = Task.query.all()

    if len(tasks) == 0:
        app.logger.warning(
            "No tasks found in database, raising HTTP exception")
        raise CustomHTTPException(description="No tasks found", code=404)

    app.logger.debug("Successfully retrieved tasks from database")
    return tasks


def select_task_by_id(task_id: int):
    app.logger.debug("Retrieving task from database by id")
    task: Task = Task.query.get(task_id)

    if task is None:
        app.logger.warning("No task found in database, raising HTTP exception")
        raise CustomHTTPException(
            description="Task with the given id not found", code=404)

    app.logger.debug("Successfully retrieved task from database")
    return task


def insert_task(data: dict):
    app.logger.debug("Creating Task object from request body")
    task = Task(**data)

    app.logger.debug("Inserting task into database")
    db.session.add(task)
    db.session.commit()

    app.logger.debug("Successfully inserted task into database")
    return task


def update_task(data: dict, task_id: int):
    task = select_task_by_id(task_id)

    app.logger.debug("Updating task from request body")
    task.title = data.get('title', task.title)
    task.body = data.get('body', task.body)
    task.status_done = data.get('status_done', task.status_done)

    app.logger.debug("Saving updated task into database")
    db.session.commit()

    app.logger.debug("Successfuly updated and saved task into database")
    return task


def delete_task(task_id: int):
    task = select_task_by_id(task_id)

    app.logger.debug("Deleting task from database")
    db.session.delete(task)
    db.session.commit()

    app.logger.debug("Successfully deleted task from database")
    return task
