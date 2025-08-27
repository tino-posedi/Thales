import tkinter as tk

class RollBar(tk.Frame):
    def __init__(self, master=None, title="Panel", width=300, height=150, header_fill="darkgray", **kwargs):
        super().__init__(master, width=width, height=height, **kwargs)
        self.master = master
        self.width = width
        self.height = height
        self.expanded = True
        self.header_fill = header_fill

        self.pack_propagate(False)

        self.header = tk.Frame(self, bg=self.header_fill, relief=tk.FLAT)
        self.header.pack(fill=tk.X)

        self.arrow_btn = tk.Button(self.header, text="▼", width=2, command=self.toggle)
        self.arrow_btn.pack(side=tk.LEFT, padx=2, pady=2)

        self.title_lbl = tk.Label(self.header, text=title, bg=self.header_fill)
        self.title_lbl.pack(side=tk.LEFT, padx=5)

        self.content = tk.Frame(self, bg="SystemButtonFace", relief=tk.RAISED, bd=3)
        self.content.pack(fill=tk.BOTH, expand=True)

    def toggle(self):
        if self.expanded:
            self.content.forget()
            self.arrow_btn.config(text="▲")
        else:
            self.content.pack(fill=tk.BOTH, expand=True)
            self.arrow_btn.config(text="▼")
        self.expanded = not self.expanded

    def add_widget(self, widget, **pack_options):
        widget.pack(in_=self.content, **pack_options)

if __name__ == "__main__":
    root = tk.Tk()
    root.title("RollBar Panel Demo")
    root.geometry("400x400")

    panel1 = RollBar(root, title="Panel 1", width=380, height=190, header_fill="lightblue")
    panel1.pack(padx=10, pady=10)
    panel1.add_widget(tk.Label(panel1.content, text="Content of Panel 1"))
    panel1.add_widget(tk.Button(panel1.content, text="Button 1"))


    root.mainloop()
