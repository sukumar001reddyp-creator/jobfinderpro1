from extensions import db
from flask import (
    Blueprint,
    render_template,
    redirect,
    request,
    flash,
    url_for
)

from flask_login import (
    login_required,
    current_user
)

from models.applied_job import AppliedJob
from services.applied_job_service import AppliedJobService


applied_jobs_bp = Blueprint(
    "applied_jobs",
    __name__,
    url_prefix="/applied-jobs"
)


@applied_jobs_bp.route("/")
@login_required
def index():

    jobs = AppliedJob.query.filter_by(
        user_id=current_user.id
    ).order_by(
        AppliedJob.applied_at.desc()
    ).all()

    return render_template(
        "dashboard/applied_jobs.html",
        jobs=jobs
    )


@applied_jobs_bp.route("/apply/<int:job_id>", methods=["POST"])
@login_required
def apply(job_id):

    saved = AppliedJobService.apply(
        current_user.id,
        job_id
    )

    if saved:

        flash(
            "Job marked as applied!",
            "success"
        )

    else:

        flash(
            "Already marked as applied.",
            "warning"
        )

    return redirect(
        request.referrer
        or url_for("search.search")
    )


@applied_jobs_bp.route("/remove/<int:job_id>", methods=["POST"])
@login_required
def remove(job_id):

    AppliedJobService.remove(
        current_user.id,
        job_id
    )

    flash(
        "Application removed.",
        "info"
    )

    return redirect(
        request.referrer
        or url_for("applied_jobs.index")
    )
@applied_jobs_bp.route("/status/<int:application_id>", methods=["POST"])
@login_required
def update_status(application_id):

    application = AppliedJob.query.filter_by(
        id=application_id,
        user_id=current_user.id
    ).first_or_404()

    application.status = request.form["status"]

    db.session.commit()

    flash(
        "Application status updated successfully!",
        "success"
    )

    return redirect(
        url_for("applied_jobs.index")
    )    