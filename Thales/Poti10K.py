from tkinter import *
import math
from tkinter import font as tkfont

SCALE = 0.7
WIDTH, HEIGHT = int(330 * SCALE), int(360 * SCALE)
CENTER_X, CENTER_Y = WIDTH // 2, int(155 * SCALE)
RADIUS = int(100 * SCALE)

class Poti10K(Frame):
    def __init__(self, parent, fill_outer_knob="#b0f0f0", fill_inner_knob="#00bfbf",
                 preset="inactive", start_value=0.0, end_value=10.0, **kwargs):
        super().__init__(parent, width=WIDTH, height=226, **kwargs, relief="raised", bd=3)

        self.fill_outer_knob = fill_outer_knob
        self.fill_inner_knob = fill_inner_knob
        self.preset_mode = preset

        self.start_value = start_value
        self.end_value = end_value
        self.value_range = self.end_value - self.start_value

        self.value = self.start_value
        self.angle = 135
        self.fine_angle = 135
        self.dragging_triangle = False
        self.dragging_circle = False

        self.led_g_state = 'off'
        self.led_r_state = 'off'
        self.blink_state = True

        self.canvas = Canvas(self, width=221, height=216, bg="SystemButtonFace")
        self.canvas.place(x=0, y=0)

        self.canvas.bind("<ButtonPress-1>", self.start_drag_triangle)
        self.canvas.bind("<ButtonRelease-1>", self.stop_drag)
        self.canvas.bind("<B1-Motion>", self.drag_main)

        self.canvas.bind("<ButtonPress-3>", self.start_drag_circle)
        self.canvas.bind("<ButtonRelease-3>", self.stop_drag)
        self.canvas.bind("<B3-Motion>", self.drag_fine)

        try:
            self.dseg_font = tkfont.Font(family="DSEG7 Classic", size=int(25 * SCALE))
        except:
            self.dseg_font = tkfont.nametofont("TkFixedFont")

        self.init_display()
        self.update_display()

        if self.preset_mode == "active":
            self.init_preset_button()

    def init_preset_button(self):
        self.preset_button = Button(self, text="", relief="raised", bd=2, compound="left")
        self.preset_button.place(x=5, y=200)

        self.color_box = Frame(self.preset_button, width=15, height=3, bg="teal")
        self.color_box.pack(side="left", padx=4, pady=2)

        self.color_box.bind("<ButtonPress-1>", lambda e: self.preset_button.event_generate("<ButtonPress-1>"))
        self.color_box.bind("<ButtonRelease-1>", lambda e: self.preset_button.event_generate("<ButtonRelease-1>"))

        self.preset_button.bind("<ButtonPress-1>", self.preset_press)
        self.preset_button.bind("<ButtonRelease-1>", self.preset_release)

        self.preset_button.config(command=self.preset_action)

    def preset_press(self, event):
        self.color_box.config(bg="cyan")

    def preset_release(self, event):
        self.color_box.config(bg="teal")

    def preset_action(self):
        self.angle = 135
        self.fine_angle = 135
        self.value = self.start_value
        self.update_display()

    def angle_to_value(self, angle):
        return self.start_value + (angle - 135) / 270 * self.value_range

    def value_to_angle(self, value):
        return 135 + (value - self.start_value) / self.value_range * 270

    def led_g_on(self):
        self.led_g_state = 'on'
        self.update_display()

    def led_g_off(self):
        self.led_g_state = 'off'
        self.update_display()

    def led_g_blink(self):
        self.led_g_state = 'blink'
        self.blink_leds()

    def led_r_on(self):
        self.led_r_state = 'on'
        self.update_display()

    def led_r_off(self):
        self.led_r_state = 'off'
        self.update_display()

    def led_r_blink(self):
        self.led_r_state = 'blink'
        self.blink_leds()

    def blink_leds(self):
        if self.led_g_state != 'blink' and self.led_r_state != 'blink':
            return
        self.blink_state = not self.blink_state
        self.update_display()
        self.after(700, self.blink_leds)

    def init_display(self):
        self.value_label = Label(self, text=f"{self.start_value:.2f}", font=self.dseg_font,
                                 fg="cyan", bg="black", bd=1, relief="flat", width=5)
        self.value_label.place(x=CENTER_X, y=int(268 * SCALE), anchor="n")

    def draw_leds(self):
        red_color = '#FF0000' if self.led_r_state == "on" else '#600000'
        if self.led_r_state == "blink":
            red_color = '#600000' if self.blink_state else '#FF0000'

        green_color = '#00FF00' if self.led_g_state == "on" else '#006000'
        if self.led_g_state == "blink":
            green_color = '#006000' if self.blink_state else '#00FF00'

        size = int(20 * SCALE)
        y = 10

        self.canvas.create_oval(10, y, 10 + size, y + size, fill=red_color)
        self.canvas.create_oval(195, y, 195 + size, y + size, fill=green_color)

    def draw_scale(self):
        arc_width = int(10 * SCALE)
        self.canvas.create_arc(CENTER_X - RADIUS, CENTER_Y - RADIUS, CENTER_X + RADIUS, CENTER_Y + RADIUS,
                               start=-45, extent=270, style=ARC, width=arc_width, outline='gray')
        for i in range(11):  
            value = int(round(self.start_value + i * (self.value_range / 10)))  
            angle_deg = 135 + (270 / 10) * i
            angle_rad = math.radians(angle_deg)
            outer = self.polar_to_cartesian(RADIUS, angle_rad)
            length = 10 * SCALE
            inner = self.polar_to_cartesian(RADIUS - length, angle_rad)
            self.canvas.create_line(*outer, *inner, fill='black')
            text_pos = self.polar_to_cartesian(RADIUS + 20 * SCALE, angle_rad)
            self.canvas.create_text(*text_pos, text=f"{value}", font=("Arial", int(12 * SCALE)))

    def polar_to_cartesian(self, radius, angle_rad):
        x = CENTER_X + radius * math.cos(angle_rad)
        y = CENTER_Y + radius * math.sin(angle_rad)
        return x, y

    def draw_knob(self):
        self.canvas.create_oval(CENTER_X - RADIUS, CENTER_Y - RADIUS,
                                CENTER_X + RADIUS, CENTER_Y + RADIUS,
                                fill=self.fill_outer_knob, outline='black')

        inner_offset = int(30 * SCALE)
        self.canvas.create_oval(CENTER_X - RADIUS + inner_offset, CENTER_Y - RADIUS + inner_offset,
                                CENTER_X + RADIUS - inner_offset, CENTER_Y + RADIUS - inner_offset,
                                fill=self.fill_inner_knob, outline='black')

        angle_rad = math.radians(self.angle)
        base = self.polar_to_cartesian(RADIUS, angle_rad)
        left = self.polar_to_cartesian(RADIUS - 30 * SCALE, angle_rad - math.radians(15))
        right = self.polar_to_cartesian(RADIUS - 30 * SCALE, angle_rad + math.radians(15))
        self.canvas.create_polygon(base, left, right, fill="#ff0000", outline="black")

        fine_rad = math.radians(self.fine_angle)
        x, y = self.polar_to_cartesian(RADIUS - 46.5 * SCALE, fine_rad)
        r = int(15.5 * SCALE)
        self.canvas.create_oval(x - r, y - r, x + r, y + r, fill="#0000ff", outline="black")

        self.canvas.create_text(207, 213, text="Thales", font="Helvetica 7", fill="gray")

    def update_display(self):
        self.canvas.delete("all")
        self.draw_leds()
        self.draw_scale()
        self.draw_knob()
        self.value_label.config(text=f"{self.value:.2f}", font=("DSEG7 Classic", 17, "bold"))  

    def start_drag_triangle(self, event):
        self.dragging_triangle = True

    def start_drag_circle(self, event):
        self.dragging_circle = True

    def stop_drag(self, event):
        self.dragging_triangle = False
        self.dragging_circle = False

    def drag_main(self, event):
        if self.dragging_triangle:
            dx, dy = event.x - CENTER_X, event.y - CENTER_Y
            angle = math.degrees(math.atan2(dy, dx))
            angle = (angle + 360) % 360
            if angle >= 135 or angle <= 45:
                if angle < 135:
                    angle += 360
                angle = max(135, min(angle, 405))
                self.angle = angle
                self.value = self.angle_to_value(self.angle)
                self.update_display()

    def drag_fine(self, event):
        if self.dragging_circle:
            dx, dy = event.x - CENTER_X, event.y - CENTER_Y
            angle = math.degrees(math.atan2(dy, dx))
            angle = (angle + 360) % 360
            if angle >= 135 or angle <= 45:
                if angle < 135:
                    angle += 360
                angle = max(135, min(angle, 405))
                delta_angle = angle - self.fine_angle
                if delta_angle > 180:
                    delta_angle -= 360
                elif delta_angle < -180:
                    delta_angle += 360
                fine_sensitivity = 0.01
                self.fine_angle = angle
                self.angle += delta_angle * fine_sensitivity
                self.angle = max(135, min(self.angle, 405))
                self.value = self.angle_to_value(self.angle)
                self.update_display()

    def return_value(self):
        return self.value

if __name__ == "__main__":
    root = Tk()
    root.title("Potentiometer with Layout Flexibility")
    poti = Poti10K(root, preset="active", start_value=140, end_value=150)
    poti.pack(padx=10, pady=10)

    poti.led_g_blink()
    poti.led_r_on()

    root.mainloop()