// Copyright (c) 2025, Siwat Sroisuwan and contributors
// For license information, please see license.txt

frappe.ui.form.on("Educational Institution", {
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
			// สำหรับข้อมูลที่มีอยู่แล้ว - โหลดข้อมูลที่เกี่ยวข้อง
			frm.trigger("load_existing_address_data");
		}
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
});
