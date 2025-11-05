import datetime
import logging
import os
from pathlib import Path

import frappe
from dotenv import load_dotenv
from frappe.utils import add_days, get_url_to_form, getdate, nowdate

# Define the number of days ahead to check for follow-up items
NUMBER_OF_DAYS_AHEAD = 30
EMAIL_RECIPIENTS = ["nnnpooh@gmail.com"]

# Remove frappe logger and set up Python logging to console
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

# Load environment variables from .env file
script_path = Path(__file__).resolve()
app_root_path = script_path.parent.parent.parent
TEMP_PATH = app_root_path / "temp"
dotenv_path = app_root_path / ".env"
load_dotenv(dotenv_path=dotenv_path)
if "environment" not in os.environ:
    raise OSError("Missing required environment variables in .env file")


def send_email_daily():
    log_prefix = "SENDING_EMAIL_DAILY"
    logger.info(f"[{log_prefix}:INFO]: Email process has started.")

    # Only send email in PRODUCTION environment
    if os.getenv("environment") != "PRODUCTION":
        logger.info(f"[{log_prefix}:INFO]: Current environment is not PRODUCTION. Email will not be sent.")
        return

    today = nowdate()
    end_date = add_days(today, NUMBER_OF_DAYS_AHEAD)
    docs = frappe.get_all(
        "Tracking Internal Items",
        filters=[
            ["folllowup_plan_date", ">=", today],
            ["folllowup_plan_date", "<=", end_date],
        ],
        order_by="folllowup_plan_date asc",
        fields=["*"],
    )

    # If no documents found, log and exit
    if len(docs) == 0:
        logger.info(f"[{log_prefix}:INFO]: No follow-up items found for today.")
        return

    msg_list = ""
    for doc in docs:
        parent = frappe.get_doc("Tracking Internal", doc["parent"])
        parent_url = get_url_to_form("Tracking Internal", parent.name)

        deadline_dt = getdate(doc["folllowup_plan_date"])
        today_dt = getdate(today)

        # Make sure both are date objects
        if type(deadline_dt) is datetime.date and type(today_dt) is datetime.date:
            due_in_days = (deadline_dt - today_dt).days
        else:
            due_in_days = 0

        msg_list += f'<li>{doc["folllowup_plan_date"] or "[No Due Date]"} (Due in {due_in_days} days) : {doc["topic"] or "[No Topic]"} : {doc["important_note"] or "[No Note]"} : {doc["followup_topic"] or "[No Topic]"} (<a href="{parent_url}">View Document</a>)</li>'

    message = f"""
        <h1>Upcoming Internal Item Due in {NUMBER_OF_DAYS_AHEAD} Days</h1>
        <ul>{msg_list}</ul>
    """
    frappe.sendmail(
        recipients=EMAIL_RECIPIENTS,
        subject="Reminder: Upcoming Internal Item Follow-ups",
        message=message,
    )


if __name__ == "__main__":
    send_email_daily()
