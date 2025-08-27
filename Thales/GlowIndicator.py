import tkinter as tk

class GlowIndicator(tk.Frame):
    def __init__(self, master=None, color='green', text='', text_orientation='right', width=102, height=40, **kwargs):
        super().__init__(master, width=width, height=height, **kwargs)
        self.color = color.lower()
        self.text = text
        self.text_orientation = text_orientation.lower()
        self.led_on = False

        self.canvas = tk.Canvas(self, width=width, height=height, highlightthickness=0)
        self.canvas.pack(fill='both', expand=True)

        self._draw()

    def _draw(self):
            self.canvas.delete("all")

            led_size = 10
            padding = 10
            canvas_height = int(self.canvas['height'])

            if self.text_orientation == 'right':
                led_x1 = padding
                led_y1 = (canvas_height - led_size) // 2
                led_x2 = led_x1 + led_size
                led_y2 = led_y1 + led_size

                text_x = led_x2 + 5
                text_y = canvas_height // 2
                text_anchor = 'w'
            else:
                text_char_width = 7 
                text_width = len(self.text) * text_char_width

                text_x = padding
                text_y = canvas_height // 2
                text_anchor = 'w'

                led_x1 = text_x + text_width + 5
                led_y1 = (canvas_height - led_size) // 2
                led_x2 = led_x1 + led_size
                led_y2 = led_y1 + led_size

            fill_color = self._get_fill_color()

            self.led = self.canvas.create_oval(led_x1, led_y1, led_x2, led_y2, fill=fill_color, outline='black')
            self.text_item = self.canvas.create_text(text_x, text_y, text=self.text, anchor=text_anchor, font=("Arial", 12))

    def _get_fill_color(self):
        if self.color == 'green':
            return '#00FF00' if self.led_on else '#006000'
        elif self.color == 'red':
            return '#FF0000' if self.led_on else '#600000'
        else:
            return '#000000'

    def set_led_on(self):
        self.led_on = True
        self.canvas.itemconfig(self.led, fill=self._get_fill_color())
        return self.led_on

    def set_led_off(self):
        self.led_on = False
        self.canvas.itemconfig(self.led, fill=self._get_fill_color())
        return self.led_on

    def get_led_state(self):
        return self.led_on

    def toggle(self):
        self.led_on = not self.led_on
        self.canvas.itemconfig(self.led, fill=self._get_fill_color())
        return self.led_on

    def update_text(self, new_text):
        self.text = new_text
        self.canvas.itemconfig(self.text_item, text=new_text)

    def update_color(self, new_color):
        self.color = new_color.lower()
        self.canvas.itemconfig(self.led, fill=self._get_fill_color())


if __name__ == '__main__':
        root = tk.Tk()
        root.geometry("300x150")

        led1 = GlowIndicator(root, color='green', text='Power', text_orientation='right')
        led1.pack(pady=10)

        led2 = GlowIndicator(root, color='red', text='Error', text_orientation='left')
        led2.pack(pady=10)

        def turn_leds_on():
            led1.set_led_on()
            led2.set_led_on()
            root.after(1000, turn_leds_off)

        def turn_leds_off():
            led1.set_led_off()
            led2.set_led_off()
            root.after(1000, turn_leds_on)

        root.after(1000, turn_leds_on)
        root.mainloop()
