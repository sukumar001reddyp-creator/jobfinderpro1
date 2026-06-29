from datetime import datetime

from extensions import db


class Alert(db.Model):

    __tablename__ = "alerts"

    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False
    )

    keyword = db.Column(db.String(255), nullable=False)

    location = db.Column(db.String(255))

    category = db.Column(db.String(100))

    company = db.Column(db.String(150))

    employment_type = db.Column(db.String(50))

    experience_level = db.Column(db.String(50))

    remote = db.Column(db.Boolean, default=False)

    frequency = db.Column(
        db.String(20),
        default="daily"
    )  # daily / weekly

    is_active = db.Column(
        db.Boolean,
        default=True
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

    # Relationship
    user = db.relationship(
        "User",
        backref=db.backref(
            "alerts",
            lazy=True,
            cascade="all, delete-orphan"
        )
    )

    def __repr__(self):
        return f"<Alert {self.keyword}>"