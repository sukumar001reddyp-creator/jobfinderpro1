from flask import Blueprint, render_template
from flask_login import login_required, current_user

from models.saved_job import SavedJob

dashboard_bp = Blueprint(
    "dashboard",
    __name__,
    url_prefix="/dashboard"
)


@dashboard_bp.route("/")
@login_required
def index():

    saved_jobs = SavedJob.query.filter_by(
        user_id=current_user.id
    ).count()

    job_alerts = 0

    return render_template(
        "dashboard/index.html",
        saved_jobs=saved_jobs,
        job_alerts=job_alerts
    )