# Copyright (c) 2025, Siwat Sroisuwan and contributors
# For license information, please see license.txt

# import frappe
from datetime import datetime

from frappe.model.document import Document


class S12Personnel(Document):
    # begin: auto-generated types
    # This code is auto-generated. Do not modify anything in this block.

    from typing import TYPE_CHECKING

    if TYPE_CHECKING:
        from frappe.types import DF

        creativity: DF.Rating
        full_name: DF.Link | None
        full_name_manual: DF.Data | None
        honesty: DF.Rating
        institute: DF.Link | None
        intercultural_communication: DF.Rating
        leadership: DF.Rating
        learning_analytical_thinking: DF.Rating
        lifelong_learning: DF.Rating
        major: DF.Link | None
        no_name_in_system: DF.Check
        presentation_communication: DF.Rating
        professional_ethics: DF.Rating
        self_management: DF.Rating
        social_responsibility: DF.Rating
        supporting_the_times: DF.Int
        teamwork: DF.Rating
        technology_learning: DF.Rating
    # end: auto-generated types

    def autoname(self) -> None:
        """
        สร้างชื่อ Document อัตโนมัติ
        """
        now_str = datetime.now().strftime("%Y%m%d_%H%M")
        name = self.full_name or self.full_name_manual or None
        if name:
            name_formatted = name.strip().replace(" ", "_")
            self.name = f"{name_formatted}-{now_str}"
        else:
            # กรณีที่ข้อมูลยังไม่ครบ ให้ใช้ชื่อชั่วคราวหรือปล่อยให้ระบบจัดการ
            # ในที่นี้จะปล่อยให้ใช้ default naming (hash) ไปก่อน
            self.name = None
