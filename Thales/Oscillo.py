import tkinter as tk
import random
import time
import math

try:
    import pyvisa
except ImportError:
    pyvisa = None
    print("PyVISA not installed. Install it with `pip install pyvisa` to enable instrument support.")

class Oscillo(tk.Frame):
    def __init__(self, master=None, plot_name="Oscillo", **kwargs):
        super().__init__(master, bd=3, relief='raised', **kwargs)
        self.canvas_width = 290
        self.canvas_height = 270
        self.plot_width = 260
        self.plot_height = 220
        self.plot_name = plot_name

        self.canvas = tk.Canvas(self, width=self.canvas_width, height=self.canvas_height,
                                bg="SystemButtonFace", highlightthickness=0)
        self.canvas.pack()

        self.plot_origin_x = 15
        self.plot_origin_y = 31
        self.plot_end_x = self.plot_origin_x + self.plot_width
        self.plot_end_y = self.plot_origin_y + self.plot_height

        self.data_channels = {1: [], 2: [], 3: [], 4: []}  
        self.max_points = 100
        self.window_duration = 10 
        self.start_time = None

        self.active_channels = set()

        self._draw_ui()

    def set_data(self, channel, data):
        self.data_channels[channel] = data
        self._draw_ui()
        for ch in self.active_channels:
            if self.data_channels[ch]:
                self._draw_plot_lines(ch)

    def start_buffered_plot(self, max_points=100, window_duration=10):
        self.data_channels = {1: [], 2: [], 3: [], 4: []}
        self.max_points = max_points
        self.window_duration = window_duration
        self.start_time = time.time()
        self.active_channels = {1, 2, 3, 4}

    def add_buffer(self, value, channel=1):
        if self.start_time is None:
            self.start_buffered_plot()
        t = time.time() - self.start_time
        self.data_channels[channel].append((t, value))
        self.data_channels[channel] = [(x, y) for x, y in self.data_channels[channel] if x >= t - self.window_duration]

        self.set_data(channel, self.data_channels[channel])

    def add_buffer_2(self, value):
        self.add_buffer(value, channel=2)

    def add_buffer_3(self, value):
        self.add_buffer(value, channel=3)

    def add_buffer_4(self, value):
        self.add_buffer(value, channel=4)

    def feed_data(self, channel, value):
        """New method to feed arbitrary data to a channel."""
        self.add_buffer(value, channel)

    def _draw_ui(self):
        self.canvas.delete("all")
        self._draw_axes()
        self._draw_title()
        self._draw_labels()
        
        for ch in self.active_channels:
            if self.data_channels[ch]:
                self._draw_plot_lines(ch)

    def _draw_axes(self):
        self.canvas.create_rectangle(self.plot_origin_x, self.plot_origin_y,
                                     self.plot_end_x, self.plot_end_y,
                                     fill="darkgreen", outline="lime")
        cell_size = 20
        num_h_lines = self.plot_height // cell_size
        for i in range(1, int(num_h_lines)):
            y = self.plot_origin_y + i * cell_size
            self.canvas.create_line(self.plot_origin_x, y, self.plot_end_x, y, fill="lime", dash=(4, 2))
        num_v_lines = self.plot_width // cell_size
        for i in range(1, int(num_v_lines)):
            x = self.plot_origin_x + i * cell_size
            self.canvas.create_line(x, self.plot_origin_y, x, self.plot_end_y, fill="lime", dash=(4, 2))

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

    def _draw_plot_lines(self, channel):
        if not self.data_channels[channel]:
            return
        xs, ys = zip(*self.data_channels[channel])
        min_x = max(xs[0], xs[-1] - self.window_duration)
        max_x = xs[-1]
        min_y, max_y = 0, 100 
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
        colors = {1: "lime", 2: "lime", 3: "lime", 4: "lime"}
        return colors.get(channel, "black")

def main():
    root = tk.Tk()
    root.title("Multi-Channel XYPlot")

    plot = Oscillo(root, plot_name="Oscillo")
    plot.pack(padx=10, pady=10)
    plot.start_buffered_plot(max_points=100, window_duration=5)

    start_time = time.time()

    def waveform_feed():
        t = time.time() - start_time
        val1 = 50 + 40 * math.sin(2 * math.pi * 0.5 * t)

        plot.feed_data(1, val1)
        
        root.after(20, waveform_feed)

    def visa_sensor_feed():
        if pyvisa is None:
            print("PyVISA not available. Using waveform fallback.")
            waveform_feed()
            return

        rm = pyvisa.ResourceManager()
        visa_resource = 'YourInstrumentResourceStringHere'

        try:
            instrument = rm.open_resource(visa_resource)
            response = instrument.query("MEAS?")  
            values = list(map(float, response.strip().split(',')))

            for i, val in enumerate(values, start=1):
                plot.feed_data(i, val)
        except Exception as e:
            print(f"VISA instrument read error: {e}. Using waveform fallback.")
            waveform_feed()

        root.after(20, visa_sensor_feed)

    # visa_sensor_feed()

    waveform_feed()

    root.mainloop()

if __name__ == "__main__":
    main()
