from database import setup_database, load_users, save_user
from member import member_login
from chef import chef_login

from cashier import cashier_login

def register():
    print("==== User Registration ====")
    username = input("Please enter a username: ")
    password = input("Please enter a password: ")
    user_type = input("Please enter the user type (member/manager/chef/cashier): ")
    if user_type not in ['member', 'manager', 'chef', 'cashier']:
        print("Invalid user type, please try again.")
        return
    users = load_users()
    if any(user[0] == username for user in users):
        print("Username already exists, please try another username.")
    else:
        save_user(username, password, user_type)
        print("Registration successful!")

def login():
    print("\n==== User Login ====")
    while True:
        print("\nPlease select:")
        print("1. member")
        print("2. manager")
        print("3. chef")
        print("4. cashier")
        print("5. undo")
        choice = input("Please enter an option (1-5): ")
        if choice == '1':
            member_login()
        elif choice == '2':
            pass
        elif choice == '3':
            chef_login()
        elif choice == '4':
            cashier_login()
        elif choice == '5':
            print("\nThank you for using our system. Goodbye!")
            break
        else:
            print("Invalid choice, please try again.")

def main():
    while True:
        print("\n==== Welcome to the Restaurant Management System ====")
        print("\nselect an operation:")
        print("1. register")
        print("2. login")
        print("3. exit")
        choice = input("Please enter an option (1-3): ")
        if choice == '1':
            register()
        elif choice == '2':
            login()
        elif choice == '3':
            print("Exiting the program.")
            break
        else:
            print("Invalid choice, please try again.")

if __name__ == '__main__':
    setup_database()
    main() 