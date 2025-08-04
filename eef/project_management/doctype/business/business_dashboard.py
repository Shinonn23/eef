from frappe import _


def get_data():
    return {
        "heatmap": True,
        "heatmap_message": _(
            "This is based on the partnership institutions related to this business"
        ),
        "fieldname": "business",
        "internal_links": {
            "Educational Institution": ["partnership_business", "business"],
        },
        "transactions": [
            {
                "label": _("Partnership"),
                "items": ["Educational Institution"],
            },
        ],
    }
