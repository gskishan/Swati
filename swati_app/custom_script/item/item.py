import frappe


@frappe.whitelist()
def get_next_item_code(custom_type, custom_category, custom_subcategory):
	prefix = "{0}-{1}-{2}-".format(
		custom_type.strip(), custom_category.strip(), custom_subcategory.strip()
	)
	existing = frappe.get_all(
		"Item",
		filters={"item_code": ["like", prefix + "%"]},
		pluck="item_code"
	)
	max_count = 0
	for code in existing:
		suffix = code[len(prefix):]
		if suffix.isdigit():
			max_count = max(max_count, int(suffix))
	return "{0}{1:04d}".format(prefix, max_count + 1)


def validate(doc, method):
    duplicate = frappe.db.exists(
        "Item",
        {
            "item_name": doc.item_name,
            "name": ["!=", doc.name]
        }
    )

    if duplicate:
        frappe.throw(
            f"Item Name <b>{doc.item_name}</b> already exists ({duplicate}). Please use a unique Item Name."
        )