import pytermgui as ptg


def dashboard_layout() -> ptg.Layout:
    layout = ptg.Layout("dashboard-layout")

    layout.add_slot("Body")
    layout.add_slot("Task status", width=0.2)

    return layout


def dashboard(manager: ptg.WindowManager) -> None:
    tasks_data = [{"do this": False}, {"do that": True}, {"do anything": False}]

    tasks = ""
    tasks_status = ""

    for task_item in tasks_data:
        for key, value in task_item.items():
            tasks += f"{key}\n"
            tasks_status += f"{value}\n"

    manager.layout = dashboard_layout()

    task_status_col = ptg.Window(f"{tasks_status}", is_persistant=True).set_title(
        "Task Status"
    )

    manager.add(task_status_col, assign="task_status")

    tasks_col = ptg.Window(f"{tasks}", is_persistant=True).set_title("Tasks")
    manager.add(tasks_col, assign="body")