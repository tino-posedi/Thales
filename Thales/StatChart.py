import tkinter as tk
import math
import random

class StatChart(tk.Frame):
    def __init__(self, parent, caption="", use_3d="inactive"):
            super().__init__(parent, bd=3, relief="raised", bg="SystemButtonFace")
            self.use_3d = use_3d
            self.canvas = tk.Canvas(self, width=375, height=235, bg="SystemButtonFace", highlightthickness=0)
            self.canvas.pack(padx=10, pady=10)
            self.points = []
            self.band_width = 4
            self.caption = caption

            self.grid_left = 18
            self.grid_top = 28
            self.grid_width = 362
            self.grid_height = 195

            self.spacing_x = 35
            self.spacing_y = 35
            self.scale_y = 0.15
            
            self.thales_label = tk.Label(self, text="Thales", font=("Arial", 8), fg="gray", bg="SystemButtonFace")
            self.thales_label.place(x=393, y=0, anchor="ne")


            self.draw_background_grid()
            self.draw_title()
            
    def draw_title(self):
        self.canvas.create_text(187, 5, text=self.caption, fill="blue", font=("Arial", 8, "bold"))
    
    def draw_background_grid(self):
        ox, oy = self.grid_left, self.grid_top
        w, h = self.grid_width, self.grid_height
        skew = 10
        depth = 15

        if self.use_3d == "active":
            self.canvas.create_polygon(
                ox + skew, oy - depth,
                ox + w + skew, oy - depth,
                ox + w, oy,
                ox, oy,
                fill="SystemButtonFace", outline=""
            )
            self.canvas.create_polygon(
                ox, oy,
                ox, oy + h,
                ox + skew, oy + h - depth,
                ox + skew, oy - depth,
                fill="#e0e0e0", outline="black"
            )
            self.canvas.create_polygon(
                ox, oy + h,
                ox + w, oy + h,
                ox + w + skew, oy + h - depth,
                ox + skew, oy + h - depth,
                fill="#d0d0d0", outline="black"
            )

            for i in range(6):
                y = oy + i * self.spacing_y
                self.canvas.create_line(
                    ox, y,
                    ox + skew, y - depth,
                    fill="gray", dash=(2,)
                )
                self.canvas.create_line(
                    ox + w, y,
                    ox + w + skew, y - depth,
                    fill="gray", dash=(2,)
                )

            for i in range(25):
                x = ox + i * self.spacing_x
                self.canvas.create_line(
                    x, oy + h,
                    x + skew, oy + h - depth,
                    fill="gray", dash=(2,)
                )

            for i in range(25):
                x = ox + i * self.spacing_x + skew
                self.canvas.create_line(
                    x, oy - depth,
                    x, oy - depth + h,
                    fill="gray", dash=(2,)
                )

            for i in range(6):
                y = oy - depth + i * self.spacing_y
                self.canvas.create_line(
                    ox + skew, y,
                    ox + w + skew, y,
                    fill="gray", dash=(2,)
                )
        else:
            for i in range(25):
                x = ox + i * self.spacing_x
                self.canvas.create_line(x, oy, x, oy + h, fill="gray", dash=(2,))
            for i in range(6):
                y = oy + i * self.spacing_y
                self.canvas.create_line(ox, y, ox + w, y, fill="gray", dash=(2,))

            self.canvas.create_line(ox, oy, ox, oy + h, fill="black", width=1)
            self.canvas.create_line(ox, oy + h, ox + w, oy + h, fill="black", width=1)

        for i in range(6):
            y_val = 1100 - i * 50
            y = oy + i * self.spacing_y
            self.canvas.create_text(ox - 18, y, text=str(y_val), font=("Arial", 6), anchor="w")

        for i in range(25):
            x = ox + i * self.spacing_x
            self.canvas.create_text(x, oy + h + 8, text=str(i), font=("Arial", 6))

    def set_point(self, x_index, y_value):
        ox, oy = self.grid_left, self.grid_top
        x = ox + x_index * self.spacing_x
        y = oy + (1100 - y_value) * self.scale_y

        self.points.append((x, y))

        if len(self.points) > 1:
            x0, y0 = self.points[-2]
            x1, y1 = self.points[-1]
            color = "green" if y1 < y0 else "red"

            if self.use_3d:
                shadow_offset = 2
                self.canvas.create_line(
                    x0 + shadow_offset, y0 + shadow_offset,
                    x1 + shadow_offset, y1 + shadow_offset,
                    fill="gray", width=2
                )

                self.canvas.create_polygon(
                    x0, y0 - self.band_width,
                    x0, y0 + self.band_width,
                    x1, y1 + self.band_width,
                    x1, y1 - self.band_width,
                    fill=color, outline="black"
                )

                self.canvas.create_line(x0, y0, x1, y1, fill="black", width=1.5)
            else:
                self.canvas.create_polygon(
                    x0, y0 - self.band_width,
                    x0, y0 + self.band_width,
                    x1, y1 + self.band_width,
                    x1, y1 - self.band_width,
                    fill=color, outline=""
                )
                self.canvas.create_line(x0, y0, x1, y1, fill="black", width=1.5)

        self.canvas.create_oval(x-2, y-2, x+2, y+2, fill="black")

if __name__ == "__main__":
    root = tk.Tk()
    root.title("TChart Scaled Down")

    chart = StatChart(root, use_3d="active", caption="Graph Demo") 
    chart.pack(padx=10, pady=10)

    for i in range(95):
        y_val = 20 + int(10 * math.cos(i / 2.0)) + random.randint(550, 900)
        chart.set_point(i, y_val)

    root.mainloop()
