from datetime import datetime

from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from extensions import db


class User(UserMixin, db.Model):

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)

    # Basic Information
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)

    email = db.Column(
        db.String(255),
        unique=True,
        nullable=False,
        index=True
    )

    phone = db.Column(db.String(20), unique=True)

    password_hash = db.Column(db.String(255), nullable=False)

    # Location
    country = db.Column(db.String(100))
    state = db.Column(db.String(100))
    city = db.Column(db.String(100))

    # Profile
    profile_photo = db.Column(db.String(255))
    headline = db.Column(db.String(255))
    bio = db.Column(db.Text)

    # Account Status
    email_verified = db.Column(db.Boolean, default=False)
    is_active = db.Column(db.Boolean, default=True)
    is_admin = db.Column(db.Boolean, default=False)

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

    # -------------------------
    # Password Methods
    # -------------------------

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(
            self.password_hash,
            password
        )

    # -------------------------
    # String Representation
    # -------------------------

    def __repr__(self):
        return f"<User {self.email}>"