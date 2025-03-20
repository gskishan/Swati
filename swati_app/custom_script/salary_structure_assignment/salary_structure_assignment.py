import frappe

def on_submit(doc, method):
    for d in doc.custom_salary_structure:
        new_doc = frappe.new_doc("Salary Structure Assignment Project Wise")
        new_doc.salary_structure = d.salary_structure
        new_doc.project = d.project
        new_doc.base = d.base
        new_doc.ref = doc.name
        new_doc.employee = doc.employee
        new_doc.employee_name = doc.employee_name
        new_doc.from_date = doc.from_date
        new_doc.company = doc.company
        new_doc.currency = doc.currency
        new_doc.department = doc.department
        new_doc.designation = doc.designation
        new_doc.grade = doc.grade
        new_doc.from_date = doc.from_date
        new_doc.income_tax_slab = doc.income_tax_slab
        new_doc.payroll_payable_account = doc.payroll_payable_account
        new_doc.variable = doc.variable
        new_doc.taxable_earnings_till_date = doc.taxable_earnings_till_date
        new_doc.tax_deducted_till_date = doc.tax_deducted_till_date

        new_doc.save()
        new_doc.submit()

def on_cancel(doc, method):
    assignments = frappe.db.sql("""
        SELECT name FROM `tabSalary Structure Assignment Project Wise`
        WHERE ref=%s
    """, (doc.name,), as_dict=True)
    
    for assignment in assignments:
        assignment_doc = frappe.get_doc("Salary Structure Assignment Project Wise", assignment.name)
        assignment_doc.cancel()