# Copyright (c) 2025, Siwat Sroisuwan and contributors
# For license information, please see license.txt

# import frappe
from datetime import datetime

from frappe.model.document import Document


class S11Personnel(Document):
    # begin: auto-generated types
    # This code is auto-generated. Do not modify anything in this block.

    from typing import TYPE_CHECKING

    if TYPE_CHECKING:
        from frappe.types import DF

        academic_stress: DF.Rating
        accommodation_condition: DF.Rating
        accommodation_safety: DF.Rating
        adapt_academic: DF.Rating
        adapt_social: DF.Rating
        adaptation_stress: DF.Rating
        addiction: DF.Rating
        amenities_access: DF.Rating
        check_data_confirmation: DF.Check
        college_activity: DF.Rating
        commute_access: DF.Rating
        coping_skill: DF.Rating
        debt_level: DF.Literal[
            "\u0e44\u0e21\u0e48\u0e21\u0e35\u0e2b\u0e19\u0e35\u0e49",
            "\u0e19\u0e49\u0e2d\u0e22\u0e01\u0e27\u0e48\u0e32 5000 \u0e1a\u0e32\u0e17",  # type: ignore
            "5000\u201320000 \u0e1a\u0e32\u0e17",  # type: ignore
            "\u0e21\u0e32\u0e01\u0e01\u0e27\u0e48\u0e32 20000 \u0e1a\u0e32\u0e17",  # type: ignore
            "\u0e44\u0e21\u0e48\u0e23\u0e30\u0e1a\u0e38",
        ]
        exercise_facility_access: DF.Rating
        expense_manage: DF.Rating
        family_problems: DF.Rating
        food_availability: DF.Rating
        food_cleanliness: DF.Rating
        food_price_appropriateness: DF.Rating
        full_name: DF.Link | None
        full_name_manual: DF.Data | None
        institute: DF.Link | None
        legal_issues: DF.Rating
        major: DF.Link | None
        medical_facility_access: DF.Rating
        mental_health_promo: DF.Rating
        monthly_saving: DF.Literal[
            "0-500 \u0e1a\u0e32\u0e17",  # type: ignore
            "500-1000 \u0e1a\u0e32\u0e17",  # type: ignore
            "1000-2000 \u0e1a\u0e32\u0e17",  # type: ignore
            "\u0e21\u0e32\u0e01\u0e01\u0e27\u0e48\u0e32 2000 \u0e1a\u0e32\u0e17",  # type: ignore
        ]
        no_name_in_system: DF.Check
        personal_health_status: DF.Literal[
            "\u0e2a\u0e38\u0e02\u0e20\u0e32\u0e1e\u0e44\u0e21\u0e48\u0e14\u0e35",
            "\u0e2a\u0e38\u0e02\u0e20\u0e32\u0e1e\u0e04\u0e48\u0e2d\u0e19\u0e02\u0e49\u0e32\u0e07\u0e14\u0e35",
            "\u0e2a\u0e38\u0e02\u0e20\u0e32\u0e1e\u0e14\u0e35",
            "\u0e2a\u0e38\u0e02\u0e20\u0e32\u0e1e\u0e14\u0e35\u0e21\u0e32\u0e01",
        ]
        personal_stress: DF.Rating
        relationship_problems: DF.Rating
        service_access: DF.Rating
        student_id: DF.Data | None
        study_problems: DF.Rating
        support_additional_needs: DF.SmallText | None
        support_college_access: DF.Rating
        support_family_level: DF.Rating
        support_peer_level: DF.Rating
        support_suggestions: DF.SmallText | None
        supporting_the_times: DF.Int
        time_manage: DF.Rating
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
