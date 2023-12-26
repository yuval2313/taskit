from datetime import datetime
from marshmallow import Schema, fields, validate
from flask import current_app as app
from app import db
from app.errors.http import CustomHTTPException


# Database Model
class Task(db.Model):
    __tablename__ = "tasks"

    id = db.Column(
        db.Integer,
        primary_key=True
    )
    title = db.Column(
        db.String(255),
        nullable=False
    )
    body = db.Column(
        db.Text,
        nullable=False
    )
    status_done = db.Column(
        db.Boolean,
        nullable=False,
        default=False
    )
    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )
    updated_at = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow
    )

    def __repr__(self):
        return '<Task (id={}, title={})>'.format(self.id, self.title)

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'body': self.body,
            'status_done': self.status_done,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }


# Request Body Schema
class TaskSchema(Schema):
    title = fields.Str(required=True, validate=validate.Length(max=255))
    body = fields.Str(required=True)
    status_done = fields.Bool(required=True, truthy={True}, falsy={False})


def validate_task_req(data: dict):
    schema = TaskSchema()

    errors = schema.validate(data)
    if errors:
        app.logger.warning("Invalid task in request body, raising exception")
        raise CustomHTTPException(
            description="Validation Error", code=400, payload=errors)
