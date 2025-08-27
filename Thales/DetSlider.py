import tkinter as tk

class DetSlider(tk.Canvas):
    def __init__(self, master, orientation="horizontal", min_val=0, max_val=100, step=None,
                 initial=None, size="medium", width=None, height=None,
                 bg_color="systemButtonFace", trench_color="#808080", knob_color="#f0f0f0",
                 border_color="#666666", bevel=True, tick_color="#0000ff", command=None, **kwargs):

        def normalize(val, default=None, is_step=False):
            if val in (None, "None", ""):
                return default
            try:
                return float(val) if is_step or "." in str(val) else int(val)
            except ValueError:
                return default

        self.min_val = normalize(min_val, 0)
        self.max_val = normalize(max_val, 100)
        self.step = normalize(step, None, is_step=True)
        self.value = normalize(initial, self.min_val)
        self.command = command 
        self.orientation = orientation

        sizes = {
            "small": (150, 20),
            "medium": (250, 30),
            "big": (350, 40)
        }

        if orientation == "vertical":
            sizes = {k: (h, w) for k, (w, h) in sizes.items()}

        width, height = width or sizes[size][0], height or sizes[size][1]
        super().__init__(master, width=width, height=height, bg=bg_color,
                         highlightthickness=0, bd=3, relief="raised", **kwargs)

        self.trench_color = trench_color
        self.knob_color = knob_color
        self.border_color = border_color
        self.bevel = bevel
        self.tick_color = tick_color

        self.knob_length = 18
        self.knob_thickness = 7
        self.trench_thickness = 4
        self.trench_offset = 0

        self.dragging = False

        self.bind("<Button-1>", self.on_click)
        self.bind("<B1-Motion>", self.on_drag)
        self.bind("<ButtonRelease-1>", self.on_release)

        self.after(15, self.draw_slider)

    def draw_slider(self):
        self.delete("all")
        w, h = self.winfo_width(), self.winfo_height()

        if self.orientation == "horizontal":
            trench_y = h // 2 + self.trench_offset
            y = trench_y

            self.create_rectangle(10, trench_y - self.trench_thickness // 2,
                                  w - 10, trench_y + self.trench_thickness // 2,
                                  fill=self.trench_color, outline="")

            pos = self.value_to_pixel(self.value)
            knob_coords = (pos - self.knob_length // 2, y - self.knob_thickness // 2,
                           pos + self.knob_length // 2, y + self.knob_thickness // 2)

            if self.step:
                num_steps = int((self.max_val - self.min_val) / self.step) + 1
                tick_y_top = trench_y - self.trench_thickness // 2 - 6
                tick_y_bot = trench_y + self.trench_thickness // 2 + 6
                for i in range(num_steps):
                    val = self.min_val + i * self.step
                    x = self.value_to_pixel(val)
                    self.create_line(x, tick_y_top, x, tick_y_top + 4, fill=self.tick_color)
                    self.create_line(x, tick_y_bot - 4, x, tick_y_bot, fill=self.tick_color)

        else:
            trench_x = w // 2 + self.trench_offset
            x = trench_x

            self.create_rectangle(trench_x - self.trench_thickness // 2, 10,
                                  trench_x + self.trench_thickness // 2, h - 10,
                                  fill=self.trench_color, outline="")

            pos = self.value_to_pixel(self.value)
            knob_coords = (x - self.knob_thickness // 2, pos - self.knob_length // 2,
                           x + self.knob_thickness // 2, pos + self.knob_length // 2)

            if self.step:
                num_steps = int((self.max_val - self.min_val) / self.step) + 1
                tick_x_left = trench_x - self.trench_thickness // 2 - 6
                tick_x_right = trench_x + self.trench_thickness // 2 + 6
                for i in range(num_steps):
                    val = self.min_val + i * self.step
                    y = self.value_to_pixel(val)
                    self.create_line(tick_x_left, y, tick_x_left + 4, y, fill=self.tick_color)
                    self.create_line(tick_x_right - 4, y, tick_x_right, y, fill=self.tick_color)

        if self.bevel:
            x0, y0, x1, y1 = knob_coords
            self.create_rectangle(x0, y0, x1, y1, fill=self.knob_color, outline=self.border_color)
            self.create_line(x0, y1, x0, y0, x1, y0, fill="white")
            self.create_line(x1, y0, x1, y1, x0, y1, fill="#444444")
        else:
            self.create_rectangle(*knob_coords, fill=self.knob_color, outline=self.border_color)

    def value_to_pixel(self, value):
        w, h = self.winfo_width(), self.winfo_height()
        val_range = self.max_val - self.min_val
        rel = (value - self.min_val) / val_range
        if self.orientation == "horizontal":
            return int(10 + rel * (w - 20))
        else:
            return int(h - 10 - rel * (h - 20))

    def pixel_to_value(self, pixel):
        w, h = self.winfo_width(), self.winfo_height()
        if self.orientation == "horizontal":
            rel = min(max((pixel - 10) / (w - 20), 0), 1)
        else:
            rel = min(max((h - 10 - pixel) / (h - 20), 0), 1)
        val = self.min_val + rel * (self.max_val - self.min_val)
        if self.step:
            steps = round((val - self.min_val) / self.step)
            val = self.min_val + steps * self.step
        return val

    def on_click(self, event):
        self.dragging = True
        self.update_value_from_event(event)

    def on_drag(self, event):
        if self.dragging:
            self.update_value_from_event(event)

    def on_release(self, event):
        self.dragging = False

    def update_value_from_event(self, event):
        pos = event.x if self.orientation == "horizontal" else event.y
        self.value = self.pixel_to_value(pos)
        self.draw_slider()
        if callable(self.command):   
            self.command(self.return_value())

    def return_value(self):
        return self.value

    def set_value(self, val):
        self.value = max(min(val, self.max_val), self.min_val)
        self.draw_slider()
        if callable(self.command):
            self.command(self.return_value())  

    def set_command(self, cmd):
        self.command = cmd

if __name__ == '__main__':
    def show_val(val):
        print("Slider value:", val)

    root = tk.Tk()
    root.title("DetSlider Test")

    slider = DetSlider(root, orientation="horizontal", min_val=0, max_val=10, step=1,
                       size="medium", command=show_val)
    slider.pack(padx=20, pady=20)

    vslider = DetSlider(root, orientation="vertical", min_val=0, max_val=5, step=0.5,
                        size="small", knob_color="orange", trench_color="lightgray", command=show_val)
    vslider.pack(padx=20, pady=20, side="left")

    root.mainloop()
