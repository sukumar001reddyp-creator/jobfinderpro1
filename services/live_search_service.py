from services.connector_service import ConnectorService


class LiveSearchService:

    def __init__(self):

        self.connector_service = ConnectorService()

    def search(
        self,
        keyword="",
        location=""
    ):

        return self.connector_service.search(
            keyword=keyword,
            location=location
        )