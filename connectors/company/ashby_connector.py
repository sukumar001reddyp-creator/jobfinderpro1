from connectors.api_connector import APIConnector
from models.job_result import JobResult, CompanyResult
from .ashby_boards import ASHBY_COMPANIES


class AshbyConnector(APIConnector):

    def __init__(self):
        super().__init__(
            source_name="Ashby",
            base_url="https://api.ashbyhq.com"
        )

    def search_jobs(self, keyword="", location=None):
        jobs = []
        print(f"🔍 Fetching from {len(ASHBY_COMPANIES)} Ashby companies...")

        for company_slug, company_name in ASHBY_COMPANIES:
            try:
                # Ashby public jobs endpoint
                response = self.get(
                    f"/posting/{company_slug}/list",
                    params={"published": "true"}
                )

                if response and isinstance(response, list):
                    for raw in response:
                        if keyword and keyword.lower() not in raw.get("title", "").lower():
                            continue

                        jobs.append(self.normalize_job(raw, company_name))

            except Exception as e:
                if "404" not in str(e):
                    print(f"[Ashby] {company_name}: {e}")

        print(f"✅ Ashby: Fetched {len(jobs)} jobs")
        return jobs

    def normalize_job(self, raw, company_name):
        company = CompanyResult(
            name=company_name,
            logo_url=None
        )

        location = raw.get("location", {})
        city = location.get("city", "") or location.get("name", "")

        return JobResult(
            job_id=raw.get("id"),
            title=raw.get("title"),
            company=company,
            city=city,
            country=location.get("country", ""),
            employment_type=raw.get("employmentType", ""),
            remote=raw.get("isRemote", False),
            salary_min=None,
            salary_max=None,
            apply_url=raw.get("applicationLink") or raw.get("url"),
            description=raw.get("descriptionPlain", raw.get("description", "")),
            source="Ashby",
            experience_level="",
            industry=""
        )