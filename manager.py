import sqlite3

def manager_menu():
    while True:
        print("\n=== Manager Login ===")
        username = input("Username: ")
        password = input("Password: ")
        
        if authenticate_manager(username, password):
            manage_system()
            break

def authenticate_manager(username, password):
    try:
        conn = sqlite3.connect('users.db')
        cursor = conn.cursor()
        cursor.execute('''
            SELECT * FROM users 
            WHERE username = ? AND password = ? AND user_type = "manager"
        ''', (username, password))
        return cursor.fetchone() is not None
    finally:
        conn.close()

# 添加其他经理相关函数... 