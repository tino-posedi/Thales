import tkinter as tk
import inspect

class BitWin:
    def __init__(self, master, bit_text="", target=None):
        self.master = master
        self.bit_text = bit_text
        self.tipwindow = None
        self.show_id = None

        if isinstance(target, str):
            self.target = self._resolve_target_from_string(target)
        else:
            self.target = target

        if self.target and not isinstance(self.target, tk.Widget) and hasattr(self.target, "frame"):
            self.target = self.target.frame

        if self.target and isinstance(self.target, tk.Widget):
            self.target.bind("<Enter>", self.schedule_tip)
            self.target.bind("<Leave>", self.hide_tip)
            self.target.bind("<Motion>", self.reset_tip_timer)

    def pack(self, *args, **kwargs):
        if self.target:
            return self.target.pack(*args, **kwargs)

    def grid(self, *args, **kwargs):
        if self.target:
            return self.target.grid(*args, **kwargs)

    def place(self, *args, **kwargs):
        if self.target:
            return self.target.place(*args, **kwargs)

    def _resolve_target_from_string(self, name):
        candidates = [name]
        if not name.startswith("."):
            candidates.append("." + name)
            candidates.append(".!" + name)
        for cand in candidates:
            try:
                w = self.master.nametowidget(cand)
                if isinstance(w, tk.Widget):
                    return w
            except Exception:
                pass

        def _find_by_winfo_name(parent, want):
            for child in parent.winfo_children():
                if child.winfo_name() == want or child.winfo_name() == want.lstrip(".!"):
                    return child
                found = _find_by_winfo_name(child, want)
                if found:
                    return found
            return None

        found = _find_by_winfo_name(self.master, name)
        if found:
            return found

        try:
            for frame_info in inspect.stack()[1:]:
                frame = frame_info.frame
                try:
                    for namespace in (frame.f_locals, frame.f_globals):
                        val = namespace.get(name, None)
                        if isinstance(val, tk.Widget) or hasattr(val, "frame"):
                            return val
                finally:
                    del frame
        except Exception:
            pass

        return None

    def schedule_tip(self, event=None):
        self.cancel_scheduled_tip()
        self.show_id = self.master.after(1000, lambda ev=event: self.show_tip(ev))

    def reset_tip_timer(self, event=None):
        if self.tipwindow:
            self.move_tip(event)
        else:
            self.schedule_tip(event)

    def cancel_scheduled_tip(self):
        if self.show_id:
            try:
                self.master.after_cancel(self.show_id)
            except Exception:
                pass
            self.show_id = None

    def show_tip(self, event=None):
        self.show_id = None
        if self.tipwindow or not self.bit_text:
            return
        if event is None:
            try:
                x = self.target.winfo_rootx() + 10
                y = self.target.winfo_rooty() + 10
            except Exception:
                x = y = 100
        else:
            x = event.x_root + 10
            y = event.y_root + 10

        self.tipwindow = tw = tk.Toplevel(self.master)
        tw.wm_overrideredirect(True)
        tw.wm_geometry(f"+{x}+{y}")
        label = tk.Label(
            tw,
            text=self.bit_text,
            justify=tk.LEFT,
            background="#ffffe0",
            relief=tk.SOLID,
            borderwidth=1,
            font=("tahoma", "8", "normal")
        )
        label.pack(ipadx=5, ipady=2)

    def move_tip(self, event):
        if self.tipwindow:
            x = event.x_root + 10
            y = event.y_root + 10
            self.tipwindow.wm_geometry(f"+{x}+{y}")

    def hide_tip(self, event=None):
        self.cancel_scheduled_tip()
        if self.tipwindow:
            try:
                self.tipwindow.destroy()
            except Exception:
                pass
            self.tipwindow = None


if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("300x200")

    button1 = tk.Button(root, text="Button 1")
    button1.pack(pady=10)

    button2 = tk.Button(root, text="Button 2")
    button2.pack(pady=10)

    BitWin(root, bit_text="This is Button 1", target="button1")
    BitWin(root, bit_text="This is Button 2", target="button2")

    root.mainloop()
