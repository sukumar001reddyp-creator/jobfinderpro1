class JobNormalizer:

    @staticmethod
    def normalize(job):

        return {
            "title": job.get("title"),
            "description": job.get("description"),
            "company": job.get("company"),
            "country": job.get("country"),
            "city": job.get("city"),
            "apply_url": job.get("apply_url"),
            "employment_type": job.get("employment_type"),
            "experience_level": job.get("experience_level"),
            "industry": job.get("industry"),
            "salary_min": job.get("salary_min"),
            "salary_max": job.get("salary_max"),
            "currency": job.get("currency"),
        }