# Copyright (c) 2025, Siwat Sroisuwan and contributors
# For license information, please see license.txt

# import frappe
from frappe.model.document import Document


class ActivityRecord(Document):
    # begin: auto-generated types
    # This code is auto-generated. Do not modify anything in this block.

    from typing import TYPE_CHECKING

    if TYPE_CHECKING:
        from frappe.types import DF

        from eef.eef.doctype.personnel_child_table.personnel_child_table import PersonnelChildTable

        amended_from: DF.Link | None
        attendees: DF.Table[PersonnelChildTable]
        date: DF.Date | None
        description: DF.LongText | None
        location: DF.Data | None
        objective: DF.SmallText | None
        outcome: DF.SmallText | None
        output: DF.SmallText | None
        person_in_charge: DF.Link | None
        student_batch: DF.Literal["2568", "2569", "2570", "2571"]
        subject: DF.Data | None
        summary: DF.LongText | None
    # end: auto-generated types

    pass

    def autoname(self):
        """Set naming series before saving the document."""
        if not self.name:
            from frappe.model.naming import make_autoname

            self.name = f"AR-{self.subject}-{self.student_batch}-{make_autoname('.####')}"
