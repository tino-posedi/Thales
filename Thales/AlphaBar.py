import tkinter as tk
from tkinter import Frame, Button, Text

class AlphaBar(Frame):
    def __init__(self, master=None, input_target=None, **kwargs):
        super().__init__(master, width=300, height=400, bd=3, relief='raised', **kwargs)
        self.pack_propagate(0)
        self.configure(bg="lightgrey")
        self.input_target = input_target
        self.shift = False
        self.caps = False
        self.shift_map = {
            '1': '!', '2': '"', '3': '§', '4': '$', '5': '%',
            '6': '&', '7': '/', '8': '(', '9': ')', '0': '=',
            'ß': '?', '´': '`', '+': '*', '#': '\'', ',': ';',
            '.': ':', '-': '_', '<': '>', '^': '°'
        }
        self.create_keys()

    def create_keys(self):
        layout = [
            ['^', '1', '2', '3', '4', '5', '6', '7', '8', '9', '0', 'ß', '´'],
            ['Tab', 'q', 'w', 'e', 'r', 't', 'z', 'u', 'i', 'o', 'p', 'ü', '+'],
            ['Caps', 'a', 's', 'd', 'f', 'g', 'h', 'j', 'k', 'l', 'ö', 'ä', '#'],
            ['Shift', '<', 'y', 'x', 'c', 'v', 'b', 'n', 'm', ',', '.', '-', '←'],
            ['Space']
        ]

        for row_index, row in enumerate(layout):
            col_index = 0
            for key in row:
                width = 3
                columnspan = 1

                if key in ['Tab', 'Caps', 'Shift']:
                    width = 5
                elif key == 'Space':
                    width = 30
                    columnspan = 13
                elif key == '←':
                    width = 4

                btn = Button(
                    self,
                    text=key,
                    width=width,
                    bg="lightgray",
                    fg="black",
                    relief="raised",
                    font=("Arial", 9),
                    command=lambda k=key: self.on_key_press(k)
                )
                btn.grid(row=row_index, column=col_index, columnspan=columnspan, padx=1, pady=1, sticky='nsew')
                col_index += columnspan

    def on_key_press(self, key):
        if not self.input_target:
            return

        if key == 'Space':
            self.input_target.insert(tk.INSERT, ' ')
        elif key == 'Tab':
            self.input_target.insert(tk.INSERT, '\t')
        
        elif key == '←':
            self.input_target.delete("insert-1c")
        elif key == 'Caps':
            self.caps = not self.caps
        elif key == 'Shift':
            self.shift = True
        else:
            output_key = key

            if key.isalpha():
                if self.caps ^ self.shift:
                    output_key = key.upper()
                else:
                    output_key = key.lower()

            elif key in self.shift_map and self.shift:
                output_key = self.shift_map[key]

            self.input_target.insert(tk.INSERT, output_key)

            if self.shift:
                self.shift = False

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Virtuelle Tastatur")
    root.geometry("500x500")
    root.resizable(True, True)

    text_area = Text(root, height=5, width=60, font=("Arial", 12))
    text_area.pack(pady=10)

    keyboard = AlphaBar(root, input_target=text_area)
    keyboard.pack(pady=10)

    root.mainloop()
