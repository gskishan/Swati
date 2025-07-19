# Copyright (c) 2025, CRUXEDGE and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class Bid(Document):
    def before_save(self):
        if not self.opportunity:
            return
        frappe.db.set_value("Opportunity",self.opportunity,"custom_bid",self.name)
