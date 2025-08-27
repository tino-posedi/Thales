import tkinter as tk
import math
from PIL import Image, ImageTk, ImageDraw

class Meter270(tk.Frame):
    def __init__(self, parent, size="medium", damp="inactive", scala_fill="white", scala_number_fill="white",
                 needle_fill="red", fill="#000079", unit="", style="roundrect",
                 red_start=0, red_end=20, yellow_start=20, yellow_end=70, green_start=70, green_end=100):
        super().__init__(parent, relief="raised", bd=3)

        size_map = {
            "small": 180,
            "medium": 250,
            "big": 320
        }
        dim = size_map.get(size, 250)
        self.width = self.height = dim
        self.canvas = tk.Canvas(self, width=dim, height=dim, bg="SystemButtonFace", highlightthickness=0)
        self.canvas.pack(padx=10, pady=10)

        self.center = (dim // 2, dim // 2)
        self.radius = dim // 2 - 48
        self.angle_range = 270
        self.fill = fill
        self.scala_fill = scala_fill
        self.scala_number_fill = scala_number_fill
        self.needle_fill = needle_fill
        self.unit = unit
        self.style = style
        
        self.red_zone = (red_start, red_end)
        self.yellow_zone = (yellow_start, yellow_end)
        self.green_zone = (green_start, green_end)

        if self.style == "roundrect":
            self.corner_radius = 15
        elif self.style == "rect":
            self.corner_radius = 0
        elif self.style == "round":
            self.corner_radius = 1000
        else:
            self.corner_radius = 15

        self.damping_active = damp == "active"
        self.current_value = 0
        self.target_value = 0

        self.set_raised_bevel_background()
        self.draw_gauge()

        self.needle = self.canvas.create_polygon(0, 0, 0, 0, 0, 0, fill=self.needle_fill, outline="black")
        self.center_circle = self.canvas.create_oval(
            self.center[0] - 10, self.center[1] - 10,
            self.center[0] + 10, self.center[1] + 10,
            fill="gray", outline="black"
        )

        if size == "small":
            display_y_offset = 45
            value_font_size = 14
            unit_font_size = 8
        elif size == "big":
            display_y_offset = 85
            value_font_size = 24
            unit_font_size = 12
        else: 
            display_y_offset = 65
            value_font_size = 18
            unit_font_size = 10

        self.value_box = self.canvas.create_rectangle(
            self.center[0] - 50, self.center[1] + display_y_offset - 12,
            self.center[0] + 48, self.center[1] + display_y_offset + 20,
            fill="black", outline="white", width=1
        )

        self.value_text = self.canvas.create_text(
            self.center[0], self.center[1] + display_y_offset + 5,
            text="0000", fill="#00ffff",
            font=("DSEG7 Classic", value_font_size, "bold")
        )

        self.unit_text = self.canvas.create_text(
            self.center[0], self.center[1] + display_y_offset + 30,
            text=self.unit, fill="white",
            font=("Arial", unit_font_size)
        )

        self.set_value(0, immediate=True)

    def set_raised_bevel_background(self):
        img = Image.new("RGBA", (self.width, self.height), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)

        shadow_color = (20, 20, 20, 180)
        highlight_color = (255, 255, 255, 150)

        if self.style == "round":
            radius = self.width // 2
            cx, cy = self.center
            draw.ellipse((cx - radius + 5, cy - radius + 5, cx + radius - 5, cy + radius - 5), fill=shadow_color)
            draw.ellipse((cx - radius + 15, cy - radius + 15, cx + radius - 15, cy + radius - 15), fill=highlight_color)
            draw.ellipse((cx - radius, cy - radius, cx + radius, cy + radius), fill=self.fill)
        else:
            draw.rounded_rectangle((5, 5, self.width - 5, self.height - 5), radius=self.corner_radius, fill=shadow_color)
            draw.rounded_rectangle((15, 15, self.width - 15, self.height - 15), radius=self.corner_radius, fill=highlight_color)
            draw.rounded_rectangle((0, 0, self.width, self.height), radius=self.corner_radius, fill=self.fill)

        self.bg_image = ImageTk.PhotoImage(img)
        self.canvas.create_image(0, 0, anchor="nw", image=self.bg_image)


    def draw_gauge(self):
        for i in range(0, 110, 10):
            angle = math.radians(225 - (i * self.angle_range / 99.4))
            x1 = self.center[0] + (self.radius - -20) * math.cos(angle)
            y1 = self.center[1] - (self.radius - -20) * math.sin(angle)
            x2 = self.center[0] + self.radius * math.cos(angle)
            y2 = self.center[1] - self.radius * math.sin(angle)
            self.canvas.create_line(x1, y1, x2, y2, fill=self.scala_fill, width=2)

            if i % 10 == 0:
                text_value = 100 if i == 100 else i
                text_x = self.center[0] + (self.radius - -33) * math.cos(angle)
                text_y = self.center[1] - (self.radius - -33) * math.sin(angle)
                self.canvas.create_text(text_x, text_y, text=str(text_value), fill=self.scala_number_fill, font=("Arial", 10))

        self.draw_colored_zones()

    def draw_colored_zones(self):
            def value_to_angle(value):
                return 225 - (value * self.angle_range / 100)

            zone_width = 10
            cx, cy = self.center
            r = self.radius

            start = value_to_angle(self.red_zone[0])
            extent = value_to_angle(self.red_zone[1]) - start
            self.canvas.create_arc(
                cx - r, cy - r, cx + r, cy + r,
                start=start, extent=extent, style=tk.ARC, outline="red", width=zone_width
            )

            start = value_to_angle(self.yellow_zone[0])
            extent = value_to_angle(self.yellow_zone[1]) - start
            self.canvas.create_arc(
                cx - r, cy - r, cx + r, cy + r,
                start=start, extent=extent, style=tk.ARC, outline="yellow", width=zone_width
            )

            start = value_to_angle(self.green_zone[0])
            extent = value_to_angle(self.green_zone[1]) - start
            self.canvas.create_arc(
                cx - r, cy - r, cx + r, cy + r,
                start=start, extent=extent, style=tk.ARC, outline="green", width=zone_width
            )

    def set_value(self, value, immediate=False):
        self.target_value = value
        if immediate or not self.damping_active:
            self.current_value = value
            self.update_needle_position()
        else:
            self.smooth_update()

    def smooth_update(self):
        if self.current_value != self.target_value:
            step = (self.target_value - self.current_value) * 0.1
            self.current_value += step
            if abs(self.target_value - self.current_value) < 0.5:
                self.current_value = self.target_value
            self.update_needle_position()
            self.after(20, self.smooth_update)

    def update_needle_position(self):
        angle = math.radians(225 - (self.current_value * self.angle_range / 100))
        tip_x = self.center[0] + (self.radius - 4) * math.cos(angle)
        tip_y = self.center[1] - (self.radius - 4) * math.sin(angle)

        base_width = 5
        base_x1 = self.center[0] + base_width * math.cos(angle + math.pi / 2)
        base_y1 = self.center[1] - base_width * math.sin(angle + math.pi / 2)

        base_x2 = self.center[0] + base_width * math.cos(angle - math.pi / 2)
        base_y2 = self.center[1] - base_width * math.sin(angle - math.pi / 2)

        self.canvas.coords(self.needle, tip_x, tip_y, base_x1, base_y1, base_x2, base_y2)
        self.canvas.itemconfig(self.value_text, text=f"{self.current_value:05.2f}")

class FullGaugeApp(tk.Tk):
    def __init__(self, damping="inactive", size="medium"):
        super().__init__()
        self.title("270-Degree Gauge UI")
        window_size = {"small": 270, "medium": 370, "big": 440}
        dim = window_size.get(size, 370)
        self.geometry(f"{dim}x{dim}")
        self.configure(bg="gray")

        self.gauge = Meter270(self, size=size, damp=damping, needle_fill="olive", style="rect",
                      red_start=80, red_end=100,
                      yellow_start=0, yellow_end=40,
                      green_start=40, green_end=80)
        self.gauge.pack(padx=35, pady=35)

        self.slider = tk.Scale(self, from_=0, to=100, orient="horizontal", command=self.update_needle)
        self.slider.pack(pady=10)

    def update_needle(self, value):
        self.gauge.set_value(int(value))

if __name__ == "__main__":
    app = FullGaugeApp(damping="active", size="medium")
    app.mainloop()
