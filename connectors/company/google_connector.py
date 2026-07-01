import requests
from models.job_result import JobResult, CompanyResult

print("API Key:", self.api_key)
class GoogleJobsConnector:

    def __init__(self):
        self.api_key = "cecc3d859f78d24f973362a10f5699cbda0d070b"
        self.url = "https://google.serper.dev/jobs"

    def search(self, query="Software Engineer", location="Hyderabad", limit=30):
        print(f"🔍 Google Jobs searching: {query} in {location}")

        payload = {
            "q": f"{query} in {location}",
            "gl": "in",
            "hl": "en",
            "num": limit
        }

        headers = {
            'X-API-KEY': self.api_key,
            'Content-Type': 'application/json'
        }

        try:
            response = requests.post(self.url, json=payload, headers=headers)
            data = response.json()

            print(f"Status: {response.status_code}")
            print(f"Raw jobs received: {len(data.get('jobs', []))}")

            jobs = []
            for job in data.get('jobs', [])[:limit]:
                company = CompanyResult(
                    name=job.get('company', 'Unknown Company'),
                    logo_url=None
                )

                jobs.append(JobResult(
                    job_id=job.get('id'),
                    title=job.get('title'),
                    company=company,
                    city=job.get('location'),
                    country="India",
                    employment_type=job.get('employmentType', ''),
                    remote=job.get('isRemote', False),
                    salary_min=None,
                    salary_max=None,
                    apply_url=job.get('applyLink'),
                    description=job.get('description', ''),
                    source="Google Jobs",
                    experience_level="",
                    industry=""
                ))

            print(f"✅ Google Jobs: {len(jobs)} real jobs fetched")
            return jobs

        except Exception as e:
            print(f"❌ Google Jobs Error: {e}")
            return []