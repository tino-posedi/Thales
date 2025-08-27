import tkinter as tk
from tkinter import Canvas, Frame
import ast  


class SelectSlide(Frame):
    def __init__(self, master=None, from_=0, to=20, steps=10, base_step_height=30, command=None, labels=None, caption=""):
        super().__init__(master, relief="raised", bd=3, bg='systembuttonface')
        self.from_ = from_
        self.to = to
        self.steps = min(max(steps, 2), 20) 
        self.command = command
        self.caption = caption

        if isinstance(labels, str):
            try:
                parsed_labels = ast.literal_eval(labels)
                if isinstance(parsed_labels, list):
                    labels = parsed_labels
                else:
                    labels = None  
            except Exception:
                labels = None 

        self.step_height = base_step_height
        self.height = (self.steps - 1) * self.step_height

        self.values = [from_ + i * (to - from_) / (self.steps - 1) for i in range(self.steps)]

        if labels and len(labels) == self.steps:
            self.step_labels = labels
        else:
            self.step_labels = [str(round(v)) for v in self.values]

        self.value_index = 0  

        self.canvas = Canvas(self, width=70, height=self.height + 48, bg='SystemButtonFace', highlightthickness=1)
        self.canvas.pack()

        self.knob_y = self.index_to_y(self.value_index)
        self.knob = None

        self.canvas.bind("<B1-Motion>", self.on_drag)
        self.canvas.bind("<Button-1>", self.on_drag)
        self.draw_slider()

    def draw_slider(self):
        self.canvas.delete("all")
        self.canvas.create_text(35, 10, text=self.caption, fill='red', font=('Arial', 10, 'bold'))
        self.canvas.create_line(35, 30, 35, self.height + 30, fill='black', width=5)

        for i in range(self.steps):
            y = self.index_to_y(i)
            self.canvas.create_line(25, y, 45, y, fill='gray')
            self.canvas.create_text(58, y, text=self.step_labels[i], fill='black', font=('Arial', 8))

        self.knob_y = self.index_to_y(self.value_index)
        self.knob = self.canvas.create_rectangle(21, self.knob_y - 3, 50, self.knob_y + 3,
                                                 fill='lightgrey', outline='black', width=2)

        self.canvas.create_text(35, self.height + 40, text="Thales", font="Helvetica 7", fill="gray")

    def index_to_y(self, index):
        return 30 + index * self.step_height

    def y_to_index(self, y):
        y = min(max(y, 30), 30 + self.height)
        relative_y = y - 30
        index = round(relative_y / self.step_height)
        return min(max(index, 0), self.steps - 1)

    def on_drag(self, event):
        index = self.y_to_index(event.y)
        if index != self.value_index:
            self.value_index = index
            self.knob_y = self.index_to_y(index)
            self.canvas.coords(self.knob, 21, self.knob_y - 3, 50, self.knob_y + 3)
            if self.command:
                self.command()

    def set_value(self, value):
        closest_index = min(range(self.steps), key=lambda i: abs(self.values[i] - value))
        self.value_index = closest_index
        self.knob_y = self.index_to_y(self.value_index)
        self.canvas.coords(self.knob, 21, self.knob_y - 3, 50, self.knob_y + 3)
        if self.command:
            self.command()

    def return_value(self):
        return self.values[self.value_index]

if __name__ == "__main__":
    root = tk.Tk()
    root.title("SelectSlide Demo")

    labels_str = '["One", "Two", "Three", "Four", "Five", "Six", "Seven", "Eight", "Nine"]'

    def print_state():
        print("Slider state: ", slider.return_value())

    slider = SelectSlide(root, from_=1, to=9, steps=9, labels=labels_str, caption="Numbers", command=print_state)
    slider.grid(row=0, column=0, padx=10, pady=10)

    tk.Button(root, text="Get Current Value", command=lambda: print("Manual check:", slider.return_value())).grid(row=1, column=0, pady=5)

    root.mainloop()
