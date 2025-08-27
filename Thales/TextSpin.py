import tkinter as tk
import ast

class TextSpin(tk.Frame):
    def __init__(self, parent, values=None, start=0, wrap="inactive",
                 text="", fill="white", number_fill="black",
                 width=200, height=35, orientation="right", **kwargs):
        super().__init__(parent, bd=3, relief="raised", **kwargs)

        self.raw_values = values 
        self.values = []

        if isinstance(values, str) and values.strip().startswith('[') and values.strip().endswith(']'):
            try:
                self.values = [str(v) for v in ast.literal_eval(values)]
            except Exception:
                self.values = [values]
        elif isinstance(values, (list, tuple)):
            self.values = [str(v) for v in values]
        elif isinstance(values, str):
            self.values = [values]
        elif values is None:
            self.values = [text] if text else [""]

        self.index = start if 0 <= start < len(self.values) else 0
        self.wrap = wrap
        self.width = width
        self.height = height

        anchor_map = {"left": "w", "center": "center", "right": "e"}
        self.anchor = anchor_map.get(orientation, "e")

        self.config(width=self.width, height=self.height)
        self.pack_propagate(False)

        container = tk.Frame(self)
        container.pack(fill="both", expand=True)

        self.label = tk.Label(container,
                              text=self.values[self.index],
                              bg=fill,
                              fg=number_fill,
                              font=("Arial", 32, "bold"),
                              anchor=self.anchor,
                              bd=1,
                              relief="solid")
        self.label.pack(side="left", fill="both", expand=True, padx=(3,0), pady=3)

        btn_frame = tk.Frame(container, bg=fill, bd=1, relief="solid")
        btn_frame.pack(side="right", fill="y", padx=3, pady=3)
        btn_frame.grid_rowconfigure(0, weight=1)
        btn_frame.grid_rowconfigure(1, weight=1)
        btn_frame.grid_columnconfigure(0, weight=1)

        arrow_font_size = 10 if self.height >= 45 else 6
        self.btn_up = tk.Button(btn_frame, text="▲", command=self._increment,
                                padx=0, pady=0, font=("Arial", arrow_font_size, "bold"))
        self.btn_up.grid(row=0, column=0, sticky="nsew")
        self.btn_down = tk.Button(btn_frame, text="▼", command=self._decrement,
                                  padx=0, pady=0, font=("Arial", arrow_font_size, "bold"))
        self.btn_down.grid(row=1, column=0, sticky="nsew")

        self._adjust_font_size(self.values[self.index])

    def _increment(self):
        if self.index < len(self.values)-1:
            self.index += 1
        elif self.wrap == "active":
            self.index = 0
        self._update_display()

    def _decrement(self):
        if self.index > 0:
            self.index -= 1
        elif self.wrap == "active":
            self.index = len(self.values)-1
        self._update_display()

    def _update_display(self):
        self.label.config(text=self.values[self.index])
        self._adjust_font_size(self.values[self.index])

    def _adjust_font_size(self, text):
        max_width = self.width*0.7
        max_height = self.height*0.8
        font_size = 1
        temp = tk.Label(self, text=text, font=("Arial", font_size, "bold"))
        temp.update_idletasks()
        while True:
            temp.config(font=("Arial", font_size, "bold"))
            temp.update_idletasks()
            if temp.winfo_reqwidth()>max_width or temp.winfo_reqheight()>max_height:
                font_size -= 1
                break
            font_size +=1
        temp.destroy()
        self.label.config(font=("Arial", font_size, "bold"))

    def return_value(self):
            return self.values[self.index]