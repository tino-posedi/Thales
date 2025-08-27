import tkinter as tk
from PIL import Image, ImageTk, ImageDraw
import math

class ArrowSpin(tk.Frame):
    def __init__(self, master=None, size=150, arrow_fill="yellow", fill="#000079", style='roundrect'):
        super().__init__(master, relief='raised', borderwidth=3)
        self.size = size
        self.arrow_fill = arrow_fill
        self.fill = fill
        self.style = style
        self.angle = 0

        self.speed = 0  
        self.direction = 'cw'  

        self.canvas = tk.Canvas(
            self,
            width=size,
            height=size,
            bg='systemButtonFace',
            highlightthickness=0
        )
        self.canvas.pack(padx=10, pady=10)

        self.rounded_rect_radius = 15
        self.draw_background()

        self.base_arrow = self.create_circular_arrow_image(size)
        self.tk_image = None
        self.image_id = None

        self.update_arrow()

    def set_speed(self, new_speed):
        self.speed = new_speed

    def set_direction(self, new_direction):
        if new_direction.lower() in ['cw', 'ccw']:
            self.direction = new_direction.lower()
        else:
            raise ValueError("Direction must be 'cw' or 'ccw'")
        self.base_arrow = self.create_circular_arrow_image(self.size)

    def draw_background(self):
        """Draw background based on style."""
        if self.style == 'roundrect':
            self.draw_rounded_background()
        elif self.style == 'rect':
            self.canvas.create_rectangle(0, 0, self.size, self.size, fill=self.fill, outline=self.fill)
        else:
            raise ValueError("Style must be 'roundrect' or 'rect'")

    def draw_rounded_background(self):
        """Draw a rounded blue rectangle on the canvas."""
        r = self.rounded_rect_radius
        w = self.size
        h = self.size
        blue = self.fill

        self.canvas.create_arc((0, 0, 2*r, 2*r), start=90, extent=90, fill=blue, outline=blue)
        self.canvas.create_arc((w-2*r, 0, w, 2*r), start=0, extent=90, fill=blue, outline=blue)
        self.canvas.create_arc((0, h-2*r, 2*r, h), start=180, extent=90, fill=blue, outline=blue)
        self.canvas.create_arc((w-2*r, h-2*r, w, h), start=270, extent=90, fill=blue, outline=blue)

        self.canvas.create_rectangle((r, 0, w - r, h), fill=blue, outline=blue)
        self.canvas.create_rectangle((0, r, w, h - r), fill=blue, outline=blue)

    def create_circular_arrow_image(self, size):
        image = Image.new("RGBA", (size, size), (0, 0, 0, 0))
        draw = ImageDraw.Draw(image)

        center = size / 2
        outer_radius = size * 0.4
        thickness = 15

        bbox = [
            center - outer_radius,
            center - outer_radius,
            center + outer_radius,
            center + outer_radius
        ]
        start_angle = 45
        end_angle = 315
        draw.arc(bbox, start=start_angle, end=end_angle, fill=self.arrow_fill, width=thickness)

        angle_deg = end_angle if self.direction == 'cw' else start_angle
        angle_rad = math.radians(angle_deg)

        end_x = center + outer_radius * math.cos(angle_rad)
        end_y = center + outer_radius * math.sin(angle_rad)

        offset_x, offset_y = (-11, 0)
        end_x += offset_x
        end_y += offset_y

        arrow_length = 30
        arrow_width = 20

        if self.direction == 'cw':
            dx = -math.sin(angle_rad)
            dy = math.cos(angle_rad)
        else:
            dx = math.sin(angle_rad)
            dy = -math.cos(angle_rad)

        nx = math.cos(angle_rad)
        ny = math.sin(angle_rad)

        tip = (end_x + arrow_length * dx, end_y + arrow_length * dy)
        left = (end_x - arrow_width * nx, end_y - arrow_width * ny)
        right = (end_x + arrow_width * nx, end_y + arrow_width * ny)

        draw.polygon([tip, left, right], fill=self.arrow_fill)
        return image

    def update_arrow(self):
        rotated = self.base_arrow.rotate(self.angle, resample=Image.BICUBIC)
        self.tk_image = ImageTk.PhotoImage(rotated)

        if self.image_id is None:
            self.image_id = self.canvas.create_image(self.size / 2, self.size / 2, image=self.tk_image)
        else:
            self.canvas.itemconfig(self.image_id, image=self.tk_image)

        direction_multiplier = -1 if self.direction == 'cw' else 1
        self.angle = (self.angle + direction_multiplier * self.speed) % 360
        self.after(50, self.update_arrow)

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Spinning Arrow")

    arrow = ArrowSpin(root, size=170, style='roundrect')
    arrow.pack(pady=20)
    arrow.set_speed(5)

    def change_direction():
        new_direction = 'ccw' if arrow.direction == 'cw' else 'cw'
        arrow.set_direction(new_direction)

    def on_speed_change(val):
        arrow.set_speed(int(val))

    change_button = tk.Button(root, text="Change Direction", command=change_direction)
    change_button.pack(pady=10)

    speed_slider = tk.Scale(root, from_=0, to=20, orient='horizontal', label="Speed", command=on_speed_change)
    speed_slider.set(5)
    speed_slider.pack(pady=10)

    root.mainloop()
