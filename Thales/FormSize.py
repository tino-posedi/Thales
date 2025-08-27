import tkinter as tk

class FormSize(tk.Frame):
    def __init__(self, master=None, w=800, h=600, **kwargs):
        super().__init__(master, width=0, height=0, borderwidth=0, highlightthickness=0, **kwargs)
        self.pack_propagate(False) 

        self.width = w
        self.height = h

        self.root = self.winfo_toplevel()

        self.root.geometry(f"{self.width}x{self.height}")

    def set_size(self, w, h):
        self.width = w
        self.height = h
        self.root.geometry(f"{self.width}x{self.height}")

    def get_size(self):
        return self.width, self.height
