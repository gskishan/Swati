from frappe.utils import today, getdate

def validate(self, method):
    if self.date and self.date < getdate(today()):
        frappe.throw(_("Backdated dates are not allowed. The date must be today or later."))
