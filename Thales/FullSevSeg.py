import tkinter as tk
import time
import tkinter.font as tkFont

class FullSevSeg(tk.Canvas):
    def __init__(self, parent, display_bg="#0000ff", number_color="#ffff00", **kwargs):
        super().__init__(parent, width=180, height=80, bg="SystemButtonFace", relief="raised", bd=3)
        
        self.value = 0 

        self.display_bg = display_bg
        self.number_color = number_color
        
        self.create_ui()

    def create_ui(self):
        self.create_rounded_rectangle(10, 10, 178, 78, radius=25, fill=self.display_bg, outline="")
        self.text_id = self.create_text(170, 44, text="", font=("DSEG7 Classic", 34, "bold"), fill=self.number_color)
        self.update_display_text()
        
    def set_value(self, new_value):
        if isinstance(new_value, (int, float)):
            self.value = new_value
            self.update_display_text()
        else:
            print("Error: Value must be an int or float.") 

    def update_display_text(self):
        display_text = str(self.value)

        if isinstance(self.value, float):
            display_text = f"{self.value:.2f}"
            
        size = 34

        font_obj = tkFont.Font(family="DSEG7 Classic", size=size, weight="bold")
        text_width = font_obj.measure(display_text)

        x_center = 80 + (185 - text_width) / 2
        y_center = 44  

        self.itemconfig(self.text_id, text=display_text, font=font_obj)
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

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Full 7-Segment Display")

    display = FullSevSeg(root, display_bg="#0000ff", number_color="#ffff00")
    display.pack(padx=20, pady=20)

    def update_val():
        for i in range(0, 50):
            val = i + 0.25 * i 
            display.set_value(val)
            root.update()
            time.sleep(0.3)

    root.after(1000, update_val)
    root.mainloop()
