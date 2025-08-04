from typing import Any

import frappe


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
                partnerships_data: list[dict[str, str]] = frappe.parse_json(partnerships)
                if not isinstance(partnerships_data, list):
                    partnerships_data = []
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
    """Sync partnerships from Business perspective"""
    try:
        # Extract list of educational institutions from current partnerships
        current_institutions: list[str] = []
        current_business_name = document_name  # Use provided document name

        for partnership in partnerships_data:
            if partnership.get("educational_institution"):
                current_institutions.append(partnership["educational_institution"])
                # Use parent from partnership if document_name wasn't provided
                if not current_business_name and partnership.get("parent"):
                    current_business_name = partnership["parent"]

        if not current_business_name:
            # If no parent is found in partnerships and no document_name provided, we can't proceed
            print("No current business name found in partnerships, skipping sync.")
            return

        # Get previous state from database to compare with current state
        previous_partnerships = frappe.db.get_all(
            "Partnership Institution",
            fields=["educational_institution"],
            filters={"parent": current_business_name},
        )
        previous_institutions = [p["educational_institution"] for p in previous_partnerships]

        # Find institutions that were removed (in previous but not in current)
        removed_institutions = set(previous_institutions) - set(current_institutions)

        # Get all existing partnerships for other businesses with the same institutions
        existing_partnerships = frappe.db.get_all(
            "Partnership Institution",
            fields=["educational_institution", "parent"],
            filters={"educational_institution": ["in", current_institutions]} if current_institutions else {},
        )

        # Group by educational institution
        institutions_to_businesses = {}
        for partnership in existing_partnerships:
            inst = partnership["educational_institution"]
            business = partnership["parent"]
            if inst not in institutions_to_businesses:
                institutions_to_businesses[inst] = []
            if business not in institutions_to_businesses[inst]:
                institutions_to_businesses[inst].append(business)

        # For each educational institution, ensure bidirectional sync
        for institution in current_institutions:
            # Validate that the educational institution exists
            if not frappe.db.exists("Educational Institution", institution):
                frappe.log_error(f"Educational Institution {institution} does not exist")
                continue

            try:
                # Get the educational institution document
                edu_doc = frappe.get_doc("Educational Institution", institution)

                # Get current partnership businesses for this educational institution
                current_businesses = [pb.business for pb in (edu_doc.partnership_business or [])]

                # Add the current business if not already present
                if current_business_name not in current_businesses:
                    edu_doc.append("partnership_business", {"business": current_business_name})

                # Remove any businesses that are no longer in the institution's partnerships
                businesses_to_keep = institutions_to_businesses.get(institution, [])
                if current_business_name not in businesses_to_keep:
                    businesses_to_keep.append(current_business_name)

                # Filter partnership_business to keep only valid ones
                edu_doc.partnership_business = [
                    pb
                    for pb in (edu_doc.partnership_business or [])
                    if pb.business in businesses_to_keep and frappe.db.exists("Business", pb.business)
                ]

                # Save the educational institution document
                edu_doc.save(ignore_permissions=True)

            except Exception as e:
                frappe.log_error(f"Error syncing educational institution {institution}: {e!s}")
                continue

        # Handle removed institutions - remove current business from their partnership_business
        for removed_institution in removed_institutions:
            if not frappe.db.exists("Educational Institution", removed_institution):
                continue

            try:
                # Get the educational institution document
                edu_doc = frappe.get_doc("Educational Institution", removed_institution)

                # Remove the current business from partnership_business
                edu_doc.partnership_business = [
                    pb for pb in (edu_doc.partnership_business or []) if pb.business != current_business_name
                ]

                # Save the educational institution document
                edu_doc.save(ignore_permissions=True)

            except Exception as e:
                frappe.log_error(
                    f"Error removing business from educational institution {removed_institution}: {e!s}"
                )
                continue

    except Exception as e:
        frappe.log_error(f"Error in _sync_business_partnerships: {e!s}")
        raise


def _sync_educational_institution_partnerships(
    partnerships_data: list[dict[str, str]], document_name: str | None = None
):
    """Sync partnerships from Educational Institution perspective"""
    try:
        # Extract list of businesses from current partnerships
        current_businesses: list[str] = []
        current_institution_name = document_name  # Use provided document name

        for partnership in partnerships_data:
            if partnership.get("business"):
                current_businesses.append(partnership["business"])
                # Use parent from partnership if document_name wasn't provided
                if not current_institution_name and partnership.get("parent"):
                    current_institution_name = partnership["parent"]

        if not current_institution_name:
            # If no parent is found in partnerships and no document_name provided, we can't proceed
            print("No current institution name found in partnerships, skipping sync.")
            return

        # Get previous state from database to compare with current state
        previous_partnerships = frappe.db.get_all(
            "Partnership Business",
            fields=["business"],
            filters={"parent": current_institution_name},
        )
        previous_businesses = [p["business"] for p in previous_partnerships]

        # Find businesses that were removed (in previous but not in current)
        removed_businesses = set(previous_businesses) - set(current_businesses)

        # Get all existing partnerships for other institutions with the same businesses
        existing_partnerships = frappe.db.get_all(
            "Partnership Business",
            fields=["business", "parent"],
            filters={"business": ["in", current_businesses]} if current_businesses else {},
        )

        # Group by business
        businesses_to_institutions = {}
        for partnership in existing_partnerships:
            business = partnership["business"]
            institution = partnership["parent"]
            if business not in businesses_to_institutions:
                businesses_to_institutions[business] = []
            if institution not in businesses_to_institutions[business]:
                businesses_to_institutions[business].append(institution)

        # For each business, ensure bidirectional sync
        for business in current_businesses:
            # Validate that the business exists
            if not frappe.db.exists("Business", business):
                frappe.log_error(f"Business {business} does not exist")
                continue

            try:
                # Get the business document
                business_doc = frappe.get_doc("Business", business)

                # Get current partnership institutions for this business
                current_institutions = [
                    pi.educational_institution for pi in (business_doc.partnership_institution or [])
                ]

                # Add the current institution if not already present
                if current_institution_name not in current_institutions:
                    business_doc.append(
                        "partnership_institution", {"educational_institution": current_institution_name}
                    )

                # Remove any institutions that are no longer in the business's partnerships
                institutions_to_keep = businesses_to_institutions.get(business, [])
                if current_institution_name not in institutions_to_keep:
                    institutions_to_keep.append(current_institution_name)

                # Filter partnership_institution to keep only valid ones
                business_doc.partnership_institution = [
                    pi
                    for pi in (business_doc.partnership_institution or [])
                    if pi.educational_institution in institutions_to_keep
                    and frappe.db.exists("Educational Institution", pi.educational_institution)
                ]

                # Save the business document
                business_doc.save(ignore_permissions=True)

            except Exception as e:
                frappe.log_error(f"Error syncing business {business}: {e!s}")
                continue

        # Handle removed businesses - remove current institution from their partnership_institution
        for removed_business in removed_businesses:
            if not frappe.db.exists("Business", removed_business):
                continue

            try:
                # Get the business document
                business_doc = frappe.get_doc("Business", removed_business)

                # Remove the current institution from partnership_institution
                business_doc.partnership_institution = [
                    pi
                    for pi in (business_doc.partnership_institution or [])
                    if pi.educational_institution != current_institution_name
                ]

                # Save the business document
                business_doc.save(ignore_permissions=True)

            except Exception as e:
                frappe.log_error(f"Error removing institution from business {removed_business}: {e!s}")
                continue

    except Exception as e:
        frappe.log_error(f"Error in _sync_educational_institution_partnerships: {e!s}")
        raise


def cleanup_orphaned_partnerships():
    """
    Utility function to clean up orphaned partnership records.
    This can be called periodically to maintain data integrity.
    """
    try:
        # Clean up Partnership Institution records with non-existent businesses
        orphaned_pi = frappe.db.sql(
            """
            SELECT pi.name, pi.parent, pi.educational_institution
            FROM `tabPartnership Institution` pi
            LEFT JOIN `tabBusiness` b ON pi.parent = b.name
            WHERE b.name IS NULL
        """,
            as_dict=True,
        )

        for record in orphaned_pi:
            frappe.delete_doc("Partnership Institution", record.name, ignore_permissions=True)
            frappe.log_error(f"Deleted orphaned Partnership Institution: {record.name}")

        # Clean up Partnership Business records with non-existent educational institutions
        orphaned_pb = frappe.db.sql(
            """
            SELECT pb.name, pb.parent, pb.business
            FROM `tabPartnership Business` pb
            LEFT JOIN `tabEducational Institution` ei ON pb.parent = ei.name
            WHERE ei.name IS NULL
        """,
            as_dict=True,
        )

        for record in orphaned_pb:
            frappe.delete_doc("Partnership Business", record.name, ignore_permissions=True)
            frappe.log_error(f"Deleted orphaned Partnership Business: {record.name}")

        # Clean up Partnership Institution records with non-existent educational institutions
        invalid_pi = frappe.db.sql(
            """
            SELECT pi.name, pi.educational_institution
            FROM `tabPartnership Institution` pi
            LEFT JOIN `tabEducational Institution` ei ON pi.educational_institution = ei.name
            WHERE ei.name IS NULL
        """,
            as_dict=True,
        )

        for record in invalid_pi:
            frappe.delete_doc("Partnership Institution", record.name, ignore_permissions=True)
            frappe.log_error(f"Deleted invalid Partnership Institution: {record.name}")

        # Clean up Partnership Business records with non-existent businesses
        invalid_pb = frappe.db.sql(
            """
            SELECT pb.name, pb.business
            FROM `tabPartnership Business` pb
            LEFT JOIN `tabBusiness` b ON pb.business = b.name
            WHERE b.name IS NULL
        """,
            as_dict=True,
        )

        for record in invalid_pb:
            frappe.delete_doc("Partnership Business", record.name, ignore_permissions=True)
            frappe.log_error(f"Deleted invalid Partnership Business: {record.name}")

        frappe.db.commit()

    except Exception as e:
        frappe.log_error(f"Error in cleanup_orphaned_partnerships: {e!s}")
        frappe.db.rollback()


@frappe.whitelist()
def validate_partnership_integrity():
    """
    Validates the integrity of all partnership relationships.
    Returns a report of any inconsistencies found.
    """
    issues = []

    try:
        # Check for Partnership Institutions without corresponding Partnership Business
        pi_without_pb = frappe.db.sql(
            """
            SELECT
                pi.parent as business_name,
                pi.educational_institution,
                'Missing Partnership Business' as issue_type
            FROM `tabPartnership Institution` pi
            WHERE NOT EXISTS (
                SELECT 1 FROM `tabPartnership Business` pb
                WHERE pb.business = pi.parent
                AND pb.parent = pi.educational_institution
            )
        """,
            as_dict=True,
        )

        issues.extend(pi_without_pb)

        # Check for Partnership Business without corresponding Partnership Institution
        pb_without_pi = frappe.db.sql(
            """
            SELECT
                pb.business as business_name,
                pb.parent as educational_institution,
                'Missing Partnership Institution' as issue_type
            FROM `tabPartnership Business` pb
            WHERE NOT EXISTS (
                SELECT 1 FROM `tabPartnership Institution` pi
                WHERE pi.educational_institution = pb.parent
                AND pi.parent = pb.business
            )
        """,
            as_dict=True,
        )

        issues.extend(pb_without_pi)

        # Check for orphaned Partnership Institution records
        orphaned_pi = frappe.db.sql(
            """
            SELECT
                pi.name,
                pi.parent as business_name,
                pi.educational_institution,
                'Orphaned Partnership Institution (Business does not exist)' as issue_type
            FROM `tabPartnership Institution` pi
            LEFT JOIN `tabBusiness` b ON pi.parent = b.name
            WHERE b.name IS NULL
        """,
            as_dict=True,
        )

        issues.extend(orphaned_pi)

        # Check for orphaned Partnership Business records
        orphaned_pb = frappe.db.sql(
            """
            SELECT
                pb.name,
                pb.parent as educational_institution,
                pb.business as business_name,
                'Orphaned Partnership Business (Educational Institution does not exist)' as issue_type
            FROM `tabPartnership Business` pb
            LEFT JOIN `tabEducational Institution` ei ON pb.parent = ei.name
            WHERE ei.name IS NULL
        """,
            as_dict=True,
        )

        issues.extend(orphaned_pb)

        return {"status": "success", "total_issues": len(issues), "issues": issues}

    except Exception as e:
        frappe.log_error(f"Error in validate_partnership_integrity: {e!s}")
        return {"status": "error", "message": f"Error validating partnership integrity: {e!s}"}


@frappe.whitelist()
def fix_partnership_integrity():
    """
    Automatically fixes partnership integrity issues by:
    1. Creating missing bidirectional partnerships
    2. Cleaning up orphaned records
    """
    try:
        # Get all businesses and their partnership institutions
        businesses = frappe.db.get_all("Business", fields=["name"], order_by="name")

        for business in businesses:
            try:
                business_doc = frappe.get_doc("Business", business.name)
                if hasattr(business_doc, "partnership_institution") and business_doc.partnership_institution:
                    partnerships_data = [
                        {"educational_institution": pi.educational_institution, "parent": business.name}
                        for pi in business_doc.partnership_institution
                    ]
                    _sync_business_partnerships(partnerships_data)
            except Exception as e:
                frappe.log_error(f"Error fixing business {business.name}: {e!s}")
                continue

        # Get all educational institutions and their partnership businesses
        institutions = frappe.db.get_all("Educational Institution", fields=["name"], order_by="name")

        for institution in institutions:
            try:
                institution_doc = frappe.get_doc("Educational Institution", institution.name)
                if hasattr(institution_doc, "partnership_business") and institution_doc.partnership_business:
                    partnerships_data = [
                        {"business": pb.business, "parent": institution.name}
                        for pb in institution_doc.partnership_business
                    ]
                    _sync_educational_institution_partnerships(partnerships_data)
            except Exception as e:
                frappe.log_error(f"Error fixing institution {institution.name}: {e!s}")
                continue

        # Clean up orphaned records
        cleanup_orphaned_partnerships()

        return {"status": "success", "message": "Partnership integrity has been fixed successfully"}

    except Exception as e:
        frappe.log_error(f"Error in fix_partnership_integrity: {e!s}")
        return {"status": "error", "message": f"Error fixing partnership integrity: {e!s}"}
