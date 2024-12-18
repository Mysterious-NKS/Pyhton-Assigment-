from database import setup_database, load_users, save_user
from member import member_login
from chef import chef_login
from manager import manager_login
from cashier import cashier_login
import os

def clear_screen():
    os.system("cls")

def register():
    clear_screen()
    print("\n╔══════════════════════════════════╗")
    print("║        User Registration         ║")
    print("╚══════════════════════════════════╝")
    username = input(" what is your username ► ").strip()
    password = input(" what is your password ► ").strip()
    print("\n╔══════════════════════════════════╗")
    print("║ Select User Type:                ║")
    print("║ 1. Member                        ║")
    print("║ 2. Manager                       ║")
    print("║ 3. Chef                          ║")
    print("║ 4. Cashier                       ║")
    print("╚══════════════════════════════════╝")
    type_choice = input(" what is your user type ► ")
    
    # 用户类型映射
    type_map = {
        '1': 'member',
        '2': 'manager',
        '3': 'chef',
        '4': 'cashier'
    }
    
    user_type = type_map.get(type_choice)
    
    if not user_type:
        print("\nInvalid user type! ❌")
        input("\nPress Enter to continue...")
        return
        
    users = load_users()
    if any(user[0] == username for user in users):
        print("Username already exists! ❌")
        input("\nPress Enter to continue...")
    else:
        save_user(username, password, user_type)
        print("\nRegistration successful! ✓")

def login():
    while True:
        clear_screen()
        print("\n╔══════════════════════════╗")
        print("║  Login Menu              ║")
        print("╠══════════════════════════╣")
        print("║  Please select:          ║")
        print("║  1. Member               ║")
        print("║  2. Manager              ║")
        print("║  3. Chef                 ║")
        print("║  4. Cashier              ║")
        print("║  5. Back                 ║")
        print("╚══════════════════════════╝")

        choice = input("\nPlease enter an option (1-5): ")
        
        if choice == '1':
            member_login()
        elif choice == '2':
            manager_login()
        elif choice == '3':
            chef_login()
        elif choice == '4':
            cashier_login()
        elif choice == '5':
            print("\n" + "*" * 40)
            print("*  Back to main page  *")
            print("*" * 40 + "\n")
            break
        else:
            print("\n" + "!" * 35)
            print("!  Invalid choice, please try again.  !")
            print("!" * 35)

def main():
    while True:
        print("\n╔══════════════════════════╗")
        print("║  LIANG Restaurant        ║")
        print("╠══════════════════════════╣")
        print("║  Please select:          ║")
        print("║  1. Register             ║")
        print("║  2. Login                ║")
        print("║  3. Exit                 ║")
        print("╚══════════════════════════╝")
        
        choice = input("\nPlease enter an option (1-3): ")
        
        if choice == '1':
            register()
        elif choice == '2':
            login()
        elif choice == '3':
            print("\n" + "*" * 40)
            print("* Thank you for using our system. Goodbye! *") 
            print("*" * 40 + "\n")
            break
        else:
            print("\n" + "!" * 35)
            print(" Invalid choice, please try again. ")
            print("!" * 35)

if __name__ == '__main__':
    setup_database()
    main() 