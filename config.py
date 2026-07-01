import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# config.py ఉన్న రూట్ ఫోల్డర్ పాత్ తీసుకుంటుంది
BASE_DIR = os.path.abspath(os.path.dirname(__file__))

class Config:
    """Base Configuration"""

    # Flask
    SECRET_KEY = os.getenv("SECRET_KEY", "jobfinder-dev-secret-key")
    
    WTF_CSRF_ENABLED = True

    # Database - ఇక్కడ instance/jobfinder.db కి కరెక్ట్ అబ్సొల్యూట్ పాత్ సెట్ చేశాం
    SQLALCHEMY_DATABASE_URI = os.getenv(
        "DATABASE_URL",
        f"sqlite:///{os.path.join(BASE_DIR, 'instance', 'jobfinder.db')}"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Uploads
    UPLOAD_FOLDER = "uploads"
    MAX_CONTENT_LENGTH = 5 * 1024 * 1024  # 5 MB

    # Mail
    MAIL_SERVER = os.getenv("MAIL_SERVER")
    MAIL_PORT = int(os.getenv("MAIL_PORT", 587))
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.getenv("MAIL_USERNAME")
    MAIL_PASSWORD = os.getenv("MAIL_PASSWORD")
    MAIL_DEFAULT_SENDER = os.getenv("MAIL_DEFAULT_SENDER")