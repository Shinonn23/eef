from typing import Any, TypeVar, cast

import frappe

from eef.eef.doctype.educational_institution.educational_institution import (
    EducationalInstitution,
)
from eef.utils.types import PartnershipBusiness, PartnershipInstitution

T = TypeVar("T")


def get_all_typed(
    doctype: str, fields: list[str], filters: dict[str, Any], _t: type[T] | None = None
) -> list[T]:
    return cast(list[T], frappe.db.get_all(doctype, fields=fields, filters=filters))


def get_partnerships(parent: str) -> list[dict[str, str]]:
    result: list[dict[str, str]] = get_all_typed(
        "Partnership Institution", ["educational_institution"], {"parent": parent}
    )
    return result


def get_partnership_institutions(
    parent: str | None = None,
    institutions: list[str] | None = None,
) -> list[PartnershipInstitution]:
    """Wrapper แบบ type-safe สำหรับ get_all ของ Partnership Institution"""

    filters: dict[str, Any] = {}
    if parent:
        filters["parent"] = parent
    if institutions:
        filters["educational_institution"] = ["in", institutions]

    result: list[PartnershipInstitution] = get_all_typed(
        "Partnership Institution", ["educational_institution", "parent"], filters
    )

    # บังคับ type cast เพื่อให้ type checker เข้าใจ
    return result


def build_institutions_to_businesses_map(
    current_institutions: list[str],
) -> dict[str, list[str]]:
    """
    Get all existing partnerships for given institutions and group them by educational institution.
    Returns a dict mapping institution -> list of businesses.
    """
    existing_partnerships = get_partnership_institutions(institutions=current_institutions)
    institutions_to_businesses: dict[str, list[str]] = {}

    for partnership in existing_partnerships:
        inst = partnership["educational_institution"]
        business = partnership["parent"]
        if inst not in institutions_to_businesses:
            institutions_to_businesses[inst] = []
        if business not in institutions_to_businesses[inst]:
            institutions_to_businesses[inst].append(business)

    return institutions_to_businesses


def sync_institution_bidirectional(
    institution: str,
    current_business_name: str,
    institutions_to_businesses: dict[str, list[str]],
):
    """
    Ensure bidirectional sync between a business and an educational institution.
    Adds the current business to the institution if missing.
    Filters partnership_business to keep only valid businesses.
    """
    if not frappe.db.exists("Educational Institution", institution):
        frappe.log_error(f"Educational Institution {institution} does not exist")
        return

    try:
        edu_doc = cast(
            EducationalInstitution,
            frappe.get_doc("Educational Institution", institution),
        )

        # Add current business if not present
        current_businesses = [pb.business for pb in (edu_doc.partnership_business or [])]
        if current_business_name not in current_businesses:
            edu_doc.append("partnership_business", {"business": current_business_name})

        # Keep only valid businesses
        businesses_to_keep = institutions_to_businesses.get(institution, [])
        if current_business_name not in businesses_to_keep:
            businesses_to_keep.append(current_business_name)

        edu_doc.partnership_business = [
            pb
            for pb in (edu_doc.partnership_business or [])
            if pb.business in businesses_to_keep and frappe.db.exists("Business", pb.business)
        ]

        edu_doc.save(ignore_permissions=True)

    except Exception as e:
        frappe.log_error(f"Error syncing educational institution {institution}: {e!s}")


def remove_business_from_institution(institution: str, current_business_name: str):
    """
    Remove the current business from an educational institution's partnerships.
    """
    if not frappe.db.exists("Educational Institution", institution):
        return

    try:
        edu_doc = cast(
            EducationalInstitution,
            frappe.get_doc("Educational Institution", institution),
        )
        edu_doc.partnership_business = [
            pb for pb in (edu_doc.partnership_business or []) if pb.business != current_business_name
        ]
        edu_doc.save(ignore_permissions=True)
    except Exception as e:
        frappe.log_error(f"Error removing business from educational institution {institution}: {e!s}")


def extract_current_entities(
    partnerships_data: list[dict[str, str]],
    key: str,
    parent_key: str = "parent",
    document_name: str | None = None,
) -> tuple[list[str], str | None]:
    current_entities: list[str] = []
    current_parent = document_name
    for item in partnerships_data:
        if val := item.get(key):
            current_entities.append(val)
            if not current_parent and (parent_val := item.get(parent_key)):
                current_parent = parent_val
    return current_entities, current_parent


def build_businesses_to_institutions_map(
    current_businesses: list[str],
) -> dict[str, list[str]]:
    """
    Get all existing partnerships for given businesses and group them by business.
    Returns a dict mapping business -> list of institutions.
    """
    existing_partnerships: list[PartnershipBusiness] = get_all_typed(
        "Partnership Business",
        ["business", "parent"],
        {"business": ["in", current_businesses]} if current_businesses else {},
    )

    businesses_to_institutions: dict[str, list[str]] = {}
    for partnership in existing_partnerships:
        business = partnership["business"]
        institution = partnership["parent"]
        if business not in businesses_to_institutions:
            businesses_to_institutions[business] = []
        if institution not in businesses_to_institutions[business]:
            businesses_to_institutions[business].append(institution)

    return businesses_to_institutions


def sync_business_bidirectional(
    business: str,
    current_institution_name: str,
    businesses_to_institutions: dict[str, list[str]],
):
    """
    Ensure bidirectional sync between a business and an educational institution.
    Adds the current institution to the business if missing.
    Filters partnership_institution to keep only valid institutions.
    """
    import frappe

    from eef.eef.doctype.business.business import Business

    if not frappe.db.exists("Business", business):
        frappe.log_error(f"Business {business} does not exist")
        return

    try:
        business_doc = cast(Business, frappe.get_doc("Business", business))

        # Add current institution if not present
        current_institutions = [
            pi.educational_institution for pi in (business_doc.partnership_institution or [])
        ]
        if current_institution_name not in current_institutions:
            business_doc.append(
                "partnership_institution",
                {"educational_institution": current_institution_name},
            )

        # Keep only valid institutions
        institutions_to_keep = businesses_to_institutions.get(business, [])
        if current_institution_name not in institutions_to_keep:
            institutions_to_keep.append(current_institution_name)

        business_doc.partnership_institution = [
            pi
            for pi in (business_doc.partnership_institution or [])
            if pi.educational_institution in institutions_to_keep
            and frappe.db.exists("Educational Institution", pi.educational_institution)
        ]

        business_doc.save(ignore_permissions=True)

    except Exception as e:
        frappe.log_error(f"Error syncing business {business}: {e!s}")


def remove_institution_from_business(business: str, current_institution_name: str):
    """
    Remove the current institution from a business's partnership_institution.
    """
    import frappe

    from eef.eef.doctype.business.business import Business

    if not frappe.db.exists("Business", business):
        return

    try:
        business_doc = cast(Business, frappe.get_doc("Business", business))
        business_doc.partnership_institution = [
            pi
            for pi in (business_doc.partnership_institution or [])
            if pi.educational_institution != current_institution_name
        ]
        business_doc.save(ignore_permissions=True)

    except Exception as e:
        frappe.log_error(f"Error removing institution from business {business}: {e!s}")
