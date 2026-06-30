import requests
from connectors.base_company_connector import BaseCompanyConnector


class GoogleConnector(BaseCompanyConnector):
    def __init__(self):
        super().__init__("Google")

    def search_jobs(self, keyword="", location=None):
        print(f"🔍 Searching Google Careers for '{keyword or 'All Jobs'}'")

        url = "https://remotive.com/api/remote-jobs"
        params = {
            "search": keyword or "",
            "limit": 100
        }

        try:
            response = requests.get(url, params=params, timeout=10)
            if response.status_code == 200:
                data = response.json()
                jobs = [self.normalize_job(item) for item in data.get("jobs", [])]
                print(f"✅ Google returned {len(jobs)} jobs")
                return jobs
        except Exception as e:
            print(f"Google error: {e}")

        return []

    def normalize_job(self, raw_job):
        return {
            "title": raw_job.get("title"),
            "company": raw_job.get("company_name", "Google"),
            "location": raw_job.get("candidate_required_location", "Remote"),
            "description": raw_job.get("description", ""),
            "apply_url": raw_job.get("url"),
            "id": raw_job.get("id") or str(hash(raw_job.get("title")))
        }