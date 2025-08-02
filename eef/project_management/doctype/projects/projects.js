// Copyright (c) 2025, Siwat Sroisuwan and contributors
// For license information, please see license.txt

frappe.ui.form.on("Projects", {
    refresh(frm) {
        const data = eef.geography.getProvinces()
        // console.log(data.map(d => d.provinceNameEn).join("\n"));
        frm.set_df_property(
            "province",
            "options",
            data
                .map(d => d.provinceNameEn)
                .sort((a, b) => a.localeCompare(b))
                .join("\n")
        );
    },
    province(frm) {
        console.log(frm.doc.province);
        const data = eef.geography.getDistricts(frm.doc.province);
        // console.log(data);
        console.log(data);
        frm.set_df_property(
            "district",
            "options",
            data
                .map(d => d.districtNameEn)
                .sort((a, b) => a.localeCompare(b))
                .join("\n")
        );
    }
});
