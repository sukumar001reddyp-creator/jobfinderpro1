from datetime import datetime

from extensions import db


class SearchHistory(db.Model):

    __tablename__ = "search_history"

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

    searched_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    # Relationship
    user = db.relationship(
        "User",
        backref=db.backref(
            "search_history",
            lazy=True,
            cascade="all, delete-orphan"
        )
    )

    def __repr__(self):
        return f"<SearchHistory {self.keyword}>"