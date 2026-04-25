# ============================================================
#  Project Title : Contact Management System
#  Author        : [Your Name]
#  Date          : April 25, 2026
#  Description   : A Flask web application for managing contacts.
#                  Supports full CRUD operations (Create, Read,
#                  Update, Delete) and a search feature.
#                  Data stored in an in-memory list (no DB needed).
# ============================================================

from flask import Flask, render_template, request, redirect, url_for

# ── App Initialization ────────────────────────────────────────
app = Flask(__name__)

# ── In-Memory Data Store ──────────────────────────────────────
# Each contact: { id, name, phone, email }
contacts = []
next_id  = 1  # Auto-incrementing ID


def get_contact(contact_id):
    """Helper: return contact dict matching contact_id, or None."""
    return next((c for c in contacts if c["id"] == contact_id), None)


# ── Seed Sample Contacts ──────────────────────────────────────
def seed_contacts():
    global next_id
    samples = [
        {"name": "Alice Johnson",  "phone": "9876543210", "email": "alice@example.com"},
        {"name": "Bob Smith",      "phone": "9123456780", "email": "bob@example.com"},
        {"name": "Carol Williams", "phone": "9988776655", "email": "carol@example.com"},
    ]
    for s in samples:
        contacts.append({"id": next_id, **s})
        next_id += 1

seed_contacts()


# ── Routes ────────────────────────────────────────────────────

# Task 2 & 4 — Home: display all contacts (with optional search)
@app.route("/")
def index():
    """
    Home page — lists all contacts.
    Supports optional ?q= search query (Task 7 Bonus).
    """
    query   = request.args.get("q", "").strip().lower()
    results = contacts

    if query:
        # Filter contacts by name or phone (case-insensitive)
        results = [
            c for c in contacts
            if query in c["name"].lower() or query in c["phone"]
        ]

    return render_template("index.html", contacts=results, query=query)


# Task 3 — Add Contact: show form and handle submission
@app.route("/add", methods=["GET", "POST"])
def add_contact():
    """
    GET  → render empty add-contact form
    POST → validate inputs, save contact, redirect home
    """
    global next_id
    error = None

    if request.method == "POST":
        name  = request.form.get("name",  "").strip()
        phone = request.form.get("phone", "").strip()
        email = request.form.get("email", "").strip()

        # Server-side validation — no empty fields
        if not name or not phone or not email:
            error = "All fields (Name, Phone, Email) are required."
        else:
            contacts.append({
                "id":    next_id,
                "name":  name,
                "phone": phone,
                "email": email,
            })
            next_id += 1
            return redirect(url_for("index"))

    return render_template("add_contact.html", error=error)


# Task 5 — Edit Contact: pre-fill form and save changes
@app.route("/edit/<int:contact_id>", methods=["GET", "POST"])
def edit_contact(contact_id):
    """
    GET  → render form pre-filled with existing contact data
    POST → validate, update contact in-place, redirect home
    """
    contact = get_contact(contact_id)
    error   = None

    if contact is None:
        return redirect(url_for("index"))

    if request.method == "POST":
        name  = request.form.get("name",  "").strip()
        phone = request.form.get("phone", "").strip()
        email = request.form.get("email", "").strip()

        if not name or not phone or not email:
            error = "All fields (Name, Phone, Email) are required."
        else:
            # Update contact in-place
            contact["name"]  = name
            contact["phone"] = phone
            contact["email"] = email
            return redirect(url_for("index"))

    return render_template("edit_contact.html", contact=contact, error=error)


# Task 6 — Delete Contact: remove and redirect
@app.route("/delete/<int:contact_id>", methods=["POST"])
def delete_contact(contact_id):
    """
    POST only — removes the contact with the given id
    and redirects to the home page.
    """
    global contacts
    contacts = [c for c in contacts if c["id"] != contact_id]
    return redirect(url_for("index"))


# ── Entry Point ───────────────────────────────────────────────
if __name__ == "__main__":
    app.run(debug=True)
