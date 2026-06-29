from models.job_source import JobSource

from connectors import (
    LinkedInConnector,
    GovernmentConnector,
    RSSConnector,
    APIConnector
)

from connectors.company.registry import COMPANY_CONNECTORS


class ConnectorManager:

    def __init__(self):

        self.connector_map = {
            "linkedin": LinkedInConnector,
            "government": GovernmentConnector,
            "rss": RSSConnector,
            "api": APIConnector,
        }

    def get_connectors(self):

        connectors = []

        sources = JobSource.query.filter_by(
            is_active=True
        ).all()

        for source in sources:

            source_type = source.source_type.lower()

            # Company Careers
            if source_type == "company":

                for company_connector in COMPANY_CONNECTORS:
                    connectors.append(company_connector())

                continue

            # Other connectors
            connector_class = self.connector_map.get(source_type)

            if connector_class:
                connectors.append(connector_class())

        return connectors

    def search_jobs(self, keyword, location=None):

        all_jobs = []

        for connector in self.get_connectors():

            try:

                jobs = connector.search_jobs(
                    keyword,
                    location
                )

                if jobs:
                    all_jobs.extend(jobs)

            except Exception as e:

                print(
                    f"{connector.source_name}: {e}"
                )

        return all_jobs