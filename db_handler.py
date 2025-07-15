import sqlite3

def init_db():
    conn = sqlite3.connect("catalog.db")
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            original_input TEXT,
            translated_input TEXT,
            description TEXT
        )
    ''')
    conn.commit()
    conn.close()

def insert_product(original, translated, description):
    conn = sqlite3.connect("catalog.db")
    c = conn.cursor()
    c.execute('''
        INSERT INTO products (original_input, translated_input, description)
        VALUES (?, ?, ?)
    ''', (original, translated, description))
    conn.commit()
    conn.close()
