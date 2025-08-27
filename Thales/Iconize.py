import tkinter as tk
import ctypes
import sys

class Iconize(tk.Frame):
    def __init__(self, master=None, hide_window="inactive", **kwargs):
        super().__init__(master, width=0, height=0, borderwidth=0, highlightthickness=0, **kwargs)
        self.pack_propagate(False)
        self.hide_window = hide_window
        self.after(10, self._apply_behavior)

    def _apply_behavior(self):
        root = self.winfo_toplevel()
        if self.hide_window == "active":
            root.withdraw()  
        if self.hide_window == "inactive":
            root.iconify()   

if __name__ == "__main__":
    root = tk.Tk()
    Iconize(root, hide_window="inactive").pack()
    root.mainloop()
