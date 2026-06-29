import feedparser

from connectors.base_connector import BaseConnector


class RSSConnector(BaseConnector):

    def __init__(self, source_name, feed_url):

        super().__init__(source_name)

        self.feed_url = feed_url

    def search_jobs(self, keyword, location=None):

        jobs = []

        feed = feedparser.parse(self.feed_url)

        keyword = keyword.lower() if keyword else ""

        for entry in feed.entries:

            title = getattr(entry, "title", "")

            summary = getattr(entry, "summary", "")

            if keyword:

                text = f"{title} {summary}".lower()

                if keyword not in text:
                    continue

            jobs.append(
                self.normalize_job(entry)
            )

        return jobs

    def normalize_job(self, raw_job):

        return {

            "title": getattr(raw_job, "title", ""),

            "description": getattr(raw_job, "summary", ""),

            "company": "Unknown",

            "country": "",

            "city": "",

            "remote": False,

            "experience_level": "",

            "employment_type": "",

            "industry": "",

            "salary_min": None,

            "salary_max": None,

            "currency": "",

            "apply_url": getattr(raw_job, "link", ""),

            "source": self.source_name

        }