from app import create_app

app = create_app()

with app.app_context():
    from services.job_sync_service import JobSyncService

    sync = JobSyncService()

    print("🚀 Starting All Syncs...")

    # Main Working Connectors
    sync.sync_greenhouse(limit=300)
    sync.sync_lever(limit=50)
    sync.sync_ashby(limit=100)
    
    # Google Jobs (Best for real results)
    sync.sync_google_jobs(limit=100)

    # Workday (optional - dummy)
    # sync.sync_workday(limit=50)

    print("✅ All Syncs Completed!")