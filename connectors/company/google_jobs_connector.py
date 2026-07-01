import requests
from models.job_result import JobResult, CompanyResult


class GoogleJobsConnector:

    def __init__(self):
        self.api_key = "1f0d714ee3a8dc6638d30834e3c232642303724b"
        self.url = "https://google.serper.dev/jobs"

    def search(self, query="Software Engineer", location="Hyderabad", limit=30):
        print(f"🔍 Google Jobs searching: {query}")

        payload = {
            "q": f"{query} jobs in {location}",
            "gl": "in",
            "hl": "en"
        }
        headers = {
            "X-API-KEY": self.api_key,
            "Content-Type": "application/json"
        }
        try:
            response = requests.post(
                self.url,
                headers=headers,
                json=payload,
                timeout=30
            )
            print("Status:", response.status_code)
            data = response.json()
            print(data)
            if response.status_code != 200:
                return []
            job_list = data.get("jobs", [])
            jobs = []
            for job in job_list:
                company = CompanyResult(
                    name=job.get("company", "Unknown"),
                    logo_url=None
                )
                jobs.append(
                    JobResult(
                        job_id=str(job.get("id", "")),
                        title=job.get("title", ""),
                        company=company,
                        city=job.get("location", ""),
                        country="India",
                        employment_type=job.get("employmentType", ""),
                        remote=job.get("isRemote", False),
                        salary_min=None,
                        salary_max=None,
                        apply_url=job.get("applyLink") or job.get("link"),
                        description=job.get("description", ""),
                        source="Google Jobs",
                        experience_level="",
                        industry=""
                    )
                )
            print(f"✅ Google Jobs: {len(jobs)} jobs")
            return jobs
        except Exception as e:
            print("Google Error:", e)
            return []