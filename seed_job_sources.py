from extensions import db
from models.job_source import JobSource
from app import create_app

def seed_job_sources():
    sources = [
        {"name": "Greenhouse", "source_type": "api", "is_active": True},
        {"name": "LinkedIn", "source_type": "scraper", "is_active": True},
        {"name": "Indeed", "source_type": "scraper", "is_active": True},
        {"name": "Naukri", "source_type": "scraper", "is_active": True},
        {"name": "Google Jobs", "source_type": "api", "is_active": True},
    ]

    for source in sources:
        existing = JobSource.query.filter_by(name=source["name"]).first()
        if not existing:
            new_source = JobSource(
                name=source["name"],
                source_type=source["source_type"],
                is_active=source["is_active"]
            )
            db.session.add(new_source)
            print(f"✅ Added {source['name']}")
        else:
            print(f"⚡ {source['name']} already exists")

    db.session.commit()
    print("🎉 All job sources seeded successfully!")

if __name__ == "__main__":
    app = create_app()
    with app.app_context():
        seed_job_sources()