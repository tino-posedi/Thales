"""
 ____                     ____                       
/\  _\                  /\  _\                     
\ \,\L\_\     __   __  __\ \,\L\_\     __     __     
 \/_\__ \   /'__\/\ \/\ \\/_\__ \   /'__\ /'_ \   
   /\ \L\ \/\  __/\ \ \_/ | /\ \L\ \/\  __//\ \L\ \  
   \ \____\ \____\\ \___/  \ \____\ \____\ \____ \ 
    \/_____/\/____/ \/__/    \/_____/\/____/\/___L\ \
                                              /\____/
                                              \_/__/ 
SevSeg.py
"""

import tkinter as tk
import time
import tkinter.font as tkFont

class SevSeg(tk.Canvas):
    def __init__(self, parent, unit="", led_r="off", led_g="off", display_bg="#0000ff", number_color="#ffff00", **kwargs):
        super().__init__(parent, width=180, height=80, bg="SystemButtonFace", relief="raised", bd=3)
        
        self.value = 0  
        self.unit = unit
        self.led_r = led_r
        self.led_g = led_g

        self.display_bg = display_bg
        self.number_color = number_color

        self.led_r_state = False
        self.led_g_state = False
        
        self.create_ui()
        self.update_leds()

    def create_ui(self):
        self.create_rounded_rectangle(10, 10, 110, 78, radius=25, fill=self.display_bg, outline="")

        self.text_id = self.create_text(60, 44, text="", font=("DSEG7 Classic", 34, "bold"), fill=self.number_color)
        self.update_display_text()

        self.create_text(150, 35, text=self.unit, font=("Arial", 19), fill="black")

        led_x = 170 
        led_y = 55 

        self.led_r_id = self.create_oval(125, 60, 140, 75, fill="black", outline="black")
        self.led_g_id = self.create_oval(160, 60, 175, 75, fill="black", outline="black")
        
        self.create_text(169, 12, text = "Thales", font = "Helvetica 7", fill = "gray")
        
    def set_value(self, new_value):
        """Set the value on the display, ensuring it is an integer."""
        if isinstance(new_value, int): 
            self.value = new_value
            self.update_display_text()
        else:
            print("Error: Value must be an integer.")  

    def update_display_text(self):
        length = len(str(self.value))  

        if length <= 2:
            size = 34
        elif length == 3:
            size = 32
        elif length == 4:
            size = 24
        else:
            size = 18

        font_obj = tkFont.Font(family="DSEG7 Classic", size=size, weight="bold")
        text_width = font_obj.measure(str(self.value))

        x_center = 10 + (185 - text_width) / 2
        y_center = 44 

        self.itemconfig(self.text_id, text=str(self.value), font=font_obj)
        self.coords(self.text_id, x_center, y_center)
    
    def create_rounded_rectangle(self, x1, y1, x2, y2, radius=25, **kwargs):
        points = [
            x1 + radius, y1,
            x2 - radius, y1,
            x2, y1,
            x2, y1 + radius,
            x2, y2 - radius,
            x2, y2,
            x2 - radius, y2,
            x1 + radius, y2,
            x1, y2,
            x1, y2 - radius,
            x1, y1 + radius,
            x1, y1,
        ]
        return self.create_polygon(points, smooth=True, splinesteps=76, **kwargs)

    def update_leds(self):
        red_color = '#FF0000' if self.led_r == "on" else '#600000'
        
        if self.led_r == "blink":
            red_color = '#600000' if self.led_r_state else '#FF0000'
 
        green_color = '#00FF00' if self.led_g == "on" else '#006000'
        
        if self.led_g == "blink":
            green_color = '#006000' if self.led_g_state else '#00FF00'

        self.itemconfig(self.led_r_id, fill=red_color)
        self.itemconfig(self.led_g_id, fill=green_color)

        if self.led_r == "blink":
            self.led_r_state = not self.led_r_state
        if self.led_g == "blink":
            self.led_g_state = not self.led_g_state

        if self.led_r == "blink" or self.led_g == "blink":
            self.after(700, self.update_leds)

    def blink_led(self, led_id, color):
        def toggle():
            current_color = self.itemcget(led_id, "fill")
            new_color = color if current_color == "black" else "black"
            self.itemconfig(led_id, fill=new_color)
            self.after(700, toggle)
        toggle()
        
    def led_r_on(self):
        self.led_r = "on"
        self.led_r_state = True
        self.update_leds()

    def led_r_off(self):
        self.led_r = "off"
        self.led_r_state = False
        self.update_leds()

    def led_r_blink(self):
        self.led_r = "blink"
        self.led_r_state = False
        self.update_leds()

    def led_g_on(self):
        self.led_g = "on"
        self.led_g_state = True
        self.update_leds()

    def led_g_off(self):
        self.led_g = "off"
        self.led_g_state = False
        self.update_leds()

    def led_g_blink(self):
        self.led_g = "blink"
        self.led_g_state = False
        self.update_leds()