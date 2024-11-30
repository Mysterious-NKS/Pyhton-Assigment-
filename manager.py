from datetime import datetime
from database import load_users
import sqlite3
import shutil # This allows me to determine the terminal's size

def terminal_size():
    #Get the terminal size dynamically.
    size = shutil.get_terminal_size(fallback=(145, 24))  # Default to 145 width, 24 height
    return size.lines, size.columns #this returns the height as lines and width as columns into two separate columns


def custom_clear_screen():
    # Push previous content down
    print("\n" * 20, end="")  # Push content out of view



def print_centered_box(columns): #This function needs an external value so the column is in the bracket
    #Print the login box centered horizontally with colours.
    # Define the box width explicitly
    box_width = 60
    padding = (columns - box_width) // 2 #Calculates the space needed on the left side to center the box horizontally.

    # Box lines with darker blue
    print(" " * padding + "\033[34m╔" + "═" * (box_width - 2) + "╗\033[0m") #"\033[34m" Changes the text color to dark blue.
    print(" " * padding + "\033[34m║" + " " * ((box_width - 22) // 2) +"\033[1;36mManager Login Page" + "\033[34m" + " " * ((box_width - 18) // 2) + "║\033[0m")
    print(" " * padding + "\033[34m╚" + "═" * (box_width - 2) + "╝\033[0m")


def manager_login():
    while True:
        try:
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

        except Exception as e:
            custom_clear_screen()  # Clear the screen before showing the error message
            print("\n" * top_padding)
            print_centered_box(columns)
            print("\n" + " " * ((columns - input_width) // 2) + f"\033[1;36m❌ An error occurred: {str(e)}\033[0m")
            input("\n" + " " * ((columns - input_width) // 2) + "\033[1;36mPress Enter to retry...\033[0m")

        finally:
            # This block ensures that the terminal is cleared before exiting, even on an exception
            custom_clear_screen()



def manager_menu():
    while True:
        try:
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
                "2. Order Management",
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

            # Handle menu choices
            if choice == "1":
                manage_user_accounts()
            elif choice == "2":
                order_management()
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

        except Exception as e:
            custom_clear_screen()  # Clear the screen before showing the error message
            print("\n" * top_padding)
            print(" " * padding + "\033[34m╔" + "═" * (box_width - 2) + "╗\033[0m")
            print(" " * padding + "\033[34m║" + " " * ((box_width - 16) // 2) +
                  "\033[1;36mAn Error Occurred" + "\033[34m" + " " * ((box_width - 16) // 2) + "║\033[0m")
            print(" " * padding + "\033[34m╚" + "═" * (box_width - 2) + "╝\033[0m")
            print("\n" + " " * ((columns - input_width) // 2) + f"\033[1;36mError: {str(e)}\033[0m")
            input("\n" + " " * ((columns - input_width) // 2) + "\033[1;36mPress Enter to retry...\033[0m")

        finally:
            # Ensures the terminal is cleared before exiting, even on an exception
            custom_clear_screen()





def add_user():
    conn = None  # Initialize conn to avoid UnboundLocalError
    try:
        custom_clear_screen()  # Clear the screen at the start

        # Header box: Add New User
        print("\033[34m╔" + "═" * 58 + "╗\033[0m")
        print("\033[34m║\033[0m \033[1;36mAdd New User" + " " * 45 + "\033[34m║\033[0m")
        print("\033[34m╚" + "═" * 58 + "╝\033[0m")

        # Input user details
        username = input("\033[1;36mEnter new username: \033[0m").strip()
        password = input("\033[1;36mEnter password: \033[0m").strip()

        # Display user type selection in a box
        custom_clear_screen()
        print("\033[34m╔" + "═" * 58 + "╗\033[0m")
        print("\033[34m║\033[0m \033[1;36mSelect User Type" + " " * 41 + "\033[34m║\033[0m")
        print("\033[34m╠" + "═" * 58 + "╣\033[0m")

        # List user types with proper alignment
        user_types = ["Member", "Manager", "Chef", "Cashier"]
        for i, user_type in enumerate(user_types, 1):
            print("\033[34m║\033[0m \033[1;36m" + f"{i}. {user_type}".ljust(57) + "\033[34m║\033[0m")

        print("\033[34m╚" + "═" * 58 + "╝\033[0m")

        # Get user type choice
        try:
            user_type_choice = int(input("\033[1;36mEnter the number for the user type: \033[0m").strip())
            if user_type_choice < 1 or user_type_choice > len(user_types):
                raise ValueError
            user_type = user_types[user_type_choice - 1].lower()
        except ValueError:
            custom_clear_screen()
            print("\033[31m╔" + "═" * 58 + "╗\033[0m")
            print("\033[31m║\033[0m \033[33mInvalid user type. Please try again." + " " * 21 + "\033[31m║\033[0m")
            print("\033[31m╚" + "═" * 58 + "╝\033[0m")
            input("\033[1;33mPress Enter to return to Manage User Accounts...\033[0m")
            return manage_user_accounts()

        # Validation: Check password is not empty
        if not password:
            custom_clear_screen()
            print("\033[31m╔" + "═" * 58 + "╗\033[0m")
            print("\033[31m║\033[0m \033[33mPassword cannot be empty." + " " * 32 + "\033[31m║\033[0m")
            print("\033[31m╚" + "═" * 58 + "╝\033[0m")
            input("\033[1;33mPress Enter to return to Manage User Accounts...\033[0m")
            return manage_user_accounts()

        # Connect to the database
        conn = sqlite3.connect("users.db")  # Connect to the users.db database
        cursor = conn.cursor()  # Create a cursor for executing SQL commands

        # Check for existing username
        cursor.execute("SELECT username FROM users WHERE username = ?", (username,))
        if cursor.fetchone():  # If a record is found, the username is already taken
            custom_clear_screen()
            print("\033[31m╔" + "═" * 58 + "╗\033[0m")
            print("\033[31m║\033[0m \033[33mUsername already taken. Please try again." + " " * 16 + "\033[31m║\033[0m")
            print("\033[31m╚" + "═" * 58 + "╝\033[0m")
            input("\033[1;33mPress Enter to return to Manage User Accounts...\033[0m")
            return manage_user_accounts()
        else:
            # Insert new user into the database
            cursor.execute(
                "INSERT INTO users (username, password, user_type) VALUES (?, ?, ?)",
                (username, password, user_type)
            )
            conn.commit()  # Save changes to the database

            custom_clear_screen()
            print("\033[34m╔" + "═" * 58 + "╗\033[0m")
            print("\033[34m║\033[0m \033[1;36mUser added successfully!" + " " * 33 + "\033[34m║\033[0m")
            print("\033[34m╚" + "═" * 58 + "╝\033[0m")
            input("\033[1;36mPress Enter to return to Manage User Accounts...\033[0m")
            return manage_user_accounts()

    except sqlite3.Error as e:
        # Error handling for database issues
        custom_clear_screen()
        print("\033[31m╔" + "═" * 58 + "╗\033[0m")
        print("\033[31m║\033[0m \033[33mDatabase error occurred. Please try again." + " " * 13 + "\033[31m║\033[0m")
        print("\033[31m╚" + "═" * 58 + "╝\033[0m")
        print("\033[1;33mError: " + str(e) + "\033[0m")
        input("\033[1;33mPress Enter to return to Manage User Accounts...\033[0m")
        return manage_user_accounts()

    finally:
        # Close the database connection only if it exists
        if conn:
            conn.close()


from datetime import datetime # will allow the program to retrieve the current time
def remove_user():
    """Removes a user from the system."""
    conn = None  # Initialize conn to avoid UnboundLocalError
    try:
        custom_clear_screen()  # Clear the screen at the start

        # Header box: Remove User
        print("\033[34m╔" + "═" * 58 + "╗\033[0m")
        print("\033[34m║\033[0m \033[1;36mRemove User" + " " * 46 + "\033[34m║\033[0m")
        print("\033[34m╚" + "═" * 58 + "╝\033[0m")

        # Input username
        username = input("\033[1;36mEnter the username to remove: \033[0m").strip()

        # Connect to the database
        conn = sqlite3.connect('users.db')
        cursor = conn.cursor()

        # Find the username in the database
        cursor.execute('SELECT username, user_type FROM users WHERE username = ?', (username,))
        user = cursor.fetchone()  # Retrieve the first matching record

        # Handle user existence and deletion
        if user:  # If a matching user is found
            user_type = user[1]  # Retrieve the user type for logging
            custom_clear_screen()
            print("\033[34m╔" + "═" * 58 + "╗\033[0m")
            print("\033[34m║\033[0m \033[1;36mFound User: Username = " + user[0] + ", Type = " + user[1] + " " * (26 - len(user[0]) - len(user[1])) + "\033[34m║\033[0m")
            print("\033[34m╚" + "═" * 58 + "╝\033[0m")

            # Confirmation for deletion
            confirm = input("\033[1;36mAre you sure you want to delete this user? (y/n): \033[0m").strip().lower()
            if confirm == 'y':
                reason = input("\033[1;36mEnter the reason for deletion: \033[0m").strip()
                cursor.execute('DELETE FROM users WHERE username = ?', (username,))
                conn.commit()

                # Log the deletion
                with open('deletion_log.txt', 'a') as log_file:
                    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # Log timestamp
                    log_file.write(f"{username} | {user_type} | {timestamp} | {reason}\n")

                custom_clear_screen()
                print("\033[34m╔" + "═" * 58 + "╗\033[0m")
                print("\033[34m║\033[0m \033[1;36mUser '" + username + "' has been removed successfully." + " " * (29 - len(username)) + "\033[34m║\033[0m")
                print("\033[34m╚" + "═" * 58 + "╝\033[0m")
                input("\033[1;36mPress Enter to return to Manage User Accounts...\033[0m")
                return manage_user_accounts()
            else:
                custom_clear_screen()
                print("\033[31m╔" + "═" * 58 + "╗\033[0m")
                print("\033[31m║\033[0m \033[33mDeletion canceled. Returning to Manage User Accounts." + " " * 2 + "\033[31m║\033[0m")
                print("\033[31m╚" + "═" * 58 + "╝\033[0m")
                input("\033[1;33mPress Enter to continue...\033[0m")
                return manage_user_accounts()
        else:
            # User not found
            custom_clear_screen()
            print("\033[31m╔" + "═" * 58 + "╗\033[0m")
            print("\033[31m║\033[0m \033[33mUser '" + username + "' not found in the database." + " " * (22 - len(username)) + "\033[31m║\033[0m")
            print("\033[31m╚" + "═" * 58 + "╝\033[0m")
            input("\033[1;33mPress Enter to return to Manage User Accounts...\033[0m")
            return manage_user_accounts()

    except sqlite3.Error as e:
        # Error handling for database issues
        custom_clear_screen()
        print("\033[31m╔" + "═" * 58 + "╗\033[0m")
        print("\033[31m║\033[0m \033[33mDatabase error occurred. Please try again." + " " * 13 + "\033[31m║\033[0m")
        print("\033[31m╚" + "═" * 58 + "╝\033[0m")
        print("\033[1;33mError: " + str(e) + "\033[0m")
        input("\033[1;33mPress Enter to return to Manage User Accounts...\033[0m")
        return manage_user_accounts()

    finally:
        # Close the database connection only if it exists
        if conn:
            conn.close()


def view_deletion_log():
    try:
        custom_clear_screen()  # Clear the screen at the start

        # Longer box width for the Deletion Log
        box_width = 100  # Adjusted for longer "Reason" entries
        print("\033[34m╔" + "═" * (box_width - 2) + "╗\033[0m")
        print("\033[34m║\033[0m \033[1;36mDeletion Log" + " " * (box_width - 15) + "\033[34m║\033[0m")
        print("\033[34m╚" + "═" * (box_width - 2) + "╝\033[0m")

        # Viewing the log file
        with open('deletion_log.txt', 'r') as log_file:  # Open the log file in read mode
            logs = log_file.readlines()  # Read all lines in the log file

            if logs:  # If logs are present
                # Table header
                print("\033[34m╔" + "═" * (box_width - 2) + "╗\033[0m")
                print("\033[34m║\033[0m \033[1;36m" + f"{'Username':<15} {'User Type':<15} {'Timestamp':<20} {'Reason'}".ljust(box_width - 3) + "\033[34m║\033[0m")
                print("\033[34m╠" + "═" * (box_width - 2) + "╣\033[0m")

                # Display each log entry
                for log in logs:
                    log_parts = log.strip().split(" | ")  # Split each log entry by the delimiter
                    if len(log_parts) == 4:  # Validate the log format
                        username, user_type, timestamp, reason = log_parts
                        print("\033[34m║\033[0m " + f"{username:<15} {user_type.upper():<15} {timestamp:<20} {reason}".ljust(box_width - 3) + "\033[34m║\033[0m")
                    else:
                        print("\033[34m║\033[0m \033[33mInvalid log format in line: " + log.strip().ljust(box_width - 3) + "\033[34m║\033[0m")

                # Close the table
                print("\033[34m╚" + "═" * (box_width - 2) + "╝\033[0m")
            else:
                # If the log file is empty
                print("\033[34m╔" + "═" * (box_width - 2) + "╗\033[0m")
                print("\033[34m║\033[0m \033[33mNo deletions logged yet.".ljust(box_width - 3) + "\033[34m║\033[0m")
                print("\033[34m╚" + "═" * (box_width - 2) + "╝\033[0m")

    except FileNotFoundError:
        # If the log file is not found
        print("\033[34m╔" + "═" * (box_width - 2) + "╗\033[0m")
        print("\033[34m║\033[0m \033[33mNo deletion log found.".ljust(box_width - 3) + "\033[34m║\033[0m")
        print("\033[34m╚" + "═" * (box_width - 2) + "╝\033[0m")

    input("\033[1;36mPress Enter to return to Manage User Accounts...\033[0m")
    return manage_user_accounts()


def view_users():
    conn = None  # Initialize the connection to avoid errors
    try:
        custom_clear_screen()  # Clear the screen at the start
        conn = sqlite3.connect("users.db")  # Connect to the database
        cursor = conn.cursor()  # Create a cursor object to execute SQL queries

        current_view = "all"  # Default view is 'all' users
        user_type = None  # Default to no filter

        box_width = 80  # Adjusted for consistent alignment with user information

        while True:
            custom_clear_screen()  # Clear screen before displaying the box
            # Box Header
            print("\033[34m╔" + "═" * (box_width - 2) + "╗\033[0m")
            if current_view == "all":
                print("\033[34m║\033[0m \033[1;36mViewing All Users" + " " * (box_width - 20) + "\033[34m║\033[0m")
            else:
                print("\033[34m║\033[0m \033[1;36mFiltered Users (" + user_type.capitalize() + "s)" + " " * (box_width - 10) + "\033[34m║\033[0m")
            print("\033[34m╚" + "═" * (box_width - 2) + "╝\033[0m")

            # Fetch and display users
            if current_view == "all":
                cursor.execute("SELECT username, user_type FROM users")
            else:
                cursor.execute("SELECT username, user_type FROM users WHERE user_type = ?", (user_type,))
            users = cursor.fetchall()

            if users:
                # Table Header
                print("\033[34m╔" + "═" * (box_width - 2) + "╗\033[0m")
                print("\033[34m║\033[0m \033[1;36m" + f"{'Username':<20} {'User Type'.upper():<15}".ljust(box_width - 3) + "\033[34m║\033[0m")
                print("\033[34m╠" + "═" * (box_width - 2) + "╣\033[0m")

                # Display users
                for user in users:
                    username, u_type = user
                    print("\033[34m║\033[0m " + f"{username:<20} {u_type.upper():<15}".ljust(box_width - 3) + "\033[34m║\033[0m")

                # Table Footer
                print("\033[34m╚" + "═" * (box_width - 2) + "╝\033[0m")
            else:
                # No users found
                print("\033[34m╔" + "═" * (box_width - 2) + "╗\033[0m")
                print("\033[34m║\033[0m \033[33mNo users found in the database.".ljust(box_width - 3) + "\033[34m║\033[0m")
                print("\033[34m╚" + "═" * (box_width - 2) + "╝\033[0m")

            # Options
            print("\033[34m╔" + "═" * (box_width - 2) + "╗\033[0m")
            print("\033[34m║\033[0m \033[1;36mOptions:".ljust(box_width - -15) + "\033[34m║\033[0m")
            if current_view == "all":
                print("\033[34m║\033[0m \033[1;36m1. Filter by User Type".ljust(box_width - -15) + "\033[34m║\033[0m")
            else:
                print("\033[34m║\033[0m \033[1;36m1. Switch Filter / Show All Users".ljust(box_width - -15) + "\033[34m║\033[0m")
            print("\033[34m║\033[0m \033[1;36m0. Return to Manage User Accounts".ljust(box_width - -15) + "\033[34m║\033[0m")
            print("\033[34m╚" + "═" * (box_width - 2) + "╝\033[0m")

            # Handle user input
            choice = input("\033[1;36mChoose an option (0-1): \033[0m").strip()

            if choice == "1":
                # Filter options
                custom_clear_screen()
                print("\033[34m╔" + "═" * (box_width - 2) + "╗\033[0m")
                print("\033[34m║\033[0m \033[1;36mFilter Options:".ljust(box_width - -15) + "\033[34m║\033[0m")
                print("\033[34m╠" + "═" * (box_width - 2) + "╣\033[0m")
                filter_options = [
                    "1. Show Members",
                    "2. Show Managers",
                    "3. Show Chefs",
                    "4. Show Cashiers",
                    "0. Return to All Users"
                ]
                for option in filter_options:
                    print("\033[34m║\033[0m \033[1;36m" + option.ljust(box_width - 3) + "\033[34m║\033[0m")
                print("\033[34m╚" + "═" * (box_width - 2) + "╝\033[0m")

                filter_choice = input("\033[1;36mChoose an option (0-4): \033[0m").strip()

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
                    print("\033[31mInvalid choice. Please try again.\033[0m")
                    input("\033[1;36mPress Enter to retry...\033[0m")
            elif choice == "0":
                custom_clear_screen()
                print("\033[1;36mReturning to Manage User Accounts...\033[0m")
                return manage_user_accounts()
            else:
                print("\033[31mInvalid choice. Please try again.\033[0m")
                input("\033[1;36mPress Enter to retry...\033[0m")

    except sqlite3.Error as e:
        # Database error handling
        custom_clear_screen()
        print("\033[31m╔" + "═" * (box_width - 2) + "╗\033[0m")
        print("\033[31m║\033[0m \033[33mAn error occurred while accessing the database:".ljust(box_width - 3) + "\033[31m║\033[0m")
        print("\033[31m║\033[0m \033[33m" + str(e).ljust(box_width - 3) + "\033[31m║\033[0m")
        print("\033[31m╚" + "═" * (box_width - 2) + "╝\033[0m")
        input("\033[1;36mPress Enter to return to Manage User Accounts...\033[0m")
        return manage_user_accounts()

    finally:
        if conn:
            conn.close()  # Close the database connection



def manage_user_accounts():
    while True:
        try:
            custom_clear_screen()  # Clear the screen at the start

            # Define the box width explicitly
            box_width = 60

            # Box lines with darker blue
            print("\033[34m╔" + "═" * (box_width - 2) + "╗\033[0m")
            print("\033[34m║\033[0m \033[1;36mManage User Accounts" + " " * 37 + "\033[34m║\033[0m")
            print("\033[34m╠" + "═" * (box_width - 2) + "╣\033[0m")

            # Menu options
            menu_items = [
                "1. Add User",
                "2. Remove User",
                "3. View Users",
                "4. View Deletion Log",
                "0. Back to Manager Menu"
            ]

            for item in menu_items:
                print("\033[34m║\033[0m \033[1;36m" + item.ljust(box_width - 3) + "\033[34m║\033[0m")

            # Bottom border of the box
            print("\033[34m╚" + "═" * (box_width - 2) + "╝\033[0m")

            # Input prompt
            choice = input("\033[1;36mChoose an option: \033[0m").strip()

            # Handle menu choices
            if choice == "1":
                add_user()
            elif choice == "2":
                remove_user()
            elif choice == "3":
                view_users()
            elif choice == "4":
                view_deletion_log()
            elif choice == "0":
                custom_clear_screen()
                print("\033[1;36mReturning to Manager Menu...\033[0m")
                break
            else:
                custom_clear_screen()
                print("\033[31m╔" + "═" * (box_width - 2) + "╗\033[0m")
                print("\033[31m║\033[0m \033[33mInvalid choice. Please try again." + " " * 18 + "\033[31m║\033[0m")
                print("\033[31m╚" + "═" * (box_width - 2) + "╝\033[0m")
                input("\033[1;33mPress Enter to retry...\033[0m")

        except Exception as e:
            custom_clear_screen()  # Clear the screen before showing the error message
            print("\033[31m╔" + "═" * (box_width - 2) + "╗\033[0m")
            print("\033[31m║\033[0m \033[33mAn Error Occurred: " + str(e)[:38].ljust(36) + "\033[31m║\033[0m")
            print("\033[31m╚" + "═" * (box_width - 2) + "╝\033[0m")
            input("\033[1;33mPress Enter to retry...\033[0m")

        finally:
            custom_clear_screen()



def order_management():
    while True:
        try:
            custom_clear_screen()  # Clear the screen at the start

            # Header box
            box_width = 58
            print("\033[34m╔" + "═" * (box_width - 2) + "╗\033[0m")
            print("\033[34m║\033[0m \033[1;36mOrder Management" + " " * (box_width - 19) + "\033[34m║\033[0m")
            print("\033[34m╠" + "═" * (box_width - 2) + "╣\033[0m")

            # Menu options
            menu_items = [
                "1. Oversee Order Details",
                "2. View Current Orders",
                "3. View All Orders",
                "4. View Completed Orders",
                "5. Update Order Status",
                "0. Back to Manager Menu"
            ]

            for item in menu_items:
                print("\033[34m║\033[0m \033[1;36m" + item.ljust(box_width - 3) + "\033[34m║\033[0m")

            # Bottom border
            print("\033[34m╚" + "═" * (box_width - 2) + "╝\033[0m")

            # User input
            choice = input("\033[1;36mChoose an option: \033[0m").strip()

            # Menu navigation
            if choice == "1":
                oversee_order_details()
            elif choice == "2":
                view_current_orders()
            elif choice == "3":
                view_all_orders()
            elif choice == "4":
                view_completed_orders()
            elif choice == "5":
                update_order_status()
            elif choice == "0":
                custom_clear_screen()
                print("\033[1;36mReturning to Manager Menu...\033[0m")
                break
            else:
                # Invalid choice handling
                custom_clear_screen()
                print("\033[31m╔" + "═" * (box_width - 2) + "╗\033[0m")
                print("\033[31m║\033[0m \033[33mInvalid choice. Please try again." + " " * (box_width - 36) + "\033[31m║\033[0m")
                print("\033[31m╚" + "═" * (box_width - 2) + "╝\033[0m")
                input("\033[1;33mPress Enter to retry...: \033[0m")
        except Exception as e:
            # Error handling
            custom_clear_screen()
            print("\033[31m╔" + "═" * (box_width - 2) + "╗\033[0m")
            print("\033[31m║\033[0m \033[33mAn Error Occurred: " + str(e)[:36].ljust(36) + "\033[31m║\033[0m")
            print("\033[31m╚" + "═" * (box_width - 2) + "╝\033[0m")
            input("\033[1;33mPress Enter to retry...: \033[0m")





def view_current_orders():
    conn = None  # Initialize the connection to avoid UnboundLocalError
    try:
        custom_clear_screen()  # Clear the screen at the start

        # Define box dimensions for proper alignment
        box_width = 80
        print("\033[34m╔" + "═" * (box_width - 2) + "╗\033[0m")
        print("\033[34m║\033[0m \033[1;36mCurrent Pending Orders" + " " * (box_width - 25) + "\033[34m║\033[0m")
        print("\033[34m╚" + "═" * (box_width - 2) + "╝\033[0m")

        conn = sqlite3.connect("users.db")  # Connect to the database
        cursor = conn.cursor()  # Create a cursor for executing SQL commands

        # Fetch all orders with 'pending' status
        cursor.execute("""
            SELECT o.order_id, u.username, o.total_amount, o.status
            FROM orders o
            INNER JOIN users u ON o.user_id = u.rowid
            WHERE o.status = 'pending'
        """)
        orders = cursor.fetchall()

        if orders:
            # Display the table header
            print("\033[34m╔" + "═" * (box_width - 2) + "╗\033[0m")
            print("\033[34m║\033[0m \033[1;36m" + f"{'Order ID':<15} {'Username':<20} {'Total Amount':<15} {'Status'}".ljust(box_width - 3) + "\033[34m║\033[0m")
            print("\033[34m╠" + "═" * (box_width - 2) + "╣\033[0m")

            # Display each pending order
            for order in orders:
                order_id, username, total_amount, status = order
                print("\033[34m║\033[0m " + f"{order_id:<15} {username:<20} RM{total_amount:<13.2f} {status}".ljust(box_width - 3) + "\033[34m║\033[0m")

            # Close the table
            print("\033[34m╚" + "═" * (box_width - 2) + "╝\033[0m")
        else:
            # No pending orders
            print("\033[34m╔" + "═" * (box_width - 2) + "╗\033[0m")
            print("\033[34m║\033[0m \033[33mNo pending orders found.".ljust(box_width - 3) + "\033[34m║\033[0m")
            print("\033[34m╚" + "═" * (box_width - 2) + "╝\033[0m")

    except sqlite3.Error as e:
        # Handle database errors
        custom_clear_screen()
        print("\033[31m╔" + "═" * (box_width - 2) + "╗\033[0m")
        print("\033[31m║\033[0m \033[33mDatabase error occurred:".ljust(box_width - 3) + "\033[31m║\033[0m")
        print("\033[31m║\033[0m \033[33m" + str(e).ljust(box_width - 3) + "\033[31m║\033[0m")
        print("\033[31m╚" + "═" * (box_width - 2) + "╝\033[0m")
        input("\033[1;36mPress Enter to return to Oversee Order Details...: \033[0m")
        return order_management()

    finally:
        if conn:
            conn.close()  # Ensure the database connection is closed

    input("\033[1;36mPress Enter to return to Oversee Order Details... \033[0m")
    return order_management()

def view_all_orders():
    conn = None
    try:
        custom_clear_screen()  # Clear the screen at the start

        # Define box dimensions for alignment
        box_width = 80
        print("\033[34m╔" + "═" * (box_width - 2) + "╗\033[0m")
        print("\033[34m║\033[0m \033[1;36mAll Orders" + " " * (box_width - 14) + "\033[34m║\033[0m")
        print("\033[34m╚" + "═" * (box_width - 2) + "╝\033[0m")

        conn = sqlite3.connect("users.db")  # Connect to the database
        cursor = conn.cursor()

        # Fetch all orders
        cursor.execute("""
            SELECT o.order_id, u.username, o.total_amount, o.status
            FROM orders o
            INNER JOIN users u ON o.user_id = u.rowid
        """)
        orders = cursor.fetchall()

        if orders:
            # Display the table header
            print("\033[34m╔" + "═" * (box_width - 2) + "╗\033[0m")
            print("\033[34m║\033[0m \033[1;36m" + f"{'Order ID':<15} {'Username':<20} {'Total Amount':<15} {'Status'}".ljust(box_width - 3) + "\033[34m║\033[0m")
            print("\033[34m╠" + "═" * (box_width - 2) + "╣\033[0m")

            # Display each order
            for order in orders:
                order_id, username, total_amount, status = order
                print("\033[34m║\033[0m " + f"{order_id:<15} {username:<20} RM{total_amount:<13.2f} {status}".ljust(box_width - 3) + "\033[34m║\033[0m")

            # Close the table
            print("\033[34m╚" + "═" * (box_width - 2) + "╝\033[0m")
        else:
            # No orders found
            print("\033[34m╔" + "═" * (box_width - 2) + "╗\033[0m")
            print("\033[34m║\033[0m \033[33mNo orders found in the database.".ljust(box_width - 3) + "\033[34m║\033[0m")
            print("\033[34m╚" + "═" * (box_width - 2) + "╝\033[0m")

    except sqlite3.Error as e:
        # Handle database errors
        custom_clear_screen()
        print("\033[31m╔" + "═" * (box_width - 2) + "╗\033[0m")
        print("\033[31m║\033[0m \033[33mDatabase error occurred:".ljust(box_width - 3) + "\033[31m║\033[0m")
        print("\033[31m║\033[0m \033[33m" + str(e).ljust(box_width - 3) + "\033[31m║\033[0m")
        print("\033[31m╚" + "═" * (box_width - 2) + "╝\033[0m")
        input("\033[1;36mPress Enter to return to Oversee Order Details...: \033[0m")
        return order_management()

    finally:
        if conn:
            conn.close()  # Ensure the database connection is closed

    input("\033[1;36mPress Enter to return to Oversee Order Details...: \033[0m")
    return order_management()

def view_completed_orders():
    conn = None
    try:
        custom_clear_screen()  # Clear the screen at the start

        # Define box dimensions for alignment
        box_width = 80
        print("\033[34m╔" + "═" * (box_width - 2) + "╗\033[0m")
        print("\033[34m║\033[0m \033[1;36mCompleted Orders" + " " * (box_width - 21) + "\033[34m║\033[0m")
        print("\033[34m╚" + "═" * (box_width - 2) + "╝\033[0m")

        conn = sqlite3.connect("users.db")  # Connect to the database
        cursor = conn.cursor()

        # Fetch completed orders
        cursor.execute("""
            SELECT o.order_id, u.username, o.total_amount, o.status
            FROM orders o
            INNER JOIN users u ON o.user_id = u.rowid
            WHERE o.status = 'completed'
        """)
        completed_orders = cursor.fetchall()

        if completed_orders:
            # Display the table header
            print("\033[34m╔" + "═" * (box_width - 2) + "╗\033[0m")
            print("\033[34m║\033[0m \033[1;36m" + f"{'Order ID':<15} {'Username':<20} {'Total Amount':<15} {'Status'}".ljust(box_width - 3) + "\033[34m║\033[0m")
            print("\033[34m╠" + "═" * (box_width - 2) + "╣\033[0m")

            # Display each completed order
            for order in completed_orders:
                order_id, username, total_amount, status = order
                print("\033[34m║\033[0m " + f"{order_id:<15} {username:<20} RM{total_amount:<13.2f} {status}".ljust(box_width - 3) + "\033[34m║\033[0m")

            # Close the table
            print("\033[34m╚" + "═" * (box_width - 2) + "╝\033[0m")
        else:
            # No completed orders found
            print("\033[34m╔" + "═" * (box_width - 2) + "╗\033[0m")
            print("\033[34m║\033[0m \033[33mNo completed orders found in the database.".ljust(box_width - 3) + "\033[34m║\033[0m")
            print("\033[34m╚" + "═" * (box_width - 2) + "╝\033[0m")

    except sqlite3.Error as e:
        # Handle database errors
        custom_clear_screen()
        print("\033[31m╔" + "═" * (box_width - 2) + "╗\033[0m")
        print("\033[31m║\033[0m \033[33mDatabase error occurred:".ljust(box_width - 3) + "\033[31m║\033[0m")
        print("\033[31m║\033[0m \033[33m" + str(e).ljust(box_width - 3) + "\033[31m║\033[0m")
        print("\033[31m╚" + "═" * (box_width - 2) + "╝\033[0m")
        input("\033[1;36mPress Enter to return to Oversee Order Details... \033[0m")
        return order_management()

    finally:
        if conn:
            conn.close()  # Ensure the database connection is closed

    input("\033[1;36mPress Enter to return to Oversee Order Details... \033[0m")
    return order_management()

def oversee_order_details():
    conn = None
    try:
        custom_clear_screen()  # Clear the screen at the start

        # Header box for Oversee Order Details
        box_width = 80
        print("\033[34m╔" + "═" * (box_width - 2) + "╗\033[0m")
        print("\033[34m║\033[0m \033[1;36mOversee Order Details" + " " * (box_width - 24) + "\033[34m║\033[0m")
        print("\033[34m╚" + "═" * (box_width - 2) + "╝\033[0m")

        # Input the Order ID to view
        order_id = input("\033[1;36mEnter the Order ID to view details (or press Enter to return): \033[0m").strip()

        if not order_id:
            # If no input, return to the previous menu
            return order_management()

        if not order_id.isdigit():
            custom_clear_screen()
            print("\033[31m╔" + "═" * (box_width - 2) + "╗\033[0m")
            print("\033[31m║\033[0m \033[33mInvalid Order ID. Please enter a numeric value.".ljust(box_width - 3) + "\033[31m║\033[0m")
            print("\033[31m╚" + "═" * (box_width - 2) + "╝\033[0m")
            input("\033[1;33mPress Enter to retry...\033[0m")
            return oversee_order_details()

        # Connect to the database
        conn = sqlite3.connect('users.db')
        cursor = conn.cursor()

        # Retrieve order details and associated items
        cursor.execute('''
            SELECT oi.item_name, oi.price, oi.quantity, (oi.price * oi.quantity) AS total_price
            FROM order_items oi
            WHERE oi.order_id = ?
        ''', (order_id,))

        items = cursor.fetchall()

        if items:
            # Header for the order details table
            custom_clear_screen()
            print("\033[34m╔" + "═" * (box_width - 2) + "╗\033[0m")
            print("\033[34m║\033[0m \033[1;36mOrder ID: " + order_id + " Details".ljust(box_width - 16) + "\033[34m║\033[0m")
            print("\033[34m╠" + "═" * (box_width - 2) + "╣\033[0m")
            print("\033[34m║\033[0m \033[1;36m" + f"{'Item Name':<20}{'Price':<20}{'Quantity':<10}{'Total Price':<15}".ljust(box_width - 3) + "\033[34m║\033[0m")
            print("\033[34m╠" + "═" * (box_width - 2) + "╣\033[0m")

            # Display each item's details
            for item in items:
                item_name, price, quantity, total_price = item
                print("\033[34m║\033[0m " + f"{item_name:<20}{price:<20.2f}{quantity:<10}{total_price:<15.2f}".ljust(box_width - 3) + "\033[34m║\033[0m")

            # Close the table
            print("\033[34m╚" + "═" * (box_width - 2) + "╝\033[0m")
        else:
            # No items found for the given Order ID
            custom_clear_screen()
            print("\033[31m╔" + "═" * (box_width - 2) + "╗\033[0m")
            print("\033[31m║\033[0m \033[33mNo items found for Order ID: " + order_id.ljust(box_width - 21) + "\033[31m║\033[0m")
            print("\033[31m╚" + "═" * (box_width - 2) + "╝\033[0m")

    except sqlite3.Error as e:
        # Handle database errors
        custom_clear_screen()
        print("\033[31m╔" + "═" * (box_width - 2) + "╗\033[0m")
        print("\033[31m║\033[0m \033[33mDatabase error occurred: " + str(e)[:50].ljust(50) + "\033[31m║\033[0m")
        print("\033[31m╚" + "═" * (box_width - 2) + "╝\033[0m")

    finally:
        # Ensure the database connection is closed
        if conn:
            conn.close()

    # Pause before returning
    input("\033[1;36mPress Enter to return to Order Management...\033[0m")
    return order_management()

def update_order_status():
    """Update the status of pending orders to 'Completed'."""
    conn = None  # Initialize the connection to avoid UnboundLocalError
    try:
        custom_clear_screen()  # Clear the screen at the start

        # Define box dimensions for proper alignment
        box_width = 80
        print("\033[34m╔" + "═" * (box_width - 2) + "╗\033[0m")
        print("\033[34m║\033[0m \033[1;36mUpdate Order Status" + " " * (box_width - 22) + "\033[34m║\033[0m")
        print("\033[34m╚" + "═" * (box_width - 2) + "╝\033[0m")

        conn = sqlite3.connect("users.db")  # Connect to the database
        cursor = conn.cursor()  # Create a cursor for executing SQL commands

        # Fetch all orders with 'pending' status
        cursor.execute("""
            SELECT o.order_id, u.username, o.total_amount, o.status
            FROM orders o
            INNER JOIN users u ON o.user_id = u.rowid
            WHERE o.status = 'pending'
        """)
        orders = cursor.fetchall()

        if orders:
            # Display the table header
            print("\033[34m╔" + "═" * (box_width - 2) + "╗\033[0m")
            print("\033[34m║\033[0m \033[1;36m" + f"{'Order ID':<15} {'Username':<20} {'Total Amount':<15} {'Status'}".ljust(box_width - 3) + "\033[34m║\033[0m")
            print("\033[34m╠" + "═" * (box_width - 2) + "╣\033[0m")

            # Display each pending order
            for order in orders:
                order_id, username, total_amount, status = order
                print("\033[34m║\033[0m " + f"{order_id:<15} {username:<20} RM{total_amount:<13.2f} {status}".ljust(box_width - 3) + "\033[34m║\033[0m")

            # Close the table
            print("\033[34m╚" + "═" * (box_width - 2) + "╝\033[0m")

            while True:
                # Prompt the manager to select an order to update
                order_id_input = input("\033[1;36mEnter the Order ID to mark as Completed (or 0 to return): \033[0m").strip()

                if order_id_input == "0":
                    # Return to the previous menu
                    return order_management()

                if not order_id_input.isdigit() or not any(str(order[0]) == order_id_input for order in orders):
                    custom_clear_screen()
                    print("\033[31m╔" + "═" * (box_width - 2) + "╗\033[0m")
                    print("\033[31m║\033[0m \033[33mInvalid Order ID. Please try again.".ljust(box_width - 3) + "\033[31m║\033[0m")
                    print("\033[31m╚" + "═" * (box_width - 2) + "╝\033[0m")
                    input("\033[1;33mPress Enter to retry...\033[0m")
                    continue

                # Update the order status to 'Completed'
                cursor.execute("UPDATE orders SET status = 'Completed' WHERE order_id = ?", (order_id_input,))
                conn.commit()

                custom_clear_screen()
                print("\033[34m╔" + "═" * (box_width - 2) + "╗\033[0m")
                print("\033[34m║\033[0m \033[1;36mOrder ID " + order_id_input + " has been marked as Completed.".ljust(box_width - 3) + "\033[34m║\033[0m")
                print("\033[34m╚" + "═" * (box_width - 2) + "╝\033[0m")
                input("\033[1;36mPress Enter to return to Update Order Status...\033[0m")
                return update_order_status()

        else:
            # No pending orders
            print("\033[34m╔" + "═" * (box_width - 2) + "╗\033[0m")
            print("\033[34m║\033[0m \033[33mNo pending orders found.".ljust(box_width - 3) + "\033[34m║\033[0m")
            print("\033[34m╚" + "═" * (box_width - 2) + "╝\033[0m")

    except sqlite3.Error as e:
        # Handle database errors
        custom_clear_screen()
        print("\033[31m╔" + "═" * (box_width - 2) + "╗\033[0m")
        print("\033[31m║\033[0m \033[33mDatabase error occurred:".ljust(box_width - 3) + "\033[31m║\033[0m")
        print("\033[31m║\033[0m \033[33m" + str(e).ljust(box_width - 3) + "\033[31m║\033[0m")
        print("\033[31m╚" + "═" * (box_width - 2) + "╝\033[0m")

    finally:
        if conn:
            conn.close()  # Ensure the database connection is closed

    input("\033[1;36mPress Enter to return to Order Management...\033[0m")
    return order_management()


def track_financial():
    while True:
        try:
            custom_clear_screen()  # Clear the screen at the start

            # Header box
            box_width = 58
            print("\033[34m╔" + "═" * (box_width - 2) + "╗\033[0m")
            print("\033[34m║\033[0m \033[1;36mTrack Financial" + " " * (box_width - 18) + "\033[34m║\033[0m")
            print("\033[34m╠" + "═" * (box_width - 2) + "╣\033[0m")

            # Menu options
            menu_items = [
                "1. Track Income",
                "2. Track Expenses",
                "3. Track Profitability",
                "0. Back to Manager Menu"
            ]

            for item in menu_items:
                print("\033[34m║\033[0m \033[1;36m" + item.ljust(box_width - 3) + "\033[34m║\033[0m")

            # Bottom border
            print("\033[34m╚" + "═" * (box_width - 2) + "╝\033[0m")

            # User input
            choice = input("\033[1;36mChoose an option: \033[0m").strip()

            # Menu navigation
            if choice == "1":
                track_income()
            elif choice == "2":
                track_expense()
            elif choice == "3":
                track_profitability()
            elif choice == "0":
                custom_clear_screen()
                print("\033[1;36mReturning to Manager Menu...\033[0m")
                break
            else:
                # Invalid choice handling
                custom_clear_screen()
                print("\033[31m╔" + "═" * (box_width - 2) + "╗\033[0m")
                print("\033[31m║\033[0m \033[33mInvalid choice. Please try again.".ljust(box_width - 3) + "\033[31m║\033[0m")
                print("\033[31m╚" + "═" * (box_width - 2) + "╝\033[0m")
                input("\033[1;33mPress Enter to retry...\033[0m")
        except Exception as e:
            # Error handling
            custom_clear_screen()
            print("\033[31m╔" + "═" * (box_width - 2) + "╗\033[0m")
            print("\033[31m║\033[0m \033[33mAn Error Occurred: " + str(e)[:36].ljust(36) + "\033[31m║\033[0m")
            print("\033[31m╚" + "═" * (box_width - 2) + "╝\033[0m")
            input("\033[1;33mPress Enter to retry...\033[0m")

def track_income():
    """Function to calculate and display total income from all orders."""
    conn = None  # Initialize the database connection
    try:
        custom_clear_screen()  # Clear the screen at the start

        # Define box dimensions for proper alignment
        box_width = 58
        print("\033[34m╔" + "═" * (box_width - 2) + "╗\033[0m")
        print("\033[34m║\033[0m \033[1;36mTotal Income Report" + " " * (box_width - 22) + "\033[34m║\033[0m")
        print("\033[34m╚" + "═" * (box_width - 2) + "╝\033[0m")

        # Connect to the database
        conn = sqlite3.connect("users.db")
        cursor = conn.cursor()

        # Calculate the total income by summing the `total_amount` column from the `orders` table
        cursor.execute("SELECT SUM(total_amount) FROM orders")
        total_income = cursor.fetchone()[0]  # Fetch the result

        if total_income is not None:
            # Display the total income
            print("\033[34m╔" + "═" * (box_width - 2) + "╗\033[0m")
            print("\033[34m║\033[0m \033[1;36mTotal Income: RM" + f"{total_income:.2f}".rjust(box_width - 19) + "\033[34m║\033[0m")
            print("\033[34m╚" + "═" * (box_width - 2) + "╝\033[0m")
        else:
            # Handle case where there are no orders
            print("\033[34m╔" + "═" * (box_width - 2) + "╗\033[0m")
            print("\033[34m║\033[0m \033[33mNo income data available.".ljust(box_width - 3) + "\033[34m║\033[0m")
            print("\033[34m╚" + "═" * (box_width - 2) + "╝\033[0m")

    except sqlite3.Error as e:
        # Handle database errors
        custom_clear_screen()
        print("\033[31m╔" + "═" * (box_width - 2) + "╗\033[0m")
        print("\033[31m║\033[0m \033[33mDatabase error occurred:".ljust(box_width - 3) + "\033[31m║\033[0m")
        print("\033[31m║\033[0m \033[33m" + str(e).ljust(box_width - 3) + "\033[31m║\033[0m")
        print("\033[31m╚" + "═" * (box_width - 2) + "╝\033[0m")
        input("\033[1;36mPress Enter to return to Track Financial...: \033[0m")
        return track_financial()

    finally:
        if conn:
            conn.close()  # Ensure the database connection is closed

    input("\033[1;36mPress Enter to return to Track Financial... \033[0m")
    return track_financial()

import re

def track_expense():
    """Displays a hardcoded total expense."""
    try:
        custom_clear_screen()  # Clear the screen at the start

        # Define box dimensions for proper alignment
        box_width = 58
        print("\033[34m╔" + "═" * (box_width - 2) + "╗\033[0m")
        print("\033[34m║\033[0m \033[1;36mTotal Expense Report" + " " * (box_width - 22) + "\033[34m║\033[0m")
        print("\033[34m╚" + "═" * (box_width - 2) + "╝\033[0m")

        total_expense = 1200.00  # Hardcoded expense value

        # Display the total expense
        print("\033[34m╔" + "═" * (box_width - 2) + "╗\033[0m")
        print("\033[34m║\033[0m \033[1;36mTotal Expense: RM" + f"{total_expense:.2f}".rjust(box_width - 19) + "\033[34m║\033[0m")
        print("\033[34m╚" + "═" * (box_width - 2) + "╝\033[0m")

    except Exception as e:
        # Handle unexpected errors
        print("\033[31m╔" + "═" * (box_width - 2) + "╗\033[0m")
        print("\033[31m║\033[0m \033[33mAn Error Occurred: " + str(e)[:36].ljust(36) + "\033[31m║\033[0m")
        print("\033[31m╚" + "═" * (box_width - 2) + "╝\033[0m")

    input("\033[1;36mPress Enter to return to Track Financial...\033[0m")
    return track_financial()

def track_profitability():
    """Displays total profit by calculating income minus expense."""
    conn = None  # Initialize the database connection
    try:
        custom_clear_screen()  # Clear the screen at the start

        # Define box dimensions for proper alignment
        box_width = 58
        print("\033[34m╔" + "═" * (box_width - 2) + "╗\033[0m")
        print("\033[34m║\033[0m \033[1;36mProfitability Report" + " " * (box_width - 24) + "\033[34m║\033[0m")
        print("\033[34m╚" + "═" * (box_width - 2) + "╝\033[0m")

        # Fetch the total income from the orders table
        conn = sqlite3.connect("users.db")
        cursor = conn.cursor()
        cursor.execute("SELECT SUM(total_amount) FROM orders")
        total_income = cursor.fetchone()[0]  # Get the total income

        # Hardcoded total expense (or replace with dynamic calculation if needed)
        total_expense = 1200.00

        # Calculate the total profit
        if total_income is None:
            total_income = 0.00  # Handle cases where there are no orders
        total_profit = total_income - total_expense

        # Display the total profit
        print("\033[34m╔" + "═" * (box_width - 2) + "╗\033[0m")
        print("\033[34m║\033[0m \033[1;36mTotal Profit: RM" + f"{total_profit:.2f}".rjust(box_width - 20) + "\033[34m║\033[0m")
        print("\033[34m╚" + "═" * (box_width - 2) + "╝\033[0m")

    except sqlite3.Error as e:
        # Handle database errors
        custom_clear_screen()
        print("\033[31m╔" + "═" * (box_width - 2) + "╗\033[0m")
        print("\033[31m║\033[0m \033[33mDatabase error occurred:".ljust(box_width - 3) + "\033[31m║\033[0m")
        print("\033[31m║\033[0m \033[33m" + str(e).ljust(box_width - 3) + "\033[31m║\033[0m")
        print("\033[31m╚" + "═" * (box_width - 2) + "╝\033[0m")
        input("\033[1;36mPress Enter to return to Track Financial...: \033[0m")
        return track_financial()

    finally:
        if conn:
            conn.close()  # Ensure the database connection is closed

    input("\033[1;36mPress Enter to return to Track Financial...\033[0m")
    return track_financial()












def control_inventory():
    """Menu for managing inventory."""
    while True:
        try:
            custom_clear_screen()  # Clear the screen at the start

            # Header box
            box_width = 58
            print("\033[34m╔" + "═" * (box_width - 2) + "╗\033[0m")
            print("\033[34m║\033[0m \033[1;36mInventory Control" + " " * (box_width - 20) + "\033[34m║\033[0m")
            print("\033[34m╠" + "═" * (box_width - 2) + "╣\033[0m")

            # Menu options
            menu_items = [
                "1. View Inventory",
                "2. Add Inventory",
                "3. Remove Inventory",
                "0. Back to Manager Menu"
            ]

            for item in menu_items:
                print("\033[34m║\033[0m \033[1;36m" + item.ljust(box_width - 3) + "\033[34m║\033[0m")

            # Bottom border
            print("\033[34m╚" + "═" * (box_width - 2) + "╝\033[0m")

            # User input
            choice = input("\033[1;36mChoose an option: \033[0m").strip()

            # Menu navigation
            if choice == "1":
                view_inventory()
            elif choice == "2":
                add_inventory()
            elif choice == "3":
                remove_inventory()
            elif choice == "0":
                custom_clear_screen()
                print("\033[1;36mReturning to Manager Menu...\033[0m")
                break
            else:
                # Invalid choice handling
                custom_clear_screen()
                print("\033[31m╔" + "═" * (box_width - 2) + "╗\033[0m")
                print("\033[31m║\033[0m \033[33mInvalid choice. Please try again." + " " * (box_width - 36) + "\033[31m║\033[0m")
                print("\033[31m╚" + "═" * (box_width - 2) + "╝\033[0m")
                input("\033[1;33mPress Enter to retry... \033[0m")
        except Exception as e:
            # Error handling
            custom_clear_screen()
            print("\033[31m╔" + "═" * (box_width - 2) + "╗\033[0m")
            print("\033[31m║\033[0m \033[33mAn Error Occurred: " + str(e)[:36].ljust(36) + "\033[31m║\033[0m")
            print("\033[31m╚" + "═" * (box_width - 2) + "╝\033[0m")
            input("\033[1;33mPress Enter to retry... \033[0m")



def view_inventory():
    try:
        custom_clear_screen()  # Clear the screen at the start

        # Define box dimensions for proper alignment
        box_width = 80
        print("\033[34m╔" + "═" * (box_width - 2) + "╗\033[0m")
        print("\033[34m║\033[0m \033[1;36mCurrent Inventory" + " " * (box_width - 21) + "\033[34m║\033[0m")
        print("\033[34m╠" + "═" * (box_width - 2) + "╣\033[0m")

        # Display inventory headers
        headers = f"{" "*20}{'Ingredient':<10} {'Quantity':<11} {'Unit':<20} {'Price (RM)'}"
        print("\033[34m║\033[0m " + headers.ljust(box_width - 3) + "\033[34m║\033[0m")
        print("\033[34m╠" + "═" * (box_width - 2) + "╣\033[0m")

        # Open the inventory file
        with open("inventory.txt", "r") as file:
            lines = file.readlines()

            # Skip the heading row from the file
            inventory_data = [line.strip() for line in lines if "|" in line and not line.startswith("+")]

            # Display inventory items
            if inventory_data:
                for line in inventory_data:
                    # Split the line and align data
                    parts = line.split('|')
                    if len(parts) >= 4:
                        ingredient = parts[0].strip()
                        quantity = parts[1].strip()
                        unit = parts[2].strip()
                        price = parts[3].strip()
                        row = f"{ingredient:<20} {quantity:<10} {unit:<10} {price:<10}"
                        print("\033[34m║\033[0m " + row.ljust(box_width - 3) + "\033[34m║\033[0m")
            else:
                # No inventory available
                print("\033[34m║\033[0m \033[33mNo inventory items available.".ljust(box_width - 3) + "\033[34m║\033[0m")

        # Close the table
        print("\033[34m╚" + "═" * (box_width - 2) + "╝\033[0m")

    except FileNotFoundError:
        # If the inventory file is missing
        print("\033[34m╔" + "═" * (box_width - 2) + "╗\033[0m")
        print("\033[34m║\033[0m \033[33mInventory file not found. Please check the system.".ljust(box_width - 3) + "\033[34m║\033[0m")
        print("\033[34m╚" + "═" * (box_width - 2) + "╝\033[0m")

    except Exception as e:
        # Handle unexpected errors
        print("\033[31m╔" + "═" * (box_width - 2) + "╗\033[0m")
        print("\033[31m║\033[0m \033[33mAn error occurred:".ljust(box_width - 3) + "\033[31m║\033[0m")
        print("\033[31m║\033[0m \033[33m" + str(e).ljust(box_width - 3) + "\033[31m║\033[0m")
        print("\033[31m╚" + "═" * (box_width - 2) + "╝\033[0m")

    input("\033[1;36mPress Enter to return to Inventory Control... \033[0m")
    return control_inventory()

def add_inventory():
    try:
        custom_clear_screen()  # Clear the screen at the start

        # Define box dimensions for proper alignment
        box_width = 80
        print("\033[34m╔" + "═" * (box_width - 2) + "╗\033[0m")
        print("\033[34m║\033[0m \033[1;36mAdd New Inventory Item" + " " * (box_width - 26) + "\033[34m║\033[0m")
        print("\033[34m╚" + "═" * (box_width - 2) + "╝\033[0m")

        # Input new item details
        ingredient = input("\033[1;36mEnter the ingredient name: \033[0m").strip()
        quantity = input("\033[1;36mEnter the quantity: \033[0m").strip()
        unit = input("\033[1;36mEnter the unit amount and type(e.g., Kg, L, pcs): \033[0m").strip()
        price = input("\033[1;36mEnter the price (RM): \033[0m").strip()

        # Validation for numeric inputs
        if not quantity.isdigit() or not price.isdigit():
            custom_clear_screen()
            print("\033[31m╔" + "═" * (box_width - 2) + "╗\033[0m")
            print("\033[31m║\033[0m \033[33mInvalid input. Quantity and Price must be numeric.".ljust(box_width - 3) + "\033[31m║\033[0m")
            print("\033[31m╚" + "═" * (box_width - 2) + "╝\033[0m")
            input("\033[1;33mPress Enter to return to Inventory Control... \033[0m")
            return control_inventory()

        # Write new item to the inventory file
        with open("inventory.txt", "a") as file:
            file.write(f"| {ingredient:<20} | {quantity:<10} | {unit:<20} | {price:<10} |\n")

        # Success message
        custom_clear_screen()
        print("\033[34m╔" + "═" * (box_width - 2) + "╗\033[0m")
        print("\033[34m║\033[0m \033[1;36mItem added successfully to the inventory.".ljust(box_width - 3) + "\033[34m║\033[0m")
        print("\033[34m╚" + "═" * (box_width - 2) + "╝\033[0m")
        input("\033[1;36mPress Enter to return to Inventory Control... \033[0m")

    except FileNotFoundError:
        # Handle missing inventory file
        print("\033[31m╔" + "═" * (box_width - 2) + "╗\033[0m")
        print("\033[31m║\033[0m \033[33mInventory file not found. Please check the system.".ljust(box_width - 3) + "\033[31m║\033[0m")
        print("\033[31m╚" + "═" * (box_width - 2) + "╝\033[0m")
        input("\033[1;33mPress Enter to return to Inventory Control... \033[0m")

    except Exception as e:
        # Handle unexpected errors
        custom_clear_screen()
        print("\033[31m╔" + "═" * (box_width - 2) + "╗\033[0m")
        print("\033[31m║\033[0m \033[33mAn error occurred:".ljust(box_width - 3) + "\033[31m║\033[0m")
        print("\033[31m║\033[0m \033[33m" + str(e).ljust(box_width - 3) + "\033[31m║\033[0m")
        print("\033[31m╚" + "═" * (box_width - 2) + "╝\033[0m")
        input("\033[1;33mPress Enter to return to Inventory Control... \033[0m")

def remove_inventory():
    """Function to remove an inventory item."""
    try:
        custom_clear_screen()  # Clear the screen at the start

        # Header box for Remove Inventory
        box_width = 80
        print("\033[34m╔" + "═" * (box_width - 2) + "╗\033[0m")
        print("\033[34m║\033[0m \033[1;36mRemove Inventory" + " " * (box_width - 20) + "\033[34m║\033[0m")
        print("\033[34m╚" + "═" * (box_width - 2) + "╝\033[0m")

        # Load the inventory
        with open('inventory.txt', 'r') as inventory_file:
            lines = inventory_file.readlines()

        # Parse inventory items and display them
        inventory = []
        print("\033[34m╔" + "═" * (box_width - 2) + "╗\033[0m")
        print("\033[34m║\033[0m \033[1;36m" + f"{'Index':<8}{'Ingredient':<20}{'Quantity':<10}{'Unit':<10}{'Price (RM)'}".ljust(box_width - 3) + "\033[34m║\033[0m")
        print("\033[34m╠" + "═" * (box_width - 2) + "╣\033[0m")

        actual_lines = []
        for i, line in enumerate(lines, start=1):  # Start index at 1 for user display
            if line.startswith('+') or line.startswith('-') or not line.strip() or 'Ingredient' in line:
                continue  # Skip decorative lines and headers
            parts = line.split('|')
            if len(parts) > 4:
                ingredient = parts[1].strip()
                quantity = parts[2].strip()
                unit = parts[3].strip()
                price = parts[4].strip()
                inventory.append((ingredient, quantity, unit, price))
                actual_lines.append(line)
                print("\033[34m║\033[0m " + f"{len(inventory):<8}{ingredient:<20}{quantity:<10}{unit:<10}{price}".ljust(box_width - 3) + "\033[34m║\033[0m")

        print("\033[34m╚" + "═" * (box_width - 2) + "╝\033[0m")

        if not inventory:
            # Handle empty inventory
            print("\033[31mNo items in inventory to remove.\033[0m")
            input("\033[1;36mPress Enter to return...\033[0m")
            return control_inventory()

        # Prompt the user to select an item to remove
        while True:
            choice = input("\033[1;36mEnter the index of the item to remove (or 0 to return): \033[0m").strip()
            if choice == "0":
                return control_inventory()
            if not choice.isdigit() or int(choice) < 1 or int(choice) > len(inventory):
                print("\033[31mInvalid choice. Please try again.\033[0m")
                continue

            index = int(choice) - 1
            selected_item = inventory[index]
            print(f"\033[1;36mSelected Item: {selected_item[0]}\033[0m")

            # Confirm removal
            confirm = input(f"\033[1;36mAre you sure you want to remove {selected_item[0]}? (y/n): \033[0m").strip().lower()
            if confirm == 'y':
                # Remove the item from the list and save changes
                actual_lines.pop(index)
                with open('inventory.txt', 'w') as inventory_file:
                    inventory_file.writelines(actual_lines)

                print("\033[32mItem removed successfully.\033[0m")
                input("\033[1;36mPress Enter to return...\033[0m")
                return control_inventory()
            else:
                print("\033[33mRemoval cancelled.\033[0m")
                input("\033[1;36mPress Enter to return...\033[0m")
                return control_inventory()

    except Exception as e:
        print(f"\033[31mError: {str(e)}\033[0m")
        input("\033[1;36mPress Enter to return...\033[0m")
        return control_inventory()


    except Exception as e:
        print(f"\033[31mError: {str(e)}\033[0m")
        input("\033[1;36mPress Enter to return...\033[0m")
        return control_inventory()





def review_customer_feedback():
    """Menu for reviewing customer feedback."""
    while True:
        try:
            custom_clear_screen()  # Clear the screen at the start

            # Header box
            box_width = 58
            print("\033[34m╔" + "═" * (box_width - 2) + "╗\033[0m")
            print("\033[34m║\033[0m \033[1;36mReview Customer Feedback" + " " * (box_width - 27) + "\033[34m║\033[0m")
            print("\033[34m╠" + "═" * (box_width - 2) + "╣\033[0m")

            # Menu options
            menu_items = [
                "1. View Feedback",
                "2. Delete Feedback",
                "0. Back to Manager Menu"
            ]

            for item in menu_items:
                print("\033[34m║\033[0m \033[1;36m" + item.ljust(box_width - 3) + "\033[34m║\033[0m")

            # Bottom border
            print("\033[34m╚" + "═" * (box_width - 2) + "╝\033[0m")

            # User input
            choice = input("\033[1;36mChoose an option: \033[0m").strip()

            # Menu navigation
            if choice == "1":
                view_feedback()
            elif choice == "2":
                delete_feedback()
            elif choice == "0":
                custom_clear_screen()
                print("\033[1;36mReturning to Manager Menu...\033[0m")
                break
            else:
                # Invalid choice handling
                custom_clear_screen()
                print("\033[31m╔" + "═" * (box_width - 2) + "╗\033[0m")
                print("\033[31m║\033[0m \033[33mInvalid choice. Please try again." + " " * (box_width - 36) + "\033[31m║\033[0m")
                print("\033[31m╚" + "═" * (box_width - 2) + "╝\033[0m")
                input("\033[1;33mPress Enter to retry... \033[0m")
        except Exception as e:
            # Error handling
            custom_clear_screen()
            print("\033[31m╔" + "═" * (box_width - 2) + "╗\033[0m")
            print("\033[31m║\033[0m \033[33mAn Error Occurred: " + str(e)[:36].ljust(36) + "\033[31m║\033[0m")
            print("\033[31m╚" + "═" * (box_width - 2) + "╝\033[0m")
            input("\033[1;33mPress Enter to retry... \033[0m")



def view_feedback():
    """Function to display customer feedback."""
    conn = None  # Initialize the connection to avoid UnboundLocalError
    try:
        custom_clear_screen()  # Clear the screen at the start

        # Define box dimensions for proper alignment
        box_width = 80
        print("\033[34m╔" + "═" * (box_width - 2) + "╗\033[0m")
        print("\033[34m║\033[0m \033[1;36mCustomer Feedback" + " " * (box_width - 20) + "\033[34m║\033[0m")
        print("\033[34m╚" + "═" * (box_width - 2) + "╝\033[0m")

        # Connect to the database
        conn = sqlite3.connect("users.db")
        cursor = conn.cursor()

        # Retrieve feedback from the `feedback` table
        cursor.execute("SELECT feedback_id, order_id, feedback FROM feedback")
        feedback_data = cursor.fetchall()

        if feedback_data:
            # Display table header
            print("\033[34m╔" + "═" * (box_width - 2) + "╗\033[0m")
            print("\033[34m║\033[0m \033[1;36m" + f"{'Feedback ID':<15} {'Order ID':<15} {'Feedback'}".ljust(box_width - 3) + "\033[34m║\033[0m")
            print("\033[34m╠" + "═" * (box_width - 2) + "╣\033[0m")

            # Display feedback records
            for feedback in feedback_data:
                feedback_id, order_id, feedback_text = feedback
                print("\033[34m║\033[0m " + f"{feedback_id:<15} {order_id:<15} {feedback_text}".ljust(box_width - 3) + "\033[34m║\033[0m")

            # Close the table
            print("\033[34m╚" + "═" * (box_width - 2) + "╝\033[0m")
        else:
            # If no feedback is present
            print("\033[34m╔" + "═" * (box_width - 2) + "╗\033[0m")
            print("\033[34m║\033[0m \033[33mNo feedback available.".ljust(box_width - 3) + "\033[34m║\033[0m")
            print("\033[34m╚" + "═" * (box_width - 2) + "╝\033[0m")

    except sqlite3.Error as e:
        # Handle database errors
        custom_clear_screen()
        print("\033[31m╔" + "═" * (box_width - 2) + "╗\033[0m")
        print("\033[31m║\033[0m \033[33mDatabase error occurred:".ljust(box_width - 3) + "\033[31m║\033[0m")
        print("\033[31m║\033[0m \033[33m" + str(e).ljust(box_width - 3) + "\033[31m║\033[0m")
        print("\033[31m╚" + "═" * (box_width - 2) + "╝\033[0m")
        input("\033[1;36mPress Enter to return to Review Customer Feedback...: \033[0m")
        return review_customer_feedback()

    finally:
        if conn:
            conn.close()  # Ensure the database connection is closed

    input("\033[1;36mPress Enter to return to Review Customer Feedback...: \033[0m")
    return review_customer_feedback()





def delete_feedback():
    """Function to delete customer feedback based on feedback_id."""
    conn = None  # Initialize the connection to avoid UnboundLocalError
    try:
        custom_clear_screen()  # Clear the screen at the start

        # Define box dimensions for proper alignment
        box_width = 80
        print("\033[34m╔" + "═" * (box_width - 2) + "╗\033[0m")
        print("\033[34m║\033[0m \033[1;36mDelete Customer Feedback" + " " * (box_width - 28) + "\033[34m║\033[0m")
        print("\033[34m╚" + "═" * (box_width - 2) + "╝\033[0m")

        conn = sqlite3.connect("users.db")
        cursor = conn.cursor()

        # Retrieve and display all feedback entries
        cursor.execute("SELECT feedback_id, order_id, feedback FROM feedback")
        feedback_data = cursor.fetchall()

        if feedback_data:
            # Display table header
            print("\033[34m╔" + "═" * (box_width - 2) + "╗\033[0m")
            print("\033[34m║\033[0m \033[1;36m" + f"{'Feedback ID':<15} {'Order ID':<15} {'Feedback'}".ljust(box_width - 3) + "\033[34m║\033[0m")
            print("\033[34m╠" + "═" * (box_width - 2) + "╣\033[0m")

            # Display feedback records
            for feedback in feedback_data:
                feedback_id, order_id, feedback_text = feedback
                print("\033[34m║\033[0m " + f"{feedback_id:<15} {order_id:<15} {feedback_text}".ljust(box_width - 3) + "\033[34m║\033[0m")

            # Close the table
            print("\033[34m╚" + "═" * (box_width - 2) + "╝\033[0m")

            # Prompt user for feedback_id to delete
            feedback_id_to_delete = input("\033[1;36mEnter the Feedback ID to delete: \033[0m").strip()

            # Check if the feedback_id exists
            cursor.execute("SELECT feedback_id FROM feedback WHERE feedback_id = ?", (feedback_id_to_delete,))
            if cursor.fetchone():
                confirm = input("\033[1;36mAre you sure you want to delete this feedback? (y/n): \033[0m").strip().lower()
                if confirm == 'y':
                    # Delete the feedback
                    cursor.execute("DELETE FROM feedback WHERE feedback_id = ?", (feedback_id_to_delete,))
                    conn.commit()

                    # Confirmation message
                    custom_clear_screen()
                    print("\033[34m╔" + "═" * (box_width - 2) + "╗\033[0m")
                    print("\033[34m║\033[0m \033[1;36mFeedback ID " + feedback_id_to_delete + " has been deleted successfully.".ljust(box_width - 3) + "\033[34m║\033[0m")
                    print("\033[34m╚" + "═" * (box_width - 2) + "╝\033[0m")
                else:
                    # Cancellation message
                    custom_clear_screen()
                    print("\033[34m╔" + "═" * (box_width - 2) + "╗\033[0m")
                    print("\033[34m║\033[0m \033[1;36mDeletion cancelled.".ljust(box_width - 3) + "\033[34m║\033[0m")
                    print("\033[34m╚" + "═" * (box_width - 2) + "╝\033[0m")
            else:
                # Feedback ID not found
                custom_clear_screen()
                print("\033[34m╔" + "═" * (box_width - 2) + "╗\033[0m")
                print("\033[34m║\033[0m \033[33mFeedback ID not found.".ljust(box_width - 3) + "\033[34m║\033[0m")
                print("\033[34m╚" + "═" * (box_width - 2) + "╝\033[0m")

        else:
            # No feedback available
            print("\033[34m╔" + "═" * (box_width - 2) + "╗\033[0m")
            print("\033[34m║\033[0m \033[33mNo feedback available.".ljust(box_width - 3) + "\033[34m║\033[0m")
            print("\033[34m╚" + "═" * (box_width - 2) + "╝\033[0m")

    except sqlite3.Error as e:
        # Handle database errors
        custom_clear_screen()
        print("\033[31m╔" + "═" * (box_width - 2) + "╗\033[0m")
        print("\033[31m║\033[0m \033[33mDatabase error occurred:".ljust(box_width - 3) + "\033[31m║\033[0m")
        print("\033[31m║\033[0m \033[33m" + str(e).ljust(box_width - 3) + "\033[31m║\033[0m")
        print("\033[31m╚" + "═" * (box_width - 2) + "╝\033[0m")
        input("\033[1;36mPress Enter to return to Review Customer Feedback...: \033[0m")
        return review_customer_feedback()

    finally:
        if conn:
            conn.close()  # Ensure the database connection is closed

    input("\033[1;36mPress Enter to return to Review Customer Feedback...: \033[0m")
    return review_customer_feedback()
