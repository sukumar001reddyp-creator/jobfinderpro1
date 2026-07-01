# connectors/company/registry.py
from .greenhouse_connector import GreenhouseConnector
from .microsoft_connector import MicrosoftConnector
from .google_connector import GoogleConnector
from .amazon_connector import AmazonConnector
from .lever import LeverConnector

COMPANY_CONNECTORS = [
    MicrosoftConnector,
    GoogleConnector,
    AmazonConnector,
    reenhouseConnector,
    LeverConnector,

]