# Copyright (c) 2025, Siwat Sroisuwan and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class Business(Document):
    # begin: auto-generated types
    # This code is auto-generated. Do not modify anything in this block.

    from typing import TYPE_CHECKING

    if TYPE_CHECKING:
        from eef.project_management.doctype.business_major_interest.business_major_interest import (
            BusinessMajorInterest,
        )
        from eef.project_management.doctype.partnership_institution.partnership_institution import (
            PartnershipInstitution,
        )
        from frappe.types import DF

        business_major_interest: DF.Table[BusinessMajorInterest]
        district: DF.Literal[None]
        name1: DF.Data | None
        partnership_institution: DF.TableMultiSelect[PartnershipInstitution]
        postal_code: DF.Data | None
        province: DF.Literal[None]
        subdistrict: DF.Literal[None]

    # end: auto-generated types

    @frappe.whitelist()
    def has_partnership_institutions(self) -> bool:
        """
        Returns True if the business has any partnership institutions, else False.
        """
        if not self.name:
            return False
        business = frappe.get_doc("Business", self.name)
        return bool(business.partnership_institution and len(business.partnership_institution) > 0) # type: ignore


@frappe.whitelist()
def get_major_query(doctype: str, txt, searchfield, start, page_len, filters):
    """Returns a list of majors associated with the business's partnership institutions."""
    business_name = filters.get("business_name")

    if not business_name:
        return []

    business = frappe.get_doc("Business", business_name)
    institution_names = [
        d.educational_institution for d in business.partnership_institution
    ]

    major = []
    for institution_name in institution_names:
        # สร้าง base filters
        filters = {"educational_institution": institution_name}

        # เพิ่ม text search filter ถ้ามี txt
        if txt:
            filters["or"] = [
                ["name", "like", f"%{txt}%"],
                ["name1", "like", f"%{txt}%"],
            ]

        majors = frappe.get_all(
            doctype,
            filters=filters,
            fields=["name", "name1"],
        )
        # คืนค่า name (hash) และ name1 (description)
        major.extend([[d.name, d.name1] for d in majors])
    return major
