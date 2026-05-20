frappe.ui.form.on('Quotation Item', {
    qty: function(frm, cdt, cdn) {
        calculate_custom_purchase_amount(frm, cdt, cdn);
    },
    rate: function(frm, cdt, cdn) {
        calculate_custom_purchase_amount(frm, cdt, cdn);
    },
    amount: function(frm, cdt, cdn) {
        calculate_custom_purchase_amount(frm, cdt, cdn);
    },
    items_add: function(frm, cdt, cdn) {
        calculate_custom_purchase_amount(frm, cdt, cdn);
    },
    items_remove: function(frm) {
        calculate_custom_total_purchase(frm);
    },
    custom_purchase_amount: function(frm, cdt, cdn) {
        calculate_custom_total_purchase(frm);
    }
});

function calculate_custom_purchase_amount(frm, cdt, cdn) {
    var row = locals[cdt][cdn];
    var amount = (row.qty || 0) * (row.rate || 0);
    frappe.model.set_value(cdt, cdn, 'custom_purchase_amount', amount);
}

function calculate_custom_total_purchase(frm) {
    var total = 0;
    (frm.doc.items || []).forEach(function(row) {
        total += (row.custom_purchase_amount || 0);
    });
    frm.set_value('custom_total_purchase', total);
}