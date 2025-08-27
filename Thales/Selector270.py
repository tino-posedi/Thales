import tkinter as tk
import math

SCALE = 0.7
WIDTH, HEIGHT = int(330 * SCALE), int(360 * SCALE)
CENTER_X, CENTER_Y = WIDTH // 2.06, int(170 * SCALE)
RADIUS = int(100 * SCALE)

class Selector270(tk.Frame):
    def __init__(self, parent, steps=5, **kwargs):
        super().__init__(parent, width=WIDTH, height=226, **kwargs, relief="raised", bd=3)
        self.steps = steps
        self.current_step = 0
        self.dragging = False

        self.canvas = tk.Canvas(self, width=221, height=216, bg="SystemButtonFace", highlightthickness=0)
        self.canvas.place(x=0, y=0)

        self.canvas.bind("<Button-1>", self.on_click)
        self.canvas.bind("<B1-Motion>", self.on_drag)
        self.canvas.bind("<ButtonRelease-1>", self.on_release)

        self.update_display()

    def draw_leds(self):
        led_radius = 4
        distance = RADIUS + 13
        angle_step = 270 / (self.steps - 1)

        for i in range(self.steps):
            angle = 135 + i * angle_step
            rad = math.radians(angle)
            x = CENTER_X + distance * math.cos(rad)
            y = CENTER_Y + distance * math.sin(rad)

            on = i == self.current_step
            color = '#FF0000' if on else '#8B0000'
            self.canvas.create_oval(x - led_radius, y - led_radius,
                                    x + led_radius, y + led_radius,
                                    fill=color, outline='black')

            label_x = CENTER_X + (distance + 20) * math.cos(rad)
            label_y = CENTER_Y + (distance + 20) * math.sin(rad)
            self.canvas.create_text(label_x, label_y, text=str(i + 1), fill="black", font=("Arial", int(16 * SCALE), "bold"))

    def draw_knob(self):
        self.canvas.create_oval(CENTER_X - RADIUS, CENTER_Y - RADIUS,
                                CENTER_X + RADIUS, CENTER_Y + RADIUS,
                                fill='#b0f0f0', outline='black')

        inner_offset = int(30 * SCALE)
        self.canvas.create_oval(CENTER_X - RADIUS + inner_offset, CENTER_Y - RADIUS + inner_offset,
                                CENTER_X + RADIUS - inner_offset, CENTER_Y + RADIUS - inner_offset,
                                fill='#00bfbf', outline='black')


        angle = 135 + (270 / (self.steps - 1)) * self.current_step
        angle_rad = math.radians(angle)
        length = RADIUS - 5

        shadow_offset = 1.5
        end_x = CENTER_X + length * math.cos(angle_rad)
        end_y = CENTER_Y + length * math.sin(angle_rad)
        shadow_x = CENTER_X + shadow_offset
        shadow_y = CENTER_Y + shadow_offset
        shadow_end_x = end_x + shadow_offset
        shadow_end_y = end_y + shadow_offset
        self.canvas.create_line(shadow_x, shadow_y, shadow_end_x, shadow_end_y, fill='#550000', width=3)

        self.canvas.create_line(CENTER_X, CENTER_Y, end_x, end_y, fill='red', width=2)
        
        self.canvas.create_text(207, 213, text = "Thales", font = "Helvetica 7", fill = "gray")

    def polar_to_cartesian(self, radius, angle_rad):
        x = CENTER_X + radius * math.cos(angle_rad)
        y = CENTER_Y + radius * math.sin(angle_rad)
        return x, y

    def update_display(self):
        self.canvas.delete("all")
        self.draw_leds()
        self.draw_knob()

    def on_click(self, event):
        self.dragging = True
        self.set_step_from_mouse(event.x, event.y)

    def return_value(self):
        return self.current_step + 1   

    def on_drag(self, event):
        if self.dragging:
            self.set_step_from_mouse(event.x, event.y)

    def on_release(self, event):
        self.dragging = False

    def set_step_from_mouse(self, x, y):
        dx, dy = x - CENTER_X, y - CENTER_Y
        angle = (math.degrees(math.atan2(dy, dx)) + 360) % 360

        if angle < 135 and angle > 45:
            return 

        if angle < 135:
            angle += 360

        angle = max(135, min(angle, 405))
        relative = (angle - 135) / 270
        new_step = int(round(relative * (self.steps - 1)))
        if new_step != self.current_step:
            self.current_step = new_step
            self.update_display()

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Rotary Switch - Drag and Snap")
    switch = Selector270(root, steps=5)
    switch.pack(padx=10, pady=10)

    def show_value():
        print("Selected step:", switch.return_value())

    btn = tk.Button(root, text="Fetch Value", command=show_value)
    btn.pack(pady=5)

    root.mainloop()