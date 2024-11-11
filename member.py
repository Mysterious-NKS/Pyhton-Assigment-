import sqlite3
from menu_data import food_list, drink_list

CART = []  # 全局购物车

def member_menu():
    while True:
        print("\n=== Member Login ===")
        username = input("Username: ")
        password = input("Password: ")
        
        if authenticate_member(username, password):
            order_menu(username)
            break

def authenticate_member(username, password):
    try:
        conn = sqlite3.connect('users.db')
        cursor = conn.cursor()
        cursor.execute('''
            SELECT * FROM users 
            WHERE username = ? AND password = ? AND user_type = "member"
        ''', (username, password))
        return cursor.fetchone() is not None
    finally:
        conn.close()

# 添加其他会员相关函数...
# browse_menu(), checkout(), track_order_status(), feedback() 等 