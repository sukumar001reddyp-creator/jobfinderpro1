from models.saved_job import SavedJob
from extensions import db


class SavedJobService:

    @staticmethod
    def save_job(user_id, job_id):

        existing = SavedJob.query.filter_by(
            user_id=user_id,
            job_id=job_id
        ).first()

        if existing:
            return False

        saved = SavedJob(
            user_id=user_id,
            job_id=job_id
        )

        db.session.add(saved)
        db.session.commit()

        return True

    @staticmethod
    def remove_job(user_id, job_id):

        saved = SavedJob.query.filter_by(
            user_id=user_id,
            job_id=job_id
        ).first()

        if not saved:
            return False

        db.session.delete(saved)
        db.session.commit()

        return True

    @staticmethod
    def get_saved_jobs(user_id):

        return SavedJob.query.filter_by(
            user_id=user_id
        ).all()

    @staticmethod
    def is_saved(user_id, job_id):

        return SavedJob.query.filter_by(
            user_id=user_id,
            job_id=job_id
        ).first() is not None