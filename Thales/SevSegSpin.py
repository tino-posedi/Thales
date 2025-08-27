import tkinter as tk
from tkinter import font
import os

class RoundedDigitCanvas(tk.Canvas):
    def __init__(self, parent, font_path=None):
        self.canvas_width = 80
        self.canvas_height = 100
        super().__init__(parent, width=self.canvas_width, height=self.canvas_height, bg='SystemButtonFace', highlightthickness=0)

        self.digit = ''
        self.font_path = "DSEG7Classic-Regular.ttf"
        self.font = self.load_dseg_font(font_path, 48)

        self.rect_margin = 5
        self.radius = 20

        self.draw_background()

        center_x = self.canvas_width // 2
        center_y = self.canvas_height // 2
        self.digit_id = self.create_text(center_x, center_y, text=self.digit, font=("DSEG7 Classic", 48, "bold"), fill='#ffff00', anchor='center')

    def draw_background(self):
        x1 = self.rect_margin
        y1 = self.rect_margin
        x2 = self.canvas_width - self.rect_margin
        y2 = self.canvas_height - self.rect_margin
        self.create_round_rect(x1, y1, x2, y2, radius=self.radius, fill='#0000ff', outline='')

    def create_round_rect(self, x1, y1, x2, y2, radius=20, **kwargs):
        """Draw a smooth rounded rectangle using a polygon."""
        points = [
            x1 + radius, y1,
            x2 - radius, y1,
            x2, y1,
            x2, y1 + radius,
            x2, y2 - radius,
            x2, y2,
            x2 - radius, y2,
            x1 + radius, y2,
            x1, y2,
            x1, y2 - radius,
            x1, y1 + radius,
            x1, y1,
        ]
        self.create_polygon(points, smooth=True, splinesteps=36, **kwargs)

    def load_dseg_font(self, font_path, size):
        if font_path and os.path.exists(font_path):
            return font.Font(file=font_path, size=size)
        else:
            return font.Font(family="DSEG7 Classic", size=size)

    def update_digit(self, value):
        self.digit = str(value)
        self.itemconfig(self.digit_id, text=self.digit)


class SevSegSpin(tk.Frame):
    def __init__(self, parent, wrap="inactive", start_value=1, end_value=9, font_path=None):
        super().__init__(parent, bg='SystemButtonFace', bd=3, relief='raised', padx=5, pady=5)

        self.wrap = wrap
        self.min_value = start_value
        self.max_value = end_value
        self.value = start_value

        self.up_btn = tk.Button(self, text='▲', command=self.increment)
        self.up_btn.pack(side='top', fill='x')

        self.display = RoundedDigitCanvas(self, font_path=font_path)
        self.display.pack()
        self.display.update_digit(self.value)

        self.down_btn = tk.Button(self, text='▼', command=self.decrement)
        self.down_btn.pack(side='bottom', fill='x')

    def increment(self):
        if self.value < self.max_value:
            self.value += 1
        elif self.wrap == "active":
            self.value = self.min_value
        self.display.update_digit(self.value)

    def decrement(self):
        if self.value > self.min_value:
            self.value -= 1
        elif self.wrap == "active":
            self.value = self.max_value
        self.display.update_digit(self.value)
    
    def return_value(self):
        return self.value

if __name__ == '__main__':
    root = tk.Tk()
    root.title("Rounded 7-Segment Counter")
    
    def print_state():
        print("Current step: ", counter.return_value())

    counter = SevSegSpin(root, wrap="inactive", start_value=1, end_value=9)
    counter.pack(padx=20, pady=20)
    
    print_state()
    root.mainloop()
