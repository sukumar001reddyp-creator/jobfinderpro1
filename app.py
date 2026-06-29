from flask import Flask
from config import Config
from routes.auth import auth_bp
from routes.jobs import jobs_bp
from routes.resume import resume_bp
from routes.saved_jobs import saved_jobs_bp
from routes.dashboard import dashboard_bp
from routes.applied_jobs import applied_jobs_bp
from routes.job_alert import job_alert_bp
from routes.recent_jobs import recent_jobs_bp
from routes.pdf import pdf_bp
from extensions import (
    db,
    migrate,
    login_manager,
    mail
)

from routes.home import home_bp
# Import models so Flask-Migrate can detect them
import models
from routes.search import search_bp

def create_app():
    app = Flask(__name__)

    # Load Configuration
    app.config.from_object(Config)

    # Initialize Extensions
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    import utils.login_manager
    mail.init_app(app)
    # Import models so Flask-Migrate can detect them
    import models

    # Register Blueprints
    app.register_blueprint(home_bp)
    app.register_blueprint(search_bp)
    app.register_blueprint(jobs_bp)
    app.register_blueprint(saved_jobs_bp)
    app.register_blueprint(job_alert_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(resume_bp)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(applied_jobs_bp)
    app.register_blueprint(recent_jobs_bp)
    app.register_blueprint(pdf_bp)
    return app


app = create_app()

if __name__ == "__main__":
    app.run(debug=True)