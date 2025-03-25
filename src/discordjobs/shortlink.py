import logging
import requests
import os
from dotenv import load_dotenv

load_dotenv()
LOGGER = logging.getLogger(__name__)

def create_shortlink(url):
    """
    Create a short link using the Short.io API.

    Args:
        url (str): The long URL for which a short link needs to be generated.

    Returns:
        str: The generated short link if successful, otherwise None.
    """
    SHORTIO_API_KEY = os.getenv('SHORTIO_API_KEY')
    response = requests.post(
        "https://api.short.io/links",
        json={
            "domain": "sysar.my",
            "originalURL": url,
        },
        headers={
            "authorization": SHORTIO_API_KEY,
            "content-type": "application/json",
        },
    )

    try:
        response.raise_for_status()
        data = response.json()
        LOGGER.info(f"Created short URL {data['shortURL']} for {data['originalURL']}")
        return data["shortURL"]
    except Exception as e:
        LOGGER.error(e)
