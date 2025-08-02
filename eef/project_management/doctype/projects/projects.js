// Copyright (c) 2025, Siwat Sroisuwan and contributors
// For license information, please see license.txt

frappe.ui.form.on("Projects", {
	refresh(frm) {
		const data = eef.geography.getProvinces();
		frm.set_df_property(
			"province",
			"options",
			data
				.map((d) => d.provinceNameEn)
				.sort((a, b) => a.localeCompare(b))
				.join("\n")
		);
		frm.set_value("province", "");
		frm.set_value("district", "");
		frm.set_value("subdistrict", "");
	},
	province(frm) {
		const data = eef.geography.getDistricts(frm.doc.province);
		frm.set_df_property(
			"district",
			"options",
			data
				.map((d) => d.districtNameEn)
				.sort((a, b) => a.localeCompare(b))
				.join("\n")
		);
        frm.set_df_property(
            "subdistrict",
            "options",
            "None"
        );
		frm.set_value("district", "None");
		frm.set_value("subdistrict", "None");
		frm.set_value("postal_code", "");
	},
	district(frm) {
		const data = eef.geography.getSubdistricts(frm.doc.province, frm.doc.district);
		frm.set_df_property(
			"subdistrict",
			"options",
			data
				.map((d) => d.subdistrictNameEn)
				.sort((a, b) => a.localeCompare(b))
				.join("\n")
		);
		frm.set_value("subdistrict", "None");
		frm.set_value("postal_code", "");
	},
	subdistrict(frm) {
		let data = {};
		if (frm.doc.subdistrict) {
			data = eef.geography.smartSearch({
				province: frm.doc.province,
				district: frm.doc.district,
				subdistrict: frm.doc.subdistrict,
			});
		}
		let postalCode = "";
		if (data.results && Array.isArray(data.results) && data.results.length > 0) {
			postalCode = data.results[0]["postalCode"];
		}
		if (postalCode && postalCode !== "") {
			frm.set_value("postal_code", postalCode);
		}
	},
});
