import frappe
from typing import Any


@frappe.whitelist()
def sync_partnerships(doctype: str, partnerships: Any):
    """
    Synchronizes partnership institutions and their associated majors.
    This function should be called when the business or educational institution is updated.
    """
    print(
        f"Syncing partnerships for doctype: {doctype}, partnerships: {frappe.parse_json(partnerships)}"
    )
    if doctype == "Business":
        institutions_data: list[dict[str, str]] = frappe.db.get_all(
            "Partnership Institution",
            fields=["educational_institution", "parent"],
            filters={"educational_institution": ["in", ["Sawananan", "AnotherOne"]]},
        )

        business_data: list[dict[str, str]] = frappe.db.get_all(
            "Partnership Business",
            fields=["educational_institution", "parent"],
            filters={"educational_institution": ["in", ["Sawananan", "AnotherOne"]]},
        )

    #     frappe.get_doc(
    #     {
    #         "doctype": "Sync Partnerships",
    #     }
    # )
