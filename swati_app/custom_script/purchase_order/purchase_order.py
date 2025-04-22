import frappe

def validate(doc, method):
    workflow_name = frappe.db.get_value("Workflow", {"document_type": "Purchase Order", "is_active": 1}, "name")
    if workflow_name and doc.workflow_state:
        transitions = frappe.get_all("Workflow Transition",
        filters={"parent": workflow_name, "next_state": doc.workflow_state},
        fields=["allowed"])
        if transitions:
            roles = list(set(t["allowed"] for t in transitions if t["allowed"]))
            doc.custom_workflow_role = ",".join(roles)  # Join roles into a comma-separated string

   