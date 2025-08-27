import tkinter as tk
import configparser
import os

class IniEdit(tk.Frame):
    def __init__(self, master=None, ini_file="file.ini", **kwargs):
        super().__init__(master, width=0, height=0, borderwidth=0, highlightthickness=0, **kwargs)
        self.pack_propagate(False)

        self.ini_file = ini_file
        self.config = configparser.ConfigParser()

        if os.path.exists(self.ini_file):
            self.config.read(self.ini_file)
        else:
            with open(self.ini_file, 'w') as f:
                self.config.write(f)

    def read(self, section, key, fallback=None):
        return self.config.get(section, key, fallback=fallback)

    def write(self, section, key, value):
        if not self.config.has_section(section):
            self.config.add_section(section)
        self.config.set(section, key, value)
        with open(self.ini_file, 'w') as f:
            self.config.write(f)

    def delete_key(self, section, key):
        if self.config.has_section(section) and self.config.has_option(section, key):
            self.config.remove_option(section, key)
            with open(self.ini_file, 'w') as f:
                self.config.write(f)

    def delete_section(self, section):
        if self.config.has_section(section):
            self.config.remove_section(section)
            with open(self.ini_file, 'w') as f:
                self.config.write(f)

    def get_sections(self):
        return self.config.sections()

    def get_keys(self, section):
        if self.config.has_section(section):
            return self.config.options(section)
        return []

def main():
    root = tk.Tk()
    root.title("INI Manager Demo")

    ini_mgr = IniEdit(root, ini_file="demo.ini")

    ini_mgr.write("Settings", "volume", "75")
    ini_mgr.write("Settings", "brightness", "50")

    print("Volume:", ini_mgr.read("Settings", "volume"))
    print("Brightness:", ini_mgr.read("Settings", "brightness"))

    btn = tk.Button(root, text="Quit", command=root.destroy)
    btn.pack(pady=20)

    root.mainloop()

if __name__ == "__main__":
    main()
