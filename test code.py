import sqlite3

CART = []
production_log = []
equipment_log = []

# track order ,pending,complete,cooking
# user key exit 可以退出
# 开一个database for receipt discount(结账界面,有用discount的在隔壁行显示用了多少)
#order id 不重复when叫多个食物

# 1.0.0 主菜单  
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



# 1.0.1 创建数据库
def setup_database():
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()

    # Create orders table if it doesn't exist (removed DROP TABLE)
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS orders (
        order_id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        item_name TEXT NOT NULL,
        price REAL NOT NULL,
        quantity INTEGER NOT NULL,
        status TEXT DEFAULT 'pending',
        FOREIGN KEY (user_id) REFERENCES users(id)
    )
    ''')

    # Create users table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL UNIQUE,
        password TEXT NOT NULL,
        user_type TEXT NOT NULL
    )
    ''')

    # Create feedback table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS feedback (
        feedback_id INTEGER PRIMARY KEY AUTOINCREMENT,
        order_id INTEGER NOT NULL,
        feedback TEXT NOT NULL,
        FOREIGN KEY (order_id) REFERENCES orders(order_id)
    )
    ''')

    conn.commit()
    conn.close()


# 1.0.2 系统执行sql语句
def execute_query(query, params=(), fetch=False):
    connection = None
    try:
        connection = sqlite3.connect('users.db')  # 确保路径正确
        cursor = connection.cursor()
        cursor.execute(query, params)
        if fetch:
            result = cursor.fetchall()
            return result
        connection.commit()
    except sqlite3.Error as e:
        print(f"Database error: {e}")
    finally:
        if connection:
            connection.close()
    return None


# 1.0.3 读取用户信息
def load_users():
    query = "SELECT username, password, user_type FROM users"
    result = execute_query(query, fetch=True)
    if result is None:
        print("Failed to load users from the database.")
        return []
    return result


# 1.0.4 保存用户信息
def save_user(username, password, user_type):
    query = "INSERT INTO users (username, password, user_type) VALUES (?, ?, ?)"
    params = (username, password, user_type)
    result = execute_query(query, params)
    if result is not None:
        print("User information has been saved.")
    else:
        print("Failed to save user information.")


# 1.0.5 注册界面
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


# 1.0.6 登入前选择岗位
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


# 1.1.0 会员登入
def member_login():
    print("\n==== Member Login ====")
    while True:
        username = input("Please enter a username: ")
        password = input("Please enter a password: ")
        users = load_users()
        user_dict = {user[0]: user for user in users}

        user = user_dict.get(username)
        if user:
            print(f"Found user: {user}")
            if user[1] == password and user[2] == 'member':
                print("Login successful!")
                order_menu(username)
                break
            else:
                print("Password is incorrect or you are not a member.")
        else:
            print("Username not found.")


# 1.1.1   登入了可以干嘛
def order_menu(username):
    print("==== Member Menu ====")
    while True:
        print("\n1. Browse menu")
        print("2. Check shopping cart")
        print("3. Change order")
        print("4. Check out")
        print("5. Track order status")
        print("6. Provide feedback")
        print("7. Exit")
        choice = input("Please select an action (1-7): ")
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
            feedback(username)
        elif choice == '7':
            exit(username)
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
    
    print("\nFood:")
    print(f"+{'-' * 5}+{'-' * 15}+{'-' * 12}+{'-' * 52}+")
    print(f"| {'No.':<3} | {'Name':<13} | {'Price (RM)':<10} | {'Recipe':<50} |")
    print(f"+{'-' * 5}+{'-' * 15}+{'-' * 12}+{'-' * 52}+")

    if not food_list:
        print(f"| {'No food items available':<84} |")
    else:
        for idx, item in enumerate(food_list, 1):
            wrapped_name = textwrap.wrap(item['name'], width=13)
            wrapped_price = textwrap.wrap(f"{item['price']:.2f}", width=10)
            wrapped_recipe = textwrap.wrap(item['recipe'], width=50)

            print(f"| {idx:<3} | {wrapped_name[0]:<13} | {wrapped_price[0]:<10} | {wrapped_recipe[0]:<50} |")
            
            for line in wrapped_name[1:]:
                print(f"| {'':<3} | {line:<13} | {'':<10} | {'':<50} |")

            for line in wrapped_price[1:]:
                print(f"| {'':<3} | {'':<13} | {line:<10} | {'':<50} |")

            for line in wrapped_recipe[1:]:
                print(f"| {'':<3} | {'':<13} | {'':<10} | {line:<50} |")

    print(f"+{'-' * 5}+{'-' * 15}+{'-' * 12}+{'-' * 52}+")

    print("\nDrink:")
    print(f"+{'-' * 5}+{'-' * 15}+{'-' * 12}+{'-' * 52}+")
    print(f"| {'No.':<3} | {'Name':<13} | {'Price (RM)':<10} | {'Recipe':<50} |")
    print(f"+{'-' * 5}+{'-' * 15}+{'-' * 12}+{'-' * 52}+")

    if not drink_list:
        print(f"| {'No drink items available':<84} |")
    else:
        for idx, item in enumerate(drink_list, len(food_list) + 1):
            wrapped_name = textwrap.wrap(item['name'], width=13)
            wrapped_price = textwrap.wrap(f"{item['price']:.2f}", width=10)
            wrapped_recipe = textwrap.wrap(item['recipe'], width=50)

            print(f"| {idx:<3} | {wrapped_name[0]:<13} | {wrapped_price[0]:<10} | {wrapped_recipe[0]:<50} |")
            
            for line in wrapped_name[1:]:
                print(f"| {'':<3} | {line:<13} | {'':<10} | {'':<50} |")

            for line in wrapped_price[1:]:
                print(f"| {'':<3} | {'':<13} | {line:<10} | {'':<50} |")

            for line in wrapped_recipe[1:]:
                print(f"| {'':<3} | {'':<13} | {'':<10} | {line:<50} |")

    print(f"+{'-' * 5}+{'-' * 15}+{'-' * 12}+{'-' * 52}+")
    print("")



# 1.1.4 会员点单
def browse_menu():
    menu = load_menu()
    if not menu:
        print("The menu is empty and cannot be browsed.")
        return

    while True:
        # 创建一个组合列表，包含所有食物和饮料
        all_items = food_list + drink_list
        display_menu(menu)
        choice = input("\nPlease enter the item number to add it to your cart, or press enter to return to the main menu: ")
        
        if choice == '':
            break
        elif choice.isdigit() and 1 <= int(choice) <= len(all_items):  # 修改这里的判断条件
            selected_item = all_items[int(choice) - 1]  # 使用组合列表获取选中项
            quantity = input(f"Please enter the number you want to order {selected_item['name']} : ")
            if quantity.isdigit() and int(quantity) > 0:
                CART.append({
                    'name': selected_item['name'], 
                    'price': selected_item['price'], 
                    'quantity': int(quantity)
                })
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
            action = input(
                f"Do you want to change {selected_item['name']} quantity or delete it? (1. update quantity 2. delete): ")
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

    confirm = input("Confirm the order?(y/n): ")
    if confirm.lower() == 'y':
        try:
            conn = sqlite3.connect('users.db')
            cursor = conn.cursor()

            # 获取 user_id
            cursor.execute('SELECT id FROM users WHERE username = ?', (username,))
            user_id = cursor.fetchone()[0]

            # 存储所有新创建的订单ID
            new_order_ids = []

            for item in CART:
                # Save to database
                cursor.execute('''
                INSERT INTO orders (user_id, item_name, price, quantity)
                VALUES (?, ?, ?, ?)
                ''', (user_id, item['name'], item['price'], item['quantity']))
                
                # 获取最新插入的订单ID
                new_order_ids.append(cursor.lastrowid)
                print(f"Order: {item['name']} - RM{item['price']} x {item['quantity']}")

            conn.commit()  # 确保提交事务
            
            # 打印所有新创建的订单ID
            print("\nOrder IDs for your reference:")
            for order_id in new_order_ids:
                print(f"Order ID: {order_id}")
            
            print("\nThe order has been submitted, thank you for your purchase!")
            
        except sqlite3.Error as e:
            print(f"An error occurred while saving the order: {e}")
        finally:
            if conn:
                conn.close()  # 确保关闭连接

        CART.clear()  # Clear the shopping cart
    else:
        print("The order has not been submitted.")


# 1.1.8 查看订单状态
def track_order_status(username):
    print("=== Order Tracking ===")
    try:
        conn = sqlite3.connect('users.db')
        cursor = conn.cursor()

        # 获取用户ID
        cursor.execute('SELECT id FROM users WHERE username = ?', (username,))
        user_id = cursor.fetchone()[0]

        # 查询该用户的所有订单
        cursor.execute('''
        SELECT order_id, item_name, price, quantity, status 
        FROM orders 
        WHERE user_id = ?
        ORDER BY order_id DESC
        ''', (user_id,))
        
        orders = cursor.fetchall()
        
        if not orders:
            print("You have no order records yet.")
            return
            
        print("\nYour order status:")
        for order in orders:
            order_id, item, price, quantity, status = order
            print(f"\nOrder ID: {order_id}")
            print(f"Item: {item}")
            print(f"Price: RM{price}")
            print(f"Quantity: {quantity}")
            print(f"Status: {status if status else 'pending'}")
            print("-" * 30)
            
    except sqlite3.Error as e:
        print(f"check order status error: {e}")
    finally:
        if conn:
            conn.close()


# 1.1.9 提供反馈
def feedback(username):
    print("\n=== Feedback ===")
    try:
        conn = sqlite3.connect('users.db')
        cursor = conn.cursor()

        # 获取用户ID
        cursor.execute('SELECT id FROM users WHERE username = ?', (username,))
        user_id = cursor.fetchone()[0]

        # 获取用户最近的订单ID
        cursor.execute('''
        SELECT order_id, item_name, price, quantity 
        FROM orders 
        WHERE user_id = ? 
        ORDER BY order_id DESC 
        LIMIT 1''', (user_id,))
        
        latest_order = cursor.fetchone()
        
        if not latest_order:
            print("No orders found. Please make an order first.")
            return

        order_id = latest_order[0]
        print(f"\nProviding feedback for Order ID: {order_id}")
        print(f"Item: {latest_order[1]}")
        print(f"Price: RM{latest_order[2]}")
        print(f"Quantity: {latest_order[3]}")
        
        # 获取用户反馈
        feedback_text = input("\nPlease enter your feedback: ")
        
        # 保存反馈
        cursor.execute('''
        INSERT INTO feedback (order_id, feedback)
        VALUES (?, ?)
        ''', (order_id, feedback_text))
        
        conn.commit()
        print("\nThank you for your feedback!")

    except sqlite3.Error as e:
        print(f"Error submitting feedback: {e}")
    finally:
        if conn:
            conn.close()



# -------------------------------------------------------------CHEF---------------------------------------------------------------------#
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
            
def save_menu_to_file(food_list, drink_list):
    with open('menu.txt', 'w') as file:
        # Set column widths based on maximum lengths for each column
        name_width = max(max(len(item['name']) for item in food_list),
                        max(len(item['name']) for item in drink_list),
                        len("Name"))
        price_width = len("Price (RM)")
        recipe_width = max(max(len(item['recipe']) for item in food_list),
                        max(len(item['recipe']) for item in drink_list),
                        len("Recipe"))

        # Define the horizontal separator for the table
        separator = "+-{}-+-{}-+-{}-+\n".format('-' * name_width, '-' * price_width, '-' * recipe_width)

        # Write food menu header
        file.write("Food:\n")
        file.write(separator)
        file.write("| {:<{}} | {:<{}} | {:<{}} |\n".format("Name", name_width, "Price (RM)", price_width, "Recipe", recipe_width))
        file.write(separator)

        # Write food items
        for item in food_list:
            file.write("| {:<{}} | {:<{}} | {:<{}} |\n".format(
                item['name'], name_width,
                item['price'], price_width,
                item['recipe'], recipe_width
            ))

        file.write(separator + "\n")

        # Write drink menu header
        file.write("Drink:\n")
        file.write(separator)
        file.write("| {:<{}} | {:<{}} | {:<{}} |\n".format("Name", name_width, "Price (RM)", price_width, "Recipe", recipe_width))
        file.write(separator)

        # Write drink items
        for item in drink_list:
            file.write("| {:<{}} | {:<{}} | {:<{}} |\n".format(
                item['name'], name_width,
                item['price'], price_width,
                item['recipe'], recipe_width
            ))

        file.write(separator)

    print("Menu has been saved to 'menu.txt' with the requested table format.")

# 1.2.1 厨师菜单
food_list = [
    {"name": "Burger", "price": 15, "recipe": "Delicious beef burgers"},
    {"name": "Pizza", "price": 20, "recipe": "Pepperoni"},
    {"name": "Salad", "price": 10, "recipe": "Healthy green salad"},
    {"name": "Sushi", "price": 25, "recipe": "Fresh sushi platter"},
    {"name": "Tacos", "price": 12, "recipe": "Spicy Mexican tacos"},
    {"name": "Pasta", "price": 18, "recipe": "Classic Italian pasta"}
]

drink_list = [
    {"name": "Tea", "price": 4, "recipe": "A warm tea from hometown"},
    {"name": "Water", "price": 1.50, "recipe": "Average fresh water"}
]

food_inv = {
    "Bread": {"quantity": 100, "unit": "10Kg"},
    "Pepperoni": {"quantity": 50, "unit": "20Kg"},
    "Ham": {"quantity": 30, "unit": "30Kg"},
    "Lettuce": {"quantity": 75, "unit": "40Kg"},
    "Bottle tomato sauce": {"quantity": 20, "unit": "10L"},
    "Fish": {"quantity": 50, "unit": "50Kg"},
    "Rice": {"quantity": 100, "unit": "60Kg"},
    "Tomato": {"quantity": 12, "unit": "70Kg"},
    "Chicken": {"quantity": 50, "unit": "80Kg"},
    "Flour": {"quantity": 500, "unit": "90Kg"}
}


# 1.2.2 添加菜品
def add_recipe():
    print("Please insert your recipe")
    print("Press Enter without typing anything to finish.")

    while True:
        food = input("Name (press Enter to finish): ").strip()

        if not food:
            break

        ask_menu = input("Type ('food' or 'drink'): ").strip().lower()
        if ask_menu not in ["food", "drink"]:
            print("Invalid type. Must be 'food' or 'drink'.")
            continue

        price = input("Price (press Enter to skip): ").strip()
        recipe = input("Recipe (press Enter to skip): ").strip()

        if not price:
            price = 0
        else:
            try:
                price = float(price)
            except ValueError:
                print("Invalid price entered. Defaulting to 0.")
                price = 0

        if not recipe:
            recipe = "No recipe provided"

        new_recipe = {
            "name": food,
            "price": price,
            "recipe": recipe
        }

        if ask_menu == "food":
            food_list.append(new_recipe)
        else:
            drink_list.append(new_recipe)

        print("\nAdded successfully!")
        print(f"+{'-' * 22}+{'-' * 12}+{'-' * 52}+")
        print(f"| {'Name':<20} | {'Price (RM)':<10} | {'Recipe':<50} |")
        print(f"+{'-' * 22}+{'-' * 12}+{'-' * 52}+")
        print(f"| {new_recipe['name']:<20} | {new_recipe['price']:<10.2f} | {new_recipe['recipe']:<50} |")
        print(f"+{'-' * 22}+{'-' * 12}+{'-' * 52}+")
        print("")

        save_menu_to_file(food_list, drink_list)  # Save the updated menu
        print(f"Menu saved to file after adding '{food}'.")

# 1.2.3 删除菜品
def remove_recipe():
    print("==== Delete Food and Drinks ====")
    name_q = input("Enter the food or drink name to remove: ").strip()
    exit_choice = input("Do you want to proceed with deletion? (yes to proceed / no to cancel): ")

    if exit_choice.lower() == 'no':
        print("Exiting the process...")
        return

    for item_list, label in [(food_list, "food"), (drink_list, "drink")]:
        for item in item_list:
            if item['name'] == name_q:
                item_list.remove(item)
                print(f"'{name_q}' along with its price and recipe has been deleted from {label} list!")
                save_menu_to_file(food_list, drink_list)  # Save the updated menu
                print(f"Menu saved to file after removing '{name_q}'.")
                return

    print("Recipe not found.")


# 1.2.4 更新菜品
import textwrap

def update_menu():
    update_txt = input("Enter the name of the food or drink to update: ")

    for item_list, label in [(food_list, "food"), (drink_list, "drink")]:
        for item in item_list:
            if item['name'] == update_txt:
                print("\nCurrent menu item details:")
                print(f"+{'-' * 22}+{'-' * 12}+{'-' * 52}+")
                print(f"| {'Name':<20} | {'Price (RM)':<10} | {'Recipe':<50} |")
                print(f"+{'-' * 22}+{'-' * 12}+{'-' * 52}+")

                # Display current details
                print(f"| {item['name']:<20} | {item['price']:<10.2f} | {item['recipe']:<50} |")
                print(f"+{'-' * 22}+{'-' * 12}+{'-' * 52}+")

                new_name = input("\nEnter new name (press Enter to skip): ")
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

                print(f"\n{label.capitalize()} '{update_txt}' updated successfully!")
                save_menu_to_file(food_list, drink_list)  # Save the updated menu
                print(f"Menu saved to file after updating '{update_txt}'.")
                return

    print(f"'{update_txt}' not found in the food or drink lists.\n")


# 1.2.5 查看菜品
import textwrap

def view_menu():
    print("==== Menu ====")

    print("\nFood:")
    print(f"+{'-' * 22}+{'-' * 12}+{'-' * 52}+")
    print(f"| {'Name':<20} | {'Price (RM)':<10} | {'Recipe':<50} |")
    print(f"+{'-' * 22}+{'-' * 12}+{'-' * 52}+")

    if not food_list:
        print(f"| {'No food items available':<86} |")
    else:
        for item in food_list:
            wrapped_name = textwrap.wrap(item['name'], width=20)
            wrapped_price = textwrap.wrap(f"{item['price']:.2f}", width=10)  # Price formatted to 2 decimal places
            wrapped_recipe = textwrap.wrap(item['recipe'], width=50)

            print(f"| {wrapped_name[0]:<20} | {wrapped_price[0]:<10} | {wrapped_recipe[0]:<50} |")

            for line in wrapped_name[1:]:
                print(f"| {line:<20} | {'':<10} | {'':<50} |")

            for line in wrapped_price[1:]:
                print(f"| {'':<20} | {line:<10} | {'':<50} |")

            for line in wrapped_recipe[1:]:
                print(f"| {'':<20} | {'':<10} | {line:<50} |")

    print(f"+{'-' * 22}+{'-' * 12}+{'-' * 52}+")

    print("\nDrink:")
    print(f"+{'-' * 22}+{'-' * 12}+{'-' * 52}+")
    print(f"| {'Name':<20} | {'Price (RM)':<10} | {'Recipe':<50} |")
    print(f"+{'-' * 22}+{'-' * 12}+{'-' * 52}+")

    if not drink_list:
        print(f"| {'No drink items available':<86} |")
    else:
        for item in drink_list:
            wrapped_name = textwrap.wrap(item['name'], width=20)
            wrapped_price = textwrap.wrap(f"{item['price']:.2f}", width=10)
            wrapped_recipe = textwrap.wrap(item['recipe'], width=50)

            print(f"| {wrapped_name[0]:<20} | {wrapped_price[0]:<10} | {wrapped_recipe[0]:<50} |")

            for line in wrapped_name[1:]:
                print(f"| {line:<20} | {'':<10} | {'':<50} |")

            for line in wrapped_price[1:]:
                print(f"| {'':<20} | {line:<10} | {'':<50} |")

            for line in wrapped_recipe[1:]:
                print(f"| {'':<20} | {'':<10} | {line:<50} |")

    print(f"+{'-' * 22}+{'-' * 12}+{'-' * 52}+")
    print("")


# 1.2.6 查看库存
def checking_inv():
    with open("inventory.txt", "w") as file:
        # Prompt user for choice
        print("==== Inventory Check ====")
        choice = input(
            "Do you want to check a specific ingredient or display the whole list? (enter 'specific' or 'all'): ").strip()

        if choice == 'specific':
            check_ing = input("Enter the ingredient: ").strip().lower()
            if check_ing in food_inv:
                quantity = food_inv[check_ing]["quantity"]
                unit = food_inv[check_ing]["unit"]

                # Write header and specific ingredient info to file
                file.write("==== Inventory Check ====\n")
                file.write(f"+{'-' * 22}+{'-' * 12}+{'-' * 52}+\n")
                file.write(f"| {'Ingredient':<20} | {'Quantity':<10} | {'Unit':<50} |\n")
                file.write(f"+{'-' * 22}+{'-' * 12}+{'-' * 52}+\n")

                # Wrap unit text if it's too long
                if len(unit) > 50:
                    wrapped_unit = textwrap.fill(unit, width=50)
                    wrapped_lines = wrapped_unit.split('\n')
                    file.write(f"| {check_ing.capitalize():<20} | {quantity:<10} | {wrapped_lines[0]:<50} |\n")
                    for line in wrapped_lines[1:]:
                        file.write(f"| {' ':<20} | {' ':<10} | {line:<50} |\n")
                else:
                    file.write(f"| {check_ing.capitalize():<20} | {quantity:<10} | {unit:<50} |\n")

                file.write(f"+{'-' * 22}+{'-' * 12}+{'-' * 52}+\n")
                print(f"'{check_ing.capitalize()}' has been saved to 'inventory.txt'.")
            else:
                print(f"'{check_ing.capitalize()}' not available in the inventory.")
                file.write(f"'{check_ing.capitalize()}' not available in the inventory.\n")

        elif choice == 'all':
            # Write header for full inventory list
            file.write("==== Inventory List ====\n")
            file.write(f"+{'-' * 22}+{'-' * 12}+{'-' * 52}+\n")
            file.write(f"| {'Ingredient':<20} | {'Quantity':<10} | {'Unit':<50} |\n")
            file.write(f"+{'-' * 22}+{'-' * 12}+{'-' * 52}+\n")

            # Write each item in the inventory to file
            for ingredient, details in food_inv.items():
                unit = details['unit']
                if len(unit) > 50:
                    wrapped_unit = textwrap.fill(unit, width=50)
                    wrapped_lines = wrapped_unit.split('\n')
                    file.write(f"| {ingredient.capitalize():<20} | {details['quantity']:<10} | {wrapped_lines[0]:<50} |\n")
                    for line in wrapped_lines[1:]:
                        file.write(f"| {' ':<20} | {' ':<10} | {line:<50} |\n")
                else:
                    file.write(f"| {ingredient.capitalize():<20} | {details['quantity']:<10} | {unit:<50} |\n")

            file.write(f"+{'-' * 22}+{'-' * 12}+{'-' * 52}+\n")
            print("Full inventory has been saved to 'inventory.txt'.")

        else:
            print("Invalid choice. Please enter 'specific' or 'all'.")


# 1.2.7 记录生产
def rec_production():
    food_name = input("Enter the name of the food or drink produced: ")
    batch_number = input("Enter batch number food or drink (required 10 characters) : ")
    if len(batch_number) != 10:
        print("Batch number must be 10 characters or fewer. Please try again.")
        return

    quantity = input("Enter production quantity: ")
    expiration_date = input("Enter expiration date (YYYY-MM-DD): ")

    production_log.append({
        "food_name": food_name,
        "batch_number": batch_number,
        "quantity": quantity,
        "expiration_date": expiration_date
        })
    print(f"Production record for '{food_name}' added successfully!\n")

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
            print("-" * 30)


# 1.2.11 厨师设置
def chef_settings():
    while True:
        print("==== Chef Settings ====")
        print("1. Add Food/Drink")
        print("2. Update Food/Drink")
        print("3. Delete Food/Drink")
        print("4. View Menu")
        print("5. Check Inventory")
        print("6. Record Production")
        print("7. View production")
        print("8. Report Equipment Issue")
        print("9. View Equipment Issues")
        print("0. Exit")

        choice = input("Choose an option: ")
        if choice == "1":
            add_recipe()
        elif choice == "2":
            update_menu()
        elif choice == "3":
            remove_recipe()
        elif choice == "4":
            view_menu()
        elif choice == "5":
            checking_inv()
        elif choice == "6":
            rec_production()
        elif choice == "7":
            view_production()
        elif choice == '8':
            report_equip_i()
        elif choice == '9':
            view_equip_i()
        elif choice == "0":
            print("Exiting...")
            break
        else:
            print("Invalid choice, please try again.")


# -------------------------------MANAGER--------------------------------------------#
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
        cursor.execute("SELECT username, user_type FROM users")
        users = cursor.fetchall() #fetchall is Fetch All
        #Displaying the users
        if users:
            print(f"{'Username':<15}{'User Type'.upper():<15}") #This is to make a header, the arrows are for the alignment and the number is the width
            print("-"*30) #This is just to make a line below the header
            for user in users:
                print(f"{user[0]:<20}{user[1]:<10}")
        else:
            print("No users found in the data base.")
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


# -------------------------------CASHIER--------------------------------------------#
def cashier_login():
    print("\n==== Cashier Login ====")
    while True:
        username = input("Please enter a username: ")
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

    while True:
        print("\n==== Cashier Menu ====")
        print("1. View Menu")
        print("2. Take Order")
        print("3. Manage Discounts for Order")
        print("4. Generate Receipt")
        print("5. Generate Sales Report")
        print("0. Exit")
        choice = input("Choose an option: ")

        if choice == "1":
            view_menu()
        elif choice == "2":
            take_order_menu()
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

def product_display_menu():
    print("\n==== Product Display ====")
    view_menu()
    input("\nPress Enter to return to the Cashier Menu.")

# Initialize a dictionary to store the current order
current_order = {}

def take_order_menu():
    print("==== Take Order ====")
    while True:
        all_items = food_list + drink_list
        
        print("Available items to order:")
        for idx, item in enumerate(all_items, 1):
            print(f"{idx}. {item['name']} - RM{item['price']} ({item['recipe']})")
        
        choice = input("\nPlease enter the item number to add it to your cart, or press enter to finish: ").strip()
        
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


if __name__ == '__main__':
    setup_database()  # 确保数据库和表已创建
    main()
