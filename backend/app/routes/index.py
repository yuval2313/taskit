from flask import render_template, redirect
from flask import current_app as app


@app.route("/")
def home():
    return redirect("/tasks")


@app.route("/tasks")
def serve_index():
    return render_template('index.html')
