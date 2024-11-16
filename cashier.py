from chef import food_list, drink_list
from database import load_users
from member import clear_screen
from member import browse_menu

current_order = {}
sales_records = []
discounts = {}

def cashier_login():
    clear_screen()
    print("\n╔══════════════════════════════════╗")
    print("║        Cashier Login              ║")
    print("╚══════════════════════════════════╝")
    while True:
        username = input("Please enter a username (press enter to undo) ► ")
        if username.lower() == '':
            return
        password = input("Please enter a password: ")

        users = load_users()
        user_dict = {user[0]: user for user in users}

        user = user_dict.get(username)
        if user and user[1] == password and user[2] == 'cashier':
            print("Login successful!")
            cashier_menu()
            break
        else:
            print("Username or password is incorrect, or you are not a cashier. Please try again.")

def cashier_menu():
    global current_order  # Move this to the beginning of the function
    clear_screen()
    while True:
        print("\n╔══════════════════════════════════╗")
        print("║        Cashier Menu              ║")
        print("╚══════════════════════════════════╝")
        print("1. View Menu")
        print("2. Check Member Order")
        print("3. Manage Discounts")
        print("4. Generate Receipt")
        print("5. Generate Sales Report")
        print("0. Exit")
        choice = input("Choose an option: ")

        if choice == "1":
            cashier_display_menu()
        elif choice == "2":
            check_order_menu()
        elif choice == "3":
            manage_discount_menu()
        elif choice == "4":
            generate_receipt(current_order)
            record_transaction(current_order)  # Record transaction after generating receipt
            current_order = {}  # Clear the order after generating receipt
        elif choice == "5":
            generate_sales_report()
        elif choice == "0":
            print("Exiting Cashier Menu...")
            break
        else:
            print("Invalid choice, please try again.")

def cashier_display_menu():
    clear_screen()
    browse_menu()

# Initialize a dictionary to store the current order
current_order = {}

def check_order_menu():
    print("==== Take Order ====")
    while True:
        all_items = food_list + drink_list
        print("Available items to order:")
        for idx, item in enumerate(all_items, 1):
            print(f"{idx}. {item['name']} - RM{item['price']} ({item['recipe']})")
        
        choice = input("\nPlease enter the item number to add into cart, or press enter to finish: ").strip()
        
        if choice == '':
            print("Order complete!")
            break
        
        if not choice.isdigit():
            print("Please enter a valid number.")
            continue
            
        choice = int(choice)
        
        if 1 <= choice <= len(all_items):
            selected_item = all_items[choice - 1]
            try:
                quantity = int(input(f"Enter quantity for {selected_item['name']}: "))
                if quantity <= 0:
                    print("Quantity must be greater than zero.")
                    continue
                
                if selected_item['name'] in current_order:
                    current_order[selected_item['name']]['quantity'] += quantity
                else:
                    current_order[selected_item['name']] = {
                        'price': selected_item['price'], 
                        'quantity': quantity
                    }
                
                print(f"{quantity} x {selected_item['name']} added to the order.")
            except ValueError:
                print("Invalid quantity, please enter a number.")
        else:
            print("Invalid option, please try again.")
    
    # 显示订单摘要
    if current_order:
        print("\nOrder Summary:")
        for item, details in current_order.items():
            print(f"{item}: {details['quantity']} x RM{details['price']} each")
        print("")
    else:
        print("No items in order.")


def manage_discount_menu():
    while True:
        print("\n==== Manage Discounts ====")
        print("1. Add Discount")
        print("2. Remove Discount")
        print("0. Return to Cashier Menu")
        choice = input("Choose an option: ")

        if choice == "1":
            item_name = input("Enter item name to add a discount: ")
            discount_percent = float(input("Enter discount percentage: "))
            add_discount(item_name, discount_percent)
        elif choice == "2":
            item_name = input("Enter item name to remove discount: ")
            remove_discount(item_name)
        elif choice == "0":
            break
        else:
            print("Invalid choice, please try again.")


# Dictionary to store discounts specifically for current order items
discounts = {}  # Example format: {'Burger': 10} for 10% off on Burger

def add_discount(item_name, discount_percent):
    if item_name in current_order:  # Only apply discount to items in the current order
        discounts[item_name] = discount_percent
        print(f"Discount of {discount_percent}% added for {item_name}.")
    else:
        print(f"Item '{item_name}' is not in the current order.")

def remove_discount(item_name):
    if item_name in discounts:
        del discounts[item_name]
        print(f"Discount removed for {item_name}.")
    else:
        print(f"No discount found for '{item_name}'.")

def generate_receipt(order):
    print("\n--- Receipt ---")
    total = 0
    for item, details in order.items():
        price = details["price"]
        quantity = details["quantity"]
        item_total = price * quantity

        # Check if a discount applies
        if item in discounts:
            discount = discounts[item]
            item_total *= (1 - discount / 100)  # Apply discount
            print(f"{item} x{quantity} - RM{price} each - {discount}% off - Subtotal: RM{round(item_total, 2)}")
        else:
            print(f"{item} x{quantity} - RM{price} each - Subtotal: RM{round(item_total, 2)}")

        total += item_total

    print(f"\nTotal: RM{round(total, 2)}")
    print("\nThank you for your order!\n")

sales_records = []  # Global list to store each transaction

def record_transaction(order):
    transaction = []
    for item, details in order.items():
        item_record = {
            "name": item,
            "quantity": details["quantity"],
            "price": details["price"],
            "discount": discounts.get(item, 0),  # Fetch discount if it exists, otherwise 0
        }
        transaction.append(item_record)
    sales_records.append(transaction)
    print("Transaction recorded.")


def generate_sales_report():
    print("\n--- Sales Report ---")
    total_sales = 0
    item_summary = {}
    total_discounted_amount = 0

    for transaction in sales_records:
        for item in transaction:
            item_name = item["name"]
            quantity = item["quantity"]
            price = item["price"]
            discount_percent = item["discount"]

            # Calculate item sales and discounts
            subtotal = price * quantity
            discount_amount = subtotal * (discount_percent / 100)
            discounted_total = subtotal - discount_amount

            # Update total sales
            total_sales += discounted_total
            total_discounted_amount += discount_amount

            # Track item popularity
            if item_name not in item_summary:
                item_summary[item_name] = {
                    "quantity_sold": 0,
                    "revenue": 0,
                }
            item_summary[item_name]["quantity_sold"] += quantity
            item_summary[item_name]["revenue"] += discounted_total

    # Display report
    print(f"\nTotal Sales Revenue: RM{round(total_sales, 2)}")
    print(f"Total Discounts Given: RM{round(total_discounted_amount, 2)}")

    print("\nItem Popularity:")
    for item, data in item_summary.items():
        print(f"{item} - Quantity Sold: {data['quantity_sold']}, Revenue: RM{round(data['revenue'], 2)}")

    print("\n--- End of Report ---")