import frappe
from frappe import _
from hrms.payroll.doctype.salary_slip.salary_slip import SalarySlip
from hrms.payroll.doctype.salary_structure.salary_structure import make_salary_slip
from frappe.utils import flt, getdate
from hrms.hr.report.monthly_attendance_sheet.monthly_attendance_sheet import get_entry_exits_summary
import json
from hrms.hr.utils import validate_active_employee
from datetime import datetime, timedelta





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
        self.calculate_ot()
        self.calculate_net_pay()
        self.set_totals()
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
        self.custom_ot_count=ot
        # Ensure overtime exists
        if ot <= 0:
            return

        # Calculate base net pay excluding overtime
        net_pay = calculate_net_pay_custom(self)
        existing_ot_entry = None

        # Calculate OT amount
        OT_Amount = (net_pay / self.payment_days) * ot
        for d in self.earnings:
            if d.salary_component == component:
                d.amount=OT_Amount
                existing_ot_entry = d
                break  # Stop loop once we find the OT component

        # If OT component already exists, do nothing
        if existing_ot_entry:
            return


        # Append OT component only if it doesn't exist
        ot_component = self.append("earnings", {})
        ot_component.salary_component = component
        ot_component.amount = OT_Amount





def calculate_overtime(employee, start_date, end_date):
    """
    Calculate overtime for an employee within a date range based on 'custom_from' and 'custom_till' fields.
    """

    # Fetch OT rules from Payroll Settings  custom added fields 
    payroll_settings = frappe.get_single("Payroll Settings")

    # Ensure OT settings exist
    if not payroll_settings.custom_half_ot_hours or not payroll_settings.custom_full_ot_hours:
        frappe.throw("OT hours range not set in Payroll Settings.")

    # Convert OT rules from string to integer range
    try:
        half_ot_min, half_ot_max = map(int, payroll_settings.custom_half_ot_hours.replace("–", "-").split("-"))
        full_ot_min, full_ot_max = map(int, payroll_settings.custom_full_ot_hours.replace("–", "-").split("-"))
    except ValueError:
        frappe.throw("Invalid OT hours format in Payroll Settings. Use a valid format like '4-5'.")

    # Default regular working hours
    regular_hours = payroll_settings.custom_shift_working_hours

    # Fetch attendance records
    attendance_records = frappe.db.sql("""
        SELECT custom_from as from_time, custom_till as till_time
        FROM `tabAttendance`
        WHERE employee = %s 
        AND attendance_date BETWEEN %s AND %s
    """, (employee, start_date, end_date), as_dict=True)

    total_ot = 0

    # Calculate OT based on working hours
    for record in attendance_records:
        from_time = record["from_time"]
        till_time = record["till_time"]

        #  Skip if time data is missing
        if not from_time or not till_time:
            continue  

        #  Convert to `time` object
        try:
            from_time = datetime.strptime(str(from_time), "%H:%M:%S").time()
            till_time = datetime.strptime(str(till_time), "%H:%M:%S").time()
        except ValueError:
            frappe.throw(f"Invalid time format in Attendance: {from_time} - {till_time}")

        #  Handle Overnight Shifts (e.g., 9 PM - 2 AM)
        if till_time < from_time:
            till_datetime = datetime.combine(datetime.today() + timedelta(days=1), till_time)
        else:
            till_datetime = datetime.combine(datetime.today(), till_time)

        from_datetime = datetime.combine(datetime.today(), from_time)
        hours_worked = (till_datetime - from_datetime).total_seconds() / 3600  # Convert seconds to hours

        # Subtract regular working hours
        extra_hours = max(hours_worked - regular_hours, 0)  # Ensure it doesn't go negative


        #  Apply OT rules
        if half_ot_min <= extra_hours <= half_ot_max:
            total_ot += 0.5
        elif full_ot_min <= extra_hours <= full_ot_max:
            total_ot += 1

            
        elif extra_hours > full_ot_max:  # Catch cases where hours exceed full OT limit
            total_ot += 1



    return total_ot, payroll_settings.custom_ot_component


def calculate_net_pay_custom(self):
    """
    Calculate total earnings, total deductions, and net pay for the Salary Slip.

    :param self: The Salary Slip document (Frappe DocType)
    :return: Dictionary containing total earnings, total deductions, and net pay
    """

    # Fetch earnings and deductions from the Salary Slip
    earnings = self.earnings or []
    deductions = self.deductions or []

    # Calculate totals
    total_earnings = sum(component.amount for component in earnings if component.amount)
    total_deductions = sum(component.amount for component in deductions if component.amount)

    # Calculate net pay
    net_pay = total_earnings - total_deductions

    return  net_pay