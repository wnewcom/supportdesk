// Labor Entry - timer in UI: Start Work, Pause, Stop
frappe.ui.form.on("Labor Entry", {
	refresh(frm) {
		if (frm.doc.__islocal) return;
		// Timer controls for technicians
		if (frm.doc.start_time && !frm.doc.end_time) {
			frm.add_custom_button(__("Stop Timer"), function () {
				frappe.db.set_value("Labor Entry", frm.doc.name, "end_time", frappe.datetime.now_datetime());
				frm.reload_doc();
			});
		} else if (!frm.doc.start_time) {
			frm.add_custom_button(__("Start Timer"), function () {
				frappe.db.set_value("Labor Entry", frm.doc.name, "start_time", frappe.datetime.now_datetime());
				frm.reload_doc();
			});
		}
	}
});
