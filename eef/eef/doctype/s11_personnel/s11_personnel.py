# Copyright (c) 2025, Siwat Sroisuwan and contributors
# For license information, please see license.txt

# import frappe
from datetime import datetime
from typing import cast

import frappe
from frappe.model.document import Document


class S11Personnel(Document):
    # begin: auto-generated types
    # This code is auto-generated. Do not modify anything in this block.

    from typing import TYPE_CHECKING

    if TYPE_CHECKING:
        from frappe.types import DF

        access_to_information_and_services: DF.Rating
        accommodation: DF.Rating
        addiction: DF.Rating
        comment_adaptation: DF.SmallText | None
        comment_living_conditions: DF.SmallText | None
        comment_mental_emotion: DF.SmallText | None
        comment_other_suggestions: DF.SmallText | None
        comment_problems: DF.SmallText | None
        counseling_access: DF.Rating
        depression: DF.Rating
        emotion_management: DF.Rating
        family_problems: DF.Rating
        financial_management: DF.Rating
        food_and_dining: DF.Rating
        full_name: DF.Link | None
        institute: DF.Link | None
        legal_issues: DF.Rating
        major: DF.Link | None
        new_environment_adaptation: DF.Rating
        personal_health: DF.Rating
        physical_wellbeing: DF.Rating
        relationship_problems: DF.Rating
        social_relation: DF.Rating
        stress_or_anxiety: DF.Rating
        study_problems: DF.Rating
        supporting_the_times: DF.Int
        time_management: DF.Rating
        transportation: DF.Rating
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
