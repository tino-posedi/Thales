import tkinter as tk
from tkinter import Canvas
import random

class MeterPanelV(tk.Frame):
    SIZE_MAP = {
        'small': (80, 350),
        'medium': (130, 575),
        'big': (180, 800)
    }

    def __init__(self, master=None, value=0.00, bar_type='blocks',
                 cap_top="Text1", cap_down="Text2", fill="#000079", peak='inactive',
                 size='small', style="roundrect",
                 red_start=66, red_end=100, yellow_start=33, yellow_end=66,
                 green_start=0, green_end=33):
        super().__init__(master)
        self.cap_top = cap_top
        self.cap_down = cap_down
        self.master = master
        self.value = value
        self.fill = fill
        self.led_r_state = 'off'
        self.led_g_state = 'off'
        self.led_r_active = False
        self.led_g_active = False
        self.bar_type = bar_type
        self.peak_active = peak == 'active'
        self.peak_value = value
        self.style = style

        self.red_start = red_start
        self.red_end = red_end
        self.yellow_start = yellow_start
        self.yellow_end = yellow_end
        self.green_start = green_start
        self.green_end = green_end
        
        self.u_width, self.u_height = self.SIZE_MAP.get(size, self.SIZE_MAP['small'])
        self.x_factor = self.u_width / 80
        self.y_factor = self.u_height / 350
        
        if self.bar_type == 'scala':
            self.scale_x = 80 * self.x_factor 
        else:
            self.scale_x = 40 * self.x_factor 
            
        self.pointer_offset_x = -25 * self.x_factor if self.bar_type == 'scala' else 0
    
        self.pack()
        self.create_widgets()
        self.blink()

    def create_widgets(self):
            bevel = tk.Frame(self, bg='SystemButtonFace', bd=3, relief='raised')
            bevel.pack(padx=0, pady=0)

            self.canvas = Canvas(bevel, width=self.u_width, height=self.u_height,
                                 bg='SystemButtonFace', highlightthickness=0)
            self.canvas.pack()

            self.radius = 10 if self.style == "roundrect" else 0
            self.draw_rounded_rect(10, 35, 70, 325, radius=self.radius, fill=self.fill)

            self.canvas.create_rectangle(
                10 * self.x_factor, 5 * self.y_factor, 70 * self.x_factor, 30 * self.y_factor,
                fill='black', outline='white'
            )
            self.display_text = self.canvas.create_text(
                40 * self.x_factor, 18 * self.y_factor,
                text=f"{self.value:.2f}", fill='cyan', font=('DSEG7 Classic', int(12 * self.y_factor), "bold")
            )

            self.canvas.create_text(40 * self.x_factor, 45 * self.y_factor, text=self.cap_top,
                                    fill='white', font=('Arial', int(10 * self.y_factor)))
            self.canvas.create_text(40 * self.x_factor, 313 * self.y_factor, text=self.cap_down,
                                    fill='white', font=('Arial', int(10 * self.y_factor)))

            self.led_g = self.canvas.create_oval(
                10 * self.x_factor, 332 * self.y_factor,
                20 * self.x_factor, 342 * self.y_factor,
                fill='#00FF00' if self.led_g_active else '#006000', outline='black')

            self.led_r = self.canvas.create_oval(
                60 * self.x_factor, 332 * self.y_factor,
                70 * self.x_factor, 342 * self.y_factor,
                fill='#FF0000' if self.led_r_active else '#600000', outline='black')

            self.draw_flood_bar()
            self.draw_scale()
            self.draw_pointer()
            if self.peak_active:
                self.draw_peak_pointer()

    def draw_rounded_rect(self, x1, y1, x2, y2, radius=80, **kwargs):
        f = self.x_factor
        points = [
            (x1 + radius) * f, y1 * self.y_factor,
            (x2 - radius) * f, y1 * self.y_factor,
            x2 * f, y1 * self.y_factor,
            x2 * f, (y1 + radius) * self.y_factor,
            x2 * f, (y2 - radius) * self.y_factor,
            x2 * f, y2 * self.y_factor,
            (x2 - radius) * f, y2 * self.y_factor,
            (x1 + radius) * f, y2 * self.y_factor,
            x1 * f, y2 * self.y_factor,
            x1 * f, (y2 - radius) * self.y_factor,
            x1 * f, (y1 + radius) * self.y_factor,
            x1 * f, y1 * self.y_factor
        ]
        self.canvas.create_polygon(points, smooth=True, **kwargs)

    def draw_scale(self):
        for i in range(0, 101, 10):
            y = self.value_to_y(i)
            self.canvas.create_line(self.scale_x, y, self.scale_x + 5, y,
                                    fill='white', width=1)
            self.canvas.create_text(self.scale_x + 15, y, text=str(i),
                                    fill='white', font=('Arial', int(9 * self.y_factor)))
        self.canvas.create_line(self.scale_x, self.value_to_y(0),
                                self.scale_x, self.value_to_y(100),
                                fill='white', width=1)
        self.canvas.create_text(40 * self.x_factor, 338 * self.y_factor,
                                text="Thales", font=("Helvetica", int(7 * self.y_factor)), fill="gray")

    def draw_flood_bar(self):
        self.canvas.delete("flood_bar")
        bottom_y = self.value_to_y(0)
        bar_left = 20 * self.x_factor
        bar_right = 35 * self.x_factor

        def draw_zone(start, end, color):
            y1 = self.value_to_y(min(start, end))
            y2 = self.value_to_y(max(start, end))
            self.canvas.create_rectangle(bar_left, y2, bar_right, y1, fill=color, outline='grey', tags="flood_bar")
        
        if self.bar_type == 'scala':
                self.scale_x = 15 * self.x_factor
                return  
        
        if self.bar_type == 'flow':
            zones = [
                (self.green_start, self.green_end, '#39ff14', 'darkgreen'),
                (self.yellow_start, self.yellow_end, 'yellow', '#9B870C'),
                (self.red_start, self.red_end, 'red', 'darkred')
            ]

            for start, end, active_color, inactive_color in zones:
                y_start = self.value_to_y(start)
                y_end = self.value_to_y(end)

                self.canvas.create_rectangle(bar_left, y_end, bar_right, y_start,
                                             fill=inactive_color, outline='grey', tags="flood_bar")

                if self.value > start:
                    active_top = max(start, min(end, self.value))
                    y_active_top = self.value_to_y(active_top)
                    self.canvas.create_rectangle(bar_left, y_active_top, bar_right, y_start,
                                                 fill=active_color, outline='grey', tags="flood_bar")

        else:
            total_blocks = 24
            block_height = 10 * self.y_factor
            block_value = 100 / total_blocks
            y = bottom_y

            for i in range(total_blocks):
                current_value = i * block_value
                if current_value < self.value:
                    if self.green_start <= current_value < self.green_end:
                        color = '#39ff14'
                    elif self.yellow_start <= current_value < self.yellow_end:
                        color = 'yellow'
                    elif self.red_start <= current_value <= self.red_end:
                        color = 'red'
                    else:
                        color = 'gray'
                else:
                    if self.green_start <= current_value < self.green_end:
                        color = 'darkgreen'
                    elif self.yellow_start <= current_value < self.yellow_end:
                        color = '#9B870C'
                    elif self.red_start <= current_value <= self.red_end:
                        color = 'darkred'
                    else:
                        color = 'gray'
                self.canvas.create_rectangle(bar_left, y - block_height, bar_right, y,
                                             fill=color, outline='grey', tags="flood_bar")
                y -= block_height

    def draw_pointer(self):
        self.canvas.delete("pointer")
        y = self.value_to_y(self.value)
        offset = self.pointer_offset_x
        self.canvas.create_polygon(
            (49 + offset) * self.x_factor, y,
            (36 + offset) * self.x_factor, y - 5 * self.y_factor,
            (36 + offset) * self.x_factor, y + 5 * self.y_factor,
            fill='red', outline='black', tags="pointer"
        )

    def draw_peak_pointer(self):
        self.canvas.delete("peak_pointer")
        y = self.value_to_y(self.peak_value)
        offset = self.pointer_offset_x
        self.canvas.create_polygon(
            (49 + offset) * self.x_factor, y,
            (36 + offset) * self.x_factor, y - 5 * self.y_factor,
            (36 + offset) * self.x_factor, y + 5 * self.y_factor,
            fill='yellow', outline='black', tags="peak_pointer"
        )

    def set_value(self, value):
        self.value = max(0, min(100, value))
        if self.peak_active and value > self.peak_value:
            self.peak_value = value
        self.draw_flood_bar()
        self.draw_pointer()
        if self.peak_active:
            self.draw_peak_pointer()

        text_str = f"{self.value:.2f}"
        text_length = len(text_str)

        x_pos = 40 * self.x_factor - (text_length - 5) * 3 * self.x_factor
        self.canvas.coords(self.display_text, x_pos, 18 * self.y_factor)
        self.canvas.itemconfig(self.display_text, text=text_str)


    def reset_peak(self):
        self.peak_value = self.value
        if self.peak_active:
            self.draw_peak_pointer()

    def value_to_y(self, value):
        top = 60 * self.y_factor
        bottom = 299 * self.y_factor
        scale_height = bottom - top
        return bottom - (value / 100) * scale_height

    def blink(self):
            if self.led_r_state == 'blink':
                self.led_r_active = not self.led_r_active
                self.canvas.itemconfig(self.led_r, fill='#FF0000' if self.led_r_active else '#8B0000')

            if self.led_g_state == 'blink':
                self.led_g_active = not self.led_g_active
                self.canvas.itemconfig(self.led_g, fill='#00FF00' if self.led_g_active else '#006400')

            self.after(700, self.blink)
    
    def led_g_on(self):
        self.led_g_state = 'on'
        self.led_g_active = True
        self.canvas.itemconfig(self.led_g, fill='#00FF00')

    def led_g_off(self):
        self.led_g_state = 'off'
        self.led_g_active = False
        self.canvas.itemconfig(self.led_g, fill='#006400')
        
    def led_g_blink(self):
        self.led_g_state = 'blink'

    def led_r_on(self):
        self.led_r_state = 'on'
        self.led_r_active = True
        self.canvas.itemconfig(self.led_r, fill='#FF0000')

    def led_r_off(self):
        self.led_r_state = 'off'
        self.led_r_active = False
        self.canvas.itemconfig(self.led_r, fill='#8B0000')

    def led_r_blink(self):
        self.led_r_state = 'blink'
            
if __name__ == "__main__":
    root = tk.Tk()
    root.title("Animated Meter Panel")

    app = MeterPanelV(root, value=0, bar_type='blocks', peak='inactive',
                      red_start=0, red_end=25, cap_top="Strom", cap_down="Amp",
                      yellow_start=70, yellow_end=100,
                      green_start=25, green_end=70, size='small')
    app.pack()

    def set_random_value():
        value = random.uniform(15, 90)
        app.set_value(value)

        if value > 25:
            app.led_g_on()
            app.led_r_blink()
            root.configure(bg = "green")
            
        else:
            app.led_r_on()
            print("Stromaufnahme zu klein!")
            root.configure(bg = "red")

        if value > 60:
            app.led_g_off()
            app.led_r_on()
            print("Stromaufnahme zu hoch!")
            root.configure(bg="red")
    root.after(2000, set_random_value)  
    root.geometry("200x400")
    root.mainloop()