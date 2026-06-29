from abc import ABC, abstractmethod


class BaseConnector(ABC):

    def __init__(self, source_name):
        self.source_name = source_name

    @abstractmethod
    def search_jobs(self, keyword, location=None):
        """
        Search jobs from a source.
        Must return a list of normalized jobs.
        """
        pass

    @abstractmethod
    def normalize_job(self, raw_job):
        """
        Convert source-specific job data
        into JobFinder Pro format.
        """
        pass