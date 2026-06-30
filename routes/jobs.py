from flask import Blueprint, render_template, abort, redirect, url_for, flash, request
from flask_login import current_user

from models.job import Job
from services.applied_job_service import AppliedJobService
from services.recent_job_service import RecentJobService
from connectors.manager import ConnectorManager
from types import SimpleNamespace

jobs_bp = Blueprint("jobs", __name__, url_prefix="/jobs")


@jobs_bp.route("/<int:job_id>")
def detail(job_id):
    job = Job.query.get(job_id)

    if not job:
        manager = ConnectorManager()
        all_jobs = manager.search_all()
        
        matched_job = next((j for j in all_jobs if str(j.get("id")) == str(job_id)), None)
        
        if matched_job:
            comp_obj = SimpleNamespace(name=matched_job.get("company", {}).get("name", "Company"))
            
            job = SimpleNamespace(
                id=matched_job.get("id"),
                title=matched_job.get("title"),
                company=comp_obj,
                city=matched_job.get("city"),
                country=matched_job.get("country"),
                employment_type=matched_job.get("employment_type"),
                remote=matched_job.get("remote"),
                description=matched_job.get("description"),
                apply_url=matched_job.get("apply_url"),   # Important: External link
                logo_url=matched_job.get("logo_url"),
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

    # 🚀 నీ rapid_connector నుండి వచ్చే రియల్ లైవ్ జాబ్స్ ని లోడ్ చేస్తున్నాం బ్రో
    manager = ConnectorManager()
    all_jobs = manager.search_all()
    matched_job = next((j for j in all_jobs if j["id"] == job_id), None)

    try:
        # మన లోకల్ డేటాబేస్ లో అప్లై రికార్డ్ సేవ్ అవుతుంది
        AppliedJobService.apply(current_user.id, job_id)
    except Exception:
        pass

    # 🌟 [100% PURE ORIGINAL LINK ROUTING]:
    # నీ rapid_connector.py ఏ ఒరిజినల్ అప్లై లింక్ ఇస్తే.. ఏ మార్పు లేకుండా డైరెక్ట్ గా ఆ లింక్ కే పంపేస్తున్నాం బ్రో!
    if matched_job and "apply_url" in matched_job:
        target_url = matched_job["apply_url"]
        
        # యుఆర్ఎల్ కి ముందు http లేదా https ఉండేలా చూసుకుంటున్నాం బ్రో
        if not target_url.startswith(("http://", "https://")):
            target_url = f"https://{target_url}"
            
        return redirect(target_url) # 👈 ఇది నేరుగా ఆ ఒరిజినల్ జాబ్ పేజీకే తీసుకెళ్తుంది!

    # ఒకవేళ ఏ లింక్ దొరకకపోతే నార్మల్ గా డీటెయిల్స్ పేజీ కి వస్తుంది
    return redirect(url_for("jobs.detail", job_id=job_id))