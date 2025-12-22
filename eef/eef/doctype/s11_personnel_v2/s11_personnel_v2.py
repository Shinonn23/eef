# Copyright (c) 2025, Siwat Sroisuwan and contributors
# For license information, please see license.txt

# import frappe
from datetime import datetime

from frappe.model.document import Document


class S11PersonnelV2(Document):
    # begin: auto-generated types
    # This code is auto-generated. Do not modify anything in this block.

    from typing import TYPE_CHECKING

    if TYPE_CHECKING:
        from frappe.types import DF

        access_to_information_and_services: DF.Rating
        accommodation: DF.Rating
        addiction: DF.Rating
        additional_suggestions: DF.SmallText | None
        check_data_confirmation: DF.Check
        comment_college_adaptation: DF.SmallText | None
        comment_living_conditions: DF.SmallText | None
        comment_mental: DF.SmallText | None
        comment_problems: DF.SmallText | None
        counseling_access: DF.Rating
        depression: DF.Rating
        emotion_management: DF.Rating
        family_problems: DF.Rating
        financial_management: DF.Rating
        food_and_dining: DF.Rating
        full_name: DF.Link | None
        full_name_manual: DF.Data | None
        institute: DF.Link
        legal_issues: DF.Rating
        major1: DF.Link | None
        major2: DF.Link | None
        new_environment_adaptation: DF.Rating
        no_name_in_system: DF.Check
        personal_health: DF.Rating
        physical_wellbeing: DF.Rating
        relationship_problems: DF.Rating
        social_relation: DF.Rating
        stress_or_anxiety: DF.Rating
        student_batch: DF.Literal["2566", "2567", "2568", "2569", "2570", "2571"]
        study_problems: DF.Rating
        supporting_the_times: DF.Int
        time_management: DF.Rating
        transportation: DF.Rating
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
