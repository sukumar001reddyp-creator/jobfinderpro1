from datetime import datetime

from extensions import db


class JobSource(db.Model):

    __tablename__ = "job_sources"

    id = db.Column(db.Integer, primary_key=True)

    # Source Information
    name = db.Column(db.String(100), nullable=False, unique=True)

    source_type = db.Column(db.String(50), nullable=False)

    website = db.Column(db.String(255))

    description = db.Column(db.Text)

    # Connector Support
    api_available = db.Column(db.Boolean, default=False)

    rss_available = db.Column(db.Boolean, default=False)

    # Future Connector Settings
    api_endpoint = db.Column(db.String(500))

    api_key_required = db.Column(db.Boolean, default=False)

    # Status
    is_active = db.Column(db.Boolean, default=True)

    # Dates
    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    updated_at = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow
    )

    # Relationships
    jobs = db.relationship(
        "Job",
        back_populates="job_source",
        lazy=True,
        cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"<JobSource {self.name}>"