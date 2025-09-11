# ![thal](https://github.com/user-attachments/assets/9f7889ac-b00e-41a5-812c-60a9d9bd1635) Thales tehničke komponente
Thales daje softverskom inženjeru iz tehničko-znanstvenog i industrijskog područja kompletan i snažan resurs za izradu programa u prikupljanju i obradi mjernih podataka, kao i za upravljanje strojevima te nadzor.

<img width="1728" height="38" alt="image" src="https://github.com/user-attachments/assets/518a2893-aa5d-4730-9f67-6182430e32f6" />

## 🚀 Primjer – Meter120  

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

## 📚 Pregled komponenti  

| Komponenta       | Opis |
|------------------|--------------|
| **Meter90**      | Panel mjerač s 90° skalom, podesivim prigušenjem, digitalnim prikazom mjerenja, upravljivim LED-icama, slobodno opisiv, boje po izboru |
| **Meter120**     | Panel mjerač s 120° skalom, podesivim prigušenjem, digitalnim prikazom mjerenja, kazaljkom, upravljivim LED-icama, slobodno opisiv, boje po izboru |
| **Meter180**     | Panel mjerač s 180° skalom, podesivim prigušenjem, digitalnim prikazom mjerenja, kazaljkom, upravljivim LED-icama, slobodno opisiv, boje po izboru |
| **Meter270**     | Panel mjerač s 270° skalom, podesivim prigušenjem, digitalnim prikazom mjerenja, slobodno opisiv, boje po izboru |
| **Meter360**     | Panel mjerač s 360° skalom, dvije neovisne skale i kazaljke, Over/Under prikaz, podesiva podjela skale, boje po izboru |
| **MeterPanelV**  | Vertikalni panel mjerač, slobodno opisiv, upravljive LED-ice, digitalni prikaz mjerenja, izgled u širokim granicama prilagodljiv |
| **MeterPanelH**  | Horizontalni panel mjerač, slobodno opisiv, upravljive LED-ice, slobodan izbor boja, podesiva podjela skale |
| **SevSeg**       | Sedmosegmentni prikaz s dvije upravljive LED-ice i prikazom jedinice, izgled prilagodljiv |
| **FullSevSeg**   | Jednostavan sedmosegmentni prikaz, slobodan izbor svih boja |
| **SevSegSpin**   | Kotačić s prikazom na sedmosegmentnom displeju, s/bez graničnika |
| **TextSpin**     | Spin element s proizvoljno mnogo tekstova, s/bez graničnika |
| **SlideButton**  | Klizni prekidač s proizvoljnim natpisom i bojama |
| **Slider**       | Klizač bez graničnih položaja, proizvoljni početni i krajnji vrijednosni raspon |
| **SelectSlide**  | Klizač s do 20 graničnih položaja, slobodno opisiv |
| **DetSlider**    | Klizač s proizvoljno mnogo graničnih položaja, proizvoljni raspon, horizontalno i vertikalno, izgled fleksibilan |
| **StatusIndicator** | Prekidač kao zamjena za checkbox/radio, boja LED-ice, veličina i izgled prilagodljivi |
| **GlowIndicator** | LED prikazna jedinica s tekstom lijevo/desno |
| **Poti270**      | Potenciometar s proizvoljno odabranim rasponom i podjelom skale |
| **Poti10K**      | Dvostruki potenciometar: vanjski gumb 270°, unutarnji 3600°, raspon slobodno odabran, opisiv |
| **Selector270**  | Rotacijski prekidač s proizvoljno mnogo graničnih položaja |
| **BoxLine**      | Prikaz bit informacija, horizontalno/vertikalno, redoslijed bitova obrnut po želji |
| **LogView**      | Prozor za logiranje tekstualnih poruka u stvarnom vremenu, idealan za protokole događaja i dijagnostiku |
| **Bevel3D**      | Osnovni element za pozadinu, udubljen ili izdignut |
| **RollBar**      | Paneli koji se mogu pomicati gore/dolje, veličina i boje prilagodljivi |
| **TransparentLabel** | Natpis rotirajući u koracima od 1°, slobodan odabir fonta, boja, veličine |
| **FlashLabel**   | Obojeno tekstualno polje s opcionalnim treptanjem, proizvoljan tekst i font, idealno za statusne prikaze |
| **StrEdit**      | Izlazno polje za digitalne instrumente/prikaze podataka |
| **GlyphButton**  | Gumb s tekstom i opcionalnim simbolom |
| **ArrowSpin**    | 360° prikaz strelice s unaprijed zadanom brzinom i smjerom |
| **LoadingBar**   | Traka napretka (postotci ili realne vrijednosti), izgled prilagodljiv |
| **Compass**      | Kompas s digitalnim prikazom kursa i odstupanja |
| **AlphaBar**     | Zamjena za tipkovnicu u sustavima bez fizičke tipkovnice |
| **DigiTime**     | Digitalni prikaz vremena, boje slobodno odabrive |
| **MagicEye**     | Bar-graf s podesivim rasponom, prikladan za jednostavan spektrogram |
| **Logicana**     | Snažna komponenta za prikaz/analizu digitalnih podataka, kanali se mogu isključiti |
| **Oscillo**      | Potpuno funkcionalna osciloskopska komponenta, slobodno podesiva |
| **xyGraph**      | Kontinuirani prikaz dolaznih mjernih vrijednosti, do određene brzine u realnom vremenu |
| **StatChart**    | Dijagram za grafički prikaz podataka, izgled konfigurabilan |
| **CurveSynth**   | Konfigurabilni uređivač krivulja i grafička komponenta za interaktivnu vizualizaciju podataka |
| **BitWin**       | Mali prozorčić (hint) za prikaz informacija ovisnih o pokazivaču miša |
| **SmartTimer**   | Timer komponenta s neograničenim brojem kanala |
| **COMPort**      | Serijska komunikacija (port, baudrate, paritet, podatkovni/stops bitovi, timeout), asinkrono čitanje i pisanje, upravljanje portom |
| **PlaySnd**      | Reprodukcija zvuka iz datoteka, pogodna za govor, obavijesti, upozorenja |
| **Iconize**      | Pokreće program kao ikonu u programskoj traci ili nevidljivo |
| **FormLang**     | Modul za više jezika s automatskim prevođenjem tekstova komponenata |
| **FormSize**     | Ograničenje veličine prozora (min./max. nezavisno podesivo) |
| **IniEdit**      | Čitanje/pisanje Windows-`.ini` datoteka, pomaže pri stvaranju i izmjeni |
| **VersInfo**     | Komponenta za verziju/programske informacije, dodaje naslovu prozora verziju, firmu, autora; vrijednosti se mogu mijenjati/čitati u radu |
| **Spy**          | Gag komponenta – oči uvijek prate pokazivač miša |
