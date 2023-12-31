from flask import redirect
from flask import current_app as app


@app.route("/")
def home():
    return redirect("/tasks")


@app.route("/tasks")
def serve_index():
    return app.send_static_file('index.html')
