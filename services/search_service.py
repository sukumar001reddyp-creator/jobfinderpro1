from models.job import Job


class SearchService:

    def search(
        self,
        keyword="",
        location=None,
        company=None,
        country=None,
        city=None,
        remote=None,
        experience_level=None,
        employment_type=None,
        industry=None,
        sort="newest"
    ):

        query = Job.query.filter(
            Job.is_active == True
        )

        # Keyword
        if keyword:
            query = query.filter(
                Job.title.ilike(f"%{keyword}%")
            )

        # Location
        if location:
            query = query.filter(
                Job.city.ilike(f"%{location}%")
            )

        # Company
        if company:
            query = query.filter(
                Job.company.has(name=company)
            )

        # Country
        if country:
            query = query.filter(
                Job.country == country
            )

        # Employment
        if employment_type:
            query = query.filter(
                Job.employment_type == employment_type
            )

        # Experience
        if experience_level:
            query = query.filter(
                Job.experience_level == experience_level
            )

        # Industry
        if industry:
            query = query.filter(
                Job.industry == industry
            )

        # Remote
        if remote is not None:
            query = query.filter(
                Job.remote == remote
            )

        # Sorting
        if sort == "oldest":

            query = query.order_by(
                Job.created_at.asc()
            )

        elif sort == "salary_high":

            query = query.order_by(
                Job.salary_max.desc()
            )

        elif sort == "salary_low":

            query = query.order_by(
                Job.salary_min.asc()
            )

        else:

            query = query.order_by(
                Job.created_at.desc()
            )

        return query