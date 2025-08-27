import tkinter as tk
import webcolors

class FlashLabel(tk.Frame):
    def __init__(self, master, fill="green", text="OK!", width=200, height=60, flash="inactive", **kwargs):
        super().__init__(master, relief="raised", borderwidth=4, **kwargs)
        self.fill = self._color_to_hex(fill)
        self.flash_mode = flash
        self._after_id = None
        
        if flash == "active":
            self.fill_light = self.fill
            self.fill_dark = self._darken_color(self.fill, factor=0.4)
            self.current_fill = self.fill_light
        else:
            self.fill_light = self.fill
            self.fill_dark = self.fill  
            self.current_fill = self.fill

        self.config(width=width, height=height)
        self.pack_propagate(False)

        self.label = tk.Label(
            self,
            text=text,
            bg=self.current_fill,
            relief="sunken",
            fg="white",
            font=("Arial", 16, "bold"),
            anchor="center",
            bd=2
        )
        self.label.pack(fill="both", expand=True, padx=4, pady=4)

        if self.flash_mode == "active":
            self._flash()

    def _flash(self):
        if self.flash_mode != "active":
            return
        self.current_fill = self.fill_dark if self.current_fill == self.fill_light else self.fill_light
        self.label.config(bg=self.current_fill)
        self._after_id = self.after(500, self._flash)

    def start_flashing(self):
        self.flash_mode = "active"
        self.fill_dark = self._darken_color(self.fill, factor=0.4)
        self.current_fill = self.fill_light
        self._flash()

    def stop_flashing(self):
        self.flash_mode = "inactive"
        if self._after_id is not None:
            self.after_cancel(self._after_id)
            self._after_id = None
        self.current_fill = self.fill
        self.label.config(bg=self.current_fill)

    def _darken_color(self, hex_color, factor=0.8):
        hex_color = hex_color.lstrip('#')
        r, g, b = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
        r, g, b = int(r*factor), int(g*factor), int(b*factor)
        return f'#{r:02x}{g:02x}{b:02x}'

    def _color_to_hex(self, color):
        import webcolors
        try:
            return webcolors.name_to_hex(color.lower())
        except ValueError:
            return color

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Flashing Label")
    root.geometry("300x120")

    flashing = FlashLabel(root, fill="teal", text="FAIL", width=260, height=60, flash="active")
    flashing.pack(padx=10, pady=10)

    root.mainloop()
