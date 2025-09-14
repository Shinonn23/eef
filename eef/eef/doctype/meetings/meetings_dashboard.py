from frappe import _


def get_data():
    return {
        "heatmap": True,
        "heatmap_message": _(
            "This shows activities and outcomes related to this meeting"
        ),
        "fieldname": "meeting",
        "internal_links": {
            "Agenda": ["meeting", "name"],
            "Discussions": ["meeting", "name"],
            "Decisions": ["meeting", "name"],
            "Action": ["meeting", "name"],
        },
        "transactions": [
            {
                "label": _("Meeting Structure"),
                "items": ["Agenda"],
            },
            {
                "label": _("Meeting Activities"),
                "items": ["Discussions"],
            },
            {
                "label": _("Meeting Outcomes"),
                "items": ["Decisions", "Action"],
            },
        ],
    }
