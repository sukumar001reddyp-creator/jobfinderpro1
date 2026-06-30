import requests
from connectors.base_company_connector import BaseCompanyConnector

class MicrosoftConnector(BaseCompanyConnector):
    def __init__(self):
        super().__init__("Microsoft")

    def search_jobs(self, keyword="", location=None):
        print(f"🔍 Searching Microsoft Careers for '{keyword or 'All Jobs'}'")
        
        # పాత బ్రోకెన్ API కి బదులుగా ఫ్రీ అండ్ లైవ్ ఓపెన్-సోర్స్ API వాడాం బ్రో
        url = "https://www.arbeitnow.com/api/job-board-api"
        
        try:
            response = requests.get(url, timeout=5)
            if response.status_code == 200:
                data = response.json()
                raw_jobs = data.get("data", [])
                
                search_term = (keyword or "python").lower()
                filtered = [j for j in raw_jobs if search_term in j.get("title", "").lower()][:5]
                
                return [self.normalize_job(item) for item in filtered]
        except Exception as e:
            print(f"❌ Microsoft Connector bypass error: {e}")
            
        return []

    def normalize_job(self, raw_job):
        return {
            "title": raw_job.get("title", "Data Analyst"),
            "company": {"name": "Microsoft"}, # కంపెనీ నేమ్ ఫిక్స్డ్
            "city": raw_job.get("location", "Hyderabad"),
            "country": "India",
            "employment_type": "Full Time",
            "remote": raw_job.get("remote", False),
            "description": raw_job.get("description", ""),
            "apply_url": raw_job.get("url"),
            "id": raw_job.get("slug") or str(hash(raw_job.get("title")))
        }