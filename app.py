from flask import Flask
from config import Config
import os

# Routes
from routes.home import home_bp
from routes.search import search_bp
from routes.jobs import jobs_bp
from routes.auth import auth_bp
from routes.resume import resume_bp
from routes.saved_jobs import saved_jobs_bp
from routes.dashboard import dashboard_bp
from routes.applied_jobs import applied_jobs_bp
from routes.job_alert import job_alert_bp
from routes.recent_jobs import recent_jobs_bp
from routes.pdf import pdf_bp

# Extensions
from extensions import db, migrate, login_manager, mail

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    mail.init_app(app)

    # ==================== FLASK-LOGIN USER LOADER ====================
    @login_manager.user_loader
    def load_user(user_id):
        from models.user import User
        return User.query.get(int(user_id))

    @login_manager.unauthorized_handler
    def unauthorized():
        from flask import flash, redirect, url_for
        flash("Please log in to access this page.", "warning")
        return redirect(url_for("auth.login"))
    # ============================================================

    # Import models
    import models

    # Register blueprints
    app.register_blueprint(home_bp)
    app.register_blueprint(search_bp)
    app.register_blueprint(jobs_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(resume_bp)
    app.register_blueprint(saved_jobs_bp)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(applied_jobs_bp)
    app.register_blueprint(job_alert_bp)
    app.register_blueprint(recent_jobs_bp)
    app.register_blueprint(pdf_bp)

    return app


app = create_app()

# ==================== TABLE CREATION ====================
with app.app_context():
    db.create_all()
    print("✅ Tables created on Render server successfully!")
# =======================================================

if __name__ == "__main__":
    app.run(debug=True)