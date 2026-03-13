# SupportDesk PSA - Frappe v15
# Required: ERPNext. Use existing ERPNext DocTypes; do not duplicate.
# Frappe best practices: frappe.get_doc / frappe.get_all; whitelist API; no core overrides.

app_name = "supportdesk"
app_title = "SupportDesk"
app_publisher = "SupportDesk"
app_description = "PSA: ticketing, labor, billing, inventory, SLA, automation, portal"
app_email = ""
app_license = "MIT"

required_apps = ["erpnext"]

# -----------------------------------------------------------------------------
# Scheduler: all jobs registered here (run on scheduler tick, default ~5 min)
# For every-minute SLA checks, configure a Scheduled Job Type in Desk.
# -----------------------------------------------------------------------------
schedule_events = [
    {"all": ["supportdesk.scheduler.sla_checker.run"]},
    {"all": ["supportdesk.scheduler.automation_runner.run"]},
]

# -----------------------------------------------------------------------------
# Doc Events
# -----------------------------------------------------------------------------
doc_events = {
    "Ticket": {
        "after_insert": "supportdesk.automation.run_automation.run_ticket_automation",
        "on_update": "supportdesk.automation.run_automation.run_ticket_automation",
    },
    "Communication": {
        "after_insert": "supportdesk.email_handler.on_email_received",
    },
}

# -----------------------------------------------------------------------------
# Portal
# -----------------------------------------------------------------------------
portal_menu_items = [
    {"title": "Tickets", "route": "/portal/tickets", "role": "SupportDesk Customer"},
    {"title": "New Ticket", "route": "/portal/new-ticket", "role": "SupportDesk Customer"},
]

# -----------------------------------------------------------------------------
# Overrides (none; use ERPNext existing models only)
# -----------------------------------------------------------------------------
# override_doctype_class = {}
# fixtures = []
