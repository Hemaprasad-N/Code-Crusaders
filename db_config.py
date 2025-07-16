# db_config.py

import mysql.connector

def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="Magesh#2004",
        database="cat_db" 
    )
import mysql.connector