import datetime
from storage import jsontasks, save_tasks
import secrets

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
            task_id=data.get("id"),
            title=data.get("title"),
            desc=data.get("description"),
            status=data.get("status"),
            created_at=data.get("date"),
        )

    def full_change_task(self, title, desc, status):
        self.title = title
        self.desc = desc
        self.status = status
        self.created_at = datetime.date.today().isoformat()
        return self

    def part_change_task(self, data):
        mapping = {
            "title": "title",
            "description": "desc",
            "status": "status",
            "date": "created_at",
        }
        for key, values in data.items():
            if key in mapping:
                setattr(self, mapping[key], values)

        return self


class Manager:
    def __init__(self, jsontasks):
        self.jsontasks = jsontasks
        self.tasks = [Task.from_dict(el) for el in jsontasks]

    def save(self):
        update = [i.to_dict() for i in self.tasks]
        self.jsontasks[:] = update
        save_tasks(self.jsontasks)

    def add_task(self, title, desc):
        status = "Not complete"
        created_at = datetime.date.today().isoformat()
        task = Task(title, desc, status, created_at)
        self.tasks.append(task)
        self.save()

    def find_task(self, task_id):
        for t in self.tasks:
            if t.id == task_id:
                return t
        return None

    def delete_task(self, task_id):
        task = self.find_task(task_id)
        if task is None:
            return False
        self.tasks.remove(task)
        self.save()
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
    elif parametr == 'dateminus':
        items.sort(key=lambda x: x["date"], reverse=True)
        return items
    return items

 # def sort_task(self, parametr):
    #     seq = list(self.tasks)
    #     if parametr == "dateplus":
    #         seq.sort(key=lambda x: x.created_at)
    #         return seq
    #     elif parametr == 'dateminus':
    #         seq.sort(key=lambda x: x.created_at, reverse=True)
    #         return seq