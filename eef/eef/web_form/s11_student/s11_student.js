frappe.ready(function () {
    // bind events here
    frappe.web_form.validate = () => {
        let value = frappe.web_form.get_value("check_data_confirmation");
        if (value == 1) {
            return true;
        } else {
            frappe.msgprint(__("Please confirm submission by checking the checkbox"));
            return false;
        }
    };

    // Event handler for when Checkbox "หาชื่อไม่เจอในระบบ" is toggled
    frappe.web_form.on("no_name_in_system", (field, value) => {
        if (value === 1) {
            // Checkbox is checked
            // Disable ชื่อ-นามสกุล (จากฐานข้อมูล)
            frappe.web_form.set_df_property("full_name", "reqd", 0);
            frappe.web_form.set_df_property("full_name", "read_only", 1);
            frappe.web_form.set_df_property("full_name", "hidden", 1);
            frappe.web_form.set_value("full_name", "");

            // Enable ชื่อ-นามสกุล (ใส่เองหากไม่เจอในระบบ)
            frappe.web_form.set_df_property("full_name_manual", "reqd", 1);
            frappe.web_form.set_df_property("full_name_manual", "hidden", 0);
        } else {
            // Checkbox is unchecked

            // Enable ชื่อ-นามสกุล (จากฐานข้อมูล)
            frappe.web_form.set_df_property("full_name", "reqd", 1);
            frappe.web_form.set_df_property("full_name", "read_only", 0);
            frappe.web_form.set_df_property("full_name", "hidden", 0);

            // Disable ชื่อ-นามสกุล (ใส่เองหากไม่เจอในระบบ)
            frappe.web_form.set_df_property("full_name_manual", "reqd", 0);
            frappe.web_form.set_df_property("full_name_manual", "hidden", 1);
            frappe.web_form.set_value("full_name_manual", "");
        }
    });

    // Filter names and major for institute
    frappe.web_form.on("institute", (field, value) => {
        filterByInstituteStudent(value);
    });
});

function filterByInstituteStudent(institute) {
    frappe.call({
        method: "eef.eef.api.webform.get_students_and_major_by_institute",
        args: {
            institute: institute,
        },
        callback: function (r) {
            // Filter full_name field
            const opt_students = [];
            if (r.message?.students) {
                const data = r.message.students;
                for (var i = 0; i < data.length; i++) {
                    opt_students.push({
                        label: data[i].name,
                        value: data[i].name,
                    });
                }
            }
            const field_full_name = frappe.web_form.fields_dict["full_name"];
            field_full_name._data = opt_students;
            field_full_name.refresh();

            // Filter major field
            const opt_major = [];
            if (r.message?.majors) {
                const data = r.message.majors;
                for (var i = 0; i < data.length; i++) {
                    opt_major.push({
                        label: data[i].name1, // name1 is the name without abbreviation.
                        value: data[i].name,
                    });
                }
            }

            const field_major = frappe.web_form.fields_dict["major"];
            field_major._data = opt_major;
            field_major.refresh();
        },
    });
}
