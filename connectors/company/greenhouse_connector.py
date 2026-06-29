from connectors.api_connector import APIConnector

from models.job_result import (
    JobResult,
    CompanyResult
)

from .greenhouse_boards import GREENHOUSE_COMPANIES


class GreenhouseConnector(APIConnector):

    def __init__(self):

        super().__init__(
            source_name="Greenhouse",
            base_url="https://boards-api.greenhouse.io/v1/boards"
        )

    def search_jobs(self, keyword="", location=None):

        keyword = (keyword or "").lower()
        location = (location or "").lower()

        jobs = []

        for board_token, company_name in GREENHOUSE_COMPANIES:

            try:

                response = self.get(
                    f"{board_token}/jobs",
                    params={
                        "content": "true"
                    }
                )

                for raw_job in response.get("jobs", []):

                    title = raw_job.get(
                        "title",
                        ""
                    ).lower()

                    city = raw_job.get(
                        "location",
                        {}
                    ).get(
                        "name",
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
                    f"[Greenhouse] {company_name}: {e}"
                )

        return jobs

    def normalize_job(
        self,
        raw_job,
        company_name
    ):

        location = raw_job.get(
            "location",
            {}
        )

        company = CompanyResult(
            name=company_name,
            logo_url=None
        )

        return JobResult(

            job_id=raw_job.get("id"),

            title=raw_job.get("title"),

            company=company,

            city=location.get(
                "name",
                ""
            ),

            country="",

            employment_type="",

            remote=False,

            salary_min=None,

            salary_max=None,

            apply_url=raw_job.get(
                "absolute_url"
            ),

            description=raw_job.get(
                "content",
                ""
            ),

            source="Greenhouse",

            experience_level="",

            industry=""

        )