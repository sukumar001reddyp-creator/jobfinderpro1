from connectors.api_connector import APIConnector

from models.job_result import (
    JobResult,
    CompanyResult
)

from .workday_boards import WORKDAY_COMPANIES


class WorkdayConnector(APIConnector):

    def __init__(self):
        super().__init__(
            source_name="Workday",
            base_url="https://www.workday.com"
        )

    def search_jobs(self, keyword="", location=None):
        keyword = (keyword or "").lower()
        location = (location or "").lower()

        jobs = []

        print(f"🔍 Scraping {len(WORKDAY_COMPANIES)} Workday companies...")

        for company_slug, company_name in WORKDAY_COMPANIES:
            try:
                # Workday jobs usually use this pattern
                url = f"https://{company_slug}.myworkdayjobs.com/wday/cxs/{company_slug}/jobs"

                response = self.get(url)   # Adjust if needed based on your APIConnector

                # Note: Workday is heavily JS rendered. This may need Selenium or RSS feed
                # For now using basic request (many will fail)

                if response and hasattr(response, 'text'):
                    # This is placeholder - Workday scraping is complex
                    print(f"[Workday] {company_name}: Basic request made (may need advanced scraping)")

                    # Dummy job for testing (remove later)
                    jobs.append(
                        self.normalize_job_dummy(company_name)
                    )

            except Exception as e:
                print(f"[Workday] {company_name}: {e}")

        return jobs

    def normalize_job(self, raw_job, company_name):
        """Real normalize when proper scraping is ready"""
        company = CompanyResult(
            name=company_name,
            logo_url=None
        )

        return JobResult(
            job_id=raw_job.get("id"),
            title=raw_job.get("title"),
            company=company,
            city=raw_job.get("city", ""),
            country=raw_job.get("country", ""),
            employment_type=raw_job.get("employment_type", ""),
            remote=raw_job.get("remote", False),
            salary_min=None,
            salary_max=None,
            apply_url=raw_job.get("apply_url"),
            description=raw_job.get("description", ""),
            source="Workday",
            experience_level="",
            industry=""
        )

    def normalize_job_dummy(self, company_name):
        """Temporary dummy for testing"""
        company = CompanyResult(
            name=company_name,
            logo_url=None
        )

        return JobResult(
            job_id="dummy-" + company_name.lower(),
            title=f"Software Engineer at {company_name}",
            company=company,
            city="Remote",
            country="United States",
            employment_type="Full-time",
            remote=True,
            salary_min=120000,
            salary_max=180000,
            apply_url=f"https://{company_name.lower()}.com/careers",
            description="Exciting opportunity at " + company_name,
            source="Workday",
            experience_level="Mid-Senior",
            industry="Technology"
        )