import os
import sys

# Add project root to Python path
PROJECT_ROOT = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..")
)

if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from app import app
from extensions import db

from models.company import Company
from models.job_source import JobSource
from models.job import Job

from seed.sample_jobs import SAMPLE_JOBS

sys.path.append(
    os.path.dirname(
        os.path.dirname(os.path.abspath(__file__))
    )
)


with app.app_context():

    for item in SAMPLE_JOBS:

        company = Company.query.filter_by(
            name=item["company_name"]
        ).first()

        if not company:

            company = Company(
                name=item["company_name"],
                slug=item["company_name"].lower().replace(" ", "-"),
                verified=True
            )

            db.session.add(company)
            db.session.commit()

        source = JobSource.query.filter_by(
            name=item["job_source_name"]
        ).first()

        if not source:

            source = JobSource(
                name=item["job_source_name"],
                source_type=item["job_source_type"]
            )

            db.session.add(source)
            db.session.commit()

        existing = Job.query.filter_by(
            source_job_id=item["source_job_id"]
        ).first()

        if existing:
            continue

        job = Job(

            source_job_id=item["source_job_id"],

            title=item["title"],
            slug=item["slug"],
            description=item["description"],

            category=item["category"],
            industry=item["industry"],
            skills=item["skills"],

            country=item["country"],
            state=item["state"],
            city=item["city"],

            remote=item["remote"],

            experience_level=item["experience_level"],
            experience_min=item["experience_min"],
            experience_max=item["experience_max"],

            employment_type=item["employment_type"],

            salary_min=item["salary_min"],
            salary_max=item["salary_max"],
            salary_type=item["salary_type"],
            currency=item["currency"],

            apply_url=item["apply_url"],

            status=item["status"],
            is_active=item["is_active"],

            company_id=company.id,
            job_source_id=source.id
        )

        db.session.add(job)

    db.session.commit()

    print("✅ Sample Jobs Inserted Successfully")