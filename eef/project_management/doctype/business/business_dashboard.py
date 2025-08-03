from frappe import _


def get_data():
    return {
        "heatmap": True,
        "heatmap_message": _(
            "This is based on the partnership institutions related to this business"
        ),
        "internal_links": {
            "Educational Institution": ["partnership_institution", "educational_institution"],
        },
        "transactions": [
            {
                "label": _("Partnership Institution"),
                "items": ["Educational Institution"],
            },
        ],
    }
