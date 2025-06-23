frappe.ui.form.on('Opportunity', {
    refresh: function(frm) {
    frm.add_custom_button('Bid', () => {
    frappe.model.with_doctype('Bid', function() {
                   var bid = frappe.model.get_new_doc('Bid');
   
                   // Copy fields from Opportunity
                   bid.opportunity_from = "Lead";
                   bid.party_name = frm.doc.party_name;
                   bid.customer_name = frm.doc.customer_name;
                   bid.opportunity_type = frm.doc.opportunity_type;
                   bid.status = "Open";  // Default status
                   bid.source=frm.doc.source;
                   bid.opportunity_owner =frm.doc.opportunity_owner;
                   bid.sales_stage =frm.doc.sales_stage;
                   bid.expected_closing =frm.doc.expected_closing;
                   bid.probability =frm.doc.probability;
                   bid.custom_design_recieved =frm.doc.custom_design_recieved;
                   bid.custom_date_of_entry =frm.doc.custom_date_of_entry;
                   bid.custom_lead_title =frm.doc.custom_lead_title;
                   bid.custom_lead_type =frm.doc.custom_lead_type;
                   bid.custom_site_address =frm.doc.custom_site_address;
                   bid.custom_short_description =frm.doc.custom_short_description;
                   bid.custom_estimated_price =frm.doc.custom_estimated_price;
                   bid.custom_win_probability =frm.doc.custom_win_probability;
                   bid.custom_submission_date =frm.doc.custom_submission_date;
                   bid.custom_delivery_period =frm.doc.custom_delivery_period;
                   bid.custom_bid_manager =frm.doc.custom_bid_manager;
                   bid.custom_sales_person =frm.doc.custom_sales_person;
                   bid.custom_project_manager =frm.doc.custom_project_manager;
                   bid.custom_customer_last_contacted_date =frm.doc.custom_customer_last_contacted_date;
                   bid.custom_next_followup_date =frm.doc.custom_next_followup_date;
                   bid.custom_bidno_bid =frm.doc.custom_bidno_bid;
                   bid.opportunity = frm.doc.name;
                   bid.custom_win__loss__cancelled =frm.doc.custom_win__loss__cancelled;
                   bid.custom_reason_for_loss =frm.doc.custom_reason_for_loss;
                   bid.custom_remarks =frm.doc.custom_remarks;
                   bid.no_of_employees =frm.doc.no_of_employees;
                   bid.annual_revenue =frm.doc.annual_revenue;
                   bid.customer_group =frm.doc.customer_group;
                   bid.industry =frm.doc.industry;
                   bid.market_segment =frm.doc.market_segment;
                   bid.website =frm.doc.website;
                   bid.city =frm.doc.city;
                   bid.state =frm.doc.state;
                   bid.country =frm.doc.country;
                   bid.territory =frm.doc.territory;
                   bid.currency =frm.doc.currency;
                   bid.conversion_rate =frm.doc.conversion_rate;
                   bid.opportunity_amount =frm.doc.opportunity_amount;
                   bid.base_opportunity_amount =frm.doc.base_opportunity_amount;
                   bid.company =frm.doc.company;
                   bid.transaction_date =frm.doc.transaction_date;
                   bid.lost_reasons =frm.doc.lost_reasons;
                   bid.order_lost_reason =frm.doc.order_lost_reason;
                   bid.campaign =frm.doc.campaign;
                   bid.title =frm.doc.title;
                   bid.competitors =frm.doc.competitors;
                   bid.contact_person =frm.doc.contact_person;
                   bid.job_title =frm.doc.job_title;
                   bid.contact_email =frm.doc.contact_email;
                   bid.contact_mobile =frm.doc.contact_mobile;
                   bid.whatsapp =frm.doc.whatsapp;
                   bid.phone =frm.doc.phone;
                   bid.phone_ext =frm.doc.phone_ext;
                   bid.address_html =frm.doc.address_html;
                   bid.customer_address =frm.doc.customer_address;
                   bid.address_display =frm.doc.address_display;
                   bid.contact_html =frm.doc.contact_html;
                   bid.contact_display =frm.doc.contact_display;
                   bid.base_total =frm.doc.base_total;
                   bid.total =frm.doc.total;
                   bid.open_activities_html =frm.doc.open_activities_html;
                   bid.all_activities_html =frm.doc.all_activities_html;
                   bid.notes_html =frm.doc.notes_html;
                   bid.notes =frm.doc.notes;
                   // Copy items if available
                   if (frm.doc.items) {
                       bid.items = frm.doc.items.map(item => ({
                           item_code: item.item_code,
                           item_name: item.item_name,
                           qty: item.qty,
                           rate: item.rate,
                           uom:item.uom,
                           brand:item.brand,
                           item_group:item.item_group,
                           description:item.description,
                           image:item.image,
                           image_view:item.image_view,
                           base_rate:item.base_rate,
                           base_amount:item.base_amount,
                           amount:item.amount,
                       }));
                   }
   
                   // Open new form with pre-filled data
                   frappe.set_route("Form", "Bid", bid.name);
               });
   },__("Create"));
           if (frm.doc.opportunity_from == "Lead") {  // Ensure field name is correct
               frappe.db.get_value("Lead", { "name": frm.doc.party_name }, "type")
                   .then(r => {
                       if (r.message && r.message.type) {
                           frm.set_value('custom_lead_type', r.message.type);
                       }
                   });
           }
    }
   });