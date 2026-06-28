# Copyright (c) 2025, Siwat Sroisuwan and contributors
# For license information, please see license.txt

from datetime import datetime

# import frappe
from frappe.model.document import Document


class PersonnelWellbeing(Document):
    # end: auto-generated types

    def autoname(self) -> None:
        """
        สร้างชื่อ Document อัตโนมัติ
        """
        now_str = datetime.now().strftime("%Y%m%d_%H%M")
        name = getattr(self, "full_name", None)
        if name:
            name_formatted = name.strip().replace(" ", "_")
            self.name = f"{name_formatted}-{now_str}"
        else:
            # กรณีที่ข้อมูลยังไม่ครบ ให้ใช้ชื่อชั่วคราวหรือปล่อยให้ระบบจัดการ
            # ในที่นี้จะปล่อยให้ใช้ default naming (hash) ไปก่อน
            self.name = None
