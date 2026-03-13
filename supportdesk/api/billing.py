# Copyright (c) 2025, SupportDesk and contributors
# ERPNext billing: create Sales Invoice from Ticket (labor + parts).

import frappe
from frappe import _
from frappe.utils import flt, get_datetime


@frappe.whitelist()
def make_invoice(ticket_name: str) -> str:
	"""Create ERPNext Sales Invoice from Ticket: labor entries (hours as qty) + ticket parts."""
	if not ticket_name or not isinstance(ticket_name, str):
		frappe.throw(_("Ticket name is required"))

	ticket = frappe.get_doc("Ticket", ticket_name)
	if not ticket.customer:
		frappe.throw(_("Ticket has no Customer. Set Customer to create invoice."))

	# Labor: Labor Entry with charge_now and billable -> Item (service_item), Qty = duration_minutes/60
	labors = frappe.get_all(
		"Labor Entry",
		filters={"ticket": ticket_name, "billable": 1, "charge_now": 1, "docstatus": 1},
		fields=["name", "service_item", "rate", "duration_minutes", "technician"],
	)
	# Parts: Ticket Part -> Item, Qty
	parts = frappe.get_all(
		"Ticket Part",
		filters={"ticket": ticket_name, "docstatus": 1},
		fields=["name", "item", "qty", "cost"],
	)

	items = []
	for le in labors:
		if not le.get("service_item"):
			continue
		qty = flt(le.get("duration_minutes") or 0) / 60.0
		if qty <= 0:
			continue
		rate = flt(le.get("rate")) or 0
		items.append({
			"item_code": le.service_item,
			"qty": qty,
			"rate": rate,
			"amount": qty * rate,
		})
	for tp in parts:
		if not tp.get("item"):
			continue
		qty = flt(tp.get("qty")) or 1
		rate = flt(tp.get("cost")) or 0
		items.append({
			"item_code": tp.item,
			"qty": qty,
			"rate": rate,
			"amount": qty * rate,
		})

	if not items:
		frappe.throw(_("No billable labor or parts found for this ticket."))

	# Use ERPNext Sales Invoice; company from default or Customer if available
	company = frappe.defaults.get_default("company")
	if not company and hasattr(frappe.get_meta("Customer"), "get_field"):
		company = frappe.get_cached_value("Customer", ticket.customer, "default_company")
	if not company:
		frappe.throw(_("Company is required for Sales Invoice. Set Default Company in Customer or Global Defaults."))

	inv = frappe.get_doc(
		{
			"doctype": "Sales Invoice",
			"company": company,
			"customer": ticket.customer,
			"customer_address": ticket.address or None,
			"contact_person": ticket.contact or None,
			"items": [{"item_code": it["item_code"], "qty": it["qty"], "rate": it["rate"]} for it in items],
		}
	)
	inv.insert(ignore_permissions=True)
	# Optionally set ticket billing_status and link invoice (custom field on SI or comment)
	ticket.db_set("billing_status", "Partially Billed")
	frappe.msgprint(_("Sales Invoice {0} created.").format(inv.name))
	return inv.name
