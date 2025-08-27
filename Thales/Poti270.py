import tkinter as tk
import math

SCALE = 0.7
WIDTH, HEIGHT = int(330 * SCALE), int(360 * SCALE)
CENTER_X, CENTER_Y = WIDTH // 2.06, int(170 * SCALE)
RADIUS = int(100 * SCALE)

class Poti270(tk.Frame):
    def __init__(self, parent, start_value=0.0, end_value=10.0, outer_knob_fill="#b0f0f0", inner_knob_fill="#00bfbf", needle_fill="red", **kwargs):
        super().__init__(parent, width=WIDTH, height=226, **kwargs, relief="raised", bd=3)
        self.start_value = start_value
        self.end_value = end_value
        self.range = self.end_value - self.start_value
        self.value = self.start_value
        self.dragging = False
        
        self.outer_knob_fill = outer_knob_fill
        self.inner_knob_fill = inner_knob_fill
        self.needle_fill = needle_fill

        self.canvas = tk.Canvas(self, width=221, height=216, bg="SystemButtonFace", highlightthickness=0)
        self.canvas.place(x=0, y=0)

        self.canvas.bind("<Button-1>", self.on_click)
        self.canvas.bind("<B1-Motion>", self.on_drag)
        self.canvas.bind("<ButtonRelease-1>", self.on_release)

        self.update_display()

    def draw_ticks_and_arc(self):
        arc_radius = RADIUS + 11
        self.canvas.create_arc(CENTER_X - arc_radius, CENTER_Y - arc_radius,
                               CENTER_X + arc_radius, CENTER_Y + arc_radius,
                               start=315, extent=270, style="arc", outline="gray", width=2)

        num_ticks = 11
        for i in range(num_ticks):
            value = self.start_value + (self.range / (num_ticks - 1)) * i
            angle = 135 + (270 / (num_ticks - 1)) * i
            rad = math.radians(angle)

            outer = RADIUS + 18
            inner = outer - 8
            x1 = CENTER_X + outer * math.cos(rad)
            y1 = CENTER_Y + outer * math.sin(rad)
            x2 = CENTER_X + inner * math.cos(rad)
            y2 = CENTER_Y + inner * math.sin(rad)
            self.canvas.create_line(x1, y1, x2, y2, fill="black")

            lx = CENTER_X + (outer + 11) * math.cos(rad)
            ly = CENTER_Y + (outer + 11) * math.sin(rad)
            self.canvas.create_text(lx, ly, text=str(round(value, 1)), font=("Arial", int(11 * SCALE)))

    def draw_knob(self):
        self.canvas.create_oval(CENTER_X - RADIUS, CENTER_Y - RADIUS,
                                CENTER_X + RADIUS, CENTER_Y + RADIUS,
                                fill=self.outer_knob_fill, outline='black') # default #b0f0f0

        inner_offset = int(30 * SCALE)
        self.canvas.create_oval(CENTER_X - RADIUS + inner_offset, CENTER_Y - RADIUS + inner_offset,
                                CENTER_X + RADIUS - inner_offset, CENTER_Y + RADIUS - inner_offset,
                                fill=self.inner_knob_fill, outline='black') # default #00bfbf

        relative = (self.value - self.start_value) / self.range
        angle = 135 + (relative * 270)
        angle_rad = math.radians(angle)
        length = RADIUS - 5

        shadow_offset = 1.5
        end_x = CENTER_X + length * math.cos(angle_rad)
        end_y = CENTER_Y + length * math.sin(angle_rad)
        self.canvas.create_line(CENTER_X + shadow_offset, CENTER_Y + shadow_offset,
                                end_x + shadow_offset, end_y + shadow_offset,
                                fill='#550000', width=3)

        self.canvas.create_line(CENTER_X, CENTER_Y, end_x, end_y, fill=self.needle_fill, width=2)
        self.canvas.create_text(207, 213, text = "Thales", font = "Helvetica 7", fill = "gray")

    def update_display(self):
        self.canvas.delete("all")
        self.draw_ticks_and_arc()
        self.draw_knob()

    def on_click(self, event):
        self.dragging = True
        self.set_value_from_mouse(event.x, event.y)

    def on_drag(self, event):
        if self.dragging:
            self.set_value_from_mouse(event.x, event.y)

    def on_release(self, event):
        self.dragging = False

    def set_value_from_mouse(self, x, y):
        dx, dy = x - CENTER_X, y - CENTER_Y
        angle = (math.degrees(math.atan2(dy, dx)) + 360) % 360

        if angle < 135 and angle > 45:
            return  # Out of range
        if angle < 135:
            angle += 360
        angle = max(135, min(angle, 405))

        relative = (angle - 135) / 270
        self.value = round(self.start_value + relative * self.range, 2)
        self.update_display()

    def return_value(self):
        return round(self.value, 2)