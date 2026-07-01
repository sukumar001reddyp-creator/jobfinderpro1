from flask import (
    Blueprint,
    render_template,
    request
)
from sqlalchemy import or_

from connectors.company.greenhouse_connector import GreenhouseConnector
from connectors.manager import ConnectorManager
from utils.pagination import Pagination
from models.job import Job

search_bp = Blueprint(
    "search",
    __name__,
    url_prefix="/search"
)


@search_bp.route("/", methods=["GET"])
def search():

    keyword = request.args.get("keyword", "").strip()
    location = request.args.get("location", "").strip()

    # Start query
    query = Job.query.filter_by(is_active=True)

    # Apply filters
    if keyword:
        query = query.filter(
            Job.title.ilike(f"%{keyword}%")
        )

    if location:
        query = query.filter(
            or_(
                Job.city.ilike(f"%{location}%"),
                Job.country.ilike(f"%{location}%")
            )
        )

    # Get all matching jobs
    raw_jobs = query.order_by(
        Job.created_at.desc()
    ).all()

    print(f"✅ Database returned {len(raw_jobs)} jobs")

    # Convert to dict for template
    jobs_list = []

    for job in raw_jobs:
        jobs_list.append({
            "id": job.id,
            "title": job.title,
            "company": {
                "name": job.company.name if job.company else "Unknown Company"
            },
            "city": job.city,
            "country": job.country,
            "employment_type": job.employment_type,
            "remote": job.remote,
            "description": job.description,
            "apply_url": job.apply_url
        })

    print(f"🚀 [DEBUG] Sending exactly {len(jobs_list)} jobs to search/index.html!")

    # Pagination
    page = request.args.get("page", 1, type=int)
    paginated_jobs = Pagination(
        jobs_list,
        page=page,
        per_page=9
    )

    return render_template(
        "search/index.html",
        jobs=paginated_jobs,
        keyword=keyword,
        location=location
    )