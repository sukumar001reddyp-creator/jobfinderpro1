from flask import Blueprint, render_template
from flask_login import login_required, current_user

from services.recent_job_service import RecentJobService

recent_jobs_bp = Blueprint(
    "recent_jobs",
    __name__,
    url_prefix="/recent-jobs"
)


@recent_jobs_bp.route("/")
@login_required
def index():

    jobs = RecentJobService.get_recent_jobs(
        current_user.id
    )

    return render_template(
        "dashboard/recent_jobs.html",
        jobs=jobs
    )