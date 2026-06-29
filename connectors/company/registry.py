from .microsoft_connector import MicrosoftConnector
from .google_connector import GoogleConnector
from .amazon_connector import AmazonConnector
from .greenhouse_connector import GreenhouseConnector

COMPANY_CONNECTORS = [

    MicrosoftConnector,

    GoogleConnector,

    AmazonConnector,

    GreenhouseConnector,

]