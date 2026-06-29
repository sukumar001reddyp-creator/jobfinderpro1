class JobFilters:

    @staticmethod
    def apply(
        jobs,
        company=None,
        country=None,
        city=None,
        remote=None,
        experience_level=None,
        employment_type=None,
        industry=None
    ):

        filtered = jobs

        if company:
            filtered = [
                job for job in filtered
                if job.get("company") == company
            ]

        if country:
            filtered = [
                job for job in filtered
                if job.get("country") == country
            ]

        if city:
            filtered = [
                job for job in filtered
                if job.get("city") == city
            ]

        if remote is not None:
            filtered = [
                job for job in filtered
                if job.get("remote") == remote
            ]

        if experience_level:
            filtered = [
                job for job in filtered
                if job.get("experience_level") == experience_level
            ]

        if employment_type:
            filtered = [
                job for job in filtered
                if job.get("employment_type") == employment_type
            ]

        if industry:
            filtered = [
                job for job in filtered
                if job.get("industry") == industry
            ]

        return filtered