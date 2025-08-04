# Copyright (c) 2025, Siwat Sroisuwan and contributors
# For license information, please see license.txt

# import frappe
from frappe.model.document import Document

from eef.utils.sync import cleanup_orphaned_partnerships


class EducationalInstitution(Document):
    # begin: auto-generated types
    # This code is auto-generated. Do not modify anything in this block.

    from typing import TYPE_CHECKING

    if TYPE_CHECKING:
        from frappe.types import DF

        from eef.project_management.doctype.partnership_business.partnership_business import (
            PartnershipBusiness,
        )

        district: DF.Literal[None]
        name1: DF.Data | None
        partnership_business: DF.TableMultiSelect[PartnershipBusiness]
        postal_code: DF.Data | None
        province: DF.Literal[None]
        subdistrict: DF.Literal[None]
    # end: auto-generated types
    def after_save(self) -> None:
        """
        Validate the Business document.
        This method is called after saving the document.
        """
        pass
        # cleanup_orphaned_partnerships()
