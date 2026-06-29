from connectors.base_connector import BaseConnector


class RSSConnector(BaseConnector):

    def __init__(self):
        super().__init__("RSS Feed")

    def search_jobs(self, keyword, location=None):
        """
        RSS integration will be added here.
        """
        return []

    def normalize_job(self, raw_job):

        return {
            "title": raw_job.get("title"),
            "description": raw_job.get("description"),
            "company": raw_job.get("company"),
            "country": raw_job.get("country"),
            "city": raw_job.get("city"),
            "remote": raw_job.get("remote", False),
            "experience_level": raw_job.get("experience_level"),
            "employment_type": raw_job.get("employment_type"),
            "industry": raw_job.get("industry"),
            "salary_min": raw_job.get("salary_min"),
            "salary_max": raw_job.get("salary_max"),
            "currency": raw_job.get("currency"),
            "apply_url": raw_job.get("apply_url"),
        }