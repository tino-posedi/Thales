import configparser
import tkinter as tk

class FormLang(tk.Frame):
    def __init__(self, master=None, config_path="config.ini", default_lang="en", available_langs=None, **kwargs):
        super().__init__(master, width=0, height=0, borderwidth=0, highlightthickness=0, **kwargs)
        self.pack_propagate(False) 

        self.config = configparser.ConfigParser()
        self.config.read(config_path)
        self.languages = available_langs if available_langs else ["en", "de", "fr"]
        self.current_lang = default_lang if default_lang in self.languages else self.languages[0]

    def translate(self, section, key):
        full_key = f"{key}_{self.current_lang}"
        return self.config.get(section, full_key, fallback=f"[{key}]")

    def switch_language(self):
        index = self.languages.index(self.current_lang)
        self.current_lang = self.languages[(index + 1) % len(self.languages)]

    def set_language(self, lang_code):
        if lang_code in self.languages:
            self.current_lang = lang_code
        else:
            raise ValueError(f"Language '{lang_code}' is not supported.")

    def get_language(self):
        return self.current_lang
