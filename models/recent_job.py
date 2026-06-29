from datetime import datetime

from extensions import db


class RecentJob(db.Model):

    __tablename__ = "recent_jobs"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False
    )

    job_id = db.Column(
        db.Integer,
        db.ForeignKey("jobs.id"),
        nullable=False
    )

    viewed_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    user = db.relationship(
        "User",
        backref="recent_jobs"
    )

    job = db.relationship(
        "Job",
        backref="recent_views"
    )