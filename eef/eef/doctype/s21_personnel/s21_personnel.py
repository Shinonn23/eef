# Copyright (c) 2025, Siwat Sroisuwan and contributors
# For license information, please see license.txt

# import frappe
from datetime import datetime

from frappe.model.document import Document


class S21Personnel(Document):
    # begin: auto-generated types
    # This code is auto-generated. Do not modify anything in this block.

    from typing import TYPE_CHECKING

    if TYPE_CHECKING:
        from frappe.types import DF

        additional_suggestions: DF.SmallText | None
        adequacy_personnel: DF.Rating
        availability_learning_media: DF.Rating
        check_data_confirmation: DF.Check
        comment_monitoring_curriculum: DF.SmallText | None
        comment_monitoring_graduates: DF.SmallText | None
        comment_monitoring_resources: DF.SmallText | None
        comment_monitoring_teaching: DF.SmallText | None
        course_design: DF.Rating
        curriculum_consistency: DF.Rating
        curriculum_development_process: DF.Rating
        employment: DF.Rating
        full_name: DF.Link | None
        full_name_manual: DF.Data | None
        graduate_skill: DF.Rating
        institute: DF.Link
        instructor_development: DF.Rating
        learning_design: DF.Rating
        learning_environment: DF.Rating
        learning_evaluation: DF.Rating
        learning_method: DF.Rating
        major1: DF.Link | None
        major2: DF.Link | None
        no_name_in_system: DF.Check
        student_academic_achievement: DF.Rating
        student_batch: DF.Literal["2566", "2567", "2568", "2569", "2570", "2571"]
        supporting_the_times: DF.Int
    # end: auto-generated types

    pass

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
