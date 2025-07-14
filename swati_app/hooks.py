app_name = "swati_app"
app_title = "Swati"
app_publisher = "CRUXEDGE"
app_description = "airport service"
app_email = "ahmadsayyed66@gmail.com"
app_license = "mit"

# Apps
# ------------------

# required_apps = []

# Each item in the list will be shown as an app in the apps page
# add_to_apps_screen = [
# 	{
# 		"name": "swati_app",
# 		"logo": "/assets/swati_app/logo.png",
# 		"title": "Swati",
# 		"route": "/swati_app",
# 		"has_permission": "swati_app.api.permission.has_app_permission"
# 	}
# ]

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
# app_include_css = "/assets/swati_app/css/swati_app.css"
# app_include_js = "/assets/swati_app/js/swati_app.js"

# include js, css files in header of web template
# web_include_css = "/assets/swati_app/css/swati_app.css"
# web_include_js = "/assets/swati_app/js/swati_app.js"

# include custom scss in every website theme (without file extension ".scss")
# website_theme_scss = "swati_app/public/scss/website"

# include js, css files in header of web form
# webform_include_js = {"doctype": "public/js/doctype.js"}
# webform_include_css = {"doctype": "public/css/doctype.css"}

# include js in page
# page_js = {"page" : "public/js/file.js"}

# include js in doctype views
# doctype_js = {
#     "Opportunity" : "swati/custom_code/opportunity/opportunity.js",
#     "Material Request" : "swati/custom_code/material_request/material_request.js"
	# "Payment Entry" : "swati/custom_code/payment_entry/payment_entry.js",
    # }
# doctype_list_js = {"doctype" : "public/js/doctype_list.js"}
# doctype_tree_js = {"doctype" : "public/js/doctype_tree.js"}
# doctype_calendar_js = {"doctype" : "public/js/doctype_calendar.js"}

# Svg Icons
# ------------------
# include app icons in desk
# app_include_icons = "swati_app/public/icons.svg"

# Home Pages
# ----------

# application home page (will override Website Settings)
# home_page = "login"

# website user home page (by Role)
# role_home_page = {
# 	"Role": "home_page"
# }

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# Jinja
# ----------

# add methods and filters to jinja environment
# jinja = {
# 	"methods": "swati_app.utils.jinja_methods",
# 	"filters": "swati_app.utils.jinja_filters"
# }

# Installation
# ------------

# before_install = "swati_app.install.before_install"
# after_install = "swati_app.install.after_install"

# Uninstallation
# ------------

# before_uninstall = "swati_app.uninstall.before_uninstall"
# after_uninstall = "swati_app.uninstall.after_uninstall"

# Integration Setup
# ------------------
# To set up dependencies/integrations with other apps
# Name of the app being installed is passed as an argument

# before_app_install = "swati_app.utils.before_app_install"
# after_app_install = "swati_app.utils.after_app_install"

# Integration Cleanup
# -------------------
# To clean up dependencies/integrations with other apps
# Name of the app being uninstalled is passed as an argument

# before_app_uninstall = "swati_app.utils.before_app_uninstall"
# after_app_uninstall = "swati_app.utils.after_app_uninstall"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "swati_app.notifications.get_notification_config"

# Permissions
# -----------
# Permissions evaluated in scripted ways

# permission_query_conditions = {
# 	"Event": "frappe.desk.doctype.event.event.get_permission_query_conditions",
# }
#
# has_permission = {
# 	"Event": "frappe.desk.doctype.event.event.has_permission",
# }

# DocType Class
# ---------------
# Override standard doctype classes

override_doctype_class = {
    "Payroll Entry": "swati_app.custom_script.payroll_entry.payroll_entry.CustomPayrollEntry",
        "Salary Slip": "swati_app.custom_script.salary_slip.salary_slip.CustomSalarySlip",

}



# Document Events
# ---------------
# Hook on document methods and events

doc_events = {
	"Salary Structure Assignment": {
		"on_submit": "swati_app.custom_script.salary_structure_assignment.salary_structure_assignment.on_submit",
        "on_cancel": "swati_app.custom_script.salary_structure_assignment.salary_structure_assignment.on_cancel"

	
	},
    "Purchase Order": {
		"validate": "swati_app.custom_script.purchase_order.purchase_order.validate",

	
	},
    "Quotation": {
		"validate": "swati_app.custom_script.quotation.quotation.validate",

	
	},
    "Project": {
		"before_save": "swati_app.custom_script.project.project.update_expected_date",

	
	},
 "ToDo": {
                "validate": "swati_app.custom_script.todo.todo.validate",
 }
}
fixtures = ["Client Script"]
# Scheduled Tasks
# ---------------

scheduler_events = {
# 	"all": [
# 		"swati_app.tasks.all"
# 	],
	"daily": [
		"swati_app.custom_script.project.project.move_expired_users"
	],
# 	"hourly": [
# 		"swati_app.tasks.hourly"
# 	],
# 	"weekly": [
# 		"swati_app.tasks.weekly"
# 	],
# 	"monthly": [
# 		"swati_app.tasks.monthly"
# 	],
}

# Testing
# -------

# before_tests = "swati_app.install.before_tests"

# Overriding Methods
# ------------------------------
#
# override_whitelisted_methods = {
# 	"frappe.desk.doctype.event.event.get_events": "swati_app.event.get_events"
# }
#
# each overriding function accepts a `data` argument;
# generated from the base implementation of the doctype dashboard,
# along with any modifications made in other Frappe apps
# override_doctype_dashboards = {
# 	"Task": "swati_app.task.get_dashboard_data"
# }

# exempt linked doctypes from being automatically cancelled
#
# auto_cancel_exempted_doctypes = ["Auto Repeat"]

# Ignore links to specified DocTypes when deleting documents
# -----------------------------------------------------------

# ignore_links_on_delete = ["Communication", "ToDo"]

# Request Events
# ----------------
# before_request = ["swati_app.utils.before_request"]
# after_request = ["swati_app.utils.after_request"]

# Job Events
# ----------
# before_job = ["swati_app.utils.before_job"]
# after_job = ["swati_app.utils.after_job"]

# User Data Protection
# --------------------

# user_data_fields = [
# 	{
# 		"doctype": "{doctype_1}",
# 		"filter_by": "{filter_by}",
# 		"redact_fields": ["{field_1}", "{field_2}"],
# 		"partial": 1,
# 	},
# 	{
# 		"doctype": "{doctype_2}",
# 		"filter_by": "{filter_by}",
# 		"partial": 1,
# 	},
# 	{
# 		"doctype": "{doctype_3}",
# 		"strict": False,
# 	},
# 	{
# 		"doctype": "{doctype_4}"
# 	}
# ]

# Authentication and authorization
# --------------------------------

# auth_hooks = [
# 	"swati_app.auth.validate"
# ]

# Automatically update python controller files with type annotations for this app.
# export_python_type_annotations = True

# default_log_clearing_doctypes = {
# 	"Logging DocType Name": 30  # days to retain logs
# }

