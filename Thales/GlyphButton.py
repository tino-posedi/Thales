import tkinter as tk
from PIL import Image, ImageTk

class GlyphButton(tk.Button):
    def __init__(self, master=None, text="GlyphButton", glyph_path=None, command=None, **kwargs):
        self._user_command = command  
        self._last_result = None      
        super().__init__(master, text=text, command=self._internal_command, takefocus=False, **kwargs)
        self.master = master
        self.text = text
        self._image_path = glyph_path
        self._image = None

        self.set_glyph(glyph_path)

    def set_glyph(self, glyph_path):
        if glyph_path:
            try:
                image = Image.open(glyph_path)
                image = image.resize((16, 16), Image.LANCZOS)
                self._image = ImageTk.PhotoImage(image)
                self.config(image=self._image, compound="left")
                return True
            except Exception as e:
                print(f"Failed to load glyph: {e}")
                self.config(image='', compound=None)
                return False
        else:
            self.config(image='', compound=None)
            return False

    def _internal_command(self):
        if self._user_command:
            self._last_result = self._user_command()
        else:
            self._last_result = None

    def return_value(self):
        return self._last_result

def main():
    def on_click():
        nonlocal is_on
        is_on = not is_on
        new_image = "BULBON.png" if is_on else "BULBOFF.png"
        button.set_glyph(new_image)
        print("Button clicked! Now:", "ON" if is_on else "OFF")

    root = tk.Tk()
    root.title("Glyph Button Toggle")
    root.geometry("300x100")

    is_on = False
    button = GlyphButton(root, glyph_path="BULBOFF.png", command=on_click)
    button.pack(pady=10)
    
    button2 = GlyphButton(root, text="Simulate", glyph_path="firstaid.png")
    button2.pack(pady=10)
    
    print("Last return value:", button.return_value()) 

    root.mainloop()

if __name__ == "__main__":
    main()
