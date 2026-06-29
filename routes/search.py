from flask import (
    Blueprint,
    render_template,
    request
)

from services.search_service import SearchService

search_bp = Blueprint(
    "search",
    __name__,
    url_prefix="/search"
)


@search_bp.route("/", methods=["GET"])
def search():

    # Search Parameters
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

    # Search
    search_service = SearchService()

    query = search_service.search(
        keyword=keyword,
        location=location,
        company=company or None,
        employment_type=employment_type or None,
        remote=True if remote else None,
        sort=sort
    )

    # Pagination
    jobs = query.paginate(
        page=page,
        per_page=9,
        error_out=False
    )

    # Render Page
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