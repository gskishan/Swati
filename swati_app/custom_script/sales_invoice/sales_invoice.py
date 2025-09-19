import frappe
from datetime import datetime

def before_save(doc, method):
    if doc.posting_date:
        posting_date = datetime.strptime(str(doc.posting_date), "%Y-%m-%d")
        year = posting_date.year
        month = posting_date.month

        if month >= 4:
            fy = str(year + 1)[-2:]   # e.g. 2025-26 -> 26
        else:
            fy = str(year)[-2:]       # e.g. 2026-27 -> 27

        doc.custom_fy = fy
