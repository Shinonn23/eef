import frappe


def _table_exists(doctype: str) -> bool:
    return bool(frappe.db.table_exists(doctype))


def _drop_table(doctype: str) -> None:
    table = f"tab{doctype}"
    frappe.db.sql_ddl(f"DROP TABLE IF EXISTS `{table}`")


def _drop_doctype_record(name: str) -> None:
    if not frappe.db.exists("DocType", name):
        return

    frappe.delete_doc(
        "DocType",
        name,
        force=True,
        ignore_permissions=True,
        ignore_missing=True,
    )


def _promote_v2_doctype(source: str, target: str) -> None:
    if not frappe.db.exists("DocType", source):
        if _table_exists(source):
            _drop_doctype_record(target)
            _drop_table(target)
            frappe.db.rename_table(source, target)
        _drop_table(source)
        return

    _drop_doctype_record(target)
    _drop_table(target)

    frappe.rename_doc(
        "DocType",
        source,
        target,
        force=True,
        ignore_permissions=True,
        show_alert=False,
        rebuild_search=False,
    )

    if _table_exists(source) and not _table_exists(target):
        frappe.db.rename_table(source, target)

    _drop_table(source)


def _rename_web_form(source: str, target: str, doc_type: str) -> None:
    if frappe.db.exists("Web Form", target):
        frappe.delete_doc(
            "Web Form",
            target,
            force=True,
            ignore_permissions=True,
            ignore_missing=True,
        )

    if frappe.db.exists("Web Form", source):
        frappe.rename_doc(
            "Web Form",
            source,
            target,
            force=True,
            ignore_permissions=True,
            show_alert=False,
            rebuild_search=False,
        )

    if frappe.db.exists("Web Form", target):
        frappe.db.set_value("Web Form", target, {"doc_type": doc_type, "route": target})


def execute() -> None:
    _promote_v2_doctype("S11 Personnel V2", "S11 Personnel")
    _promote_v2_doctype("S11 Internal V2", "S11 Internal")
    _rename_web_form("s11-personnel-v2", "s11-personnel", "S11 Personnel")
