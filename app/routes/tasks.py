from flask import request, jsonify
from flask import current_app as app
from app.models.task import validate_task_req
from app.services import tasks_service


@app.get("/api/tasks")
def get_tasks():
    app.logger.info("Handling GET /api/tasks request")
    tasks = tasks_service.select_tasks()

    app.logger.info("Returning tasks in response")
    return jsonify([task.to_dict() for task in tasks])


@app.get("/api/tasks/<int:task_id>")
def get_task_by_id(task_id: int):
    app.logger.info("Handling GET /api/tasks/<id> request")

    task = tasks_service.select_task_by_id(task_id)

    app.logger.info("Returning task in response")
    return jsonify(task.to_dict())


@app.post("/api/tasks")
def create_task():
    app.logger.info("Handling POST /api/tasks request")

    data: dict = request.get_json()

    app.logger.info("Validating request body")
    validate_task_req(data)

    task = tasks_service.insert_task(data)

    app.logger.info("Returning task in response")
    return jsonify(task.to_dict()), 201


@app.put("/api/tasks/<int:task_id>")
def update_task(task_id: int):
    app.logger.info("Handling PUT /api/tasks/<id> request")
    data: dict = request.get_json()

    app.logger.info("Validating request body")
    validate_task_req(data)

    task = tasks_service.update_task(data, task_id)

    app.logger.info("Returning task in response")
    return jsonify(task.to_dict())


@app.delete("/api/tasks/<int:task_id>")
def delete_task(task_id):
    app.logger.info("Handling DELETE /api/tasks/<id> request")

    task = tasks_service.delete_task(task_id)

    app.logger.info("Returning task in response")
    return jsonify(task.to_dict())
