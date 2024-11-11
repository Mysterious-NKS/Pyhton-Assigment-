import sqlite3

def chef_menu():
    while True:
        print("\n=== Chef Login ===")
        username = input("Username: ")
        password = input("Password: ")
        
        if authenticate_chef(username, password):
            manage_orders()
            break

def authenticate_chef(username, password):
    try:
        conn = sqlite3.connect('users.db')
        cursor = conn.cursor()
        cursor.execute('''
            SELECT * FROM users 
            WHERE username = ? AND password = ? AND user_type = "chef"
        ''', (username, password))
        return cursor.fetchone() is not None
    finally:
        conn.close()

# 添加其他厨师相关函数... 