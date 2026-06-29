from connectors.company.greenhouse_connector import GreenhouseConnector


def main():

    connector = GreenhouseConnector()

    jobs = connector.search_jobs()

    print("=" * 60)
    print(f"Total Jobs : {len(jobs)}")
    print("=" * 60)

    for job in jobs[:10]:

        print(f"Title    : {job.title}")
        print(f"Company  : {job.company.name}")
        print(f"Location : {job.city}")
        print(f"Apply    : {job.apply_url}")
        print("-" * 60)


if __name__ == "__main__":
    main()