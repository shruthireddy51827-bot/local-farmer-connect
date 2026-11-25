
import sqlite3

DB_NAME = "farmer_market.db"

def get_connection():
    return sqlite3.connect(DB_NAME)

def initialize_database():

    conn = get_connection()
    cursor = conn.cursor()

    # Farmers table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS farmers (
        farmer_id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        phone TEXT NOT NULL,
        village TEXT NOT NULL,
        username TEXT UNIQUE NOT NULL,
        password_hash TEXT NOT NULL
    )
    """)

    # Customers table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS customers (
        customer_id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        phone TEXT NOT NULL,
        username TEXT UNIQUE NOT NULL,
        password_hash TEXT NOT NULL
    )
    """)

    # Products table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS products (
        product_id INTEGER PRIMARY KEY AUTOINCREMENT,
        farmer_id INTEGER NOT NULL,
        product_name TEXT NOT NULL,
        category TEXT NOT NULL,
        quantity REAL NOT NULL,
        price REAL NOT NULL,
        image_path TEXT,
        availability TEXT DEFAULT 'Available',
        FOREIGN KEY (farmer_id)
        REFERENCES farmers(farmer_id)
    )
    """)

    # Market prices table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS market_prices (
        price_id INTEGER PRIMARY KEY AUTOINCREMENT,
        crop_name TEXT NOT NULL,
        market_name TEXT NOT NULL,
        price REAL NOT NULL,
        price_date TEXT NOT NULL
    )
    """)

    # Enquiries table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS enquiries (
        enquiry_id INTEGER PRIMARY KEY AUTOINCREMENT,
        customer_id INTEGER NOT NULL,
        farmer_id INTEGER NOT NULL,
        product_id INTEGER NOT NULL,
        message TEXT,
        status TEXT DEFAULT 'Pending'
    )
    """)

    conn.commit()
    conn.close()

    print("Database created successfully!")

if __name__ == "__main__":
    initialize_database()