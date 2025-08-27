import tkinter as tk
import math
import random

class Compass(tk.Frame):
    def __init__(self, parent, rect_style="roundrect", fill="#000079", outer_ring_fill="lime", inner_ring_fill="white",
                 course_fill ="lime", deviation_fill="yellow", arrow_course_fill = "red", arrow_deviation_fill = "red", **kwargs):
        super().__init__(parent, **kwargs)

        self.config(width=230, height=230)
        self.pack_propagate(False)

        outer_frame = tk.Frame(self, bg='SystemButtonFace', bd=3, relief="raised", width=230, height=230)
        outer_frame.pack(padx=0, pady=0)
        outer_frame.pack_propagate(False)

        self.canvas = tk.Canvas(outer_frame, width=230, height=230, bg="SystemButtonFace", highlightthickness=0)
        self.canvas.pack()

        self.center_x = 110
        self.center_y = 110
        self.radius = 90

        self.rect_style = rect_style
        self.fill = fill
        self.outer_ring_fill = outer_ring_fill
        self.inner_ring_fill = inner_ring_fill
        self.course_fill = course_fill
        self.deviation_fill = deviation_fill
        self.arrow_course_fill = arrow_course_fill
        self.arrow_deviation_fill = arrow_deviation_fill

        self.course = 0
        self.course_should = 0
        self.deviation = 0

        self.draw_all()

    def set_course_should(self, course):
        self.course_should = course % 360
        self.draw_all()

    def update_values(self, actual_course, deviation):
        self.course = actual_course % 360
        self.deviation = deviation
        self.draw_all()

    def draw_all(self):
        self.canvas.delete("all")
        self.draw_background()
        self.draw_triangles(self.course, self.deviation)
        self.draw_display()

    def draw_background(self):
        if self.rect_style == "roundrect":
            self.draw_rounded_rect(self.canvas, 10, 10, 210, 210, radius=15, fill=self.fill, outline=self.fill)
        elif self.rect_style == "rect":
            self.canvas.create_rectangle(10, 10, 210, 210, fill=self.fill, outline=self.fill)
        elif self.rect_style == "round":
            pass

        self.canvas.create_oval(self.center_x - self.radius, self.center_y - self.radius,
                                self.center_x + self.radius, self.center_y + self.radius,
                                fill=self.inner_ring_fill, outline=self.outer_ring_fill, width=10)

        self.canvas.create_text(self.center_x, self.center_y - 48, text="course", fill="black", font=("Arial", 9, "bold"))
        self.canvas.create_text(self.center_x, self.center_y + 48, text="deviation", fill="black", font=("Arial", 9, "bold"))

    def draw_rounded_rect(self, canvas, x1, y1, x2, y2, radius=20, **kwargs):
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
            x1, y1
        ]
        canvas.create_polygon(points, smooth=True, splinesteps=36, **kwargs)

    def draw_display(self):
        self.canvas.create_rectangle(self.center_x - 30, self.center_y - 35,
                                     self.center_x + 30, self.center_y - 15,
                                     fill="black")
        self.canvas.create_rectangle(self.center_x - 30, self.center_y + 15,
                                     self.center_x + 30, self.center_y + 35,
                                     fill="black")

        self.canvas.create_text(self.center_x, self.center_y - 25,
                                text=f"{self.course_should:03}",
                                font=("DSEG7 Classic", 13, "bold"), fill=self.course_fill)
        self.canvas.create_text(self.center_x, self.center_y + 25,
                                text=f"{self.deviation:03}",
                                font=("DSEG7 Classic", 13, "bold"), fill=self.deviation_fill)

    def rotated_triangle(self, angle_deg, offset_radius, up=True):
        angle_rad = math.radians(angle_deg)

        tip = (0, -offset_radius if up else offset_radius)
        base_left = (-10, -offset_radius + 20 if up else offset_radius - 20)
        base_right = (10, -offset_radius + 20 if up else offset_radius - 20)

        def rotate_point(x, y):
            xr = x * math.cos(angle_rad) - y * math.sin(angle_rad)
            yr = x * math.sin(angle_rad) + y * math.cos(angle_rad)
            return (self.center_x + xr, self.center_y + yr)

        return [*rotate_point(*tip), *rotate_point(*base_left), *rotate_point(*base_right)]

    def draw_triangles(self, course_deg, deviation_deg):
        top_triangle = self.rotated_triangle(course_deg, self.radius - 8, up=True)
        self.canvas.create_polygon(top_triangle, fill=self.arrow_course_fill, outline="black")

        dev_angle = (course_deg + deviation_deg) % 360
        bottom_triangle = self.rotated_triangle(dev_angle, self.radius - 150, up=True)
        self.canvas.create_polygon(bottom_triangle, fill=self.arrow_deviation_fill, outline="black")

def main():
    root = tk.Tk()
    root.title("Embedded Compass Widget")

    compass = Compass(root, rect_style="round")  
    compass.pack(padx=10, pady=10)

    def simulate():
        actual_course = random.randint(0, 359)
        should_course = 120
        deviation = (actual_course - should_course + 540) % 360 - 180

        compass.set_course_should(should_course)
        compass.update_values(actual_course, deviation)

        root.after(2000, simulate)

    root.after(1000, simulate)
    root.mainloop()

if __name__ == "__main__":
    main()
