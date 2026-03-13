// Ticket list view - filters, sorting, pagination (default list provides these)
frappe.listview_settings["Ticket"] = {
	refresh: function (listview) {},
	get_indicator: function (doc) {
		if (doc.status === "Closed" || doc.status === "Resolved") {
			return [doc.status, "green", "status,=," + doc.status];
		}
		if (doc.priority === "Urgent") {
			return [doc.priority, "red", "priority,=,Urgent"];
		}
		return [doc.status, "blue", "status,=," + doc.status];
	},
};
