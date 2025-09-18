# Copyright (c) 2025, Siwat Sroisuwan and contributors
# For license information, please see license.txt

# import frappe
from frappe.model.document import Document


class CurriculumDevelopment(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from frappe.types import DF

		adequacy_personnel: DF.SmallText | None
		availability_learning_media: DF.SmallText | None
		campus_province: DF.Literal[None]
		course_design: DF.SmallText | None
		curriculum_consistency: DF.SmallText | None
		curriculum_development_process: DF.SmallText | None
		employment: DF.SmallText | None
		full_name: DF.Link | None
		graduate_skill: DF.SmallText | None
		institute: DF.Link | None
		instructor_development: DF.SmallText | None
		learning_design: DF.SmallText | None
		learning_environment: DF.SmallText | None
		learning_evaluation: DF.SmallText | None
		learning_method: DF.SmallText | None
		major: DF.Link | None
		student_academic_achievement: DF.SmallText | None
		supporting_the_times: DF.Int
	# end: auto-generated types

	pass
