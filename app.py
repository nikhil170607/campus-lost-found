import streamlit as st
import sqlite3
from datetime import date
import difflib

# ==========================================
# CONFIGURATION & CONSTANTS
# ==========================================
DB_NAME = "campus_lost_found.db"

CATEGORIES = [
    "Electronics",
    "ID Card / Documents",
    "Books & Notes",
    "Keys & Wallets",
    "Bottle / Accessories",
    "Other",
]

LOCATIONS = [
    "Block-1(School of Fashion)",
    "Block-2(Camous Cafe & Baldev Raj Auditorium)",
    "Block-3(School of Physiotherapy & Paramedical Science)",
    "Block-4(School of Pharamaceutical Science)",
    "Block-6(School of Architecture & Planning and Division of Constructin and Division of Architecture & design)",
    "Block-7(Department of Pharamaceutical Science)",
    "Block-8(School of Fine Arts & School of Design(Multimedia))",
    "Block-9(Girls hostel 1)",
    "Block-10(Girls hostel 2)",
    "Block-11(Girls hostel 3)",
    "Block-12(Girls hostel 4)",
    "Block-13(Division of Student Welfare)",
    "Block-14(MIttal School of Business)",
    "Block-15(Uni-centre and School of Hotel Management & Tourism)",
    "Block-18(School of Social Science & Language and School of Phyiscal Education and Department of Education )",
    "Block-19(School of FIlms,JOurnalism and Creative Arts)",
    "Block-21(School of Law)",
    "Block-22(Girls Hostel 5)",
    "Block-23(Girls Hostel 6)",
    "Block-25,26(School of Agriculture)",
    "Block-27(School of Chemical Engineering and Physical Science)",
    "Block-28(School of Bio Engineering)",
    "Block-29(Office of PRO-Chancellor , Administration-II)",
    "Block-30(The Chancellory, Administration-I)",
    "Block-31(Division of Adnission and Museum of Academics)",
    "Block-32(Office of Vice Chancellor , Administration-III)",
    "Block-33(School of Computer Science and Engineering)",
    "Block-34(School of Computer Science and Engineering)",
    "Block-35(Shanti Devi Mittal School Auditorium)",
    "Block-36(School of Electronics and Electrical Engineering)",
    "Block-37(Central Library)",
    "Block-38(School of Computer Applications)",
    "Block-41(Apartments)",
    "Block-42(Apartments)",
    "Block-43(Apartments)",
    "Block-44(Apartments)",
    "Block-45(Boys Hostel 1)",
    "Block-48(Boys Hostel 2)",
    "Block-49(Boys Hostel 3)",
    "Block-50(Boys Hostel 7)",
    "Block-51(Boys Hostel 4)", 
    "Block-53(Boys Hostel 5)",
    "Block-55(School of Mechanical Engineering)",
    "Block-56(School of Civil Engineering)",
    "Block-57(School of Polytechnic)",



]

# ==========================================
# 1. DATABASE LAYER (SQLite3)
# ==========================================
def get_connection():
    """Create and return a database connection with Row factory for dict-like access."""
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    """Create the items table if it does not already exist."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            category TEXT NOT NULL,
            type TEXT NOT NULL,
            location TEXT NOT NULL,
            date TEXT NOT NULL,
            description TEXT NOT NULL,
            security_hint TEXT NOT NULL,
            security_answer TEXT NOT NULL,
            contact TEXT NOT NULL,
            status TEXT DEFAULT 'Open'
        )
    """)
    conn.commit()
    conn.close()


def add_item(title, category, item_type, location, item_date, description, security_hint, security_answer, contact):
    """Insert a new Lost or Found item into the database."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO items (title, category, type, location, date, description, security_hint, security_answer, contact, status)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, 'Open')
    """, (title, category, item_type, location, str(item_date), description, security_hint, security_answer.strip().lower(), contact))
    conn.commit()
    conn.close()


def fetch_items(status_filter="Open"):
    """Fetch items from the database filtered by status ('Open', 'Resolved', or 'All')."""
    conn = get_connection()
    cursor = conn.cursor()
    if status_filter == "All":
        cursor.execute("SELECT * FROM items ORDER BY id DESC")
    else:
        cursor.execute("SELECT * FROM items WHERE status = ? ORDER BY id DESC", (status_filter,))
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]


def update_item_status(item_id, new_status="Resolved"):
    """Update the status of an item (e.g., from Open to Resolved)."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE items SET status = ? WHERE id = ?", (new_status, item_id))
    conn.commit()
    conn.close()


def delete_item(item_id):
    """Delete an item record permanently."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM items WHERE id = ?", (item_id,))
    conn.commit()
    conn.close()


def load_sample_data():
    """Insert 6 realistic college campus items for instant demo and testing."""
    sample_items = [
        (
            "Casio fx-991EX Scientific Calculator",
            "Electronics",
            "Lost",
            "Academic Block A",
            "2026-10-15",
            "Black scientific calculator left on the 2nd-row desk after the morning Engineering Maths lecture.",
            "What are the 3 initials scratched on the back cover?",
            "rks",
            "rahul.sharma@campus.edu | 9876543210",
            "Open",
        ),
        (
            "Scientific Calculator (Casio Classwiz)",
            "Electronics",
            "Found",
            "Academic Block A",
            "2026-10-15",
            "Found a black Casio scientific calculator near Room 204. Handed over to me after class.",
            "What initials are scratched on the back of the calculator?",
            "rks",
            "priya.verma@campus.edu | 9123456780",
            "Open",
        ),
        (
            "Blue Milton Thermosteel Water Bottle",
            "Bottle / Accessories",
            "Found",
            "Main Canteen",
            "2026-10-16",
            "Found a 1-liter matte blue metal bottle near the juice counter.",
            "Which anime character sticker is pasted near the bottom?",
            "naruto",
            "aman.gupta@campus.edu | 9988776655",
            "Open",
        ),
        (
            "Student ID Card & Blue Lanyard",
            "ID Card / Documents",
            "Lost",
            "Central Library",
            "2026-10-17",
            "Lost my college ID card somewhere near the reading hall or issue counter.",
            "What are the last 4 digits of the Enrollment Number?",
            "4092",
            "sneha.patel@campus.edu | 9871234560",
            "Open",
        ),
        (
            "Hostel Room Key with Red Keychain",
            "Keys & Wallets",
            "Found",
            "Sports Complex",
            "2026-10-18",
            "Found a single silver key on a red keychain near the badminton court benches.",
            "What room number is stamped on the key tag?",
            "b-304",
            "vikram.singh@campus.edu | 9765432109",
            "Open",
        ),
        (
            "Data Structures & Algorithms Notebook",
            "Books & Notes",
            "Lost",
            "Computer Lab 1",
            "2026-10-14",
            "Spiral-bound Classmate notebook containing handwritten Python and DSA notes.",
            "What name is written on the inside first page?",
            "kunal",
            "kunal.mehta@campus.edu | 9654321098",
            "Resolved",
        ),
    ]

    conn = get_connection()
    cursor = conn.cursor()
    # Prevent duplicate sample insertion if clicked multiple times
    cursor.execute("SELECT COUNT(*) FROM items")
    if cursor.fetchone()[0] == 0:
        cursor.executemany("""
            INSERT INTO items (title, category, type, location, date, description, security_hint, security_answer, contact, status)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, sample_items)
        conn.commit()
        conn.close()
        return True
    conn.close()
    return False


# ==========================================
# 2. SMART MATCHING ENGINE (difflib)
# ==========================================
def find_potential_matches(title, category, item_type, description):
    """
    Compare an item against open items of the opposite type (Lost vs Found)
    using difflib.SequenceMatcher to compute text similarity.
    """
    opposite_type = "Found" if item_type == "Lost" else "Lost"
    all_open_items = fetch_items(status_filter="Open")
    candidates = [item for item in all_open_items if item["type"] == opposite_type]

    matches = []
    source_text = f"{title} {description}".lower()

    for candidate in candidates:
        target_text = f"{candidate['title']} {candidate['description']}".lower()
        text_ratio = difflib.SequenceMatcher(None, source_text, target_text).ratio()

        # Boost score by 25% if both items belong to the exact same category
        category_bonus = 0.25 if candidate["category"] == category else 0.0
        final_score = min((text_ratio + category_bonus) * 100, 99.0)

        if final_score >= 50.0:
            matches.append((candidate, round(final_score, 1)))

    # Sort matches highest score first
    matches.sort(key=lambda x: x[1], reverse=True)
    return matches


# ==========================================
# 3. STREAMLIT UI PAGES
# ==========================================
def render_dashboard():
    st.title("🎓 Campus Lost & Found Dashboard")
    st.caption("Browse active reports, filter by campus location, or search for a specific item.")

    all_items = fetch_items(status_filter="All")
    open_items = [i for i in all_items if i["status"] == "Open"]
    lost_count = sum(1 for i in open_items if i["type"] == "Lost")
    found_count = sum(1 for i in open_items if i["type"] == "Found")
    resolved_count = sum(1 for i in all_items if i["status"] == "Resolved")

    # Top-level Metrics
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Active Lost Items", lost_count)
    col2.metric("Active Found Items", found_count)
    col3.metric("Resolved / Claimed", resolved_count)
    resolution_rate = round((resolved_count / len(all_items)) * 100) if all_items else 0
    col4.metric("Resolution Rate", f"{resolution_rate}%")

    st.divider()

    # Search and Filter Bar
    f_col1, f_col2, f_col3, f_col4 = st.columns([2, 1.2, 1.5, 1.5])
    with f_col1:
        search_query = st.text_input("🔍 Search by Keyword", placeholder="e.g., Casio, Blue bottle, ID...")
    with f_col2:
        type_filter = st.selectbox("Item Type", ["All", "Lost", "Found"])
    with f_col3:
        cat_filter = st.selectbox("Category", ["All"] + CATEGORIES)
    with f_col4:
        loc_filter = st.selectbox("Campus Location", ["All"] + LOCATIONS)

    # Apply Filters dynamically
    filtered = open_items
    if type_filter != "All":
        filtered = [i for i in filtered if i["type"] == type_filter]
    if cat_filter != "All":
        filtered = [i for i in filtered if i["category"] == cat_filter]
    if loc_filter != "All":
        filtered = [i for i in filtered if i["location"] == loc_filter]
    if search_query.strip():
        q = search_query.strip().lower()
        filtered = [
            i for i in filtered
            if q in i["title"].lower() or q in i["description"].lower()
        ]

    st.subheader(f"Active Listings ({len(filtered)})")

    if not filtered:
        st.info("No matching open items found. Try adjusting your filters or click **Load Sample Campus Data** in the sidebar!")
        return

    for item in filtered:
        badge = "🔴 LOST" if item["type"] == "Lost" else "🟢 FOUND"
        header_text = f"{badge} | **{item['title']}** — *{item['location']}* (Reported: {item['date']})"
        with st.expander(header_text):
            c1, c2 = st.columns([2, 1])
            with c1:
                st.markdown(f"**Description:** {item['description']}")
                st.markdown(f"**Category:** `{item['category']}`")
            with c2:
                st.markdown(f"**Item ID:** `#{item['id']}`")
                st.markdown(f"**Security Question:** *{item['security_hint']}*")
                st.caption("🔒 Contact info is hidden until verified in the **Claim & Verify** tab.")


def render_report_form():
    st.title("📝 Report a Lost or Found Item")
    st.caption("Fill out the details below. A security question ensures only the rightful owner or finder can resolve the listing.")

    with st.form("report_item_form", clear_on_submit=True):
        col1, col2 = st.columns(2)
        with col1:
            item_type = st.radio("Are you reporting a Lost or Found item?", ["Lost", "Found"], horizontal=True)
            title = st.text_input("Item Title *", placeholder="e.g., Black Casio Scientific Calculator")
            category = st.selectbox("Category *", CATEGORIES)
            location = st.selectbox("Campus Location *", LOCATIONS)
        with col2:
            item_date = st.date_input("Date Lost / Found *", value=date.today(), max_value=date.today())
            contact = st.text_input("Your Contact Info (Email / Phone) *", placeholder="e.g., student@campus.edu | 9876543210")
            security_hint = st.text_input(
                "Verification Question (Public) *",
                placeholder="e.g., What sticker or scratch is on the back?",
            )
            security_answer = st.text_input(
                "Secret Answer / PIN (Private) *",
                placeholder="e.g., naruto (Case-insensitive, single word/number works best)",
            )

        description = st.text_area(
            "Public Description *",
            placeholder="Describe general appearance, brand, color, or where exactly it was last seen/found...",
        )

        submitted = st.form_submit_button("Submit Report", use_container_width=True)

        if submitted:
            # Input Validation
            if not all([title.strip(), description.strip(), security_hint.strip(), security_answer.strip(), contact.strip()]):
                st.error("⚠️ Please fill in all required fields marked with *.")
            elif len(contact.strip()) < 5:
                st.error("⚠️ Please provide a valid email address or phone number.")
            else:
                add_item(
                    title.strip(),
                    category,
                    item_type,
                    location,
                    item_date,
                    description.strip(),
                    security_hint.strip(),
                    security_answer.strip(),
                    contact.strip(),
                )
                st.success(f"✅ Your **{item_type}** report for **'{title}'** has been logged!")

                # Run Smart Matching immediately after submission
                matches = find_potential_matches(title, category, item_type, description)
                if matches:
                    st.warning(f"🔔 **Smart Match Alert!** We found {len(matches)} existing opposite listing(s) that closely match your report:")
                    for matched_item, score in matches:
                        st.info(
                            f"**Match Score: {score}%** — [{matched_item['type']}] **{matched_item['title']}** "
                            f"at *{matched_item['location']}* (Item ID: `#{matched_item['id']}`). "
                            f"Head to the **Claim & Verify** tab to check it!"
                        )


def render_claim_and_match():
    st.title("🔐 Claim, Verify & Smart Match")

    tab1, tab2 = st.tabs(["✅ Verify & Claim an Item", "🤖 Smart Auto-Matcher (All Open Items)"])

    with tab1:
        st.subheader("Verify Ownership to Unlock Contact Details")
        open_items = fetch_items(status_filter="Open")

        if not open_items:
            st.info("No open items available to claim right now.")
        else:
            item_options = {
                f"#{item['id']} | [{item['type']}] {item['title']} ({item['location']})": item
                for item in open_items
            }
            selected_label = st.selectbox("Select the Item you want to Claim / Resolve:", list(item_options.keys()))
            selected_item = item_options[selected_label]

            st.markdown("---")
            st.markdown(f"**Item Description:** {selected_item['description']}")
            st.markdown(f"**Security Verification Question:** `{selected_item['security_hint']}`")

            user_answer = st.text_input("Enter the Answer to the Verification Question:", key="verify_input")

            col_btn1, col_btn2 = st.columns(2)
            with col_btn1:
                if st.button("🔓 Verify & Reveal Contact Info", use_container_width=True):
                    if user_answer.strip().lower() == selected_item["security_answer"].strip().lower():
                        st.session_state["verified_item_id"] = selected_item["id"]
                        st.success("🎉 Verification Successful!")
                    else:
                        st.session_state["verified_item_id"] = None
                        st.error("❌ Incorrect answer. Please check the hint and try again.")

            # Show contact details and 'Mark as Resolved' button only if verified
            if st.session_state.get("verified_item_id") == selected_item["id"]:
                st.info(f"📞 **Reporter Contact Details:** `{selected_item['contact']}`")
                if st.button("✔️ Mark Item as Resolved / Returned", type="primary"):
                    update_item_status(selected_item["id"], "Resolved")
                    st.session_state["verified_item_id"] = None
                    st.success("Item marked as Resolved! Refreshing...")
                    st.rerun()

    with tab2:
        st.subheader("AI / Fuzzy String Matching (`difflib` Engine)")
        st.caption("Automatically pairs active **Lost** reports with active **Found** reports based on category and text similarity.")

        open_items = fetch_items(status_filter="Open")
        lost_items = [i for i in open_items if i["type"] == "Lost"]

        found_any_pair = False
        for lost in lost_items:
            matches = find_potential_matches(lost["title"], lost["category"], "Lost", lost["description"])
            for found_match, score in matches:
                found_any_pair = True
                with st.container(border=True):
                    st.markdown(f"#### 🔗 Match Confidence: `{score}%`")
                    c1, c2 = st.columns(2)
                    with c1:
                        st.markdown(f"**🔴 LOST (#{lost['id']}):** {lost['title']}")
                        st.caption(f"📍 {lost['location']} | 📅 {lost['date']}")
                        st.write(lost["description"])
                    with c2:
                        st.markdown(f"**🟢 FOUND (#{found_match['id']}):** {found_match['title']}")
                        st.caption(f"📍 {found_match['location']} | 📅 {found_match['date']}")
                        st.write(found_match["description"])

        if not found_any_pair:
            st.info("No high-confidence matches detected between current Lost and Found items.")


def render_admin_panel():
    st.title("🛠️ Admin & Campus Analytics")
    all_items = fetch_items(status_filter="All")

    if not all_items:
        st.info("Database is currently empty. Load sample data from the sidebar to view analytics.")
        return

    # Location Breakdown (Pure Python - No PyArrow DLL required)
    st.subheader("📍 Reports by Campus Location")
    loc_counts = {}
    for item in all_items:
        loc_counts[item["location"]] = loc_counts.get(item["location"], 0) + 1

    total_reports = len(all_items)
    for loc, count in sorted(loc_counts.items(), key=lambda x: x[1], reverse=True):
        percentage = int((count / total_reports) * 100)
        st.progress(
            count / total_reports,
            text=f"**{loc}** — {count} report(s) ({percentage}%)",
        )

    st.divider()
    st.subheader("📋 Manage All Database Records")

    for item in all_items:
        status_icon = "🟢 Open" if item["status"] == "Open" else "⚪ Resolved"
        col1, col2, col3 = st.columns([4, 1.2, 1])
        with col1:
            st.write(f"**#{item['id']} [{item['type']}] {item['title']}** — *{item['location']}* ({status_icon})")
        with col2:
            if item["status"] == "Open":
                if st.button("Mark Resolved", key=f"res_{item['id']}"):
                    update_item_status(item["id"], "Resolved")
                    st.rerun()
            else:
                if st.button("Re-open", key=f"open_{item['id']}"):
                    update_item_status(item["id"], "Open")
                    st.rerun()
        with col3:
            if st.button("🗑️ Delete", key=f"del_{item['id']}"):
                delete_item(item["id"])
                st.rerun()

# ==========================================
# 4. MAIN APPLICATION ENTRY POINT
# ==========================================
def main():
    st.set_page_config(page_title="Campus Lost & Found", page_icon="🎓", layout="wide")
    init_db()

    # Sidebar Navigation
    st.sidebar.title("🧭 Campus Navigation")
    menu = st.sidebar.radio(
        "Go to:",
        [
            "Dashboard & Search",
            "Report an Item",
            "Claim & Smart Match",
            "Admin & Analytics",
        ],
    )

    st.sidebar.divider()
    st.sidebar.subheader("⚡ Quick Demo Controls")
    if st.sidebar.button("📥 Load Sample Campus Data", use_container_width=True):
        inserted = load_sample_data()
        if inserted:
            st.sidebar.success("Loaded 6 sample campus items!")
            st.rerun()
        else:
            st.sidebar.warning("Database already contains items!")

    st.sidebar.caption("Built with Python, Streamlit & SQLite3")

    # Page Routing
    if menu == "Dashboard & Search":
        render_dashboard()
    elif menu == "Report an Item":
        render_report_form()
    elif menu == "Claim & Smart Match":
        render_claim_and_match()
    elif menu == "Admin & Analytics":
        render_admin_panel()


if __name__ == "__main__":
    main()
