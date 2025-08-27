import tkinter as tk
from tkinter import Canvas, Frame


class Slider(Frame):
    def __init__(self, master=None, from_=0, to=100, height=340, command=None, label=""):
        super().__init__(master, relief="raised", bd=3, bg='systembuttonface')
        self.from_ = from_
        self.to = to
        self.height = height
        self.command = command
        self.value = from_
        self.label = label

        self.canvas = Canvas(self, width=70, height=height + 48, bg='SystemButtonFace', highlightthickness=1)
        self.canvas.pack()

        self.knob_y = self.value_to_y(self.value)
        self.knob = None

        self.canvas.bind("<B1-Motion>", self.on_drag)
        self.canvas.bind("<Button-1>", self.on_drag)
        self.draw_slider()

    def draw_slider(self):
        self.canvas.delete("all")
        self.canvas.create_text(35, 10, text=self.label, fill='red', font=('Arial', 10, 'bold'))
        self.canvas.create_line(35, 30, 35, self.height + 30, fill='black', width=5)

        steps = 10
        range_val = self.to - self.from_
        step_val = range_val // steps
        for i in range(steps + 1):
            value = self.from_ + i * step_val
            y = self.value_to_y(value)
            self.canvas.create_line(25, y, 45, y, fill='gray')
            self.canvas.create_text(58, y, text=str(value), fill='black', font=('Arial', 8))

        self.knob_y = self.value_to_y(self.value)
        self.knob = self.canvas.create_rectangle(21, self.knob_y - 3, 50, self.knob_y + 3,
                                         fill='lightgrey', outline='black', width=2)

        self.canvas.create_text(35, self.height + 40, text="Thales", font="Helvetica 7", fill="gray")

    def value_to_y(self, value):
        value = max(min(value, self.to), self.from_)
        ratio = (value - self.from_) / (self.to - self.from_)
        return 30 + (1 - ratio) * self.height

    def y_to_value(self, y):
        y = min(max(y, 30), self.height + 30)
        ratio = (y - 30) / self.height
        return self.from_ + (1 - ratio) * (self.to - self.from_)

    def on_drag(self, event):
        self.knob_y = min(max(event.y, 30), self.height + 30)
        self.canvas.coords(self.knob, 21, self.knob_y - 3, 50, self.knob_y + 3)
        self.value = int(self.y_to_value(self.knob_y))
        if self.command:
            self.command()

    def set_value(self, value):
        self.value = max(min(value, self.to), self.from_)
        self.knob_y = self.value_to_y(self.value)
        self.canvas.coords(self.knob, 21, self.knob_y - 3, 50, self.knob_y + 3)
        if self.command:
            self.command()
    
    def set_command(self, command):
        self.command = command
    
    def return_value(self):
        return self.value

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Meter Panel Clone")
    def print_slider1_value():
        print("Slider 1 Value:", slider1.return_value())

    slider1 = Slider(root, from_=0, to=100, height=300, command=print_slider1_value, label="Sinus")
    slider1.grid(row=0, column=0, padx=10, pady=10)

    slider2 = Slider(root, from_=0, to=100, height=300, label="Cosinus")
    slider2.grid(row=0, column=1, padx=10, pady=10)
    
    
    get_val_butt = tk.Button(root, text = "Value", command=print_slider1_value)
    get_val_butt.grid(row=1, column=1)
    
    root.mainloop()