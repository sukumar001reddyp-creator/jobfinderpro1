from flask import (
    Blueprint,
    render_template,
    request
)

from services.live_search_service import LiveSearchService
from utils.pagination import Pagination

search_bp = Blueprint(
    "search",
    __name__,
    url_prefix="/search"
)


@search_bp.route("/", methods=["GET"])
def search():

    keyword = request.args.get(
        "keyword",
        ""
    ).strip()

    location = request.args.get(
        "location",
        ""
    ).strip()

    company = request.args.get(
        "company",
        ""
    ).strip()

    employment_type = request.args.get(
        "employment_type",
        ""
    ).strip()

    remote = request.args.get("remote")

    sort = request.args.get(
        "sort",
        "newest"
    )

    page = request.args.get(
        "page",
        1,
        type=int
    )

    search_service = LiveSearchService()

    jobs = search_service.search(
        keyword=keyword,
        location=location
    )

    jobs = Pagination(
        jobs,
        page=page,
        per_page=9
    )

    return render_template(
        "search/index.html",
        jobs=jobs,
        keyword=keyword,
        location=location,
        company=company,
        employment_type=employment_type,
        remote=remote,
        sort=sort
    )