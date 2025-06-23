frappe.ui.form.on('Material Request Item', {
    custom_create_task: function (frm, cdt, cdn) {
            let row = locals[cdt][cdn];
        
            let dialog = new frappe.ui.Dialog({
                title: "Enter Details",
                fields: [
                    {
                        label: "Is Group",
                        fieldname: "is_group",
                        fieldtype: "Check"
                    },
                    {
                        label: "Subject",
                        fieldname: "subject",
                        fieldtype: "Data"
                    },
                    {
                        label: "Expected Completed Date",
                        fieldname: "expected_completed_date",
                        fieldtype: "Date"
                    }
                ],
                primary_action_label: "Create Task",
                primary_action: function (data) {
                    
                    if (!data.subject) {
                        frappe.msgprint("Subject is required to create a task.");
                        return;
                    }
        
                    let task_data = {
                        doctype: "Task",
                        subject: data.subject,
                        is_group: data.is_group ? 1 : 0,
                        custom_material_request: frm.doc.name,
                        custom_task_item: [
                            {
                                item_code: row.item_code,
                                qty: row.qty,
                                
                            }
                        ]
                    };
    
                    frappe.call({
                        method: "frappe.client.insert",
                        args: { doc: task_data },
                        callback: function (r) {
                            if (!r.exc) {
                                frappe.msgprint(`Task created successfully: ${r.message.name}`);
                                dialog.hide();
                            } else {
                                frappe.msgprint(`Error creating Task`);
                            }
                        }
                    });
                }
            });
        
            // Show the dialog
            dialog.show();
        }
    })