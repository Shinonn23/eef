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

    frappe.get_doc(
        {
            "doctype": "Sync Partnerships",
        }
    )

    return doctype, [
        partnership["educational_institution"]
        for partnership in frappe.parse_json(partnerships)
    ]
    # Here you can implement the logic to sync partnerships and majors
    # For example, you might want to update the database or perform some calculations
    # This is just a placeholder to demonstrate the function structure
    # return {"status": "success", "message": "Partnerships synchronized successfully."
