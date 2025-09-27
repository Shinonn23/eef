# Copyright (c) 2025, Siwat Sroisuwan and contributors
# For license information, please see license.txt

# import frappe
from frappe.model.document import Document


class Discussions(Document):
    # begin: auto-generated types
    # This code is auto-generated. Do not modify anything in this block.

    from typing import TYPE_CHECKING

    if TYPE_CHECKING:
        from frappe.types import DF

        agenda: DF.Link | None
        discussion: DF.Text | None
        meeting: DF.Data | None
        participants: DF.Link | None
    # end: auto-generated types

    pass
