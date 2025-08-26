# Thales Technical Components  

Thales provides software developers in the technical-scientific and industrial fields with a powerful and complete resource for creating programs for data acquisition and evaluation as well as for machine control and monitoring.  

<img width="1585" height="40" alt="image" src="https://github.com/user-attachments/assets/7d183bbc-5607-49ec-9ce1-c57e9dc7d61a" />

## 🚀 Example – Meter120  

```python
import tkinter as tk
from Thales import Meter120

root = tk.Tk()
root.title("Meter120 Demo")

analogMeter = Meter120(root)
analogMeter.pack()

analogMeter.set_value(43.12)
analogMeter.led_g_blink()

root.mainloop()
```

---

## 📚 Component Overview  

| Component        | Description |
|------------------|-------------|
| **Meter120**     | Panel meter with 120° scale, adjustable damping, digital value display, drag pointer, controllable LEDs, freely labelable, customizable colors |
| **Meter180**     | Panel meter with 180° scale, adjustable damping, digital value display, drag pointer, controllable LEDs, freely labelable, customizable colors |
| **Meter270**     | Panel meter with 270° scale, adjustable damping, digital value display, freely labelable, customizable colors |
| **Meter360**     | Panel meter with 360° scale, two independent scales and pointers, over/under indicator, adjustable scale division, customizable colors |
| **MeterPanelV**  | Vertical panel meter, freely labelable, controllable LEDs, digital value display, appearance highly customizable |
| **MeterPanelH**  | Horizontal panel meter, freely labelable, controllable LEDs, customizable colors, adjustable scale division |
| **SevSeg**       | Seven-segment display with two controllable LEDs and unit display, customizable appearance |
| **FullSevSeg**   | Simple seven-segment display, all colors customizable |
| **SevSegSpin**   | Thumbwheel switch with seven-segment display, with/without stop |
| **SlideButton**  | Slide switch with arbitrary labeling and colors |
| **Slider**       | Slider without detents, arbitrary start and end values |
| **SelectSlide**  | Slider with up to 20 detents, freely labelable |
| **DetSlider**    | Slider with any number of detents, arbitrary start and end values, horizontal or vertical, highly customizable appearance |
| **StatusIndicator** | Switch as replacement for checkbox/radio button, LED color, size, and appearance highly customizable |
| **GlowIndicator** | LED indicator unit, text can be positioned left/right |
| **Poti270**      | Potentiometer with freely selectable start/end values and scale division |
| **Poti10K**      | Dual potentiometer: outer knob 270°, inner knob 3600°, freely selectable start/end values, labelable |
| **Selector270**  | Rotary switch with any number of detents |
| **BoxLine**      | Display unit for binary information, horizontal/vertical, bit order reversible |
| **LogView**      | Log window for real-time text messages, ideal for event logs and diagnostic data |
| **Bevel3D**      | Base element, usable as background, recessed or raised |
| **RollBar**      | Expandable/collapsible panels, size and colors highly customizable |
| **TransparentLabel** | Label rotatable in 1° steps, freely selectable fonts, colors, sizes |
| **FlashLabel**   | Colored text field with optional blinking effect, arbitrary text and font, ideal as status indicator |
| **StrEdit**      | Output field, usable as digital instrument/data display |
| **GlyphButton**  | Button with text and optional glyph |
| **ArrowSpin**    | 360° arrow display, direction and speed configurable |
| **LoadingBar**   | Progress bar (percent or real values), customizable appearance |
| **Compass**      | Compass with digital display of current course and deviation |
| **AlphaBar**     | Keyboard replacement for keyboardless systems |
| **DigiTime**     | Digital clock display, customizable colors |
| **MagicEye**     | Bar graph with adjustable start/end values, suitable for simple spectrum display |
| **Logicana**     | Powerful component for displaying/analyzing digital data, channels can be disabled |
| **Oscillo**      | Fully functional oscilloscope component, fully configurable |
| **xyGraph**      | Continuous display of incoming measurement values, real-time capable up to a certain speed |
| **StatChart**    | Chart component for graphical data display, configurable presentation |
| **SmartTimer**   | Timer component with unlimited number of channels |
| **COMPort**      | Serial communication (port, baud rate, parity, data/stop bits, timeout), asynchronous reading, writing, port management |
| **PlaySnd**      | Audio output for files, suitable for speech output, messages, warnings |
| **Iconize**      | Starts program as taskbar icon or completely invisible |
| **FormLang**     | Multi-language module for automatic text translation of widgets |
| **FormSize**     | Size limitation for forms (min/max independently selectable) |
| **IniEdit**      | Read/write Windows `.ini` files, supports creating and modifying entries |
| **VersInfo**     | Version/program info component, extends window title with version, company, author; values changeable/retrievable at runtime |
