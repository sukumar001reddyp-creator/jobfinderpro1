import requests

from .base_connector import BaseConnector


class APIConnector(BaseConnector):

    def __init__(self, source_name, base_url):
        super().__init__(source_name)
        self.base_url = base_url

    def get(self, endpoint="", params=None):

        url = self.base_url

        if endpoint:
            url = f"{self.base_url.rstrip('/')}/{endpoint.lstrip('/')}"

        response = requests.get(
            url,
            params=params,
            timeout=20,
            headers={
                "User-Agent": "JobFinderPro/1.0"
            }
        )

        response.raise_for_status()

        return response.json()

    def search_jobs(self, keyword, location=None):
        raise NotImplementedError

    def normalize_job(self, raw_job):
        raise NotImplementedError