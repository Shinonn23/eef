# Copyright (c) 2025, Siwat Sroisuwan and contributors
# For license information, please see license.txt

# import frappe
from frappe.model.document import Document


class Action(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from frappe.types import DF

		agenda: DF.Link | None
		assigned_to: DF.Link | None
		eadline: DF.Date | None
		meeting: DF.Data | None
		progress_notes: DF.Text | None
		status: DF.Literal["not started", "in progress", "completed", "delayed"] # type: ignore
		task: DF.Text | None
	# end: auto-generated types

	pass
