from connectors.company.greenhouse_connector import GreenhouseConnector
from extensions import db
from models.company import Company
from models.job import Job
from models.job_source import JobSource
from utils.slug import slugify
from datetime import datetime

class JobSyncService:
    def __init__(self):
        self.connector = GreenhouseConnector()
        self.source = JobSource.query.filter_by(name="Greenhouse").first()
        if not self.source:
            raise Exception("Greenhouse source not found. Run seed_job_sources.py")

    def get_or_create_company(self, company_result):
        name = getattr(company_result, 'name', 'Unknown Company')[:200]
        company = Company.query.filter_by(name=name).first()
        if company:
            return company

        company = Company(
            name=name,
            slug=slugify(name)[:100],
            logo=getattr(company_result, 'logo_url', None),
            verified=False,
            is_active=True
        )
        db.session.add(company)
        db.session.flush()
        return company

    def sync_greenhouse(self, limit=300):
        print("🚀 Starting Fast Greenhouse Sync...")

        companies = {c.name: c for c in Company.query.all()}
        existing_ids = {j.source_job_id for j in Job.query.with_entities(Job.source_job_id).filter_by(job_source_id=self.source.id).all()}

        raw_jobs = self.connector.search_jobs()
        print(f"✅ Fetched {len(raw_jobs)} jobs")

        new_jobs = []
        batch_size = 100

        for job_data in raw_jobs[:limit]:
            try:
                job_id = str(getattr(job_data, 'id', ''))
                if job_id in existing_ids:
                    continue

                company = self.get_or_create_company(job_data.company if hasattr(job_data, 'company') else job_data)

                job_title = getattr(job_data, 'title', 'Untitled')[:200]
                job_slug = slugify(f"{job_title}-{job_id}")[:100]

                new_job = Job(
                    title=job_title,
                    slug=job_slug,
                    source_job_id=job_id,
                    company_id=company.id,
                    job_source_id=self.source.id,
                    description=str(getattr(job_data, 'description', ''))[:5000],
                    city=str(getattr(job_data, 'city', ''))[:100],
                    country=str(getattr(job_data, 'country', ''))[:100],
                    employment_type=str(getattr(job_data, 'employment_type', ''))[:50],
                    remote=getattr(job_data, 'remote', False),
                    apply_url=str(getattr(job_data, 'apply_url', ''))[:500],
                    status="active",
                    is_active=True,
                    posted_date=datetime.utcnow()
                )
                new_jobs.append(new_job)

                if len(new_jobs) >= batch_size:
                    db.session.bulk_save_objects(new_jobs)
                    db.session.commit()
                    print(f"✅ Inserted {len(new_jobs)} jobs")
                    new_jobs = []

            except:
                continue

        if new_jobs:
            db.session.bulk_save_objects(new_jobs)
            db.session.commit()

        print("🎉 Greenhouse Sync Completed!")