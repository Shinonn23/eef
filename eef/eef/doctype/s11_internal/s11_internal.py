# Copyright (c) 2025, Siwat Sroisuwan and contributors
# For license information, please see license.txt

from datetime import datetime
from typing import cast

import frappe
from frappe.model.document import Document


class S11Internal(Document):
    # begin: auto-generated types
    # This code is auto-generated. Do not modify anything in this block.

    from typing import TYPE_CHECKING

    if TYPE_CHECKING:
        from eef.eef.doctype.major_item.major_item import MajorItem
        from frappe.types import DF

        access_to_information_and_services: DF.SmallText | None
        accommodation: DF.SmallText | None
        addiction: DF.LongText | None
        additional_suggestions: DF.SmallText | None
        counseling_access: DF.SmallText | None
        depression: DF.SmallText | None
        emotion_management: DF.SmallText | None
        family_problems: DF.LongText | None
        financial_management: DF.SmallText | None
        food_and_dining: DF.SmallText | None
        institute: DF.Link | None
        legal_issues: DF.LongText | None
        major: DF.TableMultiSelect[MajorItem]
        new_environment_adaptation: DF.SmallText | None
        personal_health: DF.SmallText | None
        physical_wellbeing: DF.SmallText | None
        relationship_problems: DF.LongText | None
        social_relation: DF.SmallText | None
        stress_or_anxiety: DF.SmallText | None
        study_problems: DF.LongText | None
        supporting_the_times: DF.Int
        time_management: DF.SmallText | None
        transportation: DF.SmallText | None
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
