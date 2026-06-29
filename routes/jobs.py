from flask import Blueprint, render_template, abort
from flask_login import current_user
from services.applied_job_service import AppliedJobService
from models.job import Job
from services.recent_job_service import RecentJobService

jobs_bp = Blueprint(
    "jobs",
    __name__,
    url_prefix="/jobs"
)


@jobs_bp.route("/<int:job_id>")
def detail(job_id):

    job = Job.query.get(job_id)
    if not job:
        abort(404)

    # Recently Viewed add cheyyadam
    if current_user.is_authenticated:
        RecentJobService.add_job(
            current_user.id,
            job.id
        )

    # Check if user already applied to this job
    is_applied = False
    if current_user.is_authenticated:
        is_applied = AppliedJobService.is_applied(
            current_user.id,
            job.id
        )

    return render_template(
        "jobs/detail.html",
        job=job,
        is_applied=is_applied
    )