
import sqlite3
import hashlib
import secrets
from datetime import date

from database import initialize_database, get_connection

def hash_password(password):
    salt = secrets.token_bytes(16)

    password_hash = hashlib.pbkdf2_hmac(
        "sha256",
        password.encode(),
        salt,
        200000
    )

    return salt.hex() + ":" + password_hash.hex()

initialize_database()

conn = get_connection()
cursor = conn.cursor()

# --------------------------------
# 1. DEMO FARMERS
# --------------------------------

farmers = [
    ("Ramesh Kumar", "0000000001", "Anekal", "demo_farmer1"),
    ("Suresh Gowda", "0000000002", "Kanakapura", "demo_farmer2"),
    ("Manjula Devi", "0000000003", "Kolar", "demo_farmer3"),
    ("Ravi Kumar", "0000000004", "Ramanagara", "demo_farmer4"),
]

farmer_ids = {}

for name, phone, village, username in farmers:

    cursor.execute(
        "SELECT farmer_id FROM farmers WHERE username = ?",
        (username,)
    )

    result = cursor.fetchone()

    if result:
        farmer_ids[username] = result[0]

    else:
        cursor.execute("""
            INSERT INTO farmers
            (name, phone, village, username, password_hash)
            VALUES (?, ?, ?, ?, ?)
        """, (
            name,
            phone,
            village,
            username,
            hash_password("Demo@12345")
        ))

        farmer_ids[username] = cursor.lastrowid

# --------------------------------
# 2. DEMO CUSTOMERS
# --------------------------------

customers = [
    ("Rahul Kumar", "0000000011", "demo_customer1"),
    ("Priya Sharma", "0000000012", "demo_customer2"),
    ("Ananya Rao", "0000000013", "demo_customer3"),
]

customer_ids = {}

for name, phone, username in customers:

    cursor.execute(
        "SELECT customer_id FROM customers WHERE username = ?",
        (username,)
    )

    result = cursor.fetchone()

    if result:
        customer_ids[username] = result[0]

    else:
        cursor.execute("""
            INSERT INTO customers
            (name, phone, username, password_hash)
            VALUES (?, ?, ?, ?)
        """, (
            name,
            phone,
            username,
            hash_password("Demo@12345")
        ))

        customer_ids[username] = cursor.lastrowid

# --------------------------------
# 3. AGRICULTURAL PRODUCTS
# --------------------------------

products = [
    ("Tomato", "Vegetables", 100, 25, "demo_farmer1"),
    ("Potato", "Vegetables", 80, 30, "demo_farmer1"),
    ("Onion", "Vegetables", 120, 35, "demo_farmer1"),
    ("Carrot", "Vegetables", 60, 40, "demo_farmer2"),
    ("Beans", "Vegetables", 50, 45, "demo_farmer2"),
    ("Banana", "Fruits", 150, 40, "demo_farmer3"),
    ("Mango", "Fruits", 70, 80, "demo_farmer3"),
    ("Ragi", "Grains", 200, 35, "demo_farmer4"),
    ("Rice", "Grains", 250, 55, "demo_farmer4"),
    ("Green Gram", "Pulses", 90, 100, "demo_farmer2"),
    ("Groundnut", "Pulses", 110, 90, "demo_farmer1"),
    ("Coconut", "Other", 100, 35, "demo_farmer3"),
]

product_ids = {}

for name, category, quantity, price, farmer_username in products:

    farmer_id = farmer_ids[farmer_username]

    cursor.execute("""
        SELECT product_id FROM products
        WHERE farmer_id = ? AND product_name = ?
    """, (farmer_id, name))

    result = cursor.fetchone()

    if result:
        product_ids[(farmer_username, name)] = result[0]

    else:
        cursor.execute("""
            INSERT INTO products
            (farmer_id, product_name, category,
             quantity, price, availability)
            VALUES (?, ?, ?, ?, ?, 'Available')
        """, (
            farmer_id,
            name,
            category,
            quantity,
            price
        ))

        product_ids[(farmer_username, name)] = cursor.lastrowid

# --------------------------------
# 4. SAMPLE MARKET PRICE RECORDS
# --------------------------------

today = date.today().isoformat()

market_prices = [
    ("Tomato", "Bengaluru APMC", 25),
    ("Tomato", "Kolar Market", 22),
    ("Tomato", "Ramanagara Market", 28),
    ("Onion", "Bengaluru APMC", 35),
    ("Onion", "Kolar Market", 32),
    ("Potato", "Bengaluru APMC", 30),
    ("Carrot", "Bengaluru APMC", 40),
    ("Banana", "Mysuru Market", 40),
    ("Ragi", "Ramanagara Market", 35),
    ("Rice", "Bengaluru APMC", 55),
    ("Green Gram", "Kolar Market", 100),
    ("Groundnut", "Ramanagara Market", 90),
]

for crop, market, price in market_prices:

    cursor.execute("""
        SELECT price_id FROM market_prices
        WHERE crop_name = ?
        AND market_name = ?
        AND price_date = ?
    """, (crop, market, today))

    if cursor.fetchone() is None:

        cursor.execute("""
            INSERT INTO market_prices
            (crop_name, market_name, price, price_date)
            VALUES (?, ?, ?, ?)
        """, (crop, market, price, today))

# --------------------------------
# 5. SAMPLE CUSTOMER ENQUIRIES
# --------------------------------

enquiries = [
    (
        "demo_customer1",
        "demo_farmer1",
        "Tomato",
        "I am interested in purchasing tomatoes.",
        "Pending"
    ),
    (
        "demo_customer2",
        "demo_farmer2",
        "Carrot",
        "Please share the available quantity.",
        "Contacted"
    ),
    (
        "demo_customer3",
        "demo_farmer3",
        "Banana",
        "I would like to know more about the product.",
        "Pending"
    ),
    (
        "demo_customer1",
        "demo_farmer4",
        "Ragi",
        "I am interested in buying ragi.",
        "Completed"
    ),
]

for customer_username, farmer_username, product_name, message, status in enquiries:

    customer_id = customer_ids[customer_username]
    farmer_id = farmer_ids[farmer_username]
    product_id = product_ids[(farmer_username, product_name)]

    cursor.execute("""
        SELECT enquiry_id FROM enquiries
        WHERE customer_id = ?
        AND product_id = ?
        AND message = ?
    """, (customer_id, product_id, message))

    if cursor.fetchone() is None:

        cursor.execute("""
            INSERT INTO enquiries
            (customer_id, farmer_id, product_id, message, status)
            VALUES (?, ?, ?, ?, ?)
        """, (
            customer_id,
            farmer_id,
            product_id,
            message,
            status
        ))

# --------------------------------
# 6. SAVE ALL DATA
# --------------------------------

conn.commit()
conn.close()

print("====================================")
print("FARMERCONNECT DEMO DATA ADDED!")
print("====================================")
print("Farmers: 4")
print("Customers: 3")
print("Products: 12")
print("Market price records: 12")
print("Customer enquiries: 4")
print("====================================")
print("Demo password: Demo@12345")
print("====================================")