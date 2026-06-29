from .base_connector import BaseConnector


class APIConnector(BaseConnector):

    def __init__(self):
        super().__init__("API")

    def search_jobs(self, keyword, location=None):
        return []

    def normalize_job(self, raw_job):
        return {}