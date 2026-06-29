from services.connector_manager import ConnectorManager
from services.job_service import JobService


class JobCollector:

    def __init__(self):

        self.connector_manager = ConnectorManager()

    def collect_jobs(self, keyword, location=None):

        jobs = self.connector_manager.search_jobs(
            keyword,
            location
        )

        for job in jobs:

            JobService.save_job(job)

        return jobs