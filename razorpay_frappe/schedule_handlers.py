import frappe


def sync_payment_link_status():
	pending_payment_links = frappe.db.get_all(
		"Razorpay Payment Link",
		filters={"status": ("in", ("Created", "Partially Paid"))},
		pluck="name",
	)

	for p_link in pending_payment_links:
		try:
			frappe.get_doc("Razorpay Payment Link", p_link).fetch_latest_status()
			frappe.db.commit()
		except Exception:
			frappe.log_error(frappe.get_traceback(), f"Razorpay Sync Error: {p_link}")
			frappe.db.rollback()
