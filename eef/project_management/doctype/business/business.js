// Copyright (c) 2025, Siwat Sroisuwan and contributors
// For license information, please see license.txt

frappe.ui.form.on("Business", {
	refresh(frm) {
		// โหลดข้อมูลจังหวัดทุกครั้ง
		const provinces = eef.geography.getProvinces();
		frm.set_df_property(
			"province",
			"options",
			provinces
				.map((d) => d.provinceNameEn)
				.sort((a, b) => a.localeCompare(b))
				.join("\n")
		);

		if (frm.is_new()) {
			// สำหรับข้อมูลใหม่ - ซ่อน section และเคลียร์ข้อมูล
			frm.set_df_property("section_break_bewc", "hidden", 1);
		} else {
			// สำหรับข้อมูลที่มีอยู่แล้ว - แสดง section และโหลดข้อมูล
			frm.set_df_property("section_break_bewc", "hidden", 0);
			frm.trigger("load_existing_address_data");
		}

        frm.call("has_partnership_institutions").then((r) => {
				if (r.message) {
                    // console.log("Partnership institutions found, showing business major interest section.");
                    // ถ้ามี partnership institution อย่างน้อย 1 รายการ ให้แสดง section
                    frm.set_df_property("business_major_interest", "hidden", 0);
                } else {
                    // console.log("No partnership institutions found, hiding business major interest section.");
                    // ถ้าไม่มี partnership institution ให้ซ่อน section
                    frm.set_df_property("business_major_interest", "hidden", 1);
                }
			})

		// ตั้งค่า query สำหรับ major field
		// console.log("Setting major query for business:", frm.doc.name);
		frm.trigger("set_major_query");
	},
	set_major_query(frm) {
		frm.set_query("major", "business_major_interest", function () {
			// console.log("Setting major query for business:", frm.doc.name);
			return {
				query: "eef.project_management.doctype.business.business.get_major_query",
				filters: {
					business_name: frm.doc.name,
				},
			};
		});
	},
	load_existing_address_data(frm) {
		// โหลดข้อมูลอำเภอตามจังหวัดที่มีอยู่
		if (frm.doc.province) {
			const districts = eef.geography.getDistricts(frm.doc.province);
			frm.set_df_property(
				"district",
				"options",
				districts
					.map((d) => d.districtNameEn)
					.sort((a, b) => a.localeCompare(b))
					.join("\n")
			);

			// โหลดข้อมูลตำบลตามอำเภอที่มีอยู่
			if (frm.doc.district) {
				const subdistricts = eef.geography.getSubdistricts(
					frm.doc.province,
					frm.doc.district
				);
				frm.set_df_property(
					"subdistrict",
					"options",
					subdistricts
						.map((d) => d.subdistrictNameEn)
						.sort((a, b) => a.localeCompare(b))
						.join("\n")
				);
			}
		}
	},
	province(frm) {
		// console.log("Province changed, refreshing district and subdistrict options.");
		// โหลดข้อมูลอำเภอตามจังหวัดที่เลือก
		const districts = eef.geography.getDistricts(frm.doc.province);
		frm.set_df_property(
			"district",
			"options",
			districts
				.map((d) => d.districtNameEn)
				.sort((a, b) => a.localeCompare(b))
				.join("\n")
		);

		// เคลียร์ข้อมูลที่เกี่ยวข้องเฉพาะเมื่อเปลี่ยนจังหวัด
		frm.set_df_property("subdistrict", "options", "");

		// เคลียร์ค่าเฉพาะเมื่อเป็นการเปลี่ยนแปลงจริง (ไม่ใช่การโหลดข้อมูลเดิม)
		if (frm.doc.district || frm.doc.subdistrict || frm.doc.postal_code) {
			frm.set_value("district", "");
			frm.set_value("subdistrict", "");
			frm.set_value("postal_code", "");
		}
	},
	district(frm) {
		// console.log("District changed, refreshing subdistrict options.");
		// โหลดข้อมูลตำบลตามอำเภอที่เลือก
		const subdistricts = eef.geography.getSubdistricts(frm.doc.province, frm.doc.district);
		frm.set_df_property(
			"subdistrict",
			"options",
			subdistricts
				.map((d) => d.subdistrictNameEn)
				.sort((a, b) => a.localeCompare(b))
				.join("\n")
		);

		// เคลียร์ค่าเฉพาะเมื่อเป็นการเปลี่ยนแปลงจริง
		if (frm.doc.subdistrict || frm.doc.postal_code) {
			frm.set_value("subdistrict", "");
			frm.set_value("postal_code", "");
		}
	},
	subdistrict(frm) {
		// console.log("Subdistrict changed, searching for postal code.");
		// ค้นหาและกำหนดรหัสไปรษณีย์
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

		// กำหนดรหัสไปรษณีย์ถ้ามี
		if (postalCode && postalCode !== "") {
			frm.set_value("postal_code", postalCode);
		} else {
			// เคลียร์รหัสไปรษณีย์ถ้าไม่พบ
			frm.set_value("postal_code", "");
		}
	},
	partnership_institution(frm) {
		// รีเฟรช query เมื่อมีการเปลี่ยนแปลง partnership institution
		// console.log("Partnership institution changed, refreshing major query.");
		frm.trigger("set_major_query");
	},
});

frappe.ui.form.on("Partnership Institution", {
	educational_institution: function (frm) {
		// รีเฟรช query เมื่อเปลี่ยน educational institution
		// console.log("Educational institution changed, refreshing major query.");
		frm.trigger("set_major_query");
	},
});

frappe.ui.form.on("Business Major Interest", {
	before_major_remove: function (frm) {
		// Refresh query when table is modified
		// console.log("Business major interest removed, refreshing major query.");
		frm.trigger("set_major_query");
	},
});
