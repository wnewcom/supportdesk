# Copyright (c) 2025, SupportDesk and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class Ticket(Document):
	def before_save(self):
		if not self.billing_status:
			self.billing_status = "Not Billed"
		# Keep ticket_id in sync with name (set after naming)
		if self.get("__islocal") and not self.ticket_id:
			pass  # name not set yet
		elif self.name and (not self.ticket_id or self.ticket_id != self.name):
			self.ticket_id = self.name

	def before_insert(self):
		if not self.naming_series:
			try:
				settings = frappe.get_single("SupportDesk Settings")
				prefix = (settings.ticket_number_prefix or "TKT").strip()
			except Exception:
				prefix = "TKT"
			self.naming_series = prefix + "-.#####"

	def on_update(self):
		# Checklist completion timestamps handled in client
		pass
