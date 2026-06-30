# connectors/company/registry.py
from .microsoft_connector import MicrosoftConnector
from .google_connector import GoogleConnector
from .amazon_connector import AmazonConnector

COMPANY_CONNECTORS = [
    MicrosoftConnector,
    GoogleConnector,
    AmazonConnector,
]