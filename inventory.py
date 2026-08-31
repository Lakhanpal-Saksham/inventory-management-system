from database import get_connection

class InventoryManager:
    @staticmethod
    def add_product(name, sku, category, quantity, price, reorder_level=5):
        with get_connection() as conn:
            cursor = conn.cursor()
            try:
                cursor.execute("""
                    INSERT INTO products (name, sku, category, quantity, price, reorder_level)
                    VALUES (?, ?, ?, ?, ?, ?)
                """, (name, sku, category, quantity, price, reorder_level))
                product_id = cursor.lastrowid
                
                # Log initial restock transaction
                cursor.execute("""
                    INSERT INTO transactions (product_id, change_type, quantity)
                    VALUES (?, 'RESTOCK', ?)
                """, (product_id, quantity))
                
                conn.commit()
                return True, "Product added successfully."
            except Exception as e:
                return False, f"Error: {e}"

    @staticmethod
    def update_stock(product_id, quantity, transaction_type):
        if quantity <= 0:
            return False, "Quantity must be positive."
            
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT quantity FROM products WHERE id = ?", (product_id,))
            row = cursor.fetchone()
            
            if not row:
                return False, "Product not found."
                
            current_qty = row[0]
            
            if transaction_type == "DISPATCH":
                if current_qty < quantity:
                    return False, f"Insufficient stock. Available: {current_qty}"
                new_qty = current_qty - quantity
            elif transaction_type == "RESTOCK":
                new_qty = current_qty + quantity
            else:
                return False, "Invalid transaction type."
                
            cursor.execute("UPDATE products SET quantity = ? WHERE id = ?", (new_qty, product_id))
            cursor.execute("""
                INSERT INTO transactions (product_id, change_type, quantity)
                VALUES (?, ?, ?)
            """, (product_id, transaction_type, quantity))
            
            conn.commit()
            return True, f"Stock updated successfully. New quantity: {new_qty}"

    @staticmethod
    def get_all_products():
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id, name, sku, category, quantity, price, reorder_level FROM products")
            return cursor.fetchall()

    @staticmethod
    def get_low_stock_items():
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id, name, sku, quantity, reorder_level FROM products WHERE quantity <= reorder_level")
            return cursor.fetchall()

    @staticmethod
    def delete_product(product_id):
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM products WHERE id = ?", (product_id,))
            conn.commit()
            return cursor.rowcount > 0
