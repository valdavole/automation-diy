# Automation DIY — Simulátor motoru a vozidla

*[Read in English](README.md)*

Domácí, open-source simulátor stavby motoru a dyna, inspirovaný žánrem her jako "Automation". Postav motor od klikové hřídele nahoru, otestuj ho na virtuálním dynu, prožeň ho testem chlazení s ručním plynem, a nakonec si zajezdi na 0–100 km/h — se zvukem motoru, který se generuje procedurálně a reaguje v reálném čase na otáčky, plyn, počet válců i typ klikové hřídele.

![screenshot placeholder](docs/screenshot.png)

## Funkce

- **Stavba motoru na 7 záložkách**: Block, Bottom End, Top End, Aspiration, Fuel & Tune, Exhaust, Drivetrain
- **Fyzikálně založená dyno simulace** — výpočet křivky točivého momentu a výkonu, se dvěma nezávislými módy selhání: mechanické přetočení (klikovka/ojnice/písty, vždy vyhraje nejslabší díl) a detonační hoření/klepání (komprese, předstih, směs AFR, oktanové číslo, materiál hlavy)
- **Telemetrie s ručním plynem** — drž plynový pedál a sleduj teplotu chladicí kapaliny; přehřátí prasklé těsnění hlavy
- **Zkušební jízda 0–100 km/h** — přenos váhy, trakční model FWD/RWD/AWD, limit přilnavosti pneumatik, řazení, launch control, detekce maximální rychlosti
- **Procedurálně generovaný zvuk motoru** — žádné nahrávky, waveform se syntetizuje živě podle specifikace tvého motoru
- **Vestavěné tooltips**, které vysvětlují reálný inženýrský dopad každého jednotlivého parametru
- **Uložení/Načtení** konfigurace motoru jako přenositelný JSON soubor
- **Předvolby inspirované reálnými vozy** pro rychlý start
- **Dvojjazyčné UI**: čeština / angličtina, přepínatelné kdykoliv za chodu

## Jak začít

### Varianta A — Předkompilovaný Windows exe
Stáhni nejnovější `.exe` ze stránky [Releases](../../releases) a spusť ho přímo. Instalace Pythonu není potřeba.

> **Známý problém:** při prvním spuštění tvůj antivirus (Defender, AVG apod.) může krátce zamknout soubor, který právě poprvé skenuje, což se může projevit jednorázovou chybou. Je to známý vedlejší efekt nepodepsaných single-file exe souborů — pokud se to stane, prostě appku spusť znovu; jakmile antivirus soubor jednou proskenuje a zapamatuje si ho, problém se znovu neobjeví.

### Varianta B — Spuštění ze zdrojového kódu
Vyžaduje Python 3.10+.

```bash
pip install numpy matplotlib sounddevice
python engine_sim.py
```

`sounddevice` (a jeho PortAudio backend) je volitelný — pokud není dostupný, appka běží normálně, jen s vypnutým tlačítkem zvuku místo živého zvuku motoru.

## Jak appku ovládat

Kompletní návod ke všem záložkám, k postupu dyno/telemetrie/zkušební jízda a k modelům selhání najdeš v **[NAVOD.md](docs/NAVOD.md)**.

## Upozornění

Některé vestavěné předvolby odkazují na reálné výrobce a modely (jako ilustrativní výkonnostní srovnání). Jde o neoficiální, fanouškovské přiblížení vytvořené pro vzdělávací účely, bez jakékoli spojitosti s uvedenými výrobci ani jejich podpory.

## Poděkování

Inspirováno žánrem hry *Automation: The Car Company Tycoon Game*. Jde o nezávislý hobby projekt bez jakékoli spojitosti s touto hrou nebo jejími vývojáři.

## Přispívání

Projekt vyrostl z jednoho postupně vyvíjeného skriptu přes mnoho iterativních verzí, takže současný kód žije v jednom velkém souboru. Pull requesty jsou vítány — rozdělení na moduly `physics.py` / `audio.py` / `gui.py` / `presets.py` je dobrý první příspěvek, pokud chceš pomoct s udržovatelností.
