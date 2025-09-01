import tkinter as tk

class CurveSynth(tk.Frame):
    def __init__(self, master=None, plot_name="Curve Synth", cap_top="Gain", cap_down="Time",
                 y_start=0, y_end=100, **kwargs):
        super().__init__(master, bd=3, relief="raised", **kwargs)
        self.canvas_width = 400
        self.canvas_height = 270
        self.plot_width = 320
        self.plot_height = 180
        self.plot_name = plot_name
        self.y_start = y_start
        self.y_end = y_end
        
        self.cap_top = cap_top
        self.cap_down = cap_down

        self.plot_origin_x = 50
        self.plot_origin_y = 40
        self.plot_end_x = self.plot_origin_x + self.plot_width
        self.plot_end_y = self.plot_origin_y + self.plot_height

        self.canvas = tk.Canvas(self, width=self.canvas_width, height=self.canvas_height,
                                bg="SystemButtonFace", highlightthickness=0)
        self.canvas.pack()

        self.curves = {
            1: {"color": "red", "points": [(10,20),(20,10),(30,40),(60,35),(80,30)]},
            2: {"color": "blue", "points": [(10,10),(30,20),(50,25),(70,30),(90,20)]},
            3: {"color": "magenta", "points": [(10,40),(20,50),(40,80),(60,90),(90,45)]},
            4: {"color": "green", "points": [(10,50),(30,60),(50,70),(70,80),(90,80)]},
        }

        self.point_items = {}   
        self.curve_items = {}

        self._draw_ui()

        self.drag_data = {"x":0, "y":0, "item":None}
        self.canvas.tag_bind("point", "<ButtonPress-1>", self.on_point_press)
        self.canvas.tag_bind("point", "<ButtonRelease-1>", self.on_point_release)
        self.canvas.tag_bind("point", "<B1-Motion>", self.on_point_motion)

    def data_to_canvas(self, x, y):
        X = self.plot_origin_x + (x/100) * self.plot_width
        Y = self.plot_end_y - ((y - self.y_start) / (self.y_end - self.y_start)) * self.plot_height
        return X, Y

    def canvas_to_data(self, X, Y):
        x = (X - self.plot_origin_x) / self.plot_width * 100
        y = self.y_start + (self.plot_end_y - Y) / self.plot_height * (self.y_end - self.y_start)
        return x, y

    def _draw_ui(self):
        self.canvas.delete("all")
        self._draw_axes()
        self._draw_title()
        self._draw_labels()
        self._draw_curves()
        self._draw_channel_labels()

    def _draw_axes(self):
        self.canvas.create_rectangle(self.plot_origin_x, self.plot_origin_y,
                                     self.plot_end_x, self.plot_end_y,
                                     fill="white", outline="black")

        step = (self.y_end - self.y_start) / 10
        for i in range(11):
            y_val = self.y_end - i * step
            y = self.plot_origin_y + i * (self.plot_height / 10)
            self.canvas.create_line(self.plot_origin_x, y, self.plot_end_x, y, fill="lightgray")
            self.canvas.create_text(self.plot_origin_x - 10, y, text=str(int(y_val)), anchor="e", font=("Arial", 8))

        for i in range(11):
            x_val = i * 10
            x = self.plot_origin_x + i * (self.plot_width / 10)
            self.canvas.create_line(x, self.plot_origin_y, x, self.plot_end_y, fill="lightgray")
            self.canvas.create_text(x, self.plot_end_y + 12, text=str(x_val), anchor="n", font=("Arial", 8))

        self.canvas.create_line(self.plot_origin_x, self.plot_origin_y,
                                self.plot_origin_x, self.plot_end_y)
        self.canvas.create_line(self.plot_origin_x, self.plot_end_y,
                                self.plot_end_x, self.plot_end_y)

    def _draw_title(self):
        self.canvas.create_rectangle(self.canvas_width // 2 - 50, 5,
                                     self.canvas_width // 2 + 50, 25,
                                     fill="black")
        self.canvas.create_text(self.canvas_width // 2, 15, text=self.plot_name,
                                fill="lime", font=("Arial", 10, "bold"))

    def _draw_labels(self):
        self.canvas.create_text(5, 5, text=self.cap_top if hasattr(self, "cap_top") else "",
                                anchor="nw", font=("Arial", 8, "bold"))
        self.canvas.create_text(self.canvas_width - 5, 5, text="Thales", anchor="ne",
                                font=("Arial", 8), fill="gray")
        self.canvas.create_text(self.plot_end_x + 22, self.plot_end_y + 33,
                                text=self.cap_down if hasattr(self, "cap_down") else "",
                                anchor="ne", font=("Arial", 8, "bold"))

    def _draw_curves(self):
        for ch, data in self.curves.items():
            color = data["color"]
            points = [self.data_to_canvas(x, y) for x, y in data["points"]]

            if ch in self.curve_items:
                self.canvas.coords(self.curve_items[ch], *sum(points, ()))
            else:
                self.curve_items[ch] = self.canvas.create_line(
                    *sum(points, ()), smooth=False, width=1, fill=color
                )

            for i, (X, Y) in enumerate(points):
                exists = any(ch == self.point_items[item][0] and i == self.point_items[item][1]
                             for item in self.point_items)
                if not exists:
                    rect_size = 3
                    item = self.canvas.create_rectangle(
                        X-rect_size, Y-rect_size, X+rect_size, Y+rect_size,
                        fill=color, outline="black", tags="point"
                    )
                    self.point_items[item] = (ch, i)


    def _draw_channel_labels(self):
        tags = [("Chan 1              ", "red"), ("Chan 2              ", "blue"),
                ("Chan 3              ", "magenta"), ("Chan 4              ", "green")]
        
        spacing = 80
        y = self.canvas_height - 20

        if hasattr(self, "channel_labels"):
            for lbl in self.channel_labels:
                lbl.destroy()
        self.channel_labels = []

        for i, (name, color) in enumerate(tags):
            x = 50 - self.plot_origin_x + i * spacing
            lbl = tk.Label(self.canvas, text=name, fg=color, font=("Arial", 8),
                           relief="sunken", bd=2)
            lbl.place(x=x, y=y)
            self.channel_labels.append(lbl)

    def on_point_press(self, event):
        self.drag_data["item"] = self.canvas.find_closest(event.x, event.y)[0]
        self.drag_data["x"] = event.x
        self.drag_data["y"] = event.y

    def on_point_release(self, event):
        self.drag_data["item"] = None
        
    def clamp_point(self, x, y):
        x = max(0, min(100, x))
        y = max(self.y_start, min(self.y_end, y)) 
        return x, y
    
    def on_point_motion(self, event):
        item = self.drag_data["item"]
        if item not in self.point_items:
            return

        ch, idx = self.point_items[item]

        x, y = self.canvas_to_data(event.x, event.y)
        x = max(0, min(100, x))
        y = max(self.y_start, min(self.y_end, y))
        self.curves[ch]["points"][idx] = (x, y)

        X, Y = self.data_to_canvas(x, y)
        rect_size = 3
        self.canvas.coords(item, X-rect_size, Y-rect_size, X+rect_size, Y+rect_size)

        points = [self.data_to_canvas(px, py) for px, py in self.curves[ch]["points"]]
        self.canvas.coords(self.curve_items[ch], *sum(points, ()))

    def return_curve_points(self, *, ch):
        if ch in self.curves:
            return [(round(x, 2), round(y, 2)) for x, y in self.curves[ch]["points"]]
        return []
    
    def return_single_point(self, *, ch, point):
        if ch in self.curves:
            points = self.curves[ch]["points"]
            if 0 <= point < len(points):
                x, y = points[point]
                return round(x, 2), round(y, 2)
        return None
    
def main():
    root = tk.Tk()
    root.title("Curve Editor")

    plot = CurveSynth(root, plot_name="Curve Synth", cap_top="Gain", cap_down="Zeit")
    plot.pack(padx=10, pady=10)
    
    def getdata():
        # points_ch1 = plot.return_curve_points(ch=1)
        # print(points_ch1)
        
        point = plot.return_single_point(ch=2, point=3)
        print(point)  
    
    button_get = tk.Button(root, text = "getval", command = getdata)
    button_get.pack()

    root.mainloop()


if __name__ == "__main__":
    main()
