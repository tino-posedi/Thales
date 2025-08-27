import tkinter as tk
import ast

class BoxLine(tk.Frame):
    def __init__(self, master=None, amount=8, captions=None,
                 vertical="active", **kwargs):
        super().__init__(master, **kwargs)
        self.amount = amount
        self.vertical = vertical.lower() == "active"
        self.states = [False] * amount
        self.boxes = [None] * amount 

        if captions is None:
            captions = [f"Bit {i+1}" for i in range(amount)]
        elif isinstance(captions, str):
            try:
                captions = ast.literal_eval(captions)
            except Exception:
                captions = [""] * amount

        if len(captions) < amount:
            captions += [""] * (amount - len(captions))
        self.captions = captions[:amount]

        self.max_caption_len = max(len(c) for c in self.captions) if not self.vertical else None

        for i in range(amount):
            state_idx = i
            container = tk.Frame(self)
            
            if self.vertical:
                container.grid(row=i, column=0, padx=2, pady=2, sticky="w")
            else:
                container.grid(row=0, column=i, padx=2, pady=2)

            lbl = tk.Label(container, text="0", bg="white", width=2, height=1,
                           font=("Arial", 10, "bold"), relief="solid", bd=1)
            lbl.bind("<Button-1>", lambda e, ix=state_idx: self.toggle(ix))
            lbl.grid(row=0, column=0)

            if not self.vertical:
                caption = self.captions[i].ljust(self.max_caption_len)
                vertical_text = "\n".join(c for c in caption)
                cap_lbl = tk.Label(container, text=vertical_text, font=("Arial", 8))
                cap_lbl.grid(row=1, column=0, pady=(2,0))
            else:
                cap = tk.Label(container, text=self.captions[i], font=("Arial", 8), anchor="w")
                cap.grid(row=0, column=1, padx=(4,0))

            self.boxes[state_idx] = lbl

    def toggle(self, idx):
        self.states[idx] = not self.states[idx]
        if self.states[idx]:
            self.boxes[idx].config(text="1", bg="yellow")
        else:
            self.boxes[idx].config(text="0", bg="white")

    def get_states(self):
        return [int(state) for state in self.states]

    class BitSetter:
        def __init__(self, boxline, idx):
            self.boxline = boxline
            self.idx = idx

        def high(self):
            self.boxline.states[self.idx] = True
            self.boxline.boxes[self.idx].config(text="1", bg="yellow")
            return self.boxline

        def low(self):
            self.boxline.states[self.idx] = False
            self.boxline.boxes[self.idx].config(text="0", bg="white")
            return self.boxline

    def set_bit(self, idx):
        if 0 <= idx < self.amount:
            return self.BitSetter(self, idx)
        else:
            raise IndexError(f"Bit index {idx} out of range (0-{self.amount - 1})")

if __name__ == "__main__":
    root = tk.Tk()
    root.title("BoxLine horizontal kompakt")

    captions = ["Bit eins", "Bit zwei", "Bit drei", "Bit vier", "P4_extra", "P5", "P6", "P7"]

    boxline_h = BoxLine(root, amount=8, captions=captions, vertical="active")
    boxline_h.pack(pady=10)

    def show_states():
        print("States:", boxline_h.get_states())

    btn = tk.Button(root, text="Zustände anzeigen", command=show_states)
    btn.pack(pady=10)

    boxline_h.set_bit(0).high()
    boxline_h.set_bit(7).high()

    root.mainloop()
