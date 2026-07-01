from flask import Blueprint, render_template

from models.job import Job
from models.company import Company
from models.job_source import JobSource

home_bp = Blueprint("home", __name__)


@home_bp.route("/")
def home():

    # Latest 9 jobs from Database
    latest_jobs = (
        Job.query
        .filter_by(is_active=True)
        .order_by(Job.created_at.desc())
        .limit(9)
        .all()
    )

    # Stats from Database
    job_count = Job.query.filter_by(is_active=True).count()
    company_count = Company.query.count()
    source_count = JobSource.query.filter_by(is_active=True).count()

    return render_template(
        "home/index.html",
        latest_jobs=latest_jobs,
        job_count=job_count,
        company_count=company_count,
        source_count=source_count
    )