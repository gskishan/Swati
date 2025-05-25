import frappe
from frappe.utils import nowdate

@frappe.whitelist()
def move_expired_users():
    today = nowdate()

    # Get all Project records
    projects = frappe.get_all("Project", fields=["name"])

    for proj in projects:
        doc = frappe.get_doc("Project", proj.name)

        # Only proceed if 'users' child table has data
        if doc.get("users"):
            updated_users = []

            for row in list(doc.users):
                if row.custom_to_date and str(row.custom_to_date) < today:
                    doc.append("custom_project_users", {
                        "user": row.user,
                        "email": frappe.db.get_value("User", row.user, "email"),
                        "full_name": row.full_name,
                        "from_date": row.custom_from_date,
                        "to_date": row.custom_to_date
                    })
                    updated_users.append(row)

            for row in updated_users:
                doc.remove(row)

            if updated_users:
                doc.save(ignore_permissions=True)
                frappe.db.commit()

def update_expected_date(doc, method):
    if doc.sales_order:
        frappe.db.set_value("Sales Order", {"name":doc.sales_order}, "custom_expected_start_date", doc.expected_start_date)
        frappe.db.set_value("Sales Order", {"name":doc.sales_order}, "custom_expected_end_date", doc.expected_end_date)
        frappe.db.commit()



