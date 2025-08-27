import tkinter as tk

class StatusIndicator(tk.Frame):
    def __init__(self, master=None, caption="Status", led_color="red", width=50, **kwargs):
        super().__init__(master, **kwargs)
        self.caption = caption
        self.led_color = led_color.lower()
        self.led_state = False 
        self.width = width
        self.configure(bg="SystemButtonFace")

        self.button = tk.Frame(self, relief="raised", borderwidth=2, bg="SystemButtonFace")
        self.button.pack(padx=5, pady=5, fill="both")
        self.button.bind("<Button-1>", self.toggle_led)

        self.canvas = tk.Canvas(self.button, width=self.width, height=20, bg="SystemButtonFace", highlightthickness=0)
        self.canvas.pack(side="left", padx=(5, 2), pady=5)
        self.canvas.bind("<Button-1>", self.toggle_led)

        self.label = tk.Label(self.button, text=self.caption, bg="SystemButtonFace")
        self.label.pack(side="left", expand=True, anchor="center")
        self.label.bind("<Button-1>", self.toggle_led)

        self.draw_led()

    def draw_led(self):
        self.canvas.delete("all")
        red_color = '#8B0000'
        green_color = '#006400'

        if self.led_color == "red":
            if self.led_state:
                red_color = '#FF0000'
            self.canvas.create_oval(4, 4, 16, 16, fill=red_color, outline='black')
        elif self.led_color == "green":
            if self.led_state:
                green_color = '#00FF00'
            self.canvas.create_oval(4, 4, 16, 16, fill=green_color, outline='black')

        self.button.config(relief="sunken" if self.led_state else "raised")

    def toggle_led(self, event=None):
        self.led_state = not self.led_state
        self.draw_led()
    
    def return_value(self):
        return self.led_state

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Status Indicator Test")
    root.geometry("300x100")

    status = StatusIndicator(root, caption="Motor Freigabe    ", led_color="green", width=30)
    status.pack(pady=20)

    root.mainloop()