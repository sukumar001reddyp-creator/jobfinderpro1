from core.http_client import HttpClient


class MicrosoftClient:

    BASE_URL = "https://careers.microsoft.com"

    def __init__(self):
        self.http = HttpClient()

    def search_jobs(self, keyword, location=None):
        """
        Placeholder for Microsoft public integration.

        Future implementation:
        - Official API (if available)
        - Public search endpoint
        - Public RSS (if available)
        """

        return []