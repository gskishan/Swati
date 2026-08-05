frappe.ui.form.on("Issue", {
    custom_end_date_and_time: function(frm) {
        calculate_downtime(frm);
    },
    custom_start_date_and_time: function(frm) {
        calculate_downtime(frm);
    }
});

function calculate_downtime(frm) {
    if (frm.doc.custom_start_date_and_time && frm.doc.custom_end_date_and_time) {

        let start = frappe.datetime.str_to_obj(frm.doc.custom_start_date_and_time);
        let end = frappe.datetime.str_to_obj(frm.doc.custom_end_date_and_time);

        if (end >= start) {
            let diff_ms = end - start;

            let total_seconds = Math.floor(diff_ms / 1000);

            let hours = Math.floor(total_seconds / 3600);
            let minutes = Math.floor((total_seconds % 3600) / 60);
            let seconds = total_seconds % 60;

            let duration = `${hours}:${String(minutes).padStart(2, "0")}:${String(seconds).padStart(2, "0")}`;

            frm.set_value("custom_total_downtime", duration);
        } else {
            frappe.msgprint(__("End Date & Time must be greater than Start Date & Time."));
            frm.set_value("custom_total_downtime", "");
        }
    } else {
        frm.set_value("custom_total_downtime", "");
    }
}