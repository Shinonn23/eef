// EEF App JavaScript Utilities

window.eef = window.eef || {};

eef.user = {
	/**
	 * Get recent projects for the current user
	 * @param {function} callback - Callback function to handle the result
	 */
	getRecentProjects(callback) {
		// console.log("[eef.user.getRecentProjects] called with callback:", callback);
		frappe.call({
			method: "frappe.client.get_value",
			args: {
				doctype: "User",
				filters: { name: frappe.session.user },
				fieldname: ["recent_projects"],
			},
			callback: function (response) {
				// console.log("[eef.user.getRecentProjects] response:", response);
				const project = response.message ? response.message.recent_projects : null;
				if (callback) callback(project);
			},
		});
	},

	/**
	 * Set recent projects for the current user
	 * @param {string} projectName - Project name to set as recent
	 * @param {function} callback - Optional callback function to handle the result
	 */
	setRecentProjects(projectName, callback) {
		// console.log("[eef.user.setRecentProjects] called with projectName:", projectName, "callback:", callback);
		frappe.call({
			method: "frappe.client.set_value",
			args: {
				doctype: "User",
				name: frappe.session.user,
				fieldname: "recent_projects",
				value: projectName,
			},
			callback: function (response) {
				// console.log("[eef.user.setRecentProjects] response:", response);
				if (response.message) {
					frappe.show_alert({
						message: __("Recent project updated successfully"),
						indicator: "green",
					});
				}
				if (callback) callback(!!response.message, response);
			},
		});
	},
};

// console.log("[eef.user] Utility functions loaded:", eef.user);
