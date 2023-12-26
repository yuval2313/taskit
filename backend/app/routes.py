from datetime import datetime
from flask import request, jsonify
from app.models import Task, db
from flask import current_app as app


@app.get("/tasks")
def get_tasks():
    query_result = Task.query.all()

    tasks = [task.to_dict() for task in query_result]

    return jsonify(tasks)


@app.post("/tasks")
def create_task():
    data = request.get_json()
    current_time = datetime.now()

    data['created_at'] = current_time
    data['updated_at'] = current_time

    task = Task(**data)

    db.session.add(task)
    db.session.commit()

    return jsonify(data), 201


@app.put("/tasks/<int:id>")
def update_task():
    data = request.get_json()
    current_time = datetime.now()

    task = db.get_or_404(Task, id)

    task['updated_at'] = current_time

    db.session.commit()

    return jsonify(data)
