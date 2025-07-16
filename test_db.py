from app.db_handler import init_db, insert_product
init_db()
insert_product("விவசாயிகள்", "Farmers", "Auto-generated description")
print("Record inserted.")