from connectors.company.base_company_connector import BaseCompanyConnector

from .client import MicrosoftClient
from .parser import MicrosoftParser


class MicrosoftConnector(BaseCompanyConnector):

    def __init__(self):
        super().__init__("Microsoft")

        self.client = MicrosoftClient()
        self.parser = MicrosoftParser()

    def search_jobs(self, keyword, location=None):

        raw_jobs = self.client.search_jobs(
            keyword=keyword,
            location=location
        )

        jobs = []

        for raw_job in raw_jobs:

            jobs.append(
                self.parser.parse(raw_job)
            )

        return jobs

    def normalize_job(self, raw_job):

        return self.parser.parse(raw_job)