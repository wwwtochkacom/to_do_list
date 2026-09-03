import sqlite3
import json
import os
from config import JSON_PATH

connection = sqlite3.connect("data/todo.db")
cursor = connection.cursor()
# cursor.execute('''CREATE TABLE tasks (
#     task_id integer,
#     title text,
#     description text,
#     status text,
#     date DATE
#     )''')
# cursor.execute("INSERT INTO tasks VALUES (9460, 'qwsad', 'asdasd', 'Complete', '2026-08-19')")
cursor.execute("SELECT rowid, title FROM tasks")
print(cursor.fetchall())

connection.commit()
connection.close()


def save_tasks(tasks_data):
    with open(JSON_PATH, "w", encoding="utf-8") as f:
        json.dump(tasks_data, f, indent=4, ensure_ascii=False)


def load_json_file():
    if (
        os.path.exists(JSON_PATH) and os.path.getsize("data/todos.json") > 0
    ):  # Проверка на наличие файла и его размер
        with open(JSON_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    else:
        return []


jsontasks = load_json_file()