from app import app, db, User, CartItem, WishlistItem

def verify():
    with app.app_context():
        # Check if tables exist
        engine = db.engine
        inspector = db.inspect(engine)
        tables = inspector.get_table_names()
        
        print(f"Tables in database: {tables}")
        
        required_tables = ['user', 'cart_item', 'wishlist_item']
        missing = [t for t in required_tables if t not in tables]
        
        if not missing:
            print("All required tables are present.")
        else:
            print(f"Missing tables: {missing}")
            # Try to create them
            db.create_all()
            print("Called db.create_all().")
            tables = inspector.get_table_names()
            print(f"Tables now: {tables}")

if __name__ == "__main__":
    verify()
