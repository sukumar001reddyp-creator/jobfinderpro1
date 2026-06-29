from connectors.company.greenhouse_connector import GreenhouseConnector

from extensions import db

from models.company import Company
from models.job import Job
from models.job_source import JobSource

from utils.slug import slugify


class JobSyncService:

    def __init__(self):

        self.connector = GreenhouseConnector()

        self.job_source = JobSource.query.filter_by(
            name="Greenhouse"
        ).first()

        if not self.job_source:

            raise Exception(
                "Greenhouse source not found. Run seed_job_sources.py"
            )

    def get_or_create_company(self, company_result):

        company = Company.query.filter_by(
            name=company_result.name
        ).first()

        if company:
            return company

        company = Company(

            name=company_result.name,

            slug=slugify(
                company_result.name
            ),

            logo=company_result.logo_url,

            verified=False,

            is_active=True

        )

        db.session.add(company)

        db.session.flush()

        return company