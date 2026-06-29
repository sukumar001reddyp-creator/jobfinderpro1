class CompanyResult:

    def __init__(
        self,
        name,
        logo_url=None
    ):
        self.name = name
        self.logo_url = logo_url


class JobResult:

    def __init__(
        self,
        job_id,
        title,
        company,
        city="",
        country="",
        description="",
        employment_type="",
        experience_level="",
        industry="",
        remote=False,
        salary_min=None,
        salary_max=None,
        currency="",
        apply_url="",
        source="",
        metadata=None
    ):

        self.id = job_id
        self.source_job_id = str(job_id)

        self.title = title
        self.company = company

        self.city = city
        self.country = country

        self.description = description

        self.employment_type = employment_type
        self.experience_level = experience_level
        self.industry = industry

        self.remote = remote

        self.salary_min = salary_min
        self.salary_max = salary_max

        self.currency = currency

        self.apply_url = apply_url

        self.source = source

        self.metadata = metadata or []