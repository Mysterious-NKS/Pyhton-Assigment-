import sqlite3
from menu_data import food_list, drink_list

def display_menu():
    print("\n=== MENU ===")
    
    print("\nFood:")
    print(f"+{'-' * 5}+{'-' * 15}+{'-' * 12}+{'-' * 52}+")
    print(f"|{'No.':<3} | {'Name':<13} | {'Price (RM)':<10} | {'Recipe':<50} |")
    print(f"+{'-' * 5}+{'-' * 15}+{'-' * 12}+{'-' * 52}+")

    for idx, item in enumerate(food_list, 1):
        print(f"| {idx:<3} | {item['name']:<13} | {item['price']:<10.2f} | {item['recipe']:<50} |")

    print(f"+{'-' * 5}+{'-' * 15}+{'-' * 12}+{'-' * 52}+")

    print("\nDrink:")
    print(f"+{'-' * 5}+{'-' * 15}+{'-' * 12}+{'-' * 52}+")
    print(f"|{'No.':<3} | {'Name':<13} | {'Price (RM)':<10} | {'Recipe':<50} |")
    print(f"+{'-' * 5}+{'-' * 15}+{'-' * 12}+{'-' * 52}+")

    for idx, item in enumerate(drink_list, len(food_list) + 1):
        print(f"| {idx:<3} | {item['name']:<13} | {item['price']:<10.2f} | {item['recipe']:<50} |")

    print(f"+{'-' * 5}+{'-' * 15}+{'-' * 12}+{'-' * 52}+")
    print("")

def view_cart(cart):
    if not cart:
        print("\nYour shopping cart is empty.")
        return
        
    print("\n=== Shopping Cart ===")
    total = 0
    for idx, item in enumerate(cart, 1):
        subtotal = item['price'] * item['quantity']
        total += subtotal
        print(f"{idx}. {item['name']} - RM{item['price']} x {item['quantity']} = RM{subtotal}")
    print(f"\nTotal Amount: RM{total}")

def get_all_items():
    return food_list + drink_list

def get_item_by_number(number):
    all_items = get_all_items()
    if 1 <= number <= len(all_items):
        return all_items[number - 1]
    return None 