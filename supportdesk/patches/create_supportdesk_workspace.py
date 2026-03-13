# Copyright (c) 2025, SupportDesk and contributors
# One-time patch: create SupportDesk workspace so Settings is accessible from Desk.

import frappe


def execute():
	try:
		if frappe.db.exists("Workspace", "SupportDesk"):
			return
		ws = frappe.get_doc(
			{
				"doctype": "Workspace",
				"name": "SupportDesk",
				"title": "SupportDesk",
				"module": "supportdesk",
				"icon": "inbox",
				"indicator_color": "Blue",
				"public": 1,
			}
		)
		for link in [
			{"label": "Tickets", "link_to": "List/Ticket", "type": "Link"},
			{"label": "Templates", "link_to": "List/Ticket Template", "type": "Link"},
			{"label": "Automation Rules", "link_to": "List/Automation Rule", "type": "Link"},
			{"label": "SLA Policies", "link_to": "List/SLA Policy", "type": "Link"},
			{"label": "Assets", "link_to": "List/Asset", "type": "Link"},
			{"label": "SupportDesk Settings", "link_to": "Form/SupportDesk Settings/SupportDesk Settings", "type": "Link"},
		]:
			ws.append("links", link)
		ws.insert(ignore_permissions=True)
		frappe.db.commit()
	except Exception as e:
		frappe.log_error(title="SupportDesk workspace patch", message=str(e))
		# Do not re-raise: allow migrate to complete; workspace can be created manually
