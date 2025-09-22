# Copyright (c) 2025, Siwat Sroisuwan and contributors
# For license information, please see license.txt

# import frappe
from frappe.model.document import Document
from datetime import datetime


class CurriculumDevelopment(Document):
    # begin: auto-generated types
    # This code is auto-generated. Do not modify anything in this block.

    from typing import TYPE_CHECKING

    if TYPE_CHECKING:
        from frappe.types import DF

        adequacy_personnel: DF.SmallText | None
        availability_learning_media: DF.SmallText | None
        course_design: DF.SmallText | None
        curriculum_consistency: DF.SmallText | None
        curriculum_development_process: DF.SmallText | None
        employment: DF.SmallText | None
        full_name: DF.Link | None
        graduate_skill: DF.SmallText | None
        institute: DF.Link | None
        instructor_development: DF.SmallText | None
        learning_design: DF.SmallText | None
        learning_environment: DF.SmallText | None
        learning_evaluation: DF.SmallText | None
        learning_method: DF.SmallText | None
        major: DF.Link | None
        student_academic_achievement: DF.SmallText | None
        supporting_the_times: DF.Int
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
