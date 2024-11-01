import sqlite3

CART = []
production_log = []
equipment_log = []

#HEllO Can you see 
#ZY234


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

