
import streamlit as st
import pandas as pd
import sqlite3
import hashlib
import secrets
import hmac
from pathlib import Path
from datetime import date

from database import initialize_database, get_connection


# ---------------- PAGE CONFIGURATION ----------------

st.set_page_config(
    page_title="Smart Local Farmer Connect",
    page_icon="🌱",
    layout="wide"
)

initialize_database()
import seed_data


# ---------------- PASSWORD FUNCTIONS ----------------

def hash_password(password):
    salt = secrets.token_bytes(16)

    password_hash = hashlib.pbkdf2_hmac(
        "sha256",
        password.encode(),
        salt,
        200000
    )

    return salt.hex() + ":" + password_hash.hex()


def verify_password(password, stored_hash):
    try:
        salt_hex, hash_hex = stored_hash.split(":")
        salt = bytes.fromhex(salt_hex)

        new_hash = hashlib.pbkdf2_hmac(
            "sha256",
            password.encode(),
            salt,
            200000
        )

        return hmac.compare_digest(
            new_hash.hex(),
            hash_hex
        )

    except (ValueError, AttributeError):
        return False


# ---------------- SESSION STATE ----------------

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False


# ---------------- CUSTOM DESIGN ----------------

st.markdown("""
<style>
.main {
    background-color: #f5faf3;
}
.hero {
    background: linear-gradient(120deg, #14532d, #4d9b55);
    padding: 35px;
    border-radius: 18px;
    color: white;
    text-align: center;
}
.hero h1 {
    color: white;
    font-size: 38px;
}
.hero p {
    font-size: 18px;
}
</style>
""", unsafe_allow_html=True)


# ---------------- SIDEBAR ----------------

st.sidebar.title("🌱 FarmerConnect")
st.sidebar.caption("Local Farmer Market Information System")

menu = st.sidebar.radio(
    "Navigation",
    [
        "Home",
        "Explore Products",
        "Market Prices",
        "Farmer Registration",
        "Customer Registration",
        "Login",
        "My Dashboard",
        "About Us"
    ]
)

st.sidebar.markdown("---")

if st.session_state.logged_in:

    st.sidebar.success(
        f"Logged in: {st.session_state.user_name}"
    )

    st.sidebar.caption(
        f"Account: {st.session_state.user_role}"
    )

    if st.sidebar.button("Logout"):

        for key in [
            "logged_in",
            "user_id",
            "user_name",
            "username",
            "user_role"
        ]:
            st.session_state.pop(key, None)

        st.rerun()

else:
    st.sidebar.info("Connecting Farmers and Customers")


# ---------------- HOME PAGE ----------------

if menu == "Home":

    st.markdown("""
    <div class="hero">
        <h1>🌱 Smart Local Farmer Connect</h1>
        <p>Connecting Farmers Directly with Customers</p>
        <p>Supporting Local Agriculture Through Technology</p>
    </div>
    """, unsafe_allow_html=True)

    st.write("")

    st.header("Welcome to FarmerConnect!")

    st.write(
        "Smart Local Farmer Connect is a digital platform "
        "that helps farmers display their agricultural products "
        "and connect directly with customers."
    )

    col1, col2, col3 = st.columns(3)

    with col1:
        st.subheader("👨‍🌾 Farmers")
        st.write("Register and display your agricultural products.")

    with col2:
        st.subheader("🛒 Customers")
        st.write("Explore products and contact local farmers.")

    with col3:
        st.subheader("📊 Market Prices")
        st.write("View available crop and market price information.")


# ---------------- FARMER REGISTRATION ----------------

elif menu == "Farmer Registration":

    st.title("👨‍🌾 Farmer Registration")

    with st.form("farmer_registration"):

        name = st.text_input("Full Name")
        phone = st.text_input("Phone Number")
        village = st.text_input("Village")
        username = st.text_input("Create Username")
        password = st.text_input("Create Password", type="password")
        confirm_password = st.text_input(
            "Confirm Password",
            type="password"
        )

        submitted = st.form_submit_button("Register as Farmer")

        if submitted:

            if not all([
                name.strip(),
                phone.strip(),
                village.strip(),
                username.strip(),
                password,
                confirm_password
            ]):
                st.error("Please fill all fields.")

            elif not phone.strip().isdigit() or len(phone.strip()) != 10:
                st.error("Enter a valid 10-digit phone number.")

            elif len(password) < 8:
                st.error("Password must contain at least 8 characters.")

            elif password != confirm_password:
                st.error("Passwords do not match.")

            else:

                conn = get_connection()
                cursor = conn.cursor()

                try:
                    cursor.execute("""
                        INSERT INTO farmers
                        (name, phone, village, username, password_hash)
                        VALUES (?, ?, ?, ?, ?)
                    """, (
                        name.strip(),
                        phone.strip(),
                        village.strip(),
                        username.strip(),
                        hash_password(password)
                    ))

                    conn.commit()
                    st.success("Farmer registration successful!")

                except sqlite3.IntegrityError:
                    st.error("This username is already registered.")

                finally:
                    conn.close()


# ---------------- CUSTOMER REGISTRATION ----------------

elif menu == "Customer Registration":

    st.title("🛒 Customer Registration")

    with st.form("customer_registration"):

        name = st.text_input("Full Name")
        phone = st.text_input("Phone Number")
        username = st.text_input("Create Username")
        password = st.text_input("Create Password", type="password")
        confirm_password = st.text_input(
            "Confirm Password",
            type="password"
        )

        submitted = st.form_submit_button("Register as Customer")

        if submitted:

            if not all([
                name.strip(),
                phone.strip(),
                username.strip(),
                password,
                confirm_password
            ]):
                st.error("Please fill all fields.")

            elif not phone.strip().isdigit() or len(phone.strip()) != 10:
                st.error("Enter a valid 10-digit phone number.")

            elif len(password) < 8:
                st.error("Password must contain at least 8 characters.")

            elif password != confirm_password:
                st.error("Passwords do not match.")

            else:

                conn = get_connection()
                cursor = conn.cursor()

                try:
                    cursor.execute("""
                        INSERT INTO customers
                        (name, phone, username, password_hash)
                        VALUES (?, ?, ?, ?)
                    """, (
                        name.strip(),
                        phone.strip(),
                        username.strip(),
                        hash_password(password)
                    ))

                    conn.commit()
                    st.success("Customer registration successful!")

                except sqlite3.IntegrityError:
                    st.error("This username is already registered.")

                finally:
                    conn.close()


# ---------------- LOGIN ----------------

elif menu == "Login":

    st.title("🔐 Farmer & Customer Login")

    with st.form("login_form"):

        role = st.selectbox(
            "Select Account Type",
            ["Farmer", "Customer"]
        )

        username = st.text_input("Username")
        password = st.text_input("Password", type="password")

        submitted = st.form_submit_button("Login")

        if submitted:

            if not username.strip() or not password:
                st.error("Please enter username and password.")

            else:

                conn = get_connection()
                cursor = conn.cursor()

                if role == "Farmer":
                    cursor.execute("""
                        SELECT farmer_id, name, username, password_hash
                        FROM farmers
                        WHERE username = ?
                    """, (username.strip(),))

                else:
                    cursor.execute("""
                        SELECT customer_id, name, username, password_hash
                        FROM customers
                        WHERE username = ?
                    """, (username.strip(),))

                user = cursor.fetchone()
                conn.close()

                if user and verify_password(password, user[3]):

                    st.session_state.logged_in = True
                    st.session_state.user_id = user[0]
                    st.session_state.user_name = user[1]
                    st.session_state.username = user[2]
                    st.session_state.user_role = role

                    st.success("Login successful!")
                    st.rerun()

                else:
                    st.error("Incorrect username or password.")


# ---------------- EXPLORE PRODUCTS ----------------

elif menu == "Explore Products":

    st.title("🛒 Explore Agricultural Products")

    search = st.text_input("Search for a product")

    category = st.selectbox(
        "Filter by Category",
        [
            "All",
            "Vegetables",
            "Fruits",
            "Grains",
            "Pulses",
            "Other"
        ]
    )

    conn = get_connection()

    products = pd.read_sql_query("""
        SELECT
            p.product_id,
            p.farmer_id,
            p.product_name,
            p.category,
            p.quantity,
            p.price,
            p.image_path,
            p.availability,
            f.name AS farmer_name,
            f.phone AS farmer_phone,
            f.village AS farmer_village
        FROM products p
        JOIN farmers f ON p.farmer_id = f.farmer_id
        WHERE p.availability = 'Available'
        ORDER BY p.product_id DESC
    """, conn)

    conn.close()

    if search.strip():
        products = products[
            products["product_name"].str.contains(
                search.strip(),
                case=False,
                na=False
            )
        ]

    if category != "All":
        products = products[
            products["category"] == category
        ]

    if products.empty:

        st.info("No matching products are available yet.")

    else:

        st.success(f"{len(products)} product(s) found.")

        for _, product in products.iterrows():

            with st.container():

                st.divider()

                col1, col2 = st.columns([1, 2])

                with col1:

                    image_path = product["image_path"]

                    if image_path and Path(image_path).is_file():
                        st.image(image_path, width=180)
                    else:
                        st.write("🌾 Product photo not uploaded")

                with col2:

                    st.subheader(product["product_name"])

                    st.write(f"**Category:** {product['category']}")
                    st.write(f"**Quantity:** {product['quantity']} kg")
                    st.write(f"**Price:** ₹{product['price']} per kg")
                    st.write(f"**Farmer:** {product['farmer_name']}")
                    st.write(f"**Village:** {product['farmer_village']}")

                    if st.session_state.logged_in and \
                       st.session_state.user_role == "Customer":

                        with st.form(
                            f"enquiry_{int(product['product_id'])}"
                        ):

                            message = st.text_area(
                                "Message to Farmer",
                                placeholder="I am interested in this product."
                            )

                            send = st.form_submit_button(
                                "Send Enquiry"
                            )

                            if send:

                                conn = get_connection()
                                cursor = conn.cursor()

                                cursor.execute("""
                                    INSERT INTO enquiries
                                    (customer_id, farmer_id, product_id, message)
                                    VALUES (?, ?, ?, ?)
                                """, (
                                    st.session_state.user_id,
                                    int(product["farmer_id"]),
                                    int(product["product_id"]),
                                    message.strip()
                                ))

                                conn.commit()
                                conn.close()

                                st.success("Enquiry sent successfully!")

                    elif not st.session_state.logged_in:

                        st.info("Login as a customer to send an enquiry.")


# ---------------- MARKET PRICES ----------------

elif menu == "Market Prices":

    st.title("📊 Local Agricultural Market Prices")

    st.write(
        "View market prices entered into the FarmerConnect system. "
        "These are submitted records, not automatic live market prices."
    )

    if st.session_state.logged_in and \
       st.session_state.user_role == "Farmer":

        st.subheader("➕ Submit a Local Market Price")

        with st.form("market_price_form"):

            crop_name = st.text_input("Crop Name")
            market_name = st.text_input("Market Name")

            market_price = st.number_input(
                "Price per kg (₹)",
                min_value=0.1,
                step=1.0
            )

            price_date = st.date_input(
                "Price Date",
                value=date.today()
            )

            submitted = st.form_submit_button("Submit Market Price")

            if submitted:

                if not crop_name.strip() or not market_name.strip():
                    st.error("Please enter crop and market names.")

                else:

                    conn = get_connection()
                    cursor = conn.cursor()

                    cursor.execute("""
                        INSERT INTO market_prices
                        (crop_name, market_name, price, price_date)
                        VALUES (?, ?, ?, ?)
                    """, (
                        crop_name.strip(),
                        market_name.strip(),
                        market_price,
                        price_date.isoformat()
                    ))

                    conn.commit()
                    conn.close()

                    st.success("Market price submitted!")
                    st.rerun()

    conn = get_connection()

    prices = pd.read_sql_query("""
        SELECT crop_name, market_name, price, price_date
        FROM market_prices
        ORDER BY price_date DESC
    """, conn)

    conn.close()

    if prices.empty:
        st.info(
            "No market price records are available yet. "
            "A farmer can submit a local market price after logging in."
        )

    else:

        st.subheader("Available Market Price Records")

        st.dataframe(
            prices,
            use_container_width=True,
            hide_index=True
        )


# ---------------- MY DASHBOARD ----------------

elif menu == "My Dashboard":

    st.title("👤 My Dashboard")

    if not st.session_state.logged_in:

        st.warning("Please login to access your dashboard.")

    else:

        st.success(
            f"Welcome, {st.session_state.user_name}!"
        )

        st.write(f"**Username:** {st.session_state.username}")
        st.write(f"**Account Type:** {st.session_state.user_role}")

        # FARMER DASHBOARD

        if st.session_state.user_role == "Farmer":

            st.divider()
            st.subheader("➕ Add a New Product")

            with st.form("add_product_form"):

                product_name = st.text_input("Product Name")

                category = st.selectbox(
                    "Category",
                    [
                        "Vegetables",
                        "Fruits",
                        "Grains",
                        "Pulses",
                        "Other"
                    ]
                )

                quantity = st.number_input(
                    "Quantity (kg)",
                    min_value=0.1,
                    step=0.5
                )

                price = st.number_input(
                    "Price per kg (₹)",
                    min_value=0.1,
                    step=1.0
                )

                product_image = st.file_uploader(
                    "Upload Product Photo (Optional)",
                    type=["jpg", "jpeg", "png"]
                )

                submitted = st.form_submit_button("Add Product")

                if submitted:

                    if not product_name.strip():

                        st.error("Please enter a product name.")

                    else:

                        image_path = None

                        if product_image is not None:

                            upload_folder = Path("uploads")
                            upload_folder.mkdir(exist_ok=True)

                            safe_filename = (
                                secrets.token_hex(8) + "_" +
                                Path(product_image.name).name
                            )

                            image_path = str(
                                upload_folder / safe_filename
                            )

                            with open(image_path, "wb") as file:
                                file.write(product_image.getvalue())

                        conn = get_connection()
                        cursor = conn.cursor()

                        cursor.execute("""
                            INSERT INTO products
                            (
                                farmer_id,
                                product_name,
                                category,
                                quantity,
                                price,
                                image_path
                            )
                            VALUES (?, ?, ?, ?, ?, ?)
                        """, (
                            st.session_state.user_id,
                            product_name.strip(),
                            category,
                            quantity,
                            price,
                            image_path
                        ))

                        conn.commit()
                        conn.close()

                        st.success("Product added successfully!")
                        st.rerun()

            # FARMER'S PRODUCTS

            st.divider()
            st.subheader("📦 My Products")

            conn = get_connection()

            my_products = pd.read_sql_query("""
                SELECT product_id, product_name, category,
                       quantity, price, availability
                FROM products
                WHERE farmer_id = ?
                ORDER BY product_id DESC
            """, conn, params=(st.session_state.user_id,))

            conn.close()

            if my_products.empty:

                st.info("You have not added any products yet.")

            else:

                for _, item in my_products.iterrows():

                    col1, col2 = st.columns([4, 1])

                    with col1:

                        st.write(
                            f"**{item['product_name']}** "
                            f"({item['category']})"
                        )

                        st.write(
                            f"Quantity: {item['quantity']} kg | "
                            f"Price: ₹{item['price']} per kg | "
                            f"Status: {item['availability']}"
                        )

                    with col2:

                        if st.button(
                            "Delete",
                            key=f"delete_{int(item['product_id'])}"
                        ):

                            conn = get_connection()
                            cursor = conn.cursor()

                            cursor.execute("""
                                DELETE FROM products
                                WHERE product_id = ? AND farmer_id = ?
                            """, (
                                int(item["product_id"]),
                                st.session_state.user_id
                            ))

                            conn.commit()
                            conn.close()

                            st.success("Product deleted.")
                            st.rerun()

            # FARMER ENQUIRIES

            st.divider()
            st.subheader("📩 Customer Enquiries")

            conn = get_connection()

            farmer_enquiries = pd.read_sql_query("""
                SELECT
                    e.enquiry_id,
                    e.message,
                    e.status,
                    c.name AS customer_name,
                    c.phone AS customer_phone,
                    p.product_name
                FROM enquiries e
                JOIN customers c ON e.customer_id = c.customer_id
                JOIN products p ON e.product_id = p.product_id
                WHERE e.farmer_id = ?
                ORDER BY e.enquiry_id DESC
            """, conn, params=(st.session_state.user_id,))

            conn.close()

            if farmer_enquiries.empty:

                st.info("No customer enquiries yet.")

            else:

                for _, enquiry in farmer_enquiries.iterrows():

                    st.write(
                        f"**Product:** {enquiry['product_name']}"
                    )

                    st.write(
                        f"**Customer:** {enquiry['customer_name']}"
                    )

                    st.write(
                        f"**Phone:** {enquiry['customer_phone']}"
                    )

                    st.write(
                        f"**Message:** {enquiry['message'] or 'No message'}"
                    )

                    st.write(
                        f"**Current Status:** {enquiry['status']}"
                    )

                    with st.form(
                        f"status_form_{int(enquiry['enquiry_id'])}"
                    ):

                        new_status = st.selectbox(
                            "Update Enquiry Status",
                            ["Pending", "Contacted", "Completed"],
                            index=(
                                ["Pending", "Contacted", "Completed"].index(
                                    enquiry["status"]
                                )
                                if enquiry["status"] in
                                ["Pending", "Contacted", "Completed"]
                                else 0
                            )
                        )

                        update = st.form_submit_button("Update Status")

                        if update:

                            conn = get_connection()
                            cursor = conn.cursor()

                            cursor.execute("""
                                UPDATE enquiries
                                SET status = ?
                                WHERE enquiry_id = ? AND farmer_id = ?
                            """, (
                                new_status,
                                int(enquiry["enquiry_id"]),
                                st.session_state.user_id
                            ))

                            conn.commit()
                            conn.close()

                            st.success("Enquiry status updated!")
                            st.rerun()

        # CUSTOMER DASHBOARD

        else:

            st.divider()
            st.subheader("📩 My Enquiries")

            conn = get_connection()

            customer_enquiries = pd.read_sql_query("""
                SELECT
                    p.product_name,
                    f.name AS farmer_name,
                    f.phone AS farmer_phone,
                    e.message,
                    e.status
                FROM enquiries e
                JOIN products p ON e.product_id = p.product_id
                JOIN farmers f ON e.farmer_id = f.farmer_id
                WHERE e.customer_id = ?
                ORDER BY e.enquiry_id DESC
            """, conn, params=(st.session_state.user_id,))

            conn.close()

            if customer_enquiries.empty:

                st.info("You have not sent any enquiries yet.")

            else:

                st.dataframe(
                    customer_enquiries,
                    use_container_width=True,
                    hide_index=True
                )


# ---------------- ABOUT US ----------------

elif menu == "About Us":

    st.title("🌱 About Smart Local Farmer Connect")

    st.write(
        "Smart Local Farmer Connect is a digital agricultural "
        "marketplace designed to connect local farmers and customers."
    )

    st.subheader("Our Objectives")

    st.write("""
    - Help farmers display their agricultural products.
    - Connect farmers directly with customers.
    - Allow customers to explore available products.
    - Provide recorded local agricultural market prices.
    - Support digital technology in agriculture.
    """)

    st.subheader("Technologies Used")

    st.write("""
    - Python
    - Streamlit
    - SQLite Database
    - Pandas
    """)
