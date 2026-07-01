from app import create_app
from extensions import db
from models.job import Job

app = create_app()

with app.app_context():
    deleted = Job.query.delete()
    db.session.commit()

    print(f"Deleted {deleted} jobs")