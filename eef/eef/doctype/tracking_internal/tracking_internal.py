# Copyright (c) 2025, Siwat Sroisuwan and contributors
# For license information, please see license.txt

from datetime import datetime
from typing import cast

import frappe
from frappe.model.document import Document


class TrackingInternal(Document):
    # begin: auto-generated types
    # This code is auto-generated. Do not modify anything in this block.

    from typing import TYPE_CHECKING

    if TYPE_CHECKING:
        from eef.eef.doctype.tracking_internal_items.tracking_internal_items import TrackingInternalItems
        from frappe.types import DF

        amended_from: DF.Link | None
        date_tracking: DF.Date
        general_note: DF.SmallText | None
        institute: DF.Link
        supporting_the_times: DF.Int
        table_notes: DF.Table[TrackingInternalItems]
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
