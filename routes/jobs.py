from flask import Blueprint, render_template, abort, redirect, url_for, flash, request
from flask_login import current_user

from models.job import Job
from services.applied_job_service import AppliedJobService
from services.recent_job_service import RecentJobService
from connectors.manager import ConnectorManager
from connectors.company.greenhouse_connector import GreenhouseConnector
from types import SimpleNamespace


def safe_get(obj, key, default=None):
    """Safe get for both dict and object"""
    if isinstance(obj, dict):
        return obj.get(key, default)
    else:
        # For JobResult or other objects
        return getattr(obj, key, default)


jobs_bp = Blueprint("jobs", __name__, url_prefix="/jobs")


@jobs_bp.route("/<int:job_id>")
def detail(job_id):
    job = Job.query.get(job_id)

    if not job:
        manager = ConnectorManager()
        manager.register(GreenhouseConnector())

        all_jobs = manager.search()

        matched_job = next(
            (j for j in all_jobs if str(safe_get(j, "id", "")) == str(job_id)),
            None
        )
        
        if matched_job:
            comp_name = safe_get(safe_get(matched_job, "company", {}), "name", "Company")
            comp_obj = SimpleNamespace(name=comp_name)
            
            job = SimpleNamespace(
                id=safe_get(matched_job, "id"),
                title=safe_get(matched_job, "title"),
                company=comp_obj,
                city=safe_get(matched_job, "city"),
                country=safe_get(matched_job, "country"),
                employment_type=safe_get(matched_job, "employment_type"),
                remote=safe_get(matched_job, "remote"),
                description=safe_get(matched_job, "description"),
                apply_url=safe_get(matched_job, "apply_url"),
                logo_url=safe_get(matched_job, "logo_url"),
                salary_min=1200000,
                salary_max=2400000
            )
        else:
            abort(404)

    # Recently viewed
    if current_user.is_authenticated and hasattr(job, 'id'):
        try:
            RecentJobService.add_job(current_user.id, job.id)
        except:
            pass

    # Check if applied
    is_applied = False
    if current_user.is_authenticated and hasattr(job, 'id'):
        try:
            is_applied = AppliedJobService.is_applied(current_user.id, job.id)
        except:
            is_applied = False

    return render_template(
        "jobs/detail.html",
        job=job,
        is_applied=is_applied
    )


@jobs_bp.route("/<int:job_id>/apply", methods=["POST"])
def apply_job(job_id):
    if not current_user.is_authenticated:
        flash("Please login to apply for this position!", "danger")
        return redirect(url_for("auth.login"))

    # Load real jobs from connector
    manager = ConnectorManager()
    manager.register(GreenhouseConnector())
    
    # ✅ Changed search_all() → search() because search_all doesn't exist
    all_jobs = manager.search()

    matched_job = next(
        (j for j in all_jobs if str(safe_get(j, "id", "")) == str(job_id)), 
        None
    )

    try:
        # Save apply record in local DB
        AppliedJobService.apply(current_user.id, job_id)
    except Exception:
        pass

    # Redirect to original apply URL from connector
    if matched_job and safe_get(matched_job, "apply_url"):
        target_url = safe_get(matched_job, "apply_url")
        
        # Ensure URL has protocol
        if not target_url.startswith(("http://", "https://")):
            target_url = f"https://{target_url}"
            
        return redirect(target_url)

    # Fallback
    return redirect(url_for("jobs.detail", job_id=job_id))