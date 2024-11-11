import sqlite3

def cashier_menu():
    while True:
        print("\n=== Cashier Login ===")
        username = input("Username: ")
        password = input("Password: ")
        
        if authenticate_cashier(username, password):
            manage_payments()
            break

def authenticate_cashier(username, password):
    try:
        conn = sqlite3.connect('users.db')
        cursor = conn.cursor()
        cursor.execute('''
            SELECT * FROM users 
            WHERE username = ? AND password = ? AND user_type = "cashier"
        ''', (username, password))
        return cursor.fetchone() is not None
    finally:
        conn.close()

# 添加其他收银员相关函数... 