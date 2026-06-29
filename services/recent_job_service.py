from extensions import db
from models.recent_job import RecentJob


class RecentJobService:

    @staticmethod
    def add_job(user_id, job_id):

        # Check if already exists
        existing = RecentJob.query.filter_by(
            user_id=user_id,
            job_id=job_id
        ).first()

        if existing:

            db.session.delete(existing)
            db.session.commit()

        recent = RecentJob(
            user_id=user_id,
            job_id=job_id
        )

        db.session.add(recent)
        db.session.commit()

        # Keep only latest 20 jobs
        jobs = RecentJob.query.filter_by(
            user_id=user_id
        ).order_by(
            RecentJob.viewed_at.desc()
        ).all()

        if len(jobs) > 20:

            for job in jobs[20:]:

                db.session.delete(job)

            db.session.commit()

    @staticmethod
    def get_recent_jobs(user_id):

        return RecentJob.query.filter_by(
            user_id=user_id
        ).order_by(
            RecentJob.viewed_at.desc()
        ).all()