import sqlite3

CART = []
production_log = []
equipment_log = []

#HEllO Can you see 
#ZY
# 123456t
#test

#1.0.0 系统read user_data.txt
def main():
    while True:
        print("\nselect an operation:")
        print("1. register")
        print("2. login")
        print("3. logout")
        choice = input("Please enter an option (1-3): ")
        if choice == '1':
            register()
        elif choice == '2':
            login()
            break
        else:
            print("Invalid choice, please try again.")

# 1.0.1 创建数据库               
def setup_database():
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    
    # Create users table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL UNIQUE,
        password TEXT NOT NULL,
        user_type TEXT NOT NULL
    )
    ''')

    # Create orders table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS orders (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL,
        item_name TEXT NOT NULL,
        price REAL NOT NULL,
        quantity INTEGER NOT NULL,
        table_number INTEGER NOT NULL,
        FOREIGN KEY (username) REFERENCES users(username)
    )
    ''')
    
    conn.commit()
    conn.close()


#1.0.2 系统执行sql语句
def execute_query(query, params=(), fetch=False):
    try:
        # 连接到SQLite数据库
        conn = sqlite3.connect('users.db')
        cursor = conn.cursor()
        
        # 执行SQL查询
        cursor.execute(query, params)
        
        # 如果fetch为True，获取查询结果
        if fetch:
            result = cursor.fetchall()
        else:
            # 否则提交更改
            conn.commit()
            result = None
    except sqlite3.Error as e:
        # 捕获数据库错误并打印错误信息
        print(f"Database error: {e}")
        result = None
    finally:
        # 关闭数据库连接
        conn.close()
    
    # 返回查询结果
    return result


#1.0.3 读取用户信息 
def load_users():
    query = "SELECT username, password, user_type FROM users"
    return execute_query(query, fetch=True)


#1.0.4 保存用户信息 
def save_user(username, password, user_type):
    query = "INSERT INTO users (username, password, user_type) VALUES (?, ?, ?)"
    params = (username, password, user_type)
    result = execute_query(query, params)
    if result is not None:
        print("User information has been saved.")
    else:
        print("Failed to save user information.")


#1.0.5 注册界面
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


#1.0.6 登入前选择岗位
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
            manager_login()
        elif choice == '3':
            chef_login()
        elif choice == '4':
            cashier_login()
        elif choice == '5':
            main()
        else:
            print("Invalid choice, please try again.")


#1.1.0 会员登入
def member_login():
    print("\n==== Member Login ====")
    while True:
        username = input("Please enter a username: ")
        password = input("Please enter a password: ")
        users = load_users()
        user_dict = {user[0]: user for user in users}
        user = user_dict.get(username)
        if user and user[1] == password and user[2] == 'member':
            print("Login successful!")
            order_menu(username)  
            break
        else:
            print("Username or password is incorrect, or you are not a member. Please try again.")


#1.1.1   登入了可以干嘛
def order_menu(username):
    print("==== Member Menu ====")
    while True:
        print("\n1. Browse menu")
        print("2. Check shopping cart")
        print("3. Change order")
        print("4. Check out")
        print("5. Track order status")
        print("6. Provide feedback")
        print("7. Cancel bill and log out")
        print("8. Log out back to main menu")
        choice = input("Please select an action (1-8): ")
        if choice == '1':
            browse_menu()
        elif choice == '2':
            view_cart()
        elif choice == '3':
            modify_cart()
        elif choice == '4':
            checkout(username)  
        elif choice == '5':
            track_order_status(username)  
        elif choice == '6':
            provide_feedback()
        elif choice == '7':
            log_out()
        elif choice == '8':
            main()
        else:
            print("Invalid choice, please try again.")


# 1.1.2 登录后系统加载菜单
def load_menu():
    menu = []
    for item in food_list:
        menu.append({
            'name': item['name'],
            'price': item['price'],
            'description': item['recipe']  
        })
    return menu


# 1.1.3 登入后看菜单
def display_menu(menu):
    print("\n=== MENU ===")
    for idx, item in enumerate(menu):
        print(f"{idx + 1}. {item['name']} - RM{item['price']}\n  description : {item['description']}")


# 1.1.4 会员点单
def browse_menu():
    menu = load_menu()
    if not menu:
        print("The menu is empty and cannot be browsed.")
        return

    while True:
        display_menu(menu)
        choice = input("\nPlease enter the item number to add it to your cart, or enter '0' to return to the main menu: ")
        if choice == '0':
            break
        elif choice.isdigit() and 1 <= int(choice) <= len(menu):
            selected_item = menu[int(choice) - 1]
            quantity = input(f"Please enter the number you want to order {selected_item['name']} : ")
            if quantity.isdigit() and int(quantity) > 0:
                CART.append({'name': selected_item['name'], 'price': selected_item['price'], 'quantity': int(quantity)})
                print(f"{quantity} set {selected_item['name']} This item has been added to your cart.\n")
            else:
                print("Invalid quantity, please try again.")
        else:
            print("Invalid option, please try again.")


# 1.1.5 看看购物车都有啥
def view_cart():
    if not CART:
        print("The shopping cart is empty.")
        return

    print("\n=== SHOPPING CART ===")
    total = 0
    for item in CART:
        print(f"{item['name']} - RM{item['price']} x {item['quantity']}")
        total += item['price'] * item['quantity']
    print(f"\ntotal: RM{total}\n")


# 1.1.6 修改购物车内容
def modify_cart():
    if not CART:
        print("The shopping cart is empty and cannot be modified.")
        return

    while True:
        print("\n=== Modify shopping cart ===")
        for idx, item in enumerate(CART):
            print(f"{idx + 1}. {item['name']} - RM{item['price']} x {item['quantity']}")
        choice = input("\nPlease enter the product number to be modified, or enter '0' to return: ")
        if choice == '0':
            break
        elif choice.isdigit() and 1 <= int(choice) <= len(CART):
            selected_item = CART[int(choice) - 1]
            action = input(f"Do you want to change {selected_item['name']} quantity or delete it? (1. update quantity 2. delete): ")
            if action == '1':
                new_quantity = input("Please enter new quantity: ")
                if new_quantity.isdigit() and int(new_quantity) > 0:
                    selected_item['quantity'] = int(new_quantity)
                    print(f"{selected_item['name']} The quantity has been update to {new_quantity}。\n")
                else:
                    print("Invalid quantity, please try again.")
            elif action == '2':
                CART.pop(int(choice) - 1)
                print(f"{selected_item['name']} item has been deleted。\n")
        else:
            print("Invalid option, please retry.")


# 1.1.7 下单
def checkout(username):
    if not CART:
        print("The shopping cart is empty and cannot be checked out.")
        return

    view_cart()
    table_number = input("Please enter your table number: ")
    if not table_number.isdigit():
        print("Invalid table number.")
        return

    confirm = input("Confirm the order?(y/n): ")
    if confirm.lower() == 'y':
        conn = sqlite3.connect('users.db')
        cursor = conn.cursor()

        for item in CART:
            # Save to database
            cursor.execute('''
            INSERT INTO orders (username, item_name, price, quantity, table_number)
            VALUES (?, ?, ?, ?, ?)
            ''', (username, item['name'], item['price'], item['quantity'], int(table_number)))
            print(f"Table {table_number}: {item['name']} - RM{item['price']} x {item['quantity']}\n")
        
        conn.commit()
        conn.close()
        
        print(f"The order has been submitted for table number {table_number}, thank you for your purchase!")
        CART.clear()  # Clear the shopping cart
    else:
        print("The order has not been submitted.")


# 1.1.8 查看订单状态
def track_order_status(username):
    print("=== Order Tracking ===")
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    
    cursor.execute('''
    SELECT item_name, price, quantity FROM orders WHERE username = ?
    ''', (username,))
    
    orders = cursor.fetchall()
    
    if orders:
        print("Here are your current orders:")
        for order in orders:
            print(f"{order[0]} - RM{order[1]} x {order[2]}")
    else:
        print("You have no current orders.")
    
    conn.close()


# 1.1.9 提供反馈
def provide_feedback():
    print("=== Provide Feedback ===")
    table_number = input("Enter your table number: ")
    if not table_number.isdigit():
        print("Invalid table number.")
        return

    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    
    cursor.execute('''
    SELECT id FROM orders WHERE table_number = ?
    ''', (int(table_number),))
    
    orders = cursor.fetchall()
    
    if not orders:
        print("No orders found for this table number.")
        conn.close()
        return

    feedback = input("Please enter your feedback: ")
    with open('feedback.txt', 'a', encoding='utf-8') as feedback_file:
        feedback_file.write(f"Table {table_number}: {feedback}\n")
    
    print("Thank you for your feedback!")
    conn.close()


# 1.1.10 突然不想吃了取消订单
def log_out(username):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    
    cursor.execute('DELETE FROM orders WHERE username = ?', (username,))
    conn.commit()
    conn.close()
    
    CART.clear()  
    print("You have been logged out, the shopping cart has been cleared, and your orders have been cancelled.")
    main()

# 在调用 log_out() 时传递 username 参数
# 例如：log_out(current_username)


# 1.1.11 更新orders表
def update_orders_table():
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()  

    # Fetch existing data
    cursor.execute('SELECT id, username, item_name, price, quantity FROM orders')
    existing_orders = cursor.fetchall()

    # Drop the existing orders table
    cursor.execute('DROP TABLE IF EXISTS orders')

    # Create a new orders table with the table_number column
    cursor.execute('''
    CREATE TABLE orders (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL,
        item_name TEXT NOT NULL,
        price REAL NOT NULL,
        quantity INTEGER NOT NULL,
        table_number INTEGER NOT NULL,
        FOREIGN KEY (username) REFERENCES users(username)
    )
    ''')
    # Restore existing data (without table_number)
    for order in existing_orders:
        cursor.execute('''
        INSERT INTO orders (id, username, item_name, price, quantity, table_number)
        VALUES (?, ?, ?, ?, ?, ?)
        ''', (order[0], order[1], order[2], order[3], order[4], 0))  # Default table_number to 0 or handle appropriately

    conn.commit()
    conn.close()


#-----------------CHEF--------------------------------#
# 1.2.0 厨师登入
def chef_login():
    print("\n==== Chef Login ====")
    while True:
        username = input("Please enter a username: ")
        password = input("Please enter a password: ")
        users = load_users()
        user_dict = {user[0]: user for user in users}
        user = user_dict.get(username)
        if user and user[1] == password and user[2] == 'chef':
            print("Login successful!")
            chef_settings()  
            break
        else:
            print("Username or password is incorrect, or you are not a chef. Please try again.")


# 1.2.1 厨师菜单
food_list = [
    {"name": "burger", "price": 15, "recipe": "Delicious beef burgers"},
    {"name": "pizza", "price": 20, "recipe": "pepperoni"},
    {"name": "salad", "price": 10, "recipe": "Healthy green salad"},
    {"name": "sushi", "price": 25, "recipe": "Fresh sushi platter"},
    {"name": "tacos", "price": 12, "recipe": "Spicy Mexican tacos"},
    {"name": "pasta", "price": 18, "recipe": "Classic Italian pasta"}
]


food_inv = {
    "bread": {"quantity": 100, "unit": "10kg"},
    "pepperoni": {"quantity": 50, "unit": "20kg"},
    "ham": {"quantity": 30, "unit":  "30kg"},
    "lettuce": {"quantity": 75, "unit": "40kg"},
    "tomato sauce": {"quantity": 20, "unit": "10000ml"},
    "fish": {"quantity": 50, "unit": "50kg"},
    "rice": {"quantity": 100, "unit": "60kg"},
    "tomato": {"quantity": 12, "unit": "70kg"},
    "chicken": {"quantity": 50, "unit": "80kg"},
    "flour": {"quantity": 500, "unit": "90kg"}
}


# 1.2.2 添加菜品
def add_recipe():
    print("Please insert your recipe")
    print("Press Enter without typing anything to finish.")
    while True:
        food = input("Name (press Enter to finish): ").strip()

        if not food:
            break

        if not food:
            print("Food name is required.")
            continue

        price = input("Price (press Enter to skip): ").strip()
        recipe = input("Recipe (press Enter to skip): ").strip()
        if not price:
            price = 0
        else:
            try:
                price = float(price)
            except ValueError:
                print("Invalid price entered. Defaulting to empty.")
                price = "Empty"
        if not recipe:
            recipe = "No recipe provided"

        new_recipe = {
            "name": food,
            "price": price,
            "recipe": recipe
        }

        food_list.append(new_recipe)
        print(f"Added Name: {food}, Price: {price}, Recipe: {recipe}")

    print("\nUpdated Recipe List:")
    for item in food_list:
        print(f"Name: {item['name']}, Price: {item['price']}, Recipe: {item['recipe']}")


# 1.2.3 删除菜品
def remove_recipe():
    print("==== Delete Food ====")
    name_q = input("Enter the food name to remove everything: ").strip()
    exit_choice = input("Do you want to proceed with deletion? (yes to proceed / no to cancel): ")

    if exit_choice == 'no':
        print("Exiting the process...")
        return

    recipe_found = False

    for this_list in food_list:
        if this_list['name'] == name_q:
            food_list.remove(this_list)
            print(f"Dish '{name_q}' along with its price and recipe has been deleted!")
            recipe_found = True
            break

        if not recipe_found:
            print("Recipe not found.")


# 1.2.4 更新菜品
def update_dish():
    update_txt = input("Enter the name of the food to update: ")

    for item in food_list:
        if item['name'] == update_txt:
            print(f"Current dish: ")
            print(f"Name: {item['name']}, Price: {item['price']}, Recipe: {item['recipe']}")

            new_name = input("Enter new name (press Enter to skip): ")
            new_price = input("Enter new price (press Enter to skip): ")
            new_recipe = input("Enter new recipe (press Enter to skip): ")

            if new_name:
                item['name'] = new_name
            if new_price:
                try:
                    item['price'] = float(new_price)
                except ValueError:
                        print("Invalid price. Keeping the old price.")
            if new_recipe:
                item['recipe'] = new_recipe

            print(f"Dish '{update_txt}' updated successfully!\n")
            return

    print(f"'{update_txt}' not found in the food list.\n")


# 1.2.5 查看菜品
def view_dish():
    print("==== Menu ====")
    if not food_list:
        print("The food list is currently empty.")
        return

    for item in food_list:
        print(f"Name: {item['name']}")
        print(f"Price: RM{item['price']}")
        print(f"Recipe: {item['recipe']}")
        print("" * 20)


# 1.2.6 查看库存
def check_inv():
    print("==== Inventory Check ====")
    print("Enter the ingredient to proceed. ")
    check_ing = input("Ingredient: ")
    if check_ing in food_inv:
        quantity = food_inv[check_ing]["quantity"]
        unit = food_inv[check_ing]["unit"]
        print(f"= {check_ing.capitalize()} =")
        print(f"Quantity: {quantity}   Weight: {unit}")
    else:
        print(f"'{check_ing.capitalize()}' not available in the inventory.")


# 1.2.7 记录生产
def rec_production():
    dish_name = input("Enter the name of the dish produced: ")
    batch_number = input("Enter batch number: ")
    quantity = input("Enter production quantity: ")
    expiration_date = input("Enter expiration date (YYYY-MM-DD): ")

    production_log.append({
        "dish_name": dish_name,
        "batch_number": batch_number,
        "quantity": quantity,
        "expiration_date": expiration_date
        })
    print(f"Production record for '{dish_name}' added successfully!\n")


# 1.2.8 查看生产
def view_production():
    print("==== Production Log ====")
    if not production_log:
        print("No production records available.")
    else:
        for record in production_log:
            print(f"Dish: {record['dish_name']}")
            print(f"Batch Number: {record['batch_number']}")
            print(f"Quantity: {record['quantity']}")
            print(f"Expiration Date: {record['expiration_date']}")
            print("-" * 30)


def rec_production():  
    dish_name = input("Enter the name of the dish produced: ")  
    batch_number = input("Enter batch number: ")   
    quantity = input("Enter production quantity: ") 
    expiration_date = input("Enter expiration date (YYYY-MM-DD): ")  
    production_log.append({ 
                        "dish_name": dish_name,   
                        "batch_number": batch_number, 
                        "quantity": quantity,      
                        "expiration_date": expiration_date    
                        })  
    print(f"Production record for '{dish_name}' added successfully!\n")


def view_production():   
    print("==== Production Log ====")  
    if not production_log:  
        print("No production records available.")  
    else:      
        for record in production_log:       
            print(f"Dish: {record['dish_name']}")    
            print(f"Batch Number: {record['batch_number']}")  
            print(f"Quantity: {record['quantity']}")      
            print(f"Expiration Date: {record['expiration_date']}")    
            print("-"*30)


# 1.2.9 报告设备问题
def report_equip_i():
    equipment_name = input("Enter equipment name: ")
    issue_description = input("Describe the malfunction or maintenance need: ")

    equipment_log.append({
        "equipment_name": equipment_name,
        "issue_description": issue_description
    })
    print(f"Issue reported for '{equipment_name}' successfully!\n")


# 1.2.10 查看设备问题
def view_equip_i():
    print("==== Equipment Issues Log ====")
    if not equipment_log:
        print("No equipment issues reported.")
    else:
        for issue in equipment_log:
            print(f"Equipment: {issue['equipment_name']}")
            print(f"Issue: {issue['issue_description']}")
            print("-"*30)


# 1.2.11 厨师设置
def chef_settings():
    while True:
        print("==== Chef Settings ====")
        print("1. Add Dish")
        print("2. Update Dish")
        print("3. Delete Dish")
        print("4. View Dish")
        print("5. Check Inventory")
        print("6. Record Production")
        print("7. View production")
        print("8. Report Equipment Issues")
        print("9. View Equipment Issues")
        print("0. Exit")
        choice = input("Choose an option: ")
        if choice == "1":
            add_recipe()
        elif choice == "2":
            update_dish()
        elif choice == "3":
            remove_recipe()
        elif choice == "4":
            view_dish()
        elif choice == "5":
            check_inv()
        elif choice == "6":
            rec_production()
        elif choice == "7":
            view_production()
        elif choice == '8': 
            report_equip_i()
        elif choice == '9':  
            view_equip_i()
        elif choice == "0":
            print("Exiting Chef Settings...")
            return
        else:
            print("Invalid choice, please try again.")


#-------------------------------MANAGER--------------------------------------------#
def manager_login():
    print("\n==== Manager Login ====")
    while True:
        username = input("Please enter a username: ")
        password = input("Please enter a password: ")
        users = load_users()
        user_dict = {user[0]: user for user in users}
        user = user_dict.get(username)
        if user and user[1] == password and user[2] == 'manager':
            print("Login successful!")
            manager_menu()  
            break
        else:
            print("Username or password is incorrect, or you are not a manager. Please try again.")


def manager_menu():
    while True:
        print("\n==== Manager Menu ====")
        print("1. Manage User Accounts")
        print("2. Oversee Order Details")
        print("3. Track Financial")
        print("4. Control Inventory")
        print("5. Review Customer Feedback")
        print("0. Exit")
        choice = input("Choose an option: ")

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
            main()  
        else:
            print("Invalid choice, please try again.")


def manage_user_accounts():
    while True:
        print("==== Manage User Accounts ====")
        print("1. Add User")
        print("2. Remove User")
        print("3. View Users")
        print("0. Exit")
        choice = input("Choose an option: ")    

        if choice == "1":
            add_user()
        elif choice == "2":
            remove_user()
        elif choice == "3":
            view_users()
        elif choice == "0":
            print("Exiting Manage User Accounts...")
            break


def add_user():
    pass


def remove_user():
    username = input("Enter the username to remove: ")
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    
    cursor.execute('SELECT username FROM users WHERE username = ?', (username,))
    user = cursor.fetchone()
    
    if user:
        cursor.execute('DELETE FROM users WHERE username = ?', (username,))
        conn.commit()
        print(f"User '{username}' removed successfully!")
    else:
        print(f"User '{username}' not found.")
    
    conn.close()


def view_users():
    pass


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
    pass


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



#-------------------------------CASHIER--------------------------------------------#
def cashier_login():
    pass



if __name__ == '__main__':
    main()
