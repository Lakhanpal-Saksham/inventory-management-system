from database import initialize_database
from inventory import InventoryManager

def print_menu():
    print("\n--- INVENTORY MANAGEMENT SYSTEM ---")
    print("1. View All Products")
    print("2. Add New Product")
    print("3. Restock / Dispatch Product")
    print("4. Check Low Stock Alerts")
    print("5. Delete Product")
    print("6. Exit")

def main():
    initialize_database()
    mgr = InventoryManager()

    while True:
        print_menu()
        choice = input("Select an option (1-6): ").strip()

        if choice == "1":
            products = mgr.get_all_products()
            if not products:
                print("Inventory is currently empty.")
            else:
                print("\nID | Name | SKU | Category | Qty | Price | Reorder Level")
                print("-" * 65)
                for p in products:
                    print(f"{p[0]} | {p[1]} | {p[2]} | {p[3]} | {p[4]} | ${p[5]:.2f} | {p[6]}")

        elif choice == "2":
            name = input("Product Name: ").strip()
            sku = input("SKU (unique code): ").strip()
            category = input("Category: ").strip()
            try:
                qty = int(input("Initial Quantity: "))
                price = float(input("Unit Price: "))
                reorder = int(input("Reorder Level (default 5): ") or 5)
                success, msg = mgr.add_product(name, sku, category, qty, price, reorder)
                print(msg)
            except ValueError:
                print("Invalid numerical input.")

        elif choice == "3":
            try:
                pid = int(input("Product ID: "))
                print("1. RESTOCK (Add stock)")
                print("2. DISPATCH (Remove stock)")
                op = input("Select type (1 or 2): ").strip()
                ttype = "RESTOCK" if op == "1" else "DISPATCH" if op == "2" else None
                if not ttype:
                    print("Invalid choice.")
                    continue
                qty = int(input("Quantity: "))
                success, msg = mgr.update_stock(pid, qty, ttype)
                print(msg)
            except ValueError:
                print("Invalid input.")

        elif choice == "4":
            low_stock = mgr.get_low_stock_items()
            if not low_stock:
                print("All products are above their reorder thresholds.")
            else:
                print("\n[ALERT] LOW STOCK PRODUCTS:")
                print("ID | Name | SKU | Current Qty | Reorder Level")
                print("-" * 50)
                for item in low_stock:
                    print(f"{item[0]} | {item[1]} | {item[2]} | {item[3]} | {item[4]}")

        elif choice == "5":
            try:
                pid = int(input("Enter Product ID to delete: "))
                if mgr.delete_product(pid):
                    print("Product deleted successfully.")
                else:
                    print("Product ID not found.")
            except ValueError:
                print("Invalid ID.")

        elif choice == "6":
            print("Exiting application. Goodbye!")
            break
        else:
            print("Invalid selection. Please choose 1 to 6.")

if __name__ == "__main__":
    main()
