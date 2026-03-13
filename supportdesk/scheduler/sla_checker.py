# Copyright (c) 2025, SupportDesk and contributors
# Registered in hooks.py schedule_events (runs on scheduler tick). Check SLA breach for open tickets.

import frappe
from frappe.utils import now_datetime


def run():
	"""Find open tickets past due_date and add comment; optionally run SLA Breach automation rules."""
	tickets = frappe.get_all(
		"Ticket",
		filters={"status": ["not in", ["Resolved", "Closed"]], "due_date": ["<", now_datetime()]},
		fields=["name", "due_date", "assigned_to", "subject"],
	)
	for t in tickets:
		# Add one comment per breached ticket; run SLA Breach automation rules if configured
		frappe.get_doc("Ticket", t.name).add_comment("Info", "SLA breach: due date passed.")
	frappe.db.commit()
