from app import create_app
from services.job_sync_service import JobSyncService
from models.job_result import CompanyResult

app = create_app()

with app.app_context():

    sync = JobSyncService()

    company = sync.get_or_create_company(
        CompanyResult("Test Company")
    )

    print(company.id)
    print(company.name)