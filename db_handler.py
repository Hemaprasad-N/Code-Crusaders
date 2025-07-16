import sqlite3

DATABASE_NAME = "products.db"

def init_db():
    """Initializes the SQLite database and creates the products table."""
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            original_text TEXT NOT NULL,
            translated_text TEXT NOT NULL,
            description TEXT NOT NULL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()

def insert_product(original_text: str, translated_text: str, description: str):
    """Inserts a new product entry into the database."""
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO products (original_text, translated_text, description) VALUES (?, ?, ?)",
        (original_text, translated_text, description)
    )
    conn.commit()
    conn.close()
    print(f"Product inserted: Original='{original_text}', Translated='{translated_text}'")

def get_all_products():
    """Retrieves all product entries from the database."""
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT original_text, translated_text, description, timestamp FROM products ORDER BY timestamp DESC")
    products = []
    for row in cursor.fetchall():
        products.append({
            "original_text": row[0],
            "translated_text": row[1],
            "description": row[2],
            "timestamp": row[3]
        })
    conn.close()
    return products

# Initialize the database when the module is imported
init_db()
