import frappe
from frappe.utils import flt
from erpnext.selling.doctype.quotation.quotation import make_sales_order as _make_sales_order


@frappe.whitelist()
def make_sales_order(source_name, target_doc=None):
	doc = _make_sales_order(source_name, target_doc)

	qtn = frappe.get_doc("Quotation", source_name)
	sales_price = {row.name: flt(row.custom_sales_price) for row in qtn.items}

	for item in doc.items:
		price = sales_price.get(item.quotation_item)
		if price:
			item.rate = price

	doc.run_method("calculate_taxes_and_totals")
	return doc

def validate(doc, method):
    pass
    # for item in doc.items:
    #     if item.rate and item.qty and item.custom_duration:
    #         amt = item.rate * item.qty * item.custom_duration
    #         item.amount = amt
    #         item.net_amount = amt
    #         item.base_amount = amt
    #         item.base_net_amount = amt
        