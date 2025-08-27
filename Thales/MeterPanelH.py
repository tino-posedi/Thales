import tkinter as tk
import threading
import time

class MeterPanelH(tk.Frame):
    def __init__(self, master=None, start_value=0, end_value=50,
                 fill="#000079", scale_fill="white", number_color="white",
                 style="roundrect", **kwargs):
        super().__init__(master, bg='systemButtonFace', bd=3, relief='raised', **kwargs)
        self.canvas = tk.Canvas(self, width=460, height=100, bg='systemButtonFace', highlightthickness=0)
        self.canvas.pack()

        self.start = start_value
        self.end = end_value
        self.needle_value = self.start
        self.style = style
        
        self.fill = fill
        self.scale_fill = scale_fill
        self.number_color = number_color
        
        self.scale_x_offset = 30

        self.led_r_state = 'off'
        self.led_g_state = 'off'
        self.led_r_active = False
        self.led_g_active = False
        self._blink = True

        self.draw_meter()
        self.update_leds()

    def draw_meter(self):
        self.canvas.delete("all")
        width = int(440)
        height = int(self.canvas['height'])
        radius = 15 if self.style == "roundrect" else 0

        self.canvas.create_arc(10, 10, 10 + 2 * radius, 10 + 2 * radius, start=90, extent=90, fill=self.fill, outline=self.fill)
        self.canvas.create_arc(width - 10 - 2 * radius, 10, width - 10, 10 + 2 * radius, start=0, extent=90, fill=self.fill, outline=self.fill)
        self.canvas.create_arc(10, height - 10 - 2 * radius, 10 + 2 * radius, height - 10, start=180, extent=90, fill=self.fill, outline=self.fill)
        self.canvas.create_arc(width - 10 - 2 * radius, height - 10 - 2 * radius, width - 10, height - 10, start=270, extent=90, fill=self.fill, outline=self.fill)

        self.canvas.create_rectangle(10 + radius, 10, width - 10 - radius, height - 10, fill=self.fill, outline=self.fill)
        self.canvas.create_rectangle(10, 10 + radius, width - 10, height - 10 - radius, fill=self.fill, outline=self.fill)

        base_y = height - 40
        scale_start_x = self.scale_x_offset
        scale_end_x = width - self.scale_x_offset
        scale_width = scale_end_x - scale_start_x

        self.canvas.create_line(scale_start_x, base_y, scale_end_x, base_y, fill=self.scale_fill)

        self.tick_positions = []
        steps = 6
        finer_ticks = 5

        for i in range(steps):
            val = self.start + i * ((self.end - self.start) / (steps - 1))
            x = scale_start_x + i * (scale_width / (steps - 1))
            self.tick_positions.append((val, x))
            self.canvas.create_line(x, base_y, x, base_y - 10, fill=self.scale_fill)
            self.canvas.create_text(x, height - 55, text=str(int(val)), fill=self.number_color, font=('Arial', 8))

            if i < steps - 1:
                major_val = self.start + i * ((self.end - self.start) / (steps - 1))
                next_major_val = self.start + (i + 1) * ((self.end - self.start) / (steps - 1))
                for j in range(1, finer_ticks):
                    minor_val = major_val + (next_major_val - major_val) * (j / finer_ticks)
                    minor_x = scale_start_x + (minor_val - self.start) / (self.end - self.start) * scale_width
                    self.canvas.create_line(minor_x, base_y, minor_x, base_y - 5, fill=self.scale_fill)

        led_x_offset = width
        self.led_r_obj = self.canvas.create_oval(led_x_offset, 25, led_x_offset + 10, 35,
                                                 fill='#FF0000', outline="black")
        self.led_g_obj = self.canvas.create_oval(led_x_offset, 65, led_x_offset + 10, 75,
                                                 fill='#006000', outline="black")

        self.needle = self.canvas.create_polygon(self.needle_coords(self.needle_value),
                                                 fill='red', outline="black")
        
        self.canvas.create_text(444, 7, text="Thales", font="Helvetica 7", fill="gray")

    def needle_coords(self, value):
        width = int(self.canvas['width'])
        height = int(95)

        value = max(self.start, min(self.end, value))

        for i in range(len(self.tick_positions) - 1):
            v1, x1 = self.tick_positions[i]
            v2, x2 = self.tick_positions[i + 1]
            if v1 <= value <= v2:
                ratio = (value - v1) / (v2 - v1)
                x = x1 + ratio * (x2 - x1)
                break
        else:
            x = self.tick_positions[-1][1]

        return [x, height - 45, x - 5, height - 25, x + 5, height - 25]

    def set_value(self, value):
        self.needle_value = value
        self.canvas.coords(self.needle, self.needle_coords(value))

    def led_g_on(self):
        self.led_g_state = 'on'
        self.led_g_active = True
        self.canvas.itemconfig(self.led_g_obj, fill='#00FF00')

    def led_g_off(self):
        self.led_g_state = 'off'
        self.led_g_active = False
        self.canvas.itemconfig(self.led_g_obj, fill='#006000')

    def led_g_blink(self):
        self.led_g_state = 'blink'
        threading.Thread(target=self._blink_led,
                         args=(self.led_g_obj, '#00FF00', '#006000', lambda: self.led_g_state == 'blink'),
                         daemon=True).start()

    def led_r_on(self):
        self.led_r_state = 'on'
        self.led_r_active = True
        self.canvas.itemconfig(self.led_r_obj, fill='#FF0000')

    def led_r_off(self):
        self.led_r_state = 'off'
        self.led_r_active = False
        self.canvas.itemconfig(self.led_r_obj, fill='#600000')

    def led_r_blink(self):
        self.led_r_state = 'blink'
        threading.Thread(target=self._blink_led,
                         args=(self.led_r_obj, '#FF0000', '#600000', lambda: self.led_r_state == 'blink'),
                         daemon=True).start()

    def _blink_led(self, tag, on_color, off_color, condition):
        while condition():
            self.canvas.itemconfig(tag, fill=on_color)
            time.sleep(0.7)
            self.canvas.itemconfig(tag, fill=off_color)
            time.sleep(0.7)

    def update_leds(self):
        if self.led_g_state == 'on':
            self.led_g_on()
        elif self.led_g_state == 'off':
            self.led_g_off()
        elif self.led_g_state == 'blink':
            self.led_g_blink()

        if self.led_r_state == 'on':
            self.led_r_on()
        elif self.led_r_state == 'off':
            self.led_r_off()
        elif self.led_r_state == 'blink':
            self.led_r_blink()