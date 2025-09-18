# Copyright (c) 2025, Siwat Sroisuwan and contributors
# For license information, please see license.txt

# import frappe
from frappe.model.document import Document


class Students(Document):
    # begin: auto-generated types
    # This code is auto-generated. Do not modify anything in this block.

    from typing import TYPE_CHECKING

    if TYPE_CHECKING:
        from frappe.types import DF

        age: DF.Int
        campus_province: DF.Literal[None]
        first_name: DF.Data | None
        full_name: DF.Data | None
        gender: DF.Literal["\u0e44\u0e21\u0e48\u0e23\u0e30\u0e1a\u0e38", "\u0e0a\u0e32\u0e22", "\u0e2b\u0e0d\u0e34\u0e07"]
        institute: DF.Link | None
        last_name: DF.Data | None
        major: DF.Link | None
        student_id: DF.Data | None
    # end: auto-generated types

    pass

    def autoname(self) -> None:
        self.full_name = f"{self.first_name} {self.last_name}"
