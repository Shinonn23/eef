# Copyright (c) 2025, Siwat Sroisuwan and contributors
# For license information, please see license.txt

from datetime import datetime
from typing import cast

import frappe
from frappe.model.document import Document


class RiskInternal(Document):
    # begin: auto-generated types
    # This code is auto-generated. Do not modify anything in this block.

    from typing import TYPE_CHECKING

    if TYPE_CHECKING:
        from frappe.types import DF

        from eef.eef.doctype.major_item.major_item import MajorItem

        amended_from: DF.Link | None
        institute: DF.Link
        major: DF.TableMultiSelect[MajorItem]
        risk_details_text: DF.LongText | None
        student_batch: DF.Literal["2566", "2567", "2568", "2569", "2570", "2571"]
        supporting_the_times: DF.Int
    # end: auto-generated types

    pass

    def autoname(self) -> None:
        """
        สร้างชื่อ Document อัตโนมัติโดยใช้ชื่อผู้สร้าง (owner) + timestamp
        """
        from frappe.core.doctype.user.user import User

        now_str: str = datetime.now().strftime("%Y%m%d_%H%M")

        try:
            # ดึง User DocType ของ owner
            user_doc = cast(User, frappe.get_doc("User", self.owner))
            owner_name: str = cast(str, user_doc.full_name) or self.owner
        except Exception:
            owner_name: str = self.owner

        # แปลงชื่อเป็น format-friendly
        name_formatted: str = owner_name.strip().replace(" ", "_")
        self.name = f"{name_formatted}-{now_str}"
