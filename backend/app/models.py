from . import db
from datetime import datetime


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
        default=False
    )
    created_at = db.Column(
        db.DateTime,
        default=datetime.now()
    )
    updated_at = db.Column(
        db.DateTime,
        default=datetime.now(),
        onupdate=datetime.now()
    )

    def __repr__(self):
        return '<Task (id={}, title={})>'.format(self.id, self.title)

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'body': self.body,
            'status_done': self.status_done,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }
