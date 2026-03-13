from frappe import _


def get_data():
    return [
        {
            "module_name": "SupportDesk",
            "category": "Modules",
            "label": _("SupportDesk"),
            "color": "#2490ef",
            "icon": "octicon octicon-inbox",
            "type": "module",
            "description": _(
                "Tickets, templates, labor, billing, inventory, SLA, automation, portal."
            ),
        }
    ]
