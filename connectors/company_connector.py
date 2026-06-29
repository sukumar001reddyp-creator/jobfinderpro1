from .base_connector import BaseConnector


class CompanyConnector(BaseConnector):

    def __init__(self):
        super().__init__("Company Careers")

    def search_jobs(self, keyword, location=None):
        return []

    def normalize_job(self, raw_job):
        return {}