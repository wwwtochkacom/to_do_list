import secrets

from sqlalchemy import select
from sqlalchemy.orm import Session

from storage import TaskBase, engine


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
            "created_at": self.created_at,
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            task_id=TaskBase.id,
            title=TaskBase.title,
            desc=TaskBase.description,
            status=TaskBase.status,
            created_at=TaskBase.created_at,
        )

    def full_change_task(self, title, desc, status, task_id):
        with Session(engine) as session:
            task = session.get(TaskBase, task_id)

            if task is None:
                return

            task.title, task.description, task.status = title, desc, status
            session.commit()

    def part_change_task(self, data, task_id):
        with Session(engine) as session:
            mapping = {
                "title": "title",
                "description": "description",
                "status": "status",
                "created_at": "created_at",
            }
            task = session.get(TaskBase, task_id)
            for key, values in data.items():
                if key in mapping:
                    setattr(task, mapping[key], values)
                    setattr(self, mapping[key], values)
            session.commit()
        return self


class Manager:
    def __init__(self, dbtasks):
        self.dbtasks = dbtasks
        self.tasks = [Task.from_dict(el) for el in dbtasks]

    def add_task(self, title, desc):
        with Session(engine) as session:
            session.add(TaskBase(title=title, description=desc))
            session.commit()

    def find_task(self, task_id):
        with Session(engine) as session:
            stmt = select(TaskBase).where(TaskBase.id == task_id)
            stmt = session.execute(stmt).scalars().one()
            return stmt.toDict()

    def delete_task(self, task_id):
        task = self.find_task(task_id)
        if task is None:
            return False

        with Session(engine) as session:
            temp = session.get(TaskBase, task_id)
            session.delete(temp)
            session.commit()

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
        items.sort(key=lambda x: x["created_at"])
        return items
    elif parametr == "dateminus":
        items.sort(key=lambda x: x["created_at"], reverse=True)
        return items
    return items
