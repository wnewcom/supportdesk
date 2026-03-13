# Copyright (c) 2025, SupportDesk and contributors
# Portal page: /portal/ticket/<name>

import frappe
from frappe import _


def get_context(context):
	name = frappe.form_dict.name
	if not name:
		frappe.redirect_to_message(_("Missing ticket"), _("Ticket name is required."), indicator_color="red")
		frappe.local.flags.redirect_location = "/portal/tickets"
		raise frappe.Redirect
	try:
		doc = frappe.get_doc("Ticket", name)
	except Exception:
		frappe.redirect_to_message(_("Not found"), _("Ticket not found."), indicator_color="red")
		frappe.local.flags.redirect_location = "/portal/tickets"
		raise frappe.Redirect
	# Permission check
	user = frappe.session.user
	if user == "Guest":
		frappe.throw(_("Not permitted"))
	contact = frappe.get_all("Contact", filters={"user": user}, pluck="name", limit=1)
	customers = []
	if contact:
		links = frappe.get_all(
			"Dynamic Link",
			filters={"parent": contact[0], "link_doctype": "Customer"},
			pluck="link_name",
		)
		customers = list(links or [])
	if doc.customer not in customers and "SupportDesk Technician" not in frappe.get_roles() and "System Manager" not in frappe.get_roles():
		frappe.throw(_("Not permitted to view this ticket"))
	context.doc = doc
	context.no_cache = 1
	return context
