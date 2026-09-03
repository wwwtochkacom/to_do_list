from flask import Flask, request, url_for, redirect, render_template
from task import Manager, sorted_list
from storage import jsontasks
from validators import validate_patch, validate_put
from config import PORT, DEBUG
import math

task_manager = Manager(jsontasks)

app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def hello():
    return '<a href="/todos"><h1> Главная </h1></a>'


@app.route("/todos", methods=["GET", "POST"])
def hello_world():
    filter_active = False
    status = request.args.get("status")
    sort = request.args.get("sort")
    
    html_list = [el.to_dict() for el in task_manager.tasks]

    if html_list:
        if status:
            filter_active = True
            html_list = task_manager.filter_task(status)
            if html_list == []:
                return "<h2> Решенных задач нет </h2>"
        if sort:
            filter_active = True
            html_list = sorted_list(html_list, sort)

        page = request.args.get("page", default=1, type=int)
        limit = request.args.get("limit", default=10, type=int)
        html_pag = html_list[(page - 1) * limit : page * limit]
        dlina = math.ceil(len(html_list) / limit)
        return render_template(
            "todos.html",
            html_pag=html_pag,
            dlina=dlina,
            filter_active=filter_active,
            page=page,
            limit=limit,
            status=status,
            sort=sort,
        )

    else:
        return """
        <a href="/todos/create/"><h1> Создать задачу </h1></a> 
        <h1> Список пуст </h1>"""


@app.route("/todos/create", methods=["GET", "POST"])
def add_task():
    if request.method == "POST":
        task_manager.add_task(request.form["title"], request.form["description"])

        return redirect("/todos/create")

    return render_template("create.html")


# Веб-интерфейс редактирования задач
@app.route("/todos/<int:task_id>/edit", methods=["GET", "POST"])
def update_task(task_id):
    task = task_manager.find_task(task_id)
    if task is None:
        return "<h2> Не найдена задача </h2>", 404

    else:
        if request.method == "GET":
            return render_template("edit.html", task=task)
        else:
            data = {
                "title": request.form["title"],
                "description": request.form["description"],
                "status": request.form["status"],
            }

            task.full_change_task(data["title"], data["description"], data["status"])
            task_manager.save()
            return redirect("/todos")


# JSON API интерфейс
@app.route("/todos/<int:task_id>", methods=["PUT"])
def api_put_task(task_id):
    task = task_manager.find_task(task_id)
    if task is None:
        return "<h2> Не найдена задача </h2>", 404
    else:
        data = request.get_json()
        if validate_put(data) is None:
            return "<h2> Не правильный ввод данных </h2>", 404
        else:
            task.full_change_task(data["title"], data["description"], data["status"])
            task_manager.save()
            return task.to_dict()


# JSON API интерфейс
@app.route("/todos/<int:task_id>", methods=["PATCH"])
def api_patch_task(task_id):
    task = task_manager.find_task(task_id)
    if task is None:
        return "<h2> Не найдена задача </h2>", 404
    else:
        data = request.get_json()
        if validate_patch(data) is None:
            return "<h2> Не правильный ввод данных </h2>", 404
        else:
            task.part_change_task(data)
            task_manager.save()
            return task.to_dict()


@app.route("/todos/<int:task_id>/delete", methods=["POST", "DELETE"])
def delete_task(task_id):
    if task_manager.delete_task(task_id) is False:
        return "<h2> Задача не найдена </h2>", 404
    else:
        return "success", 200


if __name__ == "__main__":
    app.run(port=PORT, debug=DEBUG)
