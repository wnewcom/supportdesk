# Copyright (c) 2025, SupportDesk and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.utils import get_datetime, time_diff_in_seconds, flt


class LaborEntry(Document):
	def validate(self):
		if self.start_time and self.end_time:
			start = get_datetime(self.start_time)
			end = get_datetime(self.end_time)
			if end and start and end >= start:
				self.duration_minutes = int(flt(time_diff_in_seconds(end, start)) / 60)
