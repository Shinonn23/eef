# Copyright (c) 2025, Siwat Sroisuwan and contributors
# For license information, please see license.txt

# import frappe
from frappe.model.document import Document


class Meetings(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from frappe.types import DF

		chairperson: DF.Link | None
		location: DF.Data | None
		meeting_date: DF.Date | None
		next_meeting_date: DF.Date | None
		notes: DF.Text | None
		secretary: DF.Link | None
		title: DF.Data
	# end: auto-generated types

	pass
