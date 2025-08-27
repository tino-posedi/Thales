import tkinter as tk

class StrEdit(tk.Frame):
    def __init__(self, parent, text="", fill="white", number_fill="black",
                 width=200, height=35, orientation="right", **kwargs):
        super().__init__(parent, bd=3, relief="raised", **kwargs)

        self.width = width
        self.height = height

        anchor_map = {"left": "w", "center": "center", "right": "e"}
        self.anchor = anchor_map.get(orientation, "e")  

        self.config(width=self.width, height=self.height)
        self.pack_propagate(False)

        self.label = tk.Label(
            self,
            text=text,
            bg=fill,
            fg=number_fill,
            font=("Arial", 32, "bold"),
            anchor=self.anchor,
            bd=1,
            relief="solid"
        )
        self.label.pack(fill="both", expand=True, padx=3, pady=3)

        self._adjust_font_size(text)

    def set_text(self, text):
        self.label.config(text=text)
        self._adjust_font_size(text)

    def _adjust_font_size(self, text):
        max_width = self.width * 0.9
        max_height = self.height * 0.8

        font_size = 1
        temp = tk.Label(self, text=text, font=("Arial", font_size, "bold"))
        temp.update_idletasks()
        while True:
            temp.config(font=("Arial", font_size, "bold"))
            temp.update_idletasks()
            if temp.winfo_reqwidth() > max_width or temp.winfo_reqheight() > max_height:
                font_size -= 1
                break
            font_size += 1
        temp.destroy()
        self.label.config(font=("Arial", font_size, "bold"))

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Digital Display Test")

    display_left = StrEdit(root, text="Left", fill="navy", number_fill="yellow",
                                  width=200, height=50, orientation="left")
    display_left.pack(padx=20, pady=10)

    display_center = StrEdit(root, text="Center", fill="navy", number_fill="yellow",
                                    width=200, height=50, orientation="center")
    display_center.pack(padx=20, pady=10)

    display_right = StrEdit(root, text="Right", fill="navy", number_fill="yellow",
                                    width=200, height=50, orientation="right")
    display_right.pack(padx=20, pady=10)

    root.mainloop()
