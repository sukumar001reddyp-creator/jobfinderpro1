from concurrent.futures import ThreadPoolExecutor, as_completed


class ConnectorManager:

    def __init__(self):

        self.connectors = []

    def register(self, connector):

        self.connectors.append(connector)

    def register_many(self, connectors):

        for connector in connectors:

            self.register(connector)

    def search(self, keyword=None, location=None):

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

                connector = futures[future]

                try:

                    result = future.result()

                    if result:

                        jobs.extend(result)

                except Exception as e:

                    print(
                        f"{connector.source_name}: {e}"
                    )

        return self.remove_duplicates(jobs)

    def remove_duplicates(self, jobs):

        unique = {}

        for job in jobs:

            company_name = ""

            if hasattr(job, "company") and job.company:

                company_name = getattr(
                    job.company,
                    "name",
                    ""
                )

            key = (

                getattr(
                    job,
                    "title",
                    ""
                ),

                company_name,

                getattr(
                    job,
                    "city",
                    ""
                )

            )

            if key not in unique:

                unique[key] = job

        return list(unique.values())