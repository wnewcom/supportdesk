// SupportDesk Ticket - checklist UI, timer hook
frappe.ui.form.on("Ticket", {
	refresh(frm) {
		// Checklist: show completion when checkbox toggled
		if (frm.fields_dict.checklist_items && frm.fields_dict.checklist_items.grid) {
			frm.fields_dict.checklist_items.grid.formatters.completed = function (value) {
				return value ? "✓" : "☐";
			};
		}
		if (!frm.doc.__islocal && frm.doc.customer) {
			frm.add_custom_button(__("Make Invoice"), function () {
				frappe.call({
					method: "supportdesk.api.billing.make_invoice",
					args: { ticket_name: frm.doc.name },
					callback: function (r) {
						if (r.message) {
							frappe.set_route("Form", "Sales Invoice", r.message);
							frm.reload_doc();
						}
					},
				});
			}, __("Create"));
		}
	}
});

// When checklist row completed is checked, set completed_by and completed_at (saved with parent)
frappe.ui.form.on("Ticket Checklist Item", {
	completed(frm, cdt, cdn) {
		const row = locals[cdt][cdn];
		if (row.completed) {
			frappe.model.set_value(cdt, cdn, "completed_by", frappe.session.user);
			frappe.model.set_value(cdt, cdn, "completed_at", frappe.datetime.now_datetime());
		} else {
			frappe.model.set_value(cdt, cdn, "completed_by", null);
			frappe.model.set_value(cdt, cdn, "completed_at", null);
		}
	}
});
