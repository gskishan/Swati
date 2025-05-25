frappe.ui.form.on('Payment Entry', {
    custom_get_outstanding_project_wise_invoice: function (frm) {
        if (frm.doc.payment_type == "Receive") {
            let dialog = new frappe.ui.Dialog({
                title: __('Filters'),
                fields: [
                    { fieldname: 'from_date', label: __('From Date'), fieldtype: 'Date' },
                    { fieldname: 'to_date', label: __('To Date'), fieldtype: 'Date' },
                    { fieldname: 'project', label: __('Project'), fieldtype: 'Link', options: 'Project' },
                    { fieldname: 'cost_center', label: __('Cost Center'), fieldtype: 'Link', options: 'Cost Center' },
                    { fieldname: 'allocate_payment_amount', label: __('Allocate Payment Amount'), fieldtype: 'Check', default: 1 }
                ],
                primary_action_label: __('Get Invoices'),
                primary_action: function (values) {
                    frappe.call({
                        method: "swati_app.custom_script.payment_entry.payment_entry.get_outstanding_sales_invoices",
                        args: {
                            company: frm.doc.company,
                            party_type: frm.doc.party_type,
                            party: frm.doc.party,
                            posting_date: frm.doc.posting_date,
                            project: values.project,
                            cost_center: values.cost_center
                        },
                        callback: function (r) {
                            if (r.message && r.message.length) {
                                frm.clear_table("references");

                                r.message.forEach(function (invoice) {
                                    frm.add_child("references", {
                                        reference_doctype: "Sales Invoice",
                                        reference_name: invoice.name,
                                        due_date: invoice.due_date,
                                        total_amount: invoice.grand_total || 0,
                                        outstanding_amount: invoice.outstanding_amount || 0,
                                        account: invoice.debit_to || 0,
                                        allocated_amount: values.allocate_payment_amount ? invoice.outstanding_amount : 0
                                    });
                      
                                });

                                frm.refresh_field("references");
                                frappe.msgprint(__("{0} invoices added to references table.", [r.message.length]));
                            } else {
                                frappe.msgprint(__('No outstanding invoices found.'));
                            }
                        }
                    });
                    dialog.hide();
                }
            });

            dialog.show();
        }
        
                if (frm.doc.payment_type == "Pay") {
                    let dialog = new frappe.ui.Dialog({
                        title: __('Filters'),
                        fields: [
                            { fieldname: 'from_date', label: __('From Date'), fieldtype: 'Date' },
                            { fieldname: 'to_date', label: __('To Date'), fieldtype: 'Date' },
                            { fieldname: 'project', label: __('Project'), fieldtype: 'Link', options: 'Project' },
                            { fieldname: 'cost_center', label: __('Cost Center'), fieldtype: 'Link', options: 'Cost Center' },
                            { fieldname: 'allocate_payment_amount', label: __('Allocate Payment Amount'), fieldtype: 'Check', default: 1 }
                        ],
                        primary_action_label: __('Get Invoices'),
                        primary_action: function (values) {
                            frappe.call({
                                method: "swati_app.custom_script.payment_entry.payment_entry.get_outstanding_purchase_invoices",
                                args: {
                                    company: frm.doc.company,
                                    party_type: frm.doc.party_type,
                                    party: frm.doc.party,
                                    posting_date: frm.doc.posting_date,
                                    project: values.project,
                                    cost_center: values.cost_center
                                },
                                callback: function (r) {
                                    if (r.message && r.message.length) {
                                        frm.clear_table("references");
        
                                        r.message.forEach(function (invoice) {
                                            frm.add_child("references", {
                                                reference_doctype: "Purchase Invoice",
                                                reference_name: invoice.name,
                                                due_date: invoice.due_date,
                                                total_amount: invoice.grand_total || 0,
                                                outstanding_amount: invoice.outstanding_amount || 0,
                                                bill_no :invoice.bill_no || 0,
                                                account: invoice.credit_to || 0,
                                                exchange_rate : invoice.conversion_rate || 0,
                                                allocated_amount: values.allocate_payment_amount ? invoice.outstanding_amount : 0
                                            });
                                        });
        
                                        frm.refresh_field("references");
                                        frappe.msgprint(__("{0} invoices added to references table.", [r.message.length]));
                                    } else {
                                        frappe.msgprint(__('No outstanding invoices found.'));
                                    }
                                }
                            });
                            dialog.hide();
                        }
                    });
        
                    dialog.show();
                } 
            },
                custom_get_outstanding_project_wise_order: function (frm) {
                    if (frm.doc.payment_type == "Receive") {
                        let dialog = new frappe.ui.Dialog({
                            title: __('Filters'),
                            fields: [
                                { fieldname: 'from_date', label: __('From Date'), fieldtype: 'Date' },
                                { fieldname: 'to_date', label: __('To Date'), fieldtype: 'Date' },
                                { fieldname: 'project', label: __('Project'), fieldtype: 'Link', options: 'Project' },
                                { fieldname: 'cost_center', label: __('Cost Center'), fieldtype: 'Link', options: 'Cost Center' },
                                { fieldname: 'allocate_payment_amount', label: __('Allocate Payment Amount'), fieldtype: 'Check', default: 1 }
                            ],
                            primary_action_label: __('Get Invoices'),
                            primary_action: function (values) {
                                frappe.call({
                                    method: "swati_app.custom_script.payment_entry.payment_entry.get_outstanding_sales_orders",
                                    args: {
                                        company: frm.doc.company,
                                        party_type: frm.doc.party_type,
                                        party: frm.doc.party,
                                        posting_date: frm.doc.posting_date,
                                        project: values.project,
                                        cost_center: values.cost_center
                                    },
                                    callback: function (r) {
                                        if (r.message && r.message.length) {
                                            frm.clear_table("references");
            
                                            r.message.forEach(function (invoice) {
                                                frm.add_child("references", {
                                                    reference_doctype: "Sales Order",
                                                    reference_name: invoice.name,
                                                    total_amount: invoice.grand_total || 0,
                                                    outstanding_amount: invoice.grand_total - invoice.advance_paid|| 0,
                                                    allocated_amount: values.allocate_payment_amount ? invoice.outstanding_amount : 0
                                                });
                                  
                                            });
            
                                            frm.refresh_field("references");
                                            frappe.msgprint(__("{0} invoices added to references table.", [r.message.length]));
                                        } else {
                                            frappe.msgprint(__('No outstanding invoices found.'));
                                        }
                                    }
                                });
                                dialog.hide();
                            }
                        });
            
                        dialog.show();
                    } 
                            if (frm.doc.payment_type == "Pay") {
                                let dialog = new frappe.ui.Dialog({
                                    title: __('Filters'),
                                    fields: [
                                        { fieldname: 'from_date', label: __('From Date'), fieldtype: 'Date' },
                                        { fieldname: 'to_date', label: __('To Date'), fieldtype: 'Date' },
                                        { fieldname: 'project', label: __('Project'), fieldtype: 'Link', options: 'Project' },
                                        { fieldname: 'cost_center', label: __('Cost Center'), fieldtype: 'Link', options: 'Cost Center' },
                                        { fieldname: 'allocate_payment_amount', label: __('Allocate Payment Amount'), fieldtype: 'Check', default: 1 }
                                    ],
                                    primary_action_label: __('Get Invoices'),
                                    primary_action: function (values) {
                                        frappe.call({
                                            method: "swati_app.custom_script.payment_entry.payment_entry.get_outstanding_purchase_orders",
                                            args: {
                                                company: frm.doc.company,
                                                party_type: frm.doc.party_type,
                                                party: frm.doc.party,
                                                posting_date: frm.doc.posting_date,
                                                project: values.project,
                                                cost_center: values.cost_center
                                            },
                                            callback: function (r) {
                                                if (r.message && r.message.length) {
                                                    frm.clear_table("references");
                    
                                                    r.message.forEach(function (invoice) {
                                                        frm.add_child("references", {
                                                            reference_doctype: "Purchase Order",
                                                            reference_name: invoice.name,
                                                            total_amount: invoice.grand_total || 0,
                                                            outstanding_amount: invoice.grand_total - invouce.advance_paid || 0,
                                                            exchange_rate : invoice.conversion_rate || 0,
                                                            allocated_amount: values.allocate_payment_amount ? invoice.outstanding_amount : 0
                                                        });
                                                    });
                    
                                                    frm.refresh_field("references");
                                                    frappe.msgprint(__("{0} invoices added to references table.", [r.message.length]));
                                                } else {
                                                    frappe.msgprint(__('No outstanding invoices found.'));
                                                }
                                            }
                                        });
                                        dialog.hide();
                                    }
                                });
                    
                                dialog.show();
                            } 
                        }
                    
                 
        });
     

