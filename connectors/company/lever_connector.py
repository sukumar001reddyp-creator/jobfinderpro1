from connectors.api_connector import APIConnector

from models.job_result import (
    JobResult,
    CompanyResult
)

from .lever_boards import LEVER_COMPANIES


class LeverConnector(APIConnector):

    def __init__(self):

        super().__init__(
            source_name="Lever",
            base_url="https://api.lever.co/v0/postings"
        )

    def search_jobs(self, keyword="", location=None):

        keyword = (keyword or "").lower()
        location = (location or "").lower()

        jobs = []

        for company_slug, company_name in LEVER_COMPANIES:

            try:

                response = self.get(
                    f"{company_slug}",
                    params={
                        "mode": "json"
                    }
                )

                for raw_job in response:

                    title = raw_job.get(
                        "text",
                        ""
                    ).lower()

                    city = raw_job.get(
                        "categories",
                        {}
                    ).get(
                        "location",
                        ""
                    ).lower()

                    if keyword and keyword not in title:
                        continue

                    if location and location not in city:
                        continue

                    jobs.append(
                        self.normalize_job(
                            raw_job,
                            company_name
                        )
                    )

            except Exception as e:

                print(
                    f"[Lever] {company_name}: {e}"
                )

        return jobs

    def normalize_job(
        self,
        raw_job,
        company_name
    ):

        categories = raw_job.get(
            "categories",
            {}
        )

        company = CompanyResult(
            name=company_name,
            logo_url=None
        )

        return JobResult(

            job_id=raw_job.get("id"),

            title=raw_job.get("text"),

            company=company,

            city=categories.get(
                "location",
                ""
            ),

            country="",

            employment_type=categories.get(
                "commitment",
                ""
            ),

            remote="remote" in categories.get(
                "location",
                ""
            ).lower(),

            salary_min=None,

            salary_max=None,

            apply_url=raw_job.get(
                "hostedUrl"
            ),

            description=raw_job.get(
                "descriptionPlain",
                raw_job.get("description", "")
            ),

            source="Lever",

            experience_level="",

            industry=""

        )