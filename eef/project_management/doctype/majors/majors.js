// Copyright (c) 2025, Siwat Sroisuwan and contributors
// For license information, please see license.txt

frappe.ui.form.on("Majors", {
	refresh(frm) {
		let recentProjects;
		eef.user.getRecentProjects(function (project) {
			recentProjects = project;
			if (recentProjects) {
				frm.set_value("project", recentProjects);
			} else {
				frm.set_value("project", "");
			}
		});
	},
});
