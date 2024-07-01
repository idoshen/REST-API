import sqlite3

def create_connection():
    conn = sqlite3.connect('user_management.db')
    return conn

def create_table(conn):
    create_table_sql = """
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        email TEXT NOT NULL,
        password TEXT NOT NULL
    );
    """
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except sqlite3.Error as e:
        print(e)

if __name__ == '__main__':
    conn = create_connection()
    create_table(conn)
    conn.close()
