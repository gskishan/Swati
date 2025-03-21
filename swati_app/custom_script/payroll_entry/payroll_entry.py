import frappe
from frappe import _
from frappe.model.document import Document
from hrms.payroll.doctype.payroll_entry.payroll_entry import PayrollEntry
from hrms.payroll.doctype.payroll_entry.payroll_entry import get_existing_salary_slips,log_payroll_failure

from frappe.utils import (
	DATE_FORMAT,
	add_days,
	add_to_date,
	cint,
	comma_and,
	date_diff,
	flt,
	get_link_to_form,
	getdate,
)

import json
class CustomPayrollEntry(PayrollEntry):
	@frappe.whitelist()
	def create_salary_slips(self):
		"""
		Creates salary slip for selected employees if already not created
		"""
		self.check_permission("write")
		employees = [emp.employee for emp in self.employees]

		if employees:
			args = frappe._dict(
				{
					"salary_slip_based_on_timesheet": self.salary_slip_based_on_timesheet,
					"payroll_frequency": self.payroll_frequency,
					"start_date": self.start_date,
					"end_date": self.end_date,
					"company": self.company,
					"posting_date": self.posting_date,
					"deduct_tax_for_unclaimed_employee_benefits": self.deduct_tax_for_unclaimed_employee_benefits,
					"deduct_tax_for_unsubmitted_tax_exemption_proof": self.deduct_tax_for_unsubmitted_tax_exemption_proof,
					"payroll_entry": self.name,
					"exchange_rate": self.exchange_rate,
					"currency": self.currency,
				}
			)
			create_salary_slips_for_employees(employees, args, publish_progress=False)
			

def set_salary_structure_assignment(args, employee):
	# Get the latest active Salary Structure Assignment for the given employee
	salary_structure_assignment = frappe.db.get_value(
		"Salary Structure Assignment",
		{
			"employee": employee,
			"from_date": ("<=", args.get("start_date")),
			"docstatus": 1,
		},
		"*",
		order_by="from_date desc",
		as_dict=True,
	)

	if not salary_structure_assignment:
		frappe.throw(_("No Salary Structure Assignment found for Employee {0}").format(employee))

	sa = frappe.get_doc("Salary Structure Assignment", salary_structure_assignment.get("name"))

	projects_with_salary_assignment = []
	
	# Get salary structure dynamically
	salary_structure = sa.salary_structure

	for d in sa.get("custom_salary_structure"):  # Assuming there's a child table named "projects"
		if d.project and d.salary_structure:
			projects_with_salary_assignment.append({
				"project": d.project,
				"salary_structure": salary_structure,  # Use dynamically fetched Salary Structure
				"salary_assignment": salary_structure_assignment.get("name")  # Return assignment name
			})

	return projects_with_salary_assignment


def create_salary_slips_for_employees(employees, args, publish_progress=True):
	payroll_entry = frappe.get_cached_doc("Payroll Entry", args.payroll_entry)
	delete_if_proj_salary_slip(args.payroll_entry)
	count = 0
	for emp in employees:
		args.update({"employee": emp})
		projects_with_salary_assignment = set_salary_structure_assignment(args, emp)

		if not projects_with_salary_assignment:
			frappe.msgprint(_("No projects found for Employee {0}. Skipping salary slip.").format(emp))
			continue

		for project_data in projects_with_salary_assignment:
			salary_slip_args = args.copy()
			salary_slip_args.update({
				"doctype": "Salary Slip Project Wise",
				"project": project_data["project"],
				"salary_structure": project_data["salary_structure"],
				"salary_assignment": project_data["salary_assignment"]
			})
			frappe.get_doc(salary_slip_args).insert()
			count += 1
			if publish_progress:
				frappe.publish_progress(
					count * 100 / (len(employees) * len(projects_with_salary_assignment)),
					title=_("Creating Salary Slips..."),
				)

	payroll_entry.db_set({"status": "Submitted", "salary_slips_created": 1, "error_message": ""})
	create_consolidated_salary_slips(employees, args)
	frappe.publish_realtime("completed_salary_slip_creation", user=frappe.session.user)
	
def delete_if_proj_salary_slip(payroll):
    sql = """SELECT name FROM `tabSalary Slip Project Wise` WHERE payroll_entry="{0}" """.format(payroll)
    data = frappe.db.sql(sql, as_dict=True)

    for d in data:
        doc = frappe.get_doc("Salary Slip Project Wise", d.name)
        
        # Cancel first if it's submitted
        if doc.docstatus == 1:
            doc.cancel()

        # Delete the document
        doc.delete()


def create_consolidated_salary_slips(employees, args, publish_progress=True):
	payroll_entry = frappe.get_cached_doc("Payroll Entry", args.payroll_entry)

	try:
		salary_slips_exist_for = get_existing_salary_slips(employees, args)
		count = 0

		employees = list(set(employees) - set(salary_slips_exist_for))
		for emp in employees:
			args.update({"doctype": "Salary Slip", "employee": emp})
			salaryslip = frappe.get_doc(args).insert()

			earnings = frappe.db.sql("""
				SELECT salary_component, SUM(amount) as total_amount
				FROM `tabSalary Detail`
				WHERE parent IN (SELECT name FROM `tabSalary Slip Project Wise` WHERE payroll_entry = %s AND employee = %s)
				AND parentfield = 'earnings'
				GROUP BY salary_component
			""", (args.payroll_entry, emp), as_dict=True)

			deductions = frappe.db.sql("""
				SELECT salary_component, SUM(amount) as total_amount
				FROM `tabSalary Detail`
				WHERE parent IN (SELECT name FROM `tabSalary Slip Project Wise` WHERE payroll_entry = %s AND employee = %s)
				AND parentfield = 'deductions'
				GROUP BY salary_component
			""", (args.payroll_entry, emp), as_dict=True)

			# Add earnings
			for earn in earnings:
				salaryslip.append("earnings", {
					"salary_component": earn["salary_component"],
					"amount": earn["total_amount"]
				})

			# Add deductions
			for deduct in deductions:
				salaryslip.append("deductions", {
					"salary_component": deduct["salary_component"],
					"amount": deduct["total_amount"]
				})

			salaryslip.save()

			count += 1
			if publish_progress:
				frappe.publish_progress(
					count * 100 / len(employees),
					title=_("Creating Salary Slips..."),
				)

		payroll_entry.db_set({"status": "Submitted", "salary_slips_created": 1, "error_message": ""})

		if salary_slips_exist_for:
			frappe.msgprint(
				_(
					"Salary Slips already exist for employees {}, and will not be processed by this payroll."
				).format(frappe.bold(", ".join(emp for emp in salary_slips_exist_for))),
				title=_("Message"),
				indicator="orange",
			)

	except Exception as e:
		frappe.db.rollback()
		log_payroll_failure("creation", payroll_entry, e)

	finally:
		frappe.db.commit()  # nosemgrep
		frappe.publish_realtime("completed_salary_slip_creation", user=frappe.session.user)


# def create_consolidated_salary_slips(employees, args, publish_progress=True):
#     payroll_entry = frappe.get_cached_doc("Payroll Entry", args.payroll_entry)
#     count = 0

#     for emp in employees:
#         salary_slip = frappe.get_doc({
#             "doctype": "Salary Slip",
#             "employee": emp,
#             "payroll_entry": args.payroll_entry,
#             "start_date": args.start_date,
#             "end_date": args.end_date,
#             "currency": args.currency,
#             "salary_slip_based_on_timesheet": args.salary_slip_based_on_timesheet,
#             "deduct_tax_for_unclaimed_employee_benefits": args.deduct_tax_for_unclaimed_employee_benefits,
#             "remarks": "Consolidated Salary Slip Across All Projects"
#         })

#         # Fetch earnings and deductions
#         earnings = frappe.db.sql("""
#             SELECT salary_component, SUM(amount) as total_amount
#             FROM `tabSalary Detail`
#             WHERE parent IN (SELECT name FROM `tabSalary Slip Project Wise` WHERE payroll_entry = %s AND employee = %s)
#             AND parentfield = 'earnings'
#             GROUP BY salary_component
#         """, (args.payroll_entry, emp), as_dict=True)

#         deductions = frappe.db.sql("""
#             SELECT salary_component, SUM(amount) as total_amount
#             FROM `tabSalary Detail`
#             WHERE parent IN (SELECT name FROM `tabSalary Slip Project Wise` WHERE payroll_entry = %s AND employee = %s)
#             AND parentfield = 'deductions'
#             GROUP BY salary_component
#         """, (args.payroll_entry, emp), as_dict=True)

#         # Add earnings
#         for earn in earnings:
#             salary_slip.append("earnings", {
#                 "salary_component": earn["salary_component"],
#                 "amount": earn["total_amount"]
#             })

#         # Add deductions
#         for deduct in deductions:
#             salary_slip.append("deductions", {
#                 "salary_component": deduct["salary_component"],
#                 "amount": deduct["total_amount"]
#             })

#         # Calculate net pay
#         salary_slip.calculate_net_pay()
#         salary_slip.insert()
#         count += 1

#         if publish_progress:
#             frappe.publish_progress(
#                 count * 100 / len(employees),
#                 title=_("Creating Consolidated Salary Slips...")
#             )

#     payroll_entry.db_set({"status": "Submitted", "salary_slips_created": 1, "error_message": ""})
#     frappe.publish_realtime("completed_salary_slip_creation", user=frappe.session.user)
