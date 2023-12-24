from os import getenv
from taskit import create_app
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from sqlalchemy.orm import mapped_column

app = create_app()
db = SQLAlchemy(app)
migrate = Migrate(app, db)


# db models
class Task(db.Model):
    __tablename__ = "tasks"

    id = mapped_column(db.Integer, primary_key=True)
    title = mapped_column(db.String(100), nullable=False)
    body = mapped_column(db.String(1000), nullable=False)
    status_done = mapped_column(db.Boolean, default=False, nullable=False)
    created_at = mapped_column(db.DateTime, default=datetime.now())
    updated_at = mapped_column(db.DateTime, default=datetime.now())


# routes
@app.route("/hello")
def hello():
    return "Hello World!"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=getenv("PORT", "5000"))
