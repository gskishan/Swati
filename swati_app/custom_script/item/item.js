frappe.ui.form.on('Item', {
	custom_type: function(frm) {
		generate_item_code(frm);
	},
	custom_category: function(frm) {
		generate_item_code(frm);
	},
	custom_subcategory: function(frm) {
		generate_item_code(frm);
	}
});

function generate_item_code(frm) {
	if (!frm.is_new()) return;

	if (frm.doc.custom_type && frm.doc.custom_category && frm.doc.custom_subcategory) {
		frappe.call({
			method: 'swati_app.custom_script.item.item.get_next_item_code',
			args: {
				custom_type: frm.doc.custom_type,
				custom_category: frm.doc.custom_category,
				custom_subcategory: frm.doc.custom_subcategory
			},
			callback: function(r) {
				if (r.message) {
					frm.set_value('item_code', r.message);
				}
			}
		});
	} else {
		// Clear if any part is removed
		frm.set_value('item_code', '');
	}
}