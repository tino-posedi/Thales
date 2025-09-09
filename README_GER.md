# ![thal](https://github.com/user-attachments/assets/9f7889ac-b00e-41a5-812c-60a9d9bd1635) Thales technische Komponenten
Thales gibt dem Softwareentwickler aus dem technisch-wissenschaftlichen und industriellen Bereich eine komplette und leistungsfähige Resource zur Erstellung von Programmen in der Messdatenerfassung und Auswertung als auch für Maschinensteuerung und Überwachung in die Hand.

<img width="1691" height="36" alt="image" src="https://github.com/user-attachments/assets/992e2259-6ecd-4665-8901-1df2f3d0573b" />

## 🚀 Beispiel – Meter120  

```python
import tkinter as tk
from Thales import Meter120

root = tk.Tk()
root.title("Meter120 Demo")

analogMeter = Meter120(root)
analogMeter.pack(padx=20, pady=20)

analogMeter.set_value(43.12)
analogMeter.led_g_blink()

root.mainloop()
```

---

## 📚 Komponentenübersicht  

| Komponente       | Beschreibung |
|------------------|--------------|
| **Meter120**     | Panel Meter mit 120°-Skala, einstellbarer Dämpfung, digitaler Messwertanzeige, Schleppzeiger, steuerbare LEDs, frei beschriftbar, Farben frei wählbar |
| **Meter180**     | Panel Meter mit 180°-Skala, einstellbarer Dämpfung, digitaler Messwertanzeige, Schleppzeiger, steuerbare LEDs, frei beschriftbar, Farben frei wählbar |
| **Meter270**     | Panel Meter mit 270°-Skala, einstellbarer Dämpfung, digitaler Messwertanzeige, frei beschriftbar, Farben frei wählbar |
| **Meter360**     | Panel Meter mit 360°-Skala, zwei unabhängige Skalen und Zeiger, Over/Under-Anzeige, einstellbare Skalenteilung, Farben frei wählbar |
| **MeterPanelV**  | Vertikales Panel Meter, frei beschriftbar, steuerbare LEDs, digitale Messwertanzeige, Erscheinungsbild in weiten Grenzen anpassbar |
| **MeterPanelH**  | Horizontales Panel Meter, frei beschriftbar, steuerbare LEDs, Kolorierungen frei wählbar, einstellbare Skalenteilung |
| **SevSeg**       | Siebensegmentanzeige mit zwei steuerbaren LEDs und Einheitsanzeige, Erscheinungsbild anpassbar |
| **FullSevSeg**   | Einfache Siebensegmentanzeige, alle Kolorierungen frei wählbar |
| **SevSegSpin**   | Daumenradschalter mit Siebensegmentanzeige, mit/ohne Anschlag |
| **TextSpin**     | Spin Element mit beliebig vielen Texten, mit/ohne Anschlag |
| **SlideButton**  | Schiebeschalter mit beliebiger Beschriftung und Farben |
| **Slider**       | Schieberegler ohne Raststellungen, beliebige Anfangs- und Endwerte |
| **SelectSlide**  | Schieberegler mit bis zu 20 Raststellungen, frei beschriftbar |
| **DetSlider**    | Schieberegler mit beliebig vielen Raststellungen, beliebige Anfangs- und Endwerte, horizontal und vertikal, Erscheinungsbild flexibel |
| **StatusIndicator** | Schalter als Ersatz für Checkbox/Radio, LED-Farbe, Größe und Erscheinungsbild frei anpassbar |
| **GlowIndicator** | LED-Anzeigeeinheit mit Text links/rechts positionierbar |
| **Poti270**      | Potentiometer mit frei wählbaren Anfangs-/Endwerten und Skalenteilung |
| **Poti10K**      | Doppelpotentiometer: äußerer Knopf 270°, innerer Knopf 3600°, Anfangs-/Endwerte frei wählbar, beschriftbar |
| **Selector270**  | Drehschalter mit beliebig vielen Raststellungen |
| **BoxLine**      | Anzeigeeinheit für binäre Informationen, horizontal/vertikal, Bit-Reihenfolge umkehrbar |
| **LogView**      | Logfenster für Echtzeit-Textmeldungen, ideal für Ereignisprotokolle und Diagnosedaten |
| **Bevel3D**      | Basis-Element als Hintergrund, vertieft oder erhöht |
| **RollBar**      | Auf- und abrollbare Panels, Größe und Farben flexibel |
| **TransparentLabel** | Schriftzug in 1°-Schritten drehbar, frei wählbare Fonts, Farben, Größen |
| **FlashLabel**   | Farbiges Textfeld mit optionalem Blinkeffekt, beliebiger Text und Schriftart, ideal für Statusanzeigen |
| **StrEdit**      | Ausgabefeld für digitale Instrumente/Datenanzeigen |
| **GlyphButton**  | Schaltfläche mit Text und optionalem Glyph |
| **ArrowSpin**    | 360°-Pfeilanzeige mit vorgebbarer Richtung und Geschwindigkeit |
| **LoadingBar**   | Fortschrittsbalken (Prozent oder reale Werte), Erscheinungsbild frei gestaltbar |
| **Compass**      | Kompass mit digitaler Anzeige von Ist-Kurs und Abweichung |
| **AlphaBar**     | Tastaturersatz für tastaturlose Systeme |
| **DigiTime**     | Digitale Uhrzeitanzeige, Kolorierungen frei wählbar |
| **MagicEye**     | Bar-Graph mit einstellbaren Anfangs-/Endwerten, für einfache Spektrumanzeige geeignet |
| **Logicana**     | Leistungsfähige Komponente zur Darstellung/Analyse digitaler Daten, Kanäle abschaltbar |
| **Oscillo**      | Vollwertige Oszilloskop-Komponente, frei einstellbar |
| **xyGraph**      | Fortlaufende Darstellung eingehender Messwerte, bis zu bestimmter Geschwindigkeit echtzeitfähig |
| **StatChart**    | Diagramm-Element zur grafischen Darstellung von Daten, Darstellung konfigurierbar |
| **CurveSynth**   | Konfigurierbarer Kurveneditor und Chartwidget zur interaktiven Datenvisualisierung |
| **BitWin**       | Kleines Tool Fenster, ähnlich einem Hint, zum Anzeigen von mauszeigerabhängigen Informationen. |
| **SmartTimer**   | Timer-Komponente mit unbegrenzter Zahl an Kanälen |
| **COMPort**      | Serielle Kommunikation (Port, Baudrate, Parität, Daten-/Stoppbits, Timeout), asynchrones Lesen, Schreiben, Portverwaltung |
| **PlaySnd**      | Audioausgabe für Dateien, geeignet für Sprachausgabe, Meldungen, Warnungen |
| **Iconize**      | Startet Programm als Taskleisten-Icon oder unsichtbar |
| **FormLang**     | Mehrsprachen-Modul für automatische Textübersetzung von Widgets |
| **FormSize**     | Größenbegrenzung für Formulare (min./max. unabhängig wählbar) |
| **IniEdit**      | Lesen/Schreiben von Windows-`.ini`-Dateien, unterstützt beim Erstellen und Verändern |
| **VersInfo**     | Komponente für Version/Programminfo, ergänzt Fenstertitel um Version, Firma, Autor; Werte zur Laufzeit änder-/abrufbar |
| **Spy**          | Gag Komponente, die Augen folgen immer dem Mauskursor |
