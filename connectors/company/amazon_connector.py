from .base_company_connector import BaseCompanyConnector


class AmazonConnector(BaseCompanyConnector):

    def __init__(self):
        super().__init__("Amazon")

    def search_jobs(self, keyword, location=None):

        print(
            f"Searching Amazon Careers for '{keyword}'"
        )

        return []

    def normalize_job(self, raw_job):

        return {}