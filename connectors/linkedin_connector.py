from .base_connector import BaseConnector


class LinkedInConnector(BaseConnector):

    def __init__(self):
        super().__init__("LinkedIn")

    def search_jobs(self, keyword, location=None):
        return []

    def normalize_job(self, raw_job):
        return {}