# Copyright (c) 2025, SupportDesk and contributors
# Email-to-ticket: create Ticket from incoming email when enabled in settings.

import frappe
from frappe import _


def on_email_received(doc, method=None):
	"""Create or attach to Ticket from incoming email when Enable Email to Ticket is on. Called from Communication after_insert."""
	communication = doc
	if getattr(communication, "sent_or_received", None) != "Received":
		return
	if communication.get("reference_doctype") and communication.get("reference_name"):
		return  # Reply to existing doc
	try:
		settings = frappe.get_single("SupportDesk Settings")
	except Exception:
		return
	if not getattr(settings, "enable_email_to_ticket", False):
		return
	# Create new ticket from email
	subject = (communication.get("subject") or "").strip() or _("No subject")
	content = (communication.get("content") or "").strip()
	# Try to find customer from sender email
	sender = (communication.get("sender") or "").strip()
	customer = None
	if sender:
		contact = frappe.get_all(
			"Contact",
			filters={"email_id": sender},
			fields=["name"],
			limit=1,
		)
		if contact:
			links = frappe.get_all(
				"Dynamic Link",
				filters={"parent": contact[0]["name"], "link_doctype": "Customer"},
				pluck="link_name",
				limit=1,
			)
			if links:
				customer = links[0]
	doc = frappe.get_doc(
		{
			"doctype": "Ticket",
			"subject": subject[:140],
			"description": content or subject,
			"status": "Open",
			"customer": customer,
		}
	)
	doc.insert(ignore_permissions=True)
	# Link communication to ticket
	frappe.db.set_value("Communication", communication.name, "reference_doctype", "Ticket")
	frappe.db.set_value("Communication", communication.name, "reference_name", doc.name)
	frappe.db.commit()
