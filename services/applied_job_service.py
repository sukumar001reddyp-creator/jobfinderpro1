from extensions import db
from models.applied_job import AppliedJob


class AppliedJobService:

    @staticmethod
    def apply(user_id, job_id):

        existing = AppliedJob.query.filter_by(
            user_id=user_id,
            job_id=job_id
        ).first()

        if existing:
            return False

        applied = AppliedJob(
            user_id=user_id,
            job_id=job_id
        )

        db.session.add(applied)
        db.session.commit()

        return True

    @staticmethod
    def remove(user_id, job_id):

        applied = AppliedJob.query.filter_by(
            user_id=user_id,
            job_id=job_id
        ).first()

        if not applied:
            return False

        db.session.delete(applied)
        db.session.commit()

        return True

    @staticmethod
    def is_applied(user_id, job_id):

        return AppliedJob.query.filter_by(
            user_id=user_id,
            job_id=job_id
        ).first() is not None