import datetime
import secrets
import sqlite3

from storage import save_tasks


class Task:
    def __init__(self, title, desc, status, created_at, task_id=None):
        self.id = task_id or secrets.randbelow(900000) + 100000
        self.title = title
        self.desc = desc
        self.status = status
        self.created_at = created_at

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "description": self.desc,
            "status": self.status,
            "date": self.created_at,
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            task_id=data[0],
            title=data[1],
            desc=data[2],
            status=data[3],
            created_at=data[4],
        )

    def full_change_task(self, title, desc, status, task_id):
        with sqlite3.connect("data/tasks.db") as connection:
            cursor = connection.cursor()
            cursor.execute(
                """UPDATE tasks
                SET title = ?, description = ?, status = ?
                WHERE id = (?)""",
                (title, desc, status, task_id),
            )
            connection.commit()
            return

    def part_change_task(self, data, task_id):
        mapping = {
            "title": "title",
            "description": "desc",
            "status": "status",
            "date": "created_at",
        }
        for key, values in data.items():
            if key in mapping:
                setattr(self, mapping[key], values)
            
            with sqlite3.connect("data/tasks.db") as connection:
                cursor = connection.cursor()
                cursor.execute(
                    f"""UPDATE tasks
                    SET {key} = ?
                    WHERE id = (?)""",
                    (values, task_id),
                )
        return self


class Manager:
    def __init__(self, dbtasks):
        self.dbtasks = dbtasks
        self.tasks = [Task.from_dict(el) for el in dbtasks]

    def save(self):
        update = [i.to_dict() for i in self.tasks]
        self.dbtasks[:] = update
        save_tasks(self.dbtasks)

    def add_task(self, title, desc):
        status = "Not complete"
        created_at = datetime.date.today().isoformat()
        with sqlite3.connect("data/tasks.db") as connection:
            cursor = connection.cursor()
            cursor.execute(
                """INSERT INTO tasks (id, title, description, status, date)
            VALUES (?, ?, ?, ?, ?)""",
                (secrets.randbelow(900000) + 100000, title, desc, status, created_at),
            )

    def find_task(self, task_id):
        with sqlite3.connect("data/tasks.db") as connection:
            cursor = connection.cursor()
            cursor.execute(
                "SELECT id, title, description, status, date FROM tasks WHERE id = (?)",
                (task_id,),
            )
            temp = cursor.fetchone()
            return {
                "id": temp[0],
                "title": temp[1],
                "description": temp[2],
                "status": temp[3],
                "date": temp[4],
            }

    def delete_task(self, task_id):
        task = self.find_task(task_id)
        if task is None:
            return False
        with sqlite3.connect("data/tasks.db") as connection:
            cursor = connection.cursor()
            cursor.execute("""DELETE FROM tasks WHERE id = (?)""", (task_id,))
        return True

    def filter_task(self, parametr) -> list:
        seq = []
        for t in self.tasks:
            if t.status == parametr:
                seq.append(t.to_dict())
        return seq


def sorted_list(items: list, parametr: str) -> list:
    if items is None:
        return []  # Защита от None на входе
    if parametr == "dateplus":
        items.sort(key=lambda x: x["date"])
        return items
    elif parametr == "dateminus":
        items.sort(key=lambda x: x["date"], reverse=True)
        return items
    return items
