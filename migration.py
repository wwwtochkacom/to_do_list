import json
import sqlite3

from config import DB_PATH, JSON_PATH


# Миграция данных из JSON файла в DB
def migrate_json_to_db():
    with open(JSON_PATH, "r", encoding="utf-8") as f:
        j = json.load(f)

    x = []
    for m in j:
        x.append(list(m.values()))

    connection = sqlite3.connect(DB_PATH)
    cursor = connection.cursor()

    for i in range(len(x)):
        cursor.execute(
            """INSERT INTO tasks (id, title, description, status, created_at)
                    VALUES (?, ?, ?, ?, ?)""",
            x[i],
        )

    connection.commit()
    connection.close()


if __name__ == "__main__":
    migrate_json_to_db()
