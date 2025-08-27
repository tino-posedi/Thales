import tkinter as tk
from tkinter import *
import math
import random
from PIL import Image, ImageDraw, ImageTk

class Meter120:
    def __init__(self, master=None, peak="inactive", drag="inactive", damp="inactive", unit="", fill="#000079", needle_fill="red", scala_fill="white", scala_number_fill="white", val_blink="inactive", style="roundrect"):
        frame_width = 345
        frame_height = 155

        self.fill = fill
        self.needle_fill = needle_fill
        self.scala_number_fill = scala_number_fill
        self.scala_fill = scala_fill
        self.val_blink = val_blink
        self.blinking = True
        self.blink_timer = None
        self.blink_visible = "inactive"
        self.style = style

        self.frame = tk.Frame(master, relief="raised", bd=3, width=frame_width, height=frame_height)
        self.frame.pack_propagate(True)

        self.canvas = tk.Canvas(self.frame, width=330, height=140)
        self.canvas.pack(padx=(frame_width - 330) // 2, pady=(frame_height - 140) // 2)
        
        self.center_x = 165
        self.center_y = 150

        self.led_r_mode = "off" 
        self.led_g_mode = "off"  
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

        self.needle_angle = 200
        self.needle = None

        self.draw_meter()
        self.set_value(0)

    def led_r_on(self):
        self.led_r_mode = "on"
        self.draw_leds()

    def led_r_off(self):
        self.led_r_mode = "off"
        self.draw_leds()

    def led_r_blink(self):
        self.led_r_mode = "blink"
        self.blink_led("r")

    def led_g_on(self):
        self.led_g_mode = "on"
        self.draw_leds()

    def led_g_off(self):
        self.led_g_mode = "off"
        self.draw_leds()

    def led_g_blink(self):
        self.led_g_mode = "blink"
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

    def draw_meter(self):
        radius = 15 if self.style == "roundrect" else 0
        self.draw_rounded_background(1, 1, 335, 143, radius=radius, fill=self.fill)

        for i in range(11):
            angle = 150 - (i * 12)
            rad = math.radians(angle)
            x1 = 165 + 110 * math.cos(rad)
            y1 = 170 - 110 * math.sin(rad)
            x2 = 165 + 130 * math.cos(rad)
            y2 = 170 - 130 * math.sin(rad)
            self.canvas.create_line(x1, y1, x2, y2, fill=self.scala_fill, width=2)

            num_x = self.center_x + 150 * math.cos(rad)
            num_y = self.center_y - 150 * math.sin(rad)
            self.canvas.create_text(num_x, num_y + 20, text=str(i * 10), font=("Arial", 12), fill=self.scala_number_fill)

        for i in range(21):
            if i % 2 == 0:
                continue
            value = i * 5
            angle = 210 + (value * 120 / 100)
            rad = math.radians(angle)
            x1 = 165 + 120 * math.cos(rad)
            y1 = 170 + 120 * math.sin(rad)
            x2 = 165 + 130 * math.cos(rad)
            y2 = 170 + 130 * math.sin(rad)
            self.canvas.create_line(x1, y1, x2, y2, fill=self.scala_fill, width=1)

        self.canvas.create_arc(
            self.center_x - 125, self.center_y - 110,
            self.center_x + 125, self.center_y + 110,
            start=156, extent=-132, style='arc', outline=self.scala_fill, width=1
        )

        self.draw_leds()

        x, y = self.center_x, self.center_y - 65
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
        if self.led_r_mode == "on":
            red_color = '#FF0000'
        elif self.led_r_mode == "off":
            red_color = '#600000'
        elif self.led_r_mode == "blink":
            red_color = '#8B0000' if self.led_r_state else '#FF0000'
        else:
            red_color = '#600000'

        if self.led_g_mode == "on":
            green_color = '#00FF00'
        elif self.led_g_mode == "off":
            green_color = '#006000'
        elif self.led_g_mode == "blink":
            green_color = '#006000' if self.led_g_state else '#00FF00'
        else:
            green_color = '#006000'

        self.canvas.create_oval(15, 10, 35, 30, fill=red_color, outline='black')
        self.canvas.create_oval(298, 10, 318, 30, fill=green_color, outline='black')

    def set_value(self, value):
        angle = 200 + (value * 140 / 100)
        self.canvas.itemconfig(self.display_text, text=f"{value:05.2f}")

        if self.damp == "active":
            self.smooth_move_needle(angle)
        else:
            self.update_needle(angle)

        if self.peak == "active":
            if value > self.highest_value:
                self.highest_value = value
                self.peak_x = self.center_x + 140 * math.cos(math.radians(angle))
                self.peak_y = self.center_y + 140 * math.sin(math.radians(angle))
                self.canvas.delete("peak")
                self.draw_peak(angle, tag="peak", color="yellow")

        if self.drag == "active":
            if value > self.drag_value:
                self.drag_value = value
                self.canvas.delete("drag_peak")
                self.draw_peak(angle, tag="drag_peak", color="lightgreen")
            if self.drag_timer:
                self.canvas.after_cancel(self.drag_timer)
            self.drag_timer = self.canvas.after(1000, self.decrease_drag)

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
        tip_x = self.center_x + 90 * math.cos(math.radians(angle))
        tip_y = self.center_y + 90 * math.sin(math.radians(angle))
        base_x1 = self.center_x + 6 * math.cos(math.radians(angle + 90))
        base_y1 = self.center_y + 6 * math.sin(math.radians(angle + 90))
        base_x2 = self.center_x + 6 * math.cos(math.radians(angle - 90))
        base_y2 = self.center_y + 6 * math.sin(math.radians(angle - 90))

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

    def draw_peak(self, angle, tag="peak", color="yellow"):
        peak_radius = 115
        peak_size = 13
        rad = math.radians(angle)
        peak_x = self.center_x + peak_radius * math.cos(rad)
        peak_y = self.center_y + peak_radius * math.sin(rad)
        offset_angle = math.degrees(math.atan2(peak_y - self.center_y, peak_x - self.center_x))
        tip_x, tip_y = peak_x, peak_y
        left_x = tip_x + peak_size * math.cos(math.radians(offset_angle - 45))
        left_y = tip_y + peak_size * math.sin(math.radians(offset_angle - 45))
        right_x = tip_x + peak_size * math.cos(math.radians(offset_angle + 45))
        right_y = tip_y + peak_size * math.sin(math.radians(offset_angle + 45))
        self.canvas.create_polygon(left_x, left_y, tip_x, tip_y, right_x, right_y,
                                   fill=color, outline='black', tags=tag)

    def decrease_drag(self):
        if self.drag_value > 0:
            self.drag_value -= 1
            angle = 200 + (self.drag_value * 140 / 100)
            self.canvas.delete("drag_peak")
            self.draw_peak(angle, tag="drag_peak", color="lightgreen")
            self.drag_timer = self.canvas.after(100, self.decrease_drag)
        else:
            self.drag_timer = self.canvas.after(3000, self.hide_drag)

    def hide_drag(self):
        self.canvas.delete("drag_peak")
        self.drag_timer = None

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

    meter120 = Meter120(root, peak="inactive", drag="inactive", damp="inactive",
                        unit="U/min x100", needle_fill="white", fill="teal",
                        scala_number_fill="white", scala_fill="white", val_blink="inactive", style="roundrect")
    meter120.frame.place(x=70, y=40)

    meter120.set_value(0) 

    def set_final_value():
        val = random.uniform(30, 60)
        meter120.set_value(val)

        # LED logic
        if val <= 40:
            meter120.led_r_on()
            meter120.led_g_off()
        else:
            meter120.led_g_on()
            meter120.led_r_off()

    root.after(2000, set_final_value)

    root.geometry("500x250")
    root.mainloop()