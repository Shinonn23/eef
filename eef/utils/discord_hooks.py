import logging
import os
from pathlib import Path

import requests
from dotenv import load_dotenv

from eef import ROOT_PATH

# Remove frappe logger and set up Python logging to console
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

# Load environment variables from .env file
TEMP_PATH = ROOT_PATH / "temp"
dotenv_path = ROOT_PATH / ".env"
load_dotenv(dotenv_path=dotenv_path)


def send_discord_webhook(source="", message=""):
    webhook_url = os.getenv("discord_webhook_url")
    if not webhook_url:
        logger.warning("Discord webhook URL is not set in environment variables.")
        return

    data = {"content": f"Test from [{source or 'Unknown Source'}]\n" + message}
    response = requests.post(webhook_url, json=data)
    if response.status_code == 204:
        logger.info("Discord webhook message sent successfully.")
    else:
        logger.error(
            f"Failed to send Discord webhook message. Status code: {response.status_code}, Response: {response.text}"
        )
