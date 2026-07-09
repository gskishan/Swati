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
	return "{0}{1:03d}".format(prefix, max_count + 1)