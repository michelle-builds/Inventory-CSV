# ex6_inventory_csv.py

# Inventory management tool — view, add, search, update, and delete items from a CSV file.

import csv
import os

filename = "inventory.csv"

headers = ["dept_code", "vendor", "product_name", "product_size", "regular_price", "landed_retail_price", "order_sku"]
sample_data = [
    ["DELI", "Maple Leaf", "Turkey Breast Sliced", "200g", 6.99, 5.49, "ML-4421"],
    ["DELI", "Schneiders", "Black Forest Ham", "175g", 5.99, 4.75, "SC-1132"],
    ["PRODUCE", "Naturipe", "Strawberries", "1lb", 4.99, 3.20, "NP-8801"],
    ["DAIRY", "Dairyland", "Homo Milk", "4L", 7.49, 5.90, "DL-0042"],
    ["GROCERY", "Heinz", "Ketchup", "1kg", 5.49, 3.85, "HZ-3310"],
]

if not os.path.exists(filename):
    with open(filename, "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(headers)
        writer.writerows(sample_data)

    print(f"{filename} was created")

def view_inventory():
    print("\n=== INVENTORY LIST ===")
    print("--------------------")

    with open(filename, "r", newline="") as file:
        reader = csv.DictReader(file)
        for row in reader:
            print(f"{row['dept_code']} | {row['vendor']} | {row['product_name']} | {row['product_size']} | ${float(row['regular_price']):.2f} | ${float(row['landed_retail_price']):.2f} | {row['order_sku']}")

def add_inventory_item():
    print("\n=== ADD INVENTORY ITEM ===")

    valid_depts = ["FRZ", "CHI", "PRO", "DRY", "CON", "BAK", "MEAT", "PRP", "GNF"]

    print("\nDepartment codes:")
    for code in valid_depts:
        print(f"  {code}")

    while True:
        dept_code = input("Enter dept code: ").strip().upper()
        if dept_code in valid_depts:
            break
        print(f"Invalid dept code. Please choose from the list above.")

    vendor = input("Enter vendor: ").strip()
    product_name = input("Enter product name: ").strip()
    product_size = input("Enter product size: ").strip()

    while True:
        try:
            regular_price = float(input("Enter regular price: ").strip())
            break
        except ValueError:
            print("Invalid price. Please enter a number like 5.99.")

    while True:
        try:
            landed_retail_price = float(input("Enter landed retail price: ").strip())
            break
        except ValueError:
            print("Invalid price. Please enter a number like 5.99.")

    order_sku = input("Enter order SKU: ").strip()

    new_row = [dept_code, vendor, product_name, product_size, regular_price, landed_retail_price, order_sku]

    with open(filename, "a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(new_row)

    print(f"{product_name} added to inventory.")

def search_inventory():
    print("\n=== SEARCH INVENTORY ===")
    print("1. Search by dept code")
    print("2. Search by product name")

    choice = input("\nEnter your choice (1-6): ").strip()

    if choice == "1":
        search_term = input("Enter dept code: ").strip().upper()
        search_field = "dept_code"
    elif choice == "2":
        search_term = input("Enter product name: ").strip().lower()
        search_field = "product_name"
    else:
        print("Invalid choice.")
        return

    print("\n=== SEARCH RESULTS ===")
    print("--------------------")
    found = False

    with open(filename, "r", newline="") as file:
        reader = csv.DictReader(file)
        for row in reader:
            if search_term in row[search_field].lower():
                print(f"{row['dept_code']} | {row['vendor']} | {row['product_name']} | {row['product_size']} | ${float(row['regular_price']):.2f} | ${float(row['landed_retail_price']):.2f} | {row['order_sku']}")
                found = True

    if not found:
        print("No results found.")

def delete_inventory_item():
    print("\n=== DELETE INVENTORY ITEM ===")
    search_term = input("Enter product name to delete: ").strip().lower()

    with open(filename, "r", newline="") as file:
        reader = csv.DictReader(file)
        rows = list(reader)

    matches = [row for row in rows if search_term in row["product_name"].lower()]

    if not matches:
        print("No matching products found.")
        return

    print("\nMatching items:")
    for i, row in enumerate(matches):
        print(f"{i + 1}. {row['dept_code']} | {row['vendor']} | {row['product_name']} | {row['order_sku']}")

    choice = input("\nEnter number to delete (or 0 to cancel): ").strip()

    if choice == "0":
        print("Cancelled.")
        return

    row_to_delete = matches[int(choice) - 1]
    rows = [row for row in rows if row != row_to_delete]

    with open(filename, "w", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=headers)
        writer.writeheader()
        writer.writerows(rows)

    print(f"{row_to_delete['product_name']} deleted.")

def update_inventory_item():
    print("\n=== UPDATE INVENTORY ITEM ===")
    search_term = input("Enter product name to update: ").strip().lower()

    with open(filename, "r", newline="") as file:
        reader = csv.DictReader(file)
        rows = list(reader)

    matches = [row for row in rows if search_term in row["product_name"].lower()]

    if not matches:
        print("No matching products found.")
        return

    print("\nMatching items:")
    for i, row in enumerate(matches):
        print(f"{i + 1}. {row['dept_code']} | {row['vendor']} | {row['product_name']} | {row['order_sku']}")

    choice = input("\nEnter number to update (or 0 to cancel): ").strip()

    if choice == "0":
        print("Cancelled.")
        return

    row_to_update = matches[int(choice) - 1]

    print("\nLeave field blank to keep current value.")
    for field in headers:
        current = row_to_update[field]
        new_value = input(f"{field} [{current}]: ").strip()
        if new_value != "":
            row_to_update[field] = new_value

    with open(filename, "w", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=headers)
        writer.writeheader()
        writer.writerows(rows)

    print(f"{row_to_update['product_name']} updated.")

def main_menu():
    while True:
        print("\n=== INVENTORY MENU ===")
        print("1. View all inventory")
        print("2. Add item")
        print("3. Search inventory")
        print("4. Delete item")
        print("5. Update item")
        print("6. Quit")

        choice = input("\nEnter your choice (1-6): ").strip()

        if choice == "1":
            view_inventory()
        elif choice == "2":
            add_inventory_item()
        elif choice == "3":
            search_inventory()
        elif choice == "4":
            delete_inventory_item()
        elif choice == "5":
            update_inventory_item()
        elif choice == "6":
            print("Goodbye.")
            break
        else:
            print("Invalid choice. Please enter 1-6.")

main_menu()