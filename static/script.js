async function deleteTask(id) {
    const response = await fetch(`/todos/${id}/delete`, {
        method: "DELETE"
    });

    if (response.ok) {
        location.reload();
    } else {
        alert("Не удалось удалить задачу");
    }
}