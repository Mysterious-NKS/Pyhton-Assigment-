import sqlite3

def setup_database():
    """Initialize the database and create necessary tables"""
    try:
        conn = sqlite3.connect('users.db')
        cursor = conn.cursor()

        # Create users table
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            user_type TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        ''')

        # Create orders table
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS orders (
            order_id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            total_amount REAL NOT NULL,
            status TEXT DEFAULT 'pending',
            order_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
        ''')

        # Create order_items table
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS order_items (
            item_id INTEGER PRIMARY KEY AUTOINCREMENT,
            order_id INTEGER NOT NULL,
            item_name TEXT NOT NULL,
            price REAL NOT NULL,
            quantity INTEGER NOT NULL,
            FOREIGN KEY (order_id) REFERENCES orders(order_id)
        )
        ''')

        # Create feedback table
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS feedback (
            feedback_id INTEGER PRIMARY KEY AUTOINCREMENT,
            order_id INTEGER NOT NULL,
            feedback TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (order_id) REFERENCES orders(order_id)
        )
        ''')

        conn.commit()
        print("Database setup completed successfully.")
    except sqlite3.Error as e:
        print(f"An error occurred while setting up the database: {e}")
    finally:
        if conn:
            conn.close()


def execute_query(query, params=(), fetch=False):
    connection = None
    try:
        connection = sqlite3.connect('users.db')
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

def load_users():
    query = "SELECT username, password, user_type FROM users"
    result = execute_query(query, fetch=True)
    if result is None:
        print("Failed to load users from the database.")
        return []
    return result

def save_user(username, password, user_type):
    query = "INSERT INTO users (username, password, user_type) VALUES (?, ?, ?)"
    params = (username, password, user_type)
    result = execute_query(query, params)
    if result is not None:
        print("User information has been saved.")
    else:
        print("Failed to save user information.") 

