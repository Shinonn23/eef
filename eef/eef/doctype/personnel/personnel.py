# Copyright (c) 2025, Siwat Sroisuwan and contributors
# For license information, please see license.txt

# import frappe
from frappe.model.document import Document


class Personnel(Document):
    # begin: auto-generated types
    # This code is auto-generated. Do not modify anything in this block.

    from typing import TYPE_CHECKING

    if TYPE_CHECKING:
        from frappe.types import DF

        age: DF.Int
        campus_province: DF.Literal[None]
        email: DF.Data | None
        first_name: DF.Data
        full_name: DF.Data | None
        institute: DF.Link
        last_name: DF.Data
        role: DF.Data | None
        tel: DF.Data | None
        title: DF.Literal[
            "",
            "\u0e19\u0e32\u0e22",
            "\u0e19\u0e32\u0e07\u0e2a\u0e32\u0e27",
            "\u0e19\u0e32\u0e07",
            "\u0e2d.",
            "\u0e14\u0e23.",
            "\u0e2d.\u0e14\u0e23.",
            "\u0e1c\u0e28.\u0e14\u0e23.",
            "\u0e23\u0e28.\u0e14\u0e23.",
            "\u0e28.\u0e14\u0e23.",
        ]
        เพศ: DF.Literal[
            "\u0e44\u0e21\u0e48\u0e23\u0e30\u0e1a\u0e38", "\u0e0a\u0e32\u0e22", "\u0e2b\u0e0d\u0e34\u0e07"
        ]
    # end: auto-generated types

    def autoname(self) -> None:
        self.full_name = f"{self.first_name} {self.last_name}"
