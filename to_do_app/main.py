from src import dashboard

import pytermgui as ptg
import sys

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

def main():
    with ptg.WindowManager() as manager:
        manager.layout.add_slot("Body")

        view_tasks_btn = ptg.Button(
            " View Tasks ",
            lambda *_: dashboard.dashboard(manager),
            centered=True
        )

        add_tasks_btn = ptg.Button(
            " Add Tasks",
            lambda *_: True
        )

        quit_btn = ptg.Button("Quit", lambda *_: _confirm_quit(manager))

        menu_window = ptg.Window(
            "[210 bold]Menu",
            "",
            view_tasks_btn,
            "",
            add_tasks_btn,
            "",
            quit_btn
        )

        menu_window.select(0)

        manager.add(menu_window)


if __name__ == "__main__":
    sys.exit(main())