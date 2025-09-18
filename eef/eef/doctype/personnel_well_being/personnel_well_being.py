# Copyright (c) 2025, Siwat Sroisuwan and contributors
# For license information, please see license.txt

# import frappe
from frappe.model.document import Document


class PersonnelWellbeing(Document):
    
    
    def autoname(self) -> None:
        """
        สร้างชื่อ Document อัตโนมัติจาก รหัสนักเรียน และ ครั้งที่หนุนเสริม
        """
        # ตรวจสอบว่ามีข้อมูลที่จำเป็นครบถ้วนหรือไม่
        if self.full_name and self.supporting_the_times:
            # กำหนดชื่อ (name) ของ Document ด้วย f-string
            self.name = f"{self.full_name}-{self.supporting_the_times}"
        else:
            # กรณีที่ข้อมูลยังไม่ครบ ให้ใช้ชื่อชั่วคราวหรือปล่อยให้ระบบจัดการ
            # ในที่นี้จะปล่อยให้ใช้ default naming (hash) ไปก่อน
            self.name = None


