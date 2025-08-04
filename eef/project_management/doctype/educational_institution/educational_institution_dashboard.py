from frappe import _


def get_data():
    return {
        "heatmap": True,
        "heatmap_message": _(
            "This is based on the partnership businesses related to this educational institution"
        ),
        "fieldname": "educational_institution",
        "internal_links": {
            "Business": ["partnership_institution", "educational_institution"],
        },
        "transactions": [
            {
                "label": _("Static Information"),
                "items": ["Major"],
            },
            {
                "label": _("Partnership"),
                "items": ["Business"],
            },
        ],
    }
