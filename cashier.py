import sqlite3
import os
from database import load_users
from member import display_menu
from member import load_menu

def clear_screen():
    os.system("cls")

    
#1.0 login
def cashier_login():
    clear_screen()
    print("\n╔══════════════════════════════════╗")
    print("║        Cashier Login             ║")
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

        print("")
        choice = input("Choose an option: ")
        print("")

        if choice == "1":
            cashier_display_menu() #2.0
        elif choice == "2":
            change_order_status_menu() #3.0
        elif choice == "3":
            manage_discount_menu() #4.0
        elif choice == "4":
            generate_receipt_menu() #5.0
        elif choice == "5":
            generate_report_menu() #6.0
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
def change_order_status_menu():
    while True:
        display_orders()
        print("\n╔══════════════════════════════════╗")
        print("║       Change Order Status        ║")
        print("╚══════════════════════════════════╝")
        order_id = input("Enter the Order ID to update (or press Enter to return): ").strip()
        
        if order_id == '':
            break
        
        if not order_id.isdigit():
            print("Please enter a valid numeric Order ID.")
            continue
        
        new_status = input("Enter the new status ('completed', 'pending', 'cancelled' or press Enter to return): ").strip()
        if new_status.lower() not in ['completed', 'pending', 'cancelled']:
            print("Invalid status. Please enter 'completed', 'pending', or 'cancelled'.")
            continue
        
        update_order_status(int(order_id), new_status)

#3.2
def display_orders():
    try:
        conn = sqlite3.connect('users.db')
        cursor = conn.cursor()

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

#3.3
def update_order_status(order_id, new_status):
    try:
        conn = sqlite3.connect('users.db')
        cursor = conn.cursor()

        cursor.execute('''
        UPDATE orders
        SET status = ?
        WHERE order_id = ?
        ''', (new_status, order_id))

        conn.commit()

        if cursor.rowcount > 0:
            print("")
            print(f"Order ID {order_id} status updated to '{new_status}'.")
        else:
            print(f"No order found with ID {order_id}.")

    except sqlite3.Error as e:
        print(f"An error occurred: {e}")

    finally:
        if conn:
            conn.close()


#
#
#4.1
def manage_discount_menu():
    while True:
        print("\n╔══════════════════════════════════╗")
        print("║         Manage Discount          ║")
        print("╚══════════════════════════════════╝")
        print("1. Apply Discount to Order")
        print("2. Remove Discount from Order (Restore Original Price)")
        print("0. Return to Cashier Menu")
        print(" ")

        choice = input("Choose an option: ")

        if choice == "1":
            clear_screen()
            try:
                display_orders()
                print("")
                order_id = int(input("Enter the Order ID to apply a discount: "))
                discount_percent = float(input("Enter the discount percentage: "))
                apply_discount_to_order(order_id, discount_percent)
            except ValueError:
                print("Invalid input. Please enter numeric values for Order ID and discount percentage.")
                print("")

        elif choice == "2":
            clear_screen()
            try:
                display_orders()
                print("")
                order_id = int(input("Enter the Order ID to remove the discount: "))
                restore_original_price(order_id)
                print("")
            except ValueError:
                print("Invalid input. Please enter a valid Order ID.")
                print("")

        elif choice == "0":
            break

        else:
            print("Invalid choice. Please try again.")
            print("")

#4.2
def apply_discount_to_order(order_id, discount_percent):
    try:
        conn = sqlite3.connect('users.db')
        cursor = conn.cursor()

        cursor.execute('SELECT total_amount FROM orders WHERE order_id = ?', (order_id,))
        result = cursor.fetchone()

        if result:
            current_total = result[0]
            new_total = current_total * (1 - discount_percent / 100)
            
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

#4.3
def restore_original_price(order_id):
    try:
        conn = sqlite3.connect('users.db')
        cursor = conn.cursor()

        cursor.execute('''
            SELECT SUM(price * quantity) 
            FROM order_items 
            WHERE order_id = ?
        ''', (order_id,))
        result = cursor.fetchone()

        if result and result[0] is not None:
            original_total = result[0]
            
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
def generate_receipt_menu():
    while True:
        print("\n╔══════════════════════════════════╗")
        print("║      Generate Receipt Menu       ║")
        print("╚══════════════════════════════════╝")
        display_orders()
        print("")
        order_id = input("Enter the Order ID to generate the receipt (or press 'enter' to quit): ")
        if order_id.lower() == '':
            print("Exiting receipt menu.")
            break
        try:
            order_id = int(order_id)
            generate_receipt(order_id)
            save_choice = input("Would you like to save the receipt to a file? (y/n): ").strip().lower()
            if save_choice == 'y':
                filename = input("Enter the filename (default: receipt.txt): ").strip()
                if not filename:
                    filename = "receipt.txt"
                generate_receipt_to_file(order_id, filename)
        except ValueError:
            print("Invalid input. Please enter a valid Order ID.")

#5.2
def generate_receipt(order_id):
    clear_screen()
    print("\n╔══════════════════════════════════╗")
    print("║         Generate Receipt         ║")
    print("╚══════════════════════════════════╝")

    try:
        conn = sqlite3.connect('users.db')
        cursor = conn.cursor()

        cursor.execute('''
        SELECT o.order_id, o.total_amount, o.status, o.order_date,
               GROUP_CONCAT(oi.item_name || ' (x' || oi.quantity || ') || RM' || ROUND(oi.price, 2)) as items
        FROM orders o
        LEFT JOIN order_items oi ON o.order_id = oi.order_id
        WHERE o.order_id = ?
        GROUP BY o.order_id
        ''', (order_id,))

        order = cursor.fetchone()

        if not order:
            print("Order not found.")
            return

        order_id, total_amount, status, order_date, items = order

        print("\n======== Receipt ========")
        print("Thank you for your order!")
        print("-" * 30)
        print(f"Order ID: {order_id}")
        print(f"Date: {order_date}")
        print("-" * 30)
        print("Items Ordered:")
        if items:
            item_lines = items.split("||")
            for line in item_lines:
                print(f"  {line.strip()}")
        print("-" * 30)
        print(f"Total: RM{total_amount:.2f}")
        print(f"Status: {status.capitalize()}")
        print("-" * 30)
        print("Please visit again!")
        print("")

    except sqlite3.Error as e:
        print(f"Error generating receipt: {e}")
    finally:
        if conn:
            conn.close()

#5.3
def generate_receipt_to_file(order_id, filename='receipt.txt'):
    """Generate and save the receipt to a file."""
    try:
        conn = sqlite3.connect('users.db')
        cursor = conn.cursor()

        cursor.execute('''
        SELECT o.order_id, o.total_amount, o.status, o.order_date,
               GROUP_CONCAT(oi.item_name || ' (x' || oi.quantity || ') || RM' || ROUND(oi.price, 2)) as items
        FROM orders o
        LEFT JOIN order_items oi ON o.order_id = oi.order_id
        WHERE o.order_id = ?
        GROUP BY o.order_id
        ''', (order_id,))

        order = cursor.fetchone()

        if not order:
            print("Order not found.")
            return

        order_id, total_amount, status, order_date, items = order

        with open(filename, 'w') as file:
            file.write("=== Receipt ===\n")
            file.write("Thank you for your order!\n")
            file.write("-" * 30 + "\n")
            file.write(f"Order ID: {order_id}\n")
            file.write(f"Date: {order_date}\n")
            file.write("-" * 30 + "\n")
            file.write("Items Ordered:\n")
            if items:
                item_lines = items.split("||")
                for line in item_lines:
                    file.write(f"  {line.strip()}\n")
            file.write("-" * 30 + "\n")
            file.write(f"Total: RM{total_amount:.2f}\n")
            file.write(f"Status: {status.capitalize()}\n")
            file.write("-" * 30 + "\n")
            file.write("Please visit again!\n")

        print(f"Receipt saved to {filename}.")

    except sqlite3.Error as e:
        print(f"Error generating receipt: {e}")
    finally:
        if conn:
            conn.close()


#
#
#6.1
def generate_report_menu():
    while True:
        print("\n╔══════════════════════════════════╗")
        print("║        Sales Report Menu         ║")
        print("╚══════════════════════════════════╝")
        print("1. Generate Sales Report")
        print("2. Generate Product Popularity Report")
        print("0. Exit")
        
        choice = input("Choose an option: ")

        if choice == '1':
            clear_screen()
            generate_sales_report()
        elif choice == '2':
            clear_screen()
            generate_product_popularity_report()
        elif choice == '0':
            print("Exiting report generation.")
            break
        else:
            print("Invalid choice, please try again.")

#6.2
def generate_sales_report():
    try:
        conn = sqlite3.connect('users.db')
        cursor = conn.cursor()

        cursor.execute('''
            SELECT SUM(total_amount) FROM orders WHERE status = 'completed'
        ''')
        total_sales = cursor.fetchone()[0]
        total_sales = total_sales if total_sales else 0.0

        print("\n╔══════════════════════════════════╗")
        print("║     Sales Performance Report     ║")
        print("╚══════════════════════════════════╝")
        print(f"Total Sales (Completed Orders): RM{total_sales:.2f}")

    except sqlite3.Error as e:
        print(f"An error occurred while generating the sales report: {e}")
    
    finally:
        if conn:
            conn.close()

#6.3
def generate_product_popularity_report():
    try:
        conn = sqlite3.connect('users.db')
        cursor = conn.cursor()

        cursor.execute('''
            SELECT item_name, SUM(quantity) AS total_quantity
            FROM order_items
            GROUP BY item_name
            ORDER BY total_quantity DESC
        ''')
        items = cursor.fetchall()

        print("\n╔══════════════════════════════════╗")
        print("║     Product Popularity Report    ║")
        print("╚══════════════════════════════════╝")
        if items:
            for item in items:
                item_name, total_quantity = item
                print(f"{item_name}: {total_quantity} ordered")
        else:
            print("No order data available.")

    except sqlite3.Error as e:
        print(f"An error occurred while generating the product popularity report: {e}")
    
    finally:
        if conn:
            conn.close()