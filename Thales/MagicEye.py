import tkinter as tk

class MagicEye(tk.Frame):
    def __init__(self, parent, spec_chan=10, width=300, height=150,
                 min_value=0, max_value=100, bg='black', fg='lime',
                 direction='vertical', **kwargs):
        super().__init__(parent, relief=tk.RAISED, bd=3, **kwargs)

        self.spec_chan = spec_chan
        self.min_value = min_value
        self.max_value = max_value
        self.fg = fg
        self.bg = bg
        self.direction = direction.lower()
        self.bar_values = [min_value] * spec_chan
        self.bar_ids = []
        self.margin = 0  

        self.canvas = tk.Canvas(self, width=width, height=height, bg=bg, highlightthickness=0)
        self.canvas.pack(padx=6, pady=6) 

        self._draw_all_bars()

    def _draw_all_bars(self):
        self.canvas.delete("bar")
        self.bar_ids.clear()
        w = int(self.canvas['width']) - 2 * self.margin
        h = int(self.canvas['height']) - 2 * self.margin

        for i in range(self.spec_chan):
            if self.direction == 'vertical':
                bar_width = w / self.spec_chan
                x0 = self.margin + i * bar_width + 1
                x1 = self.margin + (i + 1) * bar_width - 1
                y1 = self.margin + h
                y0 = y1
            else:
                bar_height = h / self.spec_chan
                y0 = self.margin + i * bar_height + 1
                y1 = self.margin + (i + 1) * bar_height - 1
                x0 = self.margin
                x1 = x0

            bar = self.canvas.create_rectangle(x0, y0, x1, y1,
                                               fill=self.fg, outline=self.fg, tags="bar")
            self.bar_ids.append(bar)

    def set_value(self, index, value):
        if 0 <= index < self.spec_chan:
            value = max(self.min_value, min(self.max_value, value))
            self.bar_values[index] = value
            self._update_bar(index)

    def _update_bar(self, index):
        w = int(self.canvas['width']) - 2 * self.margin
        h = int(self.canvas['height']) - 2 * self.margin
        value = self.bar_values[index]
        norm = (value - self.min_value) / (self.max_value - self.min_value)
        norm = max(0, min(1, norm))

        if self.direction == 'vertical':
            bar_width = w / self.spec_chan
            bar_height = norm * h
            x0 = self.margin + index * bar_width + 1
            x1 = self.margin + (index + 1) * bar_width - 1
            y1 = self.margin + h
            y0 = y1 - bar_height
        else:
            bar_height = h / self.spec_chan
            bar_width = norm * w
            y0 = self.margin + index * bar_height + 1
            y1 = self.margin + (index + 1) * bar_height - 1
            x0 = self.margin
            x1 = x0 + bar_width

        self.canvas.coords(self.bar_ids[index], x0, y0, x1, y1)

if __name__ == "__main__":
    import random

    def random_update():
        for i in range(spec_chan):
            graph.set_value(i, random.randint(0, 70))
        root.after(100, random_update)

    root = tk.Tk()
    root.title("Modular BarGraph Demo")

    spec_chan = 8

    graph = MagicEye(root, spec_chan=spec_chan, width=200, height=100, direction='vertical')
    graph.pack(padx=10, pady=10)

    random_update()
    root.mainloop()
