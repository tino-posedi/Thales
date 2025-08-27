import tkinter as tk

class LoadingBar(tk.Frame):
    def __init__(self, master, width=300, height=30, block_count=20, fill="navy", **kwargs):
        super().__init__(master, relief="raised", bd=3, **kwargs)
        self.canvas = tk.Canvas(self, width=width, height=height, bg='white', highlightthickness=0)
        self.canvas.pack()

        self.width = width
        self.height = height
        self.block_count = block_count
        self.block_width = width / block_count
        self.filled_blocks = 0
        self.blocks = []
        self.fill = fill

        self._draw_blocks()

    def _draw_blocks(self):
        self.blocks.clear()
        for i in range(self.block_count):
            x0 = i * self.block_width
            x1 = x0 + self.block_width - 2
            rect = self.canvas.create_rectangle(x0, 2, x1, self.height - 2, outline='gray', fill='white')
            self.blocks.append(rect)

    def update_progress(self, percent):
        blocks_to_fill = int((percent / 100) * self.block_count)
        for i in range(self.block_count):
            color = self.fill if i < blocks_to_fill else 'white'
            self.canvas.itemconfig(self.blocks[i], fill=color)

if __name__ == '__main__':
    def test_increment():
        global progress
        progress = min(100, progress + 5)
        bar.update_progress(progress)

    def test_minus_increment():
        global progress
        progress = min(100, progress - 5)
        bar.update_progress(progress)
        
    root = tk.Tk()
    root.title("Block Loading Bar")

    bar = LoadingBar(root, width=200, height=20, block_count=20)
    bar.pack(padx=20, pady=20)

    progress = 0
    btn = tk.Button(root, text="Increment 5%", command=test_increment)
    btn.pack(pady=10)
    
    btn = tk.Button(root, text="Increment 5%", command=test_minus_increment)
    btn.pack(pady=10)

    root.mainloop()