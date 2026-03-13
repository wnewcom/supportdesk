# Copyright (c) 2025, SupportDesk and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class TicketTemplate(Document):
	"""Template that adds checklist tasks to tickets; can auto-apply by status/type."""

	pass
