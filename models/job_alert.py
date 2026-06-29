from datetime import datetime

from extensions import db


class JobAlert(db.Model):

    __tablename__ = "job_alerts"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False
    )

    keyword = db.Column(
        db.String(150),
        nullable=False
    )

    location = db.Column(
        db.String(150)
    )

    employment_type = db.Column(
        db.String(100)
    )

    remote = db.Column(
        db.Boolean,
        default=False
    )

    frequency = db.Column(
        db.String(20),
        default="daily"
    )

    is_active = db.Column(
        db.Boolean,
        default=True
    )

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    user = db.relationship(
        "User",
        backref="job_alerts"
    )