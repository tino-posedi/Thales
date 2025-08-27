import tkinter as tk

class Bevel3D(tk.Frame):
    def __init__(self, master=None, width=100, height=100, relief_style="raised", **kwargs):
        super().__init__(master, bd=3, relief=relief_style, **kwargs)

        self._label_height = 15  
        self.relief_style = relief_style

        if width is not None:
            self.config(width=width)
        if height is not None:
            self.config(height=height)

        self.pack_propagate(False) 

        self.content = tk.Frame(self)
        self.content.pack(fill='both', expand=True, padx=2, pady=(2, self._label_height + 2))

        self.label = tk.Label(self, text="Thales", fg="gray", font=("Arial", 7))
        self.label.place(relx=1.0, rely=1.0, anchor='se', x=0, y=0)

    def add_widget(self, widget, **grid_options):
        widget.grid(**grid_options)

if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("320x240")
    root.title("RaisedFrame with Fixed Size")

    frame = Bevel3D(root, width=280, height=150, relief_style= "sunken")
    frame.pack(padx=10, pady=10)

    btn = tk.Button(frame.content, text="Click Me")
    entry = tk.Entry(frame.content)

    btn.grid(row=0, column=0, padx=10, pady=10, sticky='nw')
    entry.grid(row=1, column=0, padx=10, pady=10, sticky='nw')

    root.mainloop()
