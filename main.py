from member import member_menu
from chef import chef_menu
from manager import manager_menu
from cashier import cashier_menu
from database import setup_database
import sqlite3

def main():  
    while True:
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

def main():
    setup_database()  # 确保数据库和表已创建
    
    while True:
        print("\n=== Welcome to Restaurant System ===")
        print("1. Member Login")
        print("2. Chef Login")
        print("3. Manager Login")
        print("4. Cashier Login")
        print("5. Exit")
        
        choice = input("\nPlease enter your choice (1-5): ")
        
        if choice == '1':
            member_menu()
        elif choice == '2':
            chef_menu()
        elif choice == '3':
            manager_menu()
        elif choice == '4':
            cashier_menu()
        elif choice == '5':
            print("\nThank you for using our system. Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main() 