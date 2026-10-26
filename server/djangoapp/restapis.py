
# Uncomment the imports below before adding the function code
import requests
import os
from dotenv import load_dotenv

load_dotenv()

backend_url = os.getenv(
    'backend_url', default="http://localhost:3030"
)
sentiment_analyzer_url = os.getenv(
    'sentiment_analyzer_url',
    default="http://localhost:5050/"
)


def get_request(endpoint, **kwargs):
    """Send a GET request to the backend API."""
    request_url = backend_url + endpoint
    response = requests.get(request_url, params=kwargs)
    return response
