from app import create_app
from extensions import db
from models.job_source import JobSource

app = create_app()

with app.app_context():

    sources = [
        {
            "name": "Greenhouse",
            "source_type": "API",
            "website": "https://www.greenhouse.io"
        },
        {
            "name": "Lever",
            "source_type": "API",
            "website": "https://www.lever.co"
        },
        {
            "name": "Workday",
            "source_type": "API",
            "website": "https://www.workday.com"
        },
        {
            "name": "RSS",
            "source_type": "RSS",
            "website": ""
        }
    ]

    for source in sources:

        exists = JobSource.query.filter_by(
            name=source["name"]
        ).first()

        if not exists:

            db.session.add(
                JobSource(
                    name=source["name"],
                    source_type=source["source_type"],
                    website=source["website"],
                    api_available=source["source_type"] == "API",
                    rss_available=source["source_type"] == "RSS",
                    is_active=True
                )
            )

            print(f"✔ Added: {source['name']}")

        else:

            print(f"⏩ Already Exists: {source['name']}")

    db.session.commit()

    print("\n✅ Job Sources Ready!")