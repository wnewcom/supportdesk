# Copyright (c) 2025, SupportDesk and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe import _


class TicketPart(Document):
	"""Parts used on a ticket; creates Stock Entry (Material Issue) and can be added to invoice."""

	def on_submit(self):
		self.make_stock_entry()

	def make_stock_entry(self):
		if not self.warehouse or not self.item or self.qty <= 0:
			return
		company = frappe.get_value("Warehouse", self.warehouse, "company")
		if not company:
			frappe.throw(_("Warehouse {0} has no Company.").format(self.warehouse))
		ste = frappe.get_doc(
			{
				"doctype": "Stock Entry",
				"purpose": "Material Issue",
				"company": company,
				"items": [
					{
						"item_code": self.item,
						"qty": self.qty,
						"s_warehouse": self.warehouse,
						"serial_no": self.serial_no or None,
						"batch_no": self.batch_no or None,
					}
				],
			}
		)
		ste.insert(ignore_permissions=True)
		ste.submit()
		frappe.msgprint(frappe._("Stock Entry {0} created.").format(ste.name))
