from app import create_app
from services.job_sync_service import JobSyncService

# Create app and push context
app = create_app()

with app.app_context():
    print("🚀 Starting All Syncs...\n")

    sync = JobSyncService()

    # Fast Sync - Greenhouse (Recommended)
    sync.sync_greenhouse(limit=None)

    # Uncomment when ready
    # sync.sync_lever(limit=50)
    # sync.sync_workday(limit=100)
    # sync.sync_ashby(limit=100)
    # sync.sync_google_jobs(limit=100)

    print("\n🎉 All syncs completed!")