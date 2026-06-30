# utils/job_deduplicator.py
from extensions import db
from models.job import Job


class JobDeduplicator:
    @staticmethod
    def normalize_title(title):
        return (title or "").lower().strip().replace(" ", "").replace("-", "")

    @staticmethod
    def save_unique_jobs(raw_jobs):
        saved = 0
        for job in raw_jobs:
            if not Job.query.filter_by(title=job.get("title"), company=job.get("company")).first():
                # Create Job object and save
                new_job = Job(
                    title=job.get("title"),
                    company=job.get("company"),
                    location=job.get("location"),
                    description=job.get("description"),
                    apply_url=job.get("apply_url")
                )
                db.session.add(new_job)
                saved += 1
        db.session.commit()
        print(f"✅ Saved {saved} unique jobs")
        return saved