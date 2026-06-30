from flask import Blueprint, render_template

from models.job import Job
from models.company import Company
from models.job_source import JobSource

# Connector imports
from connectors.company.greenhouse_connector import GreenhouseConnector
from connectors.manager import ConnectorManager

home_bp = Blueprint("home", __name__)


@home_bp.route("/")
def home():

    # Get latest jobs from Connector
    manager = ConnectorManager()
    manager.register(GreenhouseConnector())
    all_jobs = manager.search()

    # Latest 9 jobs
    latest_jobs = all_jobs[:9]

    # Stats from connector data
    job_count = len(all_jobs)
    
    # Unique companies count
    company_count = len({
        job.company.name if hasattr(job.company, 'name') 
        else getattr(job.company, 'name', str(job.company))
        for job in all_jobs if hasattr(job, 'company') and job.company
    }) or 1

    source_count = 1  # You can improve this later if needed

    return render_template(
        "home/index.html",
        latest_jobs=latest_jobs,
        job_count=job_count,
        company_count=company_count,
        source_count=source_count
    )