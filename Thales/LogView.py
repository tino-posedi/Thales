import tkinter as tk
import threading
import time
import random

class LogView(tk.Frame):
    def __init__(self, parent, width=200, height=200):
        super().__init__(parent, bd=3, relief='sunken', width=width, height=height)
        self.pack_propagate(False)
        self.entry_widgets = []

    def add_entry(self, text, text_fill='black'):
        label = tk.Label(self, text=text, anchor='w', fg=text_fill)
        label.pack(anchor='nw', fill='x')
        self.entry_widgets.append(label)

    def del_entry(self):
        if self.entry_widgets:
            widget = self.entry_widgets.pop()
            widget.destroy()
            
    def del_all_entries(self):
            for widget in self.entry_widgets:
                widget.destroy()
            self.entry_widgets.clear()

if __name__ == '__main__':
    root = tk.Tk()
    root.title("Non-Editable Entry Frame")

    ef = LogView(root, width=300, height=200)
    ef.pack(padx=10, pady=10)

    control_frame = tk.Frame(root)
    control_frame.pack(pady=5)

    def load_kithara():
        ef.add_entry("Step: Init Kithara", text_fill="blue")
        time.sleep(2)
        ef.add_entry("Error loading Kithara", text_fill="red")
        time.sleep(1)
        ef.add_entry("Trying again.")
        time.sleep(1)
        ef.add_entry("Trying again..")
        time.sleep(1)
        ef.add_entry("Trying again....")
        time.sleep(1)
        ef.add_entry("Kithara loaded successfully", text_fill="green")
        time.sleep(1)
        ef.del_all_entries()
        time.sleep(1)
        ef.add_entry("Step: Arbeitspunkt bestimmen", text_fill="blue")
        time.sleep(1.5)

        numbers = [24.12, 35.65, 392.23, 184.11, 375.06, 832.43, 19.35]
        spin_duration = 3 
        interval = 0.01
        start_time = time.time()

        ef.add_entry("Offset: ")

        while time.time() - start_time < spin_duration:
            current = random.choice(numbers)
            ef.del_entry()
            ef.add_entry(f"Offset: {current}")
            time.sleep(interval)

        final_offset = random.choice(numbers)
        ef.del_entry()
        ef.add_entry(f"Offset: {final_offset}")
        time.sleep(1)
        ef.add_entry("Offset eingestellt!", text_fill="green")
        time.sleep(0.5)
        ef.add_entry("Step: Offset im EEPROM speichern", text_fill="blue")
        time.sleep(2)
        ef.add_entry("Offset gespeichert!", text_fill="green")
        time.sleep(0.5)
        ef.del_all_entries()
        ef.add_entry("Step: EEPROM initialisieren", text_fill="blue")
        time.sleep(3)

        eeprom_values = [random.randint(0, 255) for _ in range(36)]
        ef.add_entry("EEPROM Inhalt:")

        line = ""
        for i, val in enumerate(eeprom_values, 1):
            line += f"{val:02X} "
            if i % 6 == 0 or i == len(eeprom_values):
                ef.add_entry(line.strip())
                line = ""
                time.sleep(0.05)

        ef.add_entry("EEPROM fehlerfrei - Gerät ausliefern", text_fill="green")

    tk.Button(control_frame, text="Add Entry", command=lambda: ef.add_entry("Sample Entry")).pack(side='left', padx=5)
    tk.Button(control_frame, text="Delete Entry", command=ef.del_entry).pack(side='left', padx=5)

    threading.Thread(target=load_kithara, daemon=True).start()

    root.mainloop()