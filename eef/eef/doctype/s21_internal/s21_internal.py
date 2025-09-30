# Copyright (c) 2025, Siwat Sroisuwan and contributors
# For license information, please see license.txt

from datetime import datetime
from typing import cast

import frappe
from frappe.model.document import Document


class S21Internal(Document):
    # begin: auto-generated types
    # This code is auto-generated. Do not modify anything in this block.

    from typing import TYPE_CHECKING

    if TYPE_CHECKING:
        from eef.eef.doctype.major_item.major_item import MajorItem
        from frappe.types import DF

        adequacy_personnel: DF.SmallText | None
        availability_learning_media: DF.SmallText | None
        course_design: DF.SmallText | None
        curriculum_consistency: DF.SmallText | None
        curriculum_development_process: DF.SmallText | None
        employment: DF.SmallText | None
        graduate_skill: DF.SmallText | None
        institute: DF.Link
        instructor_development: DF.SmallText | None
        learning_design: DF.SmallText | None
        learning_environment: DF.SmallText | None
        learning_evaluation: DF.SmallText | None
        learning_method: DF.SmallText | None
        major: DF.TableMultiSelect[MajorItem]
        student_academic_achievement: DF.SmallText | None
        supporting_the_times: DF.Int
    # end: auto-generated types

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
