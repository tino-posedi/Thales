import tkinter as tk
import time
import random
import threading

class Logicana(tk.Frame):
    def __init__(self, master=None, plot_name="Logic Analyzer", channel_count=8, **kwargs):
        super().__init__(master, bd=3, relief='raised', bg="SystemButtonFace", **kwargs)
        self.canvas_width = 500
        self.canvas_height = 280
        self.plot_width = 435
        self.plot_height = 240
        self.channel_count = channel_count
        self.plot_name = plot_name
        self.paused = False

        self.plot_origin_x = 60
        self.plot_origin_y = 33
        self.plot_end_x = self.plot_origin_x + self.plot_width
        self.plot_end_y = self.plot_origin_y + self.plot_height

        self.data_channels = {i: [] for i in range(1, channel_count + 1)}
        self.visible_channels = {i: True for i in range(1, channel_count + 1)}
        self.max_points = 100
        self.window_duration = 10
        self.start_time = None

        self.running = False
        self.view_offset = 0
        self.channel_height = 30
        self.max_visible_channels = self.plot_height // self.channel_height

        self.data_source_func = None  

        self.canvas = tk.Canvas(self, width=self.canvas_width, height=self.canvas_height,
                                highlightthickness=0, bg="SystemButtonFace")
        self.canvas.pack(pady=(0, 0))

        self._load_icons()
        self._init_control_bar()
        self._draw_ui()

    def _load_icons(self):
        self.play_icon = tk.PhotoImage(file="PLAY.PNG")
        self.stop_icon = tk.PhotoImage(file="STOP.PNG")
        self.pause_icon = tk.PhotoImage(file="PAUSE.PNG")
        self.save_icon = tk.PhotoImage(file="SAVE.PNG")
        self.up_icon = tk.PhotoImage(file="ARROWUP.PNG")
        self.down_icon = tk.PhotoImage(file="ARROWDOWN.PNG")
        self.hex_icon = tk.PhotoImage(file="HEX.PNG")

    def set_data_source(self, func):
        """
        Set the data source function for live input.
        The function must return a dictionary: {channel_number: 0 or 1}
        """
        self.data_source_func = func

    def _init_control_bar(self):
        control_frame = tk.Frame(self)
        control_frame.pack(pady=(0, 6))

        start_button = tk.Button(control_frame, image=self.play_icon, width=24, height=24, command=self._start_clicked)
        start_button.grid(row=0, column=0, padx=1)

        stop_button = tk.Button(control_frame, image=self.stop_icon, width=24, height=24, command=self._stop_clicked)
        stop_button.grid(row=0, column=1, padx=1)

        self.pause_button = tk.Button(control_frame, image=self.pause_icon, width=24, height=24, command=self._toggle_pause)
        self.pause_button.grid(row=0, column=2, padx=1)

        save_button = tk.Button(control_frame, image=self.save_icon, width=24, height=24, command=self._save_plot)
        save_button.grid(row=0, column=3, padx=1)

        tk.Label(control_frame, text=" " * 1).grid(row=0, column=4)

        up_button = tk.Button(control_frame, image=self.up_icon, width=24, height=24, command=self.scroll_up)
        up_button.grid(row=0, column=5, padx=2)

        down_button = tk.Button(control_frame, image=self.down_icon, width=24, height=24, command=self.scroll_down)
        down_button.grid(row=0, column=6, padx=2)
        self.hex_view = False
       
        hex_button = tk.Button(control_frame, image=self.hex_icon, width=24, height=24, command=self._toggle_hex_view)
        hex_button.grid(row=0, column=7, padx=2)
    
    def _toggle_hex_view(self):
        self.hex_view = not self.hex_view
        self._draw_ui()
        
    def _start_clicked(self):
        self.start_buffered_plot()

    def _stop_clicked(self):
        self.stop_buffered_plot()

    def _toggle_pause(self):
        if not self.running:
            return
        self.paused = not self.paused
        self.pause_button.config(relief=tk.SUNKEN if self.paused else tk.RAISED)

    def scroll_up(self):
        if self.view_offset > 0:
            self.view_offset -= 1
            self._draw_ui()

    def scroll_down(self):
        if self.view_offset < self.channel_count - self.max_visible_channels:
            self.view_offset += 1
            self._draw_ui()

    def start_buffered_plot(self, max_points=100, window_duration=10):
        self.data_channels = {i: [] for i in range(1, self.channel_count + 1)}
        self.start_time = time.time()
        self.running = True
        self._draw_ui()
        self._poll_data_source()

    def stop_buffered_plot(self):
        self.running = False
        self.start_time = None
        self.data_channels = {i: [] for i in range(1, self.channel_count + 1)}
        self._draw_ui()

    def _poll_data_source(self):
        if not self.running:
            return
        if not self.paused:
            if self.data_source_func:
                try:
                    data = self.data_source_func()
                    if data:
                        self.buffer_read(data)
                except Exception as e:
                    print("Error reading data source:", e)
            else:
                test_data = {i: random.randint(0, 1) for i in range(1, self.channel_count + 1)}
                self.buffer_read(test_data)
        self.after(50, self._poll_data_source)

    def buffer_read(self, data_dict):
        if self.start_time is None:
            self.start_buffered_plot()
        t = time.time() - self.start_time
        for ch, val in data_dict.items():
            if ch in self.data_channels:
                self.data_channels[ch].append((t, val))
                self.data_channels[ch] = [(x, y) for x, y in self.data_channels[ch] if x >= t - self.window_duration]
        self._draw_ui()

    def feed_data(self, data_dict):
        if not self.running:
            self.start_buffered_plot()
        self.buffer_read(data_dict)

    def _save_plot(self):
        def capture_screenshot():
            try:
                self.update_idletasks()
                self.update()

                x = self.winfo_rootx() + self.canvas.winfo_x()
                y = self.winfo_rooty() + self.canvas.winfo_y()
                w = x + self.canvas.winfo_width()
                h = y + self.canvas.winfo_height()

                from PIL import ImageGrab
                img = ImageGrab.grab(bbox=(x, y, w, h))
                img.save("logicana_plot.png")
                print("Plot saved as 'logicana_plot.png'")
            except Exception as e:
                print("Error saving screenshot:", e)

        threading.Thread(target=capture_screenshot).start()

    def _draw_ui(self):
        self.canvas.delete("all")
        self._draw_title()
        self._draw_axes()
        self._draw_channels()
        self.canvas.create_text(self.canvas_width - 5, 5, text="Thales", anchor="ne", font=("Arial", 8), fill="gray")

    def _draw_title(self):
        self.canvas.create_rectangle(self.canvas_width // 2 - 50, 5,
                                     self.canvas_width // 2 + 50, 25,
                                     fill='black')
        self.canvas.create_text(self.canvas_width // 2, 15, text=self.plot_name,
                                fill='lime', font=("Arial", 10, 'bold'))

    def _draw_axes(self):   
        if self.hex_view:
            self.canvas.create_rectangle(self.plot_origin_x - 57, self.plot_origin_y,
                                         self.plot_end_x, self.plot_end_y,
                                         fill="black", outline="black")
            return
        
        self.canvas.create_rectangle(self.plot_origin_x, self.plot_origin_y,
                                     self.plot_end_x, self.plot_end_y,
                                     fill="black", outline="black")
        if any(self.data_channels.values()):
            latest_time = max((data[-1][0] for data in self.data_channels.values() if data), default=0)
        else:
            latest_time = self.window_duration
        start_time = max(0, latest_time - self.window_duration)
        for i in range(6):
            x = self.plot_origin_x + i * (self.plot_width / 5)
            self.canvas.create_line(x, self.plot_origin_y, x, self.plot_end_y, fill="gray")

    def _draw_channels(self):
        
        if self.hex_view:
            # Black background for hex view
            self.canvas.create_rectangle(self.plot_origin_x - 57, self.plot_origin_y,
                                         self.plot_end_x, self.plot_end_y,
                                         fill="black", outline="black")
            
            all_times = sorted(set(t for data in self.data_channels.values() for t, _ in data))
            max_rows = self.plot_height // 17  # row height
            start_idx = max(0, len(all_times) - max_rows)
            y = self.plot_origin_y

            for t in all_times[start_idx:]:
                bits = [self._get_value_at_time(ch, t) for ch in range(1, self.channel_count + 1)]
                bit_str = "".join(str(b) for b in reversed(bits))
                hex_str = f"{int(bit_str, 2):0{(len(bits)+3)//4}X}"

                self.canvas.create_text(self.plot_origin_x - 64, y + 7,
                                        text=f"{t:6.2f}s       :       HEX={hex_str}       BIN={bit_str}",
                                        fill="lime", anchor="w", font=("Consolas", 10))
                y += 17
            return
        if not self.hex_view:
            visible_channels = [ch for ch in range(1 + self.view_offset, 1 + self.view_offset + self.max_visible_channels)
                                if ch <= self.channel_count]
            for i, ch in enumerate(visible_channels):
                y_base = self.plot_origin_y + i * self.channel_height + self.channel_height // 2
                y_line = self.plot_origin_y + i * self.channel_height

                color = "red" if not self.visible_channels[ch] else "black"
                font_style = ("Arial", 8, 'overstrike') if not self.visible_channels[ch] else ("Arial", 8)

                label_id = self.canvas.create_text(self.plot_origin_x - 12, y_base,
                                                   text=f"Chan {ch}", fill=color, anchor="e", font=font_style)
                self.canvas.tag_bind(label_id, "<Button-1>", lambda e, chan=ch: self._toggle_channel(chan))
                self.canvas.create_line(self.plot_origin_x, y_line, self.plot_end_x, y_line, fill="cyan")

                if self.visible_channels[ch] and ch in self.data_channels and len(self.data_channels[ch]) > 1:
                    self._draw_logic_waveform(self.data_channels[ch], y_base)
            return

        all_times = sorted(set(t for data in self.data_channels.values() for t, _ in data))
        max_rows = self.plot_height // 5
        start_idx = max(0, len(all_times) - max_rows)
        y = self.plot_origin_y

        for t in all_times[start_idx:]:
            bits = [self._get_value_at_time(ch, t) for ch in range(1, self.channel_count + 1)]
            bit_str = "".join(str(b) for b in reversed(bits))
            hex_str = f"{int(bit_str, 2):0{(len(bits)+3)//4}X}"

            self.canvas.create_text(self.plot_origin_x - 64, y,
                                    text=f"{t:6.2f}s : HEX={hex_str} BIN={bit_str}",
                                    fill="lime", anchor="w", font=("Consolas", 10))
            y += 17

    def _get_value_at_time(self, ch, t):
        data = self.data_channels.get(ch, [])
        for i in reversed(range(len(data))):
            if data[i][0] <= t:
                return data[i][1]
        return 0

    def _toggle_channel(self, ch):
        self.visible_channels[ch] = not self.visible_channels[ch]
        self._draw_ui()

    def _draw_logic_waveform(self, data, y_base):
        min_x = max(data[0][0], data[-1][0] - self.window_duration)
        max_x = data[-1][0]

        def map_x(x):
            return self.plot_origin_x + (x - min_x) / (max_x - min_x) * self.plot_width if max_x != min_x else self.plot_origin_x

        high_y = y_base - 8
        low_y = y_base + 8

        for i in range(1, len(data)):
            x1, y1 = data[i - 1]
            x2, y2 = data[i]
            px1 = map_x(x1)
            px2 = map_x(x2)
            py1 = high_y if y1 else low_y
            py2 = high_y if y2 else low_y
            self.canvas.create_line(px1, py1, px2, py1, fill="lime", width=2)
            if py1 != py2:
                self.canvas.create_line(px2, py1, px2, py2, fill="lime", width=2)


if __name__ == "__main__":
    import serial

    root = tk.Tk()
    root.title("Logic Analyzer")

    logic_analyzer = Logicana(root, channel_count=20)
    logic_analyzer.pack()

    # To use live serial data, uncomment and set your serial reading function
    # ser = serial.Serial('COM3', 9600)
    # def read_serial():
    #     line = ser.readline().decode().strip()
    #     bits = list(map(int, line.split(',')))
    #     return {i+1: bits[i] for i in range(len(bits))}
    # logic_analyzer.set_data_source(read_serial)

    # logic_analyzer.start_buffered_plot()
    root.mainloop()
