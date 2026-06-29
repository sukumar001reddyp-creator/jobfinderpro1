from datetime import datetime

from extensions import db


class Company(db.Model):

    __tablename__ = "companies"

    id = db.Column(db.Integer, primary_key=True)

    # Basic Information
    name = db.Column(db.String(150), nullable=False, unique=True)
    slug = db.Column(db.String(180), nullable=False, unique=True)

    logo = db.Column(db.String(255))
    website = db.Column(db.String(255))

    # Company Details
    industry = db.Column(db.String(100))
    company_size = db.Column(db.String(50))

    country = db.Column(db.String(100))
    state = db.Column(db.String(100))
    city = db.Column(db.String(100))

    description = db.Column(db.Text)

    # Contact
    email = db.Column(db.String(255))
    phone = db.Column(db.String(30))

    # Social Media
    linkedin_url = db.Column(db.String(255))

    # Status
    verified = db.Column(db.Boolean, default=False)
    is_active = db.Column(db.Boolean, default=True)

    # Timestamps
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
        back_populates="company",
        lazy=True,
        cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"<Company {self.name}>"