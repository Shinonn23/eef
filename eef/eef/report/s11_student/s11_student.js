// Copyright (c) 2025, Siwat Sroisuwan and contributors
// For license information, please see license.txt

frappe.query_reports["S11 Student"] = {
    filters: [
        {
            fieldname: "institute",
            label: __("สถาบันการศึกษา"),
            fieldtype: "Link",
            options: "Educational Institution",
            reqd: 0,
        },
        {
            fieldname: "supporting_the_times",
            label: __("หนุนเสริมครั้งที่"),
            fieldtype: "Int",
            reqd: 0,
        },
    ],
};
