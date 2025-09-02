from frappe import _


def get_data():
    return {
        "heatmap": True,
        "heatmap_message": _("This shows activities and outcomes related to this agenda item"),
        "fieldname": "agenda",
        "internal_links": {
            "Discussions": ["agenda", "name"],
            "Decisions": ["agenda", "name"],
            "Action": ["agenda", "name"],
        },
        "transactions": [
            {
                "label": _("Agenda Activities"),
                "items": ["Discussions"],
            },
            {
                "label": _("Agenda Outcomes"),
                "items": ["Decisions", "Action"],
            },
        ],
    }
