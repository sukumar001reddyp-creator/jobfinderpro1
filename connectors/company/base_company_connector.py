from abc import ABC, abstractmethod

from connectors.base_connector import BaseConnector


class BaseCompanyConnector(BaseConnector, ABC):

    def __init__(self, company_name):
        super().__init__(company_name)

    @abstractmethod
    def search_jobs(self, keyword, location=None):
        """
        Return normalized jobs from
        company careers website.
        """
        pass

    @abstractmethod
    def normalize_job(self, raw_job):
        """
        Convert company job format
        into JobFinder Pro format.
        """
        pass