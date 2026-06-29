from connectors.base_connector import BaseConnector

from .client import RSSClient
from .parser import RSSParser


class RSSConnector(BaseConnector):

    def __init__(self):
        super().__init__("RSS")

        self.client = RSSClient()
        self.parser = RSSParser()

    def search_jobs(self, keyword, location=None):

        # RSS URL next step lo configure chestam
        return []

    def normalize_job(self, raw_job):

        return self.parser.parse(raw_job)