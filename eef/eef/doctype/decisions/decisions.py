# Copyright (c) 2025, Siwat Sroisuwan and contributors
# For license information, please see license.txt

# import frappe
from frappe.model.document import Document


class Decisions(Document):
    # begin: auto-generated types
    # This code is auto-generated. Do not modify anything in this block.

    from typing import TYPE_CHECKING

    if TYPE_CHECKING:
        from frappe.types import DF

        agenda: DF.Link | None
        decision: DF.Text | None
        meeting: DF.Data | None
        reason: DF.Text | None
        result: DF.Literal["approved", "rejected", "pending"]
    # end: auto-generated types

    pass
