import tkinter as tk
import time

class SmartTimer(tk.Frame):
    def __init__(self, master=None, duration="1000", **kwargs):
        super().__init__(master, width=0, height=0, borderwidth=0, highlightthickness=0, **kwargs)
        self.pack_propagate(False)
        
        self.duration = self._parse_duration(duration) / 1000 
        self._start_time = None
        self._done = False

    def _parse_duration(self, duration):
        if hasattr(duration, "get") and callable(duration.get):
            duration = duration.get()
        if hasattr(duration, "winfo_exists"):
            raise TypeError("Invalid duration: tkinter widget passed")
        if isinstance(duration, (int, float)):
            return float(duration)
        elif isinstance(duration, str):
            if duration.strip().isdigit():
                return float(duration.strip())
            else:
                raise ValueError("Duration string must be digits only")
        else:
            raise TypeError("Duration must be int, float, or digit string")

    def start(self):
        self._start_time = time.perf_counter()
        self._done = False
        self._check()

    def _check(self):
        elapsed = time.perf_counter() - self._start_time
        if elapsed >= self.duration:
            self._done = True
        else:
            self.after(1, self._check) 

    def is_done(self):
        return self._done

    def elapsed_ms(self):
        if self._start_time is None:
            return 0
        return int((time.perf_counter() - self._start_time) * 1000)

if __name__ == "__main__":
    root = tk.Tk()
    root.title("SmartTimer Non-Visual Widget")

    timer_widget = SmartTimer(root, duration="2000")
    timer_widget.pack()

    label = tk.Label(root, text="Timer not started")
    label.pack()

    def start_timer():
        timer_widget.start()
        label.config(text=f"Timer started for {int(timer_widget.duration * 1000)} ms")

        def check_timer():
            if timer_widget.is_done():
                label.config(text="Timer done!")
            else:
                print(f"Elapsed: {timer_widget.elapsed_ms()} ms")
                root.after(50, check_timer)

        check_timer()

    start_btn = tk.Button(root, text="Start Timer", command=start_timer)
    start_btn.pack()

    root.mainloop()
