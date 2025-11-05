# Copyright (c) 2025, Siwat Sroisuwan and contributors
# For license information, please see license.txt
import datetime

import frappe
from frappe import _
from frappe.utils import add_days, get_url_to_form, getdate, nowdate

NUMBER_OF_DAYS_AHEAD = 30


def execute(filters: dict | None = None):
    """Return columns and data for the report.

    This is the main entry point for the report. It accepts the filters as a
    dictionary and should return columns and data. It is called by the framework
    every time the report is refreshed or a filter is updated.
    """
    columns = get_columns()
    data = get_data()

    return columns, data


def get_columns() -> list[dict]:
    """Return columns for the report.

    One field definition per column, just like a DocType field definition.
    """
    return [
        {
            "label": _("Follow-up Plan Date"),
            "fieldname": "followup_plan_date",
            "fieldtype": "Data",
        },
        {
            "label": _("Days Remaining"),
            "fieldname": "days_remaining",
            "fieldtype": "Int",
        },
        {
            "label": _("Tracking Internal Document"),
            "fieldname": "tracking_internal_document",
            "fieldtype": "Link",
            "options": "Tracking Internal",
        },
        {
            "label": _("Topic"),
            "fieldname": "topic",
            "fieldtype": "Data",
        },
        {
            "label": _("Important Note"),
            "fieldname": "important_note",
            "fieldtype": "Data",
        },
    ]


def get_data() -> list[list]:
    """Return data for the report.

    The report data is a list of rows, with each row being a list of cell values.
    """

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

    data = []
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

        row = [doc["folllowup_plan_date"], due_in_days, parent.name, doc["topic"], doc["important_note"]]
        data.append(row)

    return data
