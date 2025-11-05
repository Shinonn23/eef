import logging
import frappe
from frappe.utils import nowdate, add_days

# Remove frappe logger and set up Python logging to console
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)


def send_email_daily():
    log_prefix = "SENDING_EMAIL_DAILY"
    logger.info(f"[{log_prefix}:INFO]: Email process has started.")

    today = nowdate()
    end_date = add_days(today, 100)
    docs = frappe.get_all(
        "Tracking Internal Items",
        filters=[["folllowup_plan_date", ">=", today], ["folllowup_plan_date", "<=", end_date]],
        order_by="folllowup_plan_date asc",
        fields=["*"],
    )

    msg_list = ""
    for doc in docs:
        parent = frappe.get_doc("Tracking Internal", doc["parent"])
        parent_url = frappe.utils.get_url_to_form("Tracking Internal", parent.name)
        msg_list += f'<li>{doc["folllowup_plan_date"] or "[No Due Date]"} : {doc["topic"] or "[No Topic]"} : {doc["important_note"] or "[No Note]"} : {doc["followup_topic"] or "[No Topic]"} (<a href="{parent_url}">View Document</a>)</li>'

    message = f"""
        <h1>Upcoming Internal Item Follow-ups</h1>
        <ul>{msg_list}</ul>
    """
    frappe.sendmail(
        recipients=["nnnpooh@gmail.com"],
        subject="Reminder: Upcoming Internal Item Follow-ups",
        message=message,
    )


if __name__ == "__main__":
    send_email_daily()
