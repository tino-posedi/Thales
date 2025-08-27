import tkinter as tk
import random
import time

class xyGraph(tk.Frame):
    def __init__(self, master=None, plot_name="xyGraph", y_start=0, y_end=100, **kwargs):
        super().__init__(master, bd=3, relief='raised', **kwargs)
        self.canvas_width = 400
        self.canvas_height = 270
        self.plot_width = 320
        self.plot_height = 180
        self.plot_name = plot_name
        self.y_start = y_start
        self.y_end = y_end

        self.canvas = tk.Canvas(self, width=self.canvas_width, height=self.canvas_height,
                                bg="SystemButtonFace", highlightthickness=0)
        self.canvas.pack()

        self.plot_origin_x = 50
        self.plot_origin_y = 40
        self.plot_end_x = self.plot_origin_x + self.plot_width
        self.plot_end_y = self.plot_origin_y + self.plot_height

        self.data_channels = {1: [], 2: [], 3: [], 4: []}
        self.max_points = 100
        self.window_duration = 10
        self.start_time = None

        self.active_channels = set()
        self.channel_buttons = {}

        self._initialize_channel_buttons()
        self._draw_ui()

    def _initialize_channel_buttons(self):
        tags = [("Channel 1", "red"), ("Channel 2", "blue"),
                ("Channel 3", "magenta"), ("Channel 4", "green")]
        y = self.canvas_height - 15
        for i, (name, color) in enumerate(tags):
            label_x = self.plot_origin_x + i * (self.plot_width / 4) + (self.plot_width / 1000)
            button = tk.Button(self, text=name, fg=color, relief='raised',
                               font=("Arial", 8), command=lambda ch=i+1: self.toggle_channel(ch))
            button.place(x=label_x, y=240)
            self.channel_buttons[i+1] = button

    def set_data(self, channel, data):
        self.data_channels[channel] = data
        self._draw_ui()

    def start_buffered_plot(self, max_points=100, window_duration=10):
        self.data_channels = {1: [], 2: [], 3: [], 4: []}
        self.max_points = max_points
        self.window_duration = window_duration
        self.start_time = time.time()

    def add_buffer(self, value, channel=1):
        if self.start_time is None:
            self.start_buffered_plot()
        t = time.time() - self.start_time
        self.data_channels[channel].append((t, value))
        self.data_channels[channel] = [
            (x, y) for x, y in self.data_channels[channel] if x >= t - self.window_duration
        ]
        self.set_data(channel, self.data_channels[channel])

    def add_buffer_2(self, value): self.add_buffer(value, channel=2)
    def add_buffer_3(self, value): self.add_buffer(value, channel=3)
    def add_buffer_4(self, value): self.add_buffer(value, channel=4)

    def _draw_ui(self):
        self.canvas.delete("all")
        self._draw_axes()
        self._draw_title()
        self._draw_labels()
        self._draw_channels()
        for channel in self.active_channels:
            if self.data_channels[channel]:
                self._draw_plot_lines(channel)
                self._draw_peak_avg_lines(channel)
        self._update_channel_buttons()

    def _draw_peak_avg_lines(self, channel):
        data = self.data_channels[channel]
        if not data:
            return
        ys = [y for _, y in data]
        peak = max(ys)
        avg = sum(ys) / len(ys)
        color = self._get_channel_color(channel)

        peak_y = self.plot_origin_y + (1 - (peak - self.y_start) / (self.y_end - self.y_start)) * self.plot_height
        avg_y = self.plot_origin_y + (1 - (avg - self.y_start) / (self.y_end - self.y_start)) * self.plot_height

        self.canvas.create_line(self.plot_origin_x, peak_y, self.plot_end_x, peak_y, fill=color, dash=(4, 2))
        self.canvas.create_line(self.plot_origin_x, avg_y, self.plot_end_x, avg_y, fill=color, dash=(2, 4))

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

        if self.data_channels[1]:
            current_time = self.data_channels[1][-1][0]
            start_time = max(0, current_time - self.window_duration)
            for i in range(6):
                t_val = start_time + i * (self.window_duration / 5)
                x = self.plot_origin_x + i * (self.plot_width / 5)
                self.canvas.create_line(x, self.plot_origin_y, x, self.plot_end_y, fill="lightgray")
                self.canvas.create_text(x, self.plot_end_y + 5, text=f"{t_val:.1f}", anchor="n", font=("Arial", 8))

        self.canvas.create_line(self.plot_origin_x, self.plot_origin_y, self.plot_origin_x, self.plot_end_y)
        self.canvas.create_line(self.plot_origin_x, self.plot_end_y, self.plot_end_x, self.plot_end_y)

    def _draw_title(self):
        self.canvas.create_rectangle(self.canvas_width // 2 - 40, 5,
                                     self.canvas_width // 2 + 40, 25,
                                     fill='black')
        self.canvas.create_text(self.canvas_width // 2, 15, text=self.plot_name,
                                fill='lime', font=("Arial", 10, 'bold'))

    def _draw_labels(self):
        self.canvas.create_text(5, 5, text="", anchor="nw", font=("Arial", 8, 'bold'))
        self.canvas.create_text(self.canvas_width - 5, 5, text="Thales", anchor="ne", font=("Arial", 8), fill="gray")
        self.canvas.create_text(self.plot_end_x + 5, self.plot_end_y + 12, text="",
                                anchor="nw", font=("Arial", 8, 'bold'))

    def _draw_channels(self):
        tags = [("Channel 1", "red"), ("Channel 2", "blue"),
                ("Channel 3", "magenta"), ("Channel 4", "green")]
        for i, (name, color) in enumerate(tags):
            label_x = self.plot_origin_x + i * (self.plot_width / 4) + (self.plot_width / 8)

    def toggle_channel(self, channel):
        if channel in self.active_channels:
            self.active_channels.remove(channel)
        else:
            self.active_channels.add(channel)
        self._update_channel_buttons()

    def _update_channel_buttons(self):
        for button in self.channel_buttons.values():
            channel = int(button.cget("text").split(" ")[1])
            if channel in self.active_channels:
                button.config(relief="sunken")
            else:
                button.config(relief="raised")

    def _draw_plot_lines(self, channel):
        xs, ys = zip(*self.data_channels[channel])
        min_x = max(xs[0], xs[-1] - self.window_duration)
        max_x = xs[-1]
        min_y, max_y = self.y_start, self.y_end

        def map_x(x):
            return self.plot_origin_x + (x - min_x) / (max_x - min_x) * self.plot_width if max_x != min_x else self.plot_origin_x

        def map_y(y):
            return self.plot_origin_y + (1 - (y - min_y) / (max_y - min_y)) * self.plot_height

        for i in range(1, len(self.data_channels[channel])):
            x1, y1 = self.data_channels[channel][i - 1]
            x2, y2 = self.data_channels[channel][i]
            self.canvas.create_line(map_x(x1), map_y(y1), map_x(x2), map_y(y2),
                                    fill=self._get_channel_color(channel), width=2)

    def _get_channel_color(self, channel):
        return {1: "red", 2: "blue", 3: "magenta", 4: "green"}.get(channel, "black")

    def get_peak(self, channel):
        data = self.data_channels.get(channel, [])
        return float(max(y for _, y in data)) if data else 0.0

    def get_avg(self, channel):
        data = self.data_channels.get(channel, [])
        return float(sum(y for _, y in data) / len(data)) if data else 0.0

    def clear(self):
        self.data_channels = {1: [], 2: [], 3: [], 4: []}
        self.start_time = None
        self._draw_ui()

def main():
    root = tk.Tk()
    root.title("Multi-Channel XYPlot")

    plot = xyGraph(root, plot_name="Plot Demo", y_start=20, y_end=80)
    plot.pack(padx=10, pady=10)
    plot.start_buffered_plot(max_points=10, window_duration=10)

    def simulate_sensor_feed():
        value_1 = random.randint(30, 70)
        value_2 = random.randint(40, 60)
        value_3 = random.randint(45, 75)
        value_4 = random.randint(50, 65)

        plot.add_buffer(value_1, channel=1)
        plot.add_buffer_2(value_2)
        plot.add_buffer_3(value_3)
        plot.add_buffer_4(value_4)

        root.after(200, simulate_sensor_feed)

    simulate_sensor_feed()
    root.mainloop()

if __name__ == "__main__":
    main()
