from extensions import db
from models.job import Job


class JobService:

    @staticmethod
    def get_by_source_job_id(source_job_id):

        return Job.query.filter_by(
            source_job_id=source_job_id
        ).first()

    @staticmethod
    def save_job(job_data):

        existing_job = JobService.get_by_source_job_id(
            job_data.get("source_job_id")
        )

        if existing_job:
            return existing_job

        job = Job(

            title=job_data.get("title"),
            slug=job_data.get("slug"),

            source_job_id=job_data.get("source_job_id"),

            company_id=job_data.get("company_id"),
            job_source_id=job_data.get("job_source_id"),

            description=job_data.get("description"),

            category=job_data.get("category"),
            industry=job_data.get("industry"),
            skills=job_data.get("skills"),

            country=job_data.get("country"),
            state=job_data.get("state"),
            city=job_data.get("city"),

            remote=job_data.get("remote", False),

            experience_level=job_data.get("experience_level"),
            experience_min=job_data.get("experience_min"),
            experience_max=job_data.get("experience_max"),

            employment_type=job_data.get("employment_type"),

            salary_min=job_data.get("salary_min"),
            salary_max=job_data.get("salary_max"),
            salary_type=job_data.get("salary_type"),
            currency=job_data.get("currency"),

            apply_url=job_data.get("apply_url"),

            posted_date=job_data.get("posted_date"),
            expires_at=job_data.get("expires_at"),

            status=job_data.get("status", "active"),
            is_active=job_data.get("is_active", True)
        )

        db.session.add(job)
        db.session.commit()

        return job