import sys

import pytermgui as ptg

tasks = []


class MyButton(ptg.Button):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


def get_tasks(manager: ptg.WindowManager) -> list[ptg.Label, ptg.Label]:
    labeled_tasks = []

    for items in tasks:
        for task, task_staus in items.items():
            labeled_tasks.append(
                (
                    ptg.Label(task, parent_align=0, position=1),
                    MyButton("done" if task_staus else "pending", lambda btn: update_tasks(manager, btn) ,id=f"{task}"),
                )
            )

    return labeled_tasks


def parse_task(manager: ptg.WindowManager, modal: ptg.Window) -> str:
    global tasks

    for widget in modal:
        if isinstance(widget, ptg.InputField):
            _task = widget.value
            tasks.append({_task: False})

    show_tasks_and_status(manager)
    modal.close()


def add_tasks(manager: ptg.WindowManager) -> None:
    modal = ptg.Window(
        "Task To Add",
        "",
        ptg.InputField("Eat food...", prompt="Task: ", id="task_enput"),
        "",
        ptg.Container(
            ptg.Splitter(
                ptg.Button("Enter", lambda *_: parse_task(manager, modal)),
                ptg.Button("Close", lambda *_: modal.close()),
            )
        ),
    ).center()
    manager.add(modal)

def update_tasks(manager: ptg.WindowManager, button: ptg.Button) -> None:  
    global tasks

    modal = ptg.Window(
        "Are You Sure You Want To Mark this task as done"
        "",
        ptg.Container(
            ptg.Splitter(
                ptg.Button("Yes", lambda *_: mark_as_done(button.id)),
                ptg.Button("Close", lambda *_: modal.close())
            )
        )
    ).center()

    def mark_as_done(task_name: str) -> None:
        for task in tasks:
            if task_name in task.keys():
                task[task_name] = True
        modal.close()
        show_tasks_and_status(manager)

    manager.add(modal)

def _confirm_quit(manager: ptg.WindowManager) -> None:
    """Creates an "Are you sure you want to quit" modal window"""

    modal = ptg.Window(
        "Are you sure you want to quit?",
        "",
        ptg.Container(
            ptg.Splitter(
                ptg.Button("Yes", lambda *_: manager.stop()),
                ptg.Button("No", lambda *_: modal.close()),
            ),
        ),
    ).center()

    modal.select(1)
    manager.add(modal)


def show_tasks_and_status(manager: ptg.WindowManager) -> None:
    tasks = get_tasks(manager)

    tasks_col = ptg.Window(*[task[0] for task in tasks], id="tasks_col").set_title(
        "Tasks"
    )

    tasks_status_col = ptg.Window(
        *[task[1] for task in tasks], id="tasks_status_col"
    ).set_title("Tasks Status")
    for window in manager._windows:
        if window.id in ["tasks_col", "tasks_status_col"]:
            manager.remove(window)

    manager.add(tasks_status_col, assign="body_right")
    manager.add(tasks_col, assign="body")


def define_layout() -> ptg.Layout:
    layout = ptg.Layout()

    layout.add_slot("Header", height=2)
    layout.add_break()

    layout.add_slot("Body")
    layout.add_slot("Body right", width=0.2)
    layout.add_break()

    layout.add_slot("footer", height=1)

    return layout


def main() -> None:
    with ptg.WindowManager() as manager:
        manager.layout = define_layout()

        header = ptg.Window("TO-DO-APP", box="EMPTY")
        manager.add(header, assign="header")

        show_tasks_and_status(manager)

        footer = ptg.Window(
            ptg.Splitter(
                ptg.Button("Add Task", lambda *_: add_tasks(manager)),
                ptg.Button("Quit", lambda *_: _confirm_quit(manager)),
            ),
            box="EMPTY",
        )
        manager.add(footer, assign="footer")
        manager.run()


if __name__ == "__main__":
    sys.exit(main())
