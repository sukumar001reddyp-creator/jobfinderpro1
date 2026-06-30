from concurrent.futures import ThreadPoolExecutor, as_completed


class ConnectorManager:

    def __init__(self):
        self.connectors = []

    def register(self, connector):
        self.connectors.append(connector)

    def register_many(self, connectors):
        for connector in connectors:
            self.register(connector)

    def search(self, keyword="", location=None):

        jobs = []

        with ThreadPoolExecutor(max_workers=5) as executor:

            futures = {
                executor.submit(
                    connector.search_jobs,
                    keyword,
                    location
                ): connector

                for connector in self.connectors
            }

            for future in as_completed(futures):

                try:
                    result = future.result()

                    if result:
                        jobs.extend(result)

                except Exception as e:
                    print(e)

        return jobs