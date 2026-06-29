from flask import Blueprint, render_template
from flask_login import login_required, current_user

from models.saved_job import SavedJob
from models.resume import Resume
from models.job_alert import JobAlert


dashboard_bp = Blueprint(
    "dashboard",
    __name__,
    url_prefix="/dashboard"
)


@dashboard_bp.route("/")
@login_required
def index():

    # Saved Jobs Count
    saved_jobs = SavedJob.query.filter_by(
        user_id=current_user.id
    ).count()

    # Resume Count
    resume_count = Resume.query.filter_by(
        user_id=current_user.id
    ).count()

    # Active Job Alerts Count
    job_alerts = JobAlert.query.filter_by(
        user_id=current_user.id,
        is_active=True
    ).count()

    # Applied Jobs (Future Feature)
    applied_jobs = 0

    return render_template(
        "dashboard/index.html",
        saved_jobs=saved_jobs,
        resume_count=resume_count,
        job_alerts=job_alerts,
        applied_jobs=applied_jobs
    )