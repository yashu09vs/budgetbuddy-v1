#libraries
import sqlite3
import os


def connect_db():  # function to connect to database
    base_dir = os.path.dirname(os.path.abspath(__file__))
    data_folder = os.path.join(base_dir, 'data')
    os.makedirs(data_folder, exist_ok=True)


    db_path = os.path.join(data_folder, 'budget.db')
    print("📄 DB path:", db_path)  # Optional debug can be removed
    conn = sqlite3.connect(db_path)
    return conn


def initialize_db():
    conn = connect_db()
    cursor = conn.cursor()
    #creates an expense table if it doesnt exist, ! safe to run more than once !
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS expenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            amount REAL NOT NULL,
            category TEXT NOT NULL,
            date TEXT NOT NULL,
            notes TEXT
        )
    ''')
    conn.commit() #save changes
    conn.close()  #close connection to database


def get_all_expenses():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM expenses')
    rows = cursor.fetchall()
    conn.close()
    return rows
