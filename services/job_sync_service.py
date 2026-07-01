from connectors.company.greenhouse_connector import GreenhouseConnector
from connectors.company.lever_connector import LeverConnector
from connectors.company.workday_connector import WorkdayConnector
from connectors.company.ashby_connector import AshbyConnector
from connectors.company.google_jobs_connector import GoogleJobsConnector   # Google Jobs Added

from extensions import db
from models.company import Company
from models.job import Job
from models.job_source import JobSource
from utils.slug import slugify
from datetime import datetime


class JobSyncService:

    def __init__(self):
        self.greenhouse = GreenhouseConnector()
        self.lever = LeverConnector()
        self.workday = WorkdayConnector()
        self.ashby = AshbyConnector()
        self.google_jobs = GoogleJobsConnector()   # Google Jobs

        self.greenhouse_source = JobSource.query.filter_by(name="Greenhouse").first()
        self.lever_source = JobSource.query.filter_by(name="Lever").first()
        self.workday_source = JobSource.query.filter_by(name="Workday").first()
        self.ashby_source = JobSource.query.filter_by(name="Ashby").first()
        self.google_source = JobSource.query.filter_by(name="Google Jobs").first()

        if not self.greenhouse_source:
            raise Exception("Greenhouse source not found in DB")
        if not self.lever_source:
            raise Exception("Lever source not found in DB. Run seed_job_sources.py")
        if not self.workday_source:
            raise Exception("Workday source not found in DB. Run seed_job_sources.py")
        if not self.ashby_source:
            raise Exception("Ashby source not found in DB. Run seed_job_sources.py")
        if not self.google_source:
            raise Exception("Google Jobs source not found in DB. Run seed_job_sources.py")

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

    def sync_greenhouse(self, limit=200):
        print("🔄 Syncing Greenhouse...")
        self._sync_source(self.greenhouse, self.greenhouse_source, limit)

    def sync_lever(self, limit=50):
        print("🔄 Syncing Lever...")
        self._sync_source(self.lever, self.lever_source, limit)

    def sync_workday(self, limit=100):
        print("🔄 Syncing Workday...")
        self._sync_source(self.workday, self.workday_source, limit)

    def sync_ashby(self, limit=100):
        print("🔄 Syncing Ashby...")
        self._sync_source(self.ashby, self.ashby_source, limit)

    def sync_google_jobs(self, limit=100):
        print("🔄 Syncing Google Jobs...")
        try:
            jobs = self.google_jobs.search(
                query="Software Engineer", 
                location="Hyderabad", 
                limit=limit
            )
            print(f"✅ Google Jobs: {len(jobs)} real jobs fetched")
            # You can save these jobs to DB if needed later
        except Exception as e:
            print(f"❌ Google Jobs Sync Failed: {e}")

    def _sync_source(self, connector, job_source, limit=100):
        try:
            raw_jobs = connector.search_jobs()
            print(f"✅ Fetched {len(raw_jobs)} jobs from {job_source.name}")

            new_count = 0
            updated_count = 0

            for job_data in raw_jobs[:limit]:
                try:
                    company = self.get_or_create_company(
                        job_data.company if hasattr(job_data, 'company') else job_data
                    )

                    job_title = getattr(job_data, 'title', 'Untitled Position')
                    base_slug = slugify(f"{job_title} {company.name}")
                    job_slug = base_slug
                    counter = 1

                    while Job.query.filter_by(slug=job_slug).first():
                        job_slug = f"{base_slug}-{counter}"
                        counter += 1

                    existing_job = Job.query.filter_by(
                        source_job_id=str(getattr(job_data, 'id', '')),
                        job_source_id=job_source.id
                    ).first()

                    if existing_job:
                        existing_job.slug = job_slug
                        existing_job.title = job_title
                        existing_job.description = getattr(job_data, 'description', existing_job.description)
                        existing_job.city = getattr(job_data, 'city', existing_job.city)
                        existing_job.country = getattr(job_data, 'country', existing_job.country)
                        existing_job.employment_type = getattr(job_data, 'employment_type', existing_job.employment_type)
                        existing_job.remote = getattr(job_data, 'remote', existing_job.remote)
                        existing_job.apply_url = getattr(job_data, 'apply_url', existing_job.apply_url)
                        existing_job.is_active = True
                        updated_count += 1
                    else:
                        new_job = Job(
                            title=job_title,
                            slug=job_slug,
                            source_job_id=str(getattr(job_data, 'id', '')),
                            company_id=company.id,
                            job_source_id=job_source.id,
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
                    print(f"⚠️ Error on job '{getattr(job_data, 'title', 'Unknown')}': {e}")
                    continue

            db.session.commit()
            print(f"✅ {job_source.name} Sync Done → New: {new_count} | Updated: {updated_count}")

        except Exception as e:
            db.session.rollback()
            print(f"❌ {job_source.name} Sync Failed: {e}")
            raise