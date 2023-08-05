import tkinter as tk


def tcl_center_window(window: tk.Tk | tk.Toplevel) -> None:
    """Centers a window on desktop. `Returns None`"""
    window.eval("tk::PlaceWindow . center")


def tcl_bell(window: tk.Tk | tk.Toplevel) -> None:
    """Plays system bell sound. `Returns None`"""
    window.eval("bell")


def tcl_choose_font(window: tk.Tk | tk.Toplevel) -> tuple | None:
    """Select a font using system font dialog. `Returns a tuple or None if no selection was made`"""

    selection_holder = []

    def callback(sel):
        sel = sel.strip()
        font = sel[sel.index("{") + 2 : sel.index("}")]
        size = int(sel[sel.index("}") + 1 :].strip())
        selection_holder.append((font, size))

    cmd_tag = window.register(callback)
    window.eval(f"tk::fontchooser configure -command {cmd_tag}")
    window.eval(f"tk::fontchooser show")

    if len(selection_holder):
        return selection_holder[0]
