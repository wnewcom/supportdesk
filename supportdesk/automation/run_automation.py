# Copyright (c) 2025, SupportDesk and contributors
# Run automation rules and template auto-apply on ticket events.
# Templates auto-apply when ticket status or ticket_type matches trigger (comma-separated in template).

import json
import frappe
from frappe import _


def run_ticket_automation(doc, method=None):
	"""Called from doc_events on Ticket after_insert and on_update."""
	if not doc or doc.doctype != "Ticket":
		return
	try:
		settings = frappe.get_single("SupportDesk Settings")
	except Exception:
		settings = None
	if settings and not getattr(settings, "automation_enabled", True):
		return
	# 1) Auto-apply templates by status or ticket_type (triggers in Ticket Template)
	_apply_templates(doc)
	# 2) Run automation rules (trigger_event: Ticket Created / Ticket Updated)
	_run_automation_rules(doc, method)


def _apply_templates(ticket):
	"""Apply Ticket Templates with auto_apply=1 when status or ticket_type matches trigger."""
	templates = frappe.get_all(
		"Ticket Template",
		filters={"auto_apply": 1},
		fields=["name", "default_status_trigger", "ticket_type_trigger", "checklist_items"],
	)
	for t in templates:
		apply = False
		if t.get("default_status_trigger") and ticket.status:
			triggers = [s.strip() for s in (t.default_status_trigger or "").split(",") if s.strip()]
			if ticket.status in triggers:
				apply = True
		if t.get("ticket_type_trigger") and ticket.ticket_type:
			triggers = [s.strip() for s in (t.ticket_type_trigger or "").split(",") if s.strip()]
			if ticket.ticket_type in triggers:
				apply = True
		if not apply:
			continue
		template_doc = frappe.get_doc("Ticket Template", t.name)
		for row in template_doc.checklist_items or []:
			existing = frappe.get_all(
				"Ticket Checklist Item",
				filters={"ticket": ticket.name, "task_description": row.task_description},
				limit=1,
			)
			if existing:
				continue
			frappe.get_doc({
				"doctype": "Ticket Checklist Item",
				"ticket": ticket.name,
				"task_description": row.task_description,
				"required": row.get("required") or 0,
				"order": row.get("order") or 0,
			}).insert(ignore_permissions=True)
	frappe.db.commit()


def _run_automation_rules(ticket, method=None):
	"""Run Automation Rule docs whose trigger_event matches."""
	trigger = "Ticket Created" if method == "after_insert" else "Ticket Updated"
	rules = frappe.get_all(
		"Automation Rule",
		filters={"enabled": 1, "trigger_event": trigger},
		fields=["name", "conditions", "actions"],
	)
	for r in rules:
		if not _conditions_match(r, ticket):
			continue
		_execute_actions(r, ticket)


def _conditions_match(rule, ticket) -> bool:
	"""Simple condition check; extend for JSON conditions."""
	# Placeholder: no conditions = match
	if not rule.get("conditions") or not (rule.conditions or "").strip():
		return True
	# Could parse JSON and evaluate; for now accept all
	return True


def _execute_actions(rule_doc, ticket):
	"""Apply actions: assign, priority, tag, note, email."""
	rule = frappe.get_doc("Automation Rule", rule_doc.name)
	actions_str = (rule.actions or "").strip()
	if not actions_str:
		return
	try:
		actions = json.loads(actions_str) if actions_str.startswith("{") or actions_str.startswith("[") else {}
	except Exception:
		actions = {}
	if isinstance(actions, dict):
		actions = [actions]
	for a in actions if isinstance(actions, list) else [actions]:
		action_type = a.get("action") or a.get("type")
		if action_type == "assign" and a.get("user"):
			ticket.db_set("assigned_to", a["user"])
		elif action_type == "priority" and a.get("priority"):
			ticket.db_set("priority", a["priority"])
		elif action_type == "add_tag" and a.get("tag"):
			# Append to tags
			cur = (ticket.tags or "").strip()
			ticket.db_set("tags", (cur + " " + a["tag"]).strip())
	frappe.db.commit()
