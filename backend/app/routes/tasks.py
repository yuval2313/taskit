from flask import request, jsonify
from flask import current_app as app
from app.models.task import validate_task_req
from app.services import tasks_service


@app.get("/tasks")
def get_tasks():
    tasks = tasks_service.select_tasks()

    return jsonify([task.to_dict() for task in tasks])


@app.get("/tasks/<int:task_id>")
def get_task_by_id(task_id: int):
    task = tasks_service.select_task_by_id(task_id)

    return jsonify(task.to_dict())


@app.post("/tasks")
def create_task():
    data: dict = request.get_json()

    validate_task_req(data)

    task = tasks_service.insert_task(data)

    return jsonify(task.to_dict()), 201


@app.put("/tasks/<int:task_id>")
def update_task(task_id: int):
    data: dict = request.get_json()

    validate_task_req(data)

    task = tasks_service.update_task(data, task_id)

    return jsonify(task.to_dict())


@app.delete("/tasks/<int:task_id>")
def delete_task(task_id):
    task = tasks_service.delete_task(task_id)

    return jsonify(task.to_dict())
