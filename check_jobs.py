from app import create_app
from models.job import Job

app = create_app()

with app.app_context():

    jobs = Job.query.order_by(Job.id.desc()).limit(5).all()

    for j in jobs:
        print("=" * 60)
        print("ID:", j.id)
        print("TITLE:", j.title)
        print("APPLY:", j.apply_url)