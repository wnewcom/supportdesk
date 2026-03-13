# Copyright (c) 2025, SupportDesk and contributors
# AI assistant hooks - extend for ticket summarization, priority suggestions, suggested replies.

import frappe


def get_ai_ticket_summary(ticket_doc):
	"""Return placeholder for AI-generated summary. Integrate with your LLM API."""
	if not ticket_doc:
		return ""
	# Optional: call external API for summary
	return (ticket_doc.subject or "") + ": " + ((ticket_doc.description or "")[:200] + "..." if (ticket_doc.description or "").__len__() > 200 else (ticket_doc.description or ""))


def suggest_priority(ticket_doc):
	"""Return suggested priority (Low/Normal/High/Urgent). Override with AI."""
	return ticket_doc.priority or "Normal"
