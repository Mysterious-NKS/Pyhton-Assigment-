import sqlite3
from database import load_users
from member import clear_screen
from member import display_menu
from member import load_menu

# In cashier.py

def some_function():
    from cashier import display_orders  # Local import to avoid circular import
    # Now you can use display_orders here

current_order = {}
sales_records = []
discounts = {}

#1.0 login
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

#
#
#1.1 menu
def cashier_menu():
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
            cashier_display_menu() #2.0
        elif choice == "2":
            change_order_status_menu() #3.0
        elif choice == "3":
            manage_discount_menu() #4.0
        elif choice == "4":
            generate_receipt_menu() #5.0
        elif choice == "5":
            generate_sales_report()
        elif choice == "0":
            print("Exiting Cashier Menu...")
            break
        else:
            print("Invalid choice, please try again.")

#
#
#2.1
def cashier_display_menu():
    clear_screen()
    load_menu()
    menu = load_menu()
    display_menu(menu)


#
#
#3.1
def display_orders():
    try:
        conn = sqlite3.connect('users.db')
        cursor = conn.cursor()
        
        # Fetch all orders
        cursor.execute('SELECT order_id, user_id, total_amount, status, order_date FROM orders')
        orders = cursor.fetchall()
        
        if orders:
            print("\n==== Orders List ====")
            print(f"+{'-'*10}+{'-'*10}+{'-'*15}+{'-'*12}+{'-'*20}+")
            print(f"| {'Order ID':<8} | {'User ID':<8} | {'Total (RM)':<13} | {'Status':<10} | {'Order Date':<18} |")
            print(f"+{'-'*10}+{'-'*10}+{'-'*15}+{'-'*12}+{'-'*20}+")
            
            for order in orders:
                order_id, user_id, total_amount, status, order_date = order
                print(f"| {order_id:<8} | {user_id:<8} | {total_amount:<13.2f} | {status:<10} | {order_date:<18} |")
            
            print(f"+{'-'*10}+{'-'*10}+{'-'*15}+{'-'*12}+{'-'*20}+")
        else:
            print("\nNo orders found.")
    
    except sqlite3.Error as e:
        print(f"An error occurred: {e}")
    
    finally:
        if conn:
            conn.close()

def update_order_status(order_id, new_status):
    try:
        conn = sqlite3.connect('users.db')
        cursor = conn.cursor()
        
        # Update the order status
        cursor.execute('''
        UPDATE orders
        SET status = ?
        WHERE order_id = ?
        ''', (new_status, order_id))
        
        conn.commit()
        
        if cursor.rowcount > 0:
            print(f"Order ID {order_id} status updated to '{new_status}'.")
        else:
            print(f"No order found with ID {order_id}.")
    
    except sqlite3.Error as e:
        print(f"An error occurred: {e}")
    
    finally:
        if conn:
            conn.close()

def change_order_status_menu():
    while True:
        # Display the list of orders
        display_orders()
        
        print("\n==== Change Order Status ====")
        order_id = input("Enter the Order ID to update (or press Enter to return): ").strip()
        
        if order_id == '':
            break
        
        if not order_id.isdigit():
            print("Please enter a valid numeric Order ID.")
            continue
        
        new_status = input("Enter the new status ('completed', 'pending', 'cancelled'): ").strip()
        if new_status.lower() not in ['completed', 'pending', 'cancelled']:
            print("Invalid status. Please enter 'completed', 'pending', or 'cancelled'.")
            continue
        
        update_order_status(int(order_id), new_status)

#
#
#4.1
def apply_discount_to_order(order_id, discount_percent):
    try:
        conn = sqlite3.connect('users.db')
        cursor = conn.cursor()

        # Fetch the current total amount for the order
        cursor.execute('SELECT total_amount FROM orders WHERE order_id = ?', (order_id,))
        result = cursor.fetchone()

        if result:
            current_total = result[0]
            # Calculate the discounted total
            new_total = current_total * (1 - discount_percent / 100)
            
            # Update the total_amount in the database
            cursor.execute('UPDATE orders SET total_amount = ? WHERE order_id = ?', (new_total, order_id))
            conn.commit()
            
            print(f"Discount of {discount_percent}% applied to Order ID {order_id}.")
            print(f"Updated Total Amount: RM{new_total:.2f}")
        else:
            print(f"Order ID {order_id} not found.")
    
    except sqlite3.Error as e:
        print(f"An error occurred while applying the discount: {e}")
    
    finally:
        if conn:
            conn.close()

def manage_discount_menu():
    while True:
        clear_screen()
        # Show the current orders before allowing discount management 
        display_orders()
        print("\n==== Manage Discounts ====")
        print("1. Apply Discount to Order")
        print("2. Remove Discount from Order (Restore Original Price)")
        print("0. Return to Cashier Menu")
        choice = input("Choose an option: ")

        if choice == "1":
            try:
                order_id = int(input("Enter the Order ID to apply a discount: "))
                discount_percent = float(input("Enter the discount percentage: "))
                apply_discount_to_order(order_id, discount_percent)
            except ValueError:
                print("Invalid input. Please enter numeric values for Order ID and discount percentage.")
        
        elif choice == "2":
            try:
                order_id = int(input("Enter the Order ID to remove the discount: "))
                restore_original_price(order_id)
            except ValueError:
                print("Invalid input. Please enter a valid Order ID.")
        
        elif choice == "0":
            break
        
        else:
            print("Invalid choice. Please try again.")

def restore_original_price(order_id):
    try:
        conn = sqlite3.connect('users.db')
        cursor = conn.cursor()

        # Fetch the order items to calculate the original total
        cursor.execute('''
            SELECT SUM(price * quantity) 
            FROM order_items 
            WHERE order_id = ?
        ''', (order_id,))
        result = cursor.fetchone()

        if result and result[0] is not None:
            original_total = result[0]
            
            # Update the total_amount in the orders table
            cursor.execute('UPDATE orders SET total_amount = ? WHERE order_id = ?', (original_total, order_id))
            conn.commit()
            
            print(f"Discount removed for Order ID {order_id}.")
            print(f"Restored Total Amount: RM{original_total:.2f}")
        else:
            print(f"No items found for Order ID {order_id}.")
    
    except sqlite3.Error as e:
        print(f"An error occurred while restoring the original price: {e}")
    
    finally:
        if conn:
            conn.close()


#
# 
# 5.1
def generate_receipt(order_id):
    try:
        conn = sqlite3.connect('users.db')
        cursor = conn.cursor()

        # Get order details
        cursor.execute('''
            SELECT users.username, orders.total_amount, orders.status, orders.order_date
            FROM orders
            JOIN users ON orders.user_id = users.id
            WHERE orders.order_id = ?
        ''', (order_id,))
        order_details = cursor.fetchone()

        if not order_details:
            print(f"Order ID {order_id} not found.")
            return

        username, total_amount, status, order_date = order_details

        # Print the receipt header
        print("\n==== Receipt ====")
        print(f"Order ID: {order_id}")
        print(f"Customer: {username}")
        print(f"Order Date: {order_date}")
        print(f"Status: {status}")
        print("-" * 30)

        # Get the order items
        cursor.execute('''
            SELECT item_name, price, quantity 
            FROM order_items 
            WHERE order_id = ?
        ''', (order_id,))
        items = cursor.fetchall()

        if items:
            total_price = 0
            for item_name, price, quantity in items:
                subtotal = price * quantity
                total_price += subtotal
                print(f"{item_name:<20}{price:<10.2f}{quantity:<10}{subtotal:<10.2f}")
        
            print("-" * 30)
            print(f"{'Total Amount:':<30} RM{total_price:.2f}")
        else:
            print("No items found for this order.")
        
        # Update the order status to 'completed'
        cursor.execute('''
            UPDATE orders
            SET status = 'completed'
            WHERE order_id = ?
        ''', (order_id,))
        conn.commit()

        print("\nReceipt Generated Successfully!")
    
    except sqlite3.Error as e:
        print(f"An error occurred while generating the receipt: {e}")
    
    finally:
        if conn:
            conn.close()

def generate_receipt_menu():
    while True:
        # Show the list of orders before generating the receipt
        display_orders()

        # Ask the cashier to select an order ID to generate receipt
        order_id = input("\nEnter the Order ID to generate a receipt, or press enter to return: ").strip()

        if order_id == '':
            break
        elif order_id.isdigit():
            order_id = int(order_id)
            generate_receipt(order_id)
        else:
            print("Invalid input. Please enter a valid Order ID.")


#6.1
def generate_sales_report():
    pass