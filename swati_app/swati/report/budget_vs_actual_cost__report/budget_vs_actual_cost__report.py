# Copyright (c) 2025, CRUXEDGE and contributors
# For license information, please see license.txt

# import frappe


import frappe
from frappe.utils import flt

def execute(filters=None):
    columns = get_columns()
    data = []

    # Get all projects
    project_query = """
        SELECT
            pr.name AS project,
            pr.project_name,
            pr.creation
        FROM `tabProject` pr
        WHERE 1=1
    """
    if filters.get("project"):
        project_query += " AND pr.name = %(project)s"
    if filters.get("from_date"):
        project_query += " AND pr.creation >= %(from_date)s"
    if filters.get("to_date"):
        project_query += " AND pr.creation <= %(to_date)s"
    project_query += " ORDER BY pr.creation DESC"

    projects = frappe.db.sql(project_query, filters, as_dict=True)

    for pr in projects:
        # Get related Material Requests
        mr_list = frappe.db.get_all("Material Request",
            filters={"docstatus": 1},
            fields=["name"],
        )
        mr_items = frappe.db.sql("""
               SELECT DISTINCT mr.name
               FROM `tabMaterial Request` mr
               INNER JOIN `tabMaterial Request Item` mri ON mr.name = mri.parent
               WHERE mr.docstatus = 1 AND mri.project = %s
           """, pr.project)
        material_requests = [mr[0] for mr in mr_items]

        # Get Purchase Orders
        po_list = frappe.db.get_all("Purchase Order",
            filters={"docstatus": 1, "project": pr.project},
            fields=["name", "total"]
        )

        # Get Purchase Order Items
        po_items = frappe.db.sql("""
            SELECT poi.item_code, poi.parent
            FROM `tabPurchase Order Item` poi
            INNER JOIN `tabPurchase Order` po ON po.name = poi.parent
            WHERE po.docstatus = 1 AND po.project = %s
        """, pr.project, as_dict=True)

        # Get Quotations
        quotations = frappe.db.get_all("Quotation",
            filters={"docstatus": 1},
            or_filters=[["custom_project", "=", pr.project]],
            fields=["name"]
        )

        max_len = max(
            len(material_requests),
            len(po_list),
            len(po_items),
            len(quotations),
            1  # at least one row
        )

        # Convert all lists to lists of values
        material_requests = list(material_requests)
        po_names = [po.name for po in po_list]
        po_totals = {po.name: po.total for po in po_list}
        po_item_lines = po_items
        quotation_names = [q.name for q in quotations]

        for i in range(max_len):
            data.append([
                pr.project,
                pr.project_name,
                pr.creation,
                material_requests[i] if i < len(material_requests) else "",
                po_names[i] if i < len(po_names) else "",
                po_item_lines[i]["item_code"] if i < len(po_item_lines) else "",
                flt(po_totals.get(po_item_lines[i]["parent"])) if i < len(po_item_lines) else 0.0,
                quotation_names[i] if i < len(quotation_names) else "",
            ])

    return columns, data

def get_columns():
    return [
        {"label": "Project No", "fieldname": "project", "fieldtype": "Link", "options": "Project", "width": 200},
        {"label": "Project Name", "fieldname": "project_name", "fieldtype": "Data", "width": 200},
        {"label": "Project Creation", "fieldname": "project_creation", "fieldtype": "Datetime", "width": 180,"hidden":1},
        {"label": "Material request Number", "fieldname": "material_request", "fieldtype": "Link", "options": "Material Request", "width": 200},
        {"label": "PO Number", "fieldname": "purchase_order", "fieldtype": "Link", "options": "Purchase Order", "width": 200},
        {"label": "Item Description", "fieldname": "po_item", "fieldtype": "Data", "width": 200},
        {"label": "Budgeted Price", "fieldname": "po_total", "fieldtype": "Currency", "width": 150},
        {"label": "Quotation", "fieldname": "quotation", "fieldtype": "Link", "options": "Quotation", "width": 200},
    ]
