from .base_company_connector import BaseCompanyConnector


class GoogleConnector(BaseCompanyConnector):

    def __init__(self):
        super().__init__("Google")

    def search_jobs(self, keyword, location=None):

        print(
            f"Searching Google Careers for '{keyword}'"
        )

        return []

    def normalize_job(self, raw_job):

        return {}