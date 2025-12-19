from frappe.utils import today, getdate
import frappe
from frappe import _


def validate(self, method):
    if self.date and self.date < getdate(today()):
        pass
        #frappe.throw(_("Backdated dates are not allowed in Todo. The date must be today or later."))
