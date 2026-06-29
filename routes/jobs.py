from flask import Blueprint, render_template, abort

from models.job import Job

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

    return render_template(
        "jobs/detail.html",
        job=job
    )