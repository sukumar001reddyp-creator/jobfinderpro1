from datetime import datetime

from extensions import db


class AppliedJob(db.Model):

    __tablename__ = "applied_jobs"

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

    status = db.Column(
        db.String(30),
        default="Applied"
    )

    notes = db.Column(db.Text)

    applied_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    updated_at = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow
    )

    __table_args__ = (
        db.UniqueConstraint(
            "user_id",
            "job_id",
            name="uq_applied_job"
        ),
    )

    # Relationships
    user = db.relationship(
        "User",
        backref=db.backref(
            "applied_jobs",
            lazy=True,
            cascade="all, delete-orphan"
        )
    )

    job = db.relationship(
        "Job",
        backref=db.backref(
            "applications",
            lazy=True,
            cascade="all, delete-orphan"
        )
    )

    def __repr__(self):
        return f"<AppliedJob User:{self.user_id} Job:{self.job_id}>"