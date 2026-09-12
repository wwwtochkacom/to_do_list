import os
import sqlite3

from config import JSON_PATH

with sqlite3.connect("data/tasks.db") as connection:
    cursor = connection.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS  tasks (
        id INTEGER PRIMARY KEY,
        title TEXT ,
        description TEXT,
        status TEXT, 
        date DATE NOT NULL
    )
    """)



def save_tasks(tasks_data):
    # print(tasks_data, len(tasks_data)) 
    with sqlite3.connect("data/tasks.db") as connection:
        cursor = connection.cursor()
        cursor.execute(
            '''INSERT INTO tasks (id, title, description, status, date)
                VALUES (?, ?, ?, ?, ?)''',
                tasks_data[-1],
                )


def load_tasks():
    if (
        os.path.exists("data/tasks.db") and os.path.getsize("data/tasks.db") > 0
    ):  # Проверка на наличие файла и его размер
        with sqlite3.connect("data/tasks.db") as connection:
            cursor = connection.cursor()
            cursor.execute('''SELECT id, title, description, status, date FROM tasks''')
            return cursor.fetchall()
    else:
        return []

def render_page():
    with sqlite3.connect("data/tasks.db") as connection:
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM tasks")
        return cursor.fetchall()

dbtasks = load_tasks()