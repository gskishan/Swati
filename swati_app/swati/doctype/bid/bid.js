// Copyright (c) 2025, CRUXEDGE and contributors
// For license information, please see license.txt

frappe.ui.form.on('Bid', {
    refresh: function(frm) {
        if (frm.doc.docstatus == 1){
        frm.add_custom_button('Quotation', () => {
            frappe.model.with_doctype('Quotation', function() {
                let quotation = frappe.model.get_new_doc('Quotation');

                // Copy fields from Bid
                quotation.quotation_to = "Lead";
                quotation.party_name = frm.doc.party_name;
                quotation.contact_person = frm.doc.contact_person ;
                quotation.customer_address = frm.doc.custom_site_address;

                // Copy items if available
                if (frm.doc.items && frm.doc.items.length) {
                    quotation.items = [];
                    frm.doc.items.forEach(item => {
                        let new_item = frappe.model.add_child(quotation, "Quotation Item", "items");
                        Object.assign(new_item, {
                            item_code: item.item_code,
                            item_name: item.item_name,
                            qty: item.qty,
                            rate: item.rate,
                            uom: item.uom,
                            brand: item.brand,
                            item_group: item.item_group,
                            description: item.description,
                            image: item.image,
                            image_view: item.image_view,
                            base_rate: item.base_rate,
                            base_amount: item.base_amount,
                            amount: item.amount,
                            prevdoc_doctype: "Opportunity",
                            prevdoc_docname: frm.doc.opportunity,
                            custom_against_bid:frm.doc.name,
                            
                        });
                    });
                }

                // Open new form with pre-filled data
                frappe.set_route("Form", "Quotation", quotation.name);
            });
        }, __("Create"));
        frm.add_custom_button('Sales Order', () => {
            frappe.model.with_doctype('Sales Order', function() {
                let sales_order = frappe.model.get_new_doc('Sales Order');
        
                // Copy fields from Bid
                sales_order.contact_person = frm.doc.contact_person;
                sales_order.customer_address = frm.doc.custom_site_address;
        
                // Copy items if available
                if (frm.doc.items && frm.doc.items.length) {
                    sales_order.items = [];
                    frm.doc.items.forEach(item => {
                        let new_item = frappe.model.add_child(sales_order, "Sales Order Item", "items");
                        Object.assign(new_item, {
                            item_code: item.item_code,
                            item_name: item.item_name,
                            qty: item.qty,
                            rate: item.rate,
                            uom: item.uom,
                            brand: item.brand,
                            item_group: item.item_group,
                            description: item.description,
                            image: item.image,
                            image_view: item.image_view,
                            base_rate: item.base_rate,
                            base_amount: item.base_amount,
                            amount: item.amount,
                            custom_against_bid: frm.doc.name
                        });
                    });
                }
        
                // Open new form with pre-filled data
                frappe.set_route("Form", "Sales Order", sales_order.name);
            });
        }, __("Create"));
        
    }
    }
});

