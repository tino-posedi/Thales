import tkinter as tk
import math
import time
import threading

class Meter360(tk.Frame):
    def __init__(self, master=None, width=290, height=290,
                 inner_from=0, inner_to=10000, outer_from=0, outer_to=1000,
                 style="roundrect", outer_ring_fill="magenta", inner_ring_fill="yellow", fill="#000079", **kwargs):
        super().__init__(master, width=width, height=height, bd=3, relief="raised", **kwargs)
        self.width = width
        self.height = height
        self.style = style

        self.led_r_mode = "off"
        self.led_g_mode = "off"
        self.led_r_state = True
        self.led_g_state = True
        self.blink_delay = 700 

        self.outer_ring_fill = outer_ring_fill
        self.inner_ring_fill = inner_ring_fill
        self.fill = fill

        self.last_value = 0
        self.direction = "none"
        self.blink_up = False
        self.blink_down = False
        self.triangle_state = True 

        self.inner_from = inner_from
        self.inner_to = inner_to
        self.outer_from = outer_from
        self.outer_to = outer_to

        self.canvas = tk.Canvas(self, width=width, height=height, highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)

        self.needle_angle = 0
        self.secondary_needle_angle = 0
        self.draw_widget()
        self.blink()

    def led_r_on(self):
        self.led_r_mode = "on"
        self.draw_leds()

    def led_r_off(self):
        self.led_r_mode = "off"
        self.draw_leds()

    def led_r_blink(self):
        self.led_r_mode = "blink"

    def led_g_on(self):
        self.led_g_mode = "on"
        self.draw_leds()

    def led_g_off(self):
        self.led_g_mode = "off"
        self.draw_leds()

    def led_g_blink(self):
        self.led_g_mode = "blink"

    def draw_smooth_rounded_rect(self, x1, y1, x2, y2, r, **kwargs):
        points = [
            x1+r, y1, x2-r, y1, x2, y1, x2, y1+r,
            x2, y2-r, x2, y2, x2-r, y2, x1+r, y2,
            x1, y2, x1, y2-r, x1, y1+r, x1, y1, x1+r, y1
        ]
        self.canvas.create_polygon(points, smooth=True, splinesteps=36, **kwargs)

    def draw_widget(self):
        self.canvas.delete("all")
        pad = 15
        x1, y1 = pad, pad
        x2, y2 = self.width - pad, self.height - pad

        if self.style == "round":
            radius = min(x2 - x1, y2 - y1) / 2
            cx, cy = (x1 + x2) / 2, (y1 + y2) / 2
            self.canvas.create_oval(cx - radius, cy - radius, cx + radius, cy + radius,
                                    fill=self.fill, width=0)
        else:
            self.draw_smooth_rounded_rect(x1, y1, x2, y2, 30 if self.style == "roundrect" else 0, fill=self.fill, width=0)

        cx = (x1 + x2) / 2
        cy = (y1 + y2) / 2
        outer_radius = min(x2 - x1, y2 - y1) / 2 - 35
        inner_radius = outer_radius - 2.1

        self.canvas.create_oval(cx - outer_radius, cy - outer_radius,
                                cx + outer_radius, cy + outer_radius,
                                outline=self.outer_ring_fill, width=2)

        self.canvas.create_oval(cx - inner_radius, cy - inner_radius,
                                cx + inner_radius, cy + inner_radius,
                                outline=self.inner_ring_fill, width=2)

        for i in range(12):
            angle_deg = 270 + i * 30
            angle_rad = math.radians(angle_deg)

            x_start = cx + outer_radius * math.cos(angle_rad)
            y_start = cy + outer_radius * math.sin(angle_rad)
            x_end = cx + (outer_radius + 8) * math.cos(angle_rad)
            y_end = cy + (outer_radius + 8) * math.sin(angle_rad)
            self.canvas.create_line(x_start, y_start, x_end, y_end, fill=self.outer_ring_fill, width=2)

            label_radius = outer_radius + 20
            label_value = int(self.outer_from + i * ((self.outer_to - self.outer_from) / 11))
            x_text = cx + label_radius * math.cos(angle_rad)
            y_text = cy + label_radius * math.sin(angle_rad)
            self.canvas.create_text(x_text, y_text, text=str(label_value), fill=self.outer_ring_fill,
                                    font=("Arial", 9, "bold"), anchor="center")

        for i in range(12):
            angle_deg = 270 + i * 30
            angle_rad = math.radians(angle_deg)

            x_start = cx + inner_radius * math.cos(angle_rad)
            y_start = cy + inner_radius * math.sin(angle_rad)
            x_end = cx + (inner_radius - 8) * math.cos(angle_rad)
            y_end = cy + (inner_radius - 8) * math.sin(angle_rad)
            self.canvas.create_line(x_start, y_start, x_end, y_end, fill=self.inner_ring_fill, width=2)

            label_radius = inner_radius - 23
            label_value = int(self.inner_from + i * ((self.inner_to - self.inner_from) / 11))
            x_text = cx + label_radius * math.cos(angle_rad)
            y_text = cy + label_radius * math.sin(angle_rad)
            self.canvas.create_text(x_text, y_text, text=str(label_value), fill=self.inner_ring_fill,
                                    font=("Arial", 9), anchor="center")

        needle_length = inner_radius + 10
        self.draw_needle(cx, cy, needle_length, self.needle_angle)
        self.draw_needle(cx, cy, needle_length / 1.2, self.secondary_needle_angle)

        knob_radius = 12
        self.canvas.create_oval(cx - knob_radius, cy - knob_radius,
                                cx + knob_radius, cy + knob_radius,
                                fill="grey", outline="black", width=1)

        if self.style != "round":
            self.draw_leds()
            self.draw_direction_triangles()

    def draw_needle(self, cx, cy, length, angle):
        angle_rad = math.radians(angle - 90)
        base_width = 16
        x_tip = cx + length * math.cos(angle_rad)
        y_tip = cy + length * math.sin(angle_rad)
        perp_angle = angle_rad + math.pi / 2
        x_base_left = cx + (base_width / 2) * math.cos(perp_angle)
        y_base_left = cy + (base_width / 2) * math.sin(perp_angle)
        x_base_right = cx - (base_width / 2) * math.cos(perp_angle)
        y_base_right = cy - (base_width / 2) * math.sin(perp_angle)
        self.canvas.create_polygon([x_base_left, y_base_left, x_tip, y_tip, x_base_right, y_base_right],
                                   fill="red", outline="black")

    def draw_leds(self):
        led_size = 20
        led_y = self.height - 35  

        if self.led_r_mode == "on":
            red_color = '#FF0000'
        elif self.led_r_mode == "off":
            red_color = '#600000'
        elif self.led_r_mode == "blink":
            red_color = '#FF0000' if self.led_r_state else '#600000'
        else:
            red_color = '#600000'

        if self.led_g_mode == "on":
            green_color = '#00FF00'
        elif self.led_g_mode == "off":
            green_color = '#006000'
        elif self.led_g_mode == "blink":
            green_color = '#00FF00' if self.led_g_state else '#006000'
        else:
            green_color = '#006000'

        self.canvas.create_oval(30, led_y - led_size / 2, 30 + led_size, led_y + led_size / 2,
                                fill=red_color, outline='black')
        self.canvas.create_oval(self.width - 30 - led_size, led_y - led_size / 2,
                                self.width - 30, led_y + led_size / 2,
                                fill=green_color, outline='black')

    def blink(self):
        if self.led_r_mode == "blink":
            self.led_r_state = not self.led_r_state
        if self.led_g_mode == "blink":
            self.led_g_state = not self.led_g_state

        if self.direction == "up":
            self.triangle_state = not self.triangle_state
            self.blink_up = self.triangle_state
            self.blink_down = False
        elif self.direction == "down":
            self.triangle_state = not self.triangle_state
            self.blink_down = self.triangle_state
            self.blink_up = False
        else:
            self.blink_up = False
            self.blink_down = False

        self.draw_widget()
        self.after(self.blink_delay, self.blink)

    def draw_direction_triangles(self):
        triangle_size = 20
        up_x_offset, up_y_offset = 105, 25
        down_x_offset, down_y_offset = -105, 5

        up_cx = self.width / 2 + up_x_offset
        up_top_y = up_y_offset
        points_up = [up_cx, up_top_y,
                     up_cx - triangle_size, up_top_y + triangle_size,
                     up_cx + triangle_size, up_top_y + triangle_size]
        up_color = "cyan" if self.blink_up else "teal"
        self.canvas.create_polygon(points_up, fill=up_color, outline="black", width=1)

        down_cx = self.width / 2 + down_x_offset
        down_top_y = down_y_offset
        points_down = [down_cx, down_top_y + 2 * triangle_size,
                       down_cx - triangle_size, down_top_y + triangle_size,
                       down_cx + triangle_size, down_top_y + triangle_size]
        down_color = "yellow" if self.blink_down else "olive"
        self.canvas.create_polygon(points_down, fill=down_color, outline="black")

    def set_value_one(self, angle):
        angle = angle % 360
        self.direction = "up" if angle > self.last_value else "down" if angle < self.last_value else "none"
        self.last_value = angle
        self.needle_angle = angle
        self.draw_widget()

    def set_value_two(self, angle):
        angle = angle % 360
        self.direction = "up" if angle > self.last_value else "down" if angle < self.last_value else "none"
        self.last_value = angle
        self.secondary_needle_angle = angle
        self.draw_widget()

    def stop_blink(self):
        self.blink_up = False
        self.blink_down = False

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Gauge with LEDs")

    widget = Meter360(root,
                      inner_from=1000, inner_to=8000,
                      outer_from=0, outer_to=256,
                      style="roundrect",
                      outer_ring_fill="blue", inner_ring_fill="red", fill="lightgray")
    widget.pack(padx=20, pady=20)
    
    def rotate_red_then_yellow():
        global angle, direction
        angle = 0
        direction = 1
        while True:
            angle += direction
            if angle >= 360:
                angle = 360
                direction = -1
            elif angle <= 0:
                angle = 0
                root.after(0, widget.set_value_one, angle)
                break
            root.after(0, widget.set_value_one, angle)
            time.sleep(0.01)

        angle = 0
        direction = 1
        while True:
            angle += direction
            if angle >= 360:
                angle = 360
                direction = -1
            elif angle <= 0:
                angle = 0
                root.after(0, widget.set_value_two, angle)
                break
            root.after(0, widget.set_value_two, angle)
            time.sleep(0.01)
    
    widget.led_r_blink()   
    widget.led_g_blink()      
    
    threading.Thread(target=rotate_red_then_yellow, daemon=True).start()

    root.mainloop()
