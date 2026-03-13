# Copyright (c) 2025, SupportDesk and contributors
# Customer portal API - whitelisted; customers see only their tickets.

import frappe
from frappe import _


@frappe.whitelist()
def get_my_tickets():
	"""List tickets for current user (customer): filter by contact/customer link to user."""
	user = frappe.session.user
	if frappe.session.user == "Guest":
		frappe.throw(_("Not permitted"))

	# Find customer linked to this user (e.g. Contact linked to user)
	contact = frappe.get_all(
		"Contact",
		filters={"user": user},
		fields=["name"],
		limit=1,
	)
	customers = []
	if contact:
		links = frappe.get_all(
			"Dynamic Link",
			filters={"parent": contact[0]["name"], "link_doctype": "Customer"},
			pluck="link_name",
		)
		customers = list(set(links))
	if not customers:
		# Customer portal: only show tickets for linked customer
		return []

	tickets = frappe.get_all(
		"Ticket",
		filters={"customer": ["in", customers]},
		fields=["name", "ticket_id", "subject", "status", "priority", "creation"],
		order_by="modified desc",
		limit=100,
	)
	return tickets


@frappe.whitelist()
def get_ticket(name: str):
	"""Return ticket doc for portal; only if customer matches current user."""
	if not name or frappe.session.user == "Guest":
		frappe.throw(_("Not permitted"))
	doc = frappe.get_doc("Ticket", name)
	# Permission: ensure user is customer or has role
	contact = frappe.get_all("Contact", filters={"user": frappe.session.user}, pluck="name", limit=1)
	customers = []
	if contact:
		links = frappe.get_all(
			"Dynamic Link",
			filters={"parent": contact[0]["name"], "link_doctype": "Customer"},
			pluck="link_name",
		)
		customers = list(links or [])
	else:
		customers = []
	if doc.customer not in customers and "SupportDesk Technician" not in frappe.get_roles() and "System Manager" not in frappe.get_roles():
		frappe.throw(_("Not permitted to view this ticket"))
	return doc.as_dict()
