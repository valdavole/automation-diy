# Automation DIY — Simulátor motoru a vozidla

*[Read in English](README.md)*

Open-source simulátor stavby motoru, virtuálního dyna, dynamiky vozidla a času na kolo, inspirovaný žánrem her ve stylu „Automation“.

Postav motor od klikové hřídele nahoru, otestuj ho na virtuálním dynu, prověř chlazení při ručním plynu, změř zrychlení 0–100 km/h nebo 0–60 mph a maximální rychlost a nakonec pošli auto na kompletně simulovanou testovací dráhu dlouhou 3,605 km. Zvuk motoru se generuje procedurálně a živě reaguje na otáčky, plyn, počet válců, typ plnění i klikovou hřídel.

> **Aktuální verze: v4.8.5 — Fullscreen & Settings Update + Tweaks**

![screenshot placeholder](docs/screenshot1.png)

## Funkce

- **Fullscreen rozhraní v jediném okně** se stálým levým menu, vloženými simulačními obrazovkami, chybovými overlayi a ovládáním přes F11/ESC
- **Centrální panel Nastavení** pro načítání a ukládání buildů, změnu jazyka, přepnutí mezi km/h a mph a bezpečné ukončení simulátoru
- **Stavba motoru a vozidla na 7 záložkách**: Block, Bottom End, Top End, Aspiration, Fuel & Tune, Exhaust, Drivetrain
- **Fyzikálně založená dyno simulace** s živým vloženým grafem momentu a výkonu a telemetrií otáček, momentu a výkonu
- **Nezávislé modely selhání motoru**:
  - mechanické přetočení podle nejslabší klikové hřídele, ojnic nebo pístů
  - klepání a detonace ovlivněné kompresí, plnicím tlakem, předstihem, AFR, palivovou mapou, oktanovým číslem, vstřikováním, materiálem hlavy a technologickou úrovní
- **Telemetrie s ručním plynem** s živou teplotou chladicí kapaliny a možností prasknutí těsnění pod hlavou při přehřátí
- **Simulace 0–100 km/h / 0–60 mph a maximální rychlosti**, která zohledňuje:
  - ztráty pohonu a rozdíly mezi FWD, RWD a AWD
  - podélný přenos hmotnosti
  - limit přilnavosti pneumatik
  - čelní plochu, součinitel odporu, poloměr kola, valivý odpor a aerodynamický přítlak
  - elektronický omezovač rychlosti i maximálku omezenou převody a otáčkami
  - živý převod jednotek, který mění zobrazení a cíl zrychlení, nikoliv fyziku vozidla
- **Volitelné jemné nastavení jednotlivých převodů** pro převodovky se 4–8 stupni
  - při vypnuté volbě zůstávají původní automatické sady převodů
  - po zapnutí lze každý převod upravit samostatně
  - vestavěné presety používají ve výchozím stavu automatické převody, takže si zachovávají své zavedené výsledky
- **Testovací dráha dlouhá 3,605 km s letmým měřeným kolem**
  - tři měřené sektory
  - živé zobrazení rychlosti, převodu, sektoru a času kola
  - brzdné zóny, rychlostní limity v zatáčkách, třecí kružnice pneumatik, akcelerace, odpor vzduchu, přítlak a časové ztráty při řazení
  - jedna společná geometrie pro fyziku i vykreslení, takže zobrazený okruh je přesně ten, který simulátor počítá
- **Procedurálně generovaný zvuk motoru** bez nahraných vzorků
- **Vestavěné tooltips** vysvětlující inženýrský vliv jednotlivých parametrů
- **Bezpečné uložení a načtení** přenositelných JSON konfigurací motoru a vozidla včetně kompatibilních výchozích hodnot a přísnější validace starších či poškozených souborů
- **Předvolby inspirované reálnými vozy** pro rychlý začátek
- **Dvojjazyčné UI**: čeština a angličtina, přepínatelné za chodu v Nastavení
- **Volitelné jednotky rychlosti**: km/h s měřením 0–100 km/h, nebo mph s měřením 0–60 mph

![screenshot placeholder](docs/screenshot2.png)

![screenshot placeholder](docs/screenshot3.png)

![screenshot placeholder](docs/screenshot4.png)

## Jak začít

### Varianta A — Předkompilované Windows exe

Stáhni nejnovější `.exe` ze stránky [Releases](../../releases) a spusť ho přímo. Instalace Pythonu není potřeba.

> **Známý problém:** při prvním spuštění může antivirus, například Microsoft Defender nebo AVG, krátce zamknout soubor během kontroly nepodepsaného single-file exe. To se může projevit jednorázovou chybou při spuštění. Po dokončení prvního skenu obvykle stačí aplikaci spustit znovu.

### Varianta B — Spuštění ze zdrojového kódu

Vyžaduje Python 3.10+.

```bash
pip install numpy matplotlib sounddevice
python automation_diy_4.8.5.py
```

`tkinter` je součástí většiny standardních instalací Pythonu pro Windows. Na některých linuxových distribucích může být potřeba doinstalovat ho přes systémového správce balíčků.

`sounddevice` a jeho PortAudio backend jsou volitelné. Pokud nejsou dostupné, simulátor běží normálně, pouze jsou vypnuté ovládací prvky živého zvuku motoru.

Aplikace se spouští v režimu celé obrazovky. Klávesou **F11** fullscreen zapneš nebo vypneš. **Esc** zavře overlay, vrátí tě z jiného režimu do stavby motoru nebo při otevřené stavbě opustí fullscreen. Načítání, ukládání, jazyk, jednotky rychlosti a ukončení aplikace najdeš v levém panelu **Nastavení**.

## Typický postup

1. Vyber preset nebo začni od výchozího buildu.
2. Nastav motor napříč sedmi záložkami.
3. Spusť **1. Dyno Pull** a sleduj živý graf a telemetrii.
4. Na obrazovce Dyna si prohlédni dokončené křivky momentu a výkonu.
5. Volitelně spusť **2. Ruční plyn**.
6. Spusť **3. Zkušební jízdu** pro 0–100 km/h nebo 0–60 mph a maximální rychlost.
7. Spusť **4. Testovací dráhu** pro srovnatelný čas letmého kola.
8. Až budeš s buildem spokojený, otevři **Nastavení → Uložit motor / vozidlo jako...**.

Kompletní vysvětlení rozhraní, Nastavení, jednotek rychlosti, všech záložek, simulačních režimů, modelů selhání, vlastních převodů a testovací dráhy najdeš v **[NAVOD.md](docs/NAVOD.md)**.

## Rozsah simulace

Automation DIY je přístupný herní inženýrský simulátor, nikoliv náhrada profesionálního softwaru pro simulaci spalovacího cyklu, CFD, víceprvkovou dynamiku vozidla nebo motorsportovou simulaci času na kolo.

Výsledky jsou deterministické a vhodné pro porovnávání buildů uvnitř simulátoru. Reálné hodnoty ovlivňují také jevy, které model neřeší, například teplota pneumatik, geometrie podvozku, povrch vozovky, počasí, chování řidiče, přechodová odezva turba, výrobní tolerance a podrobný průběh spalování.

## Upozornění

Některé vestavěné předvolby odkazují na reálné výrobce a modely jako na ilustrativní výkonnostní srovnání. Jde o neoficiální fanouškovské aproximace vytvořené pro vzdělávací a zábavní účely. Projekt není s uvedenými výrobci propojen, podporován jimi ani z jejich dat přímo odvozen.

## Poděkování

Inspirováno žánrem hry *Automation: The Car Company Tycoon Game*. Jde o nezávislý hobby projekt bez jakékoli spojitosti s touto hrou nebo jejími vývojáři.

## Přispívání

Projekt vyrostl z jednoho postupně rozvíjeného skriptu přes mnoho iterací, takže současný kód stále žije převážně v jednom velkém souboru.

Pull requesty jsou vítány. Rozdělení projektu například na moduly `physics.py`, `audio.py`, `gui.py`, `track.py` a `presets.py` by bylo hodnotným prvním příspěvkem ke snadnější údržbě a testování.
