import json
import os
import sqlite3

from config import JSON_PATH

connection = sqlite3.connect("data/tasks.db")
cursor = connection.cursor()
cursor.execute("""
CREATE TABLE IF NOT EXISTS  tasks (
    id INTEGER PRIMARY KEY,
    title TEXT ,
    description TEXT,
    status BOOLEAN DEFAULT FALSE, 
    date DATE NOT NULL
)
""")

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
