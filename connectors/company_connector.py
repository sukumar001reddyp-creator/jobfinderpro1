from .base_connector import BaseConnector


class CompanyConnector(BaseConnector):

    def __init__(self, company_name, careers_url):
        super().__init__(company_name)
        self.company_name = company_name
        self.careers_url = careers_url

    def search_jobs(self, keyword, location=None):
        """
        Company-specific implementation.
        This method will be overridden by
        Microsoft, Google, Amazon, etc.
        """
        raise NotImplementedError

    def normalize_job(self, raw_job):
        """
        Convert company-specific response
        into JobFinder Pro format.
        """
        raise NotImplementedError