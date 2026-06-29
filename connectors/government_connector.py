from .base_connector import BaseConnector


class GovernmentConnector(BaseConnector):

    def __init__(self, portal_name):
        super().__init__(portal_name)

    def search_jobs(self, keyword, location=None):
        """
        This method will be implemented by
        each government job portal connector.
        """
        raise NotImplementedError

    def normalize_job(self, raw_job):
        """
        Convert government portal data
        into JobFinder Pro format.
        """
        raise NotImplementedError