import tkinter as tk
import serial
import serial.tools.list_ports
import threading
import queue
import time

class COMPort(tk.Frame):
    def __init__(self, master=None, port=None, baudrate=9600,
                 parity=serial.PARITY_NONE, data_bits=8, stop_bits=serial.STOPBITS_ONE,
                 timeout=1, on_data_received=None, **kwargs):
        super().__init__(master, width=0, height=0, borderwidth=0, highlightthickness=0)
        self.pack_propagate(False)

        self.port = port
        self.baudrate = baudrate
        self.parity = parity
        self.data_bits = data_bits
        self.stop_bits = stop_bits
        self.timeout = timeout

        self.on_data_received = on_data_received

        self._serial = None
        self._running = False
        self._thread = None
        self._read_queue = queue.Queue()

    def open_port(self):
        if not self.port:
            raise ValueError("Port property not set")
        self._serial = serial.Serial(
            port=self.port,
            baudrate=self.baudrate,
            bytesize=self.data_bits,
            parity=self.parity,
            stopbits=self.stop_bits,
            timeout=self.timeout
        )
        self._running = True
        self._thread = threading.Thread(target=self._read_loop, daemon=True)
        self._thread.start()

    def close_port(self):
        self._running = False
        if self._thread:
            self._thread.join(timeout=1)
        if self._serial and self._serial.is_open:
            self._serial.close()
        self._serial = None

    def write(self, data: str):
        if self._serial and self._serial.is_open:
            self._serial.write(data.encode('utf-8'))
        else:
            raise ConnectionError("Port not open")

    def read_string(self):
        """Return all currently received data as a string"""
        data = ""
        while not self._read_queue.empty():
            data += self._read_queue.get()
        return data

    def read_line(self):
        """Return one line from the read buffer (newline terminated)"""
        line = ""
        while not self._read_queue.empty():
            chunk = self._read_queue.get()
            line += chunk
            if "\n" in line:
                parts = line.split("\n", 1)
                remainder = parts[1]
                self._read_queue.put(remainder)
                return parts[0] + "\n"
        return None

    def get_available_ports(self):
        return [port.device for port in serial.tools.list_ports.comports()]

    def is_open(self):
        return self._serial.is_open if self._serial else False

    def _read_loop(self):
        while self._running and self._serial and self._serial.is_open:
            try:
                if self._serial.in_waiting > 0:
                    data = self._serial.read(self._serial.in_waiting).decode('utf-8', errors='ignore')
                    self._read_queue.put(data)
                    if self.on_data_received:
                        self.on_data_received(data)
                else:
                    time.sleep(0.01)
            except serial.SerialException:
                break