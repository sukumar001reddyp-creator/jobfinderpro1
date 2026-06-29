class MicrosoftParser:

    def parse(self, raw_job):

        return {
            "title": raw_job.get("title"),
            "description": raw_job.get("description"),
            "city": raw_job.get("city"),
            "country": raw_job.get("country"),
            "employment_type": raw_job.get("employment_type"),
            "experience_level": raw_job.get("experience_level"),
            "industry": raw_job.get("industry"),
            "salary_min": raw_job.get("salary_min"),
            "salary_max": raw_job.get("salary_max"),
            "currency": raw_job.get("currency"),
            "apply_url": raw_job.get("apply_url"),
        }