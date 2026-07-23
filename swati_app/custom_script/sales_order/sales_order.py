import frappe
from frappe.utils import flt
from erpnext.selling.doctype.sales_order.sales_order import make_project as _make_project


@frappe.whitelist()
def make_project(source_name, target_doc=None):
	doc = _make_project(source_name, target_doc)
	doc.estimated_costing = flt(
		frappe.db.get_value("Sales Order", source_name, "custom_total_purchase")
	)
	return doc