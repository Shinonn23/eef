from typing import Any, cast

import frappe

from eef.utils.partnerships import (
    build_businesses_to_institutions_map,
    build_institutions_to_businesses_map,
    extract_current_entities,
    get_partnerships,
    remove_business_from_institution,
    remove_institution_from_business,
    sync_business_bidirectional,
    sync_institution_bidirectional,
)
from eef.utils.types import PartnershipBusiness


@frappe.whitelist()
def sync_partnerships(doctype: str, partnerships: Any, document_name: str | None = None):
    """
    Synchronizes partnership institutions and their associated majors.
    This function should be called when the business or educational institution is updated.

    Args:
        doctype (str): The doctype of the document being updated (e.g., "Business" or "Educational Institution").
        partnerships (Any): A JSON string containing the partnerships data.
        document_name (str): The current name of the document (used when partnerships is empty).
    """
    try:
        print(
            f"Syncing partnerships for doctype: {doctype}, partnerships: {partnerships}, document_name: {document_name}"
        )

        # Validate input parameters
        if not doctype or doctype not in ["Business", "Educational Institution"]:
            frappe.throw(f"Invalid doctype: {doctype}. Must be 'Business' or 'Educational Institution'")
            return

        # Handle empty or None partnerships
        if not partnerships:
            partnerships_data = []
        else:
            try:
                partnerships_data = cast(list[dict[str, str]], frappe.parse_json(partnerships))

            except Exception as e:
                frappe.log_error(f"Error parsing partnerships JSON: {e!s}")
                partnerships_data = []

        if doctype == "Business":
            _sync_business_partnerships(partnerships_data, document_name)
        elif doctype == "Educational Institution":
            _sync_educational_institution_partnerships(partnerships_data, document_name)

    except Exception as e:
        frappe.log_error(f"Error in sync_partnerships: {e!s}")
        frappe.throw(f"Failed to sync partnerships: {e!s}")


def _sync_business_partnerships(partnerships_data: list[dict[str, str]], document_name: str | None = None):
    """
    Sync partnerships from the perspective of a business.
    Handles adding/removing partnerships for educational institutions
    and ensures bidirectional sync.
    """
    try:
        # Extract institutions and business name
        current_institutions, current_business_name = extract_current_entities(
            partnerships_data, "educational_institution"
        )
        if not current_business_name:
            print("No current business name found in partnerships, skipping sync.")
            return

        # Get previous partnerships
        previous_partnerships: list[dict[str, str]] = get_partnerships(current_business_name)
        previous_institutions = [p["educational_institution"] for p in previous_partnerships]

        # Determine removed institutions
        removed_institutions = set(previous_institutions) - set(current_institutions)

        # Build mapping institution -> businesses
        institutions_to_businesses = build_institutions_to_businesses_map(current_institutions)

        # Sync current institutions
        for institution in current_institutions:
            sync_institution_bidirectional(institution, current_business_name, institutions_to_businesses)

        # Remove business from removed institutions
        for removed_institution in removed_institutions:
            remove_business_from_institution(removed_institution, current_business_name)

    except Exception as e:
        frappe.log_error(f"Error in _sync_business_partnerships: {e!s}")
        raise


def _sync_educational_institution_partnerships(
    partnerships_data: list[dict[str, str]], document_name: str | None = None
):
    """
    Sync partnerships from the perspective of an Educational Institution.
    Handles adding/removing partnerships for businesses and ensures bidirectional sync.
    """
    try:
        # Extract businesses and institution name
        current_businesses, current_institution_name = extract_current_entities(partnerships_data, "business")
        if not current_institution_name:
            print("No current institution name found in partnerships, skipping sync.")
            return

        # Get previous businesses
        previous_partnerships = cast(
            list[PartnershipBusiness],
            frappe.db.get_all(
                "Partnership Business",
                fields=["business", "parent"],
                filters=({"business": ["in", current_businesses]} if current_businesses else {}),
            ),
        )
        previous_businesses = [p["business"] for p in previous_partnerships]

        # Determine removed businesses
        removed_businesses = set(previous_businesses) - set(current_businesses)
        # Build mapping business -> institutions
        businesses_to_institutions = build_businesses_to_institutions_map(current_businesses)

        # Sync current businesses
        for business in current_businesses:
            sync_business_bidirectional(business, current_institution_name, businesses_to_institutions)

        # Remove institution from removed businesses
        for removed_business in removed_businesses:
            remove_institution_from_business(removed_business, current_institution_name)

    except Exception as e:
        frappe.log_error(f"Error in _sync_educational_institution_partnerships: {e!s}")
        raise
