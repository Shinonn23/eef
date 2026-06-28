import frappe
from frappe import _


# Guest access is required because anonymous web forms call this endpoint.
@frappe.whitelist(allow_guest=True)  # nosemgrep
def get_students_and_major_by_institute():
    institute = frappe.form_dict.get("institute")
    if not institute:
        frappe.throw(_("Argument 'institute' is required."))
    students = frappe.db.get_list(
        "Students",
        filters={"institute": institute},
        fields=["name"],
        order_by="name",
    )
    majors = frappe.db.get_list(
        "Major",
        filters={"educational_institution": institute},
        fields=["name", "name1"],  # name1 is the name without abbreviation
        order_by="name",
    )
    return {"students": students, "majors": majors}


# Guest access is required because anonymous web forms call this endpoint.
@frappe.whitelist(allow_guest=True)  # nosemgrep
def get_personnel_and_major_by_institute():
    institute = frappe.form_dict.get("institute")
    if not institute:
        frappe.throw(_("Argument 'institute' is required."))
    personnels = frappe.db.get_list(
        "Personnel",
        filters={"institute": institute},
        fields=["name", "full_name"],
        order_by="name",
    )
    majors = frappe.db.get_list(
        "Major",
        filters={"educational_institution": institute},
        fields=["name", "name1"],  # name1 is the name without abbreviation
        order_by="name",
    )
    return {"personnels": personnels, "majors": majors}
