import frappe
from frappe import _
from hrms.payroll.doctype.salary_slip.salary_slip import SalarySlip
from hrms.payroll.doctype.salary_structure.salary_structure import make_salary_slip
from frappe.utils import flt, getdate
from hrms.hr.report.monthly_attendance_sheet.monthly_attendance_sheet import get_entry_exits_summary
import json
from hrms.hr.utils import validate_active_employee

from datetime import datetime



class CustomSalarySlip(SalarySlip):
    def validate(self):
        self.check_salary_withholding()
        self.status = self.get_status()
        validate_active_employee(self.employee)
        self.validate_dates()
        self.check_existing()

        if self.payroll_frequency:
            self.get_date_details()

        if not (len(self.get("earnings")) or len(self.get("deductions"))):
            # get details from salary structure
            self.get_emp_and_working_day_details()
        else:
            self.get_working_days_details(lwp=self.leave_without_pay)

        self.set_salary_structure_assignment()
        self.calculate_net_pay()
        self.add_calculate_ot()
        self.calculate_net_pay()
        self.compute_year_to_date()
        self.compute_month_to_date()
        self.compute_component_wise_year_to_date()

        self.add_leave_balances()

        max_working_hours = frappe.db.get_single_value(
            "Payroll Settings", "max_working_hours_against_timesheet"
        )
        if max_working_hours:
            if self.salary_slip_based_on_timesheet and (self.total_working_hours > int(max_working_hours)):
                frappe.msgprint(
                    _("Total working hours should not be greater than max working hours {0}").format(
                        max_working_hours
                    ),
                    alert=True,
                )


def calculate_ot(self):
    ot, component = calculate_overtime(self.employee, self.start_date, self.end_date)
    
    # Ensure overtime exists
    if ot <= 0:
        return

    # Calculate base net pay excluding overtime
    net_pay = self.net_pay
    existing_ot_entry = None

    for d in self.earnings:
        if d.salary_component == component:
            existing_ot_entry = d
            break  # Stop loop once we find the OT component

    # If OT component already exists, do nothing
    if existing_ot_entry:
        return

    # Calculate OT amount
    OT_Amount = (net_pay / self.payment_days) * ot

    # Append OT component only if it doesn't exist
    ot_component = self.append("earnings", {})
    ot_component.salary_component = component
    ot_component.amount = OT_Amount





def calculate_overtime(employee, start_date, end_date):
    """
    Calculate overtime for a given employee within a date range using 'from' and 'till' fields.
    """

    # Fetch OT rules from Payroll Settings
    payroll_settings = frappe.get_single("Payroll Settings")
    half_ot_hours_range = payroll_settings.half_ot_hours.split("-")  # Example: "11-12"
    full_ot_hours_range = payroll_settings.full_ot_hours.split("-")  # Example: "15-16"

    half_ot_min, half_ot_max = int(half_ot_hours_range[0]), int(half_ot_hours_range[1])
    full_ot_min, full_ot_max = int(full_ot_hours_range[0]), int(full_ot_hours_range[1])

    # Fetch attendance records (From and Till times in 24-hour format)
    attendance_records = frappe.db.sql("""
        SELECT custom_from from,custom_till till
        FROM `tabAttendance`
        WHERE employee = %s 
        AND attendance_date BETWEEN %s AND %s
    """, (employee, start_date, end_date), as_dict=True)

    total_ot = 0

    # Calculate OT based on working hours
    for record in attendance_records:
        from_time = datetime.strptime(record["from"], "%H:%M:%S")  # 24-hour format
        till_time = datetime.strptime(record["till"], "%H:%M:%S")  # 24-hour format

        # Calculate total working hours
        hours_worked = (till_time - from_time).total_seconds() / 3600  # Convert seconds to hours

        # Apply OT rules
        if half_ot_min <= hours_worked <= half_ot_max:
            total_ot += 0.5
        elif full_ot_min <= hours_worked <= full_ot_max:
            total_ot += 1


    return total_ot,payroll_settings.custom_ot_component

