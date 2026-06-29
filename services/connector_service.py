from connectors.manager import ConnectorManager

from connectors.company.greenhouse_connector import (
    GreenhouseConnector,
)


class ConnectorService:

    def __init__(self):

        self.manager = ConnectorManager()

        self.manager.register(
            GreenhouseConnector()
        )

    def search(
        self,
        keyword="",
        location=""
    ):

        return self.manager.search(
            keyword=keyword,
            location=location
        )