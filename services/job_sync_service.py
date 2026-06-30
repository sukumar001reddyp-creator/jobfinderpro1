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

        self.job_source = JobSource.query.filter_by(name="Greenhouse").first()
        if not self.job_source:
            raise Exception("Greenhouse source not found. Run seed_job_sources.py")

    def get_or_create_company(self, company_result):
        company = Company.query.filter_by(name=company_result.name).first()
        if company:
            return company

        company = Company(
            name=company_result.name,
            slug=slugify(company_result.name),
            logo=getattr(company_result, 'logo_url', None),
            verified=False,
            is_active=True
        )
        db.session.add(company)
        db.session.flush()
        return company

    def sync_greenhouse(self, limit=100):
        """Sync jobs from Greenhouse"""
        print("🔄 Starting Greenhouse job sync...")

        try:
            raw_jobs = self.connector.search_jobs()
            print(f"✅ Fetched {len(raw_jobs)} jobs from Greenhouse")

            new_count = 0
            updated_count = 0

            for job_data in raw_jobs[:limit]:
                try:
                    company = self.get_or_create_company(
                        job_data.company if hasattr(job_data, 'company') else job_data
                    )

                    job_title = getattr(job_data, 'title', 'Untitled Position')
                    base_slug = slugify(f"{job_title}-{company.name}")
                    job_slug = base_slug
                    counter = 1

                    # Make slug unique
                    while Job.query.filter_by(slug=job_slug).first():
                        job_slug = f"{base_slug}-{counter}"
                        counter += 1

                    # Check if job exists
                    existing_job = Job.query.filter_by(
                        source_job_id=str(getattr(job_data, 'id', '')),
                        job_source_id=self.job_source.id
                    ).first()

                    if existing_job:
                        # Update
                        existing_job.title = job_title
                        existing_job.slug = job_slug
                        existing_job.description = getattr(job_data, 'description', existing_job.description)
                        existing_job.city = getattr(job_data, 'city', existing_job.city)
                        existing_job.country = getattr(job_data, 'country', existing_job.country)
                        existing_job.employment_type = getattr(job_data, 'employment_type', existing_job.employment_type)
                        existing_job.remote = getattr(job_data, 'remote', existing_job.remote)
                        existing_job.apply_url = getattr(job_data, 'apply_url', existing_job.apply_url)
                        existing_job.is_active = True
                        updated_count += 1
                    else:
                        # Create new
                        new_job = Job(
                            title=job_title,
                            slug=job_slug,
                            source_job_id=str(getattr(job_data, 'id', '')),
                            company_id=company.id,
                            job_source_id=self.job_source.id,
                            description=getattr(job_data, 'description', ''),
                            city=getattr(job_data, 'city', None),
                            country=getattr(job_data, 'country', None),
                            employment_type=getattr(job_data, 'employment_type', None),
                            remote=getattr(job_data, 'remote', False),
                            apply_url=getattr(job_data, 'apply_url', ''),
                            status="active",
                            is_active=True,
                            posted_date=datetime.utcnow()
                        )
                        db.session.add(new_job)
                        new_count += 1

                except Exception as e:
                    print(f"⚠️ Error processing job '{getattr(job_data, 'title', 'Unknown')}': {e}")
                    continue

            db.session.commit()
            print(f"✅ Greenhouse Sync completed! New: {new_count} | Updated: {updated_count}")

        except Exception as e:
            db.session.rollback()
            print(f"❌ Sync failed: {e}")
            raise