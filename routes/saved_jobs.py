from flask import (
    Blueprint,
    redirect,
    url_for,
    flash,
    render_template,
    request
)

from flask_login import (
    login_required,
    current_user
)

from services.saved_job_service import SavedJobService


saved_jobs_bp = Blueprint(
    "saved_jobs",
    __name__,
    url_prefix="/saved-jobs"
)


@saved_jobs_bp.route("/save/<int:job_id>", methods=["POST"])
@login_required
def save_job(job_id):

    saved = SavedJobService.save_job(
        current_user.id,
        job_id
    )

    if saved:

        flash(
            "Job saved successfully!",
            "success"
        )

    else:

        flash(
            "Job already saved.",
            "warning"
        )

    return redirect(
        request.referrer
        or url_for("search.search")
    )


@saved_jobs_bp.route("/remove/<int:job_id>", methods=["POST"])
@login_required
def remove_job(job_id):

    SavedJobService.remove_job(
        current_user.id,
        job_id
    )

    flash(
        "Job removed!",
        "info"
    )

    return redirect(
        request.referrer
        or url_for("saved_jobs.list_saved_jobs")
    )


@saved_jobs_bp.route("/")
@login_required
def list_saved_jobs():

    jobs = SavedJobService.get_saved_jobs(
        current_user.id
    )

    return render_template(
        "dashboard/saved_jobs.html",
        jobs=jobs
    )