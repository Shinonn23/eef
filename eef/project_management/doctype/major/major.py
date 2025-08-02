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

		approved_scholarship_amount: DF.Data | None
		desired_job_title: DF.Data | None
		institution_confirmed_students: DF.Data | None
		name1: DF.Data
		project: DF.Link
		screened_and_allocated_amount: DF.Data | None
	# end: auto-generated types
	pass
