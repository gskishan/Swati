import frappe
from frappe import _
from frappe.utils import getdate

def build_conditions(base_conditions, filters, project=None, cost_center=None):
    if project:
        base_conditions += " AND project = %(project)s"
        filters["project"] = project
    if cost_center:
        base_conditions += " AND cost_center = %(cost_center)s"
        filters["cost_center"] = cost_center
    return base_conditions, filters

@frappe.whitelist()
def get_outstanding_sales_invoices(company, party_type, party, posting_date, project=None, cost_center=None):
    conditions = """
        docstatus = 1
        AND outstanding_amount > 0
        AND company = %(company)s
        AND customer = %(party)s
    """
    filters = {
        "company": company,
        "party": party,
        "posting_date": getdate(posting_date),
    }

    conditions, filters = build_conditions(conditions, filters, project, cost_center)

    return frappe.db.sql(f"""
        SELECT
            name, posting_date, due_date, outstanding_amount, customer, project, debit_to, grand_total
        FROM
            `tabSales Invoice`
        WHERE
            {conditions}
        ORDER BY posting_date ASC
    """, filters, as_dict=True)


@frappe.whitelist()
def get_outstanding_sales_orders(company, party_type, party, posting_date, project=None, cost_center=None):
    conditions = """
        docstatus = 1
        AND advance_paid < grand_total
        AND company = %(company)s
        AND customer = %(party)s
    """
    filters = {
        "company": company,
        "party": party,
        "posting_date": getdate(posting_date),
    }

    conditions, filters = build_conditions(conditions, filters, project, cost_center)

    return frappe.db.sql(f"""
        SELECT
            name, transaction_date, grand_total, customer, project, advance_paid
        FROM
            `tabSales Order`
        WHERE
            {conditions}
        ORDER BY transaction_date ASC
    """, filters, as_dict=True)


@frappe.whitelist()
def get_outstanding_purchase_invoices(company, party_type, party, posting_date, project=None, cost_center=None):
    conditions = """
        docstatus = 1
        AND outstanding_amount > 0
        AND company = %(company)s
        AND supplier = %(party)s
    """
    filters = {
        "company": company,
        "party": party,
        "posting_date": getdate(posting_date),
    }

    conditions, filters = build_conditions(conditions, filters, project, cost_center)

    return frappe.db.sql(f"""
        SELECT
            name, posting_date, due_date, bill_no, conversion_rate,
            outstanding_amount, supplier, project, credit_to,grand_total
        FROM
            `tabPurchase Invoice`
        WHERE
            {conditions}
        ORDER BY posting_date ASC
    """, filters, as_dict=True)


@frappe.whitelist()
def get_outstanding_purchase_orders(company, party_type, party, posting_date, project=None, cost_center=None):
    conditions = """
        docstatus = 1
        AND advance_paid < grand_total
        AND company = %(company)s
        AND supplier = %(party)s
    """
    filters = {
        "company": company,
        "party": party,
        "posting_date": getdate(posting_date),
    }

    conditions, filters = build_conditions(conditions, filters, project, cost_center)

    return frappe.db.sql(f"""
        SELECT
            name, transaction_date, grand_total, supplier, project, advance_paid
        FROM
            `tabPurchase Order`
        WHERE
            {conditions}
        ORDER BY transaction_date ASC
    """, filters, as_dict=True)
