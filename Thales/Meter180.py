import tkinter as tk
from tkinter import *
import math
from PIL import Image, ImageDraw, ImageTk

class Meter180:
    def __init__(self, master=None, green_start=45, green_end=100,
                 yellow_start=0, yellow_end=15,
                 red_start=15, red_end=45, peak="inactive", drag="inactive",
                 damp="inactive", unit="", fill="#000079", needle_fill="red",
                 scala_fill="white", scala_number_fill="white", val_blink="inactive",
                 style="roundrect"):
        frame_width = 345
        frame_height = 148
        
        self.fill = fill
        self.needle_fill = needle_fill
        self.scala_number_fill = scala_number_fill
        self.scala_fill = scala_fill
        self.val_blink = val_blink
        self.blinking = True
        self.blink_timer = None
        self.blink_visible = "inactive"
        
        self.green_start = green_start
        self.green_end = green_end
        self.yellow_start = yellow_start
        self.yellow_end = yellow_end
        self.red_start = red_start
        self.red_end = red_end

        self.style = style

        self.frame = tk.Frame(master, relief="raised", bd=3, width=frame_width, height=frame_height)
        self.frame.pack_propagate(True)

        self.canvas = tk.Canvas(self.frame, width=330, height=160)
        self.canvas.pack(padx=(frame_width - 330) // 2, pady=(frame_height - 140))

        self.center_x = 165
        self.center_y = 147

        self.led_r_state = False
        self.led_g_state = False

        self.peak = peak
        self.drag = drag
        self.damp = damp
        self.unit = unit

        self.bg_image = None
        self.highest_value = 0
        self.peak_x = None
        self.peak_y = None
        self.drag_value = 0
        self.drag_timer = None
        self.needle_angle = -185
        self.needle = None

        self.draw_meter()
        self.set_value(0)
    
    def led_r_on(self):
        self.led_r = "on"
        self.led_r_state = True
        self.draw_leds()

    def led_r_off(self):
        self.led_r = "off"
        self.led_r_state = False
        self.draw_leds()

    def led_r_blink(self):
        self.led_r = "blink"
        self.blink_led("r")

    def led_g_on(self):
        self.led_g = "on"
        self.led_g_state = True
        self.draw_leds()

    def led_g_off(self):
        self.led_g = "off"
        self.led_g_state = False
        self.draw_leds()

    def led_g_blink(self):
        self.led_g = "blink"
        self.blink_led("g")
    
    def draw_rounded_background(self, x1, y1, x2, y2, radius=75, fill="#000079"):
        width = x2 - x1
        height = y2 - y1

        image = Image.new("RGBA", (width, height), (0, 0, 0, 0))
        draw = ImageDraw.Draw(image)

        draw.rounded_rectangle((0, 0, width, height), radius=radius, fill=fill)

        self.bg_image = ImageTk.PhotoImage(image)
        self.canvas.create_image(x1, y1, anchor=NW, image=self.bg_image)
        self.canvas.bg_image = self.bg_image 
    
    def draw_colored_zones(self):
        def draw_zone(start_val, end_val, color):
            start_angle = -180 - (start_val / 100) * 180
            extent = -((end_val - start_val) / 100) * 180
            self.canvas.create_arc(
                self.center_x - 91, self.center_y - 91,
                self.center_x + 91, self.center_y + 91,
                start=start_angle, extent=extent,
                style=tk.ARC, width=10, outline=color
            )

        if self.green_start != self.green_end:
            draw_zone(self.green_start, self.green_end, "green")
        if self.yellow_start != self.yellow_end:
            draw_zone(self.yellow_start, self.yellow_end, "yellow")
        if self.red_start != self.red_end:
            draw_zone(self.red_start, self.red_end, "red")

    
    def draw_meter(self):
        radius = 15 if self.style == "roundrect" else 0
        self.draw_rounded_background(1, 1, 335, 165, radius=radius, fill=self.fill)

        # Larger arcs
        self.canvas.create_arc(30, 0, 370, 340, start=280, extent=40, outline='red', width=10, style=tk.ARC)
        self.canvas.create_arc(30, 0, 370, 340, start=260, extent=40, outline='green', width=10, style=tk.ARC)
        self.canvas.create_arc(30, 0, 370, 340, start=300, extent=40, outline='red', width=10, style=tk.ARC)
        
        self.draw_colored_zones()
        
        for i in range(11):
            angle = -180 - (i * 18)
            x1 = self.center_x + 110 * math.cos(math.radians(angle))
            y1 = self.center_y - 110 * math.sin(math.radians(angle))
            x2 = self.center_x + 95 * math.cos(math.radians(angle))
            y2 = self.center_y - 95 * math.sin(math.radians(angle))
            self.canvas.create_line(x1, y1, x2, y2, fill=self.scala_fill, width=2)

            num_x = self.center_x + 130 * math.cos(math.radians(angle))
            num_y = self.center_y - 130 * math.sin(math.radians(angle))
            self.canvas.create_text(num_x, num_y, text=str(i * 10), font=("Arial", 12), fill=self.scala_number_fill)

        self.draw_leds()

        x, y = self.center_x, self.center_y - 50
        width = 60
        height = 25

        self.display_rect = self.canvas.create_rectangle(
            x - width // 2, y - height // 2,
            x + width // 2, y + height // 2,
            fill="black", outline="white", width=1
        )

        self.display_text = self.canvas.create_text(
            x, y,
            text="00.00", font=("DSEG7 Classic", 12, "bold"),
            fill="cyan"
        )

        self.unit_text = self.canvas.create_text(
            x, y + 23,
            text=self.unit, font=("Arial", 10, "normal"),
            fill="white"
        )

        self.canvas.tag_raise(self.display_text)
        self.canvas.tag_raise(self.unit_text)

    def draw_leds(self):
        red_color = '#FF0000' if self.led_r_state else '#600000'
        green_color = '#00FF00' if self.led_g_state else '#006000'
        self.canvas.create_oval(15, 10, 35, 30, fill=red_color, outline='black')
        self.canvas.create_oval(298, 10, 318, 30, fill=green_color, outline='black')

    def set_value(self, value):
        angle = -180 - (value / 100) * 180
        self.canvas.itemconfig(self.display_text, text=f"{value:05.2f}")

        if self.damp == "active":
            self.smooth_move_needle(angle)
        else:
            self.update_needle(angle)

        if self.peak == "active":
            if value > self.highest_value:
                self.highest_value = value
                self.peak_x = self.center_x + 97 * math.cos(math.radians(angle))
                self.peak_y = self.center_y - 97 * math.sin(math.radians(angle))
                self.canvas.delete("peak")
                self.draw_peak(self.peak_x, self.peak_y)

        if self.drag == "active":
            if value > self.drag_value:
                self.drag_value = value
                self.canvas.delete("drag_peak")
                self.draw_peak(
                    self.center_x + 97 * math.cos(math.radians(angle)),
                    self.center_y - 97 * math.sin(math.radians(angle)),
                    tag="drag_peak", color="lightgreen")
            self.canvas.after(1000, self.decrease_drag)

        if self.val_blink == "active" and (value == 0 or value == 100):
            if self.blinking != "active":
                self.blinking = "active"
                self.start_value_blink()
        else:
            if self.blinking == "active":
                self.stop_value_blink()

    def start_value_blink(self):
        self.blink_visible = not self.blink_visible
        fill_color = "red" if self.blink_visible else "darkred"
        self.canvas.itemconfig(self.display_text, fill=fill_color)
        self.blink_timer = self.canvas.after(500, self.start_value_blink)

    def stop_value_blink(self):
        if self.blink_timer:
            self.canvas.after_cancel(self.blink_timer)
            self.blink_timer = None
        self.canvas.itemconfig(self.display_text, fill="cyan")
        self.blinking = "inactive"

    def smooth_move_needle(self, target_angle):
        diff = target_angle - self.needle_angle
        step = diff * 0.1
        if abs(diff) > 1:
            new_angle = self.needle_angle + step
            self.update_needle(new_angle)
            self.canvas.after(20, self.smooth_move_needle, target_angle)
        else:
            self.update_needle(target_angle)

    def update_needle(self, angle):
        self.needle_angle = angle
        tip_x = self.center_x + 110 * math.cos(math.radians(angle))
        tip_y = self.center_y - 110 * math.sin(math.radians(angle))
        base_x1 = self.center_x + 5 * math.cos(math.radians(angle + 90))
        base_y1 = self.center_y - 5 * math.sin(math.radians(angle + 90))
        base_x2 = self.center_x + 5 * math.cos(math.radians(angle - 90))
        base_y2 = self.center_y - 5 * math.sin(math.radians(angle - 90))

        if self.needle:
            self.canvas.delete("needle")
        self.needle = self.canvas.create_polygon(
            tip_x, tip_y, base_x1, base_y1, base_x2, base_y2,
            fill=self.needle_fill, outline='black', tags="needle"
        )
        self.canvas.create_oval(self.center_x - 5, self.center_y - 5,
                                self.center_x + 5, self.center_y + 5,
                                fill='gray', outline='black', tags="needle")
        self.canvas.tag_raise("needle")

    def draw_peak(self, x, y, tag="peak", color="yellow"):
        peak_size = 13
        angle = math.degrees(math.atan2(self.center_y - y, x - self.center_x))
        offset_x = (x - self.center_x) * 1.15
        offset_y = (y - self.center_y) * 1.00
        peak_x = self.center_x + offset_x
        peak_y = self.center_y + offset_y
        tip_x, tip_y = peak_x, peak_y
        left_x = tip_x + peak_size * math.cos(math.radians(angle - 45))
        left_y = tip_y - peak_size * math.sin(math.radians(angle - 45))
        right_x = tip_x + peak_size * math.cos(math.radians(angle + 45))
        right_y = tip_y - peak_size * math.sin(math.radians(angle + 45))

        self.canvas.create_polygon(left_x, left_y, tip_x, tip_y, right_x, right_y,
                                   fill=color, outline='black', tags=tag)

    def decrease_drag(self):
        if self.drag_value > 0:
            self.drag_value -= 1
            angle = -185 - (self.drag_value * 100 / 59)
            tip_x = self.center_x + 97 * math.cos(math.radians(angle))
            tip_y = self.center_y - 97 * math.sin(math.radians(angle))
            self.canvas.delete("drag_peak")
            self.draw_peak(tip_x, tip_y, tag="drag_peak", color="lightgreen")
            self.drag_timer = self.canvas.after(100, self.decrease_drag)
        else:
            self.drag_timer = self.canvas.after(2000, self.hide_drag)


    def hide_drag(self):
        self.canvas.delete("drag_peak")

    def blink_led(self, led):
        if led == "r":
            self.led_r_state = not self.led_r_state
        elif led == "g":
            self.led_g_state = not self.led_g_state
        self.draw_leds()
        self.canvas.after(700, self.blink_led, led)
        
    def pack(self, **kwargs):
        self.frame.pack(**kwargs)
if __name__ == "__main__":
    root = tk.Tk()
    root.title("Meter120 Display")

    peak = "active"
    drag = "inactive"
    damp = "inactive"

    meter120 = Meter180(root, peak=peak, drag=drag, damp=damp,
                        unit="U/min x100", green_start=65, green_end=100,
    yellow_start=5, yellow_end=65,
    red_start=0, red_end=5, val_blink="active", style="rect")
    meter120.frame.place(x=70, y=40)

    def update_needle(value):
        meter120.set_value(int(value))
        
    meter120.led_g_blink()

    schieber = Scale(root, from_=0, to=100, orient=HORIZONTAL, command=update_needle)
    schieber.pack()

    root.mainloop()