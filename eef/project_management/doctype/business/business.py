# Copyright (c) 2025, Siwat Sroisuwan and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

from eef.utils.sync import cleanup_orphaned_partnerships


class Business(Document):
    # begin: auto-generated types
    # This code is auto-generated. Do not modify anything in this block.

    from typing import TYPE_CHECKING

    if TYPE_CHECKING:
        from frappe.types import DF

        from eef.project_management.doctype.business_major_interest.business_major_interest import (
            BusinessMajorInterest,
        )
        from eef.project_management.doctype.partnership_institution.partnership_institution import (
            PartnershipInstitution,
        )

        business_major_interest: DF.Table[BusinessMajorInterest]
        district: DF.Literal[None]
        name1: DF.Data | None
        partnership_institution: DF.TableMultiSelect[PartnershipInstitution]
        postal_code: DF.Data | None
        province: DF.Literal[None]
        subdistrict: DF.Literal[None]
    # end: auto-generated types

    def after_save(self) -> None:
        """
        Validate the Business document.
        This method is called after saving the document.
        """
        pass
        # cleanup_orphaned_partnerships()

    @frappe.whitelist()
    def has_partnership_institutions(self) -> bool:
        """
        Returns True if the business has any partnership institutions, else False.
        """
        # ถ้า instance ยังไม่ได้บันทึก (is_new) ให้ return False ทันที
        if self.is_new():
            return False

        # กรณี instance ยังไม่ได้บันทึก (local doc)
        if hasattr(self, "partnership_institution") and self.partnership_institution:
            return len(self.partnership_institution) > 0

        if not self.name:
            return False

        business = frappe.get_doc("Business", self.name)
        return bool(
            getattr(business, "partnership_institution", None) and len(business.partnership_institution) > 0
        )


@frappe.whitelist()
def get_major_query(doctype: str, txt, searchfield, start, page_len, filters):
    """Returns a list of majors associated with the business's partnership institutions."""
    business_name = filters.get("business_name")
    existing_majors = filters.get("existing_majors", [])

    if not business_name:
        return []

    business = frappe.get_doc("Business", business_name)
    institution_names = [d.educational_institution for d in business.partnership_institution]

    if not institution_names:
        return []

    # สร้าง filters สำหรับ query
    query_filters = {"educational_institution": ["in", institution_names]}
    
    # เพิ่ม text search filter ถ้ามี txt
    if txt:
        query_filters["name"] = ["like", f"%{txt}%"]

    # ดึงข้อมูล majors
    majors = frappe.get_all(
        doctype,
        filters=query_filters,
        fields=["name", "educational_institution"],
    )

    # กรอง existing majors ออก และ return เฉพาะที่มี name
    result = []
    for major in majors:
        if major.name and major.name not in existing_majors:
            result.append([major.name, major.educational_institution])
    
    return result
