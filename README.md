# SupportDesk

PSA (Professional Services Automation) for Frappe v15 + ERPNext: ticketing, templates with checklists, labor tracking, ERPNext billing & inventory, CRM linking, automation rules, SLA, email-to-ticket, customer portal, AI hooks.

## Install

```bash
bench get-app /path/to/supportdesk
bench --site your-site.local install-app supportdesk
bench build --app supportdesk
```

After install, create these roles in **Setup > Role** (if not present) and assign to users:

- **SupportDesk Customer** – portal access (view/create tickets)
- **SupportDesk Technician** – tickets, labor, parts, templates
- **SupportDesk Manager** – templates, automation rules, SLA policies, settings

## Module & Workspace

Appears in ERPNext Desk sidebar as **SupportDesk**. Clicking it opens the SupportDesk workspace with links to Tickets, Templates, Automation Rules, SLA Policies, Assets, and **SupportDesk Settings** (single-doc settings). Workspace is created on first migrate via patch.

## Best practices (this app)

- **DocTypes:** Pascal Case (Ticket, Labor Entry, Ticket Template, etc.); child tables use parent prefix where appropriate.
- **ERPNext:** Uses existing DocTypes (Customer, Contact, Address, Item, Warehouse, Sales Invoice, Stock Entry) via `frappe.get_doc` / `frappe.get_all`; no core overrides.
- **Scheduler:** All jobs registered in `hooks.py` under `schedule_events` (SLA checker, automation runner).
- **Templates:** Ticket Template auto-apply runs on ticket create/update when `auto_apply` is set and status or ticket_type matches the trigger (comma-separated).
- **Settings:** SupportDesk Settings is a Single doctype and is linked from the SupportDesk workspace.

## Troubleshooting "Internal Server Error"

1. **Get the traceback** (on the server):
   ```bash
   cd ~/frappe-bench
   tail -100 sites/erp.local/logs/web.error.log
   ```
   Or when running `bench start`, check the terminal for the Python traceback when you trigger the error.

2. **Common causes**
   - **Module not found:** Ensure the app is installed in the env: `./env/bin/pip install -e apps/supportdesk`
   - **Wrong folder structure:** You must have `apps/supportdesk/supportdesk/hooks.py` (two-level `supportdesk`).
   - **Migrate failed:** Run `bench --site erp.local migrate` and fix any patch/doctype errors.
   - **Clear cache:** `bench --site erp.local clear-cache` then reload.

3. **Temporarily simplify hooks** to isolate the error: in `hooks.py` comment out `doc_events` and `schedule_events`, restart, and see if the site loads. Then re-enable one block at a time.

## Features

- **Ticketing:** Ticket DocType with CRM links (Customer, Contact, Address), status, priority, checklist.
- **Templates:** Ticket Template + Template Checklist Item; auto-apply by status/ticket type.
- **Labor:** Labor Entry with timer (Start/Stop), duration; **Make Invoice** creates Sales Invoice from labor + parts.
- **Parts:** Ticket Part (submittable) creates Stock Entry (Material Issue).
- **Automation:** Automation Rule (trigger + actions); runs on ticket create/update.
- **SLA:** SLA Policy; scheduler runs every minute to check breach.
- **Email-to-ticket:** Enable in SupportDesk Settings; incoming Communication creates Ticket.
- **Portal:** `/portal/tickets`, `/portal/ticket/<name>`, `/portal/new-ticket` (Jinja).
- **AI:** Hooks in `supportdesk.ai.hooks` for summary/priority (extend with your LLM).
