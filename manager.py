from datetime import datetime
from database import load_users
import sqlite3
import shutil

def terminal_size():
    #Get the terminal size dynamically.
    size = shutil.get_terminal_size(fallback=(145, 24))  # Default to 145 width, 24 height
    return size.lines, size.columns


def custom_clear_screen():
    # Push previous content down
    print("\n" * 20, end="")  # Push content out of view



def print_centered_box(columns):
    #Print the login box centered horizontally with colours.
    # Define the box width explicitly
    box_width = 60
    padding = (columns - box_width) // 2

    # Box lines with darker blue
    print(" " * padding + "\033[34m╔" + "═" * (box_width - 2) + "╗\033[0m")
    print(" " * padding + "\033[34m║" + " " * ((box_width - 22) // 2) +
          "\033[1;36mManager Login Page" + "\033[34m" + " " * ((box_width - 18) // 2) + "║\033[0m")
    print(" " * padding + "\033[34m╚" + "═" * (box_width - 2) + "╝\033[0m")


def manager_login():
    while True:
        custom_clear_screen()  # Clear the screen at the start
        rows, columns = terminal_size()  # Get terminal dimensions

        # Place the box at the top-middle of the terminal
        top_padding = 2  # Adjust for top spacing
        print("\n" * top_padding)

        # Print the centered box with updated colours
        print_centered_box(columns)

        # Center the input fields horizontally
        input_width = 40  # Approximate width of the input prompt
        username = input("\n" + " " * ((columns - input_width) // 2) + "\033[1;36mEnter your username: \033[0m").strip()
        password = input(" " * ((columns - input_width) // 2) + "\033[1;36mEnter your password: \033[0m").strip()

        users = load_users()
        user_dict = {user[0]: user for user in users}
        user = user_dict.get(username)

        if user and user[1] == password and user[2] == 'manager':
            custom_clear_screen()  # Clear the screen before showing the success message
            print("\n" * top_padding)
            print_centered_box(columns)
            print("\n" + " " * ((columns - input_width) // 2) + "\033[1;36m✓ Login successful! Welcome, Manager.\033[0m")
            input("\n" + " " * ((columns - input_width) // 2) + "\033[1;36mPress Enter to continue...\033[0m")
            manager_menu()  # Proceed to the manager menu
            break
        else:
            custom_clear_screen()  # Clear the screen before showing the error message
            print("\n" * top_padding)
            print_centered_box(columns)
            print("\n" + " " * ((columns - input_width) // 2) + "\033[1;36m❌ Username or password is incorrect.\033[0m")
            retry = input("\n" + " " * ((columns - input_width) // 2) + "\033[1;36mRetry? (y/n): \033[0m").strip().lower()
            if retry != 'y':
                custom_clear_screen()
                print("\n" * top_padding)
                print_centered_box(columns)
                print("\n" + " " * ((columns - input_width) // 2) + "\033[1;36mReturning to the main menu...\033[0m")
                break


def manager_menu():
    """Displays the manager menu."""
    while True:
        custom_clear_screen()  # Clear the screen at the start
        rows, columns = terminal_size()  # Get terminal dimensions

        # Define the box width explicitly
        box_width = 60
        padding = (columns - box_width) // 2
        top_padding = 2  # Adjust for top spacing

        # Place the box at the top-middle of the terminal
        print("\n" * top_padding)

        # Box lines with darker blue
        print(" " * padding + "\033[34m╔" + "═" * (box_width - 2) + "╗\033[0m")
        print(" " * padding + "\033[34m║" + " " * ((box_width - 14) // 2) +
              "\033[1;36mManager Menu" + "\033[34m" + " " * ((box_width - 14) // 2) + "║\033[0m")
        print(" " * padding + "\033[34m╠" + "═" * (box_width - 2) + "╣\033[0m")

        # Menu options
        menu_items = [
            "1. Manage User Accounts",
            "2. Oversee Order Details",
            "3. Track Financial",
            "4. Control Inventory",
            "5. Review Customer Feedback",
            "0. Exit"
        ]

        for item in menu_items:
            print(" " * padding + "\033[34m║\033[0m " + "\033[1;36m" + item.ljust(box_width - 3) + "\033[0m" + "\033[34m║\033[0m")

        # Bottom border of the box
        print(" " * padding + "\033[34m╚" + "═" * (box_width - 2) + "╝\033[0m")

        # Center the input fields horizontally
        input_width = 40  # Approximate width of the input prompt
        choice = input("\n" + " " * ((columns - input_width) // 2) + "\033[1;36mChoose an option: \033[0m").strip()

        if choice == "1":
            manage_user_accounts()
        elif choice == "2":
            oversee_order_details()
        elif choice == "3":
            track_financial()
        elif choice == "4":
            control_inventory()
        elif choice == "5":
            review_customer_feedback()
        elif choice == "0":
            custom_clear_screen()
            print("\n" + " " * ((columns - input_width) // 2) + "\033[1;36mExiting Manager Menu...\033[0m")
            break
        else:
            custom_clear_screen()
            print("\n" + " " * ((columns - input_width) // 2) + "\033[1;36mInvalid choice, please try again.\033[0m")


        if choice == "1":
            manage_user_accounts()
        elif choice == "2":
            oversee_order_details()
        elif choice == "3":
            track_financial()
        elif choice == "4":
            control_inventory()
        elif choice == "5":
            review_customer_feedback()
        elif choice == "0":
            print("Exiting Manager Menu...")
            exit()
        else:
            print("Invalid choice, please try again.")


def manage_user_accounts():
    while True:
        print("==== Manage User Accounts ====")
        print("1. Add User")
        print("2. Remove User")
        print("3. View Users")
        print("4. View Deletion log")
        print("0. Exit")
        choice = input("Choose an option: ")

        if choice == "1":
            add_user()
        elif choice == "2":
            remove_user()
        elif choice == "3":
            view_users()
        elif choice == "4":
            view_deletion_log()
        elif choice == "0":
            print("Exiting Manage User Accounts...")
        break


def add_user():
    print("---- Add User ----")

    # input details of user
    username = input("Enter new username: ").strip()  #.strip is to remove unnecessary space
    password = input("Enter password: ").strip() # The variable is grey because it is a local variable.
    user_type = input("Enter user type (member/manager/chef/cashier): ").strip().lower()# the .lower is to prevent it from being too case-sensitive.

    #make sure the manager doesn't type random stuff for user_type
    if user_type not in ["member","manager","chef","cashier"]:
        print("Invalid user type. Please enter one of the following: member, manager, chef, cashier.")
        return #return will take the manager back to the manage user accounts section.

    #Making sure the password isn't blank.
    if not password:
        print("Password cannot be empty.")
        return

    #Connecting to the Database
    try: #This is for error handling
        conn = sqlite3.connect("users.db") # connects to the users.db database
        cursor = conn.cursor() #Creates an object that can make SQL commands on the database

    #making sure the username doesn't conflict with an already existing username.
        cursor.execute("SELECT username FROM users WHERE username = ?", (username,)) #make a sql statement to see if the username already exist.
        if cursor.fetchone(): #take the first matching record.
            print("This username has been taken, please try again.")
        else:
            cursor.execute("INSERT INTO users (username, password, user_type) VALUES (?, ?, ?)",(username, password, user_type))
            conn.commit() #save the changes to the database
            print(f"User '{username}' added successfully as '{user_type}'.")
    except sqlite3.Error as e: #Error Handling
        print(f"An error occurred while accessing the database: {e}")
    finally: #Error Handling
        conn.close()

from datetime import datetime # will allow the program to retrieve the current time
def remove_user():
    print("---- Remove User ----")

    #Find the user to be removed.
    username = input("Enter the username to remove: ").strip()

    #Connect to database
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()

    #Finding the username in the database and deleting it.
    try: #this is for error handling
        cursor.execute('SELECT username, user_type FROM users WHERE username = ?', (username,)) #This will retrieve the username and user_type
        user = cursor.fetchone() #user will become the first matching record.

    #Confirmation for deletion
        if user: #Meaning there is a matching result for the username.
            user_type = user[1] #retrieve the user type for the log
            print(f"Found user: Username = {user[0]}, Type = {user[1]}") #Display the info of the user.
            confirm = input(f"Are you sure you want to delete the user '{username}'? (y/n): ").strip().lower()
        #DELETION
            if confirm == 'y':
                reason = input("Enter the reason for deletion: ").strip()
                cursor.execute('DELETE FROM users WHERE username = ?', (username,))
                conn.commit()
                #Made a log for all deletion
                with open('deletion_log.txt', 'a') as log_file:
                    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S") #timestamp for the log
                    log_file.write(f"{username} | {user_type} | {timestamp} | {reason}\n")
                print(f"User '{username}' has been removed.")
            else:
                print("Deletion canceled.")
        else:
            print(f"User '{username}' not found.")
    except sqlite3.Error as e: #Will continue the program even if there is an error
        print(f"An error occurred while accessing the database: {e}")
    finally: #Will disconnect the database regardless of what happens.
        conn.close()

def view_deletion_log():
    print("---- Deletion Log ----")

    # Viewing te log
    try:
        with open('deletion_log.txt', 'r') as log_file: #R stands for read
            logs = log_file.readlines()  #Read all lines in the log file
            #Display the log
            if logs:
                print(f"{'Username':<15} {'User Type':<15} {'Timestamp':<20} {'Reason'}") #Header
                print("-"*80)#line
                for log in logs:
                    log_parts = log.strip().split(" | ") #For a vertical line in between
                    if len(log_parts) == 4: #Error handling
                        print(f"{log_parts[0]:<15} {log_parts[1].upper():<15} {log_parts[2]:<20} {log_parts[3]}") #show the contents
                    else:
                        print("Invalid log format in line:", log.strip())
            else:
                print("No deletions logged yet.")
    except FileNotFoundError:
        print("No deletion log found.")

def view_users():
    print("---- View Users ----")

    #Connect to database
    try:
        conn = sqlite3.connect("users.db")
        cursor = conn.cursor()

        current_view = "all"  # Track current view state: 'all' or a specific filter
        user_type = None  # Default to no filter

        while True:
            # Fetch and display users based on current view
            if current_view == "all":
                cursor.execute("SELECT username, user_type FROM users")
                users = cursor.fetchall()
                print("\nAll Users:")
            else:
                cursor.execute("SELECT username, user_type FROM users WHERE user_type = ?", (user_type,))
                users = cursor.fetchall()
                print(f"\nFiltered Users ({user_type.capitalize()}s):")
            #Display the users
            if users:
                print(f"{'Username':<15}{'User Type'.upper():<15}") #This is to make a header, the arrows are for the alignment and the number is the width
                print("-"*30) #This is just to make a line below the header
                for user in users:
                    print(f"{user[0]:<20}{user[1]:<10}")
            else:
                print("No users found in the data base.")
            #Provide options after displaying all users
            print("\nOptions:")
            if current_view == "all":
                print("1. Filter by User Type")
            else:
                print("1. Switch Filter / Show All Users")
            print("0. Return to Manage User Accounts")
            choice = input("Choose an option (0-1): ").strip()

            if choice == "1":
                print("\nFilter Options:")
                print("1. Show Members")
                print("2. Show Managers")
                print("3. Show Chefs")
                print("4. Show Cashiers")
                print("0. Return to All Users")
                filter_choice = input("Choose an option (0-4): ").strip()

                if filter_choice == "1":
                    user_type = "member"
                    current_view = "filter"
                elif filter_choice == "2":
                    user_type = "manager"
                    current_view = "filter"
                elif filter_choice == "3":
                    user_type = "chef"
                    current_view = "filter"
                elif filter_choice == "4":
                    user_type = "cashier"
                    current_view = "filter"
                elif filter_choice == "0":
                    current_view = "all"
                else:
                    print("Invalid choice. Please try again.")
            elif choice == "0":
                print("Returning to Manage USer Accounts....")
                break
            else:
                print("Invalid choice. Please try again. ")
    except sqlite3.Error as e: #Error Handling
        print(f"An error occurred while accessing the database: {e}")
    finally: #Error handling
        conn.close()




def oversee_order_details():
    while True:
        print("==== Oversee Order Details ====")
        print("1. View Current Orders")
        print("2. View Order History")
        print("0. Exit")
        choice = input("Choose an option: ")

        if choice == "1":
            view_current_orders()
        elif choice == "2":
            view_order_history()
        elif choice == "0":
            print("Exiting Oversee Order Details...")
            break
        else:
            print("Invalid choice, please try again.")


def view_current_orders():
    print("---- Current Orders ----")

    # Connect to the database
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()

    # Retrieve orders from the orders table.
    try:
        cursor.execute("SELECT username, item_name, price, quantity FROM orders")
        orders = cursor.fetchall()
        #Display the orders
        if orders:
            #The headers and alignment.
            print(f"{'Username':<15} {'Item Name':<10} {'Price':<10} {'Quantity':<10}")
            print("-" * 70)
            #The orders
            for order in orders:
                print(f"{order[0]:<15} {order[1]:<10} {order[2]:<10.2f} {order[3]:<10}")
        else:
            print("No current orders available.")
    except sqlite3.Error as e:
        print(f"An error occurred while retrieving orders: {e}")
    finally:
        conn.close()


def view_order_history():
    pass


def track_financial():
    while True:
        print("==== Track Financial ====")
        print("1. View Inventory Report")
        print("2. View Sales Report")
        print("0. Exit")
        choice = input("Choose an option: ")

        if choice == "1":
            view_inventory_report()
        elif choice == "2":
            view_sales_report()
        elif choice == "0":
            print("Exiting Track Financial...")
            break
        else:
            print("Invalid choice, please try again.")


def view_inventory_report():
    pass


def view_sales_report():
    pass


def control_inventory():
    while True:
        print("==== Control Inventory ====")
        print("1. Check Inventory")
        print("2. Update Inventory")
        print("0. Exit")
        choice = input("Choose an option: ")

        if choice == "1":
            check_inv()
        elif choice == "2":
            update_inventory()
        elif choice == "0":
            print("Exiting Control Inventory...")
            break
        else:
            print("Invalid choice, please try again.")


def check_inv():
    pass


def update_inventory():
    pass


def review_customer_feedback():
    while True:
        print("==== Review Customer Feedback ====")
        print("1. View Feedback")
        print("2. Delete Feedback")
        print("0. Exit")
        choice = input("Choose an option: ")

        if choice == "1":
            view_feedback()
        elif choice == "2":
            delete_feedback()
        elif choice == "0":
            print("Exiting Review Customer Feedback...")
            break
        else:
            print("Invalid choice, please try again.")


def view_feedback():
    pass


def delete_feedback():
    pass