from database import load_users
from chef import food_list, drink_list
import sqlite3
import textwrap
import os
CART = []
CURRENT_ORDER_ID = None

def clear_screen():
    os.system("cls")

# 1.1.0 会员登入
def member_login():
    clear_screen()
    print("\n╔══════════════════════════════════╗")
    print("║        Member Login              ║")
    print("╚══════════════════════════════════╝")
    while True:
        username = input("Please enter a username (press enter to undo) ► ")
        if username.lower() == '':
            return
            
        password = input("Please enter a password ► ")
        users = load_users()
        user_dict = {user[0]: user for user in users}

        user = user_dict.get(username)
        if user:
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
    clear_screen()
    while True:
        print("\n╔══════════════════════════════════╗")
        print("║        Member Menu               ║")
        print("╚══════════════════════════════════╝")
        print("1. Browse menu")
        print("2. view and modify cart")
        print("3. checkout")
        print("4. track order status")
        print("5. provide feedback")
        print("6. Exit")
        choice = input("\nPlease select an action (1-6) ► ")
        if choice == '1':
            browse_menu()
        elif choice == '2':
            view_and_modify_cart()
        elif choice == '3':
            checkout(username)
        elif choice == '4':
            track_order_status(username)
        elif choice == '5':
            feedback(username)
        elif choice == '6': 
            print(f"{username} Goodbye!")
            break
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
    print("\n╔══════════════════════════════════╗")
    print("║            MENU                  ║")
    print("╚══════════════════════════════════╝")
    
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
    clear_screen()
    menu = load_menu()
    if not menu:
        print("The menu is empty and cannot be browsed.")
        return

    while True:
        # 创建一个组合列表，包含所有食物和饮料
        all_items = food_list + drink_list
        display_menu(menu)
        choice = input("\nEnter the item number to add it to your cart, or press enter back to the main menu: ")
        
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


# 1.1.5 查看购物车
def view_and_modify_cart():
    clear_screen()
    if not CART:
        print("The shopping cart is empty.")
        return

    while True:
        print("\n╔══════════════════════════════════╗")
        print("║          SHOPPING CART           ║")
        print("╚══════════════════════════════════╝")
        total = 0
        for idx, item in enumerate(CART):
            print(f"{idx + 1}. {item['name']} - RM{item['price']} x {item['quantity']}")
            total += item['price'] * item['quantity']
        print(f"\nTotal: RM{total}\n")

        choice = input("\nEnter item number to modify, or press enter to return: ")
        if choice == '':
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
    global CURRENT_ORDER_ID
    clear_screen()
    if not CART:
        print("The shopping cart is empty and cannot be checked out.")
        return

    try:
        print("\n╔══════════════════════════════════╗")
        print("║          Order Summary           ║")
        print("╚══════════════════════════════════╝")
        total_amount = 0
        print("\nItems in your cart:")
        for item in CART:
            subtotal = item['price'] * item['quantity']
            total_amount += subtotal
            print(f"- {item['name']}")
            print(f"  Price: RM{item['price']} x {item['quantity']} = RM{subtotal}")
        
        print(f"\nTotal Amount: RM{total_amount}")
        
        print("\nPlease confirm your order details:")
        print("1. Confirm and place order")
        print("2. Back to Member Menu")
        
        choice = input("\nYour choice (1-3): ")
        
        if choice == '1':
            try:
                conn = sqlite3.connect('users.db')
                cursor = conn.cursor()

                # 获取用户ID
                cursor.execute('SELECT rowid FROM users WHERE username = ?', (username,))
                user_id = cursor.fetchone()[0]

                # 创建主订单记录
                cursor.execute('''
                INSERT INTO orders (user_id, total_amount)
                VALUES (?, ?)
                ''', (user_id, total_amount))
                
                # Store the order ID immediately after insertion
                CURRENT_ORDER_ID = cursor.lastrowid

                # 插入订单项目
                for item in CART:
                    cursor.execute('''
                    INSERT INTO order_items (order_id, item_name, price, quantity)
                    VALUES (?, ?, ?, ?)
                    ''', (CURRENT_ORDER_ID, item['name'], item['price'], item['quantity']))

                conn.commit()

                # 显示订单确认
                print("\n=== Order Confirmation ===")
                print(f"Order ID: {CURRENT_ORDER_ID}")
                print("\nItems ordered:")
                for item in CART:
                    print(f"- {item['name']}")
                    print(f"  Quantity: {item['quantity']}")
                    print(f"  Price per item: RM{item['price']}")
                    print(f"  Subtotal: RM{item['price'] * item['quantity']}")
                print(f"\nTotal Amount: RM{total_amount}")
                print("\nThank you for your purchase!")
                print("You can track your order status using the 'Track Order Status' option.")

                # Clear cart but keep CURRENT_ORDER_ID
                CART.clear()

            except sqlite3.Error as e:
                CURRENT_ORDER_ID = None  # Reset on error
                print(f"An error occurred while processing your order: {e}")
                print("Please try again later or contact support.")
            finally:
                if conn:
                    conn.close()
                    
        elif choice == '2':
            print("\nReturning to menu...")
            return
        elif choice == '3':
            print("\nCheckout cancelled.")
            return
        else:
            print("\nInvalid choice. Checkout cancelled.")
            
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        print("Please try again later or contact support.")


# 1.1.8 查看订单状态
def track_order_status(username):
    clear_screen()
    if CURRENT_ORDER_ID is None:
        print("No active order to track. Please make an order first.")
        return
    
    print("\n╔══════════════════════════════════╗")
    print("║          Order Tracking          ║")
    print("╚══════════════════════════════════╝")    
    try:
        conn = sqlite3.connect('users.db')
        cursor = conn.cursor()

        cursor.execute('''
        SELECT o.order_id, o.total_amount, o.status, o.order_date,
                GROUP_CONCAT(oi.item_name || ' (x' || oi.quantity || ')') as items
        FROM orders o
        LEFT JOIN order_items oi ON o.order_id = oi.order_id
        WHERE o.order_id = ?
        GROUP BY o.order_id
        ''', (CURRENT_ORDER_ID,))
        
        order = cursor.fetchone()
        
        if not order:
            print("Order not found.")
            return
            
        print("\nYour order status:")
        order_id, total_amount, status, order_date, items = order
        print(f"\nOrder ID: {order_id}")
        print(f"Items: {items}")
        print(f"Total Amount: RM{total_amount}")
        print(f"Status: {status}")
        print(f"Order Date: {order_date}")
        print("-" * 30)
            
    except sqlite3.Error as e:
        print(f"Error checking order status: {e}")
    finally:
        if conn:
            conn.close()


# 1.1.9 提供反馈
def feedback(username):
    clear_screen()
    
    if CURRENT_ORDER_ID is None:
        print("No active order to provide feedback. Please make an order first.")
        return
    
    print("\n╔══════════════════════════════════╗")
    print("║             Feedback             ║")
    print("╚══════════════════════════════════╝")    

    try:
        conn = sqlite3.connect('users.db')
        cursor = conn.cursor()

        # 获取用户ID
        cursor.execute('SELECT rowid FROM users WHERE username = ?', (username,))
        user_id = cursor.fetchone()[0]

        # 获取用户最近的订单及其商品
        cursor.execute('''
        SELECT o.order_id, o.total_amount, o.status,
                GROUP_CONCAT(oi.item_name || ' (x' || oi.quantity || ')') as items
        FROM orders o
        LEFT JOIN order_items oi ON o.order_id = oi.order_id
        WHERE o.user_id = ?
        GROUP BY o.order_id
        ORDER BY o.order_id DESC
        LIMIT 1
        ''', (user_id,))
        
        current_order = cursor.fetchone()
        
        if not current_order:
            print("No orders found. Please make an order first.")
            return

        order_id, total_amount, status, items = current_order
        print(f"\nProviding feedback for Order ID: {order_id}")
        print(f"Items: {items}")
        print(f"Total Amount: RM{total_amount}")
        print(f"Status: {status}")
        
        # 检查是否已经有反馈
        cursor.execute('SELECT feedback FROM feedback WHERE order_id = ?', (order_id,))
        existing_feedback = cursor.fetchone()
        
        if existing_feedback:
            print("\nYou have already provided feedback for this order:")
            print(f"Previous feedback: {existing_feedback[0]}")
            return

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
