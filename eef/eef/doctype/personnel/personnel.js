// Copyright (c) 2025, Siwat Sroisuwan and contributors
// For license information, please see license.txt

// frappe.ui.form.on("Personnel", {
// 	refresh(frm) {

// 	},
// });

frappe.ui.form.on("Personnel", {
    refresh(frm) {
        const campus_province = eef.geography.getProvinces();
        frm.set_df_property(
            "campus_province",
            "options",
            campus_province
                .map((d) => d.provinceNameEn)
                .sort((a, b) => a.localeCompare(b))
                .join("\n")
        );
    },
});
