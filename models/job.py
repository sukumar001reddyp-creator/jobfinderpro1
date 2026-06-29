from datetime import datetime

from extensions import db


class Job(db.Model):

    __tablename__ = "jobs"

    id = db.Column(db.Integer, primary_key=True)

    # -------------------------
    # Basic Information
    # -------------------------
    title = db.Column(db.String(255), nullable=False)
    slug = db.Column(db.String(300), unique=True, nullable=False)

    # Original source job ID (helps avoid duplicate jobs)
    source_job_id = db.Column(db.String(255), unique=True)

    # -------------------------
    # Relationships
    # -------------------------
    company_id = db.Column(
        db.Integer,
        db.ForeignKey("companies.id"),
        nullable=False
    )

    job_source_id = db.Column(
        db.Integer,
        db.ForeignKey("job_sources.id"),
        nullable=False
    )

    # -------------------------
    # Job Details
    # -------------------------
    description = db.Column(db.Text, nullable=False)

    category = db.Column(db.String(100))
    industry = db.Column(db.String(100))
    skills = db.Column(db.Text)

    country = db.Column(db.String(100))
    state = db.Column(db.String(100))
    city = db.Column(db.String(100))

    remote = db.Column(db.Boolean, default=False)

    experience_level = db.Column(db.String(50))
    experience_min = db.Column(db.Integer)
    experience_max = db.Column(db.Integer)

    employment_type = db.Column(db.String(50))

    # -------------------------
    # Salary
    # -------------------------
    salary_min = db.Column(db.Integer)
    salary_max = db.Column(db.Integer)

    salary_type = db.Column(db.String(20))      # Monthly / Yearly / Hourly
    currency = db.Column(db.String(10))

    # -------------------------
    # Apply
    # -------------------------
    apply_url = db.Column(db.String(500), nullable=False)

    # -------------------------
    # Status
    # -------------------------
    status = db.Column(
        db.String(20),
        default="active"
    )

    is_active = db.Column(
        db.Boolean,
        default=True
    )

    # -------------------------
    # Dates
    # -------------------------
    posted_date = db.Column(db.DateTime)

    expires_at = db.Column(db.DateTime)

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    updated_at = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow
    )

    # -------------------------
    # Relationships
    # -------------------------
    company = db.relationship(
        "Company",
        back_populates="jobs"
    )

    job_source = db.relationship(
        "JobSource",
        back_populates="jobs"
    )

    # -------------------------
    # String Representation
    # -------------------------
    def __repr__(self):
        return f"<Job {self.title}>"