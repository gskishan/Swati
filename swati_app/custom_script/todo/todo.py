import frappe
from frappe import _
from frappe.utils import nowdate

def validate(self, method):
    if self.date and self.date < nowdate():
        frappe.throw(_("Backdated Date are not allowed. The date must be today or later."))
