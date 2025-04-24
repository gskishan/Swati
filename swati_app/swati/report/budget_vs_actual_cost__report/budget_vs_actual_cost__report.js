// Copyright (c) 2025, CRUXEDGE and contributors
// For license information, please see license.txt

frappe.query_reports["Budget vs Actual Cost  Report"] = {
	"filters": [
        {
            "fieldname": "project",
            "label": "Project",
            "fieldtype": "Link",
            "options": "Project"
        },
        {
            "fieldname": "from_date",
            "label": "From Date",
            "fieldtype": "Date"
        },
        {
            "fieldname": "to_date",
            "label": "To Date",
            "fieldtype": "Date"
        }

	]
};
