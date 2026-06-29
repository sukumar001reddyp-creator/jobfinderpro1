from .base_company_connector import BaseCompanyConnector


class MicrosoftConnector(BaseCompanyConnector):

    def __init__(self):
        super().__init__("Microsoft")

    def search_jobs(self, keyword, location=None):

        print(
            f"Searching Microsoft Careers for '{keyword}'"
        )

        return []

    def normalize_job(self, raw_job):

        return {}