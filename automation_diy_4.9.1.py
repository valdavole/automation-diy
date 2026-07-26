import time
import sys
import os
import platform
import threading
import math
import wave
import tempfile
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import json

is_windows = platform.system() == "Windows"
if is_windows:
    import winsound

SOUND_AVAILABLE = False
SOUND_ERROR = ""
try:
    import sounddevice as sd
    SOUND_AVAILABLE = True
except (ImportError, OSError) as exc:
    SOUND_ERROR = str(exc)

# --- LOKALIZAČNÍ SLOVNÍK (CZ / EN) ---
T = {
    "cz": {
        "app_title": "Automation DIY - Verze 4.9.1 (Localization & Tooltip Stability Update)",
        "menu_file": "Soubor",
        "menu_settings": "⚙  NASTAVENÍ",
        "settings_title": "NASTAVENÍ SIMULÁTORU",
        "settings_files": "VOZIDLA A MOTORY",
        "settings_language": "JAZYK",
        "settings_speed_units": "JEDNOTKY RYCHLOSTI",
        "settings_close": "ZAVŘÍT NASTAVENÍ",
        "settings_quit": "UKONČIT SIMULÁTOR",
        "settings_kmh": "Kilometry za hodinu (km/h)",
        "settings_mph": "Míle za hodinu (mph)",
        "settings_audio": "ZVUK A VOLITELNÉ MODULY",
        "sound_ready": "Živý zvuk motoru je připraven.",
        "sound_missing": "Zvukový modul není dostupný. Ruční plyn i zkušební jízda fungují dál v tichém režimu.",
        "sound_help": "NÁVOD K INSTALACI ZVUKU",
        "sound_help_title": "ŽIVÝ ZVUK MOTORU",
        "sound_help_body": "Simulátor je plně použitelný i bez zvuku. Pro živý zvuk otevři terminál ve složce projektu a spusť:\n\npip install -r requirements.txt\n\nPokud je sounddevice už nainstalovaný, ověř funkční PortAudio a výchozí výstupní zvukové zařízení. Potom simulátor restartuj.",
        "sound_silent_sidebar": "⚠  ZVUK: TICHÝ REŽIM",
        "ui_dyno_ready": "Připraveno k měření",
        "ui_live_telemetry": "ŽIVÁ TELEMETRIE",
        "ui_ready": "Připraveno",
        "ui_dyno_running": "Měření probíhá…",
        "ui_dyno_cancelled": "Měření bylo přerušeno",
        "ui_engine_control": "OVLÁDÁNÍ MOTORU",
        "ui_throttle_instruction": "Podrž tlačítko pro plný plyn. Uvolněním motor necháš spadnout na volnoběh.",
        "ui_mode_exit_hint": "ESC nebo levé menu bezpečně ukončí režim.",
        "ui_speed": "RYCHLOST",
        "ui_gear": "PŘEVOD",
        "ui_tcs_ready": "TCS PŘIPRAVENO",
        "ui_tcs_ok": "TCS OK",
        "ui_slip": "PROKLUZ",
        "ui_max": "MAX",
        "ui_track_start_finish": "START / CÍL",
        "ui_fullscreen_hint": "F11  CELÁ OBRAZOVKA",
        "ui_back_hint": "ESC  ZPĚT",
        "menu_load": "Načíst motor / vozidlo (.json)...",
        "menu_save": "Uložit motor / vozidlo jako (.json)...",
        "menu_quit": "Ukončit",
        "lbl_engine_name": "Název vozu/motoru:",
        "tab_1": "1. Blok motoru", "tab_2": "2. Spodek motoru", "tab_3": "3. Hlava a rozvody",
        "tab_4": "4. Plnění", "tab_5": "5. Palivo a ladění", "tab_6": "6. Výfuk", "tab_7": "7. Pohon",
        
        "lbl_config": "Konfigurace:", "lbl_vangle": "Úhel V:", "lbl_cyl": "Počet válců:", "lbl_block": "Materiál bloku:",
        "lbl_bore": "Vrtání:", "lbl_stroke": "Zdvih:", "lbl_rad": "Účinnost chladiče:", "lbl_tech": "Technologická úroveň:", "lbl_calc_disp": "Vypočítaný objem:",
        "tt_config": "Inline (Řadový): Levný, plynulý chod, ale u mnoha válců je moc dlouhý.\nV (Vidlicový): Kompaktní, krátký, skvělý pro 6 a 8 válců.\nBoxer (Plochý): Protiběžné písty. Dokonalé vyvážení a nízké těžiště.",
        "tt_vangle": "60°: Vhodný pro V6, motor je užší.\n90°: Klasika pro V8, skvělé vyvážení rotujících hmot.\n120°: Velmi plochý motor, snižuje těžiště, ale je extrémně široký.",
        "tt_cyl": "3 až 5: Levnější, vhodné pro malé objemy.\n6 až 8: Výkonný standard, kultivovaný chod.\n10 až 16: Exotické superauta. Obrovský výkon a spotřeba.",
        "tt_block": "Cast Iron: Těžká, nezničitelná.\nAluminium (Light/Heavy/Billet): Hliník je standard. Heavy je pevnější, Light lehčí. Billet je frézovaný z jednoho kusu pro závodní nasazení.\nAlSi (Light/Heavy): Slitina bez vložek, snižuje tření.\nMagnesium: Motorsport, nejlehčí, nejnižší tření.",
        "tt_bore": "Určuje průměr pístu.\nVětší vrtání = umožňuje instalaci větších ventilů pro lepší průtok vzduchu ve vysokých otáčkách.",
        "tt_stroke": "Určuje vzdálenost, kterou píst urazí.\nVětší zdvih = masivní nárůst točivého momentu v nízkých otáčkách, ale fyzicky brání motoru dosáhnout vysokých RPM.\nSlider pokrývá běžných 50–120 mm; do pole lze pro speciální motory ručně zadat 20–150 mm.",
        "tt_rad": "Větší chladič (vysoká účinnost v %) dokáže mnohem efektivněji odvádět teplo z bloku.\nUdrží tak motor déle v zátěži bez uvaření kapaliny a destrukce těsnění.",
        "tt_tech": "Určuje technologickou éru motoru.\n60 = 70. léta (karburátory).\n100 = moderní standard (beze změny).\n115+ = špičkové high-tech motory.\nOvlivňuje celkovou účinnost, dýchání motoru, tření a odolnost proti klepání.",

        "lbl_crank": "Materiál klikovky:", "lbl_conrods": "Materiál ojnic:", "lbl_pistons": "Materiál pístů:", "lbl_bal": "Vyvažováky:", "lbl_bal_mass": "Váha vyvažováků:",
        "tt_crank": "Cast / Cast Iron Heavy: Sériovka (max 6500 RPM), Heavy verze je robustnější.\nForged / Forged Steel (Heavy/Light): Kovaná, zlatý střed pro turba (8500 RPM).\nBillet / Billet Steel Heavy: Frézovaná z jednoho kusu, přežije i 11500 RPM.\nFlat-plane: U motorů V8 naprosto změní ZVUK i charakter na moderní / vysokootáčkový!",
        "tt_conrods": "Cast (Light/Heavy): Sériovka do 6000 RPM.\nHeavy Duty: Do náklaďáků (7000 RPM).\nForged (Light/Heavy): Kované, zlatý střed (8500 RPM).\nLW Forged: Odlehčené kované (10000 RPM).\nTitanium: Nejlehčí, nejdražší (12000 RPM).",
        "tt_pistons": "Cast (Light/Heavy): Sériové (6500 RPM).\nHeavy Duty: Max 7000 RPM.\nHypereutectic Cast: Odolnější odlitek, lepší na emise a lehké turbo.\nForged (Light/Heavy): Nezbytné pro turba, odolají detonacím (8500 RPM).\nLW Forged: Superlehké (12000 RPM).\nLow Friction: Sníží spotřebu, ale nic nevydrží (7500 RPM).",
        "tt_bal": "None: Motor vibruje, je nejlehčí.\nHarmonic Damper: Guma tlumí kmity (+200 RPM limit, malé tření).\nFull Balancers: Přídavné hřídele (+500 RPM limit, ale sežerou výkon).",
        "tt_bal_mass": "Přidání protizávaží perfektně vyváží motor, což posune limit otáček nahoru, ale přidá hmotnost na rotační vrstvě, takže stoupne vnitřní tření a motor bude mít pomalejší odezvu.",

        "lbl_head_mat": "Materiál hlavy:", "lbl_springs": "Tuhost pružin:", "lbl_vvl_prof": "VVL Profil:", "lbl_vvl_rpm": "VVL Otáčky:",
        "tt_head_mat": "Cast Iron / Iron (Eco/Std/Perf): Litina drží teplo a silně ZVYŠUJE sklony ke klepání. Eco je levná, Perf má lepší flow.\nAluminium / Alu (Eco/Std/Perf): Hliník skvěle odvádí teplo (snižuje šanci na detonace).\nAlu Billet Race: Závodní, nejlepší odvod tepla a nejnižší tření.",

        "lbl_valve": "Rozvody:", "lbl_valvesn": "Ventilů na válec:", "lbl_vvt": "VVT (Časování):", "lbl_vvl": "VVL (Variabilní zdvih)",
        "lbl_cam": "Profil vačky:", "lbl_comp": "Kompresní poměr:",
        "tt_valve": "Pushrod (OHV): Vačka v bloku, těžké tyčky. Dusí se po překročení 4200 RPM.\nSOHC: 1 vačka v hlavě. Spolehlivé.\nDOHC: 2 vačky v hlavě. Perfektní pro vysoké otáčky.\nDAOHC: Přímé ovládání, závodní záležitost.",
        "tt_valvesn": "2: Skvělé pro nízké otáčky, nahoře se dusí.\n3: Kompromis.\n4: Moderní standard, ideální průtok.\n5: Extrémní výkon nahoře.",
        "tt_vvt": "None: Pevné časování.\nIntake: Mění časování sací vačky. Zlepšuje plynulost.\nAll: Variabilní sací i výfuková. Vyrovná křivku přes celé spektrum.",
        "tt_vvl": "None: Pevný zdvih.\nVVL: Variabilní zdvih - přepne na ostrou vačku v daných otáčkách.\nCVVL: Plynule variabilní - vyrovná křivku a zvýší celkovou efektivitu.",
        "tt_vvl_prof": "Určuje ostrost druhého (VVL) vačkového profilu. \n0-30: Jemný profil pro nízké otáčky.\n40-60: Sportovní.\n70-100: Závodní agresivní vačka, skvělá nahoře.",
        "tt_vvl_rpm": "Určuje přesné otáčky, při kterých systém VVL přepne z normálního profilu (Tab 3: Profil vačky) na ostrý VVL Profil.",
        "tt_springs": "Tvrdší pružiny a zdvihátka (50-100) umožní motoru točit mnohem vyšší otáčky bez 'odskakování ventilů' (Valve Float), ale přidávají tření a mírně snižují výkon.",
        "tt_cam": "Určuje dýchání motoru. Vyšší profil přesouvá výkon k omezovači a volnoběh je neklidný.",
        "tt_comp": "Vyšší komprese (10+): Motor je silnější, ale ROSTE RIZIKO DETONACE!\nNízká komprese (7-9): Nutná pro přeplňování obřím turbem.\nNafta (Diesel) tyto limity ignoruje.",

        "lbl_asp": "Typ plnění:", "lbl_tb": "Ložiska turba:", "lbl_tc": "Konfigurace:", "lbl_ic": "Velikost mezichladiče:",
        "lbl_tsize": "Velikost turba:", "lbl_tboost": "Plnicí tlak:", "lbl_sct": "Typ kompresoru:", "lbl_scp": "Řemenice / max. tlak:",
        "lbl_csize": "Velikost kompresoru:",
        "tt_asp": "NA (Atmosféra): Plynulá reakce.\nTurbo: Poháněné výfukem (má Lag).\nSupercharger: Kompresor hnaný řemenem. Okamžitá reakce.",
        "tt_tb": "Journal (Kluzná): Levná, pomalejší náběh.\nBall Bearings (Kuličková): Razantně zkracují Turbo Lag.",
        "tt_tc": "Single: Velký Lag.\nTwin: Rychlejší roztočení (méně Lagu).\nQuad: Čtyři malá turba, super rychlá reakce u velkých motorů.",
        "tt_ic": "Větší chladič zachrání motor před klepáním, ale mírně zvětšuje Turbo Lag.",
        "tt_tsize": "Velké turbo umí fouknout obrovský plnící tlak, ale roztáčí se nekonečně dlouho.",
        "tt_tboost": "Kolik barů tlaku pustíš do sání. Přes 1.5 baru to chce kvalitní palivo a kované díly!",
        "tt_sct": "Roots: Kopne hned z nuly.\nTwin-screw: Mnohem efektivnější a plynulejší.\nCentrifugal (Odstředivý): Fouká tím víc, čím rychleji točíš motor.",
        "tt_scp": "Menší řemenice = kompresor se točí rychleji = větší tlak.",
        "tt_csize": "Větší jednotka zvládne tlačit mnohem víc vzduchu ve vysokých RPM, ale odebere si obří množství výkonu motoru (parazitní ztráta) jen na to, abys s ní vůbec pootočil.",

        "lbl_fdeliv": "Vstřikování:", "lbl_inconf": "Konfig. sání:", "lbl_man": "Sací svody:", "lbl_fuel": "Druh paliva:", "lbl_afr": "Směs (AFR):",
        "lbl_ign": "Předstih:", "lbl_lim": "Omezovač RPM:",
        "lbl_carb_size": "Velikost klapky/karb.:", "lbl_fuel_map": "Mapa paliva (Směs):", "lbl_man_size": "Velikost sání:",
        "tt_fdeliv": "Carburetor: Klasika, horší odpařování (klepání).\nMechanical Injection: Závodní, obří spotřeba.\nSingle Point EFI: Základní stříkačka (1 tryska).\nEFI Multi: Moderní nepřímý vstřik.\nDirect Injection: Chladí válce zevnitř, brutálně brání detonacím.",
        "tt_inconf": "Single: Úsporné.\nTwin: Dvě klapky.\nITB (Nezávislé klapky): Šílená odezva a brutální výkon nahoře.",
        "tt_man": "Standard (Low/Mid): Vyvážené. Low je na spodek.\nPerformance (Mid/High): Větší průtok, High posouvá výkon nahoru.\nRace: Závodní nahoře.\nCompact: Vejdou se všude, ale dusí.\nVariable: Zvětšuje celkové spektrum otáček.",
        "tt_fuel": "Odolnost proti klepání. Low Quality 85/Regular 91: Hrozné palivo. Premium 95/Super 98: Standard. Ultimate 100/E85/Methanol: Pro velká turba. Nitromethane: Absolutní šílenost, masivní výkon. Diesel: Nikdy nezdetonuje.",
        "tt_afr": "14.7 = Dokonalé spalování.\n12.5 - 13.0 = Bohatá směs, největší výkon.\n15+ = Chudá směs. Spotřeba padá, ale drasticky ROSTE RIZIKO DETONACÍ.",
        "tt_ign": "Víc předstihu = vyšší výkon.\nAle bacha: Agresivní předstih u vysoké komprese rychle roztaví písty (Klepání).\nIgnorováno u Dieselu.",
        "tt_lim": "NIKDY nedávej výš, než co vydrží tvé ojnice, jinak motor vybuchne!\nPosuvník pokrývá běžných 3000–12000 RPM. Extrémní závodní motory lze ručně zadat až do 20000 RPM, ale pouze odpovídající krátkozdvihová high-tech architektura takové otáčky přežije.",
        "tt_carb_size": "Určuje velikost karburátoru nebo škrtící klapky. Menší (0-40) pomáhá průtoku a krouťáku v nízkých otáčkách. Větší (60-100) je nutný pro vysoké otáčky, aby se motor nezadusil.",
        "tt_man_size": "Šířka sacích kanálů. Malá přidává tah dole, velká odemyká vysoké otáčky, ale zhorší odezvu plynu v nízkých.",
        "tt_fuel_map": "Nastavení palivové mapy. 0-40 (Lean): Snižuje spotřebu, ale rapidně roste riziko klepání a klesá výkon. 60-100 (Rich): Více paliva chladí válec a mírně zvedne výkon.",

        "lbl_arch": "Architektura:", "lbl_head_exh": "Výfukové svody:", "lbl_diam": "Průměr potrubí:", "lbl_cat": "Katalyzátor:",
        "lbl_muf1": "Tlumič 1:", "lbl_muf2": "Tlumič 2:", "lbl_head_size": "Velikost svodů:", "lbl_bypass": "Výfuk. klapky:",
        "tt_arch": "Dual efektivně ohromně zvětšuje celkový průřez výfuku.",
        "tt_head_exh": "Compact Cast: Obrovská restrikce.\nCast (Low/Mid/Std): Litina, brzdí výkon.\nTubular (Std/Mid/Long/Race): Plynulý odvod plynů. Long/Race dají max výkon u omezovače, ale uberou spodek.",
        "tt_diam": "Pokud máš 1000 koní a průměr odtoku jako z umyvadla (25mm), motor se zadusí a křivka spadne.",
        "tt_cat": "None: Žádný restriktor.\n2-way/3-way/Reactor: Různé typy keramik, které dusí výkon.\nHigh Flow (s Pre-Cat): Sportovní propustnější katalyzátory, minimální ztráta výkonu.",
        "tt_muf": "None (Rovná roura): Žádná restrikce.\nStraight: Dobrý průtok.\nBaffled: Plyny kličkují = ztráta výkonu.\nReverse Flow: Nejtišší, ale největší dusítko.",
        "tt_head_size": "Průměr svodového potrubí. Velký pomáhá extrémním výkonům, malý pomáhá rychlosti výfukových plynů pro lepší krouťák dole.",
        "tt_bypass": "No Valves: Výfuk jde vždy přes tlumiče.\nBypass Valves: Klapky se v 3500 RPM otevřou a zcela obejdou tlumiče, čímž uvolní maximální výkon za cenu hluku.",

        "lbl_veh": "Předvolba vozu:", "lbl_weight": "Váha:", "lbl_cd": "Odpor vzduchu (Cd):", "lbl_grip": "Přilnavost pneumatik:",
        "lbl_area": "Čelní plocha:", "lbl_wheel": "Poloměr kola:", "lbl_speed_limit": "Omezovač rychlosti:", "lbl_downforce": "Přítlak (Cl·A):",
        "lbl_gears": "Počet převodů:", "lbl_fd": "Stálý převod:", "lbl_drive": "Pohon nápravy:",
        "lbl_custom_gears": "Jemné nastavení jednotlivých převodů", "btn_reset_gears": "Načíst automatické převody",
        "lbl_gear_1": "1. převod:", "lbl_gear_2": "2. převod:", "lbl_gear_3": "3. převod:", "lbl_gear_4": "4. převod:",
        "lbl_gear_5": "5. převod:", "lbl_gear_6": "6. převod:", "lbl_gear_7": "7. převod:", "lbl_gear_8": "8. převod:",
        "tt_veh": "Přednastaví hodnoty šasi podle typických zástupců daných kategorií.\nUšetří ti čas při testování různých motorů v různých typech aut.",
        "tt_weight": "Celková hmotnost vozu s řidičem a náplněmi.\nZásadní parametr pro zrychlení z místa podle Newtonova druhého zákona (F=m*a).",
        "tt_cd": "Koeficient aerodynamického odporu.\nKlíčový pro maximální rychlost. Běžná auta mají kolem 0.30, supersporty méně.",
        "tt_grip": "Přilnavost pneumatik (bezrozměrný koeficient).\nOmezuje maximální podélnou sílu na hnaných kolech. Sama o sobě nevytváří aerodynamický přítlak.\nSlider nabízí běžných 0,5–2,0; do pole lze ručně zadat 0,3–2,5.",
        "tt_area": "Čelní referenční plocha vozu v m². Aerodynamický odpor je úměrný součinu Cd × plocha.",
        "tt_wheel": "Dynamický poloměr hnaného kola v metrech. Ovlivňuje převod síly i rychlost při daných otáčkách.",
        "tt_speed_limit": "Elektronický omezovač maximální rychlosti. 0 znamená bez elektronického omezení.",
        "tt_downforce": "Součin součinitele přítlaku a referenční plochy (Cl·A) v m². 0 = žádný modelovaný přítlak.",
        "tt_gears": "Počet rychlostních stupňů v převodovce.\nVíc rychlostí udrží motor déle v ideálním spektru otáček.",
        "tt_fd": "Stálý převod na hnané nápravě (diferenciál).\nVětší číslo = kratší kvalty, lepší zrychlení, ale nižší maximálka a víc řazení.\nSlider nabízí běžných 2,0–6,0; do pole lze ručně zadat 1,5–10,0.",
        "tt_drive": "FWD: Náhon na přední. Ztrácí trakci při zrychlení.\nRWD: Náhon na zadní. Trakce roste při zrychlení.\nAWD: Náhon na všechna kola. Maximální využití váhy pro trakci.",
        "tt_custom_gears": "Volitelné přesné převody. Když není zaškrtnuto, simulátor používá stejné automatické sady jako doposud. Počet viditelných převodů odpovídá zvolenému počtu rychlostí.",

        "btn_dyno": "1. Spustit dyno", "btn_graph": "Zobrazit graf", "btn_rev": "2. Ruční plyn", "btn_drive": "3. Zkušební jízda", "btn_track": "4. Simulace okruhu", "btn_no_snd": "Zvuk není dostupný",
        "msg_dyno_hdr": "--- MĚŘENÍ NA DYNU:", "msg_rpm": "Otáčky", "msg_trq": "Točák", "msg_hp": "Výkon",
        "msg_done": "\nHotovo!", "msg_blown": "💥 ZNIČENO!", "msg_fix": "🔧 JAK TO OPRAVIT:", 
        "msg_max_hp": "Max Výkon:", "msg_max_trq": "Max Moment:", "msg_ready": "-> Připraveno na Zkušební jízdu!",

        "win_rev_title": "Telemetrie (Ruční plyn a Chlazení)", "lbl_coolant": "Teplota kapaliny:", "btn_pedal": "PLYNOVÝ PEDÁL (Držet stisknuté)",
        "msg_hg_blown": "💥 PRASKLÉ TĚSNĚNÍ POD HLAVOU! 💥",
        "msg_invalid": "Neplatné vstupní hodnoty",
        "msg_file_error": "Chyba souboru",
        "win_drv_title": "Zkušební jízda (0–max)", "btn_launch": "SPUSTIT JÍZDU", "btn_skip": "PŘESKOČIT NA MAX",
        "btn_retry": "NOVÝ POKUS", "btn_accel": "ZRYCHLUJEME...", "msg_not_reached": "Nedosaženo",
        "win_track_title": "Simulace okruhu – měřené kolo", "btn_track_start": "SPUSTIT MĚŘENÉ KOLO", "btn_track_retry": "NOVÉ KOLO",
        "lbl_lap_time": "Čas kola", "lbl_track_speed": "Rychlost", "lbl_track_gear": "Převod", "lbl_track_sector": "Sektor",
        "lbl_track_length": "Délka dráhy", "lbl_track_avg": "Průměrná rychlost", "lbl_track_max": "Maximální rychlost",
        "msg_track_ready": "Připraveno na start", "msg_track_running": "Měřené kolo probíhá...", "msg_track_finished": "Kolo dokončeno"
    },
    "en": {
        "app_title": "Automation DIY - Version 4.9.1 (Localization & Tooltip Stability Update)",
        "menu_file": "File",
        "menu_settings": "⚙  SETTINGS",
        "settings_title": "SIMULATOR SETTINGS",
        "settings_files": "VEHICLES & ENGINES",
        "settings_language": "LANGUAGE",
        "settings_speed_units": "SPEED UNITS",
        "settings_close": "CLOSE SETTINGS",
        "settings_quit": "QUIT SIMULATOR",
        "settings_kmh": "Kilometres per hour (km/h)",
        "settings_mph": "Miles per hour (mph)",
        "settings_audio": "AUDIO AND OPTIONAL MODULES",
        "sound_ready": "Live engine audio is ready.",
        "sound_missing": "The audio module is unavailable. Manual Throttle and Test Drive still work in silent mode.",
        "sound_help": "AUDIO INSTALLATION GUIDE",
        "sound_help_title": "LIVE ENGINE AUDIO",
        "sound_help_body": "The simulator remains fully usable without audio. For live engine sound, open a terminal in the project folder and run:\n\npip install -r requirements.txt\n\nIf sounddevice is already installed, check PortAudio and the default output device, then restart the simulator.",
        "sound_silent_sidebar": "⚠  AUDIO: SILENT MODE",
        "ui_dyno_ready": "Ready for dyno",
        "ui_live_telemetry": "LIVE TELEMETRY",
        "ui_ready": "Ready",
        "ui_dyno_running": "Dyno pull in progress…",
        "ui_dyno_cancelled": "Dyno run cancelled",
        "ui_engine_control": "ENGINE CONTROL",
        "ui_throttle_instruction": "Hold the button for full throttle. Release it to return to idle.",
        "ui_mode_exit_hint": "ESC or the left menu safely closes this mode.",
        "ui_speed": "SPEED",
        "ui_gear": "GEAR",
        "ui_tcs_ready": "TCS READY",
        "ui_tcs_ok": "TCS OK",
        "ui_slip": "SLIP",
        "ui_max": "MAX",
        "ui_track_start_finish": "START / FINISH",
        "ui_fullscreen_hint": "F11  FULLSCREEN",
        "ui_back_hint": "ESC  BACK",
        "menu_load": "Load engine / vehicle (.json)...",
        "menu_save": "Save engine / vehicle as (.json)...",
        "menu_quit": "Quit",
        "lbl_engine_name": "Car/Engine Name:",
        "tab_1": "1. Block", "tab_2": "2. Bottom End", "tab_3": "3. Top End",
        "tab_4": "4. Aspiration", "tab_5": "5. Fuel & Tune", "tab_6": "6. Exhaust", "tab_7": "7. Drivetrain",
        
        "lbl_config": "Configuration:", "lbl_vangle": "V Angle:", "lbl_cyl": "Cylinders:", "lbl_block": "Block Material:",
        "lbl_bore": "Bore:", "lbl_stroke": "Stroke:", "lbl_rad": "Radiator Efficiency:", "lbl_tech": "Technology Level:", "lbl_calc_disp": "Calculated Disp:",
        "tt_config": "Inline: Cheap, smooth running, but too long for many cylinders.\nV: Compact, short, great for 6 and 8 cylinders.\nBoxer (Flat): Opposed pistons. Perfect balance and low center of gravity.",
        "tt_vangle": "60°: Suitable for V6, engine is narrower.\n90°: Classic for V8, great balance of rotating masses.\n120°: Very flat engine, lowers CG, but extremely wide.",
        "tt_cyl": "3 to 5: Cheaper, suitable for small displacements.\n6 to 8: Powerful standard, refined running.\n10 to 16: Exotic supercars. Massive power and consumption.",
        "tt_block": "Cast Iron: Heavy, indestructible.\nAluminium (Light/Heavy/Billet): Standard. Heavy is stronger, Light is lighter. Billet is CNC machined for racing.\nAlSi (Light/Heavy): Sleeveless alloy, reduces friction.\nMagnesium: Motorsport, lightest, lowest friction.",
        "tt_bore": "Determines the piston diameter.\nLarger bore = allows installing bigger valves for better airflow at high RPM.",
        "tt_stroke": "Determines the distance the piston travels.\nLarger stroke = massive increase in low-end torque, but physically limits the engine from reaching high RPM.\nThe slider covers the usual 50–120 mm range; special engines may use 20–150 mm by typing the value manually.",
        "tt_rad": "A larger radiator (high efficiency in %) can dissipate heat from the block much more effectively.\nIt keeps the engine under load longer without boiling the coolant and destroying the head gasket.",
        "tt_tech": "Determines the technological era of the engine.\n60 = 1970s era.\n100 = modern standard (unchanged).\n115+ = cutting-edge high-tech engines.\nAffects overall efficiency, breathing, friction, and knock resistance.",

        "lbl_crank": "Crankshaft:", "lbl_conrods": "Connecting Rods:", "lbl_pistons": "Pistons:", "lbl_bal": "Balancers:", "lbl_bal_mass": "Balancer Mass:",
        "tt_crank": "Cast / Cast Iron Heavy: Stock (max 6500 RPM), Heavy is sturdier.\nForged / Forged Steel (Heavy/Light): Forged, sweet spot for turbos (8500 RPM).\nBillet / Billet Steel Heavy: CNC machined, survives 11500 RPM.\nFlat-plane: On V8s, completely changes SOUND and rev character to modern/high-revving!",
        "tt_conrods": "Cast (Light/Heavy): Stock up to 6000 RPM.\nHeavy Duty: For trucks (7000 RPM).\nForged (Light/Heavy): Sweet spot (8500 RPM).\nLW Forged: Lightweight forged (10000 RPM).\nTitanium: Lightest, most expensive (12000 RPM).",
        "tt_pistons": "Cast (Light/Heavy): Stock (6500 RPM).\nHeavy Duty: Max 7000 RPM.\nHypereutectic Cast: Stronger cast, better for emissions and light turbo.\nForged (Light/Heavy): Resists detonation (8500 RPM).\nLW Forged: Super light (12000 RPM).\nLow Friction: Lowers fuel consumption, very fragile (7500 RPM).",
        "tt_bal": "None: Engine vibrates, but is the lightest.\nHarmonic Damper: Calms vibrations (+200 RPM limit, small friction).\nFull Balancers: Add. shafts (+500 RPM limit, but eats power).",
        "tt_bal_mass": "Adding counterweights perfectly balances the engine, raising RPM limits but adding rotational mass, which increases internal friction and slows down throttle response.",

        "lbl_head_mat": "Head Material:", "lbl_springs": "Springs & Lifters:", "lbl_vvl_prof": "VVL Profile:", "lbl_vvl_rpm": "VVL RPM:",
        "tt_head_mat": "Cast Iron / Iron (Eco/Std/Perf): Retains heat, heavily INCREASING knock risk. Eco is cheap, Perf flows better.\nAluminium / Alu (Eco/Std/Perf): Dissipates heat well (lowers knock risk).\nAlu Billet Race: Racing head, best cooling and lowest friction.",

        "lbl_valve": "Valvetrain:", "lbl_valvesn": "Valves per Cyl:", "lbl_vvt": "VVT (Timing):", "lbl_vvl": "VVL (Variable Lift)",
        "lbl_cam": "Cam Profile:", "lbl_comp": "Compression Ratio:",
        "tt_valve": "Pushrod (OHV): Cam in block, heavy pushrods. Chokes past 4200 RPM.\nSOHC: 1 cam in head. Reliable.\nDOHC: 2 cams in head. Perfect for high RPM.\nDAOHC: Direct actuation, racing tier.",
        "tt_valvesn": "2: Great for low RPM, chokes at the top.\n3: A compromise.\n4: Modern standard, ideal airflow.\n5: Extreme top-end power.",
        "tt_vvt": "None: Fixed timing.\nIntake: Varies intake cam timing. Improves smoothness.\nAll: Variable intake and exhaust. Flattens the curve across the whole spectrum.",
        "tt_vvl": "None: Fixed lift.\nVVL: Variable Valve Lift - switches to aggressive cam profile at set RPM.\nCVVL: Continuous - flattens the torque curve and maximizes efficiency.",
        "tt_vvl_prof": "Determines the aggressiveness of the second (VVL) cam profile. \n0-30: Mild profile for low-end torque.\n40-60: Sporty.\n70-100: Aggressive racing cam for top-end power.",
        "tt_vvl_rpm": "Sets the exact RPM where the VVL system switches from the normal cam profile (Tab 3: Cam Profile) to the aggressive VVL Profile.",
        "tt_springs": "Stiffer springs and lifters (50-100) allow the engine to rev much higher without valve float, but add friction and slightly reduce power.",
        "tt_cam": "Determines engine breathing. Higher profile shifts power to the redline with a rough idle.",
        "tt_comp": "Higher compression (10+): Engine is stronger, but DETONATION RISK INCREASES!\nLow compression (7-9): Necessary for forced induction with a giant turbo.\nDiesel ignores these limits.",

        "lbl_asp": "Aspiration:", "lbl_tb": "Turbo Bearings:", "lbl_tc": "Configuration:", "lbl_ic": "Intercooler Size:",
        "lbl_tsize": "Turbo Size:", "lbl_tboost": "Max Boost:", "lbl_sct": "Supercharger Type:", "lbl_scp": "Pulley (Max Boost):",
        "lbl_csize": "Compressor Size:",
        "tt_asp": "NA (Naturally Aspirated): Smooth response.\nTurbo: Exhaust-driven (has Lag).\nSupercharger: Belt-driven compressor. Instant response.",
        "tt_tb": "Journal: Cheap, slower spool.\nBall Bearings: Drastically shortens Turbo Lag.",
        "tt_tc": "Single: Big Lag.\nTwin: Faster spool (less lag).\nQuad: Four small turbos, super fast spool for huge engines.",
        "tt_ic": "A larger intercooler saves the engine from knocking, but slightly increases Turbo Lag.",
        "tt_tsize": "A big turbo can blow immense boost pressure, but takes forever to spool up.",
        "tt_tboost": "How many bars of pressure you push into the intake. Over 1.5 bar requires high-quality fuel and forged parts!",
        "tt_sct": "Roots: Kicks instantly from zero.\nTwin-screw: Much more efficient and smoother.\nCentrifugal: Blows more the faster you rev the engine.",
        "tt_scp": "Smaller pulley = compressor spins faster = more pressure.",
        "tt_csize": "A larger unit pushes much more air at high RPM, but takes a massive amount of engine power (parasitic loss) just to spin it.",

        "lbl_fdeliv": "Fuel Delivery:", "lbl_inconf": "Intake Config:", "lbl_man": "Intake Manifold:", "lbl_fuel": "Fuel Type:", "lbl_afr": "AFR (Mixture):",
        "lbl_ign": "Ignition Timing:", "lbl_lim": "RPM Limit:",
        "lbl_carb_size": "Carb/Throttle Size:", "lbl_fuel_map": "Fuel Map:", "lbl_man_size": "Manifold Size:",
        "tt_fdeliv": "Carburetor: Classic, worse vaporization (knocking).\nMechanical Injection: Racing, poor economy.\nSingle Point EFI: Basic 1-injector system.\nEFI Multi: Modern port injection.\nDirect Injection: Cools cylinders internally, massively reducing knock risk.",
        "tt_inconf": "Single: Economical.\nTwin: Two throttle bodies.\nITB (Independent Throttle Bodies): Insane response and brutal top-end power.",
        "tt_man": "Standard (Low/Mid): Balanced. Low biases bottom end.\nPerformance (Mid/High): Better flow, High shifts power up.\nRace: Top-end racing.\nCompact: Fits anywhere but chokes.\nVariable: Broadens the powerband.",
        "tt_fuel": "Knock resistance. Low Quality 85/Regular 91: Terrible fuel. Premium 95/Super 98: Standard. Ultimate 100/E85/Methanol: For big turbos. Nitromethane: Absolute insanity, massive power boost. Diesel: Never knocks.",
        "tt_afr": "14.7 = Perfect combustion.\n12.5 - 13.0 = Rich mixture, highest power.\n15+ = Lean mixture. MPG goes up, but DETONATION RISK skyrockets.",
        "tt_ign": "More advance = higher power.\nBut beware: Aggressive timing with high compression quickly melts pistons (Knock).\nIgnored for Diesel.",
        "tt_lim": "NEVER set higher than what your conrods can handle, otherwise the engine will explode!\nThe slider covers the usual 3000–12000 RPM range. Extreme race engines may be entered manually up to 20000 RPM, but only a suitable short-stroke high-tech architecture can survive it.",
        "tt_carb_size": "Sets the carburetor or throttle body size. Smaller (0-40) helps low-end torque. Larger (60-100) is necessary for high RPMs to prevent choking.",
        "tt_man_size": "Width of the intake runners. Small adds low-end grunt, large unlocks high RPMs but hurts throttle response down low.",
        "tt_fuel_map": "Fuel map tuning. 0-40 (Lean): Lowers consumption but massively increases knock risk and drops power. 60-100 (Rich): More fuel cools the cylinder and slightly boosts power.",

        "lbl_arch": "Architecture:", "lbl_head_exh": "Headers:", "lbl_diam": "Pipe Diameter:", "lbl_cat": "Catalytic Converter:",
        "lbl_muf1": "Muffler 1:", "lbl_muf2": "Muffler 2:", "lbl_head_size": "Header Size:", "lbl_bypass": "Bypass Valves:",
        "tt_arch": "Dual effectively massively increases the overall exhaust cross-section.",
        "tt_head_exh": "Compact Cast: Massive restriction.\nCast (Low/Mid/Std): Restricts power.\nTubular (Std/Mid/Long/Race): Smooth extraction. Long/Race give max top-end power but hurt the low-end.",
        "tt_diam": "If you have 1000 HP and a drain diameter like a sink (25mm), the engine will choke and the curve will drop.",
        "tt_cat": "None: No restriction.\n2-way/3-way/Reactor: Various ceramics that choke power.\nHigh Flow (w/ Pre-Cat): Sporty, less restrictive meshes, minimal power loss.",
        "tt_muf": "None (Straight pipe): No restriction.\nStraight: Good flow.\nBaffled: Gases zigzag = power loss.\nReverse Flow: Quietest, massive restriction.",
        "tt_head_size": "Header pipe diameter. Large helps extreme power output, small helps exhaust gas velocity for better low-end torque.",
        "tt_bypass": "No Valves: Exhaust always passes through mufflers.\nBypass Valves: Opens above 3500 RPM, completely bypassing mufflers for maximum flow at the cost of noise.",

        "lbl_veh": "Vehicle Preset:", "lbl_weight": "Weight:", "lbl_cd": "Air Drag (Cd):", "lbl_grip": "Tire Grip:",
        "lbl_area": "Frontal Area:", "lbl_wheel": "Wheel Radius:", "lbl_speed_limit": "Speed Limiter:", "lbl_downforce": "Downforce (Cl·A):",
        "lbl_gears": "Gears:", "lbl_fd": "Final Drive:", "lbl_drive": "Drivetrain:",
        "lbl_custom_gears": "Fine-tune individual gear ratios", "btn_reset_gears": "Load automatic ratios",
        "lbl_gear_1": "1st gear:", "lbl_gear_2": "2nd gear:", "lbl_gear_3": "3rd gear:", "lbl_gear_4": "4th gear:",
        "lbl_gear_5": "5th gear:", "lbl_gear_6": "6th gear:", "lbl_gear_7": "7th gear:", "lbl_gear_8": "8th gear:",
        "tt_veh": "Pre-sets chassis values according to typical representatives of the given categories.\nSaves you time when testing different engines in different types of cars.",
        "tt_weight": "Total weight of the vehicle with driver and fluids.\nCrucial parameter for acceleration from a standstill according to Newton's second law (F=m*a).",
        "tt_cd": "Aerodynamic drag coefficient.\nKey for top speed. Normal cars have around 0.30, supercars less.",
        "tt_grip": "Tire grip (dimensionless coefficient).\nLimits longitudinal force at the driven wheels. It does not create aerodynamic downforce by itself.\nThe slider covers the usual 0.5–2.0 range; 0.3–2.5 can be entered manually.",
        "tt_area": "Vehicle frontal reference area in m². Aerodynamic drag is proportional to Cd × area.",
        "tt_wheel": "Dynamic driven-wheel radius in metres. It affects both wheel force and road speed at a given RPM.",
        "tt_speed_limit": "Electronic maximum-speed limiter. 0 disables electronic limiting.",
        "tt_downforce": "Lift-coefficient-area product (Cl·A) in m². 0 means no modelled downforce.",
        "tt_gears": "Number of gears in the transmission.\nMore gears keep the engine longer in the ideal RPM spectrum.",
        "tt_fd": "Final drive ratio on the driven axle (differential).\nHigher number = shorter gears, better acceleration, but lower top speed and more shifting.\nThe slider covers the usual 2.0–6.0 range; 1.5–10.0 can be entered manually.",
        "tt_drive": "FWD: Front-Wheel Drive. Loses traction under acceleration.\nRWD: Rear-Wheel Drive. Traction increases under acceleration.\nAWD: All-Wheel Drive. Maximum use of weight for traction.",
        "tt_custom_gears": "Optional exact ratios. When unchecked, the simulator uses the same automatic ratio sets as before. The number of visible ratios follows the selected gear count.",

        "btn_dyno": "1. Dyno Pull", "btn_graph": "Show Graph", "btn_rev": "2. Manual Throttle", "btn_drive": "3. Test Drive", "btn_track": "4. Track Simulation", "btn_no_snd": "Sound N/A",
        "msg_dyno_hdr": "--- DYNO PULL:", "msg_rpm": "RPM", "msg_trq": "Torque", "msg_hp": "Power",
        "msg_done": "\nDone!", "msg_blown": "💥 DESTROYED!", "msg_fix": "🔧 HOW TO FIX:", 
        "msg_max_hp": "Max Power:", "msg_max_trq": "Max Torque:", "msg_ready": "-> Ready for Test Drive!",

        "win_rev_title": "Telemetry (Throttle & Cooling)", "lbl_coolant": "Coolant Temp:", "btn_pedal": "THROTTLE PEDAL (Hold)",
        "msg_hg_blown": "💥 BLOWN HEAD GASKET! 💥",
        "msg_invalid": "Invalid input values",
        "msg_file_error": "File error",
        "win_drv_title": "Test Drive (0 - Max)", "btn_launch": "START LAUNCH", "btn_skip": "SKIP TO TOP SPEED",
        "btn_retry": "RETRY LAUNCH", "btn_accel": "ACCELERATING...", "msg_not_reached": "Not Reached",
        "win_track_title": "Track Simulation - Timed Lap", "btn_track_start": "START TIMED LAP", "btn_track_retry": "NEW LAP",
        "lbl_lap_time": "Lap time", "lbl_track_speed": "Speed", "lbl_track_gear": "Gear", "lbl_track_sector": "Sector",
        "lbl_track_length": "Track length", "lbl_track_avg": "Average speed", "lbl_track_max": "Maximum speed",
        "msg_track_ready": "Ready to start", "msg_track_running": "Timed lap in progress...", "msg_track_finished": "Lap complete"
    }
}

# --- VIZUÁLNÍ KOMPONENTY (Analogový otáčkoměr) ---
class AnalogTachometer(tk.Canvas):
    def __init__(self, parent, max_rpm, redline_rpm, size=280, **kwargs):
        super().__init__(parent, width=size, height=size, bg='#111111', highlightthickness=0, **kwargs)
        self.size = size
        self.cx = size / 2
        self.cy = size / 2
        self.r = size * 0.42
        self.max_rpm = max_rpm
        self.redline = redline_rpm
        self.draw_dial()
        self.needle = self.create_line(self.cx, self.cy, self.cx, self.cy, fill='#ff3333', width=4, capstyle=tk.ROUND)
        self.set_rpm(0)

    def draw_dial(self):
        self.create_oval(self.cx-self.r*1.05, self.cy-self.r*1.05, self.cx+self.r*1.05, self.cy+self.r*1.05, outline='#333333', width=3)
        for r in range(0, int(self.max_rpm) + 1000, 1000):
            angle_rad = math.radians(135 + (r / self.max_rpm) * 270)
            is_red = r >= self.redline
            color = '#ff3333' if is_red else '#ffffff'
            
            x1 = self.cx + self.r * 0.85 * math.cos(angle_rad)
            y1 = self.cy + self.r * 0.85 * math.sin(angle_rad)
            x2 = self.cx + self.r * math.cos(angle_rad)
            y2 = self.cy + self.r * math.sin(angle_rad)
            self.create_line(x1, y1, x2, y2, fill=color, width=3 if r % 2000 == 0 else 1)
            
            if r % 1000 == 0:
                tx = self.cx + self.r * 0.65 * math.cos(angle_rad)
                ty = self.cy + self.r * 0.65 * math.sin(angle_rad)
                self.create_text(tx, ty, text=str(r//1000), fill=color, font=("Arial", 14, "bold"))
        self.create_oval(self.cx-12, self.cy-12, self.cx+12, self.cy+12, fill='#222222', outline='#555555', width=2)
        self.create_text(self.cx, self.cy + self.r * 0.4, text="RPM x1000", fill="gray", font=("Arial", 10))

    def set_rpm(self, rpm):
        fraction = min(rpm / self.max_rpm, 1.05)
        angle_rad = math.radians(135 + fraction * 270)
        nx = self.cx + self.r * 0.95 * math.cos(angle_rad)
        ny = self.cy + self.r * 0.95 * math.sin(angle_rad)
        self.coords(self.needle, self.cx, self.cy, nx, ny)

# --- AKUSTICKÝ ENGINE ---
def generate_audio_frame(phases, rev_phases, cylinders, aspiration, rpm, throttle_load=1.0, flutter_intensity=0.0, flutter_phases=None, crank_type="Cast"):
    if cylinders == 3:
        w = 0.8 * np.sin(rev_phases) + np.sin(phases) + 0.5 * np.sin(phases * 2.0)
        w = np.tanh(w * 2.5)
        lope = 1.0 - (0.25 * np.sin(rev_phases * 0.5))
    elif cylinders <= 6:
        w = 0.7 * np.sin(rev_phases) + np.sin(phases) + 0.3 * np.sin(phases * 2.0)
        w = np.tanh(w * 2.0)
        lope = 1.0 - (0.1 * np.sin(rev_phases * 0.5))
    elif cylinders == 8:
        if crank_type == "Flat-plane":
            w = 1.2 * np.sin(phases) + 0.8 * np.sin(rev_phases * 2.0) + 0.6 * np.sin(rev_phases) + 0.2 * np.sin(phases * 2.0)
            w = np.tanh(w * 1.8) 
            lope = 1.0 - (0.05 * np.sin(rev_phases))
        else:
            w = 1.2 * np.sin(rev_phases * 0.5) + 1.0 * np.sin(rev_phases) + 0.8 * np.sin(phases)
            w = np.tanh(w * 3.5)
            lope = 1.0 - (0.3 * np.sin(rev_phases * 0.5))
    elif cylinders <= 12:
        bank_phase = rev_phases * (cylinders / 4.0)
        w = 1.0 * np.sin(rev_phases) + 0.8 * np.sin(bank_phase) + 0.6 * np.sin(phases) 
        w = np.tanh(w * 1.5)
        lope = 1.0 - (0.05 * np.sin(rev_phases))
    else:
        w = 1.5 * np.sin(rev_phases) + 1.2 * np.sin(rev_phases * 2.0) + 0.8 * np.sin(rev_phases * 4.0) + 0.3 * np.sin(phases)
        w = np.tanh(w * 1.5) 
        lope = 1.0 - (0.02 * np.sin(rev_phases))
        
    noise = np.random.normal(0, 0.005, len(phases))
    base_audio = (w * lope + noise) * 0.25
    
    if aspiration == "Turbo":
        turbo_vol = np.clip((rpm - 2500) / 4000.0, 0.0, 1.0)
        if throttle_load > 0:
            turbo_wind = np.random.normal(0, 0.025, len(phases)) * turbo_vol * throttle_load
            turbo_spool = np.sin(rev_phases * 15.0) * 0.015 * turbo_vol * throttle_load
            base_audio += turbo_wind + turbo_spool
        if flutter_intensity > 0 and flutter_phases is not None:
            surge_noise = np.random.normal(0, 0.08, len(phases))
            flutter_chop = np.maximum(0, np.sin(flutter_phases))**2 
            base_audio += surge_noise * flutter_chop * flutter_intensity * turbo_vol
            
    elif aspiration == "Supercharger":
        sc_vol = np.clip(rpm / 7000.0, 0.1, 1.0) * (0.5 + 0.5 * throttle_load)
        sc_whine = 0.15 * np.sin(rev_phases * 8.0) + 0.08 * np.sin(rev_phases * 16.0)
        base_audio += sc_whine * sc_vol
        
    return base_audio

def generate_engine_wav(rpm_list, cylinders, aspiration, crank_type="Cast", filename="dyno_temp.wav", step_duration=0.08):
    fs = 22050 
    num_steps = len(rpm_list)
    total_time = num_steps * step_duration
    num_samples = int(total_time * fs)
    t_samples = np.linspace(0, total_time, num_samples, endpoint=False)
    t_rpms = np.linspace(0, total_time, num_steps, endpoint=False)
    rpm_samples = np.interp(t_samples, t_rpms, rpm_list)
    freqs = (rpm_samples / 60.0) * (cylinders / 2.0)
    rev_freqs = (rpm_samples / 60.0)
    d_phase = 2.0 * np.pi * freqs / fs
    phases = np.cumsum(d_phase)
    d_rev_phase = 2.0 * np.pi * rev_freqs / fs
    rev_phases = np.cumsum(d_rev_phase)
    wave_data = generate_audio_frame(phases, rev_phases, cylinders, aspiration, rpm_samples, throttle_load=1.0, crank_type=crank_type)
    wave_data = np.clip(wave_data * 1.5, -1.0, 1.0)
    wave_int = np.int16(wave_data * 32767) 
    with wave.open(filename, "w") as f:
        f.setnchannels(1)
        f.setsampwidth(2)
        f.setframerate(fs)
        f.writeframes(wave_int.tobytes())

# --- NEZÁVISLÉ FYZIKÁLNÍ JÁDRO ---
def clamp(value, low, high):
    return max(low, min(high, value))


def get_gear_ratios(gear_count, custom_ratios=None):
    """Vrátí původní automatickou sadu, nebo přesně zadané volitelné převody."""
    gear_count = int(clamp(int(gear_count), 4, 8))
    if custom_ratios is not None:
        ratios = [float(value) for value in list(custom_ratios)[:gear_count]]
        if len(ratios) != gear_count:
            raise ValueError("Custom gear-ratio count does not match the gearbox")
        if any(not math.isfinite(value) or value < 0.30 or value > 5.50 for value in ratios):
            raise ValueError("Custom gear ratios must be between 0.30 and 5.50")
        if any(ratios[i] <= ratios[i + 1] for i in range(len(ratios) - 1)):
            raise ValueError("Custom gear ratios must decrease with every higher gear")
        return ratios
    if gear_count == 4:
        return [2.8, 1.5, 1.0, 0.8]
    if gear_count == 5:
        return [3.3, 1.9, 1.3, 1.0, 0.8]
    if gear_count == 6:
        return [3.5, 2.0, 1.4, 1.0, 0.8, 0.6]
    return [4.0, 2.5, 1.7, 1.2, 0.9, 0.7, 0.55, 0.45][:gear_count]


# Jediná geometrie testovací dráhy. Stejné body se používají pro kresbu, délku,
# sektory, poloměry zatáček i fyzikální výpočet rychlostního profilu.
TEST_TRACK_TARGET_LENGTH = 3605.0
TEST_TRACK_SAMPLE_STEP = 5.0

# Řídicí body technického okruhu v lokálních souřadnicích. Catmull-Romova křivka
# z nich vytvoří spojitou uzavřenou stopu s rovinkami, vracáky, esíčky i rychlými oblouky.
TEST_TRACK_CONTROL_POINTS = np.asarray([
    (0.0, 0.0),
    (260.0, -8.0),
    (560.0, 0.0),
    (760.0, 60.0),
    (820.0, 190.0),
    (790.0, 320.0),
    (700.0, 390.0),
    (850.0, 460.0),
    (920.0, 590.0),
    (850.0, 700.0),
    (680.0, 730.0),
    (540.0, 670.0),
    (420.0, 730.0),
    (280.0, 680.0),
    (150.0, 600.0),
    (70.0, 480.0),
    (110.0, 360.0),
    (250.0, 330.0),
    (370.0, 390.0),
    (500.0, 350.0),
    (585.0, 250.0),
    (520.0, 170.0),
    (390.0, 150.0),
    (290.0, 210.0),
    (180.0, 170.0),
    (70.0, 190.0),
    (10.0, 100.0),
], dtype=float)


def _catmull_rom_closed(points, samples_per_segment=35):
    """Vzorkuje uzavřenou Catmull-Romovu křivku bez duplicitního koncového bodu."""
    points = np.asarray(points, dtype=float)
    result = []
    count = len(points)
    for i in range(count):
        p0 = points[(i - 1) % count]
        p1 = points[i]
        p2 = points[(i + 1) % count]
        p3 = points[(i + 2) % count]
        for j in range(samples_per_segment):
            t = j / samples_per_segment
            t2 = t * t
            t3 = t2 * t
            point = 0.5 * (
                (2.0 * p1)
                + (-p0 + p2) * t
                + (2.0 * p0 - 5.0 * p1 + 4.0 * p2 - p3) * t2
                + (-p0 + 3.0 * p1 - 3.0 * p2 + p3) * t3
            )
            result.append(point)
    return np.asarray(result, dtype=float)


def _resample_closed_polyline(points, target_length, step):
    """Přeškáluje a převzorkuje uzavřenou stopu na téměř konstantní délku kroku."""
    points = np.asarray(points, dtype=float)
    closed = np.vstack((points, points[0]))
    seg = np.linalg.norm(np.diff(closed, axis=0), axis=1)
    raw_length = float(np.sum(seg))
    if raw_length <= 1e-9:
        raise ValueError('Track geometry has zero length')

    scaled = points * (target_length / raw_length)
    closed = np.vstack((scaled, scaled[0]))
    seg = np.linalg.norm(np.diff(closed, axis=0), axis=1)
    cumulative = np.concatenate(([0.0], np.cumsum(seg)))
    total = float(cumulative[-1])
    point_count = max(120, int(round(total / step)))
    sample_s = np.linspace(0.0, total, point_count, endpoint=False)
    x = np.interp(sample_s, cumulative, closed[:, 0])
    y = np.interp(sample_s, cumulative, closed[:, 1])
    sampled = np.column_stack((x, y))

    next_points = np.roll(sampled, -1, axis=0)
    ds = np.linalg.norm(next_points - sampled, axis=1)
    # Druhé drobné škálování odstraní chybu vzniklou převzorkováním.
    sampled *= target_length / float(np.sum(ds))
    next_points = np.roll(sampled, -1, axis=0)
    ds = np.linalg.norm(next_points - sampled, axis=1)
    return sampled, ds


def _cyclic_smooth(values, passes=5):
    values = np.asarray(values, dtype=float)
    for _ in range(passes):
        values = (
            np.roll(values, 2) + 4.0 * np.roll(values, 1) + 6.0 * values
            + 4.0 * np.roll(values, -1) + np.roll(values, -2)
        ) / 16.0
    return values


def build_test_track_geometry():
    """Vytvoří jediný zdroj pravdy pro vykreslení i fyzikální model okruhu."""
    dense = _catmull_rom_closed(TEST_TRACK_CONTROL_POINTS)
    points, ds = _resample_closed_polyline(dense, TEST_TRACK_TARGET_LENGTH, TEST_TRACK_SAMPLE_STEP)

    # Diskrétní křivost ze změny tečného směru. Poloměr = 1 / křivost.
    prev_points = np.roll(points, 1, axis=0)
    next_points = np.roll(points, -1, axis=0)
    tangent_a = points - prev_points
    tangent_b = next_points - points
    angle_a = np.arctan2(tangent_a[:, 1], tangent_a[:, 0])
    angle_b = np.arctan2(tangent_b[:, 1], tangent_b[:, 0])
    delta = (angle_b - angle_a + np.pi) % (2.0 * np.pi) - np.pi
    local_ds = 0.5 * (np.linalg.norm(tangent_a, axis=1) + np.linalg.norm(tangent_b, axis=1))
    curvature = np.abs(delta) / np.maximum(local_ds, 1e-6)
    curvature = _cyclic_smooth(curvature, passes=6)
    radii = np.where(curvature > 1.0 / 5000.0, 1.0 / curvature, np.inf)

    distances = np.concatenate(([0.0], np.cumsum(ds)))
    mid_distances = distances[:-1] + ds * 0.5
    sector_boundaries = (TEST_TRACK_TARGET_LENGTH * 0.31, TEST_TRACK_TARGET_LENGTH * 0.63)
    sectors = np.where(mid_distances < sector_boundaries[0], 1,
                       np.where(mid_distances < sector_boundaries[1], 2, 3)).astype(int)

    return {
        'points': points,
        'step_lengths': ds,
        'radii': radii,
        'sectors': sectors,
        'distances': distances,
        'track_length': float(np.sum(ds)),
    }


TEST_TRACK_GEOMETRY = build_test_track_geometry()


def run_track_simulation(veh_params, engine_data, geometry=None):
    """Vypočítá deterministické letmé kolo přímo po vykreslené geometrii okruhu."""
    geometry = geometry or TEST_TRACK_GEOMETRY
    rpm_arr = np.asarray(engine_data['rpm'], dtype=float)
    trq_arr = np.asarray(engine_data['torque'], dtype=float)
    if rpm_arr.size == 0 or trq_arr.size != rpm_arr.size:
        raise ValueError("Engine curve is empty or inconsistent")
    if not np.all(np.isfinite(rpm_arr)) or not np.all(np.isfinite(trq_arr)) or np.max(trq_arr) <= 0.0:
        raise ValueError("Engine curve has no usable torque")

    mass = clamp(float(veh_params.get('weight', 1350.0)), 500.0, 3000.0)
    cd = clamp(float(veh_params.get('cd', 0.30)), 0.15, 0.80)
    area = clamp(float(veh_params.get('area', 2.2)), 1.2, 4.0)
    grip = clamp(float(veh_params.get('grip', 0.9)), 0.3, 2.5)
    wheel_radius = clamp(float(veh_params.get('wheel_radius', 0.33)), 0.20, 0.55)
    speed_limiter_kmh = max(0.0, float(veh_params.get('speed_limiter', 0.0)))
    downforce_cla = clamp(float(veh_params.get('downforce_cla', 0.0)), 0.0, 4.0)
    gear_count = int(clamp(int(veh_params.get('gears', 5)), 4, 8))
    final_drive = clamp(float(veh_params.get('final_drive', 4.1)), 1.5, 10.0)
    drivetrain = veh_params.get('drivetrain', 'FWD')
    ratios = get_gear_ratios(gear_count, veh_params.get('gear_ratios'))

    points = np.asarray(geometry['points'], dtype=float)
    step_lengths = np.asarray(geometry['step_lengths'], dtype=float)
    radii = np.asarray(geometry['radii'], dtype=float)
    sectors = np.asarray(geometry['sectors'], dtype=int)
    point_count = len(step_lengths)
    track_length = float(np.sum(step_lengths))
    if not (len(points) == len(radii) == len(sectors) == point_count):
        raise ValueError('Track geometry arrays are inconsistent')

    max_rpm = float(rpm_arr[-1])
    drivetrain_eff = {"FWD": 0.90, "RWD": 0.88, "AWD": 0.82}.get(drivetrain, 0.88)
    driven_fraction = {"FWD": 0.60, "RWD": 0.55, "AWD": 1.00}.get(drivetrain, 0.55)
    rho = 1.2
    g = 9.81
    rolling_coeff = 0.015

    top_gear_speed = (max_rpm / (ratios[-1] * final_drive)) * (2.0 * math.pi * wheel_radius) / 60.0
    electronic_limit = speed_limiter_kmh / 3.6 if speed_limiter_kmh > 0.0 else float('inf')
    absolute_speed_limit = min(top_gear_speed, electronic_limit, 125.0)

    speed_limits = np.full(point_count, absolute_speed_limit, dtype=float)
    lateral_grip = grip * 0.96
    for i, radius in enumerate(radii):
        if math.isfinite(radius):
            denominator = mass / radius - lateral_grip * 0.5 * rho * downforce_cla
            if denominator > 1e-9:
                speed_limits[i] = min(absolute_speed_limit, math.sqrt(lateral_grip * mass * g / denominator))

    def total_tire_accel(speed):
        normal_accel = g + (0.5 * rho * downforce_cla * speed * speed) / mass
        return grip * normal_accel

    def lateral_accel(speed, radius):
        return 0.0 if not math.isfinite(radius) else speed * speed / radius

    def best_drive_accel(speed, radius):
        wheel_rpm = (speed / (2.0 * math.pi * wheel_radius)) * 60.0
        total_capacity = total_tire_accel(speed)
        lat = lateral_accel(speed, radius)
        longitudinal_capacity = math.sqrt(max(0.0, total_capacity * total_capacity - lat * lat))
        traction_force = mass * longitudinal_capacity * driven_fraction
        drag = 0.5 * rho * cd * area * speed * speed
        rolling = mass * g * rolling_coeff
        best_accel = -(drag + rolling) / (mass * 1.05)
        best_gear = gear_count - 1

        if speed_limiter_kmh > 0.0 and speed >= electronic_limit:
            return min(0.0, best_accel), best_gear

        for gear_index, ratio in enumerate(ratios):
            engine_rpm = wheel_rpm * ratio * final_drive
            if engine_rpm > max_rpm * 1.001:
                continue
            calc_rpm = clamp(engine_rpm, 1000.0, max_rpm)
            torque = float(np.interp(calc_rpm, rpm_arr, trq_arr))
            wheel_force = torque * ratio * final_drive * drivetrain_eff / wheel_radius
            wheel_force = min(wheel_force, traction_force)
            accel = (wheel_force - drag - rolling) / (mass * 1.05)
            if accel > best_accel:
                best_accel = accel
                best_gear = gear_index
        return best_accel, best_gear

    def braking_accel(speed, radius):
        total_capacity = total_tire_accel(speed)
        lat = lateral_accel(speed, radius)
        tire_braking = math.sqrt(max(0.0, total_capacity * total_capacity - lat * lat))
        tire_braking = min(tire_braking, 1.25 * g)
        aero_braking = (0.5 * rho * cd * area * speed * speed) / mass
        return max(0.5, tire_braking + aero_braking)

    profile = speed_limits.copy()

    # Cyklický zpětný průchod vytvoří brzdné zóny před zatáčkami skutečné geometrie.
    for _ in range(9):
        for i in range(point_count - 1, -1, -1):
            next_i = (i + 1) % point_count
            allowed = math.sqrt(max(0.0, profile[next_i] ** 2 + 2.0 * braking_accel(profile[next_i], radii[next_i]) * step_lengths[i]))
            profile[i] = min(profile[i], allowed)

    # Dopředný průchod omezí profil tím, co auto mezi body skutečně stihne zrychlit.
    for _ in range(14):
        for i in range(point_count):
            next_i = (i + 1) % point_count
            accel, _ = best_drive_accel(profile[i], radii[i])
            allowed = math.sqrt(max(0.0, profile[i] ** 2 + 2.0 * max(accel, -2.0) * step_lengths[i]))
            profile[next_i] = min(profile[next_i], allowed)

    for _ in range(5):
        for i in range(point_count - 1, -1, -1):
            next_i = (i + 1) % point_count
            allowed = math.sqrt(max(0.0, profile[next_i] ** 2 + 2.0 * braking_accel(profile[next_i], radii[next_i]) * step_lengths[i]))
            profile[i] = min(profile[i], allowed)
        for i in range(point_count):
            next_i = (i + 1) % point_count
            accel, _ = best_drive_accel(profile[i], radii[i])
            allowed = math.sqrt(max(0.0, profile[i] ** 2 + 2.0 * max(accel, -2.0) * step_lengths[i]))
            profile[next_i] = min(profile[next_i], allowed)

    profile = np.maximum(profile, 1.0)
    gears = np.asarray([best_drive_accel(profile[i], radii[i])[1] for i in range(point_count)], dtype=int)
    next_profile = np.roll(profile, -1)
    interval_times = 2.0 * step_lengths / np.maximum(profile + next_profile, 1e-6)

    shift_penalties = np.zeros(point_count, dtype=float)
    upshifts = 0
    downshifts = 0
    for i in range(point_count):
        next_i = (i + 1) % point_count
        if gears[next_i] > gears[i]:
            shift_penalties[i] = 0.16
            upshifts += 1
        elif gears[next_i] < gears[i]:
            shift_penalties[i] = 0.03
            downshifts += 1

    interval_times = interval_times + shift_penalties
    cumulative_time = np.concatenate(([0.0], np.cumsum(interval_times)))
    distances = np.concatenate(([0.0], np.cumsum(step_lengths)))
    lap_time = float(cumulative_time[-1])

    sector_times = [float(np.sum(interval_times[sectors == sector])) for sector in (1, 2, 3)]
    closed_points = np.vstack((points, points[0]))

    return {
        'lap_time': lap_time,
        'track_length': track_length,
        'average_speed': track_length / lap_time,
        'max_speed': float(np.max(profile)),
        'sector_times': sector_times,
        'upshifts': upshifts,
        'downshifts': downshifts,
        'distances': distances,
        'cumulative_time': cumulative_time,
        'speed_profile': np.concatenate((profile, [profile[0]])),
        'gear_profile': np.concatenate((gears, [gears[0]])),
        'sector_profile': np.concatenate((sectors, [sectors[0]])),
        'track_points': closed_points,
        'corner_radii': np.concatenate((radii, [radii[0]])),
    }

def run_engine_simulation(params):
    lang = params.get('lang', 'cz')
    tech_level = clamp(float(params.get('tech_level', 100)), 50.0, 150.0)
    tech_factor = tech_level / 100.0
    b = clamp(float(params.get('bore', 87.5)), 50.0, 120.0)
    s = clamp(float(params.get('stroke', 83.1)), 20.0, 150.0)
    c = int(clamp(int(params.get('cylinders', 4)), 3, 16))
    disp_cc = math.pi * ((b/20)**2) * (s/10) * c
    
    rpm_limit = int(clamp(int(params.get('rpm_limit', 6500)), 3000, 20000))

    oversquare_ratio = b / max(s, 1e-6)
    race_architecture = (
        clamp((tech_level - 120.0) / 30.0, 0.0, 1.0)
        * clamp((float(params.get('cam_profile', 30)) - 80.0) / 20.0, 0.0, 1.0)
        * clamp((rpm_limit - 12000.0) / 7000.0, 0.0, 1.0)
        * clamp((oversquare_ratio - 1.60) / 0.70, 0.0, 1.0)
        * (1.0 if params.get('valvetrain', 'DOHC') == 'DAOHC' else 0.0)
        * (1.0 if params.get('intake_conf', 'Single') == 'ITB' else 0.0)
        * (1.0 if 'Race' in params.get('manifold', 'Standard') else 0.0)
        * (1.0 if params.get('aspiration', 'NA') == 'NA' else 0.0)
        * (1.0 if params.get('crank', 'Cast') in ('Billet', 'Billet Steel Heavy') else 0.0)
        * (1.0 if params.get('conrods', 'Heavy Duty') == 'Titanium' else 0.0)
        * (1.0 if params.get('pistons', 'Cast') == 'LW Forged' else 0.0)
    )
    blow_up = False
    blow_up_reason = ""
    blow_up_fix = ""
    
    # 1. Integrace Balanceru (Zvyšuje mechanický limit, ale ovlivní tření)
    bal = params.get('balancer', 'None')
    bal_mass = 0.0 if bal == "None" else float(params.get('balancer_mass', 0.0))
    bal_rpm_bonus = 0
    friction_mult = 1.0
    if bal == "Harmonic Damper":
        bal_rpm_bonus = 200
        friction_mult *= 1.02
    elif bal == "Full Balancers":
        bal_rpm_bonus = 500
        friction_mult *= 1.05
    bal_rpm_bonus += (bal_mass * 10)
    friction_mult *= (1.0 + (bal_mass * 0.002))

    # 2. Integrace Block Material (Hořčík a AlSi snižují vnitřní tření motoru díky absenci těžkých vložek)
    b_mat = params.get('block_mat', 'Aluminium')
    if "AlSi" in b_mat: friction_mult *= 0.95
    elif "Magnesium" in b_mat: friction_mult *= 0.90
    elif "Billet" in b_mat: friction_mult *= 0.93

    cl_map = {"Cast": 6500, "Cast Iron Heavy": 6200, "Forged": 8500, "Forged Steel Heavy": 8000,
              "Forged Steel Light": 8800, "Billet": 11500, "Billet Steel Heavy": 10500, "Flat-plane": 9500}
    crank_lim = cl_map.get(params.get('crank', 'Cast'), 6500) + bal_rpm_bonus

    cn_map = {"Cast": 6000, "Cast Heavy": 5500, "Cast Light": 6500, "Heavy Duty": 7000,
              "Forged": 8500, "Forged Heavy": 8000, "Forged Light": 9000,
              "LW Forged": 10000, "Titanium": 12000}
    conrod_lim = cn_map.get(params.get('conrods', 'Heavy Duty'), 6000)

    pt_map = {"Cast": 6500, "Cast Heavy": 6000, "Cast Light": 6800, "Heavy Duty": 7000,
              "Forged": 8500, "Forged Heavy": 8000, "Forged Light": 9000,
              "LW Forged": 12000, "Hypereutectic Cast": 7200, "Low Friction": 7500}
    piston_lim = pt_map.get(params.get('pistons', 'Cast'), 6500)

    if race_architecture > 0.0:
        motorsport_limit = 12000.0 + 7000.0 * race_architecture
        crank_lim = max(crank_lim, motorsport_limit)
        conrod_lim = max(conrod_lim, motorsport_limit)
        piston_lim = max(piston_lim, motorsport_limit)
    
    part_limits = {"Kliková hřídel/Crankshaft": crank_lim, "Ojnice/Conrods": conrod_lim, "Písty/Pistons": piston_lim}
    weakest_part = min(part_limits, key=part_limits.get)
    mech_limit = part_limits[weakest_part]
    
    fuel_type = params.get('fuel_type', 'Premium 95')
    is_diesel = fuel_type == "Diesel"
    
    if rpm_limit > mech_limit:
        blow_up = True
        if lang == 'cz':
            blow_up_reason = f"Otáčky přetrhly motor vejpůl ({mech_limit} RPM). Nejslabší článek: {weakest_part}."
            blow_up_fix = f"V záložce 'Bottom End' vyměň '{weakest_part}' za odolnější materiál, nebo sniž Omezovač RPM pod {mech_limit}."
        else:
            blow_up_reason = f"Revs tore the engine apart ({mech_limit} RPM). Weakest link: {weakest_part}."
            blow_up_fix = f"In the 'Bottom End' tab, upgrade '{weakest_part}' to a stronger material, or lower RPM Limit below {mech_limit}."
        actual_limit = mech_limit
    else:
        actual_limit = rpm_limit

    rpm_range = np.arange(1000, actual_limit, 100)
    if rpm_range.size == 0 or rpm_range[-1] != actual_limit:
        rpm_range = np.append(rpm_range, actual_limit)
    octane_dict = {"Low Quality 85": 85, "Regular 85": 85, "Regular 91": 91, "Premium 95": 95, "Super 98": 98,
                   "Ultimate 100": 100, "E85": 105, "Methanol": 115, "Diesel": 0,
                   "Leaded Gasoline": 98, "Compressed Gas": 110, "Nitromethane": 150}
    octane = octane_dict.get(fuel_type, 95)

    ign_val = params.get('ignition', 50)
    ign_mult = 1.0 + (ign_val * 0.003)
    if is_diesel: ign_mult = 1.0 
    
    man = params.get('manifold', 'Standard')
    intake_conf = params.get('intake_conf', 'Single')
    man_mult, man_shift = 1.0, 0
    if "Race" in man: man_mult, man_shift = 1.1, 1000
    elif "Perf. High" in man: man_mult, man_shift = 1.08, 800
    elif "Perf" in man: man_mult, man_shift = 1.05, 500
    elif "Std. Mid" in man: man_mult, man_shift = 1.02, 200
    elif "Compact" in man: man_mult, man_shift = 0.9, -500
    elif "Low" in man: man_mult, man_shift = 0.95, -300
    elif "Variable" in man: man_mult, man_shift = 1.05, 0 # Variable broadens curve
    if intake_conf == "ITB": man_mult *= 1.08

    headers = params.get('headers', 'Cast')
    headers_mult = 1.0
    if "Compact Cast" in headers: headers_mult = 0.95
    elif "Cast Low" in headers: headers_mult = 0.96
    elif "Cast Mid" in headers: headers_mult = 0.97
    elif "Cast" in headers: headers_mult = 0.97
    elif "Tubular Race" in headers: headers_mult = 1.05
    elif "Tubular Long" in headers: headers_mult = 1.04
    elif "Tubular Mid" in headers: headers_mult = 1.03
    elif "Tubular" in headers: headers_mult = 1.02

    carb_sz = (params.get('carb_size', 50) - 50) / 50.0
    man_sz = (params.get('man_size', 50) - 50) / 50.0
    head_sz = (params.get('head_size', 50) - 50) / 50.0
    man_shift += (man_sz + head_sz + carb_sz) * 400

    raw_bonus = (ign_mult * man_mult * headers_mult) - 1.0
    if fuel_type == "Nitromethane": raw_bonus += 0.50 # Nitro cheat code
    
    asp = params.get('aspiration', 'NA')
    if raw_bonus > 0:
        max_bonus = 0.15 if asp == "NA" else 0.40
        if fuel_type == "Nitromethane": max_bonus = 1.0
        actual_bonus = max_bonus * (1.0 - np.exp(-raw_bonus / max_bonus))
        tuning_mult = 1.0 + actual_bonus
    else:
        tuning_mult = 1.0 + raw_bonus

    comp = params.get('comp_ratio', 10.0)
    afr = params.get('afr', 14.7)
    fuel_map = params.get('fuel_map', 50)
    
    if is_diesel:
        afr_mult = 1.0 
        diesel_coeff = 65 + tech_factor * 40
        base_torque = (disp_cc / 1000) * diesel_coeff * (1.0 + ((comp - 15) * 0.015)) * tuning_mult
    else:
        gas_coeff = 70 + tech_factor * 45
        afr_mult = 1.0 - 0.02 * ((afr - 13.0)**2)
        afr_mult *= 1.0 - abs(fuel_map - 50) * 0.0005
        base_torque = (disp_cc / 1000) * gas_coeff * (1.0 + ((comp - 10) * 0.025)) * afr_mult * tuning_mult

    cam = params.get('cam_profile', 30)
    valves = params.get('valves', 4)
    vvt = params.get('vvt', 'None')
    
    vvl_state = str(params.get('vvl', 'None'))
    if vvl_state == "True": vvl_state = "VVL"
    elif vvl_state == "False": vvl_state = "None"
    
    valvetrain = params.get('valvetrain', 'DOHC')

    vt_shift = 0
    if valvetrain == "Pushrod (OHV)": vt_shift = -800  
    elif valvetrain == "DOHC" or valvetrain == "DAOHC": vt_shift = 500   

    def build_ve_curve(c_prof):
        if is_diesel:
            peak_rpm = 1700 + (c_prof * 10) + ((valves - 2) * 120) + (man_shift * 0.20)
            left_spread = 900 + (c_prof * 8)
            right_spread = 1900 + (c_prof * 15)
            if vvt == "Intake": right_spread *= 1.15
            elif vvt == "All": right_spread *= 1.25
            
            # Plynulý základ 45 % pro naftu (běží bez škrtící klapky, nasává víc vzduchu)
            left_side = 0.45 + 0.55 * np.exp(-0.5 * ((rpm_range - peak_rpm) / left_spread)**2)
            right_side = 0.45 + 0.55 * np.exp(-0.5 * ((rpm_range - peak_rpm) / right_spread)**2)
            return np.where(rpm_range < peak_rpm, left_side, right_side)
        else:
            peak_rpm = 2800 + (c_prof * 24) + ((valves - 2) * 260) + (man_shift * 0.65) + (vt_shift * 0.45)
            left_spread = 1350 + (c_prof * 9)
            right_spread = 2050 + (c_prof * 15)
            if vvt == "Intake":
                left_spread *= 1.05
                right_spread *= 1.15
            elif vvt == "All":
                left_spread *= 1.15
                right_spread *= 1.30
            if "Variable" in man:
                left_spread *= 1.10
                right_spread *= 1.15

            # Asymetrická křivka: sériový motor po maximu momentu neklesá tak prudce,
            # aby byl realistický výkon ve vyšších otáčkách.
            left_side = 0.35 + 0.65 * np.exp(-0.5 * ((rpm_range - peak_rpm) / left_spread)**2)
            right_side = 0.35 + 0.65 * np.exp(-0.5 * ((rpm_range - peak_rpm) / right_spread)**2)
            road_curve = np.where(rpm_range < peak_rpm, left_side, right_side)
            if race_architecture <= 0.0:
                return road_curve

            # Pneumatic-valvetrain-era F1-style engines trade low-RPM filling for
            # breathing that remains strong almost to the limiter.
            race_peak = actual_limit * 0.90
            race_left = actual_limit * 0.28
            race_right = actual_limit * 0.45
            race_left_side = 0.12 + 0.62 * np.exp(-0.5 * ((rpm_range - race_peak) / race_left)**2)
            race_right_side = 0.12 + 0.62 * np.exp(-0.5 * ((rpm_range - race_peak) / race_right)**2)
            race_curve = np.where(rpm_range < race_peak, race_left_side, race_right_side)
            return road_curve * (1.0 - race_architecture) + race_curve * race_architecture

    ve_curve = build_ve_curve(cam)
    ve_curve *= (0.55 + 0.45 * tech_factor)
    
    if vvl_state in ["VVL", "CVVL"]:
        vvl_prof = params.get('vvl_prof', 60)
        vvl_rpm = params.get('vvl_rpm', 4000)
        ve_high = build_ve_curve(vvl_prof)
        if vvl_state == "CVVL": ve_high *= 1.08 
        else: ve_high *= 1.05
        blend = 1 / (1 + np.exp(-(rpm_range - vvl_rpm) / 200.0))
        ve_curve = ve_curve * (1 - blend) + np.maximum(ve_curve, ve_high) * blend

    if valvetrain == "Pushrod (OHV)":
        ohv_choke = np.exp(-0.5 * (np.maximum(0, rpm_range - 4200) / 900)**2)
        ve_curve *= ohv_choke

    piston_speed = 2 * (s / 1000.0) * (rpm_range / 60.0)
    piston_speed_limit = 22.0 + 18.0 * race_architecture
    speed_choke = np.where(
        piston_speed > piston_speed_limit,
        np.exp(-(piston_speed - piston_speed_limit) * 0.1),
        1.0
    )
    ve_curve *= speed_choke
    
    if is_diesel:
        diesel_choke = np.exp(-0.5 * (np.maximum(0, rpm_range - 4200) / 800)**2)
        ve_curve *= diesel_choke

    ve_curve *= (1.0 + (carb_sz + man_sz) * 0.05 * (rpm_range / max(rpm_range)))

    vt_base = {"Pushrod (OHV)": 4500, "SOHC": 6000, "DOHC": 7500, "DAOHC": 8500}.get(valvetrain, 6000)
    springs = params.get('springs', 50)
    valve_float_lim = vt_base + (springs * 40)
    if race_architecture > 0.0:
        valve_float_lim = max(
            valve_float_lim,
            12500.0 + 7500.0 * race_architecture
        )
    float_choke = np.where(rpm_range > valve_float_lim, np.exp(-(rpm_range - valve_float_lim) * 0.005), 1.0)
    ve_curve *= float_choke
    friction_mult *= (1.0 + (springs - 50) * 0.001)

    # 3. Integrace Fuel Delivery (Typ vstřikování ovlivňuje účinnost sání a Knock index)
    f_deliv = params.get('fuel_deliv', 'EFI Multi')
    knock_modifier = 0
    if "Carburetor" in f_deliv or "Mechanical" in f_deliv or "Single Point" in f_deliv:
        ve_curve *= 0.96
        knock_modifier += 2
    elif f_deliv == "Direct Injection":
        ve_curve *= 1.05
        knock_modifier -= 5

    # 4. Integrace Head Material (Litinová hlava drží teplo a způsobuje klepání, Hliník odvádí)
    h_mat = params.get('head_mat', 'Aluminium')
    if "Iron" in h_mat: knock_modifier += 3
    if "Eco" in h_mat: friction_mult *= 0.98; knock_modifier += 1
    elif "Perf" in h_mat: knock_modifier -= 1
    elif "Billet Race" in h_mat: knock_modifier -= 2; friction_mult *= 0.95
    elif h_mat == "Aluminium": knock_modifier -= 1

    knock_modifier -= (fuel_map - 50) * 0.1

    torque = base_torque * ve_curve

    active_boost = 0.0
    if asp == "Turbo":
        active_boost = params.get('boost', 0.5)
        turb_size = params.get('turb_size', 50)
        ic_size = params.get('intercooler', 50)
        
        # Spool je závislý na velikosti turba, průtoku motoru, počtu turbodmychadel a ložiscích.
        displacement_l = max(0.5, disp_cc / 1000.0)
        lag_rpm = 1500 + (turb_size * 18) + (ic_size * 1.0) - min(700, max(0.0, displacement_l - 1.0) * 140)
        t_conf = params.get('turbo_config', 'Single')
        if t_conf == "Twin": lag_rpm -= 300
        elif t_conf == "Quad": lag_rpm -= 550
        if params.get('turbo_bearing', 'Journal') == "Ball Bearings": lag_rpm -= 250
        lag_rpm = clamp(lag_rpm, 1100.0, 5200.0)

        # Intercooler primárně zlepšuje hustotu náplně a odolnost proti klepání;
        # nemá násobit nebo rušit nastavený plnicí tlak.
        charge_eff = 0.86 + 0.12 * (ic_size / 100.0)
        knock_modifier -= ic_size * 0.04
        spool_smoothness = 260.0
        spool = 1.0 / (1.0 + np.exp(-(rpm_range - lag_rpm) / spool_smoothness))
        boost_curve = 1.0 + active_boost * charge_eff * spool
        torque *= boost_curve
        
    elif asp == "Supercharger":
        active_boost = params.get('sc_pulley', 0.8)
        sc_type = params.get('sc_type', 'Roots')
        
        # 6. Integrace velikosti kompresoru (Zvyšuje průtok ve vysokých RPM, ale odebírá mechanickou sílu)
        c_size = params.get('comp_size', 50)
        sc_efficiency = (c_size / 100.0)
        parasitic_loss = (c_size / 100.0) * active_boost * 15.0 # Větší kompresor = větší ztráta v Nm
        
        if sc_type == "Roots": torque *= (1.0 + active_boost * 0.9 * sc_efficiency)
        elif sc_type == "Centrifugal": torque *= (1.0 + (active_boost * 1.15 * sc_efficiency * (rpm_range / max(rpm_range))))
        elif sc_type == "Twin-screw": torque *= (1.0 + active_boost * 1.0 * sc_efficiency)
        
        torque -= parasitic_loss
        torque = np.maximum(torque, 0.0)

    lean_penalty = (afr - 14.7) * 4 if afr > 14.7 else 0
    
    knock_modifier -= (tech_factor - 1.0) * 30
    
    if is_diesel:
        knock_index = 0 
    else:
        effective_comp = comp + (active_boost * 1.5)
        knock_index = max(0, (effective_comp * 5.0) + (ign_val * 0.2) + lean_penalty - octane + 22 + knock_modifier)

    if knock_index > 0:
        torque *= np.exp(-0.08 * knock_index)
        if knock_index > 20 and not blow_up:
            blow_up = True
            if lang == 'cz':
                blow_up_reason = "Extrémní detonační hoření (Knock)! Směs explodovala sama a písty se roztavily."
                blow_up_fix = "Sniž kompresní poměr, dej palivo s vyšším oktanovým číslem, sniž Tlak (Boost), stáhni Předstih, nebo obohať směs (nižší AFR)."
            else:
                blow_up_reason = "Extreme Knock detected! Premature detonation melted the pistons."
                blow_up_fix = "Lower Compression, use higher Octane fuel, lower Boost, retard Ignition Timing, or run richer AFR."

    exh_diam = params.get('exh_diam', 50.0)
    if params.get('exh_arch', 'Single') == "Dual": exh_diam *= 1.414 
    peak_torque_for_exhaust = max(0.0, float(np.max(torque)))
    req_diam = math.sqrt(peak_torque_for_exhaust / 2.0) * 2.5 if peak_torque_for_exhaust > 0.0 else 0.0
    if req_diam > 0.0 and exh_diam < req_diam:
        choke_factor = 1.0 - ((req_diam - exh_diam) / req_diam) * (rpm_range / max(rpm_range))
        torque *= np.maximum(0.5, choke_factor)

    muff1 = params.get('muffler1', 'Baffled')
    muff2 = params.get('muffler2', 'Baffled')
    muff_mult1 = 1.0
    muff_mult2 = 1.0

    if "Baffled" in muff1: muff_mult1 = 0.98
    elif "Reverse Flow" in muff1 or "Reverse" in muff1: muff_mult1 = 0.96
    if "Baffled" in muff2: muff_mult2 = 0.98
    elif "Reverse Flow" in muff2 or "Reverse" in muff2: muff_mult2 = 0.96

    total_muff = muff_mult1 * muff_mult2
    if params.get('bypass', 'No Valves') == "Bypass Valves":
        bypass_open = 1 / (1 + np.exp(-(rpm_range - 3500) / 200.0))
        torque *= (total_muff * (1 - bypass_open) + 1.0 * bypass_open)
    else:
        torque *= total_muff

    cat = params.get('cat', '3-way')
    if "2-way" in cat: torque *= 0.97
    elif ("3-way" in cat or "3-Way" in cat or "Three-Way" in cat) and "High Flow" not in cat: torque *= 0.985
    elif "High Flow" in cat: torque *= 0.995
    elif "Reactor" in cat: torque *= 0.95

    friction_mult *= (1.4 - 0.4 * tech_factor)
    cyl_count = c
    friction_torque = (disp_cc / 1000.0) * (4.0 + (cyl_count * 0.5) + 0.8 * (rpm_range / 1000.0)**1.5) * friction_mult
    torque = torque - friction_torque
    torque = np.maximum(torque, 0)

    hp = (torque * rpm_range) / 7127.0  # mechanical horsepower (HP), not metric PS
    
    return {
        "rpm": rpm_range, 
        "torque": torque, 
        "hp": hp, 
        "blew_up": blow_up, 
        "reason": blow_up_reason, 
        "fix": blow_up_fix
    }

def run_vehicle_kinematics(veh_params, engine_data):
    """Jednoduchá podélná dynamika vozu s omezením trakcí, převody, redlinem a aerodynamikou."""
    dt = 0.02
    rpm_arr = np.asarray(engine_data['rpm'], dtype=float)
    trq_arr = np.asarray(engine_data['torque'], dtype=float)
    if rpm_arr.size == 0 or trq_arr.size != rpm_arr.size:
        raise ValueError("Engine curve is empty or inconsistent")
    if not np.all(np.isfinite(rpm_arr)) or not np.all(np.isfinite(trq_arr)) or np.max(trq_arr) <= 0.0:
        raise ValueError("Engine curve has no usable torque")

    max_rpm = float(rpm_arr[-1])
    max_hp_idx = int(np.argmax(engine_data["hp"]))
    max_hp_rpm = float(engine_data["rpm"][max_hp_idx])
    ideal_shift_rpm = min(max_rpm - 50.0, max_hp_rpm + 400.0)

    mass = clamp(float(veh_params.get('weight', 1350.0)), 500.0, 3000.0)
    cd = clamp(float(veh_params.get('cd', 0.30)), 0.15, 0.80)
    area = clamp(float(veh_params.get('area', 2.2)), 1.2, 4.0)
    grip = clamp(float(veh_params.get('grip', 0.9)), 0.3, 2.5)
    wheel_radius = clamp(float(veh_params.get('wheel_radius', 0.33)), 0.20, 0.55)
    speed_limiter_kmh = max(0.0, float(veh_params.get('speed_limiter', 0.0)))
    downforce_cla = clamp(float(veh_params.get('downforce_cla', 0.0)), 0.0, 4.0)
    gear_count = int(clamp(int(veh_params.get('gears', 5)), 4, 8))
    fd = clamp(float(veh_params.get('final_drive', 4.1)), 1.5, 10.0)
    drivetrain = veh_params.get('drivetrain', 'FWD')
    ratios = get_gear_ratios(gear_count, veh_params.get('gear_ratios'))

    drivetrain_eff = {"FWD": 0.90, "RWD": 0.88, "AWD": 0.82}.get(drivetrain, 0.88)
    rho = 1.2
    g = 9.81
    rolling_coeff = 0.015
    wheelbase = 2.7
    cg_height = 0.5
    w_f = 0.60 if drivetrain == "FWD" else 0.50
    w_r = 1.0 - w_f

    sim_v = 0.0
    sim_gear = 0
    sim_time = 0.0
    sim_time_100 = None
    sim_time_60_mph = None
    sim_shift_delay = 0.0
    sim_a_prev = 0.0
    sim_max_v = 0.0

    max_sim_steps = int(300 / dt)
    peak_trq_rpm = float(rpm_arr[int(np.argmax(trq_arr))])
    launch_rpm = min(max(1800.0, peak_trq_rpm * 0.85), max_rpm * 0.75)

    for _ in range(max_sim_steps):
        sim_time += dt
        sim_max_v = max(sim_max_v, sim_v)
        if sim_time_100 is None and sim_v * 3.6 >= 100.0:
            sim_time_100 = sim_time
        if sim_time_60_mph is None and sim_v * 2.2369362920544 >= 60.0:
            sim_time_60_mph = sim_time

        drag = 0.5 * rho * cd * area * sim_v**2
        roll = mass * g * rolling_coeff
        a = 0.0
        is_shifting_now = sim_shift_delay > 0.0
        if is_shifting_now:
            sim_shift_delay = max(0.0, sim_shift_delay - dt)
            a = -(drag + roll) / mass
        else:
            wheel_rpm = (sim_v / (2.0 * math.pi * wheel_radius)) * 60.0
            engine_rpm = wheel_rpm * ratios[sim_gear] * fd
            calc_rpm = launch_rpm if sim_gear == 0 and engine_rpm < launch_rpm else max(1000.0, engine_rpm)

            if calc_rpm > ideal_shift_rpm and sim_gear < gear_count - 1:
                sim_gear += 1
                sim_shift_delay = 0.20
                is_shifting_now = True
                a = -(drag + roll) / mass
            else:
                over_redline = sim_gear == gear_count - 1 and engine_rpm > max_rpm
                electronically_limited = speed_limiter_kmh > 0.0 and sim_v * 3.6 >= speed_limiter_kmh
                if over_redline or electronically_limited:
                    force_wheel = 0.0
                else:
                    calc_rpm = min(calc_rpm, max_rpm)
                    current_trq = float(np.interp(calc_rpm, rpm_arr, trq_arr))
                    force_wheel = (current_trq * ratios[sim_gear] * fd * drivetrain_eff) / wheel_radius

                aero_downforce = 0.5 * rho * downforce_cla * sim_v**2
                transfer = (mass * sim_a_prev * cg_height) / wheelbase
                if drivetrain == "FWD":
                    driven_weight = mass * g * w_f - transfer + aero_downforce * 0.40
                elif drivetrain == "RWD":
                    driven_weight = mass * g * w_r + transfer + aero_downforce * 0.60
                else:
                    driven_weight = mass * g + aero_downforce
                max_grip_force = max(0.0, driven_weight * grip)
                force_wheel = min(force_wheel, max_grip_force)
                a = (force_wheel - drag - roll) / (mass * 1.05)

        sim_a_prev = a
        sim_v = max(0.0, sim_v + a * dt)
        if not is_shifting_now and abs(a) < 0.001 and sim_v > 15.0:
            break

    return {
        "time_0_100": sim_time_100,
        "time_0_60_mph": sim_time_60_mph,
        "top_speed": sim_max_v,
        "final_gear": sim_gear
    }

class ToolTip(object):
    """One in-app tooltip at a time, with reliable cleanup across screen changes."""
    _active_tooltip = None

    def __init__(self, widget, text_var):
        self.widget = widget
        self.text_var = text_var
        self.tipwindow = None
        self.id = None
        self.widget.bind("<Enter>", self.enter, add="+")
        self.widget.bind("<Leave>", self.leave, add="+")
        self.widget.bind("<ButtonPress>", self.leave, add="+")
        self.widget.bind("<Unmap>", self.leave, add="+")
        self.widget.bind("<Destroy>", self.leave, add="+")

    @classmethod
    def hide_active(cls):
        active = cls._active_tooltip
        if active is not None:
            active.unschedule()
            active.hidetip()

    def enter(self, event=None):
        self.schedule()

    def leave(self, event=None):
        self.unschedule()
        self.hidetip()

    def schedule(self):
        self.unschedule()
        try:
            self.id = self.widget.after(500, self.showtip)
        except tk.TclError:
            self.id = None

    def unschedule(self):
        after_id = self.id
        self.id = None
        if after_id:
            try:
                self.widget.after_cancel(after_id)
            except tk.TclError:
                pass

    def _pointer_is_inside_widget(self):
        try:
            if not self.widget.winfo_exists() or not self.widget.winfo_ismapped():
                return False
            px, py = self.widget.winfo_pointerxy()
            x0, y0 = self.widget.winfo_rootx(), self.widget.winfo_rooty()
            return x0 <= px < x0 + self.widget.winfo_width() and y0 <= py < y0 + self.widget.winfo_height()
        except tk.TclError:
            return False

    def showtip(self, event=None):
        self.id = None
        if not self._pointer_is_inside_widget():
            return
        if ToolTip._active_tooltip is not None and ToolTip._active_tooltip is not self:
            ToolTip._active_tooltip.hidetip()
        self.hidetip()
        try:
            root = self.widget.winfo_toplevel()
            txt = self.text_var.get() if isinstance(self.text_var, tk.StringVar) else self.text_var
            label = tk.Label(root, text=txt, justify=tk.LEFT, wraplength=430,
                             background="#202a35", foreground="white", relief=tk.SOLID,
                             borderwidth=1, font=("tahoma", "9", "normal"), padx=8, pady=6)
            root.update_idletasks()
            x = self.widget.winfo_pointerx() - root.winfo_rootx() + 16
            y = self.widget.winfo_pointery() - root.winfo_rooty() + 18
            x = max(8, min(x, max(8, root.winfo_width() - 450)))
            y = max(8, min(y, max(8, root.winfo_height() - 160)))
            label.place(x=x, y=y)
            label.lift()
            self.tipwindow = label
            ToolTip._active_tooltip = self
        except tk.TclError:
            self.tipwindow = None

    def hidetip(self):
        tw = self.tipwindow
        self.tipwindow = None
        if ToolTip._active_tooltip is self:
            ToolTip._active_tooltip = None
        if tw is not None:
            try:
                if tw.winfo_exists():
                    tw.destroy()
            except tk.TclError:
                pass
# --- FULLSCREEN OBRAZOVKY 4.9.1 ---
class AutoScrollFrame(ttk.Frame):
    """Obsah s automatickým svislým scrollováním pouze při skutečném přetečení."""
    def __init__(self, parent, background="#101720", **kwargs):
        super().__init__(parent, **kwargs)
        self._background = background
        self._overflow = False
        self._refresh_pending = False

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.canvas = tk.Canvas(
            self, bg=background, highlightthickness=0, bd=0,
            xscrollincrement=0, yscrollincrement=24
        )
        self.scrollbar = ttk.Scrollbar(self, orient=tk.VERTICAL, command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        self.canvas.grid(row=0, column=0, sticky="nsew")

        self.content = ttk.Frame(self.canvas, padding=18)
        self._window_id = self.canvas.create_window((0, 0), window=self.content, anchor="nw")

        self.content.bind("<Configure>", self._schedule_refresh, add="+")
        self.canvas.bind("<Configure>", self._schedule_refresh, add="+")

        # Kolečko funguje i nad vnořenými Entry/Combobox/Scale prvky. Každý
        # scrollovací panel zareaguje jen tehdy, když je viditelný a kurzor je nad ním.
        root = self.winfo_toplevel()
        root.bind_all("<MouseWheel>", self._on_mousewheel, add="+")
        root.bind_all("<Button-4>", self._on_mousewheel, add="+")
        root.bind_all("<Button-5>", self._on_mousewheel, add="+")

    def _schedule_refresh(self, event=None):
        if self._refresh_pending:
            return
        self._refresh_pending = True
        self.after_idle(self.refresh)

    def refresh(self):
        self._refresh_pending = False
        if not self.winfo_exists():
            return
        self.update_idletasks()

        viewport_width = max(1, self.canvas.winfo_width())
        viewport_height = max(1, self.canvas.winfo_height())
        requested_height = max(1, self.content.winfo_reqheight())
        content_height = max(viewport_height, requested_height)

        self.canvas.itemconfigure(
            self._window_id, width=viewport_width, height=content_height
        )
        self.canvas.configure(scrollregion=(0, 0, viewport_width, content_height))

        overflow = requested_height > viewport_height + 2
        if overflow != self._overflow:
            self._overflow = overflow
            if overflow:
                self.scrollbar.grid(row=0, column=1, sticky="ns")
            else:
                self.scrollbar.grid_remove()
                self.canvas.yview_moveto(0.0)

    def _pointer_is_inside(self):
        try:
            pointer_x = self.winfo_pointerx()
            pointer_y = self.winfo_pointery()
            left = self.canvas.winfo_rootx()
            top = self.canvas.winfo_rooty()
            right = left + self.canvas.winfo_width()
            bottom = top + self.canvas.winfo_height()
            return left <= pointer_x < right and top <= pointer_y < bottom
        except tk.TclError:
            return False

    def _on_mousewheel(self, event):
        if not self._overflow or not self.winfo_ismapped() or not self._pointer_is_inside():
            return None

        if getattr(event, "num", None) == 4:
            steps = -1
        elif getattr(event, "num", None) == 5:
            steps = 1
        else:
            delta = getattr(event, "delta", 0)
            if delta == 0:
                return None
            steps = -1 if delta > 0 else 1
            magnitude = max(1, abs(int(delta / 120)))
            steps *= magnitude

        self.canvas.yview_scroll(steps, "units")
        return "break"

    def scroll_to_top(self):
        self.canvas.yview_moveto(0.0)


class EmbeddedScreen(tk.Frame):
    """Frame kompatibilní s původním rozhraním Toplevel, vložený do jediného okna."""
    def __init__(self, app, name, **kwargs):
        super().__init__(app.screen_container, **kwargs)
        self.app = app
        self.screen_name = name
        self._alive = True

    def title(self, *args, **kwargs):
        return None

    def geometry(self, *args, **kwargs):
        return None

    def resizable(self, *args, **kwargs):
        return None

    def protocol(self, *args, **kwargs):
        return None

    def transient(self, *args, **kwargs):
        return None

    def grab_set(self, *args, **kwargs):
        return None

    def grab_release(self, *args, **kwargs):
        return None

    def lift(self, *args, **kwargs):
        if self._alive:
            self.app.show_screen(self.screen_name)

    def winfo_exists(self):
        return int(self._alive and super().winfo_exists())

    def destroy(self):
        if not self._alive:
            return
        self._alive = False
        self.app.screens.pop(self.screen_name, None)
        super().destroy()

# --- HLAVNÍ APLIKACE (GUI) ---
class EngineApp:
    def __init__(self, root):
        self.root = root
        self.vars = {}
        self.allowed_values = {}
        self._suspend_vehicle_preset_callback = False
        self.vars['app_lang'] = tk.StringVar(value='cz')
        
        self.lang_vars = {k: tk.StringVar(value=v) for k, v in T['cz'].items()}
        
        self.root.title(self.lang_vars['app_title'].get())
        self.root.minsize(1100, 700)
        self.fullscreen = True
        self.root.attributes("-fullscreen", True)
        self.root.bind("<F11>", self.toggle_fullscreen)
        self.root.bind("<Escape>", self.handle_escape)
        self.root.protocol("WM_DELETE_WINDOW", self.shutdown)
        self.screens = {}
        self.current_screen = None
        self.nav_buttons = {}
        self.graph_figure = None
        self.graph_canvas = None
        self._message_overlay = None
        self._settings_overlay = None
        self._dyno_after_id = None
        self._throttle_after_id = None
        self._drive_after_id = None
        self._track_after_id = None
        self._screen_transitioning = False
        self.track_canvas_width = 640
        self.track_canvas_height = 500
        self._track_layout_pending = False
        self._track_redraw_pending = False
        self._track_compact_layout = None
        self.track_current_distance = 0.0
        
        self.setup_master_presets()
        self.create_variables()
        self.snapshot_factory_defaults()
        self.create_menu()
        self.configure_styles()
        self.create_shell()
        self.create_language_selector()
        self.create_widgets()
        self.show_screen("builder")
        messagebox.showerror = self.show_error_overlay
        
        self.dyno_results = {}
        self.dyno_params = None
        self._dyno_running = False
        self._dyno_changed_during_run = False
        self.bind_dyno_invalidation_traces()
        self.update_displacement()
        self.update_dynamic_ui()

    def tr(self, key):
        return self.lang_vars.get(key, tk.StringVar(value="")).get()

    def _ui(self, cz_text, en_text):
        return cz_text if self.vars['app_lang'].get() == 'cz' else en_text

    def _speed_unit_label(self):
        return "mph" if self.speed_unit.get() == 'mph' else "km/h"

    def _speed_from_mps(self, speed_mps):
        factor = 2.2369362920544 if self.speed_unit.get() == 'mph' else 3.6
        return float(speed_mps) * factor

    def _speed_from_kmh(self, speed_kmh):
        if self.speed_unit.get() == 'mph':
            return float(speed_kmh) * 0.621371192237334
        return float(speed_kmh)

    def _speed_to_kmh(self, displayed_speed):
        if self.speed_unit.get() == 'mph':
            return float(displayed_speed) / 0.621371192237334
        return float(displayed_speed)

    def _speed_limiter_display_max(self):
        return 280.0 if self.speed_unit.get() == 'mph' else 450.0

    def _sync_speed_limiter_display_from_canonical(self, *args):
        if getattr(self, '_speed_limiter_syncing', False):
            return
        try:
            canonical = float(self.vars['speed_limiter'].get())
        except (ValueError, TypeError, tk.TclError, KeyError, AttributeError):
            return
        if not hasattr(self, 'speed_limiter_display'):
            return
        self._speed_limiter_syncing = True
        try:
            self.speed_limiter_display.set(round(self._speed_from_kmh(canonical), 1))
        finally:
            self._speed_limiter_syncing = False

    def _sync_speed_limiter_canonical_from_display(self, *args):
        if getattr(self, '_speed_limiter_syncing', False):
            return
        try:
            displayed = float(self.speed_limiter_display.get())
        except (ValueError, TypeError, tk.TclError, AttributeError):
            return
        canonical = clamp(self._speed_to_kmh(displayed), 0.0, 450.0)
        normalized_display = self._speed_from_kmh(canonical)
        self._speed_limiter_syncing = True
        try:
            self.vars['speed_limiter'].set(round(canonical, 3))
            self.speed_limiter_display.set(round(normalized_display, 1))
        finally:
            self._speed_limiter_syncing = False

    def _acceleration_label(self):
        return "0-60 mph" if self.speed_unit.get() == 'mph' else "0-100 km/h"

    def _acceleration_target_mps(self):
        if self.speed_unit.get() == 'mph':
            return 60.0 / 2.2369362920544
        return 100.0 / 3.6

    def _selected_acceleration_time(self, result):
        key = 'time_0_60_mph' if self.speed_unit.get() == 'mph' else 'time_0_100'
        return result.get(key)

    def _refresh_screen_title(self):
        titles = {
            "builder": ("GARÁŽ / STAVBA MOTORU", "GARAGE / ENGINE BUILDER"),
            "dyno": ("DYNO & ŽIVÝ GRAF", "DYNO & LIVE GRAPH"),
            "throttle": ("RUČNÍ PLYN", "MANUAL THROTTLE"),
            "drive": ("ZKUŠEBNÍ JÍZDA", "TEST DRIVE"),
            "track": ("SIMULACE OKRUHU", "TRACK SIMULATION"),
        }
        if self.current_screen in titles:
            self.screen_title.set(self._ui(*titles[self.current_screen]))

    def update_settings_summary(self):
        if not hasattr(self, 'settings_summary_var'):
            return
        lang = "CZ" if self.vars['app_lang'].get() == 'cz' else "EN"
        self.settings_summary_var.set(f"⚙  {lang}  •  {self._speed_unit_label()}")

    def apply_speed_unit(self):
        if self.speed_unit.get() not in ('kmh', 'mph'):
            self.speed_unit.set('kmh')
        self.speed_unit_text.set(self._speed_unit_label())
        if hasattr(self, 'speed_limiter_scale'):
            self.speed_limiter_scale.configure(to=self._speed_limiter_display_max())
        self._sync_speed_limiter_display_from_canonical()
        self.update_settings_summary()
        self._refresh_localized_screen_texts()

    def _refresh_speed_displays(self):
        """Refresh visible values without restarting or altering any simulation."""
        drive = getattr(self, 'drive_win', None)
        if drive is not None and drive.winfo_exists():
            if hasattr(self, 'lbl_speed'):
                self.lbl_speed.config(text=f"{self._speed_from_mps(getattr(self, 'v', 0.0)):.0f}")
            if (hasattr(self, 'lbl_tcs') and getattr(self, 'max_achieved_speed', 0.0) > 0.0
                    and not getattr(self, 'drive_running', False)):
                self.lbl_tcs.config(
                    text=f"{self.tr('ui_max')}: {self._speed_from_mps(self.max_achieved_speed):.0f} {self._speed_unit_label()}"
                )
            if hasattr(self, 'lbl_accel'):
                result = getattr(self, 'drive_reference_result', None)
                if result is not None and not getattr(self, 'drive_running', False):
                    self.accel_time = self._selected_acceleration_time(result)
                    if self.accel_time is None:
                        value = self.tr('msg_not_reached')
                    else:
                        value = f"{self.accel_time:.2f} s"
                    self.lbl_accel.config(text=f"{self._acceleration_label()}: {value}")
                elif getattr(self, 'drive_running', False):
                    selected = self._selected_acceleration_time(result or {})
                    if getattr(self, 'v', 0.0) >= self._acceleration_target_mps() and selected is not None:
                        self.accel_time = selected
                        self.lbl_accel.config(text=f"{self._acceleration_label()}: {selected:.2f} s")
                    else:
                        self.accel_time = None
                        self.lbl_accel.config(
                            text=f"{self._acceleration_label()}: {getattr(self, 'drive_time', 0.0):.1f} s"
                        )

        track = getattr(self, 'track_win', None)
        if track is not None and track.winfo_exists():
            if hasattr(self, 'lbl_track_live_speed'):
                speed_mps = 0.0
                if self.track_result is not None:
                    cumulative = self.track_result['cumulative_time']
                    shown = min(getattr(self, 'track_sim_elapsed', 0.0), self.track_result['lap_time'])
                    idx = int(np.searchsorted(cumulative, shown, side='right') - 1)
                    idx = int(clamp(idx, 0, len(cumulative) - 2))
                    speed_mps = float(self.track_result['speed_profile'][idx])
                self.lbl_track_live_speed.config(
                    text=f"{self.tr('lbl_track_speed')}: {self._speed_from_mps(speed_mps):.0f} {self._speed_unit_label()}"
                )
            if (self.track_result is not None and not getattr(self, 'track_running', False)
                    and hasattr(self, 'lbl_track_stats')):
                self.lbl_track_stats.config(
                    text=(f"{self.tr('lbl_track_length')}: {self.track_result['track_length'] / 1000.0:.3f} km\n"
                          f"{self.tr('lbl_track_avg')}: {self._speed_from_mps(self.track_result['average_speed']):.1f} {self._speed_unit_label()}\n"
                          f"{self.tr('lbl_track_max')}: {self._speed_from_mps(self.track_result['max_speed']):.1f} {self._speed_unit_label()}")
                )

    def open_settings_overlay(self):
        ToolTip.hide_active()
        if self._settings_overlay is not None and self._settings_overlay.winfo_exists():
            self._settings_overlay.lift()
            return
        overlay = tk.Frame(self.root, bg="#05080c")
        overlay.place(relx=0, rely=0, relwidth=1, relheight=1)
        panel = tk.Frame(overlay, bg="#101720", highlightbackground="#43d9ff", highlightthickness=2)
        panel.place(relx=0.5, rely=0.5, anchor=tk.CENTER, relwidth=0.56, relheight=0.84)
        panel.grid_columnconfigure(0, weight=1)
        panel.grid_columnconfigure(1, weight=1)

        tk.Label(panel, textvariable=self.lang_vars['settings_title'], bg="#101720", fg="white",
                 font=("Arial", 20, "bold")).grid(row=0, column=0, columnspan=2, pady=(34, 26))

        files = tk.LabelFrame(panel, text=self.tr('settings_files'), bg="#101720", fg="#43d9ff",
                              font=("Arial", 11, "bold"), bd=1, relief=tk.GROOVE, padx=22, pady=20)
        files.grid(row=1, column=0, columnspan=2, sticky="ew", padx=42, pady=10)
        files.grid_columnconfigure(0, weight=1)
        files.grid_columnconfigure(1, weight=1)
        tk.Button(files, textvariable=self.lang_vars['menu_load'],
                  command=lambda: self._run_settings_action(self.load_engine),
                  bg="#223447", fg="white", activebackground="#2e4961", activeforeground="white",
                  relief=tk.FLAT, padx=18, pady=12, font=("Arial", 10, "bold"), cursor="hand2").grid(
                      row=0, column=0, sticky="ew", padx=(0, 8))
        tk.Button(files, textvariable=self.lang_vars['menu_save'],
                  command=lambda: self._run_settings_action(self.save_engine),
                  bg="#223447", fg="white", activebackground="#2e4961", activeforeground="white",
                  relief=tk.FLAT, padx=18, pady=12, font=("Arial", 10, "bold"), cursor="hand2").grid(
                      row=0, column=1, sticky="ew", padx=(8, 0))

        language = tk.LabelFrame(panel, text=self.tr('settings_language'), bg="#101720", fg="#43d9ff",
                                 font=("Arial", 11, "bold"), bd=1, relief=tk.GROOVE, padx=22, pady=16)
        language.grid(row=2, column=0, sticky="nsew", padx=(42, 10), pady=10)
        lang_common = dict(variable=self.vars['app_lang'], command=self.apply_language, bg="#101720",
                           fg="#e7edf3", activebackground="#101720", activeforeground="white",
                           selectcolor="#172330", font=("Arial", 11), bd=0)
        tk.Radiobutton(language, text="CZ  Čeština", value='cz', **lang_common).pack(anchor="w", pady=6)
        tk.Radiobutton(language, text="GB  English", value='en', **lang_common).pack(anchor="w", pady=6)

        units = tk.LabelFrame(panel, text=self.tr('settings_speed_units'), bg="#101720", fg="#43d9ff",
                              font=("Arial", 11, "bold"), bd=1, relief=tk.GROOVE, padx=22, pady=16)
        units.grid(row=2, column=1, sticky="nsew", padx=(10, 42), pady=10)
        unit_common = dict(variable=self.speed_unit, command=self.apply_speed_unit, bg="#101720",
                           fg="#e7edf3", activebackground="#101720", activeforeground="white",
                           selectcolor="#172330", font=("Arial", 11), bd=0)
        tk.Radiobutton(units, textvariable=self.lang_vars['settings_kmh'], value='kmh', **unit_common).pack(anchor="w", pady=6)
        tk.Radiobutton(units, textvariable=self.lang_vars['settings_mph'], value='mph', **unit_common).pack(anchor="w", pady=6)

        audio = tk.LabelFrame(panel, text=self.tr('settings_audio'), bg="#101720", fg="#43d9ff",
                              font=("Arial", 11, "bold"), bd=1, relief=tk.GROOVE, padx=22, pady=14)
        audio.grid(row=3, column=0, columnspan=2, sticky="ew", padx=42, pady=10)
        audio.grid_columnconfigure(0, weight=1)
        audio_status_key = 'sound_ready' if SOUND_AVAILABLE else 'sound_missing'
        audio_status_color = '#63f28a' if SOUND_AVAILABLE else '#ffcc55'
        tk.Label(audio, text=self.tr(audio_status_key), bg="#101720", fg=audio_status_color,
                 font=("Arial", 10, "bold"), wraplength=620, justify=tk.LEFT).grid(
                     row=0, column=0, sticky="w", padx=(0, 16), pady=4)
        if not SOUND_AVAILABLE:
            tk.Button(audio, textvariable=self.lang_vars['sound_help'], command=self.show_sound_help,
                      bg="#7a5a19", fg="white", activebackground="#a77a20", activeforeground="white",
                      relief=tk.FLAT, padx=14, pady=9, font=("Arial", 9, "bold"), cursor="hand2").grid(
                          row=0, column=1, sticky="e")

        actions = tk.Frame(panel, bg="#101720")
        actions.grid(row=4, column=0, columnspan=2, sticky="ew", padx=42, pady=(22, 30))
        actions.grid_columnconfigure(0, weight=1)
        actions.grid_columnconfigure(1, weight=1)
        tk.Button(actions, textvariable=self.lang_vars['settings_close'], command=self.close_settings_overlay,
                  bg="#223447", fg="white", activebackground="#2e4961", activeforeground="white",
                  relief=tk.FLAT, padx=18, pady=13, font=("Arial", 10, "bold"), cursor="hand2").grid(
                      row=0, column=0, sticky="ew", padx=(0, 8))
        tk.Button(actions, textvariable=self.lang_vars['settings_quit'], command=self.shutdown,
                  bg="#8b2f3a", fg="white", activebackground="#b23f4c", activeforeground="white",
                  relief=tk.FLAT, padx=18, pady=13, font=("Arial", 10, "bold"), cursor="hand2").grid(
                      row=0, column=1, sticky="ew", padx=(8, 0))

        self._settings_overlay = overlay
        overlay.lift()

    def close_settings_overlay(self):
        if self._settings_overlay is not None and self._settings_overlay.winfo_exists():
            self._settings_overlay.destroy()
        self._settings_overlay = None

    def _run_settings_action(self, action):
        self.close_settings_overlay()
        action()

    def configure_styles(self):
        style = ttk.Style(self.root)
        try:
            style.theme_use("clam")
        except tk.TclError:
            pass
        style.configure("TFrame", background="#101720")
        style.configure("TLabel", background="#101720", foreground="#e7edf3",
                        font=("Arial", 11))
        style.configure("TCheckbutton", background="#101720", foreground="#e7edf3",
                        font=("Arial", 10))
        style.map("TCheckbutton", background=[("active", "#101720")])
        style.configure("TButton", background="#223447", foreground="white",
                        font=("Arial", 10, "bold"), padding=(14, 9), borderwidth=0)
        style.map("TButton",
                  background=[("active", "#2e4961"), ("disabled", "#18222d")],
                  foreground=[("disabled", "#5e6d7b")])
        style.configure("TEntry", fieldbackground="#172330", foreground="white",
                        insertcolor="white", padding=7)
        style.configure("TCombobox", fieldbackground="#172330", background="#223447",
                        foreground="white", arrowcolor="#43d9ff", padding=7)
        style.map("TCombobox",
                  fieldbackground=[("readonly", "#172330")],
                  foreground=[("readonly", "white")],
                  selectbackground=[("readonly", "#172330")],
                  selectforeground=[("readonly", "white")])
        style.configure("Horizontal.TScale", background="#101720", troughcolor="#263645")
        style.configure("TNotebook", background="#0b1017", borderwidth=0, tabmargins=(0, 0, 0, 0))
        style.configure("TNotebook.Tab", background="#18232e", foreground="#aebdca",
                        font=("Arial", 10, "bold"), padding=(18, 11), borderwidth=0)
        style.map("TNotebook.Tab",
                  background=[("selected", "#1e3a4c"), ("active", "#223447")],
                  foreground=[("selected", "#43d9ff"), ("active", "white")])
        style.configure("TLabelframe", background="#101720", foreground="#43d9ff",
                        bordercolor="#2b3c4b", relief=tk.FLAT)
        style.configure("TLabelframe.Label", background="#101720", foreground="#43d9ff",
                        font=("Arial", 10, "bold"))

    def create_shell(self):
        self.root.configure(bg="#090d12")
        self.shell = tk.Frame(self.root, bg="#090d12")
        self.shell.pack(fill=tk.BOTH, expand=True)

        self.sidebar = tk.Frame(self.shell, bg="#111821", width=225)
        self.sidebar.pack(side=tk.LEFT, fill=tk.Y)
        self.sidebar.pack_propagate(False)

        tk.Label(self.sidebar, text="AUTOMATION DIY", bg="#111821", fg="#f2f5f8",
                 font=("Arial", 18, "bold")).pack(pady=(28, 3))
        tk.Label(self.sidebar, text="ENGINE LAB 4.9.1", bg="#111821", fg="#43d9ff",
                 font=("Arial", 9, "bold")).pack(pady=(0, 16))

        self.settings_button = tk.Button(
            self.sidebar, textvariable=self.lang_vars['menu_settings'], command=self.open_settings_overlay,
            anchor="w", bg="#17647c", fg="white", activebackground="#2189a8",
            activeforeground="white", relief=tk.FLAT, bd=0, padx=22, pady=13,
            font=("Arial", 10, "bold"), cursor="hand2"
        )
        self.settings_button.pack(fill=tk.X, padx=10, pady=(0, 8))

        self.sound_notice_button = None
        if not SOUND_AVAILABLE:
            self.sound_notice_button = tk.Button(
                self.sidebar, textvariable=self.lang_vars['sound_silent_sidebar'], command=self.show_sound_help,
                anchor="w", bg="#4f3c18", fg="#ffdd7a", activebackground="#74561e",
                activeforeground="white", relief=tk.FLAT, bd=0, padx=22, pady=9,
                font=("Arial", 9, "bold"), cursor="hand2"
            )
            self.sound_notice_button.pack(fill=tk.X, padx=10, pady=(0, 10))

        nav_items = [
            ("builder", "GARAGE", lambda: self.show_screen("builder")),
            ("dyno", "DYNO & GRAPH", lambda: self.show_screen("dyno")),
            ("throttle", "MANUAL THROTTLE", self.open_throttle_window),
            ("drive", "TEST DRIVE", self.open_drive_window),
            ("track", "TRACK SIMULATION", self.open_track_window),
        ]
        self._nav_texts = {
            "builder": ("GARÁŽ", "GARAGE"),
            "dyno": ("DYNO & GRAF", "DYNO & GRAPH"),
            "throttle": ("RUČNÍ PLYN", "MANUAL THROTTLE"),
            "drive": ("ZKUŠEBNÍ JÍZDA", "TEST DRIVE"),
            "track": ("SIMULACE OKRUHU", "TRACK SIMULATION"),
        }
        for name, text, command in nav_items:
            text = self._ui(*self._nav_texts[name])
            btn = tk.Button(self.sidebar, text=text, command=command, anchor="w",
                            bg="#111821", fg="#c6d1dc", activebackground="#1d2a38",
                            activeforeground="white", disabledforeground="#526273",
                            relief=tk.FLAT, bd=0, padx=24, pady=14,
                            font=("Arial", 10, "bold"), cursor="hand2")
            btn.pack(fill=tk.X, padx=10, pady=3)
            self.nav_buttons[name] = btn

        # Režimy vyžadující platný dyno pull jsou do jeho dokončení zamčené.
        for name in ("throttle", "drive", "track"):
            self.nav_buttons[name].config(state=tk.DISABLED)
        tk.Frame(self.sidebar, bg="#263442", height=1).pack(fill=tk.X, padx=18, pady=20)
        self.fullscreen_hint_button = tk.Button(
            self.sidebar, textvariable=self.lang_vars['ui_fullscreen_hint'], command=self.toggle_fullscreen,
            anchor="w", bg="#111821", fg="#7f93a6", activebackground="#1d2a38",
            activeforeground="white", relief=tk.FLAT, bd=0, padx=24, pady=9
        )
        self.fullscreen_hint_button.pack(fill=tk.X, padx=10)
        self.back_hint_button = tk.Button(
            self.sidebar, textvariable=self.lang_vars['ui_back_hint'], command=self.handle_escape,
            anchor="w", bg="#111821", fg="#7f93a6", activebackground="#1d2a38",
            activeforeground="white", relief=tk.FLAT, bd=0, padx=24, pady=9
        )
        self.back_hint_button.pack(fill=tk.X, padx=10)

        self.main_area = tk.Frame(self.shell, bg="#090d12")
        self.main_area.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.topbar = tk.Frame(self.main_area, bg="#0d141c", height=62)
        self.topbar.pack(fill=tk.X)
        self.topbar.pack_propagate(False)
        self.screen_title = tk.StringVar(value="GARAGE")
        tk.Label(self.topbar, textvariable=self.screen_title, bg="#0d141c", fg="white",
                 font=("Arial", 16, "bold")).pack(side=tk.LEFT, padx=28)

        self.language_host = tk.Frame(self.topbar, bg="#0d141c")
        self.language_host.pack(side=tk.RIGHT, padx=24)
        self.screen_container = tk.Frame(self.main_area, bg="#090d12")
        self.screen_container.pack(fill=tk.BOTH, expand=True)

        self.builder_screen = tk.Frame(self.screen_container, bg="#0b1017")
        self.screens["builder"] = self.builder_screen

    def toggle_fullscreen(self, event=None):
        self.fullscreen = not self.fullscreen
        self.root.attributes("-fullscreen", self.fullscreen)
        if not self.fullscreen:
            try:
                self.root.state("zoomed")
            except tk.TclError:
                self.root.geometry("1400x850")
        return "break"

    def handle_escape(self, event=None):
        if self._settings_overlay is not None and self._settings_overlay.winfo_exists():
            self.close_settings_overlay()
        elif self._message_overlay is not None and self._message_overlay.winfo_exists():
            self._message_overlay.destroy()
            self._message_overlay = None
        elif self.current_screen != "builder":
            self.show_screen("builder")
        elif self.fullscreen:
            self.toggle_fullscreen()
        return "break"

    def _cancel_after(self, attr_name):
        after_id = getattr(self, attr_name, None)
        if after_id is not None:
            try:
                self.root.after_cancel(after_id)
            except tk.TclError:
                pass
            setattr(self, attr_name, None)

    def _stop_dyno_playback(self, discard_incomplete=True):
        self._cancel_after('_dyno_after_id')
        if is_windows:
            try:
                winsound.PlaySound(None, winsound.SND_PURGE)
            except Exception:
                pass
        temp_path = getattr(self, '_dyno_temp_path', None)
        if temp_path:
            try:
                os.remove(temp_path)
            except OSError:
                pass
            self._dyno_temp_path = None
        was_running = self._dyno_running
        self._dyno_running = False
        if was_running and discard_incomplete:
            self.dyno_results = {}
            self.dyno_params = None
            self._reset_dyno_visuals()
            if hasattr(self, 'dyno_status'):
                self.dyno_status.config(text=self.tr("ui_dyno_cancelled"), fg="#ffb454")
            if hasattr(self, 'btn_graph'):
                self.btn_graph.config(state=tk.DISABLED)
            for name in ("throttle", "drive", "track"):
                if name in self.nav_buttons:
                    self.nav_buttons[name].config(state=tk.DISABLED)
        if hasattr(self, 'btn_run'):
            self.btn_run.config(state=tk.NORMAL)
        if hasattr(self, 'builder_run_button'):
            self.builder_run_button.config(state=tk.NORMAL)

    def _cleanup_screen(self, name):
        ToolTip.hide_active()
        if name == "dyno":
            if self._dyno_running:
                self._stop_dyno_playback(discard_incomplete=True)
            return
        if name == "throttle":
            self.throttle_active = False
            self._cancel_after('_throttle_after_id')
            self.stop_audio_stream()
            screen = getattr(self, 'rev_window', None)
            if screen is not None and screen.winfo_exists():
                screen.destroy()
            self.rev_window = None
        elif name == "drive":
            self.drive_running = False
            self.throttle_active = False
            self._cancel_after('_drive_after_id')
            self.stop_audio_stream()
            screen = getattr(self, 'drive_win', None)
            if screen is not None and screen.winfo_exists():
                screen.destroy()
            self.drive_win = None
        elif name == "track":
            self.track_running = False
            self._cancel_after('_track_after_id')
            screen = getattr(self, 'track_win', None)
            if screen is not None and screen.winfo_exists():
                screen.destroy()
            self.track_win = None

    def _activate_screen(self, name):
        screen = self.screens.get(name)
        if screen is None or not screen.winfo_exists():
            return
        for widget in list(self.screen_container.winfo_children()):
            widget.pack_forget()
        screen.pack(fill=tk.BOTH, expand=True)
        self.current_screen = name
        self._refresh_screen_title()
        for key, btn in self.nav_buttons.items():
            active = key == name
            btn.configure(bg="#1b3445" if active else "#111821",
                          fg="#43d9ff" if active else "#c6d1dc")

    def show_screen(self, name):
        ToolTip.hide_active()
        screen = self.screens.get(name)
        if screen is None or not screen.winfo_exists():
            return
        if self.current_screen == name:
            return
        if self._screen_transitioning:
            return
        self._screen_transitioning = True
        try:
            previous = self.current_screen
            if previous is not None:
                self._cleanup_screen(previous)
            self._activate_screen(name)
        finally:
            self._screen_transitioning = False

    def show_error_overlay(self, title, message, **kwargs):
        ToolTip.hide_active()
        if self._message_overlay is not None and self._message_overlay.winfo_exists():
            self._message_overlay.destroy()
        overlay = tk.Frame(self.root, bg="#000000")
        overlay.place(relx=0, rely=0, relwidth=1, relheight=1)
        panel = tk.Frame(overlay, bg="#171d25", highlightbackground="#e65353", highlightthickness=2)
        panel.place(relx=0.5, rely=0.5, anchor=tk.CENTER, width=520, height=250)
        tk.Label(panel, text=str(title), bg="#171d25", fg="#ff6b6b",
                 font=("Arial", 16, "bold")).pack(pady=(28, 12))
        tk.Label(panel, text=str(message), bg="#171d25", fg="white", wraplength=450,
                 justify=tk.CENTER, font=("Arial", 11)).pack(expand=True, padx=25)
        def close():
            if overlay.winfo_exists():
                overlay.destroy()
            self._message_overlay = None
        tk.Button(panel, text="OK", command=close, bg="#29394a", fg="white", relief=tk.FLAT,
                  padx=30, pady=8, font=("Arial", 10, "bold")).pack(pady=(8, 24))
        self._message_overlay = overlay
        overlay.lift()
        return None

    def show_info_overlay(self, title, message, accent="#43d9ff"):
        ToolTip.hide_active()
        if self._message_overlay is not None and self._message_overlay.winfo_exists():
            self._message_overlay.destroy()
        overlay = tk.Frame(self.root, bg="#000000")
        overlay.place(relx=0, rely=0, relwidth=1, relheight=1)
        panel = tk.Frame(overlay, bg="#171d25", highlightbackground=accent, highlightthickness=2)
        panel.place(relx=0.5, rely=0.5, anchor=tk.CENTER, width=620, height=330)
        tk.Label(panel, text=str(title), bg="#171d25", fg=accent,
                 font=("Arial", 16, "bold")).pack(pady=(28, 14))
        tk.Label(panel, text=str(message), bg="#171d25", fg="white", wraplength=540,
                 justify=tk.CENTER, font=("Arial", 11)).pack(expand=True, padx=28)
        def close():
            if overlay.winfo_exists():
                overlay.destroy()
            self._message_overlay = None
        tk.Button(panel, text="OK", command=close, bg="#29394a", fg="white", relief=tk.FLAT,
                  padx=30, pady=8, font=("Arial", 10, "bold")).pack(pady=(10, 24))
        self._message_overlay = overlay
        overlay.lift()

    def show_sound_help(self):
        self.close_settings_overlay()
        detail = self.tr('sound_help_body')
        if SOUND_ERROR:
            detail += f"\n\n{self._ui('Technický detail', 'Technical detail')}: {SOUND_ERROR}"
        self.show_info_overlay(self.tr('sound_help_title'), detail, accent="#ffcc55")

    def shutdown(self):
        if self.current_screen is not None:
            self._cleanup_screen(self.current_screen)
        self._stop_dyno_playback(discard_incomplete=False)
        self.stop_audio_stream()
        if is_windows:
            try:
                winsound.PlaySound(None, winsound.SND_PURGE)
            except Exception:
                pass
        self.root.destroy()

    def _dyno_spec_text(self):
        if self.dyno_params is None:
            return "", ""
        params = self.dyno_params
        name = str(params.get('engine_name', ''))
        disp = math.pi * ((float(params['bore']) / 20.0) ** 2) * (float(params['stroke']) / 10.0) * int(params['cylinders'])
        spec = f"{disp:.0f} cc {params.get('config', '')}{params.get('cylinders', '')}"
        return name, spec

    def _localized_dyno_result(self):
        """Return localized failure strings without changing the authoritative curves."""
        if not self.dyno_results or not self.dyno_results.get('blew_up') or self.dyno_params is None:
            return self.dyno_results
        try:
            localized_params = dict(self.dyno_params)
            localized_params['lang'] = self.vars['app_lang'].get()
            return run_engine_simulation(localized_params)
        except Exception:
            return self.dyno_results

    def _refresh_dyno_console_language(self):
        if not hasattr(self, 'txt_output') or not self.dyno_results or self.dyno_params is None:
            return
        name, spec = self._dyno_spec_text()
        self._dyno_header = f"{self.tr('msg_dyno_hdr')} {name} ({spec}) ---"
        rpm_values = self.dyno_results.get('rpm', [])
        if len(rpm_values) == 0:
            return
        if self._dyno_running:
            index = int(clamp(getattr(self, '_dyno_index', 1) - 1, 0, len(rpm_values) - 1))
        else:
            index = len(rpm_values) - 1
        rpm = int(rpm_values[index])
        trq = float(self.dyno_results['torque'][index])
        hp = float(self.dyno_results['hp'][index])
        self._write_pull(self._dyno_header, rpm, trq, hp)
        if self._dyno_running:
            return
        self._write_log(self.tr('msg_done'))
        if self.dyno_results.get('blew_up'):
            localized = self._localized_dyno_result()
            self._write_log(f"{self.tr('msg_blown')} {localized.get('reason', '')}")
            self._write_log(f"{self.tr('msg_fix')} {localized.get('fix', '')}")
        else:
            max_hp = float(np.max(self.dyno_results['hp']))
            max_hp_rpm = int(self.dyno_results['rpm'][int(np.argmax(self.dyno_results['hp']))])
            max_trq = float(np.max(self.dyno_results['torque']))
            max_trq_rpm = int(self.dyno_results['rpm'][int(np.argmax(self.dyno_results['torque']))])
            self._write_log(f"{self.tr('msg_max_hp')}  {max_hp:.0f} HP @ {max_hp_rpm} RPM")
            self._write_log(f"{self.tr('msg_max_trq')} {max_trq:.0f} Nm @ {max_trq_rpm} RPM")
            self._write_log(self.tr('msg_ready'))

    def _refresh_localized_screen_texts(self):
        """Refresh text that is stateful and therefore cannot use one fixed StringVar."""
        ToolTip.hide_active()

        if hasattr(self, 'dyno_ax_torque'):
            self.dyno_ax_torque.set_ylabel(f"{self.tr('msg_trq')} (Nm)", color='#43d9ff')
            self.dyno_ax_hp.set_ylabel(f"{self.tr('msg_hp')} (HP)", color='#ff6b6b')
            self.dyno_torque_line.set_label(self.tr('msg_trq'))
            self.dyno_hp_line.set_label(self.tr('msg_hp'))
            self.graph_canvas.draw_idle()
        if hasattr(self, 'dyno_engine_title'):
            if self.dyno_params is None:
                self.dyno_engine_title.config(text=self.tr('ui_dyno_ready'))
            else:
                name, spec = self._dyno_spec_text()
                self.dyno_engine_title.config(
                    text=f"{name}   •   {spec}   •   {self.dyno_params.get('aspiration', '')}"
                )
        if hasattr(self, 'dyno_status'):
            if self._dyno_running:
                self.dyno_status.config(text=self.tr('ui_dyno_running'), fg='#ffcc55')
            elif self.dyno_results:
                if self.dyno_results.get('blew_up'):
                    self.dyno_status.config(text=self.tr('msg_blown'), fg='#ff5f5f')
                else:
                    max_hp = float(np.max(self.dyno_results['hp']))
                    max_hp_rpm = int(self.dyno_results['rpm'][int(np.argmax(self.dyno_results['hp']))])
                    max_trq = float(np.max(self.dyno_results['torque']))
                    max_trq_rpm = int(self.dyno_results['rpm'][int(np.argmax(self.dyno_results['torque']))])
                    self.dyno_status.config(
                        text=(f"{self.tr('msg_max_hp')} {max_hp:.0f} HP @ {max_hp_rpm} RPM\n"
                              f"{self.tr('msg_max_trq')} {max_trq:.0f} Nm @ {max_trq_rpm} RPM"),
                        fg='#63f28a'
                    )
            else:
                self.dyno_status.config(text=self.tr('ui_ready'), fg='#8fa5b7')
        self._refresh_dyno_console_language()

        rev = getattr(self, 'rev_window', None)
        if rev is not None and rev.winfo_exists() and hasattr(self, 'lbl_temp'):
            if getattr(self, 'engine_blown', False):
                self.lbl_temp.config(text=self.tr('msg_hg_blown'), fg='#ff5f5f')
            else:
                self.lbl_temp.config(
                    text=f"{self.tr('lbl_coolant')} {int(getattr(self, 'coolant_temp', 90.0))}°C",
                    fg='#ff5f5f' if getattr(self, 'coolant_temp', 90.0) > 115.0 else '#8fa5b7'
                )

        drive = getattr(self, 'drive_win', None)
        if drive is not None and drive.winfo_exists():
            if hasattr(self, 'drive_skip_text'):
                self.drive_skip_text.set(self.tr('btn_skip'))
            if hasattr(self, 'drive_launch_text'):
                if getattr(self, 'drive_running', False):
                    self.drive_launch_text.set(self.tr('btn_accel'))
                elif getattr(self, 'max_achieved_speed', 0.0) > 0.0:
                    self.drive_launch_text.set(self.tr('btn_retry'))
                else:
                    self.drive_launch_text.set(self.tr('btn_launch'))
            if hasattr(self, 'lbl_tcs'):
                if getattr(self, 'max_achieved_speed', 0.0) > 0.0 and not getattr(self, 'drive_running', False):
                    self.lbl_tcs.config(
                        text=f"{self.tr('ui_max')}: {self._speed_from_mps(self.max_achieved_speed):.0f} {self._speed_unit_label()}",
                        fg='black', bg='lime'
                    )
                elif getattr(self, 'drive_running', False):
                    if getattr(self, 'slip_active', False):
                        self.lbl_tcs.config(text=self.tr('ui_slip'), fg='black', bg='orange')
                    else:
                        self.lbl_tcs.config(text=self.tr('ui_tcs_ok'), fg='gray', bg='#222222')
                else:
                    self.lbl_tcs.config(text=self.tr('ui_tcs_ready'), fg='#8fa5b7', bg='#1b2631')

        track = getattr(self, 'track_win', None)
        if track is not None and track.winfo_exists():
            result = getattr(self, 'track_result', None)
            running = getattr(self, 'track_running', False)
            if hasattr(self, 'track_button_text'):
                self.track_button_text.set(self.tr('btn_track_start' if running or result is None else 'btn_track_retry'))
            shown_time = 0.0
            speed_mps = 0.0
            gear_text = 'N'
            sector = 1
            if result is not None:
                shown_time = min(getattr(self, 'track_sim_elapsed', 0.0), result['lap_time'])
                cumulative = result['cumulative_time']
                idx = int(np.searchsorted(cumulative, shown_time, side='right') - 1)
                idx = int(clamp(idx, 0, len(cumulative) - 2))
                speed_mps = float(result['speed_profile'][idx])
                gear_text = str(int(result['gear_profile'][idx]) + 1)
                sector = int(result['sector_profile'][idx])
            self.lbl_track_live_speed.config(
                text=f"{self.tr('lbl_track_speed')}: {self._speed_from_mps(speed_mps):.0f} {self._speed_unit_label()}"
            )
            self.lbl_track_live_gear.config(text=f"{self.tr('lbl_track_gear')}: {gear_text}")
            self.lbl_track_live_sector.config(text=f"{self.tr('lbl_track_sector')}: {sector}")
            self.lbl_track_lap.config(text=f"{self.tr('lbl_lap_time')}: {self._format_lap_time(shown_time) if result is not None else '--:--.---'}")
            if running:
                self.lbl_track_status.config(text=self.tr('msg_track_running'), fg='#ffcc55')
            elif result is not None:
                self.lbl_track_status.config(text=self.tr('msg_track_finished'), fg='lime')
                sectors = result['sector_times']
                self.lbl_track_stats.config(
                    text=(f"{self.tr('lbl_track_length')}: {result['track_length'] / 1000.0:.3f} km\n"
                          f"{self.tr('lbl_track_avg')}: {self._speed_from_mps(result['average_speed']):.1f} {self._speed_unit_label()}\n"
                          f"{self.tr('lbl_track_max')}: {self._speed_from_mps(result['max_speed']):.1f} {self._speed_unit_label()}")
                )
                self.lbl_track_sectors.config(
                    text=f"S1: {sectors[0]:.3f} s\nS2: {sectors[1]:.3f} s\nS3: {sectors[2]:.3f} s"
                )
            else:
                self.lbl_track_status.config(text=self.tr('msg_track_ready'), fg='#8fa5b7')
                self.lbl_track_stats.config(text=f"{self.tr('lbl_track_length')}: 3.605 km")
                self.lbl_track_sectors.config(text='S1: --.-- s\nS2: --.-- s\nS3: --.-- s')
            self._schedule_track_redraw()

        self._refresh_speed_displays()

    def apply_language(self):
        lang = self.vars['app_lang'].get()
        for k, v in T[lang].items():
            if k in self.lang_vars:
                self.lang_vars[k].set(v)
        
        self.root.title(self.lang_vars['app_title'].get())
        for name, button in self.nav_buttons.items():
            if name in self._nav_texts:
                button.configure(text=self._ui(*self._nav_texts[name]))

        if hasattr(self, "builder_run_button"):
            self.builder_run_button.configure(
                text=self._ui("SPUSTIT DYNO", "RUN DYNO")
            )

        self._refresh_screen_title()
        self.update_settings_summary()

        for i, tab_key in enumerate(['tab_1', 'tab_2', 'tab_3', 'tab_4', 'tab_5', 'tab_6', 'tab_7']):
            self.notebook.tab(i, text=self.tr(tab_key))
        self._refresh_localized_screen_texts()
        if self._settings_overlay is not None and self._settings_overlay.winfo_exists():
            self.close_settings_overlay()
            self.root.after_idle(self.open_settings_overlay)

    def setup_master_presets(self):
        self.master_presets = {
            "Mazda 6 (LF-DE 2.0)": {
                'config': "Inline", 'cylinders': 4, 'v_angle': 90, 'block_mat': "Aluminium",
                'bore': 87.5, 'stroke': 83.1, 'radiator': 50,
                'crank': "Cast", 'conrods': "Heavy Duty", 'pistons': "Cast", 'balancer': "None",
                'head_mat': "Aluminium", 'valvetrain': "DOHC", 'valves': 4, 'vvt': "None", 'vvl': False, 'cam_profile': 55, 'comp_ratio': 10.0,
                'aspiration': "NA", 'turbo_bearing': "Journal", 'turbo_config': "Single", 'intercooler': 50, 'turb_size': 50, 'boost': 0.5, 'sc_type': "Roots", 'comp_size': 50, 'sc_pulley': 0.8,
                'fuel_deliv': "EFI Multi", 'intake_conf': "Single", 'manifold': "Standard", 'fuel_type': "Premium 95", 'afr': 14.7, 'ignition': 25, 'rpm_limit': 6500,
                'exh_arch': "Single", 'headers': "Cast", 'exh_diam': 44.0, 'cat': "3-way", 'muffler1': "Baffled", 'muffler2': "Baffled",
                'veh_preset': "Mazda 6 (2002)", 'veh_weight': 1350.0, 'veh_cd': 0.30, 'veh_area': 2.20, 'wheel_radius': 0.315, 'speed_limiter': 0.0, 'downforce_cla': 0.0, 'tire_grip': 0.9, 'gears': 5, 'final_drive': 4.3, 'drivetrain': "FWD",
                'tech_level': 98
            },
            "Škoda Octavia 1.9 TDI": {
                'config': "Inline", 'cylinders': 4, 'v_angle': 90, 'block_mat': "Cast Iron",
                'bore': 79.5, 'stroke': 95.5, 'radiator': 40,
                'crank': "Forged", 'conrods': "Heavy Duty", 'pistons': "Heavy Duty", 'balancer': "None",
                'head_mat': "Aluminium", 'valvetrain': "SOHC", 'valves': 2, 'vvt': "None", 'vvl': False, 'cam_profile': 0, 'comp_ratio': 17.0,
                'aspiration': "Turbo", 'turbo_bearing': "Journal", 'turbo_config': "Single", 'intercooler': 30, 'turb_size': 20, 'boost': 0.8, 'sc_type': "Roots", 'comp_size': 50, 'sc_pulley': 0.8,
                'fuel_deliv': "Direct Injection", 'intake_conf': "Single", 'manifold': "Standard", 'fuel_type': "Diesel", 'afr': 17.0, 'ignition': 15, 'rpm_limit': 4500,
                'exh_arch': "Single", 'headers': "Cast", 'exh_diam': 45.0, 'cat': "3-way", 'muffler1': "Baffled", 'muffler2': "Baffled",
                'veh_preset': "Vlastní (Custom)", 'veh_weight': 1350.0, 'veh_cd': 0.31, 'veh_area': 2.15, 'wheel_radius': 0.305, 'speed_limiter': 0.0, 'downforce_cla': 0.0, 'tire_grip': 0.8, 'gears': 5, 'final_drive': 3.1, 'drivetrain': "FWD",
                'tech_level': 82
            },
            "BMW M3 E46 (S54B32)": {
                'config': "Inline", 'cylinders': 6, 'v_angle': 90, 'block_mat': "Cast Iron",
                'bore': 87.0, 'stroke': 91.0, 'radiator': 70,
                'crank': "Forged", 'conrods': "Forged", 'pistons': "Forged", 'balancer': "Harmonic Damper",
                'head_mat': "Aluminium", 'valvetrain': "DOHC", 'valves': 4, 'vvt': "All", 'vvl': False, 'cam_profile': 75, 'comp_ratio': 11.5,
                'aspiration': "NA", 'turbo_bearing': "Journal", 'turbo_config': "Single", 'intercooler': 50, 'turb_size': 50, 'boost': 0.5, 'sc_type': "Roots", 'comp_size': 50, 'sc_pulley': 0.8,
                'fuel_deliv': "EFI Multi", 'intake_conf': "ITB", 'manifold': "Performance", 'fuel_type': "Ultimate 100", 'afr': 13.5, 'ignition': 60, 'rpm_limit': 8000,
                'exh_arch': "Dual", 'headers': "Tubular", 'exh_diam': 60.0, 'cat': "High Flow", 'muffler1': "Straight", 'muffler2': "Baffled",
                'veh_preset': "Lehký sporťák", 'veh_weight': 1495.0, 'veh_cd': 0.32, 'veh_area': 2.00, 'wheel_radius': 0.325, 'speed_limiter': 250.0, 'downforce_cla': 0.0, 'tire_grip': 1.1, 'gears': 6, 'final_drive': 3.62, 'drivetrain': "RWD",
                'tech_level': 100
            },
            "Audi RS6 C7 (4.0 TFSI)": {
                'config': "V", 'cylinders': 8, 'v_angle': 90, 'block_mat': "Aluminium",
                'bore': 84.5, 'stroke': 89.0, 'radiator': 90,
                'crank': "Flat-plane", 'conrods': "Forged", 'pistons': "Forged", 'balancer': "Harmonic Damper",
                'head_mat': "Aluminium", 'valvetrain': "DOHC", 'valves': 4, 'vvt': "All", 'vvl': False, 'cam_profile': 30, 'comp_ratio': 8.8,
                'aspiration': "Turbo", 'turbo_bearing': "Ball Bearings", 'turbo_config': "Twin", 'intercooler': 70, 'turb_size': 40, 'boost': 0.58, 'sc_type': "Roots", 'comp_size': 50, 'sc_pulley': 0.8,
                'fuel_deliv': "Direct Injection", 'intake_conf': "Twin", 'manifold': "Performance", 'fuel_type': "Ultimate 100", 'afr': 14.5, 'ignition': 35, 'rpm_limit': 6800,
                'exh_arch': "Dual", 'headers': "Tubular", 'exh_diam': 65.0, 'cat': "High Flow", 'muffler1': "Straight", 'muffler2': "Straight",
                'veh_preset': "Vlastní (Custom)", 'veh_weight': 1950.0, 'veh_cd': 0.35, 'veh_area': 2.36, 'wheel_radius': 0.350, 'speed_limiter': 250.0, 'downforce_cla': 0.0, 'tire_grip': 1.2, 'gears': 7, 'final_drive': 3.2, 'drivetrain': "AWD",
                'tech_level': 98
            },
            "Mercedes-Benz C63 AMG (M156)": {
                'config': "V", 'cylinders': 8, 'v_angle': 90, 'block_mat': "Aluminium",
                'bore': 102.2, 'stroke': 94.6, 'radiator': 85,
                'crank': "Forged", 'conrods': "Forged", 'pistons': "Forged", 'balancer': "Harmonic Damper",
                'head_mat': "Aluminium", 'valvetrain': "DOHC", 'valves': 4, 'vvt': "All", 'vvl': False, 'cam_profile': 45, 'comp_ratio': 11.3,
                'aspiration': "NA", 'turbo_bearing': "Journal", 'turbo_config': "Single", 'intercooler': 50, 'turb_size': 50, 'boost': 0.5, 'sc_type': "Roots", 'comp_size': 50, 'sc_pulley': 0.8,
                'fuel_deliv': "EFI Multi", 'intake_conf': "Twin", 'manifold': "Standard", 'fuel_type': "Premium 95", 'afr': 13.0, 'ignition': 30, 'rpm_limit': 7200,
                'exh_arch': "Dual", 'headers': "Cast", 'exh_diam': 65.0, 'cat': "High Flow", 'muffler1': "Straight", 'muffler2': "Straight",
                'veh_preset': "Vlastní (Custom)", 'veh_weight': 1730.0, 'veh_cd': 0.32, 'veh_area': 2.20, 'wheel_radius': 0.335, 'speed_limiter': 250.0, 'downforce_cla': 0.0, 'tire_grip': 1.0, 'gears': 7, 'final_drive': 3.06, 'drivetrain': "RWD",
                'tech_level': 88
            },
            "Bugatti Veyron 16.4 Super Sport": {
                'config': "V", 'cylinders': 16, 'v_angle': 90, 'block_mat': "Aluminium",
                'bore': 86.0, 'stroke': 86.0, 'radiator': 100,
                'crank': "Billet", 'conrods': "Titanium", 'pistons': "Forged", 'balancer': "Full Balancers",
                'head_mat': "Aluminium", 'valvetrain': "DOHC", 'valves': 4, 'vvt': "All", 'vvl': False, 'cam_profile': 25, 'comp_ratio': 9.0,
                'aspiration': "Turbo", 'turbo_bearing': "Ball Bearings", 'turbo_config': "Quad", 'intercooler': 100, 'turb_size': 50, 'boost': 0.67, 'sc_type': "Roots", 'comp_size': 50, 'sc_pulley': 0.8,
                'fuel_deliv': "EFI Multi", 'intake_conf': "Twin", 'manifold': "Performance", 'fuel_type': "Ultimate 100", 'afr': 12.0, 'ignition': 55, 'rpm_limit': 6500,
                'exh_arch': "Dual", 'headers': "Tubular", 'exh_diam': 90.0, 'cat': "High Flow", 'muffler1': "None", 'muffler2': "Straight",
                'veh_preset': "Moderní Supersport", 'veh_weight': 1888.0, 'veh_cd': 0.36, 'veh_area': 2.07, 'wheel_radius': 0.365, 'speed_limiter': 415.0, 'downforce_cla': 0.10, 'tire_grip': 1.5, 'gears': 7, 'final_drive': 3.8, 'drivetrain': "AWD",
                'tech_level': 100
            }
        }

    def apply_master_preset(self, event=None):
        name = self.vars['engine_name'].get()
        if name in self.master_presets:
            p = self.master_presets[name]
            # Reset VŠECHNY parametry na tovární výchozí hodnoty jako první krok.
            # Díky tomu i nový slider, který zapomeneme doplnit do některého presetu,
            # spadne na rozumný default místo toho, aby "přežil" z předešlého vozidla.
            for k, default_v in self.factory_defaults.items():
                self._set_var(k, default_v)
            if 'veh_preset' in p:
                self.vars['veh_preset'].set(p['veh_preset'])
            for k, v in p.items():
                if k in self.vars and k != 'veh_preset':
                    if k == 'vvl' and isinstance(v, bool):
                        self.vars[k].set("VVL" if v else "None")
                    else:
                        self._set_var(k, v)
            self.update_displacement()
            self.update_dynamic_ui()

    def _set_var(self, k, v):
        if isinstance(self.vars[k], tk.BooleanVar):
            if not isinstance(v, bool):
                raise TypeError(f"{k} must be a JSON boolean")
            self.vars[k].set(v)
        elif isinstance(self.vars[k], tk.DoubleVar): self.vars[k].set(float(v))
        elif isinstance(self.vars[k], tk.IntVar): self.vars[k].set(int(v))
        else: self.vars[k].set(str(v))

    def snapshot_factory_defaults(self):
        # Uloží startovní hodnotu KAŽDÉHO slideru/comboboxu hned po vytvoření
        # proměnných - tj. dřív, než se do nich sáhne presetem nebo uloženým motorem.
        self.factory_defaults = {
            k: v.get() for k, v in self.vars.items()
            if k not in ['calc_disp', 'app_lang', 'engine_name']
        }

    def create_variables(self):
        self.vars['engine_name'] = tk.StringVar(value="Mazda 6 (LF-DE 2.0)")
        self.vars['config'] = tk.StringVar(value="Inline")
        self.vars['cylinders'] = tk.IntVar(value=4)
        self.vars['v_angle'] = tk.IntVar(value=90)
        self.vars['block_mat'] = tk.StringVar(value="Aluminium")
        self.vars['bore'] = tk.DoubleVar(value=87.5)  
        self.vars['stroke'] = tk.DoubleVar(value=83.1) 
        self.vars['radiator'] = tk.IntVar(value=50) 
        self.vars['tech_level'] = tk.IntVar(value=98)
        self.vars['calc_disp'] = tk.StringVar(value="0 cc") 
        
        self.vars['crank'] = tk.StringVar(value="Cast")
        self.vars['conrods'] = tk.StringVar(value="Heavy Duty")
        self.vars['pistons'] = tk.StringVar(value="Cast")
        self.vars['balancer'] = tk.StringVar(value="None")
        self.vars['balancer_mass'] = tk.DoubleVar(value=0.0)
        
        self.vars['head_mat'] = tk.StringVar(value="Aluminium")
        self.vars['valvetrain'] = tk.StringVar(value="DOHC")
        self.vars['valves'] = tk.IntVar(value=4)
        self.vars['vvt'] = tk.StringVar(value="None")
        self.vars['vvl'] = tk.StringVar(value="None")
        self.vars['vvl_prof'] = tk.IntVar(value=60)
        self.vars['vvl_rpm'] = tk.IntVar(value=4000)
        self.vars['springs'] = tk.IntVar(value=50)
        self.vars['cam_profile'] = tk.IntVar(value=55)
        self.vars['comp_ratio'] = tk.DoubleVar(value=10.0)
        
        self.vars['aspiration'] = tk.StringVar(value="NA")
        self.vars['turbo_bearing'] = tk.StringVar(value="Journal")
        self.vars['turbo_config'] = tk.StringVar(value="Single")
        self.vars['intercooler'] = tk.IntVar(value=50)
        self.vars['turb_size'] = tk.IntVar(value=50)
        self.vars['boost'] = tk.DoubleVar(value=0.5)
        self.vars['sc_type'] = tk.StringVar(value="Roots")
        self.vars['comp_size'] = tk.IntVar(value=50)
        self.vars['sc_pulley'] = tk.DoubleVar(value=0.8)
        
        self.vars['fuel_deliv'] = tk.StringVar(value="EFI Multi")
        self.vars['carb_size'] = tk.IntVar(value=50)
        self.vars['intake_conf'] = tk.StringVar(value="Single")
        self.vars['manifold'] = tk.StringVar(value="Standard")
        self.vars['man_size'] = tk.IntVar(value=50)
        self.vars['fuel_type'] = tk.StringVar(value="Premium 95")
        self.vars['fuel_map'] = tk.IntVar(value=50)
        self.vars['afr'] = tk.DoubleVar(value=14.7)
        self.vars['ignition'] = tk.IntVar(value=25)
        self.vars['rpm_limit'] = tk.IntVar(value=6500)
        
        self.vars['headers'] = tk.StringVar(value="Cast")
        self.vars['head_size'] = tk.IntVar(value=50)
        self.vars['exh_arch'] = tk.StringVar(value="Single")
        self.vars['exh_diam'] = tk.DoubleVar(value=44.0)
        self.vars['bypass'] = tk.StringVar(value="No Valves")
        self.vars['cat'] = tk.StringVar(value="3-way")
        self.vars['muffler1'] = tk.StringVar(value="Baffled")
        self.vars['muffler2'] = tk.StringVar(value="Baffled")
        
        self.vars['veh_preset'] = tk.StringVar(value="Mazda 6 (2002)")
        self.vars['veh_weight'] = tk.DoubleVar(value=1350.0)
        self.vars['veh_cd'] = tk.DoubleVar(value=0.30)
        self.vars['veh_area'] = tk.DoubleVar(value=2.20)
        self.vars['wheel_radius'] = tk.DoubleVar(value=0.315)
        self.vars['speed_limiter'] = tk.DoubleVar(value=0.0)  # canonical storage: km/h
        self.speed_unit = tk.StringVar(value='kmh')
        self.speed_unit_text = tk.StringVar(value='km/h')
        self.speed_limiter_display = tk.DoubleVar(value=0.0)
        self._speed_limiter_syncing = False
        self.vars['speed_limiter'].trace_add('write', self._sync_speed_limiter_display_from_canonical)
        self.speed_limiter_display.trace_add('write', self._sync_speed_limiter_canonical_from_display)
        self.vars['downforce_cla'] = tk.DoubleVar(value=0.0)
        self.vars['tire_grip'] = tk.DoubleVar(value=0.9)
        self.vars['gears'] = tk.IntVar(value=5)
        self.vars['final_drive'] = tk.DoubleVar(value=4.3)
        self.vars['drivetrain'] = tk.StringVar(value="FWD")
        self.vars['custom_gears'] = tk.BooleanVar(value=False)
        default_custom_ratios = [3.3, 1.9, 1.3, 1.0, 0.8, 0.65, 0.55, 0.45]
        for index, ratio in enumerate(default_custom_ratios, start=1):
            self.vars[f'gear_{index}'] = tk.DoubleVar(value=ratio)

    def create_menu(self):
        """Native menu bar is replaced by a visible in-game settings panel."""
        self.menubar = None
        self.filemenu = None
        try:
            self.root.configure(menu="")
        except tk.TclError:
            pass

    def create_language_selector(self):
        # Language and speed-unit selectors live in Settings. The top bar only
        # shows the active choices and opens the same panel.
        self.settings_summary_var = tk.StringVar()
        self.settings_summary_button = tk.Button(
            self.language_host, textvariable=self.settings_summary_var,
            command=self.open_settings_overlay, bg="#172330", fg="#d7e0e8",
            activebackground="#223447", activeforeground="white", relief=tk.FLAT,
            bd=0, padx=15, pady=8, font=("Arial", 9, "bold"), cursor="hand2"
        )
        self.settings_summary_button.pack()
        self.update_settings_summary()

    def save_engine(self):
        file_path = filedialog.asksaveasfilename(
            defaultextension=".json",
            filetypes=[("JSON files", "*.json")],
            initialfile=f"{self.vars['engine_name'].get()}.json"
        )
        if not file_path:
            return
        try:
            data = {k: v.get() for k, v in self.vars.items() if k not in ['calc_disp', 'app_lang']}
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=4, ensure_ascii=False)
        except (OSError, TypeError, tk.TclError) as exc:
            messagebox.showerror(self.tr('msg_file_error'), str(exc))

    def load_engine(self):
        file_path = filedialog.askopenfilename(filetypes=[("JSON files", "*.json")])
        if not file_path:
            return
        backup = {k: v.get() for k, v in self.vars.items() if k != 'calc_disp'}
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            if not isinstance(data, dict):
                raise ValueError("JSON root must be an object")

            self._suspend_vehicle_preset_callback = True
            try:
                for k, default_v in self.factory_defaults.items():
                    self._set_var(k, default_v)
                if 'veh_preset' in data:
                    self._set_var('veh_preset', data['veh_preset'])
                    self.apply_vehicle_preset_values(self.vars['veh_preset'].get())
                for k, value in data.items():
                    if k not in self.vars or k in ('calc_disp', 'app_lang', 'veh_preset'):
                        continue
                    if k == 'vvl' and isinstance(value, bool):
                        self.vars[k].set("VVL" if value else "None")
                    else:
                        self._set_var(k, value)
            finally:
                self._suspend_vehicle_preset_callback = False
            self.collect_parameters()  # validace typů, rozsahů a povolených voleb
            self.update_dynamic_ui()
            self.update_displacement()
        except (OSError, ValueError, TypeError, json.JSONDecodeError, tk.TclError) as exc:
            self._suspend_vehicle_preset_callback = True
            try:
                for k, value in backup.items():
                    if k in self.vars:
                        self._set_var(k, value)
            finally:
                self._suspend_vehicle_preset_callback = False
            self.update_dynamic_ui()
            self.update_displacement()
            messagebox.showerror(self.tr('msg_file_error'), str(exc))

    def create_widgets(self):
        top_frame = tk.Frame(self.builder_screen, bg="#0f1720", padx=28, pady=20)
        top_frame.pack(fill=tk.X, padx=28, pady=(24, 4))
        tk.Label(top_frame, textvariable=self.lang_vars["lbl_engine_name"], bg="#0f1720", fg="#dce6ee",
                 font=("Arial", 11, "bold")).pack(side=tk.LEFT, padx=(0, 14))

        self.cb_engine_name = ttk.Combobox(top_frame, textvariable=self.vars['engine_name'],
                                           font=("Arial", 11), state="normal")
        self.cb_engine_name['values'] = list(self.master_presets.keys())
        self.cb_engine_name.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 18))
        self.cb_engine_name.bind("<<ComboboxSelected>>", self.apply_master_preset)
        self.builder_run_button = tk.Button(
            top_frame, text=self._ui("SPUSTIT DYNO", "RUN DYNO"), command=self.start_dyno,
            bg="#18a8c9", fg="#071015", activebackground="#3bd4f4", activeforeground="#071015",
            relief=tk.FLAT, bd=0, padx=24, pady=10, font=("Arial", 11, "bold"), cursor="hand2"
        )
        self.builder_run_button.pack(side=tk.RIGHT)

        self.notebook = ttk.Notebook(self.builder_screen)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=28, pady=(12, 28))
        self.scrollable_tabs = []

        def configure_parent(parent):
            parent.grid_columnconfigure(0, weight=1, minsize=220)
            parent.grid_columnconfigure(1, weight=5, minsize=320)
            parent.grid_columnconfigure(2, weight=0, minsize=100)
            parent.grid_columnconfigure(3, weight=1, minsize=75)

        def prepare_tab(tab, row_count):
            configure_parent(tab)
            row_minimum = 38 if row_count >= 11 else 48
            for row in range(row_count):
                tab.grid_rowconfigure(row, weight=1, minsize=row_minimum)

        def create_scrollable_tab(tab_key, row_count):
            wrapper = AutoScrollFrame(self.notebook, background="#101720")
            tab = wrapper.content
            prepare_tab(tab, row_count)
            self.notebook.add(wrapper, text=self.tr(tab_key))
            self.scrollable_tabs.append(wrapper)
            return tab

        def refresh_active_scroll_tab(event=None):
            try:
                selected = self.notebook.index(self.notebook.select())
                wrapper = self.scrollable_tabs[selected]
            except (tk.TclError, IndexError, ValueError):
                return
            wrapper.scroll_to_top()
            wrapper._schedule_refresh()

        self.notebook.bind("<<NotebookTabChanged>>", refresh_active_scroll_tab, add="+")

        def make_combo(parent, r, lbl_key, var_name, options, tt_key):
            self.allowed_values[var_name] = tuple(options)
            configure_parent(parent)
            lbl = ttk.Label(parent, textvariable=self.lang_vars[lbl_key], font=("Arial", 11, "bold"))
            lbl.grid(row=r, column=0, sticky=tk.W, pady=9, padx=(24, 16))
            cb = ttk.Combobox(parent, textvariable=self.vars[var_name], values=options,
                              state="readonly", font=("Arial", 11))
            cb.grid(row=r, column=1, columnspan=3, sticky=tk.EW, pady=9, padx=(8, 28))
            ToolTip(lbl, self.lang_vars[tt_key]); ToolTip(cb, self.lang_vars[tt_key])
            return lbl, cb

        def make_slider(parent, r, lbl_key, var_name, f_, t_, res, unit, tt_key):
            configure_parent(parent)
            lbl = ttk.Label(parent, textvariable=self.lang_vars[lbl_key], font=("Arial", 11, "bold"))
            lbl.grid(row=r, column=0, sticky=tk.W, pady=9, padx=(24, 16))

            if var_name == 'speed_limiter':
                def snap_speed_limiter(raw_value):
                    try:
                        raw = float(raw_value)
                    except (TypeError, ValueError):
                        return
                    step = 5.0
                    maximum = self._speed_limiter_display_max()
                    snapped = clamp(round(raw / step) * step, 0.0, maximum)
                    self.speed_limiter_display.set(round(snapped, 1))

                self.speed_limiter_scale = ttk.Scale(
                    parent, variable=self.speed_limiter_display, from_=0.0,
                    to=self._speed_limiter_display_max(), orient=tk.HORIZONTAL,
                    command=snap_speed_limiter
                )
                self.speed_limiter_scale.grid(row=r, column=1, sticky=tk.EW, pady=9, padx=(8, 18))
                entry = ttk.Entry(parent, textvariable=self.speed_limiter_display, width=10,
                                  justify=tk.CENTER, font=("Arial", 11))
                entry.grid(row=r, column=2, sticky=tk.EW, padx=(0, 8))
                self.speed_limiter_unit_label = ttk.Label(
                    parent, textvariable=self.speed_unit_text, font=("Arial", 10)
                )
                self.speed_limiter_unit_label.grid(row=r, column=3, sticky=tk.W, padx=(0, 24))
                self._sync_speed_limiter_display_from_canonical()
                ToolTip(lbl, self.lang_vars[tt_key])
                ToolTip(self.speed_limiter_scale, self.lang_vars[tt_key])
                ToolTip(entry, self.lang_vars[tt_key])
                return self.speed_limiter_scale

            decimals = max(0, len(str(res).split('.')[1].rstrip('0'))) if '.' in str(res) else 0
            def snap_scale(raw_value):
                raw = float(raw_value)
                snapped = f_ + round((raw - f_) / res) * res
                snapped = clamp(snapped, f_, t_)
                var = self.vars[var_name]
                if isinstance(var, tk.IntVar):
                    var.set(int(round(snapped)))
                else:
                    var.set(round(snapped, decimals))

            scale = ttk.Scale(parent, variable=self.vars[var_name], from_=f_, to=t_,
                              orient=tk.HORIZONTAL, command=snap_scale)
            scale.grid(row=r, column=1, sticky=tk.EW, pady=9, padx=(8, 18))
            entry = ttk.Entry(parent, textvariable=self.vars[var_name], width=10, justify=tk.CENTER,
                              font=("Arial", 11))
            entry.grid(row=r, column=2, sticky=tk.EW, padx=(0, 8))
            unit_lbl = ttk.Label(parent, text=unit, font=("Arial", 10))
            unit_lbl.grid(row=r, column=3, sticky=tk.W, padx=(0, 24))

            def update_lbl(*args):
                try:
                    float(self.vars[var_name].get())
                    if var_name in ['bore', 'stroke', 'cylinders']:
                        self.update_displacement()
                except (ValueError, TypeError, tk.TclError):
                    pass
            self.vars[var_name].trace_add("write", update_lbl)
            update_lbl()
            ToolTip(lbl, self.lang_vars[tt_key]); ToolTip(scale, self.lang_vars[tt_key]); ToolTip(entry, self.lang_vars[tt_key])
            return scale

        # TAB 1 - Block
        tab1 = create_scrollable_tab("tab_1", 9)
        make_combo(tab1, 0, "lbl_config", 'config', ["Inline", "V", "Boxer"], "tt_config")
        self.frame_v = ttk.Frame(tab1); self.frame_v.grid(row=1, column=0, columnspan=4, sticky=tk.EW)
        make_combo(self.frame_v, 0, "lbl_vangle", 'v_angle', [60, 90, 120], "tt_vangle")
        make_combo(tab1, 2, "lbl_cyl", 'cylinders', [3, 4, 5, 6, 8, 10, 12, 16], "tt_cyl")
        make_combo(tab1, 3, "lbl_block", 'block_mat', ["Cast Iron", "Aluminium", "Aluminium Heavy", "Aluminium Light", "AlSi", "AlSi Heavy", "AlSi Light", "Aluminium Billet", "Magnesium"], "tt_block")
        make_slider(tab1, 4, "lbl_bore", 'bore', 50.0, 120.0, 0.1, "mm", "tt_bore")
        make_slider(tab1, 5, "lbl_stroke", 'stroke', 50.0, 120.0, 0.1, "mm", "tt_stroke")
        make_slider(tab1, 6, "lbl_rad", 'radiator', 10, 100, 1, "%", "tt_rad")
        make_slider(tab1, 7, "lbl_tech", 'tech_level', 50, 150, 1, "", "tt_tech")
        ttk.Label(tab1, textvariable=self.lang_vars['lbl_calc_disp'], font=("Arial", 11, "bold")).grid(row=8, column=0, pady=12, padx=(24, 16), sticky=tk.W)
        ttk.Label(tab1, textvariable=self.vars['calc_disp'], font=("Arial", 15, "bold"), foreground="#43d9ff").grid(row=8, column=1, sticky=tk.W, padx=8)

        # TAB 2 - Bottom End
        tab2 = create_scrollable_tab("tab_2", 5)
        make_combo(tab2, 0, "lbl_crank", 'crank', ["Cast", "Cast Iron Heavy", "Forged", "Forged Steel Heavy", "Forged Steel Light", "Billet", "Billet Steel Heavy", "Flat-plane"], "tt_crank")
        make_combo(tab2, 1, "lbl_conrods", 'conrods', ["Cast", "Cast Heavy", "Cast Light", "Heavy Duty", "Forged", "Forged Heavy", "Forged Light", "LW Forged", "Titanium"], "tt_conrods")
        make_combo(tab2, 2, "lbl_pistons", 'pistons', ["Cast", "Cast Heavy", "Cast Light", "Heavy Duty", "Forged", "Forged Heavy", "Forged Light", "LW Forged", "Hypereutectic Cast", "Low Friction"], "tt_pistons")
        make_combo(tab2, 3, "lbl_bal", 'balancer', ["None", "Harmonic Damper", "Full Balancers"], "tt_bal")
        self.frame_bal_mass = ttk.Frame(tab2); self.frame_bal_mass.grid(row=4, column=0, columnspan=4, sticky=tk.EW)
        make_slider(self.frame_bal_mass, 0, "lbl_bal_mass", 'balancer_mass', 0.0, 50.0, 0.1, "kg", "tt_bal_mass")

        # TAB 3 - Top End
        tab3 = create_scrollable_tab("tab_3", 9)
        make_combo(tab3, 0, "lbl_head_mat", 'head_mat', ["Cast Iron", "Iron Eco.", "Iron Std.", "Iron Perf", "Aluminium", "Alu Eco", "Alu Std.", "Alu Perf", "Alu Billet Race"], "tt_head_mat")
        make_combo(tab3, 1, "lbl_valve", 'valvetrain', ["Pushrod (OHV)", "SOHC", "DOHC", "DAOHC"], "tt_valve")
        make_combo(tab3, 2, "lbl_valvesn", 'valves', [2, 3, 4, 5], "tt_valvesn")
        make_combo(tab3, 3, "lbl_vvt", 'vvt', ["None", "Intake", "All"], "tt_vvt")
        make_combo(tab3, 4, "lbl_vvl", 'vvl', ["None", "VVL", "CVVL"], "tt_vvl")
        self.frame_vvl_set = ttk.Frame(tab3); self.frame_vvl_set.grid(row=5, column=0, columnspan=4, sticky=tk.EW)
        make_slider(self.frame_vvl_set, 0, "lbl_vvl_prof", 'vvl_prof', 0, 100, 1, "", "tt_vvl_prof")
        make_slider(self.frame_vvl_set, 1, "lbl_vvl_rpm", 'vvl_rpm', 500, 12000, 100, "RPM", "tt_vvl_rpm")
        make_slider(tab3, 6, "lbl_springs", 'springs', 0, 100, 1, "", "tt_springs")
        make_slider(tab3, 7, "lbl_cam", 'cam_profile', 0, 100, 1, "", "tt_cam")
        make_slider(tab3, 8, "lbl_comp", 'comp_ratio', 7.0, 22.0, 0.1, ": 1", "tt_comp")

        # TAB 4 - Aspiration
        tab4 = create_scrollable_tab("tab_4", 7)
        make_combo(tab4, 0, "lbl_asp", 'aspiration', ["NA", "Turbo", "Supercharger"], "tt_asp")
        self.frame_turbo = ttk.Frame(tab4); self.frame_turbo.grid(row=1, column=0, columnspan=4, sticky=tk.EW, pady=5)
        make_combo(self.frame_turbo, 0, "lbl_tb", 'turbo_bearing', ["Journal", "Ball Bearings"], "tt_tb")
        make_combo(self.frame_turbo, 1, "lbl_tc", 'turbo_config', ["Single", "Twin", "Quad"], "tt_tc")
        make_slider(self.frame_turbo, 2, "lbl_ic", 'intercooler', 0, 100, 1, "%", "tt_ic")
        make_slider(self.frame_turbo, 3, "lbl_tsize", 'turb_size', 10, 100, 1, "", "tt_tsize")
        make_slider(self.frame_turbo, 4, "lbl_tboost", 'boost', 0.1, 3.0, 0.1, "bar", "tt_tboost")
        self.frame_sc = ttk.Frame(tab4); self.frame_sc.grid(row=2, column=0, columnspan=4, sticky=tk.EW, pady=5)
        make_combo(self.frame_sc, 0, "lbl_sct", 'sc_type', ["Roots", "Twin-screw", "Centrifugal"], "tt_sct")
        make_slider(self.frame_sc, 1, "lbl_csize", 'comp_size', 10, 100, 1, "", "tt_csize")
        make_slider(self.frame_sc, 2, "lbl_scp", 'sc_pulley', 0.1, 3.0, 0.1, "bar", "tt_scp")

        # TAB 5 - Fuel & Tune
        tab5 = create_scrollable_tab("tab_5", 10)
        make_combo(tab5, 0, "lbl_fdeliv", 'fuel_deliv', ["Carburetor", "Mechanical Fuel Injection", "Single Point EFI", "EFI Multi", "Direct Injection"], "tt_fdeliv")
        make_slider(tab5, 1, "lbl_carb_size", 'carb_size', 0, 100, 1, "", "tt_carb_size")
        make_combo(tab5, 2, "lbl_inconf", 'intake_conf', ["Single", "Twin", "ITB"], "tt_inconf")
        make_combo(tab5, 3, "lbl_man", 'manifold', ["Standard", "Std. Low", "Std. Mid", "Performance", "Perf. Mid", "Perf. High", "Race", "Compact", "Variable"], "tt_man")
        make_slider(tab5, 4, "lbl_man_size", 'man_size', 0, 100, 1, "", "tt_man_size")
        make_combo(tab5, 5, "lbl_fuel", 'fuel_type', ["Low Quality 85", "Regular 91", "Premium 95", "Super 98", "Ultimate 100", "E85", "Methanol", "Diesel", "Leaded Gasoline", "Compressed Gas", "Nitromethane"], "tt_fuel")
        make_slider(tab5, 6, "lbl_fuel_map", 'fuel_map', 0, 100, 1, "", "tt_fuel_map")
        make_slider(tab5, 7, "lbl_afr", 'afr', 10.0, 20.0, 0.1, "", "tt_afr")
        make_slider(tab5, 8, "lbl_ign", 'ignition', 0, 100, 1, "", "tt_ign")
        make_slider(tab5, 9, "lbl_lim", 'rpm_limit', 3000, 12000, 10, "RPM", "tt_lim")

        # TAB 6 - Exhaust
        tab6 = create_scrollable_tab("tab_6", 8)
        make_combo(tab6, 0, "lbl_arch", 'exh_arch', ["Single", "Dual"], "tt_arch")
        make_combo(tab6, 1, "lbl_head_exh", 'headers', ["Compact Cast", "Cast Low", "Cast Mid", "Cast", "Tubular", "Tubular Mid", "Tubular Long", "Tubular Race"], "tt_head_exh")
        make_slider(tab6, 2, "lbl_head_size", 'head_size', 0, 100, 1, "", "tt_head_size")
        make_slider(tab6, 3, "lbl_diam", 'exh_diam', 25.0, 150.0, 0.5, "mm", "tt_diam")
        make_combo(tab6, 4, "lbl_bypass", 'bypass', ["No Valves", "Bypass Valves"], "tt_bypass")
        make_combo(tab6, 5, "lbl_cat", 'cat', ["None", "2-way", "3-way", "High Flow", "Exhaust Reactor", "Three-Way + Pre-Cat", "High Flow 3-Way + Pre-Cat"], "tt_cat")
        make_combo(tab6, 6, "lbl_muf1", 'muffler1', ["None", "Straight", "Baffled", "Reverse Flow"], "tt_muf")
        make_combo(tab6, 7, "lbl_muf2", 'muffler2', ["None", "Straight", "Baffled", "Reverse Flow"], "tt_muf")

        # TAB 7 - Drivetrain
        tab7 = create_scrollable_tab("tab_7", 13)
        def apply_veh_preset(*args):
            if self._suspend_vehicle_preset_callback:
                return
            self.apply_vehicle_preset_values(self.vars['veh_preset'].get())
        self.vars['veh_preset'].trace_add("write", apply_veh_preset)
        make_combo(tab7, 0, "lbl_veh", 'veh_preset', ["Vlastní (Custom)", "Mazda 6 (2002)", "Muscle Car (1969)", "Lehký sporťák", "Moderní Supersport"], "tt_veh")
        make_slider(tab7, 1, "lbl_weight", 'veh_weight', 500.0, 3000.0, 10.0, "kg", "tt_weight")
        make_slider(tab7, 2, "lbl_cd", 'veh_cd', 0.20, 0.60, 0.01, "", "tt_cd")
        make_slider(tab7, 3, "lbl_area", 'veh_area', 1.2, 4.0, 0.01, "m²", "tt_area")
        make_slider(tab7, 4, "lbl_wheel", 'wheel_radius', 0.20, 0.55, 0.005, "m", "tt_wheel")
        make_slider(tab7, 5, "lbl_speed_limit", 'speed_limiter', 0.0, 450.0, 5.0, "km/h", "tt_speed_limit")
        make_slider(tab7, 6, "lbl_downforce", 'downforce_cla', 0.0, 4.0, 0.05, "m²", "tt_downforce")
        make_slider(tab7, 7, "lbl_grip", 'tire_grip', 0.5, 2.0, 0.1, "µ", "tt_grip")
        make_combo(tab7, 8, "lbl_gears", 'gears', [4, 5, 6, 7, 8], "tt_gears")
        make_slider(tab7, 9, "lbl_fd", 'final_drive', 2.0, 6.0, 0.1, ": 1", "tt_fd")
        make_combo(tab7, 10, "lbl_drive", 'drivetrain', ["FWD", "RWD", "AWD"], "tt_drive")

        self.chk_custom_gears = ttk.Checkbutton(tab7, textvariable=self.lang_vars['lbl_custom_gears'], variable=self.vars['custom_gears'])
        self.chk_custom_gears.grid(row=11, column=0, columnspan=4, sticky=tk.W, pady=(12, 5), padx=24)
        ToolTip(self.chk_custom_gears, self.lang_vars['tt_custom_gears'])

        self.frame_custom_gears = ttk.LabelFrame(tab7, padding=10)
        self.frame_custom_gears.grid(row=12, column=0, columnspan=4, sticky=tk.EW, pady=8, padx=24)
        self.gear_ratio_rows = []
        for index in range(1, 9):
            holder = ttk.Frame(self.frame_custom_gears)
            grid_row = (index - 1) % 4
            grid_col = 0 if index <= 4 else 2
            holder.grid(row=grid_row, column=grid_col, columnspan=2, sticky=tk.EW,
                        padx=(0, 20) if index <= 4 else (20, 0), pady=5)
            ttk.Label(holder, textvariable=self.lang_vars[f'lbl_gear_{index}'], width=12).pack(side=tk.LEFT)
            entry = ttk.Entry(holder, textvariable=self.vars[f'gear_{index}'], width=10, justify=tk.CENTER)
            entry.pack(side=tk.LEFT, padx=5)
            ttk.Label(holder, text=": 1").pack(side=tk.LEFT, padx=(3, 0))
            ToolTip(holder, self.lang_vars['tt_custom_gears']); ToolTip(entry, self.lang_vars['tt_custom_gears'])
            self.gear_ratio_rows.append(holder)
        ttk.Button(self.frame_custom_gears, textvariable=self.lang_vars['btn_reset_gears'],
                   command=self.reset_custom_gear_ratios).grid(row=4, column=0, columnspan=4, pady=(8, 0))

        self.vars['config'].trace_add("write", self.update_dynamic_ui)
        self.vars['aspiration'].trace_add("write", self.update_dynamic_ui)
        self.vars['balancer'].trace_add("write", self.update_dynamic_ui)
        self.vars['vvl'].trace_add("write", self.update_dynamic_ui)
        self.vars['custom_gears'].trace_add("write", self.update_dynamic_ui)
        self.vars['gears'].trace_add("write", self.on_gear_count_change)

        self.create_dyno_screen()
        self.btn_rev = self.nav_buttons['throttle']
        self.btn_drive = self.nav_buttons['drive']
        self.btn_track = self.nav_buttons['track']

    def create_dyno_screen(self):
        self.dyno_screen = tk.Frame(self.screen_container, bg="#0b1017")
        self.screens['dyno'] = self.dyno_screen
        self.dyno_screen.grid_columnconfigure(0, weight=4)
        self.dyno_screen.grid_columnconfigure(1, weight=2, minsize=360)
        self.dyno_screen.grid_rowconfigure(1, weight=1)

        header = tk.Frame(self.dyno_screen, bg="#0f1720", padx=28, pady=18)
        header.grid(row=0, column=0, columnspan=2, sticky="ew", padx=28, pady=(24, 12))
        self.dyno_engine_title = tk.Label(header, text=self.tr("ui_dyno_ready"),
                                          bg="#0f1720", fg="white", font=("Arial", 15, "bold"))
        self.dyno_engine_title.pack(side=tk.LEFT)
        controls = tk.Frame(header, bg="#0f1720")
        controls.pack(side=tk.RIGHT)
        self.btn_graph = ttk.Button(controls, textvariable=self.lang_vars['btn_graph'],
                                    command=self.plot_graph, state=tk.DISABLED)
        self.btn_graph.pack(side=tk.RIGHT, padx=(10, 0))
        self.btn_run = tk.Button(controls, textvariable=self.lang_vars['btn_dyno'], command=self.start_dyno,
                                 bg="#18a8c9", fg="#071015", activebackground="#3bd4f4",
                                 activeforeground="#071015", relief=tk.FLAT, bd=0, padx=22, pady=10,
                                 font=("Arial", 10, "bold"), cursor="hand2")
        self.btn_run.pack(side=tk.RIGHT)

        graph_card = tk.Frame(self.dyno_screen, bg="#101720", highlightbackground="#263746", highlightthickness=1)
        graph_card.grid(row=1, column=0, sticky="nsew", padx=(28, 12), pady=(0, 14))
        graph_card.grid_rowconfigure(0, weight=1); graph_card.grid_columnconfigure(0, weight=1)

        fig = plt.Figure(figsize=(10, 6), dpi=100, facecolor="#101720")
        self.dyno_ax_torque = fig.add_subplot(111)
        self.dyno_ax_torque.set_facecolor("#111923")
        self.dyno_ax_torque.set_xlabel("RPM", color="white")
        self.dyno_ax_torque.set_ylabel(self.tr('msg_trq') + ' (Nm)', color='#43d9ff')
        self.dyno_ax_torque.tick_params(axis='x', colors='white')
        self.dyno_ax_torque.tick_params(axis='y', colors='#43d9ff')
        self.dyno_ax_torque.grid(True, linestyle='--', alpha=0.22)
        for spine in self.dyno_ax_torque.spines.values():
            spine.set_color('#526273')
        self.dyno_ax_hp = self.dyno_ax_torque.twinx()
        self.dyno_ax_hp.set_ylabel(self.tr('msg_hp') + ' (HP)', color='#ff6b6b')
        self.dyno_ax_hp.tick_params(axis='y', colors='#ff6b6b')
        for spine in self.dyno_ax_hp.spines.values():
            spine.set_color('#526273')
        self.dyno_torque_line, = self.dyno_ax_torque.plot([], [], color='#43d9ff', linewidth=2.7, label=self.tr('msg_trq'))
        self.dyno_hp_line, = self.dyno_ax_hp.plot([], [], color='#ff6b6b', linewidth=2.7, label=self.tr('msg_hp'))
        fig.subplots_adjust(left=0.14, right=0.84, bottom=0.14, top=0.95)
        self.graph_figure = fig
        self.graph_canvas = FigureCanvasTkAgg(fig, master=graph_card)
        self.graph_canvas.draw()
        self.graph_canvas.get_tk_widget().grid(row=0, column=0, sticky="nsew", padx=12, pady=12)

        stats = tk.Frame(self.dyno_screen, bg="#101720", highlightbackground="#263746", highlightthickness=1)
        stats.grid(row=1, column=1, sticky="nsew", padx=(12, 28), pady=(0, 14))
        self.dyno_telemetry_title = tk.Label(
            stats, textvariable=self.lang_vars["ui_live_telemetry"], bg="#101720", fg="#8fa5b7",
            font=("Arial", 10, "bold")
        )
        self.dyno_telemetry_title.pack(pady=(28, 18))
        self.dyno_live_rpm = tk.Label(stats, text="1000", bg="#101720", fg="#43d9ff", font=("Courier", 42, "bold"))
        self.dyno_live_rpm.pack()
        tk.Label(stats, text="RPM", bg="#101720", fg="#8fa5b7", font=("Arial", 10, "bold")).pack(pady=(0, 24))
        metric_row = tk.Frame(stats, bg="#101720")
        metric_row.pack(fill=tk.X, padx=24)
        hp_card = tk.Frame(metric_row, bg="#151f2a", padx=16, pady=18)
        hp_card.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 6))
        self.dyno_live_hp = tk.Label(hp_card, text="0", bg="#151f2a", fg="#ff6b6b", font=("Courier", 27, "bold"))
        self.dyno_live_hp.pack(); tk.Label(hp_card, text="HP", bg="#151f2a", fg="#a8b6c2").pack()
        trq_card = tk.Frame(metric_row, bg="#151f2a", padx=16, pady=18)
        trq_card.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(6, 0))
        self.dyno_live_trq = tk.Label(trq_card, text="0", bg="#151f2a", fg="#43d9ff", font=("Courier", 27, "bold"))
        self.dyno_live_trq.pack(); tk.Label(trq_card, text="Nm", bg="#151f2a", fg="#a8b6c2").pack()
        self.dyno_status = tk.Label(stats, text=self.tr("ui_ready"), bg="#101720", fg="#8fa5b7",
                                    font=("Arial", 12, "bold"), wraplength=310, justify=tk.CENTER)
        self.dyno_status.pack(fill=tk.X, padx=30, pady=28)

        console_card = tk.Frame(self.dyno_screen, bg="#101720", highlightbackground="#263746", highlightthickness=1)
        console_card.grid(row=2, column=0, columnspan=2, sticky="ew", padx=28, pady=(0, 28))
        self.txt_output = tk.Text(console_card, height=7, bg="#05080b", fg="#55ff77",
                                  insertbackground="white", font=("Courier", 10), relief=tk.FLAT,
                                  padx=14, pady=12)
        self.txt_output.pack(fill=tk.X, padx=1, pady=1)
        self.txt_output.config(state=tk.DISABLED)
        self._reset_dyno_visuals()

    def _reset_dyno_visuals(self):
        if hasattr(self, 'dyno_torque_line'):
            self.dyno_torque_line.set_data([], [])
            self.dyno_hp_line.set_data([], [])
            self.dyno_ax_torque.set_xlim(1000, 7000)
            self.dyno_ax_torque.set_ylim(0, 200)
            self.dyno_ax_hp.set_ylim(0, 200)
            self.graph_canvas.draw_idle()
        if hasattr(self, 'dyno_live_rpm'):
            self.dyno_live_rpm.config(text="1000")
            self.dyno_live_hp.config(text="0")
            self.dyno_live_trq.config(text="0")

    def apply_vehicle_preset_values(self, preset):
        if preset == "Mazda 6 (2002)":
            values = (1350.0, 0.30, 2.20, 0.315, 0.0, 0.0, 0.9, 5, 4.3, "FWD")
        elif preset == "Muscle Car (1969)":
            values = (1750.0, 0.45, 2.35, 0.345, 0.0, 0.0, 0.7, 4, 3.1, "RWD")
        elif preset == "Lehký sporťák":
            values = (1050.0, 0.33, 1.85, 0.305, 0.0, 0.05, 1.1, 6, 3.62, "RWD")
        elif preset == "Moderní Supersport":
            values = (1550.0, 0.28, 2.00, 0.345, 0.0, 0.25, 1.4, 8, 3.8, "AWD")
        else:
            return
        self.vars['custom_gears'].set(False)
        keys = ('veh_weight', 'veh_cd', 'veh_area', 'wheel_radius', 'speed_limiter', 'downforce_cla', 'tire_grip', 'gears', 'final_drive', 'drivetrain')
        for key, value in zip(keys, values):
            self._set_var(key, value)

    def reset_custom_gear_ratios(self):
        gear_count = int(self.vars['gears'].get())
        automatic = get_gear_ratios(gear_count)
        tail_defaults = {
            4: [0.65, 0.55, 0.45, 0.35],
            5: [0.65, 0.55, 0.45],
            6: [0.50, 0.40],
            7: [0.45],
            8: [],
        }
        values = automatic + tail_defaults[gear_count]
        for index, value in enumerate(values, start=1):
            self.vars[f'gear_{index}'].set(value)

    def on_gear_count_change(self, *args):
        if not self.vars['custom_gears'].get():
            self.reset_custom_gear_ratios()
        self.update_dynamic_ui()

    def get_selected_gear_ratios(self):
        gear_count = int(self.vars['gears'].get())
        if not self.vars['custom_gears'].get():
            return None
        return [float(self.vars[f'gear_{index}'].get()) for index in range(1, gear_count + 1)]

    def build_vehicle_params(self):
        params = self.collect_parameters()
        return {
            'weight': float(params['veh_weight']),
            'cd': float(params['veh_cd']),
            'area': float(params['veh_area']),
            'wheel_radius': float(params['wheel_radius']),
            'speed_limiter': float(params['speed_limiter']),
            'downforce_cla': float(params['downforce_cla']),
            'grip': float(params['tire_grip']),
            'gears': int(params['gears']),
            'final_drive': float(params['final_drive']),
            'drivetrain': params['drivetrain'],
            'gear_ratios': self.get_selected_gear_ratios(),
        }

    def bind_dyno_invalidation_traces(self):
        vehicle_keys = {
            'veh_preset', 'veh_weight', 'veh_cd', 'veh_area', 'wheel_radius',
            'speed_limiter', 'downforce_cla', 'tire_grip', 'gears', 'final_drive',
            'drivetrain', 'custom_gears',
            *(f'gear_{index}' for index in range(1, 9)),
        }
        for key, var in self.vars.items():
            if key not in vehicle_keys and key not in ('calc_disp', 'app_lang'):
                var.trace_add('write', self.invalidate_dyno)

    def invalidate_dyno(self, *args):
        if self._dyno_running:
            self._dyno_changed_during_run = True
            return

        # Změna motoru během aktivního režimu musí nejprve bezpečně ukončit
        # jeho callbacky a zvuk. Jinak by další tick ručního plynu nebo jízdy
        # sáhl do právě vyprázdněných dyno dat a vyhodil KeyError.
        if self.current_screen in ('throttle', 'drive', 'track'):
            self.show_screen('builder')

        self.dyno_results = {}
        self.dyno_params = None
        if hasattr(self, 'btn_graph'):
            self.btn_graph.config(state=tk.DISABLED)
        for name in ('throttle', 'drive', 'track'):
            if name in self.nav_buttons:
                self.nav_buttons[name].config(state=tk.DISABLED)
        if hasattr(self, 'dyno_status'):
            self.dyno_status.config(text=self._ui("Motor byl změněn. Spusť nové měření.",
                                                   "Engine changed. Run a new dyno pull."), fg="#ffb454")

    def update_dynamic_ui(self, *args):
        if self.vars['config'].get() == "V": self.frame_v.grid()
        else: self.frame_v.grid_remove()
        
        asp = self.vars['aspiration'].get()
        if asp == "Turbo": self.frame_turbo.grid(); self.frame_sc.grid_remove()
        elif asp == "Supercharger": self.frame_turbo.grid_remove(); self.frame_sc.grid()
        else: self.frame_turbo.grid_remove(); self.frame_sc.grid_remove()

        if self.vars['balancer'].get() == "None": self.frame_bal_mass.grid_remove()
        else: self.frame_bal_mass.grid()

        if self.vars['vvl'].get() == "None": self.frame_vvl_set.grid_remove()
        else: self.frame_vvl_set.grid()

        if hasattr(self, 'frame_custom_gears'):
            if self.vars['custom_gears'].get():
                self.frame_custom_gears.grid()
                gear_count = int(self.vars['gears'].get())
                for index, holder in enumerate(self.gear_ratio_rows, start=1):
                    if index <= gear_count:
                        holder.grid()
                    else:
                        holder.grid_remove()
            else:
                self.frame_custom_gears.grid_remove()

        if hasattr(self, 'scrollable_tabs'):
            for scroll_tab in self.scrollable_tabs:
                scroll_tab._schedule_refresh()

    def update_displacement(self):
        try:
            b, s, c = self.vars['bore'].get(), self.vars['stroke'].get(), self.vars['cylinders'].get()
            disp = math.pi * ((b/20)**2) * (s/10) * c
            self.vars['calc_disp'].set(f"{disp:.0f} cc")
            return disp
        except (ValueError, TypeError, tk.TclError):
            return 2000

    def safe_log(self, msg):
        self.root.after(0, self._write_log, msg)

    def _write_log(self, msg):
        self.txt_output.config(state=tk.NORMAL)
        self.txt_output.insert(tk.END, msg + "\n")
        self.txt_output.see(tk.END)
        self.txt_output.config(state=tk.DISABLED)

    def safe_clear_console(self):
        self.root.after(0, self._clear_console)

    def _clear_console(self):
        self.txt_output.config(state=tk.NORMAL)
        self.txt_output.delete(1.0, tk.END)
        self.txt_output.config(state=tk.DISABLED)

    def safe_update_pull(self, header, rpm, trq, hp):
        self.root.after(0, self._write_pull, header, rpm, trq, hp)

    def _write_pull(self, header, rpm, trq, hp):
        self.txt_output.config(state=tk.NORMAL)
        self.txt_output.delete(1.0, tk.END)
        self.txt_output.insert(tk.END, header + "\n\n")
        self.txt_output.insert(tk.END, f"{self.tr('msg_rpm')}: {rpm:04d} | {self.tr('msg_trq')}: {trq:4.0f} Nm | {self.tr('msg_hp')}: {hp:4.0f} HP")
        self.txt_output.config(state=tk.DISABLED)

    def collect_parameters(self):
        params = {'lang': self.vars['app_lang'].get()}
        errors = []
        try:
            displayed_limiter = float(self.speed_limiter_display.get())
            if not math.isfinite(displayed_limiter):
                errors.append('speed_limiter')
        except (TypeError, ValueError, tk.TclError):
            errors.append('speed_limiter')
        for key, var in self.vars.items():
            if key in ('calc_disp', 'app_lang'):
                continue
            try:
                params[key] = var.get()
            except tk.TclError:
                errors.append(key)

        limits = {
            'bore': (50.0, 120.0), 'stroke': (20.0, 150.0), 'radiator': (10.0, 100.0),
            'tech_level': (50.0, 150.0), 'balancer_mass': (0.0, 50.0), 'vvl_prof': (0.0, 100.0),
            'vvl_rpm': (500.0, 12000.0), 'springs': (0.0, 100.0), 'cam_profile': (0.0, 100.0),
            'comp_ratio': (7.0, 22.0), 'intercooler': (0.0, 100.0), 'turb_size': (10.0, 100.0),
            'boost': (0.1, 3.0), 'comp_size': (10.0, 100.0), 'sc_pulley': (0.1, 3.0),
            'carb_size': (0.0, 100.0), 'man_size': (0.0, 100.0), 'fuel_map': (0.0, 100.0),
            'afr': (10.0, 20.0), 'ignition': (0.0, 100.0), 'rpm_limit': (3000.0, 20000.0),
            'head_size': (0.0, 100.0), 'exh_diam': (25.0, 150.0), 'veh_weight': (500.0, 3000.0),
            'veh_cd': (0.20, 0.60), 'veh_area': (1.2, 4.0), 'wheel_radius': (0.20, 0.55),
            'speed_limiter': (0.0, 450.0), 'downforce_cla': (0.0, 4.0), 'tire_grip': (0.3, 2.5),
            'final_drive': (1.5, 10.0),
        }
        for key, (low, high) in limits.items():
            if key not in params:
                continue
            try:
                value = float(params[key])
                if not math.isfinite(value) or value < low or value > high:
                    errors.append(f"{key} [{low}, {high}]")
            except (TypeError, ValueError):
                errors.append(key)
        for key, options in self.allowed_values.items():
            if key in params and params[key] not in options:
                errors.append(f"{key}: {params[key]!r}")
        if int(params.get('cylinders', 0)) not in (3, 4, 5, 6, 8, 10, 12, 16):
            errors.append('cylinders')
        if int(params.get('gears', 0)) not in (4, 5, 6, 7, 8):
            errors.append('gears')
        if bool(params.get('custom_gears', False)):
            try:
                gear_count = int(params['gears'])
                ratios = [float(params[f'gear_{index}']) for index in range(1, gear_count + 1)]
                get_gear_ratios(gear_count, ratios)
            except (KeyError, TypeError, ValueError) as exc:
                errors.append(str(exc))
        if errors:
            raise ValueError(", ".join(dict.fromkeys(errors)))
        return params

    def start_dyno(self):
        self.show_screen("dyno")
        self.btn_run.config(state=tk.DISABLED)
        self.builder_run_button.config(state=tk.DISABLED)
        self.btn_graph.config(state=tk.DISABLED)
        for name in ('throttle', 'drive', 'track'):
            self.nav_buttons[name].config(state=tk.DISABLED)
        self._clear_console()
        self._reset_dyno_visuals()
        self.dyno_results = {}
        self.dyno_params = None
        self._dyno_changed_during_run = False

        try:
            params = self.collect_parameters()
            results = run_engine_simulation(params)
            if (not np.all(np.isfinite(results['hp'])) or not np.all(np.isfinite(results['torque']))
                    or float(np.max(results['hp'])) <= 0.0 or float(np.max(results['torque'])) <= 0.0):
                if params.get('lang') == 'cz':
                    raise ValueError("Motor nevytváří použitelný výkon ani točivý moment")
                raise ValueError("Engine produces no usable power or torque")
        except (ValueError, TypeError, tk.TclError, FloatingPointError) as exc:
            messagebox.showerror(self.tr('msg_invalid'), str(exc))
            self.btn_run.config(state=tk.NORMAL)
            self.builder_run_button.config(state=tk.NORMAL)
            return

        self.dyno_params = params
        self.dyno_results = results
        self._dyno_running = True
        name = str(params.get('engine_name', ''))
        disp = math.pi * ((float(params['bore']) / 20.0) ** 2) * (float(params['stroke']) / 10.0) * int(params['cylinders'])
        spec = f"{disp:.0f} cc {params.get('config', '')}{params.get('cylinders', '')}"
        self._dyno_header = f"{self.tr('msg_dyno_hdr')} {name} ({spec}) ---"
        self.dyno_engine_title.config(text=f"{name}   •   {spec}   •   {params.get('aspiration', '')}")
        self.dyno_status.config(text=self.tr("ui_dyno_running"), fg="#ffcc55")
        self._dyno_index = 0
        self._dyno_step_ms = 80
        self._dyno_temp_path = None

        rpm = np.asarray(results['rpm'], dtype=float)
        hp = np.asarray(results['hp'], dtype=float)
        trq = np.asarray(results['torque'], dtype=float)
        max_val = max(float(np.max(hp)), float(np.max(trq)), 1.0)
        self.dyno_ax_torque.set_xlim(float(rpm[0]), float(rpm[-1]))
        self.dyno_ax_torque.set_ylim(0, max_val * 1.12)
        self.dyno_ax_hp.set_ylim(0, max_val * 1.12)
        self.dyno_torque_line.set_data([], [])
        self.dyno_hp_line.set_data([], [])
        self.graph_canvas.draw_idle()

        if is_windows:
            try:
                fd, path = tempfile.mkstemp(prefix='automation_dyno_', suffix='.wav')
                os.close(fd)
                self._dyno_temp_path = path
                generate_engine_wav(results['rpm'], int(params['cylinders']), params['aspiration'],
                                    params.get('crank', 'Cast'), path, self._dyno_step_ms / 1000.0)
                winsound.PlaySound(path, winsound.SND_FILENAME | winsound.SND_ASYNC)
            except (OSError, wave.Error, ValueError):
                self._dyno_temp_path = None

        self._dyno_after_id = self.root.after(350, self._dyno_tick)

    def _dyno_tick(self):
        self._dyno_after_id = None
        if not self._dyno_running or not self.dyno_results:
            return
        if self._dyno_index < len(self.dyno_results['rpm']):
            i = self._dyno_index
            rpm = int(self.dyno_results['rpm'][i])
            trq = float(self.dyno_results['torque'][i])
            hp = float(self.dyno_results['hp'][i])
            self._write_pull(self._dyno_header, rpm, trq, hp)
            self.dyno_live_rpm.config(text=f"{rpm}")
            self.dyno_live_trq.config(text=f"{trq:.0f}")
            self.dyno_live_hp.config(text=f"{hp:.0f}")
            visible = slice(0, i + 1)
            self.dyno_torque_line.set_data(self.dyno_results['rpm'][visible], self.dyno_results['torque'][visible])
            self.dyno_hp_line.set_data(self.dyno_results['rpm'][visible], self.dyno_results['hp'][visible])
            self.graph_canvas.draw_idle()
            self._dyno_index += 1
            self._dyno_after_id = self.root.after(self._dyno_step_ms, self._dyno_tick)
            return
        self._finish_dyno()

    def _finish_dyno(self):
        self._dyno_after_id = None
        if is_windows:
            try:
                winsound.PlaySound(None, winsound.SND_PURGE)
            except Exception:
                pass
            if self.dyno_results.get('blew_up'):
                winsound.MessageBeep(winsound.MB_ICONHAND)
            if self._dyno_temp_path:
                try:
                    os.remove(self._dyno_temp_path)
                except OSError:
                    pass
                self._dyno_temp_path = None

        self._write_log(self.tr('msg_done'))
        if self.dyno_results['blew_up']:
            self._write_log(f"{self.tr('msg_blown')} {self.dyno_results['reason']}")
            self._write_log(f"{self.tr('msg_fix')} {self.dyno_results['fix']}")
            self.dyno_status.config(text=self.tr('msg_blown'), fg="#ff5f5f")
        else:
            max_hp = float(np.max(self.dyno_results['hp']))
            max_hp_rpm = int(self.dyno_results['rpm'][int(np.argmax(self.dyno_results['hp']))])
            max_trq = float(np.max(self.dyno_results['torque']))
            max_trq_rpm = int(self.dyno_results['rpm'][int(np.argmax(self.dyno_results['torque']))])
            self._write_log(f"{self.tr('msg_max_hp')}  {max_hp:.0f} HP @ {max_hp_rpm} RPM")
            self._write_log(f"{self.tr('msg_max_trq')} {max_trq:.0f} Nm @ {max_trq_rpm} RPM")
            self._write_log(self.tr('msg_ready'))
            self.dyno_status.config(
                text=(f"{self.tr('msg_max_hp')} {max_hp:.0f} HP @ {max_hp_rpm} RPM\n"
                      f"{self.tr('msg_max_trq')} {max_trq:.0f} Nm @ {max_trq_rpm} RPM"),
                fg="#63f28a"
            )

        self._dyno_running = False
        self.btn_run.config(state=tk.NORMAL)
        self.builder_run_button.config(state=tk.NORMAL)
        self.btn_graph.config(state=tk.NORMAL)
        if not self.dyno_results.get('blew_up', True):
            self.nav_buttons['track'].config(state=tk.NORMAL)
            self.nav_buttons['throttle'].config(state=tk.NORMAL)
            self.nav_buttons['drive'].config(state=tk.NORMAL)
        if self._dyno_changed_during_run:
            self.invalidate_dyno()

    def plot_graph(self):
        if not self.dyno_results:
            self.show_screen('dyno')
            return
        self.show_screen('dyno')
        rpm = self.dyno_results['rpm']
        hp = self.dyno_results['hp']
        trq = self.dyno_results['torque']
        max_val = max(float(np.max(hp)), float(np.max(trq)), 1.0)
        self.dyno_ax_torque.set_xlim(float(rpm[0]), float(rpm[-1]))
        self.dyno_ax_torque.set_ylim(0, max_val * 1.12)
        self.dyno_ax_hp.set_ylim(0, max_val * 1.12)
        self.dyno_torque_line.set_data(rpm, trq)
        self.dyno_hp_line.set_data(rpm, hp)
        self.graph_canvas.draw_idle()

    def open_throttle_window(self):
        if not self.dyno_results or self.dyno_results.get("blew_up", True):
            return
        if self.current_screen == 'throttle' and getattr(self, 'rev_window', None) is not None and self.rev_window.winfo_exists():
            return
        try:
            self.collect_parameters()
        except (ValueError, TypeError, tk.TclError, FloatingPointError) as exc:
            messagebox.showerror(self.tr('msg_invalid'), str(exc))
            return

        old = self.screens.get('throttle')
        if old is not None and old.winfo_exists():
            old.destroy()
        self.rev_window = EmbeddedScreen(self, "throttle", bg="#0b1017")
        self.screens["throttle"] = self.rev_window
        self.rev_window.grid_columnconfigure(0, weight=3)
        self.rev_window.grid_columnconfigure(1, weight=2)
        self.rev_window.grid_rowconfigure(0, weight=1)

        self.throttle_active = False
        self.last_throttle = False
        self.flutter_intensity = 0.0
        self.current_rpm = 1000.0
        self.audio_phase = 0.0
        self.rev_phase = 0.0
        self.flutter_phase = 0.0
        self.coolant_temp = 90.0
        self.engine_blown = False
        self.blow_timer = 0.0
        self.radiator_eff = float(self.dyno_params['radiator']) / 100.0
        limit_rpm = float(self.dyno_params['rpm_limit'])

        gauge_card = tk.Frame(self.rev_window, bg="#101720", highlightbackground="#263746", highlightthickness=1)
        gauge_card.grid(row=0, column=0, sticky="nsew", padx=(54, 18), pady=54)
        gauge_card.grid_rowconfigure(0, weight=1); gauge_card.grid_columnconfigure(0, weight=1)
        self.tacho_rev = AnalogTachometer(gauge_card, max_rpm=limit_rpm + 1000,
                                          redline_rpm=limit_rpm, size=430)
        self.tacho_rev.grid(row=0, column=0, pady=(28, 8))
        self.lbl_telemetry = tk.Label(gauge_card, text="0 HP  |  0 Nm", font=("Courier", 18, "bold"),
                                      bg="#101720", fg='white')
        self.lbl_telemetry.grid(row=1, column=0, pady=8)
        self.lbl_temp = tk.Label(gauge_card, text=f"{self.tr('lbl_coolant')} 90°C",
                                 font=("Arial", 14, "bold"), bg="#101720", fg="#8fa5b7")
        self.lbl_temp.grid(row=2, column=0, pady=(4, 28))

        pedal_card = tk.Frame(self.rev_window, bg="#101720", highlightbackground="#263746", highlightthickness=1)
        pedal_card.grid(row=0, column=1, sticky="nsew", padx=(18, 54), pady=54)
        pedal_card.grid_columnconfigure(0, weight=1); pedal_card.grid_rowconfigure(2, weight=1)
        self.throttle_control_title = tk.Label(
            pedal_card, textvariable=self.lang_vars["ui_engine_control"], bg="#101720",
            fg="#43d9ff", font=("Arial", 14, "bold")
        )
        self.throttle_control_title.grid(row=0, column=0, pady=(42, 10))
        self.throttle_instruction = tk.Label(
            pedal_card, textvariable=self.lang_vars["ui_throttle_instruction"],
            bg="#101720", fg="#aebdca", font=("Arial", 11), wraplength=390,
            justify=tk.CENTER
        )
        self.throttle_instruction.grid(row=1, column=0, padx=36, pady=(0, 20))
        self.btn_pedal = tk.Button(
            pedal_card, textvariable=self.lang_vars["btn_pedal"],
            bg="#1e3a4c", fg="white", activebackground="#18a8c9",
            activeforeground="#071015", relief=tk.FLAT, bd=0,
            font=("Arial", 13, "bold"), cursor="hand2"
        )
        self.btn_pedal.grid(row=2, column=0, padx=55, pady=35, sticky="nsew")
        self.btn_pedal.bind("<ButtonPress-1>", lambda e: setattr(self, 'throttle_active', True) if not self.engine_blown else None)
        self.btn_pedal.bind("<ButtonRelease-1>", lambda e: setattr(self, 'throttle_active', False))
        self.btn_pedal.bind("<Leave>", lambda e: setattr(self, 'throttle_active', False))
        self.throttle_exit_hint = tk.Label(
            pedal_card, textvariable=self.lang_vars["ui_mode_exit_hint"],
            bg="#101720", fg="#6f8395", font=("Arial", 9)
        )
        self.throttle_exit_hint.grid(row=3, column=0, pady=(0, 28))

        self.show_screen("throttle")
        self.start_audio_stream()
        self.update_throttle_physics()

    def update_throttle_physics(self):
        self._throttle_after_id = None
        if (self.current_screen != 'throttle' or not hasattr(self, 'rev_window')
                or self.rev_window is None or not self.rev_window.winfo_exists()):
            return
        if not self.dyno_results or self.dyno_params is None:
            self.show_screen('builder')
            return
        limit_rpm = float(self.dyno_params['rpm_limit'])

        if not self.engine_blown:
            target_rpm = limit_rpm if self.throttle_active else 1000.0
            diff = target_rpm - self.current_rpm
            self.current_rpm += diff * (0.08 if self.throttle_active else 0.04)
            self.current_rpm = max(1000.0, min(self.current_rpm, limit_rpm))
            cur_hp = np.interp(self.current_rpm, self.dyno_results["rpm"], self.dyno_results["hp"])
            cur_trq = np.interp(self.current_rpm, self.dyno_results["rpm"], self.dyno_results["torque"])
            load = 1.0 if self.throttle_active else 0.05
            heat_gen = math.sqrt(max(1, cur_hp)) * 0.06 * load * (self.current_rpm / limit_rpm)
            cooling = self.radiator_eff * ((self.coolant_temp - 20.0) / 100.0)
            self.coolant_temp = max(20.0, self.coolant_temp + (heat_gen - cooling - 0.01) * 0.05)
            self.lbl_temp.config(text=f"{self.tr('lbl_coolant')} {int(self.coolant_temp)}°C",
                                 fg="#ff5f5f" if self.coolant_temp > 115.0 else "#8fa5b7")
            if self.coolant_temp >= 130.0:
                self.engine_blown = True
                self.throttle_active = False
                self.lbl_temp.config(text=self.tr("msg_hg_blown"), fg="#ff5f5f")
        else:
            self.blow_timer += 0.03
            self.current_rpm *= 0.95
            cur_hp, cur_trq = 0, 0

        if not self.engine_blown:
            self.tacho_rev.set_rpm(self.current_rpm)
            self.lbl_telemetry.config(text=f"{int(cur_hp)} HP  |  {int(cur_trq)} Nm")
        self._throttle_after_id = self.root.after(30, self.update_throttle_physics)

    def on_rev_close(self):
        self._cleanup_screen('throttle')
        self._activate_screen('builder')

    def open_drive_window(self):
        if not self.dyno_results or self.dyno_results.get("blew_up", True):
            return
        if self.current_screen == 'drive' and getattr(self, 'drive_win', None) is not None and self.drive_win.winfo_exists():
            return
        try:
            self.drive_vehicle_params = self.build_vehicle_params()
        except (ValueError, TypeError, tk.TclError, FloatingPointError) as exc:
            messagebox.showerror(self.tr('msg_invalid'), str(exc))
            return

        old = self.screens.get('drive')
        if old is not None and old.winfo_exists():
            old.destroy()
        self.drive_win = EmbeddedScreen(self, "drive", bg="#0b1017")
        self.screens["drive"] = self.drive_win
        self.drive_win.grid_columnconfigure(0, weight=3)
        self.drive_win.grid_columnconfigure(1, weight=2)
        self.drive_win.grid_rowconfigure(0, weight=1)
        limit_rpm = float(self.dyno_params['rpm_limit'])

        gauge_card = tk.Frame(self.drive_win, bg="#101720", highlightbackground="#263746", highlightthickness=1)
        gauge_card.grid(row=0, column=0, sticky="nsew", padx=(54, 18), pady=54)
        gauge_card.grid_rowconfigure(0, weight=1); gauge_card.grid_columnconfigure(0, weight=1)
        self.tacho_drive = AnalogTachometer(gauge_card, max_rpm=limit_rpm + 1000,
                                            redline_rpm=limit_rpm, size=430)
        self.tacho_drive.grid(row=0, column=0, pady=28)

        dashboard = tk.Frame(self.drive_win, bg="#101720", highlightbackground="#263746", highlightthickness=1)
        dashboard.grid(row=0, column=1, sticky="nsew", padx=(18, 54), pady=54)
        dashboard.grid_columnconfigure(0, weight=1)
        self.drive_speed_title = tk.Label(
            dashboard, textvariable=self.lang_vars["ui_speed"], bg="#101720", fg="#8fa5b7",
            font=("Arial", 10, "bold")
        )
        self.drive_speed_title.grid(row=0, column=0, pady=(38, 0))
        self.lbl_speed = tk.Label(dashboard, text="0", font=("Courier", 76, "bold"), bg="#101720", fg='#43d9ff')
        self.lbl_speed.grid(row=1, column=0, pady=(0, 0))
        self.lbl_speed_unit = tk.Label(dashboard, textvariable=self.speed_unit_text,
                                       font=("Courier", 16), bg="#101720", fg='white')
        self.lbl_speed_unit.grid(row=2, column=0)

        gear_card = tk.Frame(dashboard, bg="#151f2a", padx=26, pady=14)
        gear_card.grid(row=3, column=0, sticky="ew", padx=42, pady=22)
        self.drive_gear_title = tk.Label(
            gear_card, textvariable=self.lang_vars["ui_gear"], font=("Arial", 12, "bold"),
            bg="#151f2a", fg='#8fa5b7'
        )
        self.drive_gear_title.pack(side=tk.LEFT)
        self.lbl_gear = tk.Label(gear_card, text="N", font=("Courier", 34, "bold"), bg="#151f2a", fg='white')
        self.lbl_gear.pack(side=tk.RIGHT)

        self.lbl_tcs = tk.Label(dashboard, text=self.tr("ui_tcs_ready"), font=("Arial", 13, "bold"),
                                bg='#1b2631', fg='#8fa5b7', padx=18, pady=9)
        self.lbl_tcs.grid(row=4, column=0, sticky="ew", padx=42, pady=6)
        self.lbl_accel = tk.Label(dashboard, text=f"{self._acceleration_label()}: -- s",
                                  font=("Courier", 15, "bold"), bg="#101720", fg='#8fa5b7')
        self.lbl_accel.grid(row=5, column=0, pady=18)

        btn_container = tk.Frame(dashboard, bg='#101720')
        btn_container.grid(row=6, column=0, pady=(4, 35))
        self.drive_launch_text = tk.StringVar(value=self.tr("btn_launch"))
        self.drive_skip_text = tk.StringVar(value=self.tr("btn_skip"))
        self.btn_launch = ttk.Button(
            btn_container, textvariable=self.drive_launch_text, command=self.start_launch
        )
        self.btn_launch.pack(side=tk.LEFT, padx=7)
        self.btn_skip = ttk.Button(
            btn_container, textvariable=self.drive_skip_text, command=self.skip_to_top_speed,
            state=tk.DISABLED
        )
        self.btn_skip.pack(side=tk.LEFT, padx=7)

        self.drive_running = False
        self.throttle_active = False
        self.last_throttle = False
        self.v = 0.0
        self.max_achieved_speed = 0.0
        self.gear = 0
        self.current_rpm = 1000.0
        self.shift_delay = 0.0
        self.a_prev = 0.0
        self.slip_active = False
        self.drive_time = 0.0
        self.accel_time = None
        self.drive_reference_result = None
        self.audio_phase = 0.0
        self.rev_phase = 0.0
        self.flutter_phase = 0.0
        self.flutter_intensity = 0.0

        self.show_screen("drive")
        self.start_audio_stream(is_drive=True)
        self._drive_after_id = self.root.after(100, self.drive_step)

    def start_launch(self):
        if self.drive_running:
            return
        try:
            # Jeden autoritativní výpočet používá stejnou fyziku jako tlačítko
            # "Přeskočit na max". Živá animace k tomuto výsledku přirozeně dojede.
            self.drive_reference_result = run_vehicle_kinematics(
                self.drive_vehicle_params, self.dyno_results
            )
        except (ValueError, TypeError, tk.TclError, FloatingPointError) as exc:
            messagebox.showerror(self.tr('msg_invalid'), str(exc), parent=self.drive_win)
            return

        self.drive_running = True
        self.throttle_active = True
        self.v = 0.0
        self.max_achieved_speed = 0.0
        self.gear = 0
        self.current_rpm = 1000.0
        self.a_prev = 0.0
        self.shift_delay = 0.0
        self.drive_time = 0.0
        self.accel_time = None

        self.lbl_speed.config(text="0")
        self.lbl_gear.config(text="1", fg="white")
        self.lbl_tcs.config(text=self.tr("ui_tcs_ok"), fg="gray", bg="#222222")
        self.lbl_accel.config(text=f"{self._acceleration_label()}: -- s", fg="gray")
        self.drive_launch_text.set(self.tr("btn_accel"))
        self.btn_launch.config(state=tk.DISABLED)
        self.btn_skip.config(state=tk.NORMAL)

    def _finish_drive_result(self, result):
        """Ukončí živou i přeskočenou jízdu přesně stejným výsledkem."""
        self.v = float(result["top_speed"])
        self.max_achieved_speed = self.v
        self.gear = int(result["final_gear"])

        veh_params = self.drive_vehicle_params
        wheel_rpm = (self.v / (2.0 * math.pi * veh_params['wheel_radius'])) * 60.0
        ratios = get_gear_ratios(veh_params['gears'], veh_params.get('gear_ratios'))
        max_rpm = float(self.dyno_results['rpm'][-1])
        self.current_rpm = min(
            max_rpm,
            max(1000.0, wheel_rpm * ratios[self.gear] * veh_params['final_drive'])
        )

        self.accel_time = self._selected_acceleration_time(result)
        if self.accel_time is not None:
            self.lbl_accel.config(
                text=f"{self._acceleration_label()}: {self.accel_time:.2f} s", fg="#00ffff"
            )
        else:
            self.lbl_accel.config(
                text=f"{self._acceleration_label()}: {self.tr('msg_not_reached')}", fg="red"
            )

        self.drive_running = False
        self.throttle_active = False
        self.tacho_drive.set_rpm(self.current_rpm)
        self.lbl_speed.config(text=f"{self._speed_from_mps(self.v):.0f}")
        self.lbl_gear.config(text=str(self.gear + 1), fg="white")
        self.lbl_tcs.config(
            text=f"{self.tr('ui_max')}: {self._speed_from_mps(self.max_achieved_speed):.0f} {self._speed_unit_label()}",
            fg="black", bg="lime"
        )
        self.drive_launch_text.set(self.tr("btn_retry"))
        self.btn_launch.config(state=tk.NORMAL)
        self.btn_skip.config(state=tk.DISABLED)

    def skip_to_top_speed(self):
        if not self.drive_running:
            return
        self.btn_skip.config(state=tk.DISABLED)

        try:
            result = self.drive_reference_result
            if result is None:
                result = run_vehicle_kinematics(
                    self.drive_vehicle_params, self.dyno_results
                )
                self.drive_reference_result = result
        except (ValueError, TypeError, tk.TclError, FloatingPointError) as exc:
            messagebox.showerror(self.tr('msg_invalid'), str(exc), parent=self.drive_win)
            self.btn_skip.config(state=tk.NORMAL)
            return

        self._finish_drive_result(result)

    def drive_step(self):
        self._drive_after_id = None
        if (self.current_screen != 'drive' or not hasattr(self, 'drive_win')
                or self.drive_win is None or not self.drive_win.winfo_exists()):
            return
        if not self.dyno_results or self.dyno_params is None:
            self.show_screen('builder')
            return

        # Stejný časový krok jako autoritativní run_vehicle_kinematics().
        dt = 0.02

        rpm_arr = self.dyno_results['rpm']
        trq_arr = self.dyno_results['torque']
        max_rpm = float(rpm_arr[-1])
        max_hp_idx = int(np.argmax(self.dyno_results["hp"]))
        ideal_shift_rpm = min(
            max_rpm - 50.0,
            float(self.dyno_results["rpm"][max_hp_idx]) + 400.0
        )

        veh_params = self.drive_vehicle_params
        mass = veh_params['weight']
        cd = veh_params['cd']
        area = veh_params['area']
        r = veh_params['wheel_radius']
        speed_limiter = veh_params['speed_limiter']
        downforce_cla = veh_params['downforce_cla']
        grip = veh_params['grip']
        gear_count = veh_params['gears']
        fd = veh_params['final_drive']
        drivetrain = veh_params['drivetrain']

        ratios = get_gear_ratios(gear_count, veh_params.get('gear_ratios'))
        drivetrain_eff = {"FWD": 0.90, "RWD": 0.88, "AWD": 0.82}.get(drivetrain, 0.88)
        rho = 1.2
        g = 9.81
        wheelbase = 2.7
        cg_height = 0.5
        w_f = 0.60 if drivetrain == "FWD" else 0.50
        w_r = 1.0 - w_f

        if not self.drive_running:
            # Po dokončení měření se plyn skutečně pustí a vůz dál přirozeně
            # zpomaluje odporem vzduchu a valivým odporem. Naměřená maximálka
            # zůstává v zeleném panelu, zatímco rychloměr a otáčkoměr ukazují
            # aktuální coast-down stav.
            self.throttle_active = False
            if self.v > 0.0:
                drag = 0.5 * rho * cd * area * self.v**2
                roll = mass * g * 0.015
                coast_a = -(drag + roll) / mass
                self.v = max(0.0, self.v + coast_a * dt)

                wheel_rpm = (self.v / (2.0 * math.pi * r)) * 60.0
                coupled_rpm = wheel_rpm * ratios[self.gear] * fd
                # Při puštěném plynu otáčky následují rychlost vozu, ale motor
                # nikdy neklesne pod volnoběh. Malé vyhlazení brání cuknutí
                # ručičky v okamžiku přechodu z plného plynu do coast-downu.
                target_rpm = clamp(coupled_rpm, 1000.0, max_rpm)
                self.current_rpm += (target_rpm - self.current_rpm) * 0.18
            else:
                self.v = 0.0
                self.current_rpm += (1000.0 - self.current_rpm) * 0.18
                if abs(self.current_rpm - 1000.0) < 1.0:
                    self.current_rpm = 1000.0

            self.tacho_drive.set_rpm(self.current_rpm)
            self.lbl_speed.config(text=f"{self._speed_from_mps(self.v):.0f}")
            self._drive_after_id = self.root.after(30, self.drive_step)
            return

        self.drive_time += dt
        if self.accel_time is None and self.v > 0.1:
            self.lbl_accel.config(
                text=f"{self._acceleration_label()}: {self.drive_time:.1f} s", fg="white"
            )
        if self.accel_time is None and self.v >= self._acceleration_target_mps():
            self.accel_time = self.drive_time
            self.lbl_accel.config(
                text=f"{self._acceleration_label()}: {self.accel_time:.2f} s", fg="#00ffff"
            )

        self.max_achieved_speed = max(self.max_achieved_speed, self.v)
        a = 0.0
        self.slip_active = False
        is_shifting_now = self.shift_delay > 0.0

        if is_shifting_now:
            self.shift_delay = max(0.0, self.shift_delay - dt)
            self.current_rpm = max(1000.0, self.current_rpm - 60.0)
            drag = 0.5 * rho * cd * area * self.v**2
            roll = mass * g * 0.015
            a = -(drag + roll) / mass
        else:
            wheel_rpm = (self.v / (2.0 * math.pi * r)) * 60.0
            engine_rpm = wheel_rpm * ratios[self.gear] * fd

            peak_trq_rpm = float(rpm_arr[int(np.argmax(trq_arr))])
            # Fyzika launchu zůstává přesně shodná s run_vehicle_kinematics().
            # Startovní kolísání ručičky se přidává až později pouze jako
            # vizuální a zvukový efekt, takže neovlivní čas ani maximálku.
            launch_rpm = min(max(1800.0, peak_trq_rpm * 0.85), max_rpm * 0.75)
            clutch_slipping = self.gear == 0 and engine_rpm < launch_rpm
            calc_rpm = (
                launch_rpm
                if clutch_slipping
                else max(1000.0, engine_rpm)
            )

            if calc_rpm > ideal_shift_rpm and self.gear < gear_count - 1:
                self.gear += 1
                self.shift_delay = 0.20
                is_shifting_now = True
                drag = 0.5 * rho * cd * area * self.v**2
                roll = mass * g * 0.015
                a = -(drag + roll) / mass
            else:
                over_redline = self.gear == gear_count - 1 and engine_rpm > max_rpm
                electronically_limited = (
                    speed_limiter > 0.0 and self.v * 3.6 >= speed_limiter
                )
                if over_redline or electronically_limited:
                    force_wheel = 0.0
                    calc_rpm = min(engine_rpm, max_rpm)
                else:
                    calc_rpm = min(calc_rpm, max_rpm)
                    current_trq = float(np.interp(calc_rpm, rpm_arr, trq_arr))
                    force_wheel = (
                        current_trq * ratios[self.gear] * fd * drivetrain_eff / r
                    )

                drag = 0.5 * rho * cd * area * self.v**2
                roll = mass * g * 0.015
                aero_downforce = 0.5 * rho * downforce_cla * self.v**2
                transfer = mass * self.a_prev * cg_height / wheelbase

                if drivetrain == "FWD":
                    driven_weight = mass * g * w_f - transfer + aero_downforce * 0.40
                elif drivetrain == "RWD":
                    driven_weight = mass * g * w_r + transfer + aero_downforce * 0.60
                else:
                    driven_weight = mass * g + aero_downforce

                # Shodná trakční hranice s dávkovým výpočtem.
                max_grip_force = max(0.0, driven_weight * grip)
                if force_wheel > max_grip_force:
                    self.slip_active = True
                    force_wheel = max_grip_force
                    calc_rpm = min(max_rpm, calc_rpm + 800.0)

                # Vrácený clutch wobble: při rozjezdu ručička a zvuk jemně
                # kolísají, jako když se spojka postupně zakusuje. Výpočet síly
                # už proběhl z čistého calc_rpm, takže jde pouze o prezentaci.
                visual_rpm = calc_rpm
                if clutch_slipping:
                    engagement = clamp(engine_rpm / max(launch_rpm, 1.0), 0.0, 1.0)
                    wobble_amplitude = 165.0 * (1.0 - engagement)
                    wobble = (
                        math.sin(self.drive_time * 25.0)
                        + 0.30 * math.sin(self.drive_time * 11.0)
                    ) * wobble_amplitude
                    visual_rpm = clamp(calc_rpm + wobble, 1000.0, max_rpm)
                self.current_rpm = visual_rpm
                a = (force_wheel - drag - roll) / (mass * 1.05)

        self.a_prev = a
        self.v = max(0.0, self.v + a * dt)
        self.max_achieved_speed = max(self.max_achieved_speed, self.v)

        self.tacho_drive.set_rpm(self.current_rpm)
        self.lbl_speed.config(text=f"{self._speed_from_mps(self.v):.0f}")
        if self.shift_delay > 0.0:
            self.lbl_gear.config(text="--", fg="yellow")
        else:
            self.lbl_gear.config(text=str(self.gear + 1), fg="white")

        if self.slip_active:
            self.lbl_tcs.config(text=self.tr("ui_slip"), fg="black", bg="orange")
        else:
            self.lbl_tcs.config(text=self.tr("ui_tcs_ok"), fg="gray", bg="#222222")

        reference = self.drive_reference_result
        target_reached = (
            reference is not None
            and self.max_achieved_speed >= float(reference['top_speed']) - 0.02
        )
        physically_settled = (
            not is_shifting_now and abs(a) < 0.001 and self.v > 15.0
        )
        timed_out = self.drive_time >= 300.0

        if target_reached or physically_settled or timed_out:
            if reference is None:
                reference = run_vehicle_kinematics(
                    self.drive_vehicle_params, self.dyno_results
                )
                self.drive_reference_result = reference
            self._finish_drive_result(reference)

        self._drive_after_id = self.root.after(20, self.drive_step)

    def on_drive_close(self):
        self._cleanup_screen('drive')
        self._activate_screen('builder')

    def open_track_window(self):
        if not self.dyno_results or self.dyno_results.get('blew_up', True):
            return
        if self.current_screen == 'track' and getattr(self, 'track_win', None) is not None and self.track_win.winfo_exists():
            return
        old = self.screens.get('track')
        if old is not None and old.winfo_exists():
            old.destroy()

        self.track_win = EmbeddedScreen(self, "track", bg="#0b1017")
        self.screens["track"] = self.track_win

        # The complete track screen becomes scroll-safe only when a compact layout
        # genuinely needs more vertical room. At normal resolutions the scrollbar
        # stays hidden, just like the adaptive builder tabs.
        self.track_scroller = AutoScrollFrame(self.track_win, background="#0b1017")
        self.track_scroller.pack(fill=tk.BOTH, expand=True)
        self.track_layout = tk.Frame(self.track_scroller.content, bg="#0b1017")
        self.track_layout.pack(fill=tk.BOTH, expand=True)

        self.track_left = tk.Frame(
            self.track_layout, bg="#101720", highlightbackground="#263746", highlightthickness=1
        )
        self.track_left.grid_rowconfigure(0, weight=1)
        self.track_left.grid_columnconfigure(0, weight=1)
        self.track_canvas = tk.Canvas(
            self.track_left, width=640, height=500, bg='#0b4d20', highlightthickness=0
        )
        self.track_canvas.grid(row=0, column=0, sticky="nsew", padx=18, pady=18)
        self.track_canvas.bind("<Configure>", self._schedule_track_redraw, add="+")

        self.track_right = tk.Frame(
            self.track_layout, bg="#101720", highlightbackground="#263746", highlightthickness=1
        )
        self.track_right.grid_columnconfigure(0, weight=1)
        self.track_right.grid_columnconfigure(1, weight=1)

        self.lbl_track_status = tk.Label(
            self.track_right, text=self.tr('msg_track_ready'), font=('Arial', 14, 'bold'),
            bg='#101720', fg='#8fa5b7', wraplength=340
        )
        self.lbl_track_lap = tk.Label(
            self.track_right, text=f"{self.tr('lbl_lap_time')}: --:--.---",
            font=('Courier', 22, 'bold'), bg='#101720', fg='#43d9ff'
        )

        self.track_live_panel = tk.Frame(self.track_right, bg="#151f2a", padx=22, pady=18)
        self.lbl_track_live_speed = tk.Label(
            self.track_live_panel, text=f"{self.tr('lbl_track_speed')}: 0 {self._speed_unit_label()}",
            font=('Courier', 13), bg='#151f2a', fg='white'
        )
        self.lbl_track_live_speed.pack(pady=4)
        self.lbl_track_live_gear = tk.Label(
            self.track_live_panel, text=f"{self.tr('lbl_track_gear')}: N",
            font=('Courier', 13), bg='#151f2a', fg='white'
        )
        self.lbl_track_live_gear.pack(pady=4)
        self.lbl_track_live_sector = tk.Label(
            self.track_live_panel, text=f"{self.tr('lbl_track_sector')}: 1",
            font=('Courier', 13), bg='#151f2a', fg='white'
        )
        self.lbl_track_live_sector.pack(pady=4)

        self.lbl_track_stats = tk.Label(
            self.track_right, text=f"{self.tr('lbl_track_length')}: 3.605 km",
            justify=tk.LEFT, font=('Courier', 11), bg='#101720', fg='#8fa5b7', wraplength=330
        )
        self.lbl_track_sectors = tk.Label(
            self.track_right, text='S1: --.-- s\nS2: --.-- s\nS3: --.-- s',
            justify=tk.LEFT, font=('Courier', 11), bg='#101720', fg='white'
        )
        self.track_button_text = tk.StringVar(value=self.tr('btn_track_start'))
        self.btn_track_start = ttk.Button(
            self.track_right, textvariable=self.track_button_text, command=self.start_track_lap
        )

        self.track_running = False
        self.track_result = None
        self.track_sim_elapsed = 0.0
        self.track_last_real_time = None
        self.track_current_distance = 0.0
        self.track_canvas_points = []
        self.track_car = None

        self.track_scroller.canvas.bind("<Configure>", self._schedule_track_layout, add="+")
        self.show_screen("track")
        self.root.after_idle(self._apply_track_layout)

    def _schedule_track_layout(self, event=None):
        if self._track_layout_pending:
            return
        self._track_layout_pending = True
        self.root.after_idle(self._apply_track_layout)

    def _apply_track_layout(self):
        self._track_layout_pending = False
        if (getattr(self, 'track_win', None) is None or not self.track_win.winfo_exists()
                or not hasattr(self, 'track_layout')):
            return

        viewport_width = max(1, self.track_scroller.canvas.winfo_width())
        compact = viewport_width < 980
        self._track_compact_layout = compact

        self.track_left.grid_forget()
        self.track_right.grid_forget()
        for column in range(2):
            self.track_layout.grid_columnconfigure(column, weight=0, minsize=0)
        for row in range(2):
            self.track_layout.grid_rowconfigure(row, weight=0, minsize=0)

        if compact:
            self.track_layout.grid_columnconfigure(0, weight=1)
            self.track_layout.grid_rowconfigure(0, weight=1, minsize=380)
            self.track_layout.grid_rowconfigure(1, weight=0, minsize=260)
            self.track_left.grid(row=0, column=0, sticky="nsew", padx=0, pady=(0, 10))
            self.track_right.grid(row=1, column=0, sticky="ew", padx=0, pady=(10, 0))
            self._grid_track_information(compact=True)
        else:
            self.track_layout.grid_columnconfigure(0, weight=5, minsize=420)
            self.track_layout.grid_columnconfigure(1, weight=3, minsize=310)
            self.track_layout.grid_rowconfigure(0, weight=1, minsize=500)
            self.track_left.grid(row=0, column=0, sticky="nsew", padx=(0, 10), pady=0)
            self.track_right.grid(row=0, column=1, sticky="nsew", padx=(10, 0), pady=0)
            self._grid_track_information(compact=False)

        self.track_scroller._schedule_refresh()
        self._schedule_track_redraw()

    def _grid_track_information(self, compact=False):
        widgets = (
            self.lbl_track_status, self.lbl_track_lap, self.track_live_panel,
            self.lbl_track_stats, self.lbl_track_sectors, self.btn_track_start
        )
        for widget in widgets:
            widget.grid_forget()

        if compact:
            self.track_right.grid_columnconfigure(0, weight=1)
            self.track_right.grid_columnconfigure(1, weight=1)
            self.lbl_track_status.config(wraplength=720)
            self.lbl_track_status.grid(row=0, column=0, columnspan=2, pady=(18, 8), padx=20)
            self.lbl_track_lap.grid(row=1, column=0, columnspan=2, pady=6)
            self.track_live_panel.grid(row=2, column=0, sticky="nsew", padx=(20, 10), pady=12)
            self.lbl_track_stats.grid(row=2, column=1, sticky="w", padx=(10, 20), pady=12)
            self.lbl_track_sectors.grid(row=3, column=0, pady=(6, 20))
            self.btn_track_start.grid(row=3, column=1, pady=(6, 20))
        else:
            self.track_right.grid_columnconfigure(0, weight=1)
            self.track_right.grid_columnconfigure(1, weight=0)
            self.lbl_track_status.config(wraplength=340)
            self.lbl_track_status.grid(row=0, column=0, pady=(36, 14), padx=24)
            self.lbl_track_lap.grid(row=1, column=0, pady=8)
            self.track_live_panel.grid(row=2, column=0, sticky="ew", padx=28, pady=18)
            self.lbl_track_stats.grid(row=3, column=0, pady=10)
            self.lbl_track_sectors.grid(row=4, column=0, pady=10)
            self.btn_track_start.grid(row=5, column=0, pady=(16, 30))

    def _schedule_track_redraw(self, event=None):
        if self._track_redraw_pending:
            return
        self._track_redraw_pending = True
        self.root.after_idle(self._redraw_track_canvas)

    def _redraw_track_canvas(self):
        self._track_redraw_pending = False
        if (getattr(self, 'track_canvas', None) is None or not self.track_canvas.winfo_exists()):
            return
        width = max(1, self.track_canvas.winfo_width())
        height = max(1, self.track_canvas.winfo_height())
        if width < 120 or height < 120:
            return

        self.track_canvas_width = width
        self.track_canvas_height = height
        self.track_canvas.delete("all")
        self.track_canvas_points = self._build_track_canvas_points(TEST_TRACK_GEOMETRY['points'])
        closed = self.track_canvas_points + [self.track_canvas_points[0]]
        flat_points = [coord for point in closed for coord in point]
        smallest = min(width, height)
        outer_width = max(22, int(smallest * 0.072))
        inner_width = max(16, int(outer_width * 0.80))
        centre_width = max(1, int(smallest * 0.004))
        self.track_canvas.create_line(*flat_points, fill='#24282c', width=outer_width,
                                      smooth=False, joinstyle=tk.ROUND)
        self.track_canvas.create_line(*flat_points, fill='#676767', width=inner_width,
                                      smooth=False, joinstyle=tk.ROUND)
        self.track_canvas.create_line(*flat_points, fill='#d8d8d8', width=centre_width,
                                      smooth=False, joinstyle=tk.ROUND)

        p0 = np.asarray(self.track_canvas_points[0], dtype=float)
        p1 = np.asarray(self.track_canvas_points[1], dtype=float)
        tangent = p1 - p0
        tangent /= max(np.linalg.norm(tangent), 1e-9)
        normal = np.asarray((-tangent[1], tangent[0]))
        half_line = max(12.0, smallest * 0.030)
        start_a = p0 - normal * half_line
        start_b = p0 + normal * half_line
        self.track_canvas.create_line(start_a[0], start_a[1], start_b[0], start_b[1],
                                      fill='white', width=max(3, int(smallest * 0.009)))
        self.track_canvas.create_text(
            p0[0] + 12, p0[1] - max(18, smallest * 0.040),
            text=self.tr('ui_track_start_finish'), fill='white', font=('Arial', 9, 'bold')
        )

        if self.track_result is not None:
            x, y = self._track_map_position(self.track_current_distance)
        else:
            x, y = self.track_canvas_points[0]
        radius = max(6, int(smallest * 0.014))
        self.track_car = self.track_canvas.create_oval(
            x - radius, y - radius, x + radius, y + radius,
            fill='#00ffff', outline='white', width=2
        )

    def _format_lap_time(self, seconds):
        minutes = int(seconds // 60)
        remaining = seconds - minutes * 60
        return f"{minutes}:{remaining:06.3f}"

    def _build_track_canvas_points(self, world_points):
        """Převede fyzikální geometrii na aktuální herní plátno bez změny jejího tvaru."""
        points = np.asarray(world_points, dtype=float)
        min_xy = np.min(points, axis=0)
        max_xy = np.max(points, axis=0)
        span = np.maximum(max_xy - min_xy, 1.0)
        width = float(self.track_canvas_width)
        height = float(self.track_canvas_height)
        margin = max(24.0, min(width, height) * 0.07)
        scale = min((width - 2.0 * margin) / span[0], (height - 2.0 * margin) / span[1])
        centred = (points - (min_xy + max_xy) * 0.5) * scale
        canvas = centred + np.asarray((width * 0.5, height * 0.5))
        canvas[:, 1] = height - canvas[:, 1]
        return [tuple(point) for point in canvas]

    def _track_map_position(self, distance):
        """Interpoluje polohu přímo mezi stejnými body, které používá fyzika."""
        result = self.track_result
        distances = result['distances']
        points = np.asarray(self.track_canvas_points + [self.track_canvas_points[0]], dtype=float)
        distance = float(distance) % result['track_length']
        index = int(np.searchsorted(distances, distance, side='right') - 1)
        index = int(clamp(index, 0, len(distances) - 2))
        d0, d1 = distances[index], distances[index + 1]
        fraction = 0.0 if d1 <= d0 else (distance - d0) / (d1 - d0)
        point = points[index] + (points[index + 1] - points[index]) * fraction
        return float(point[0]), float(point[1])

    def start_track_lap(self):
        if self.track_running:
            return
        if not self.dyno_results or self.dyno_params is None:
            self.show_screen('builder')
            return
        try:
            veh_params = self.build_vehicle_params()
            self.track_result = run_track_simulation(veh_params, self.dyno_results)
        except (ValueError, TypeError, tk.TclError, FloatingPointError) as exc:
            messagebox.showerror(self.tr('msg_invalid'), str(exc), parent=self.track_win)
            return

        if not self.track_canvas_points:
            self._redraw_track_canvas()
        self.track_running = True
        self.track_sim_elapsed = 0.0
        self.track_current_distance = 0.0
        self.track_last_real_time = time.perf_counter()
        self.track_playback_rate = max(1.0, self.track_result['lap_time'] / 10.0)
        self.lbl_track_status.config(text=self.tr('msg_track_running'), fg='#ffcc55')
        self.lbl_track_lap.config(text=f"{self.tr('lbl_lap_time')}: 0:00.000")
        self.lbl_track_sectors.config(text='S1: --.-- s\nS2: --.-- s\nS3: --.-- s')
        self.btn_track_start.config(state=tk.DISABLED)
        self._track_after_id = self.root.after(30, self.track_tick)

    def track_tick(self):
        self._track_after_id = None
        if (self.current_screen != 'track' or not self.track_running or not hasattr(self, 'track_win')
                or self.track_win is None or not self.track_win.winfo_exists()):
            return
        now = time.perf_counter()
        real_dt = max(0.0, now - self.track_last_real_time)
        self.track_last_real_time = now
        self.track_sim_elapsed += real_dt * self.track_playback_rate
        lap_time = self.track_result['lap_time']
        shown_time = min(self.track_sim_elapsed, lap_time)

        cumulative = self.track_result['cumulative_time']
        index = int(np.searchsorted(cumulative, shown_time, side='right') - 1)
        index = int(clamp(index, 0, len(cumulative) - 2))
        t0, t1 = cumulative[index], cumulative[index + 1]
        fraction = 0.0 if t1 <= t0 else (shown_time - t0) / (t1 - t0)
        distances = self.track_result['distances']
        distance = distances[index] + (distances[index + 1] - distances[index]) * fraction
        self.track_current_distance = float(distance)
        x, y = self._track_map_position(distance)
        self.track_canvas.coords(self.track_car, x - 7, y - 7, x + 7, y + 7)

        speed = self._speed_from_mps(float(self.track_result['speed_profile'][index]))
        gear = int(self.track_result['gear_profile'][index]) + 1
        sector = int(self.track_result['sector_profile'][index])
        self.lbl_track_lap.config(text=f"{self.tr('lbl_lap_time')}: {self._format_lap_time(shown_time)}")
        self.lbl_track_live_speed.config(text=f"{self.tr('lbl_track_speed')}: {speed:.0f} {self._speed_unit_label()}")
        self.lbl_track_live_gear.config(text=f"{self.tr('lbl_track_gear')}: {gear}")
        self.lbl_track_live_sector.config(text=f"{self.tr('lbl_track_sector')}: {sector}")

        if self.track_sim_elapsed < lap_time:
            self._track_after_id = self.root.after(30, self.track_tick)
            return

        self.track_running = False
        sectors = self.track_result['sector_times']
        self.lbl_track_status.config(text=self.tr('msg_track_finished'), fg='lime')
        self.lbl_track_lap.config(text=f"{self.tr('lbl_lap_time')}: {self._format_lap_time(lap_time)}")
        self.lbl_track_stats.config(
            text=(f"{self.tr('lbl_track_length')}: {self.track_result['track_length'] / 1000.0:.3f} km\n"
                  f"{self.tr('lbl_track_avg')}: {self._speed_from_mps(self.track_result['average_speed']):.1f} {self._speed_unit_label()}\n"
                  f"{self.tr('lbl_track_max')}: {self._speed_from_mps(self.track_result['max_speed']):.1f} {self._speed_unit_label()}")
        )
        self.lbl_track_sectors.config(text=f"S1: {sectors[0]:.3f} s\nS2: {sectors[1]:.3f} s\nS3: {sectors[2]:.3f} s")
        self.btn_track_start.config(state=tk.NORMAL)
        self.track_button_text.set(self.tr('btn_track_retry'))

    def on_track_close(self):
        self._cleanup_screen('track')
        self._activate_screen('builder')

    def start_audio_stream(self, is_drive=False):
        if not SOUND_AVAILABLE:
            self.stream = None
            return
        cylinders = int(self.dyno_params['cylinders'])
        aspiration = self.dyno_params['aspiration']
        crank = self.dyno_params['crank']
        fs = 44100 
        
        def audio_callback(outdata, frames, time_info, status):
            if not is_drive and getattr(self, 'engine_blown', False):
                steam = np.random.normal(0, 0.8, frames) * max(0, 1.0 - getattr(self, 'blow_timer', 0)/2.0)
                outdata[:, 0] = steam * 0.5
                return

            rpm = getattr(self, 'current_rpm', 1000.0)
            
            if is_drive:
                throttle_load = 1.0 if self.throttle_active and self.shift_delay <= 0 else 0.0
            else:
                throttle_load = 1.0 if self.throttle_active else 0.0
                
            if throttle_load == 0.0 and getattr(self, 'last_throttle', False) and rpm > 3000 and aspiration == "Turbo":
                self.flutter_intensity = 1.0 
            self.last_throttle = throttle_load > 0.0
            
            freq = (rpm / 60.0) * (cylinders / 2.0)
            d_phase = 2.0 * np.pi * freq / fs
            phases = getattr(self, 'audio_phase', 0.0) + np.arange(1, frames + 1) * d_phase
            self.audio_phase = phases[-1]
            
            rev_freq = rpm / 60.0
            d_rev_phase = 2.0 * np.pi * rev_freq / fs
            rev_phases = getattr(self, 'rev_phase', 0.0) + np.arange(1, frames + 1) * d_rev_phase
            self.rev_phase = rev_phases[-1]
            
            d_flut = 2.0 * np.pi * 7.5 / fs
            flut_phases = getattr(self, 'flutter_phase', 0.0) + np.arange(1, frames + 1) * d_flut
            self.flutter_phase = flut_phases[-1]
            
            wave_data = generate_audio_frame(
                phases, rev_phases, cylinders, aspiration, rpm, 
                throttle_load, getattr(self, 'flutter_intensity', 0.0), flut_phases, crank
            )
            outdata[:, 0] = wave_data
            if hasattr(self, 'flutter_intensity'): self.flutter_intensity *= 0.93 
            
        try:
            self.stream = sd.OutputStream(samplerate=fs, channels=1, callback=audio_callback, blocksize=2048)
            self.stream.start()
        except Exception as e:
            self.root.after(0, self._write_log, f"Chyba při startu zvuku: {e}")

    def stop_audio_stream(self):
        stream = getattr(self, 'stream', None)
        if stream is None:
            return
        try:
            if stream.active:
                stream.stop()
            stream.close()
        except Exception:
            pass
        finally:
            self.stream = None

if __name__ == "__main__":
    root = tk.Tk()
    app = EngineApp(root)
    root.mainloop()