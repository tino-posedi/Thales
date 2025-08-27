import tkinter as tk

class VersInfo(tk.Frame):
    def __init__(self, master=None, version="1.0.0", company="", author="", **kwargs):
        super().__init__(master, width=0, height=0, borderwidth=0, highlightthickness=0, **kwargs)
        self.pack_propagate(False)

        self.version = version
        self.company = company
        self.author = author

        self.root = self.winfo_toplevel()
        self.apply_title()

    def apply_title(self):
        parts = []
        if self.version:
            parts.append(self.version)
        if self.company:
            parts.append(self.company)
        if self.author:
            parts.append(self.author)

        title_info = " | ".join(parts)
        if title_info:
            base_title = self.root.title() or "Application"
            self.root.title(f"{base_title} - {title_info}")

    def set_version(self, version):
        self.version = version
        self.apply_title()

    def set_company(self, company):
        self.company = company
        self.apply_title()

    def set_author(self, author):
        self.author = author
        self.apply_title()

    def get_info(self):
        return self.version, self.company, self.author

def main():
    root = tk.Tk()
    root.title("My Application")

    ver = VersInfo(
        root,
        version="2.1.2",
        company="Test Company",
        author="Test Name"
    )

    btn = tk.Button(root, text="Quit", command=root.destroy)
    btn.pack(pady=20)

    root.mainloop()

if __name__ == "__main__":
    main()