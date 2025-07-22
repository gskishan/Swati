# Copyright (c) 2025, CRUXEDGE and contributors
# For license information, please see license.txt
import frappe
from datetime import datetime, timedelta

def execute(filters=None):
    if not filters or not (filters.get("from_date") and filters.get("to_date")):
        frappe.throw("Please set both From Date and To Date.")

    employee_filter = {}
    if filters.get("employee"):
        employee_filter["name"] = filters["employee"]

    employees = frappe.get_all("Employee", fields=["name", "employee_name", "department", "designation"], filters=employee_filter)

    data = []
    for emp in employees:
        project_wise_ot = calculate_overtime_by_project(
            emp.name,
            filters["from_date"],
            filters["to_date"],
            filters.get("project")  # may be None
        )

        for project, total_ot in project_wise_ot.items():
            data.append({
                "employee": emp.name,
                "employee_name": emp.employee_name,
                "department": emp.department,
                "designation": emp.designation,
                "project": project or "Not Set",
                "total_ot": total_ot
            })

    return get_columns(), data


def calculate_overtime_by_project(employee, start_date, end_date, filter_project=None):
    payroll_settings = frappe.get_single("Payroll Settings")

    if not payroll_settings.custom_half_ot_hours or not payroll_settings.custom_full_ot_hours:
        frappe.throw("OT hours range not set in Payroll Settings.")

    try:
        half_ot_min, half_ot_max = map(int, payroll_settings.custom_half_ot_hours.replace("–", "-").split("-"))
        full_ot_min, full_ot_max = map(int, payroll_settings.custom_full_ot_hours.replace("–", "-").split("-"))
    except ValueError:
        frappe.throw("Invalid OT hours format in Payroll Settings. Use format like '4-5'.")

    regular_hours = payroll_settings.custom_shift_working_hours or 9

    # Optional project filter
    project_condition = "AND custom_project = %s" if filter_project else ""
    args = [employee, start_date, end_date]
    if filter_project:
        args.append(filter_project)

    attendance_records = frappe.db.sql(f"""
        SELECT custom_from as from_time, custom_till as till_time, custom_project
        FROM `tabAttendance`
        WHERE employee = %s 
        AND attendance_date BETWEEN %s AND %s
        {project_condition}
    """, tuple(args), as_dict=True)

    project_wise_ot = {}

    for record in attendance_records:
        from_time = record["from_time"]
        till_time = record["till_time"]
        project = record["custom_project"]

        if not from_time or not till_time:
            continue

        try:
            from_time = datetime.strptime(str(from_time), "%H:%M:%S").time()
            till_time = datetime.strptime(str(till_time), "%H:%M:%S").time()
        except ValueError:
            frappe.throw(f"Invalid time format in Attendance: {from_time} - {till_time}")

        if till_time < from_time:
            till_datetime = datetime.combine(datetime.today() + timedelta(days=1), till_time)
        else:
            till_datetime = datetime.combine(datetime.today(), till_time)

        from_datetime = datetime.combine(datetime.today(), from_time)
        hours_worked = (till_datetime - from_datetime).total_seconds() / 3600

        extra_hours = max(hours_worked - regular_hours, 0)

        ot_hours = 0
        if half_ot_min <= extra_hours <= half_ot_max:
            ot_hours = 0.5
        elif full_ot_min <= extra_hours <= full_ot_max:
            ot_hours = 1
        elif extra_hours > full_ot_max:
            ot_hours = 1

        if ot_hours:
            project_key = project or None
            project_wise_ot[project_key] = project_wise_ot.get(project_key, 0) + ot_hours

    return project_wise_ot


def get_columns():
    return [
        {"label": "Employee ID", "fieldname": "employee", "fieldtype": "Link", "options": "Employee", "width": 120},
        {"label": "Employee Name", "fieldname": "employee_name", "fieldtype": "Data", "width": 150},
        {"label": "Department", "fieldname": "department", "fieldtype": "Link", "options": "Department", "width": 120},
        {"label": "Designation", "fieldname": "designation", "fieldtype": "Link", "options": "Designation", "width": 120},
        {"label": "Project", "fieldname": "project", "fieldtype": "Link", "options": "Project", "width": 140},
        {"label": "Total OT", "fieldname": "total_ot", "fieldtype": "Float", "width": 100}
    ]

