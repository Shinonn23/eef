# Copyright (c) 2025, Siwat Sroisuwan and contributors
# For license information, please see license.txt

# import frappe
from frappe.model.document import Document


class Businesses(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from frappe.types import DF

		district: DF.Literal[None]
		name1: DF.Data | None
		postal_code: DF.Data | None
		project: DF.Link | None
		province: DF.Literal[None]
		subdistrict: DF.Literal[None]
	# end: auto-generated types
    
	pass
