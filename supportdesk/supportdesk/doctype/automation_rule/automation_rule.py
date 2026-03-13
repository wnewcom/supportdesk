# Copyright (c) 2025, SupportDesk and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class AutomationRule(Document):
	"""Rule to run on ticket events: assign, change priority, add tag, note, email."""

	pass
