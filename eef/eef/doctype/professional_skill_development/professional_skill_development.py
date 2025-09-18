# Copyright (c) 2025, Siwat Sroisuwan and contributors
# For license information, please see license.txt

# import frappe
from frappe.model.document import Document


class ProfessionalSkillDevelopment(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from frappe.types import DF

		campus_province: DF.Literal[None]
		creativity: DF.SmallText | None
		full_name: DF.Link | None
		honesty: DF.SmallText | None
		institute: DF.Link | None
		intercultural_communication: DF.SmallText | None
		leadership: DF.SmallText | None
		learning_analytical_thinking: DF.SmallText | None
		lifelong_learning: DF.SmallText | None
		major: DF.Link | None
		presentation_communication: DF.SmallText | None
		professional_ethics: DF.SmallText | None
		self_management: DF.SmallText | None
		social_responsibility: DF.SmallText | None
		supporting_the_times: DF.Int
		teamwork: DF.SmallText | None
		technology_learning: DF.SmallText | None
	# end: auto-generated types

	pass
