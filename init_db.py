from database import engine
from models import Product

print("Creating MySQL table...")
Product.metadata.create_all(bind=engine)
print("✅ Done.")
