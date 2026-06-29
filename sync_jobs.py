from app import create_app

from services.job_sync_service import JobSyncService


app = create_app()

with app.app_context():

    sync = JobSyncService()

    sync.sync_greenhouse()