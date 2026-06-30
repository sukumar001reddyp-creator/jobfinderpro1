from flask import (
    Blueprint,
    render_template,
    request
)

from connectors.company.greenhouse_connector import GreenhouseConnector
from connectors.manager import ConnectorManager
from utils.pagination import Pagination

search_bp = Blueprint(
    "search",
    __name__,
    url_prefix="/search"
)


@search_bp.route("/", methods=["GET"])
def search():

    keyword = request.args.get("keyword", "").strip()
    location = request.args.get("location", "").strip()

    manager = ConnectorManager()
    manager.register(GreenhouseConnector())

    try:

        raw_jobs = manager.search(
            keyword=keyword,
            location=location
        )

        print(f"✅ Manager returned {len(raw_jobs)} jobs")

    except Exception as e:

        print(f"❌ Connector Manager Error: {e}")
        raw_jobs = []

    jobs_list = []

    for job in raw_jobs:

        jobs_list.append({

            "id": job.id,

            "title": job.title,

            "company": {
                "name": job.company.name
            },

            "city": job.city,

            "country": job.country,

            "employment_type": job.employment_type,

            "remote": job.remote,

            "description": job.description,

            "apply_url": job.apply_url

        })

    print(
        f"🚀 [DEBUG] Sending exactly {len(jobs_list)} jobs to search/index.html!"
    )

    page = request.args.get(
        "page",
        1,
        type=int
    )

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