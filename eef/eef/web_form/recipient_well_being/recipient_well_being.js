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

            // Enable สถาบัน
            frappe.web_form.set_df_property("institute", "reqd", 1);
            frappe.web_form.set_df_property("institute", "hidden", 0);
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

            // Disable สถาบัน
            frappe.web_form.set_df_property("institute", "reqd", 0);
            frappe.web_form.set_df_property("institute", "hidden", 1);
            frappe.web_form.set_value("institute", "");
        }
    });
});
