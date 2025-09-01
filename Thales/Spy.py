import tkinter as tk
import math

class Spy(tk.Frame):
    def __init__(self, master, eyeball_color="white", pupil_color="black", width=120, height=80):
        super().__init__(master, width=width, height=height)
        self.pack_propagate(False) 

        self.canvas = tk.Canvas(self, width=width, height=height,
                                bg=self.master.cget("bg"), highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)

        self.eye_width = 40
        self.eye_height = 60
        self.pupil_radius = min(self.eye_width, self.eye_height) // 5
        self.eyeball_color = eyeball_color
        self.pupil_color = pupil_color

        center_y = height // 2
        spacing = 45
        center_x = width // 2

        self.eyes = [
            {"x": center_x - spacing//2, "y": center_y},
            {"x": center_x + spacing//2, "y": center_y}
        ]

        for eye in self.eyes:
            eye["eyeball"] = self.canvas.create_oval(
                eye["x"] - self.eye_width//2, eye["y"] - self.eye_height//2,
                eye["x"] + self.eye_width//2, eye["y"] + self.eye_height//2,
                fill=self.eyeball_color, outline="black", width=1
            )
            eye["pupil"] = self.canvas.create_oval(
                eye["x"] - self.pupil_radius, eye["y"] - self.pupil_radius,
                eye["x"] + self.pupil_radius, eye["y"] + self.pupil_radius,
                fill=self.pupil_color
            )

        self._bind_to_root()

    def _bind_to_root(self):
        top = self.winfo_toplevel()
        top.bind("<Motion>", self._mouse_move)

    def _mouse_move(self, event):
        widget_x = self.winfo_rootx()
        widget_y = self.winfo_rooty()
        rel_x = event.x_root - widget_x
        rel_y = event.y_root - widget_y

        for eye in self.eyes:
            dx = rel_x - eye["x"]
            dy = rel_y - eye["y"]
            angle = math.atan2(dy, dx)

            max_x = self.eye_width//2 - self.pupil_radius - 2
            max_y = self.eye_height//2 - self.pupil_radius - 2

            pupil_x = eye["x"] + max_x * math.cos(angle)
            pupil_y = eye["y"] + max_y * math.sin(angle)

            self.canvas.coords(
                eye["pupil"],
                pupil_x - self.pupil_radius, pupil_y - self.pupil_radius,
                pupil_x + self.pupil_radius, pupil_y + self.pupil_radius
            )


if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("800x600")
    root.configure(bg="SystemButtonFace")

    spy1 = Spy(root, eyeball_color="white", pupil_color="black")
    spy1.pack(padx=20, pady=20)

    spy2 = Spy(root, eyeball_color="lightblue", pupil_color="blue")
    spy2.pack(padx=20, pady=20)

    root.mainloop()
