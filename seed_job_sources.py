    def search(self, query="Software Engineer", location="Hyderabad", limit=30):
        print(f"🔍 Google Jobs searching: {query} in {location}")

        payload = {
            "q": query,
            "gl": "in",
            "hl": "en",
            "location": location,
            "num": limit
        }

        headers = {
            'X-API-KEY': self.api_key,
            'Content-Type': 'application/json'
        }

        try:
            response = requests.post(self.url, json=payload, headers=headers)
            data = response.json()

            jobs = []
            job_list = data.get('jobs', [])[:limit]

            for job in job_list:
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