# Copyright (c) 2025, Siwat Sroisuwan and contributors
# For license information, please see license.txt

# import frappe
from frappe.model.document import Document


class MeetingParticipants(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from frappe.types import DF

		attendance_status: DF.Literal["present", "absent", "late", "leave_early"]
		parent: DF.Data
		parentfield: DF.Data
		parenttype: DF.Data
		participant: DF.Link | None
		role: DF.Literal["chairperson", "secretary", "attendee"]
	# end: auto-generated types

	pass
