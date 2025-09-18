frappe.ready(function () {
    // bind events here
    frappe.web_form.validate = () => {
        let value = frappe.web_form.get_value("check_data_confirmation");
        if (value == 1) {
            return true;
        } else {
            frappe.msgprint("กรุณายืนยันการส่งโดยการเลือกปุ่ม Checkbox");
            return false;
        }
    };
});
