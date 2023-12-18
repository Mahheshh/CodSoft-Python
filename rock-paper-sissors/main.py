import sys

import pytermgui as ptg


def close_modal(manager: ptg.WindowManager, modal: ptg.Window) -> None:
    for window in manager._windows:
        if modal not in window:
            continue
        for widget in window._widgets:
            if widget.id == modal.id:
                window.remove(modal)


def attach_new_modal(window: ptg.Window, modal: ptg.Window) -> None:
    window._add_widget(modal)


def play_again_callback(manager: ptg.WindowManager, modal: ptg.Container) -> None:
    close_modal(manager, modal)


def game_callback(button: ptg.Button, manager: ptg.WindowManager) -> None:
    modal = ptg.Container(
        f"You have selected {button.label}",
        ptg.Button("Play Again", lambda *_: play_again_callback(manager, modal)),
    ).center()

    for window in manager._windows:
        if window.id == "game_window":
            for widget in window._widgets:
                if widget.id == "game_window_container":
                    window.remove(widget)
            window._add_widget(modal)


def define_layout() -> ptg.Layout:
    layout = ptg.Layout()

    layout.add_slot("header", height=1)
    layout.add_break()

    layout.add_slot("body")
    layout.add_break()

    layout.add_slot("footer", height=1)

    return layout


def main():
    with ptg.WindowManager() as manager:
        manager.layout = define_layout()

        header = ptg.Window("Rock-Paper-Scissors", box="EMPTY")
        manager.add(header, assign="header")

        game_buttons = ptg.Container(
            ptg.Splitter(
                ptg.Button("🗻", lambda button: game_callback(button, manager)),
                ptg.Button("📃", lambda button: game_callback(button, manager)),
                ptg.Button("✂", lambda button: game_callback(button, manager)),
            ),
            id="game_window_container",
        )

        game_window = ptg.Window(game_buttons, id="game_window")
        manager.add(game_window, assign="body")

        footer_buttons = ptg.Splitter(
            ptg.Button("Play Again", lambda *_: True),
            ptg.Button("Quit", lambda *_: manager.stop()),
        )
        footer = ptg.Window(footer_buttons, box="EMPTY")
        manager.add(footer, assign="footer")

        manager.run()


if __name__ == "__main__":
    sys.exit(main())