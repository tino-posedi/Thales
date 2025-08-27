import tkinter as tk
import threading
import os
import pyaudio
from pydub import AudioSegment

class PlaySnd(tk.Frame):
    def __init__(self, master=None, audio_file=None, **kwargs):
        super().__init__(master, width=0, height=0, borderwidth=0, highlightthickness=0, **kwargs)
        self.pack_propagate(False)
        self._audio_file = None
        self._audio_segment = None
        self._thread = None

        if audio_file:
            self.set_audio_file(audio_file)

    def set_audio_file(self, file_path):
        if not os.path.isfile(file_path):
            raise FileNotFoundError(f"Audio file not found: {file_path}")
        if not file_path.lower().endswith(".wav"):
            raise ValueError("Only .wav files are supported")
        self._audio_file = file_path
        self._audio_segment = AudioSegment.from_wav(file_path)

    def play(self, audio_file=None):
        if audio_file:
            self.set_audio_file(audio_file)
        if not self._audio_segment:
            return
        if self._thread and self._thread.is_alive():
            return
        self._thread = threading.Thread(target=self._play_internal, daemon=True)
        self._thread.start()

    def _play_internal(self):
        try:
            p = pyaudio.PyAudio()

            converted = self._audio_segment.set_frame_rate(44100).set_channels(2).set_sample_width(2)

            raw_data = converted.raw_data
            channels = 2
            sample_width = 2
            frame_rate = 44100

            stream = p.open(format=p.get_format_from_width(sample_width),
                            channels=channels,
                            rate=frame_rate,
                            output=True)

            chunk_size = 8196
            for i in range(0, len(raw_data), chunk_size):
                stream.write(raw_data[i:i+chunk_size])

            stream.stop_stream()
            stream.close()
            p.terminate()
        except Exception as e:
            print(f"Error playing .wav file: {e}")

if __name__ == "__main__":
    import tkinter as tk

    def on_play():
        announcer.play()
        
    def on2_play():
        announcer2.play()

    root = tk.Tk()
    root.title("AudioAnnouncer with pydub + pyaudio")

    announcer = PlaySnd(root, audio_file="DEMO.wav")
    announcer.pack()
    
    announcer2 = PlaySnd(root, audio_file="ACHTNG.wav")
    announcer2.pack()

    play_btn = tk.Button(root, text="Play .WAV", command=on_play)
    play_btn.pack(pady=10)
    
    play2_btn = tk.Button(root, text="Play Achtung", command=on2_play)
    play2_btn.pack(pady=10)

    root.mainloop()
