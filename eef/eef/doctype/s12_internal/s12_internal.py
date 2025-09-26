# Copyright (c) 2025, Siwat Sroisuwan and contributors
# For license information, please see license.txt

from datetime import datetime

# import frappe
from frappe.model.document import Document


class S12Internal(Document):
    # begin: auto-generated types
    # This code is auto-generated. Do not modify anything in this block.

    from typing import TYPE_CHECKING

    if TYPE_CHECKING:
        from frappe.types import DF

        creativity: DF.SmallText | None
        full_name: DF.Link | None
        honesty: DF.SmallText | None
        institute: DF.Link | None
        intercultural_communication: DF.SmallText | None
        leadership: DF.SmallText | None
        learning_analytical_thinking: DF.SmallText | None
        lifelong_learning: DF.SmallText | None
        major: DF.Link | None
        presentation_communication: DF.SmallText | None
        professional_ethics: DF.SmallText | None
        self_management: DF.SmallText | None
        social_responsibility: DF.SmallText | None
        supporting_the_times: DF.Int
        teamwork: DF.SmallText | None
        technology_learning: DF.SmallText | None
    # end: auto-generated types

    def autoname(self) -> None:
        """
        สร้างชื่อ Document อัตโนมัติ
        """
        now_str = datetime.now().strftime("%Y%m%d_%H%M")
        name = self.full_name or None
        if name:
            name_formatted = name.strip().replace(" ", "_")
            self.name = f"{name_formatted}-{now_str}"
        else:
            # กรณีที่ข้อมูลยังไม่ครบ ให้ใช้ชื่อชั่วคราวหรือปล่อยให้ระบบจัดการ
            # ในที่นี้จะปล่อยให้ใช้ default naming (hash) ไปก่อน
            self.name = None
