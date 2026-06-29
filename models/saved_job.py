from datetime import datetime

from extensions import db


class SavedJob(db.Model):

    __tablename__ = "saved_jobs"

    id = db.Column(db.Integer, primary_key=True)

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

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    # Prevent duplicate saves
    __table_args__ = (
        db.UniqueConstraint(
            "user_id",
            "job_id",
            name="uq_saved_job"
        ),
    )

    # Relationships
    user = db.relationship(
        "User",
        backref=db.backref(
            "saved_jobs",
            lazy=True,
            cascade="all, delete-orphan"
        )
    )

    job = db.relationship(
        "Job",
        backref=db.backref(
            "saved_by_users",
            lazy=True,
            cascade="all, delete-orphan"
        )
    )

    def __repr__(self):
        return f"<SavedJob User:{self.user_id} Job:{self.job_id}>"