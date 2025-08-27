import tkinter as tk
import time
import tkinter.font as tkFont

class DigiTime(tk.Canvas):
    def __init__(self, parent, display_bg="#0000ff", number_color="#ffff00", **kwargs):
        super().__init__(parent, width=140, height=70, bg="SystemButtonFace", relief="raised", bd=3)

        self.colon_visible = True  
        self.display_bg = display_bg
        self.number_color = number_color

        self.create_ui()
        self.update_time()

    def create_ui(self):
        self.create_rounded_rectangle(10, 10, 140, 70, radius=20, fill=self.display_bg, outline="")

        self.text_id = self.create_text(70, 44, text="", font=("DSEG7 Classic", 28, "bold"), fill=self.number_color)
        self.update_display_text()

    def update_display_text(self):
        display_value = time.strftime("%H:%M")
        if not self.colon_visible:
            display_value = display_value.replace(":", " ")

        font_obj = tkFont.Font(family="DSEG7 Classic", size=26, weight="bold")
        x_center = 74
        y_center = 40

        self.itemconfig(self.text_id, text=display_value, font=font_obj)
        self.coords(self.text_id, x_center, y_center)

    def update_time(self):
        self.colon_visible = not self.colon_visible 
        self.update_display_text()
        self.after(1000, self.update_time)  

    def create_rounded_rectangle(self, x1, y1, x2, y2, radius=20, **kwargs):
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

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Digital Clock")

    sev = DigiTime(root)
    sev.pack(padx=10, pady=10)

    root.mainloop()