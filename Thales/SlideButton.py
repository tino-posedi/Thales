import tkinter as tk

class SlideButton(tk.Frame):
    def __init__(self, master=None, size="small", cap_top = "", cap_down = "", fill_top="maroon", fill_down="green", **kwargs):
        size_map = {
            "small": (45, 80, 10),   
            "medium": (60, 100, 12),
            "large": (100, 160, 14)
        }

        if size not in size_map:
            raise ValueError("Invalid size. Use 'small', 'medium', or 'large'.")

        self.width, self.height, self.font_size = size_map[size]
        super().__init__(master, bd=3, relief="raised", width=self.width, height=self.height, **kwargs)

        self.state = False 

        self.canvas = tk.Canvas(self, width=self.width, height=self.height, highlightthickness=0)
        self.canvas.pack()
        self.cap_top = cap_top
        self.cap_down = cap_down
        self.fill_top = fill_top
        self.fill_down = fill_down

        padding = 5
        self.slider_height = (self.height - 2 * padding) // 2

        self.bg_rect = self.canvas.create_rectangle(padding, padding, self.width - padding, self.height - padding,
                                                    fill="maroon", outline="gray")

        self.text = self.canvas.create_text(
            self.width // 2,
            self.slider_height // 2 + padding,
            text=self.cap_top,
            fill="white",
            font=("Arial", self.font_size, "bold")
        )

        self.slider = self.canvas.create_rectangle(
            padding, self.slider_height + padding,
            self.width - padding, self.height - padding,
            fill="darkgrey", outline="gray"
        )

        groove_y = ((self.slider_height + self.height - padding // 2)) + 15 
        self.groove = self.canvas.create_line(
            padding + 5, groove_y, self.width - padding - 5, groove_y,
            fill="grey", width=3
        )

        self.canvas.bind("<Button-1>", self.toggle)

        self.update_view()

    def toggle(self, event=None):
        self.state = not self.state
        self.update_view()

    def update_view(self):
        padding = 5
        if self.state:  
            self.canvas.itemconfig(self.bg_rect, fill=self.fill_top)
            self.canvas.itemconfig(self.text, text=self.cap_top, fill="white")
            self.canvas.coords(self.text, self.width // 2, self.slider_height // 2 + padding)
            self.canvas.coords(self.slider,
                               padding, self.slider_height + padding,
                               self.width - padding, self.height - padding)
            groove_y = (self.slider_height + self.height - padding) // 2
            self.canvas.coords(self.groove,
                               padding + 5, groove_y,
                               self.width - padding - 5, groove_y)
        else: 
            self.canvas.itemconfig(self.bg_rect, fill=self.fill_down)
            self.canvas.itemconfig(self.text, text=self.cap_down, fill="white")
            self.canvas.coords(self.text, self.width // 2, self.height - self.slider_height // 2 - padding)
            self.canvas.coords(self.slider,
                               padding, padding,
                               self.width - padding, self.slider_height + padding)
            groove_y = (padding + self.slider_height) // 2
            self.canvas.coords(self.groove,
                               padding + 5, groove_y,
                               self.width - padding - 5, groove_y)

    def return_value(self):
        return True if self.state else False

if __name__ == "__main__":
    def print_state():
        print("Button State:", btn.return_value())

    root = tk.Tk()
    root.title("Slider Switch with Size Options")

    btn = SlideButton(root, size="small", cap_top="ON", cap_down="OFF", fill_top="gold", fill_down="blue")
    btn.pack(padx=20, pady=20)

    tk.Button(root, text="Check State", command=print_state).pack()

    root.mainloop()
