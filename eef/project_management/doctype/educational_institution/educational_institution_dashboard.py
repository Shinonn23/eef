from frappe import _


def get_data():
    return {
        "heatmap": True,
        "heatmap_message": _(
            "This is based on the partnership businesses related to this educational institution"
        ),
        "internal_links": {
            "Business": ["partnership_business", "business"],
        },
        "transactions": [
            {
                "label": _("Partnership Business"),
                "items": ["Business"],
            },
        ],
    }
