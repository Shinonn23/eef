# Copyright (c) 2025, Siwat Sroisuwan and contributors
# For license information, please see license.txt

# import frappe
from frappe.model.document import Document


class S21Personnel(Document):
    # begin: auto-generated types
    # This code is auto-generated. Do not modify anything in this block.

    from typing import TYPE_CHECKING

    if TYPE_CHECKING:
        from frappe.types import DF

        additional_suggestions: DF.SmallText | None
        adequacy_personnel: DF.Rating
        availability_learning_media: DF.Rating
        check_data_confirmation: DF.Check
        comment_monitoring_curriculum: DF.SmallText | None
        comment_monitoring_graduates: DF.SmallText | None
        comment_monitoring_resources: DF.SmallText | None
        comment_monitoring_teaching: DF.SmallText | None
        course_design: DF.Rating
        curriculum_consistency: DF.Rating
        curriculum_development_process: DF.Rating
        employment: DF.Rating
        full_name: DF.Link
        full_name_manual: DF.Data | None
        graduate_skill: DF.Rating
        institute: DF.Link
        instructor_development: DF.Rating
        learning_design: DF.Rating
        learning_environment: DF.Rating
        learning_evaluation: DF.Rating
        learning_method: DF.Rating
        major1: DF.Link | None
        major2: DF.Link | None
        no_name_in_system: DF.Check
        student_academic_achievement: DF.Rating
        supporting_the_times: DF.Int
    # end: auto-generated types

    pass
