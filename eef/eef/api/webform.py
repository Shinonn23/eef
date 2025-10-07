import frappe


@frappe.whitelist(allow_guest=True)
def get_students_and_major_by_institute():
    institute = frappe.form_dict.get("institute")
    if not institute:
        frappe.throw("Argument 'institute' is required.")
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


@frappe.whitelist(allow_guest=True)
def get_personnel_and_major_by_institute():
    institute = frappe.form_dict.get("institute")
    if not institute:
        frappe.throw("Argument 'institute' is required.")
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
