# Copyright (c) 2025, Siwat Sroisuwan and contributors
# For license information, please see license.txt

# import frappe
from frappe.model.document import Document


class Major(Document):
    # begin: auto-generated types
    # This code is auto-generated. Do not modify anything in this block.

    from typing import TYPE_CHECKING

    if TYPE_CHECKING:
        from frappe.types import DF

        educational_institution: DF.Link
        name1: DF.Data
    # end: auto-generated types

    def autoname(self) -> None:
        """
        Automatically sets the name of the Major document to the educational institution's name.
        """
        x = self.educational_institution.split(" ")
        edu_name = f"{x[0]}{x[1]}" if len(x) > 1 else x[0][:2]
        self.name = f"{self.name1} - {edu_name.upper()}".strip()
