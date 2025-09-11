import tkinter as tk
from tkinter import *
import math
from PIL import Image, ImageDraw, ImageTk

class Meter90:
    def __init__(self, master=None, green_start=60, green_end=80,
                 yellow_start=0, yellow_end=10,
                 red_start=80, red_end=100, peak="inactive", drag="inactive",
                 damp="inactive", unit="", fill="#000079", needle_fill="red",
                 scala_fill="white", scala_number_fill="white", val_blink="inactive",
                 style="roundrect"):

        frame_width = 200
        frame_height = 200

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
        
        self.arc_start_angle = 180  
        self.arc_end_angle = 90    
        self.arc_span = self.arc_start_angle - self.arc_end_angle

        self.style = style

        self.frame = tk.Frame(master, relief="raised", bd=3, width=frame_width, height=frame_height)
        self.frame.pack_propagate(True)

        self.canvas = tk.Canvas(self.frame, width=175, height=175, bg="systembuttonface", highlightthickness=0)

        self.canvas.place(x = 10, y = 10)

        self.center_x = frame_width // 1.4
        self.center_y = frame_height - 50

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
        self.needle_angle = 0
        self.needle = None

        self.draw_meter()
        self.set_value(0)

    def led_r_on(self):
        self.led_r_state = True
        self.draw_leds()

    def led_r_off(self):
        self.led_r_state = False
        self.draw_leds()

    def led_r_blink(self):
        self.blink_led("r")

    def led_g_on(self):
        self.led_g_state = True
        self.draw_leds()

    def led_g_off(self):
        self.led_g_state = False
        self.draw_leds()

    def led_g_blink(self):
        self.blink_led("g")
    
    def draw_rounded_background(self, fill="#000079", radius=10):
        width, height = 175, 175
        image = Image.new("RGBA", (width, height), (0, 0, 0, 0))
        draw = ImageDraw.Draw(image)
        draw.rounded_rectangle((0, 0, width, height), radius=radius, fill=fill)

        self.bg_image = ImageTk.PhotoImage(image)
        self.canvas.create_image(0, 0, anchor=NW, image=self.bg_image)
        self.canvas.bg_image = self.bg_image

    def draw_meter(self):

        radius = 12 if self.style == "roundrect" else 0
        self.draw_rounded_background(fill=self.fill, radius=radius)

        offset = 10          
        arc_radius = 115
        tick_outer = 130
        tick_inner = 120
        num_radius = 140

        def draw_zone(start_val, end_val, color):
            start_angle = 180 - (start_val / 100) * 90
            extent = -((end_val - start_val) / 100) * 90
            self.canvas.create_arc(
                self.center_x - arc_radius + offset, self.center_y - arc_radius + offset,
                self.center_x + arc_radius + offset, self.center_y + arc_radius + offset,
                start=start_angle, extent=extent,
                style=tk.ARC, width=9, outline=color
            )

        if self.green_start != self.green_end:
            draw_zone(self.green_start, self.green_end, "green")
        if self.yellow_start != self.yellow_end:
            draw_zone(self.yellow_start, self.yellow_end, "yellow")
        if self.red_start != self.red_end:
            draw_zone(self.red_start, self.red_end, "red")

        for i in range(11):
            angle = 180 - (i * 9)
            x1 = self.center_x + offset + tick_outer * math.cos(math.radians(angle))
            y1 = self.center_y + offset - tick_outer * math.sin(math.radians(angle))
            x2 = self.center_x + offset + tick_inner * math.cos(math.radians(angle))
            y2 = self.center_y + offset - tick_inner * math.sin(math.radians(angle))
            self.canvas.create_line(x1, y1, x2, y2, fill=self.scala_fill, width=2)

            num_x = self.center_x + offset + num_radius * math.cos(math.radians(angle))
            num_y = self.center_y + offset - num_radius * math.sin(math.radians(angle))
            self.canvas.create_text(num_x, num_y, text=str(i * 10),
                                    font=("Arial", 10), fill=self.scala_number_fill)

        disp_offset_x = -20     
        disp_offset_y = -45   
        unit_offset_x = -20    
        unit_offset_y = -20   

        disp_width = 80
        disp_height = 28
        disp_x = self.center_x + disp_offset_x
        disp_y = self.center_y + disp_offset_y
        self.display_rect = self.canvas.create_rectangle(
            disp_x - disp_width // 2, disp_y - disp_height // 2,
            disp_x + disp_width // 2, disp_y + disp_height // 2,
            fill="black", outline="white", width=1
        )

        self.display_text = self.canvas.create_text(
            disp_x, disp_y,
            text="0000", font=("DSEG7 Classic", 14, "bold"),
            fill="cyan"
        )
        self.unit_text = self.canvas.create_text(
            self.center_x + unit_offset_x, self.center_y + unit_offset_y,
            text=self.unit, font=("Arial", 10, "normal"),
            fill="white"
        )

        self.draw_leds()
    
    def draw_leds(self):
        red_color = '#FF0000' if self.led_r_state else '#600000'
        green_color = '#00FF00' if self.led_g_state else '#006000'
        self.canvas.create_oval(10, 10, 25, 25, fill=red_color, outline='black')
        self.canvas.create_oval(30, 10, 45, 25, fill=green_color, outline='black')
    
    
    def set_value(self, value):
        value = max(0, min(100, value))
        angle = self.arc_start_angle - (value / 100) * self.arc_span
        self.canvas.itemconfig(self.display_text, text=f"{value:05.2f}")

        if self.damp == "active":
            self.smooth_move_needle(angle)
        else:
            self.update_needle(angle)

        # Peak logic
        if self.peak == "active":
            if value > self.highest_value:
                self.highest_value = value
                tip_x = self.center_x + self.needle_offset_x + 125 * math.cos(math.radians(angle))
                tip_y = self.center_y + self.needle_offset_y - 125 * math.sin(math.radians(angle))
                self.canvas.delete("peak")
                self.draw_peak(tip_x, tip_y)

        # Drag logic
        if self.drag == "active":
            if value > self.drag_value:
                self.drag_value = value
                tip_x = self.center_x + self.needle_offset_x + 125 * math.cos(math.radians(angle))
                tip_y = self.center_y + self.needle_offset_y - 125 * math.sin(math.radians(angle))
                self.canvas.delete("drag_peak")
                self.draw_peak(tip_x, tip_y, tag="drag_peak", color="lightgreen")
            self.canvas.after(1000, self.decrease_drag)


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

        needle_length = 125
        needle_width = 7
        knob_radius = 9
        self.needle_offset_x = 11 
        self.needle_offset_y = 10 

        cx = self.center_x + self.needle_offset_x
        cy = self.center_y + self.needle_offset_y

        tip_x = cx + needle_length * math.cos(math.radians(angle))
        tip_y = cy - needle_length * math.sin(math.radians(angle))
        base_x1 = cx + needle_width * math.cos(math.radians(angle + 90))
        base_y1 = cy - needle_width * math.sin(math.radians(angle + 90))
        base_x2 = cx + needle_width * math.cos(math.radians(angle - 90))
        base_y2 = cy - needle_width * math.sin(math.radians(angle - 90))

        if self.needle:
            self.canvas.delete("needle")

        self.needle = self.canvas.create_polygon(
            tip_x, tip_y, base_x1, base_y1, base_x2, base_y2,
            fill=self.needle_fill, outline='black', tags="needle"
        )

        self.canvas.create_oval(
            cx - knob_radius, cy - knob_radius,
            cx + knob_radius, cy + knob_radius,
            fill='gray', outline='black', tags="needle"
        )

        self.canvas.tag_raise("needle")
        
    def draw_peak(self, x, y, tag="peak", color="yellow"):
        peak_size = 13
        angle = math.degrees(math.atan2(self.center_y - y, x - self.center_x))
        offset_x = (x - self.center_x) * 1.0
        offset_y = (y - self.center_y) * 1.0
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
            angle = self.arc_start_angle - (self.drag_value / 100) * self.arc_span
            tip_x = self.center_x + self.needle_offset_x + 125 * math.cos(math.radians(angle))
            tip_y = self.center_y + self.needle_offset_y - 125 * math.sin(math.radians(angle))
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
    root.title("Meter90 Display")
    root.geometry("800x600")

    meter90 = Meter90(root, unit="mA", green_start=70, green_end=100,
                      yellow_start=40, yellow_end=70,
                      red_start=0, red_end=40, style="roundrect", peak="active", drag="active")
    meter90.frame.place(x=20, y=20)

    def update_needle(value):
        meter90.set_value(float(value))
        
        if(float(value) > 40):
            meter90.led_r_off()
            meter90.led_g_on()
        else:
            meter90.led_g_off()
            meter90.led_r_on()

    schieber = Scale(
        root,
        from_=0.0,
        to=100.0,
        orient=HORIZONTAL,
        resolution=0.01,
        command=update_needle,
        length=300
    )
    schieber.pack()

    root.mainloop()
