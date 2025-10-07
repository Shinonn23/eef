# Copyright (c) 2025, Siwat Sroisuwan and contributors
# For license information, please see license.txt

# import frappe
from frappe.model.document import Document


class TrackingInternalItems(Document):
    # begin: auto-generated types
    # This code is auto-generated. Do not modify anything in this block.

    from typing import TYPE_CHECKING

    if TYPE_CHECKING:
        from frappe.types import DF

        folllowup_plan: DF.SmallText | None
        followup_topic: DF.SmallText | None
        highlight: DF.SmallText | None
        important_note: DF.SmallText | None
        parent: DF.Data
        parentfield: DF.Data
        parenttype: DF.Data
        problems_obstacles: DF.SmallText | None
        topic: DF.Literal[
            "\u0e14\u0e49\u0e32\u0e19\u0e17\u0e35\u0e48 1: \u0e04\u0e27\u0e32\u0e21\u0e40\u0e1b\u0e47\u0e19\u0e2d\u0e22\u0e39\u0e48",
            "\u0e14\u0e49\u0e32\u0e19\u0e17\u0e35\u0e48 2: \u0e01\u0e32\u0e23\u0e1e\u0e31\u0e12\u0e19\u0e32\u0e2b\u0e25\u0e31\u0e01\u0e2a\u0e39\u0e15\u0e23",
            "\u0e14\u0e49\u0e32\u0e19\u0e17\u0e35\u0e48 3: \u0e01\u0e32\u0e23\u0e21\u0e35\u0e07\u0e32\u0e19\u0e17\u0e33",
            "\u0e14\u0e49\u0e32\u0e19\u0e17\u0e35\u0e48 4: \u0e01\u0e32\u0e23\u0e1a\u0e23\u0e34\u0e2b\u0e32\u0e23\u0e42\u0e04\u0e23\u0e07\u0e01\u0e32\u0e23",
            "\u0e17\u0e35\u0e21\u0e2b\u0e19\u0e38\u0e19\u0e40\u0e2a\u0e23\u0e34\u0e21 \u0e01\u0e2a\u0e28",
        ]
    # end: auto-generated types

    pass
