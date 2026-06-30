# connectors/base_company_connector.py
from connectors.base_connector import BaseConnector


class BaseCompanyConnector(BaseConnector):
    def __init__(self, company_name):
        super().__init__(company_name)

    def search_jobs(self, keyword, location=None):
        raise NotImplementedError("Subclasses must implement search_jobs")

    def normalize_job(self, raw_job):
        raise NotImplementedError("Subclasses must implement normalize_job")