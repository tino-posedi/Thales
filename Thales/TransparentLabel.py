import tkinter as tk
from tkinter import font as tkfont
from PIL import Image, ImageDraw, ImageFont, ImageTk
from matplotlib import font_manager
import ast

def get_font_path(font_name):
    for font in font_manager.findSystemFonts(fontpaths=None, fontext='ttf'):
        if font_name.lower() in font.lower():
            return font
    return None

class TransparentLabel(tk.Canvas):
    def __init__(self, parent, text="Text", font="Arial", size=12, style=None,
                 fill="black", degree=0, shadow="inactive", shadow_offset=(2, 2),
                 transparency=255, **kwargs):

        if style is None:
            style = []

        if isinstance(shadow_offset, str):
            try:
                shadow_offset = ast.literal_eval(shadow_offset)
            except Exception:
                shadow_offset = (2, 2)

        weight = "bold" if "bold" in style else "normal"
        slant = "italic" if "italic" in style else "roman"
        underline = "underline" in style

        self.tk_font = tkfont.Font(family=font, size=size, weight=weight, slant=slant, underline=underline)

        font_path = get_font_path(font)
        pil_font = ImageFont.truetype(font_path, size) if font_path else ImageFont.load_default()

        bbox = pil_font.getbbox(text)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]

        shadow_x, shadow_y = shadow_offset if shadow == "active" else (0, 0)
        pad = max(size // 2, 20)
        base_w = text_width + abs(shadow_x) + pad * 2
        base_h = text_height + abs(shadow_y) + pad * 2

        img = Image.new("RGBA", (base_w, base_h), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)
        text_pos = (pad, pad)

        def to_rgba(color, alpha):
            if isinstance(color, str):
                return color
            elif isinstance(color, tuple) and len(color) == 3:
                return (*color, alpha)
            elif isinstance(color, tuple) and len(color) == 4:
                return color
            return (0, 0, 0, alpha)

        fill_rgba = to_rgba(fill, transparency)
        shadow_rgba = (50, 50, 50, transparency)  

        if shadow == "active":
            shadow_pos = (text_pos[0] + shadow_x, text_pos[1] + shadow_y)
            draw.text(shadow_pos, text, font=pil_font, fill=shadow_rgba)

        draw.text(text_pos, text, font=pil_font, fill=fill_rgba)

        if degree != 0:
            img = img.rotate(degree, expand=True, resample=Image.BICUBIC)

        self.tk_image = ImageTk.PhotoImage(img)

        super().__init__(parent, width=img.width, height=img.height, highlightthickness=0,
                         bg=kwargs.get("bg", parent["bg"]))
        self.create_image(0, 0, image=self.tk_image, anchor="nw")


if __name__ == "__main__":
    root = tk.Tk()
    root.configure(bg="#334455")

    TransparentLabel(
        root,
        text="Thales",
        font="Tahoma",
        size=52,
        fill="red",  
        degree=35,
        shadow="active",
        shadow_offset=(10, 10),
        transparency=160
    ).pack(pady=10)

    TransparentLabel(
        root,
        text="No Shadow",
        font="Tahoma",
        size=32,
        fill="red",
        degree=0,
        shadow="inactive"
    ).pack(pady=10)

    root.mainloop()
