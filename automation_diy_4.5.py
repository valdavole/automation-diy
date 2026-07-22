import time
import sys
import os
import platform
import threading
import math
import wave
import numpy as np
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import json

is_windows = platform.system() == "Windows"
if is_windows:
    import winsound

SOUND_AVAILABLE = False
try:
    import sounddevice as sd
    SOUND_AVAILABLE = True
except (ImportError, OSError):
    pass

# --- LOKALIZAČNÍ SLOVNÍK (CZ / EN) ---
T = {
    "cz": {
        "app_title": "Automation DIY - Verze 4.5 (Aero & Dynamics Update)",
        "menu_file": "Soubor",
        "menu_load": "Načíst motor (.json)...",
        "menu_save": "Uložit motor jako (.json)...",
        "menu_quit": "Ukončit",
        "lbl_engine_name": "Název vozu/motoru:",
        "tab_1": "1. Block", "tab_2": "2. Bottom End", "tab_3": "3. Top End",
        "tab_4": "4. Aspiration", "tab_5": "5. Fuel & Tune", "tab_6": "6. Exhaust", "tab_7": "7. Drivetrain",
        
        "lbl_config": "Konfigurace:", "lbl_vangle": "Úhel V:", "lbl_cyl": "Počet válců:", "lbl_block": "Materiál bloku:",
        "lbl_bore": "Vrtání (Bore):", "lbl_stroke": "Zdvih (Stroke):", "lbl_rad": "Účinnost chladiče:", "lbl_tech": "Technologická úroveň:", "lbl_calc_disp": "Vypočítaný objem:",
        "tt_config": "Inline (Řadový): Levný, plynulý chod, ale u mnoha válců je moc dlouhý.\nV (Vidlicový): Kompaktní, krátký, skvělý pro 6 a 8 válců.\nBoxer (Plochý): Protiběžné písty. Dokonalé vyvážení a nízké těžiště.",
        "tt_vangle": "60°: Vhodný pro V6, motor je užší.\n90°: Klasika pro V8, skvělé vyvážení rotujících hmot.\n120°: Velmi plochý motor, snižuje těžiště, ale je extrémně široký.",
        "tt_cyl": "3 až 5: Levnější, vhodné pro malé objemy.\n6 až 8: Výkonný standard, kultivovaný chod.\n10 až 16: Exotické superauta. Obrovský výkon a spotřeba.",
        "tt_block": "Cast Iron: Těžká, nezničitelná.\nAluminium (Light/Heavy/Billet): Hliník je standard. Heavy je pevnější, Light lehčí. Billet je frézovaný z jednoho kusu pro závodní nasazení.\nAlSi (Light/Heavy): Slitina bez vložek, snižuje tření.\nMagnesium: Motorsport, nejlehčí, nejnižší tření.",
        "tt_bore": "Určuje průměr pístu.\nVětší vrtání = umožňuje instalaci větších ventilů pro lepší průtok vzduchu ve vysokých otáčkách.",
        "tt_stroke": "Určuje vzdálenost, kterou píst urazí.\nVětší zdvih = masivní nárůst točivého momentu v nízkých otáčkách, ale fyzicky brání motoru dosáhnout vysokých RPM.",
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

        "lbl_asp": "Typ plnění:", "lbl_tb": "Ložiska turba:", "lbl_tc": "Konfigurace:", "lbl_ic": "Velikost Intercooleru:",
        "lbl_tsize": "Velikost Turba:", "lbl_tboost": "Tlak (Boost):", "lbl_sct": "Typ kompresoru:", "lbl_scp": "Tlak (Max Boost):",
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
        "lbl_ign": "Předstih (Ignition):", "lbl_lim": "Omezovač RPM:",
        "lbl_carb_size": "Velikost klapky/karb.:", "lbl_fuel_map": "Mapa paliva (Směs):", "lbl_man_size": "Velikost sání:",
        "tt_fdeliv": "Carburetor: Klasika, horší odpařování (klepání).\nMechanical Injection: Závodní, obří spotřeba.\nSingle Point EFI: Základní stříkačka (1 tryska).\nEFI Multi: Moderní nepřímý vstřik.\nDirect Injection: Chladí válce zevnitř, brutálně brání detonacím.",
        "tt_inconf": "Single: Úsporné.\nTwin: Dvě klapky.\nITB (Nezávislé klapky): Šílená odezva a brutální výkon nahoře.",
        "tt_man": "Standard (Low/Mid): Vyvážené. Low je na spodek.\nPerformance (Mid/High): Větší průtok, High posouvá výkon nahoru.\nRace: Závodní nahoře.\nCompact: Vejdou se všude, ale dusí.\nVariable: Zvětšuje celkové spektrum otáček.",
        "tt_fuel": "Odolnost proti klepání. Low Quality 85/Regular 91: Hrozné palivo. Premium 95/Super 98: Standard. Ultimate 100/E85/Methanol: Pro velká turba. Nitromethane: Absolutní šílenost, masivní výkon. Diesel: Nikdy nezdetonuje.",
        "tt_afr": "14.7 = Dokonalé spalování.\n12.5 - 13.0 = Bohatá směs, největší výkon.\n15+ = Chudá směs. Spotřeba padá, ale drasticky ROSTE RIZIKO DETONACÍ.",
        "tt_ign": "Víc předstihu = vyšší výkon.\nAle bacha: Agresivní předstih u vysoké komprese rychle roztaví písty (Klepání).\nIgnorováno u Dieselu.",
        "tt_lim": "NIKDY nedávej výš, než co vydrží tvé ojnice, jinak motor vybuchne!",
        "tt_carb_size": "Určuje velikost karburátoru nebo škrtící klapky. Menší (0-40) pomáhá průtoku a krouťáku v nízkých otáčkách. Větší (60-100) je nutný pro vysoké otáčky, aby se motor nezadusil.",
        "tt_man_size": "Šířka sacích kanálů. Malá přidává tah dole, velká odemyká vysoké otáčky, ale zhorší odezvu plynu v nízkých.",
        "tt_fuel_map": "Nastavení palivové mapy. 0-40 (Lean): Snižuje spotřebu, ale rapidně roste riziko klepání a klesá výkon. 60-100 (Rich): Více paliva chladí válec a mírně zvedne výkon.",

        "lbl_arch": "Architektura:", "lbl_head_exh": "Svody (Headers):", "lbl_diam": "Průměr potrubí:", "lbl_cat": "Katalyzátor:",
        "lbl_muf1": "Tlumič 1:", "lbl_muf2": "Tlumič 2:", "lbl_head_size": "Velikost svodů:", "lbl_bypass": "Výfuk. klapky:",
        "tt_arch": "Dual efektivně ohromně zvětšuje celkový průřez výfuku.",
        "tt_head_exh": "Compact Cast: Obrovská restrikce.\nCast (Low/Mid/Std): Litina, brzdí výkon.\nTubular (Std/Mid/Long/Race): Plynulý odvod plynů. Long/Race dají max výkon u omezovače, ale uberou spodek.",
        "tt_diam": "Pokud máš 1000 koní a průměr odtoku jako z umyvadla (25mm), motor se zadusí a křivka spadne.",
        "tt_cat": "None: Žádný restriktor.\n2-way/3-way/Reactor: Různé typy keramik, které dusí výkon.\nHigh Flow (s Pre-Cat): Sportovní propustnější katalyzátory, minimální ztráta výkonu.",
        "tt_muf": "None (Rovná roura): Žádná restrikce.\nStraight: Dobrý průtok.\nBaffled: Plyny kličkují = ztráta výkonu.\nReverse Flow: Nejtišší, ale největší dusítko.",
        "tt_head_size": "Průměr svodového potrubí. Velký pomáhá extrémním výkonům, malý pomáhá rychlosti výfukových plynů pro lepší krouťák dole.",
        "tt_bypass": "No Valves: Výfuk jde vždy přes tlumiče.\nBypass Valves: Klapky se v 3500 RPM otevřou a zcela obejdou tlumiče, čímž uvolní maximální výkon za cenu hluku.",

        "lbl_veh": "Předvolba vozu:", "lbl_weight": "Váha:", "lbl_cd": "Odpor vzduchu (Cd):", "lbl_grip": "Trakce (Tire Grip):",
        "lbl_gears": "Počet převodů:", "lbl_fd": "Stálý převod:", "lbl_drive": "Pohon nápravy:",
        "tt_veh": "Přednastaví hodnoty šasi podle typických zástupců daných kategorií.\nUšetří ti čas při testování různých motorů v různých typech aut.",
        "tt_weight": "Celková hmotnost vozu s řidičem a náplněmi.\nZásadní parametr pro zrychlení z místa podle Newtonova druhého zákona (F=m*a).",
        "tt_cd": "Koeficient aerodynamického odporu.\nKlíčový pro maximální rychlost. Běžná auta mají kolem 0.30, supersporty méně.",
        "tt_grip": "Přilnavost pneumatik (koeficient smykového tření).\nOmezuje maximální tažnou sílu na kolech, než se začnou protáčet.",
        "tt_gears": "Počet rychlostních stupňů v převodovce.\nVíc rychlostí udrží motor déle v ideálním spektru otáček.",
        "tt_fd": "Stálý převod na hnané nápravě (diferenciál).\nVětší číslo = kratší kvalty, lepší zrychlení, ale nižší maximálka a víc řazení.",
        "tt_drive": "FWD: Náhon na přední. Ztrácí trakci při zrychlení.\nRWD: Náhon na zadní. Trakce roste při zrychlení.\nAWD: Náhon na všechna kola. Maximální využití váhy pro trakci.",

        "btn_dyno": "1. Dyno Pull", "btn_graph": "Graf", "btn_rev": "2. Ruční plyn", "btn_drive": "3. Zkušební Jízda", "btn_no_snd": "Zvuk Nedostupný",
        "msg_dyno_hdr": "--- DYNO PULL (Měření výkonu):", "msg_rpm": "Otáčky", "msg_trq": "Točák", "msg_hp": "Výkon",
        "msg_done": "\nHotovo!", "msg_blown": "💥 ZNIČENO!", "msg_fix": "🔧 JAK TO OPRAVIT:", 
        "msg_max_hp": "Max Výkon:", "msg_max_trq": "Max Moment:", "msg_ready": "-> Připraveno na Zkušební jízdu!",

        "win_rev_title": "Telemetrie (Ruční plyn a Chlazení)", "lbl_coolant": "Teplota kapaliny:", "btn_pedal": "PLYNOVÝ PEDÁL (Držet stisknuté)",
        "msg_hg_blown": "💥 PRASKLÉ TĚSNĚNÍ POD HLAVOU! 💥",
        "win_drv_title": "Zkušební Jízda (0 - Max)", "btn_launch": "START LAUNCH", "btn_skip": "PŘESKOČIT NA MAX",
        "btn_retry": "NOVÝ POKUS", "btn_accel": "ZRYCHLUJEME...", "msg_not_reached": "Nedosaženo"
    },
    "en": {
        "app_title": "Automation DIY - Version 4.5 (Aero & Dynamics Update)",
        "menu_file": "File",
        "menu_load": "Load Engine (.json)...",
        "menu_save": "Save Engine As (.json)...",
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
        "tt_stroke": "Determines the distance the piston travels.\nLarger stroke = massive increase in low-end torque, but physically limits the engine from reaching high RPM.",
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
        "tt_lim": "NEVER set higher than what your conrods can handle, otherwise the engine will explode!",
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
        "lbl_gears": "Gears:", "lbl_fd": "Final Drive:", "lbl_drive": "Drivetrain:",
        "tt_veh": "Pre-sets chassis values according to typical representatives of the given categories.\nSaves you time when testing different engines in different types of cars.",
        "tt_weight": "Total weight of the vehicle with driver and fluids.\nCrucial parameter for acceleration from a standstill according to Newton's second law (F=m*a).",
        "tt_cd": "Aerodynamic drag coefficient.\nKey for top speed. Normal cars have around 0.30, supercars less.",
        "tt_grip": "Tire grip (coefficient of sliding friction).\nLimits the maximum pulling force on the wheels before they start spinning.",
        "tt_gears": "Number of gears in the transmission.\nMore gears keep the engine longer in the ideal RPM spectrum.",
        "tt_fd": "Final drive ratio on the driven axle (differential).\nHigher number = shorter gears, better acceleration, but lower top speed and more shifting.",
        "tt_drive": "FWD: Front-Wheel Drive. Loses traction under acceleration.\nRWD: Rear-Wheel Drive. Traction increases under acceleration.\nAWD: All-Wheel Drive. Maximum use of weight for traction.",

        "btn_dyno": "1. Dyno Pull", "btn_graph": "Show Graph", "btn_rev": "2. Manual Throttle", "btn_drive": "3. Test Drive", "btn_no_snd": "Sound N/A",
        "msg_dyno_hdr": "--- DYNO PULL:", "msg_rpm": "RPM", "msg_trq": "Torque", "msg_hp": "Power",
        "msg_done": "\nDone!", "msg_blown": "💥 DESTROYED!", "msg_fix": "🔧 HOW TO FIX:", 
        "msg_max_hp": "Max Power:", "msg_max_trq": "Max Torque:", "msg_ready": "-> Ready for Test Drive!",

        "win_rev_title": "Telemetry (Throttle & Cooling)", "lbl_coolant": "Coolant Temp:", "btn_pedal": "THROTTLE PEDAL (Hold)",
        "msg_hg_blown": "💥 BLOWN HEAD GASKET! 💥",
        "win_drv_title": "Test Drive (0 - Max)", "btn_launch": "START LAUNCH", "btn_skip": "SKIP TO TOP SPEED",
        "btn_retry": "RETRY LAUNCH", "btn_accel": "ACCELERATING...", "msg_not_reached": "Not Reached"
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
    t_samples = np.linspace(0, total_time, num_samples)
    t_rpms = np.linspace(0, total_time, num_steps)
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
def run_engine_simulation(params):
    lang = params.get('lang', 'cz')
    tech_level = params.get('tech_level', 100)
    tech_factor = tech_level / 100.0
    b = params.get('bore', 87.5)
    s = params.get('stroke', 83.1)
    c = params.get('cylinders', 4)
    disp_cc = math.pi * ((b/20)**2) * (s/10) * c
    
    rpm_limit = params.get('rpm_limit', 6500)
    blow_up = False
    blow_up_reason = ""
    blow_up_fix = ""
    
    # 1. Integrace Balanceru (Zvyšuje mechanický limit, ale ovlivní tření)
    bal = params.get('balancer', 'None')
    bal_mass = params.get('balancer_mass', 0.0)
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

    rpm_range = np.arange(1000, actual_limit + 100, 100)
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
            peak_rpm = 1900 + (c_prof * 15) + ((valves - 2) * 150) + (man_shift * 0.3)
            left_spread = 1200 + (c_prof * 10)
            right_spread = 2500 + (c_prof * 20)
            if vvt == "Intake": right_spread *= 1.15
            elif vvt == "All": right_spread *= 1.25
            
            # Plynulý základ 45 % pro naftu (běží bez škrtící klapky, nasává víc vzduchu)
            left_side = 0.45 + 0.55 * np.exp(-0.5 * ((rpm_range - peak_rpm) / left_spread)**2)
            right_side = 0.45 + 0.55 * np.exp(-0.5 * ((rpm_range - peak_rpm) / right_spread)**2)
            return np.where(rpm_range < peak_rpm, left_side, right_side)
        else:
            peak_rpm = 3000 + (c_prof * 45) + ((valves - 2) * 500) + man_shift + vt_shift
            spread = 1500 + (c_prof * 15)
            if vvt == "Intake": spread *= 1.25
            elif vvt == "All": spread *= 1.5
            if "Variable" in man: spread *= 1.15
            
            # Plynulý základ 35 % pro benzín
            return 0.35 + 0.65 * np.exp(-0.5 * ((rpm_range - peak_rpm) / spread)**2)

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
    speed_choke = np.where(piston_speed > 22.0, np.exp(-(piston_speed - 22.0) * 0.1), 1.0)
    ve_curve *= speed_choke
    
    if is_diesel:
        diesel_choke = np.exp(-0.5 * (np.maximum(0, rpm_range - 4200) / 800)**2)
        ve_curve *= diesel_choke

    ve_curve *= (1.0 + (carb_sz + man_sz) * 0.05 * (rpm_range / max(rpm_range)))

    vt_base = {"Pushrod (OHV)": 4500, "SOHC": 6000, "DOHC": 7500, "DAOHC": 8500}.get(valvetrain, 6000)
    springs = params.get('springs', 50)
    valve_float_lim = vt_base + (springs * 40)
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
        
        # 5. Integrace Turbo Config (Víc menších turb znamená mnohem menší lag)
        lag_rpm = 2000 + (turb_size * 20) + (ic_size * 4)
        t_conf = params.get('turbo_config', 'Single')
        if t_conf == "Twin": lag_rpm -= 400
        elif t_conf == "Quad": lag_rpm -= 800
            
        if params.get('turbo_bearing', 'Journal') == "Ball Bearings": lag_rpm -= 500
        ic_eff = 0.6 + (ic_size / 250.0) 
        actual_boost = active_boost * ic_eff
        
        # OPRAVA: Plynulý náběh turba (Sigmoid) místo ostrého matematického zlomu
        spool_smoothness = 200.0  # Hodnota, která určuje, jak pozvolna se turbo roztáčí
        boost_curve = 1.0 + (actual_boost * 1.10 * (1 / (1 + np.exp(-(rpm_range - lag_rpm) / spool_smoothness))))
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
    req_diam = math.sqrt(np.max(torque) / 2) * 2.5 
    if exh_diam < req_diam:
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

    hp = (torque * rpm_range) / 7021.5
    
    return {
        "rpm": rpm_range, 
        "torque": torque, 
        "hp": hp, 
        "blew_up": blow_up, 
        "reason": blow_up_reason, 
        "fix": blow_up_fix
    }

def run_vehicle_kinematics(veh_params, engine_data):
    dt = 0.02
    rpm_arr = engine_data['rpm']
    trq_arr = engine_data['torque']
    max_rpm = rpm_arr[-1]
    max_hp_idx = np.argmax(engine_data["hp"])
    max_hp_rpm = engine_data["rpm"][max_hp_idx]
    ideal_shift_rpm = min(max_rpm - 50, max_hp_rpm + 400)
    
    mass = veh_params.get('weight', 1350.0)
    cd = veh_params.get('cd', 0.30)
    grip = veh_params.get('grip', 0.9)
    gear_count = veh_params.get('gears', 5)
    fd = veh_params.get('final_drive', 4.1)
    drivetrain = veh_params.get('drivetrain', 'FWD')

    if gear_count <= 4: ratios = [2.8, 1.5, 1.0, 0.8]
    elif gear_count == 5: ratios = [3.3, 1.9, 1.3, 1.0, 0.8]
    elif gear_count == 6: ratios = [3.5, 2.0, 1.4, 1.0, 0.8, 0.6]
    else: ratios = [4.0, 2.5, 1.7, 1.2, 0.9, 0.7, 0.55, 0.45][:gear_count]

    r = 0.33 
    area = 2.2 
    rho = 1.2 
    g = 9.81
    wheelbase = 2.7
    cg_height = 0.5
    w_f = 0.6 if drivetrain == "FWD" else 0.5
    w_r = 0.4 if drivetrain == "FWD" else 0.5
    
    sim_v = 0.0
    sim_gear = 0
    sim_time = 0.0
    sim_time_100 = None
    sim_shift_delay = 0.0
    sim_a_prev = 0.0
    sim_max_v = 0.0
    
    max_sim_steps = int(300 / dt)
    
    for step in range(max_sim_steps):
        sim_time += dt
        a = 0.0
        is_shifting_now = False
        
        if sim_v > sim_max_v:
            sim_max_v = sim_v
            
        if sim_time_100 is None and sim_v * 3.6 >= 100.0:
            sim_time_100 = sim_time
            
        if sim_shift_delay > 0:
            sim_shift_delay -= dt
            is_shifting_now = True

        if is_shifting_now:
            a = (-0.5 * rho * cd * area * sim_v**2 - mass * g * 0.015) / mass
        else:
            wheel_rpm = (sim_v / (2 * math.pi * r)) * 60
            engine_rpm = wheel_rpm * ratios[sim_gear] * fd
            
            # Najdeme, v jakých otáčkách má motor maximální krouticí moment
            max_trq_idx = np.argmax(trq_arr)
            peak_trq_rpm = rpm_arr[max_trq_idx]
            
            # Ideální start (Launch Control) je zhruba na 85 % maxima krouťáku.
            # Omezíme to zespodu na 2500 RPM a shora nesmí překročit 75 % červeného pole.
            launch_rpm = min(max(2500.0, peak_trq_rpm * 0.85), max_rpm * 0.75)
            if sim_gear == 0 and engine_rpm < launch_rpm:
                calc_rpm = launch_rpm
            else:
                calc_rpm = max(1000.0, engine_rpm)
            
            if calc_rpm > ideal_shift_rpm:
                if sim_gear < gear_count - 1:
                    sim_gear += 1
                    sim_shift_delay = 0.20 
                    is_shifting_now = True
                    a = (-0.5 * rho * cd * area * sim_v**2 - mass * g * 0.015) / mass
                else:
                    calc_rpm = max_rpm
            
            if not is_shifting_now:
                current_trq = np.interp(calc_rpm, rpm_arr, trq_arr)
                force_wheel = (current_trq * ratios[sim_gear] * fd * 0.86) / r
                
                # 1. Vypočítáme aerodynamický odpor dřív, abychom z něj určili přítlak
                drag = 0.5 * rho * cd * area * sim_v**2
                roll = mass * g * 0.015
                
                # 2. Simulace přítlaku (Downforce). Reálný přítlak dělá funkční aero paket
                # (křídla, difuzor, spoiler) - ne odpor vzduchu (Cd) samotný, ten o přítomnosti
                # aera nic neříká (hranaté auto s vysokým Cd nemá přítlak o nic víc než áčko).
                # Jako proxy bereme grip pneumatik - u aut v presetech roste právě se sportovním/
                # závodním laděním. Běžné auto (grip <= 1.0) tak nemá žádný umělý přítlak,
                # závodně laděné auto ho má, ale v reálných, ne přehnaných hodnotách.
                aero_factor = max(0.0, min(1.0, (grip - 1.0) / 0.5))
                aero_downforce = drag * aero_factor * 0.8
                
                # 3. Rozložení umělé váhy na nápravy vč. aerodynamiky
                transfer = (mass * sim_a_prev * cg_height) / wheelbase
                
                if drivetrain == "FWD": 
                    driven_weight = (mass * g * w_f) - transfer + (aero_downforce * 0.4)
                elif drivetrain == "RWD": 
                    driven_weight = (mass * g * w_r) + transfer + (aero_downforce * 0.6)
                else: 
                    driven_weight = mass * g + aero_downforce
                    
                driven_weight = max(driven_weight, mass * g * 0.1)
                max_grip_force = driven_weight * grip
                
                # --- OPRAVA: Oříznutí hrubé síly motoru na fyzický limit pneumatik ---
                force_wheel = min(force_wheel, max_grip_force)
                    
                # Zbytek výpočtu zrychlení (drag a roll už máš spočítané nahoře)
                net_force = force_wheel - drag - roll
                a = net_force / (mass * 1.05)
                
        sim_a_prev = a
        sim_v += a * dt
        sim_v = max(sim_v, 0.0)
        
        if not is_shifting_now and a < 0.001 and sim_v > 15.0:
            break
            
    return {
        "time_0_100": sim_time_100,
        "top_speed": sim_max_v,
        "final_gear": sim_gear
    }

class ToolTip(object):
    def __init__(self, widget, text_var):
        self.widget = widget
        self.text_var = text_var
        self.tipwindow = None
        self.id = None
        self.widget.bind("<Enter>", self.enter)
        self.widget.bind("<Leave>", self.leave)

    def enter(self, event=None):
        self.schedule()

    def leave(self, event=None):
        self.unschedule()
        self.hidetip()

    def schedule(self):
        self.unschedule()
        self.id = self.widget.after(500, self.showtip)

    def unschedule(self):
        id = self.id
        self.id = None
        if id: self.widget.after_cancel(id)

    def showtip(self, event=None):
        x, y, cx, cy = self.widget.bbox("insert")
        x += self.widget.winfo_rootx() + 25
        y += self.widget.winfo_rooty() + 25
        self.tipwindow = tw = tk.Toplevel(self.widget)
        tw.wm_overrideredirect(1)
        tw.wm_geometry(f"+{x}+{y}")
        txt = self.text_var.get() if isinstance(self.text_var, tk.StringVar) else self.text_var
        label = tk.Label(tw, text=txt, justify=tk.LEFT,
                         background="#ffffe0", relief=tk.SOLID, borderwidth=1,
                         font=("tahoma", "9", "normal"), padx=5, pady=5)
        label.pack(ipadx=4, ipady=2)

    def hidetip(self):
        tw = self.tipwindow
        self.tipwindow = None
        if tw: tw.destroy()

# --- HLAVNÍ APLIKACE (GUI) ---
class EngineApp:
    def __init__(self, root):
        self.root = root
        self.vars = {}
        self.vars['app_lang'] = tk.StringVar(value='cz')
        
        self.lang_vars = {k: tk.StringVar(value=v) for k, v in T['cz'].items()}
        
        self.root.title(self.lang_vars['app_title'].get())
        self.root.geometry("750x750")
        
        self.setup_master_presets()
        self.create_variables()
        self.snapshot_factory_defaults()
        self.create_menu()
        
        self.create_language_selector()
        self.create_widgets()
        
        self.dyno_results = {}
        self.update_displacement()
        self.update_dynamic_ui()

    def tr(self, key):
        return self.lang_vars.get(key, tk.StringVar(value="")).get()

    def apply_language(self):
        lang = self.vars['app_lang'].get()
        for k, v in T[lang].items():
            if k in self.lang_vars:
                self.lang_vars[k].set(v)
        
        self.root.title(self.lang_vars['app_title'].get())
        self.filemenu.entryconfigure(0, label=self.tr("menu_load"))
        self.filemenu.entryconfigure(1, label=self.tr("menu_save"))
        self.filemenu.entryconfigure(3, label=self.tr("menu_quit"))
        self.menubar.entryconfigure(1, label=self.tr("menu_file"))

        for i, tab_key in enumerate(['tab_1', 'tab_2', 'tab_3', 'tab_4', 'tab_5', 'tab_6', 'tab_7']):
            self.notebook.tab(i, text=self.tr(tab_key))

    def setup_master_presets(self):
        self.master_presets = {
            "Sériová Mazda LF-DE 2.0": {
                'config': "Inline", 'cylinders': 4, 'v_angle': 90, 'block_mat': "Aluminium",
                'bore': 87.5, 'stroke': 83.1, 'radiator': 50,
                'crank': "Cast", 'conrods': "Heavy Duty", 'pistons': "Cast", 'balancer': "None",
                'head_mat': "Aluminium", 'valvetrain': "DOHC", 'valves': 4, 'vvt': "None", 'vvl': False, 'cam_profile': 25, 'comp_ratio': 10.0,
                'aspiration': "NA", 'turbo_bearing': "Journal", 'turbo_config': "Single", 'intercooler': 50, 'turb_size': 50, 'boost': 0.5, 'sc_type': "Roots", 'comp_size': 50, 'sc_pulley': 0.8,
                'fuel_deliv': "EFI Multi", 'intake_conf': "Single", 'manifold': "Standard", 'fuel_type': "Premium 95", 'afr': 14.7, 'ignition': 30, 'rpm_limit': 6500,
                'exh_arch': "Single", 'headers': "Cast", 'exh_diam': 44.0, 'cat': "3-way", 'muffler1': "Baffled", 'muffler2': "Baffled",
                'veh_preset': "Mazda 6 (2002)", 'veh_weight': 1350.0, 'veh_cd': 0.30, 'tire_grip': 0.9, 'gears': 5, 'final_drive': 4.9, 'drivetrain': "FWD",
                'tech_level': 98
            },
            "Škoda Octavia 1.9 TDI": {
                'config': "Inline", 'cylinders': 4, 'v_angle': 90, 'block_mat': "Cast Iron",
                'bore': 79.5, 'stroke': 95.5, 'radiator': 40,
                'crank': "Forged", 'conrods': "Heavy Duty", 'pistons': "Heavy Duty", 'balancer': "None",
                'head_mat': "Aluminium", 'valvetrain': "SOHC", 'valves': 2, 'vvt': "None", 'vvl': False, 'cam_profile': 0, 'comp_ratio': 17.0,
                'aspiration': "Turbo", 'turbo_bearing': "Journal", 'turbo_config': "Single", 'intercooler': 30, 'turb_size': 20, 'boost': 0.7, 'sc_type': "Roots", 'comp_size': 50, 'sc_pulley': 0.8,
                'fuel_deliv': "Direct Injection", 'intake_conf': "Single", 'manifold': "Standard", 'fuel_type': "Diesel", 'afr': 17.0, 'ignition': 15, 'rpm_limit': 4500,
                'exh_arch': "Single", 'headers': "Cast", 'exh_diam': 45.0, 'cat': "3-way", 'muffler1': "Baffled", 'muffler2': "Baffled",
                'veh_preset': "Vlastní (Custom)", 'veh_weight': 1350.0, 'veh_cd': 0.31, 'tire_grip': 0.8, 'gears': 5, 'final_drive': 3.1, 'drivetrain': "FWD",
                'tech_level': 82
            },
            "BMW M3 E46 (S54B32)": {
                'config': "Inline", 'cylinders': 6, 'v_angle': 90, 'block_mat': "Cast Iron",
                'bore': 87.0, 'stroke': 91.0, 'radiator': 70,
                'crank': "Forged", 'conrods': "Forged", 'pistons': "Forged", 'balancer': "Harmonic Damper",
                'head_mat': "Aluminium", 'valvetrain': "DOHC", 'valves': 4, 'vvt': "All", 'vvl': False, 'cam_profile': 55, 'comp_ratio': 11.5,
                'aspiration': "NA", 'turbo_bearing': "Journal", 'turbo_config': "Single", 'intercooler': 50, 'turb_size': 50, 'boost': 0.5, 'sc_type': "Roots", 'comp_size': 50, 'sc_pulley': 0.8,
                'fuel_deliv': "EFI Multi", 'intake_conf': "ITB", 'manifold': "Performance", 'fuel_type': "Ultimate 100", 'afr': 13.5, 'ignition': 60, 'rpm_limit': 8000,
                'exh_arch': "Dual", 'headers': "Tubular", 'exh_diam': 60.0, 'cat': "High Flow", 'muffler1': "Straight", 'muffler2': "Baffled",
                'veh_preset': "Lehký sporťák", 'veh_weight': 1495.0, 'veh_cd': 0.32, 'tire_grip': 1.1, 'gears': 6, 'final_drive': 3.62, 'drivetrain': "RWD",
                'tech_level': 100
            },
            "Audi RS6 C7 (4.0 TFSI)": {
                'config': "V", 'cylinders': 8, 'v_angle': 90, 'block_mat': "Aluminium",
                'bore': 84.5, 'stroke': 89.0, 'radiator': 90,
                'crank': "Flat-plane", 'conrods': "Forged", 'pistons': "Forged", 'balancer': "Harmonic Damper",
                'head_mat': "Aluminium", 'valvetrain': "DOHC", 'valves': 4, 'vvt': "All", 'vvl': False, 'cam_profile': 30, 'comp_ratio': 8.8,
                'aspiration': "Turbo", 'turbo_bearing': "Ball Bearings", 'turbo_config': "Twin", 'intercooler': 70, 'turb_size': 40, 'boost': 0.50, 'sc_type': "Roots", 'comp_size': 50, 'sc_pulley': 0.8,
                'fuel_deliv': "Direct Injection", 'intake_conf': "Twin", 'manifold': "Performance", 'fuel_type': "Ultimate 100", 'afr': 14.5, 'ignition': 35, 'rpm_limit': 6800,
                'exh_arch': "Dual", 'headers': "Tubular", 'exh_diam': 65.0, 'cat': "High Flow", 'muffler1': "Straight", 'muffler2': "Straight",
                'veh_preset': "Vlastní (Custom)", 'veh_weight': 1950.0, 'veh_cd': 0.35, 'tire_grip': 1.2, 'gears': 7, 'final_drive': 3.2, 'drivetrain': "AWD",
                'tech_level': 98
            },
            "Mercedes-Benz C63 AMG (M156)": {
                'config': "V", 'cylinders': 8, 'v_angle': 90, 'block_mat': "Aluminium",
                'bore': 102.2, 'stroke': 94.6, 'radiator': 85,
                'crank': "Forged", 'conrods': "Forged", 'pistons': "Forged", 'balancer': "Harmonic Damper",
                'head_mat': "Aluminium", 'valvetrain': "DOHC", 'valves': 4, 'vvt': "All", 'vvl': False, 'cam_profile': 30, 'comp_ratio': 11.3,
                'aspiration': "NA", 'turbo_bearing': "Journal", 'turbo_config': "Single", 'intercooler': 50, 'turb_size': 50, 'boost': 0.5, 'sc_type': "Roots", 'comp_size': 50, 'sc_pulley': 0.8,
                'fuel_deliv': "EFI Multi", 'intake_conf': "Twin", 'manifold': "Standard", 'fuel_type': "Premium 95", 'afr': 13.0, 'ignition': 45, 'rpm_limit': 7200,
                'exh_arch': "Dual", 'headers': "Cast", 'exh_diam': 65.0, 'cat': "High Flow", 'muffler1': "Straight", 'muffler2': "Straight",
                'veh_preset': "Vlastní (Custom)", 'veh_weight': 1730.0, 'veh_cd': 0.32, 'tire_grip': 1.0, 'gears': 7, 'final_drive': 3.06, 'drivetrain': "RWD",
                'tech_level': 90
            },
            "Bugatti Veyron 16.4 Super Sport": {
                'config': "V", 'cylinders': 16, 'v_angle': 90, 'block_mat': "Aluminium",
                'bore': 86.0, 'stroke': 86.0, 'radiator': 100,
                'crank': "Billet", 'conrods': "Titanium", 'pistons': "Forged", 'balancer': "Full Balancers",
                'head_mat': "Aluminium", 'valvetrain': "DOHC", 'valves': 4, 'vvt': "All", 'vvl': False, 'cam_profile': 25, 'comp_ratio': 9.0,
                'aspiration': "Turbo", 'turbo_bearing': "Ball Bearings", 'turbo_config': "Quad", 'intercooler': 100, 'turb_size': 50, 'boost': 0.50, 'sc_type': "Roots", 'comp_size': 50, 'sc_pulley': 0.8,
                'fuel_deliv': "EFI Multi", 'intake_conf': "Twin", 'manifold': "Performance", 'fuel_type': "Ultimate 100", 'afr': 12.0, 'ignition': 55, 'rpm_limit': 6500,
                'exh_arch': "Dual", 'headers': "Tubular", 'exh_diam': 90.0, 'cat': "High Flow", 'muffler1': "None", 'muffler2': "Straight",
                'veh_preset': "Moderní Supersport", 'veh_weight': 1888.0, 'veh_cd': 0.36, 'tire_grip': 1.5, 'gears': 7, 'final_drive': 2.7, 'drivetrain': "AWD",
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
        if isinstance(self.vars[k], tk.BooleanVar): self.vars[k].set(bool(v))
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
        self.vars['engine_name'] = tk.StringVar(value="Sériová Mazda LF-DE 2.0")
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
        self.vars['cam_profile'] = tk.IntVar(value=25)
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
        self.vars['ignition'] = tk.IntVar(value=30)
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
        self.vars['tire_grip'] = tk.DoubleVar(value=0.9)
        self.vars['gears'] = tk.IntVar(value=5)
        self.vars['final_drive'] = tk.DoubleVar(value=4.9)
        self.vars['drivetrain'] = tk.StringVar(value="FWD")

    def create_menu(self):
        self.menubar = tk.Menu(self.root)
        self.filemenu = tk.Menu(self.menubar, tearoff=0)
        self.filemenu.add_command(label=self.tr("menu_load"), command=self.load_engine)
        self.filemenu.add_command(label=self.tr("menu_save"), command=self.save_engine)
        self.filemenu.add_separator()
        self.filemenu.add_command(label=self.tr("menu_quit"), command=self.root.quit)
        self.menubar.add_cascade(label=self.tr("menu_file"), menu=self.filemenu)
        self.root.config(menu=self.menubar)

    def create_language_selector(self):
        lang_frame = ttk.Frame(self.root)
        lang_frame.pack(fill=tk.X, padx=10, pady=(5,0))
        ttk.Radiobutton(lang_frame, text="🇨🇿 Čeština", variable=self.vars['app_lang'], value='cz', command=self.apply_language).pack(side=tk.RIGHT, padx=5)
        ttk.Radiobutton(lang_frame, text="🇬🇧 English", variable=self.vars['app_lang'], value='en', command=self.apply_language).pack(side=tk.RIGHT, padx=5)

    def save_engine(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("JSON files", "*.json")], initialfile=f"{self.vars['engine_name'].get()}.json")
        if file_path:
            data = {k: v.get() for k, v in self.vars.items() if k not in ['calc_disp', 'app_lang']}
            with open(file_path, 'w', encoding='utf-8') as f: json.dump(data, f, indent=4, ensure_ascii=False)

    def load_engine(self):
        file_path = filedialog.askopenfilename(filetypes=[("JSON files", "*.json")])
        if file_path:
            with open(file_path, 'r', encoding='utf-8') as f: data = json.load(f)
            # Stejný důvod jako u apply_master_preset: pokud starší uložený motor
            # nějaký (novější) parametr vůbec neobsahuje, nesmí zůstat hodnota
            # z dřívějška - nejdřív reset na tovární default, pak overlay uložených dat.
            for k, default_v in self.factory_defaults.items():
                self._set_var(k, default_v)
            for k, v in data.items():
                if k in self.vars:
                    if k == 'vvl' and isinstance(v, bool):
                        self.vars[k].set("VVL" if v else "None")
                    else:
                        self._set_var(k, v)
            self.update_dynamic_ui()
            self.update_displacement()

    def create_widgets(self):
        top_frame = ttk.Frame(self.root, padding="10 10 10 0")
        top_frame.pack(fill=tk.X)
        ttk.Label(top_frame, textvariable=self.lang_vars["lbl_engine_name"], font=("Arial", 10, "bold")).pack(side=tk.LEFT, padx=(0, 10))
        
        self.cb_engine_name = ttk.Combobox(top_frame, textvariable=self.vars['engine_name'], width=45, font=("Arial", 10))
        self.cb_engine_name['values'] = list(self.master_presets.keys())
        self.cb_engine_name.pack(side=tk.LEFT)
        self.cb_engine_name.bind("<<ComboboxSelected>>", self.apply_master_preset)

        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        def make_combo(parent, r, lbl_key, var_name, options, tt_key):
            lbl = ttk.Label(parent, textvariable=self.lang_vars[lbl_key])
            lbl.grid(row=r, column=0, sticky=tk.W, pady=3)
            cb = ttk.Combobox(parent, textvariable=self.vars[var_name], values=options, state="readonly", width=22)
            cb.grid(row=r, column=1, columnspan=2, sticky=tk.EW, pady=3)
            ToolTip(lbl, self.lang_vars[tt_key]); ToolTip(cb, self.lang_vars[tt_key])
            return lbl, cb

        def make_slider(parent, r, lbl_key, var_name, f_, t_, res, unit, tt_key):
            lbl = ttk.Label(parent, textvariable=self.lang_vars[lbl_key])
            lbl.grid(row=r, column=0, sticky=tk.W, pady=3)
            scale = ttk.Scale(parent, variable=self.vars[var_name], from_=f_, to=t_, orient=tk.HORIZONTAL)
            scale.grid(row=r, column=1, sticky=tk.EW, pady=3, padx=5)
            entry = ttk.Entry(parent, textvariable=self.vars[var_name], width=8, justify=tk.CENTER)
            entry.grid(row=r, column=2, sticky=tk.W, padx=2)
            unit_lbl = ttk.Label(parent, text=unit)
            unit_lbl.grid(row=r, column=3, sticky=tk.W)
            
            def update_lbl(*args):
                try:
                    float(self.vars[var_name].get())
                    if var_name in ['bore', 'stroke', 'cylinders']: self.update_displacement()
                except ValueError: pass
            self.vars[var_name].trace_add("write", update_lbl)
            update_lbl()
            ToolTip(lbl, self.lang_vars[tt_key]); ToolTip(scale, self.lang_vars[tt_key]); ToolTip(entry, self.lang_vars[tt_key])
            return scale
        
        # TAB 1 - Block
        tab1 = ttk.Frame(self.notebook, padding=10)
        self.notebook.add(tab1, text=self.tr("tab_1"))
        make_combo(tab1, 0, "lbl_config", 'config', ["Inline", "V", "Boxer"], "tt_config")
        self.frame_v = ttk.Frame(tab1); self.frame_v.grid(row=1, column=0, columnspan=4, sticky=tk.EW)
        make_combo(self.frame_v, 0, "lbl_vangle", 'v_angle', [60, 90, 120], "tt_vangle")
        make_combo(tab1, 2, "lbl_cyl", 'cylinders', [3, 4, 5, 6, 8, 10, 12, 16], "tt_cyl")
        make_combo(tab1, 3, "lbl_block", 'block_mat', ["Cast Iron", "Aluminium", "Aluminium Heavy", "Aluminium Light", "AlSi", "AlSi Heavy", "AlSi Light", "Aluminium Billet", "Magnesium"], "tt_block")
        make_slider(tab1, 4, "lbl_bore", 'bore', 50.0, 120.0, 0.1, "mm", "tt_bore")
        make_slider(tab1, 5, "lbl_stroke", 'stroke', 50.0, 120.0, 0.1, "mm", "tt_stroke")
        make_slider(tab1, 6, "lbl_rad", 'radiator', 10, 100, 1, "%", "tt_rad")
        make_slider(tab1, 7, "lbl_tech", 'tech_level', 50, 150, 1, "", "tt_tech")
        ttk.Label(tab1, textvariable=self.lang_vars['lbl_calc_disp']).grid(row=8, column=0, pady=10, sticky=tk.W)
        ttk.Label(tab1, textvariable=self.vars['calc_disp'], font=("Arial", 10, "bold")).grid(row=8, column=1, sticky=tk.W)

        # TAB 2 - Bottom End
        tab2 = ttk.Frame(self.notebook, padding=10)
        self.notebook.add(tab2, text=self.tr("tab_2"))
        make_combo(tab2, 0, "lbl_crank", 'crank', ["Cast", "Cast Iron Heavy", "Forged", "Forged Steel Heavy", "Forged Steel Light", "Billet", "Billet Steel Heavy", "Flat-plane"], "tt_crank")
        make_combo(tab2, 1, "lbl_conrods", 'conrods', ["Cast", "Cast Heavy", "Cast Light", "Heavy Duty", "Forged", "Forged Heavy", "Forged Light", "LW Forged", "Titanium"], "tt_conrods")
        make_combo(tab2, 2, "lbl_pistons", 'pistons', ["Cast", "Cast Heavy", "Cast Light", "Heavy Duty", "Forged", "Forged Heavy", "Forged Light", "LW Forged", "Hypereutectic Cast", "Low Friction"], "tt_pistons")
        make_combo(tab2, 3, "lbl_bal", 'balancer', ["None", "Harmonic Damper", "Full Balancers"], "tt_bal")
        self.frame_bal_mass = ttk.Frame(tab2); self.frame_bal_mass.grid(row=4, column=0, columnspan=4, sticky=tk.EW)
        make_slider(self.frame_bal_mass, 0, "lbl_bal_mass", 'balancer_mass', 0.0, 50.0, 0.1, "kg", "tt_bal_mass")

        # TAB 3 - Top End
        tab3 = ttk.Frame(self.notebook, padding=10)
        self.notebook.add(tab3, text=self.tr("tab_3"))
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
        tab4 = ttk.Frame(self.notebook, padding=10)
        self.notebook.add(tab4, text=self.tr("tab_4"))
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
        tab5 = ttk.Frame(self.notebook, padding=10)
        self.notebook.add(tab5, text=self.tr("tab_5"))
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
        tab6 = ttk.Frame(self.notebook, padding=10)
        self.notebook.add(tab6, text=self.tr("tab_6"))
        make_combo(tab6, 0, "lbl_arch", 'exh_arch', ["Single", "Dual"], "tt_arch")
        make_combo(tab6, 1, "lbl_head_exh", 'headers', ["Compact Cast", "Cast Low", "Cast Mid", "Cast", "Tubular", "Tubular Mid", "Tubular Long", "Tubular Race"], "tt_head_exh")
        make_slider(tab6, 2, "lbl_head_size", 'head_size', 0, 100, 1, "", "tt_head_size")
        make_slider(tab6, 3, "lbl_diam", 'exh_diam', 25.0, 150.0, 0.5, "mm", "tt_diam")
        make_combo(tab6, 4, "lbl_bypass", 'bypass', ["No Valves", "Bypass Valves"], "tt_bypass")
        make_combo(tab6, 5, "lbl_cat", 'cat', ["None", "2-way", "3-way", "High Flow", "Exhaust Reactor", "Three-Way + Pre-Cat", "High Flow 3-Way + Pre-Cat"], "tt_cat")
        make_combo(tab6, 6, "lbl_muf1", 'muffler1', ["None", "Straight", "Baffled", "Reverse Flow"], "tt_muf")
        make_combo(tab6, 7, "lbl_muf2", 'muffler2', ["None", "Straight", "Baffled", "Reverse Flow"], "tt_muf")

        # TAB 7 - Drivetrain
        tab7 = ttk.Frame(self.notebook, padding=10)
        self.notebook.add(tab7, text=self.tr("tab_7"))
        def apply_veh_preset(*args):
            preset = self.vars['veh_preset'].get()
            if preset == "Mazda 6 (2002)":
                self.vars['veh_weight'].set(1350.0); self.vars['veh_cd'].set(0.30); self.vars['tire_grip'].set(0.9); self.vars['gears'].set(5); self.vars['drivetrain'].set("FWD")
            elif preset == "Muscle Car (1969)":
                self.vars['veh_weight'].set(1750.0); self.vars['veh_cd'].set(0.45); self.vars['tire_grip'].set(0.7); self.vars['gears'].set(4); self.vars['drivetrain'].set("RWD")
            elif preset == "Lehký sporťák":
                self.vars['veh_weight'].set(1050.0); self.vars['veh_cd'].set(0.33); self.vars['tire_grip'].set(1.1); self.vars['gears'].set(6); self.vars['drivetrain'].set("RWD")
            elif preset == "Moderní Supersport":
                self.vars['veh_weight'].set(1550.0); self.vars['veh_cd'].set(0.28); self.vars['tire_grip'].set(1.4); self.vars['gears'].set(8); self.vars['drivetrain'].set("AWD")
        self.vars['veh_preset'].trace_add("write", apply_veh_preset)
        make_combo(tab7, 0, "lbl_veh", 'veh_preset', ["Vlastní (Custom)", "Mazda 6 (2002)", "Muscle Car (1969)", "Lehký sporťák", "Moderní Supersport"], "tt_veh")
        make_slider(tab7, 1, "lbl_weight", 'veh_weight', 500.0, 3000.0, 10.0, "kg", "tt_weight")
        make_slider(tab7, 2, "lbl_cd", 'veh_cd', 0.20, 0.60, 0.01, "", "tt_cd")
        make_slider(tab7, 3, "lbl_grip", 'tire_grip', 0.5, 2.0, 0.1, "µ", "tt_grip")
        make_combo(tab7, 4, "lbl_gears", 'gears', [4, 5, 6, 7, 8], "tt_gears")
        make_slider(tab7, 5, "lbl_fd", 'final_drive', 2.0, 6.0, 0.1, ": 1", "tt_fd")
        make_combo(tab7, 6, "lbl_drive", 'drivetrain', ["FWD", "RWD", "AWD"], "tt_drive")

        # Bind traces for dynamic updates
        self.vars['config'].trace_add("write", self.update_dynamic_ui)
        self.vars['aspiration'].trace_add("write", self.update_dynamic_ui)
        self.vars['balancer'].trace_add("write", self.update_dynamic_ui)
        self.vars['vvl'].trace_add("write", self.update_dynamic_ui)

        # --- SPODNÍ ČÁST (Konzole a tlačítka) ---
        bottom_frame = ttk.Frame(self.root, padding=10)
        bottom_frame.pack(fill=tk.BOTH, expand=False)
        self.txt_output = tk.Text(bottom_frame, height=8, bg="black", fg="lime", font=("Courier", 10))
        self.txt_output.pack(fill=tk.X, pady=5)
        self.txt_output.config(state=tk.DISABLED)

        btn_frame = ttk.Frame(bottom_frame)
        btn_frame.pack(pady=5)
        self.btn_run = ttk.Button(btn_frame, textvariable=self.lang_vars["btn_dyno"], command=self.start_dyno)
        self.btn_run.pack(side=tk.LEFT, padx=5)
        self.btn_graph = ttk.Button(btn_frame, textvariable=self.lang_vars["btn_graph"], command=self.plot_graph, state=tk.DISABLED)
        self.btn_graph.pack(side=tk.LEFT, padx=5)
        
        if SOUND_AVAILABLE:
            self.btn_rev = ttk.Button(btn_frame, textvariable=self.lang_vars["btn_rev"], command=self.open_throttle_window, state=tk.DISABLED)
            self.btn_rev.pack(side=tk.LEFT, padx=5)
            self.btn_drive = ttk.Button(btn_frame, textvariable=self.lang_vars["btn_drive"], command=self.open_drive_window, state=tk.DISABLED)
            self.btn_drive.pack(side=tk.LEFT, padx=5)
        else:
            self.btn_rev = ttk.Button(btn_frame, textvariable=self.lang_vars["btn_no_snd"], state=tk.DISABLED)
            self.btn_rev.pack(side=tk.LEFT, padx=5)

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

    def update_displacement(self):
        try:
            b, s, c = self.vars['bore'].get(), self.vars['stroke'].get(), self.vars['cylinders'].get()
            disp = math.pi * ((b/20)**2) * (s/10) * c
            self.vars['calc_disp'].set(f"{disp:.0f} cc")
            return disp
        except: return 2000

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

    def start_dyno(self):
        self.btn_run.config(state=tk.DISABLED)
        self.btn_graph.config(state=tk.DISABLED)
        if SOUND_AVAILABLE: 
            self.btn_rev.config(state=tk.DISABLED)
            self.btn_drive.config(state=tk.DISABLED)
        
        self.safe_clear_console()
        params = {'lang': self.vars['app_lang'].get()}
        for k, v in self.vars.items():
            if k not in ['calc_disp', 'app_lang']:
                try: params[k] = v.get()
                except tk.TclError:
                    if isinstance(v, tk.DoubleVar): params[k] = 0.0
                    elif isinstance(v, tk.IntVar): params[k] = 0
                    else: params[k] = ""

        self.dyno_params = params
        self.dyno_results = run_engine_simulation(params)
        threading.Thread(target=self.pull_thread, args=(params,), daemon=True).start()

    def pull_thread(self, params):
        name = self.vars['engine_name'].get()
        spec = f"{self.vars['calc_disp'].get()} {self.vars['config'].get()}{self.vars['cylinders'].get()}"
        header = f"{self.tr('msg_dyno_hdr')} {name} ({spec}) ---"
        
        step_duration = 0.08
        if is_windows:
            try:
                generate_engine_wav(self.dyno_results["rpm"], self.vars['cylinders'].get(), self.vars['aspiration'].get(), params.get('crank', 'Cast'), "dyno_temp.wav", step_duration)
                winsound.PlaySound("dyno_temp.wav", winsound.SND_FILENAME | winsound.SND_ASYNC)
            except: pass

        time.sleep(0.5)

        for i, rpm in enumerate(self.dyno_results["rpm"]):
            hp, trq = self.dyno_results["hp"][i], self.dyno_results["torque"][i]
            self.safe_update_pull(header, rpm, trq, hp)
            time.sleep(step_duration)

        if is_windows:
            winsound.PlaySound(None, winsound.SND_PURGE)
            if self.dyno_results["blew_up"]: winsound.MessageBeep(winsound.MB_ICONHAND) 
            try: os.remove("dyno_temp.wav")
            except: pass

        self.safe_log(self.tr('msg_done'))
        if self.dyno_results["blew_up"]:
            self.safe_log(f"{self.tr('msg_blown')} {self.dyno_results['reason']}")
            self.safe_log(f"{self.tr('msg_fix')} {self.dyno_results['fix']}")
        else:
            max_hp = np.max(self.dyno_results["hp"])
            max_hp_rpm = self.dyno_results["rpm"][np.argmax(self.dyno_results["hp"])]
            max_trq = np.max(self.dyno_results["torque"])
            max_trq_rpm = self.dyno_results["rpm"][np.argmax(self.dyno_results["torque"])]
            self.safe_log(f"{self.tr('msg_max_hp')}  {max_hp:.0f} HP @ {max_hp_rpm} RPM")
            self.safe_log(f"{self.tr('msg_max_trq')} {max_trq:.0f} Nm @ {max_trq_rpm} RPM")
            self.safe_log(self.tr('msg_ready'))

        self.root.after(0, lambda: self.btn_run.config(state=tk.NORMAL))
        self.root.after(0, lambda: self.btn_graph.config(state=tk.NORMAL))
        if not self.dyno_results.get("blew_up", True) and SOUND_AVAILABLE:
            self.root.after(0, lambda: self.btn_rev.config(state=tk.NORMAL))
            self.root.after(0, lambda: self.btn_drive.config(state=tk.NORMAL))

    def plot_graph(self):
        if not self.dyno_results: return
        rpm, hp, trq = self.dyno_results["rpm"], self.dyno_results["hp"], self.dyno_results["torque"]
        max_val = max(np.max(hp), np.max(trq))
        y_max = max_val * 1.1 
        
        fig, ax1 = plt.subplots(figsize=(9, 5))
        ax1.set_xlabel('RPM')
        ax1.set_ylabel(self.tr('msg_trq') + ' (Nm)', color='tab:blue')
        ax1.plot(rpm, trq, color='tab:blue', linewidth=2.5, label=self.tr('msg_trq'))
        ax1.tick_params(axis='y', labelcolor='tab:blue')
        ax1.set_ylim(0, y_max)
        ax1.grid(True, linestyle='--', alpha=0.5)

        ax2 = ax1.twinx()
        ax2.set_ylabel(self.tr('msg_hp') + ' (HP)', color='tab:red')
        ax2.plot(rpm, hp, color='tab:red', linewidth=2.5, label=self.tr('msg_hp'))
        ax2.tick_params(axis='y', labelcolor='tab:red')
        ax2.set_ylim(0, y_max)
        plt.title(f"Dyno: {self.vars['engine_name'].get()} - {self.vars['calc_disp'].get()} {self.vars['aspiration'].get()}")
        fig.tight_layout()
        plt.show()

    # --- OKNO 1: RUČNÍ PLYN ---
    def open_throttle_window(self):
        if not self.dyno_results or self.dyno_results.get("blew_up", True): return
        
        self.rev_window = tk.Toplevel(self.root)
        self.rev_window.title(self.tr("win_rev_title"))
        self.rev_window.geometry("350x450")
        self.rev_window.configure(bg='#111111')
        self.rev_window.resizable(False, False)
        self.rev_window.protocol("WM_DELETE_WINDOW", self.on_rev_close)
        self.rev_window.transient(self.root)
        self.rev_window.grab_set()
        
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
        self.radiator_eff = float(self.vars['radiator'].get()) / 100.0
        limit_rpm = float(self.vars['rpm_limit'].get())
        
        self.tacho_rev = AnalogTachometer(self.rev_window, max_rpm=limit_rpm+1000, redline_rpm=limit_rpm, size=280)
        self.tacho_rev.pack(pady=10)
        
        self.lbl_telemetry = tk.Label(self.rev_window, text="0 HP | 0 Nm", font=("Courier", 12), bg='#111111', fg='white')
        self.lbl_telemetry.pack(pady=2)
        
        self.lbl_temp = tk.Label(self.rev_window, text=f"{self.tr('lbl_coolant')} 90°C", font=("Arial", 12, "bold"), bg='#111111', fg="white")
        self.lbl_temp.pack(pady=5)
        
        btn_pedal = ttk.Button(self.rev_window, text=self.tr("btn_pedal"))
        btn_pedal.pack(fill=tk.BOTH, expand=True, padx=40, pady=15)
        
        btn_pedal.bind("<ButtonPress-1>", lambda e: setattr(self, 'throttle_active', True) if not self.engine_blown else None)
        btn_pedal.bind("<ButtonRelease-1>", lambda e: setattr(self, 'throttle_active', False))
        
        self.start_audio_stream()
        self.update_throttle_physics()

    def update_throttle_physics(self):
        if not hasattr(self, 'rev_window') or not self.rev_window.winfo_exists(): return
        limit_rpm = float(self.vars['rpm_limit'].get())
        
        if not self.engine_blown:
            target_rpm = limit_rpm if self.throttle_active else 1000.0
            diff = target_rpm - self.current_rpm
            self.current_rpm += diff * (0.08 if self.throttle_active else 0.04)
            self.current_rpm = max(1000.0, min(self.current_rpm, limit_rpm))
            
            cur_hp = np.interp(self.current_rpm, self.dyno_results["rpm"], self.dyno_results["hp"])
            cur_trq = np.interp(self.current_rpm, self.dyno_results["rpm"], self.dyno_results["torque"])
            
            load = 1.0 if self.throttle_active else 0.05
            heat_gen = math.sqrt(max(1, cur_hp)) * 0.06 * load * (self.current_rpm / limit_rpm)
            cooling = self.radiator_eff * ((self.coolant_temp - 20.0) / 100.0) * 1.0
            
            self.coolant_temp = max(20.0, self.coolant_temp + (heat_gen - cooling - 0.01) * 0.05)
            self.lbl_temp.config(text=f"{self.tr('lbl_coolant')} {int(self.coolant_temp)}°C", fg="red" if self.coolant_temp > 115.0 else "white")
            
            if self.coolant_temp >= 130.0:
                self.engine_blown = True
                self.throttle_active = False
                self.lbl_temp.config(text=self.tr("msg_hg_blown"), fg="red")
        else:
            self.blow_timer += 0.03
            self.current_rpm *= 0.95 
            cur_hp, cur_trq = 0, 0
            
        if not self.engine_blown:
            self.tacho_rev.set_rpm(self.current_rpm)
            self.lbl_telemetry.config(text=f"{int(cur_hp)} HP | {int(cur_trq)} Nm")
        
        self.rev_window.after(30, self.update_throttle_physics)

    def on_rev_close(self):
        self.stop_audio_stream()
        self.rev_window.grab_release()
        self.rev_window.destroy()

    # --- OKNO 2: ZKUŠEBNÍ JÍZDA ---
    def open_drive_window(self):
        if not self.dyno_results or self.dyno_results.get("blew_up", True): return
        
        self.drive_win = tk.Toplevel(self.root)
        self.drive_win.title(self.tr("win_drv_title"))
        self.drive_win.geometry("640x410")
        self.drive_win.configure(bg='#111111')
        self.drive_win.resizable(False, False)
        self.drive_win.protocol("WM_DELETE_WINDOW", self.on_drive_close)
        self.drive_win.transient(self.root)
        self.drive_win.grab_set()

        limit_rpm = float(self.vars['rpm_limit'].get())
        
        left_frame = tk.Frame(self.drive_win, bg='#111111')
        left_frame.pack(side=tk.LEFT, padx=20, pady=20)
        self.tacho_drive = AnalogTachometer(left_frame, max_rpm=limit_rpm+1000, redline_rpm=limit_rpm, size=300)
        self.tacho_drive.pack()

        right_frame = tk.Frame(self.drive_win, bg='#111111')
        right_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        self.lbl_speed = tk.Label(right_frame, text="0", font=("Courier", 54, "bold"), bg='#111111', fg='#00ffff')
        self.lbl_speed.pack(pady=(5, 0))
        tk.Label(right_frame, text="km/h", font=("Courier", 16), bg='#111111', fg='white').pack()

        gear_frame = tk.Frame(right_frame, bg='#111111')
        gear_frame.pack(pady=5)
        tk.Label(gear_frame, text="GEAR: ", font=("Arial", 16), bg='#111111', fg='gray').pack(side=tk.LEFT)
        self.lbl_gear = tk.Label(gear_frame, text="N", font=("Courier", 32, "bold"), bg='#111111', fg='white')
        self.lbl_gear.pack(side=tk.LEFT)

        self.lbl_tcs = tk.Label(right_frame, text="TCS READY", font=("Arial", 14, "bold"), bg='#222222', fg='gray', width=16, relief=tk.RAISED)
        self.lbl_tcs.pack(pady=5)
        
        self.lbl_0_100 = tk.Label(right_frame, text="0-100: -- s", font=("Courier", 14, "bold"), bg='#111111', fg='gray')
        self.lbl_0_100.pack(pady=5)

        btn_container = tk.Frame(right_frame, bg='#111111')
        btn_container.pack(pady=10)
        
        self.btn_launch = ttk.Button(btn_container, text=self.tr("btn_launch"), command=self.start_launch)
        self.btn_launch.pack(side=tk.LEFT, padx=5, ipadx=5, ipady=3)
        
        self.btn_skip = ttk.Button(btn_container, text=self.tr("btn_skip"), command=self.skip_to_top_speed, state=tk.DISABLED)
        self.btn_skip.pack(side=tk.LEFT, padx=5, ipadx=5, ipady=3)

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
        self.top_speed_timer = 0
        
        self.drive_time = 0.0
        self.time_100 = None

        self.audio_phase = 0.0 
        self.rev_phase = 0.0 
        self.flutter_phase = 0.0
        self.flutter_intensity = 0.0
        
        self.start_audio_stream(is_drive=True)
        self.drive_win.after(100, self.drive_step)

    def start_launch(self):
        if self.drive_running: return
        self.drive_running = True
        self.throttle_active = True
        self.v = 0.0
        self.max_achieved_speed = 0.0
        self.gear = 0
        self.a_prev = 0.0
        self.shift_delay = 0.0
        self.top_speed_timer = 0
        self.drive_time = 0.0
        self.time_100 = None
        
        self.lbl_0_100.config(text="0-100: -- s", fg="gray")
        self.btn_launch.config(state=tk.DISABLED, text=self.tr("btn_accel"))
        self.btn_skip.config(state=tk.NORMAL)

    def skip_to_top_speed(self):
        if not self.drive_running: return
        self.btn_skip.config(state=tk.DISABLED)
        
        veh_params = {
            'weight': float(self.vars['veh_weight'].get()),
            'cd': float(self.vars['veh_cd'].get()),
            'grip': float(self.vars['tire_grip'].get()),
            'gears': int(self.vars['gears'].get()),
            'final_drive': float(self.vars['final_drive'].get()),
            'drivetrain': self.vars['drivetrain'].get()
        }

        res = run_vehicle_kinematics(veh_params, self.dyno_results)
        
        self.v = res["top_speed"]
        self.max_achieved_speed = res["top_speed"]
        self.gear = res["final_gear"]
        
        r = 0.33
        wheel_rpm = (self.v / (2 * math.pi * r)) * 60
        fd = veh_params['final_drive']
        
        gear_count = veh_params['gears']
        if gear_count <= 4: ratios = [2.8, 1.5, 1.0, 0.8]
        elif gear_count == 5: ratios = [3.3, 1.9, 1.3, 1.0, 0.8]
        elif gear_count == 6: ratios = [3.5, 2.0, 1.4, 1.0, 0.8, 0.6]
        else: ratios = [4.0, 2.5, 1.7, 1.2, 0.9, 0.7, 0.55, 0.45][:gear_count]
        
        max_rpm = self.dyno_results['rpm'][-1]
        self.current_rpm = min(max_rpm, max(1000.0, wheel_rpm * ratios[self.gear] * fd))
        
        self.time_100 = res["time_0_100"]
        if self.time_100 is not None:
            self.lbl_0_100.config(text=f"0-100: {self.time_100:.2f} s", fg="#00ffff")
        else:
            self.lbl_0_100.config(text=f"0-100: {self.tr('msg_not_reached')}", fg="red")
            
        self.drive_running = False 
        self.lbl_tcs.config(text=f"MAX: {int(self.max_achieved_speed * 3.6)} km/h", fg="black", bg="lime")
        self.btn_launch.config(state=tk.NORMAL, text=self.tr("btn_retry"))

    def drive_step(self):
        if not hasattr(self, 'drive_win') or not self.drive_win.winfo_exists(): return
        dt = 0.03
        
        if self.drive_running:
            self.drive_time += dt
            if self.time_100 is None and self.v > 0.1: 
                self.lbl_0_100.config(text=f"0-100: {self.drive_time:.1f} s", fg="white")
            if self.time_100 is None and self.v * 3.6 >= 100.0:
                self.time_100 = self.drive_time
                self.lbl_0_100.config(text=f"0-100: {self.time_100:.2f} s", fg="#00ffff")
        
        rpm_arr = self.dyno_results['rpm']
        trq_arr = self.dyno_results['torque']
        max_rpm = rpm_arr[-1]
        max_hp_idx = np.argmax(self.dyno_results["hp"])
        ideal_shift_rpm = min(max_rpm - 50, self.dyno_results["rpm"][max_hp_idx] + 400)

        mass = float(self.vars['veh_weight'].get())
        cd = float(self.vars['veh_cd'].get())
        grip = float(self.vars['tire_grip'].get())
        gear_count = int(self.vars['gears'].get())
        fd = float(self.vars['final_drive'].get())
        drivetrain = self.vars['drivetrain'].get()

        if gear_count <= 4: ratios = [2.8, 1.5, 1.0, 0.8]
        elif gear_count == 5: ratios = [3.3, 1.9, 1.3, 1.0, 0.8]
        elif gear_count == 6: ratios = [3.5, 2.0, 1.4, 1.0, 0.8, 0.6]
        else: ratios = [4.0, 2.5, 1.7, 1.2, 0.9, 0.7, 0.55, 0.45][:gear_count]

        r = 0.33 
        area = 2.2 
        rho = 1.2 
        g = 9.81
        wheelbase = 2.7
        cg_height = 0.5
        w_f = 0.6 if drivetrain == "FWD" else 0.5
        w_r = 0.4 if drivetrain == "FWD" else 0.5

        if not self.drive_running:
            self.throttle_active = False
            if self.current_rpm > 1000.0:
                self.current_rpm = max(1000.0, self.current_rpm - 40.0) 
            drag_a = (-0.5 * rho * cd * area * self.v**2 - mass * g * 0.015) / mass
            self.v += drag_a * dt
            self.v = max(self.v, 0.0)
            self.tacho_drive.set_rpm(self.current_rpm)
            self.lbl_speed.config(text=f"{int(self.v * 3.6)}")
            self.drive_win.after(30, self.drive_step)
            return

        self.max_achieved_speed = max(self.max_achieved_speed, self.v)
        a = 0.0
        self.slip_active = False
        is_shifting_now = False

        if self.shift_delay > 0:
            self.shift_delay -= dt
            is_shifting_now = True

        if is_shifting_now:
            self.current_rpm = max(1000.0, self.current_rpm - 60.0)
            a = (-0.5 * rho * cd * area * self.v**2 - mass * g * 0.015) / mass
        else:
            wheel_rpm = (self.v / (2 * math.pi * r)) * 60
            engine_rpm = wheel_rpm * ratios[self.gear] * fd
            
            # Najdeme, v jakých otáčkách má motor maximální krouticí moment
            max_trq_idx = np.argmax(trq_arr)
            peak_trq_rpm = rpm_arr[max_trq_idx]
            
            # Ideální start (Launch Control) je zhruba na 85 % maxima krouťáku.
            # Omezíme to zespodu na 2500 RPM a shora nesmí překročit 75 % červeného pole.
            launch_rpm = min(max(2500.0, peak_trq_rpm * 0.85), max_rpm * 0.75)
            if self.gear == 0 and engine_rpm < launch_rpm:
                calc_rpm = launch_rpm + math.sin(time.time() * 25) * 150
            else:
                calc_rpm = max(1000.0, engine_rpm)
            
            if calc_rpm > ideal_shift_rpm:
                if self.gear < gear_count - 1:
                    self.gear += 1
                    self.shift_delay = 0.20 
                    is_shifting_now = True
                    a = (-0.5 * rho * cd * area * self.v**2 - mass * g * 0.015) / mass
                else:
                    calc_rpm = max_rpm

            if not is_shifting_now:
                current_trq = np.interp(calc_rpm, rpm_arr, trq_arr)
                force_wheel = (current_trq * ratios[self.gear] * fd * 0.86) / r
                
                # 1. Vypočítáme aerodynamický odpor dřív, abychom z něj určili přítlak
                drag = 0.5 * rho * cd * area * self.v**2
                roll = mass * g * 0.015
                
                # 2. Simulace přítlaku (Downforce). Reálný přítlak dělá funkční aero paket
                # (křídla, difuzor, spoiler) - ne odpor vzduchu (Cd) samotný, ten o přítomnosti
                # aera nic neříká (hranaté auto s vysokým Cd nemá přítlak o nic víc než áčko).
                # Jako proxy bereme grip pneumatik - u aut v presetech roste právě se sportovním/
                # závodním laděním. Běžné auto (grip <= 1.0) tak nemá žádný umělý přítlak,
                # závodně laděné auto ho má, ale v reálných, ne přehnaných hodnotách.
                aero_factor = max(0.0, min(1.0, (grip - 1.0) / 0.5))
                aero_downforce = drag * aero_factor * 0.8
                
                # 3. Rozložení umělé váhy na nápravy vč. aerodynamiky
                transfer = (mass * self.a_prev * cg_height) / wheelbase
                
                if drivetrain == "FWD": 
                    driven_weight = (mass * g * w_f) - transfer + (aero_downforce * 0.4)
                elif drivetrain == "RWD": 
                    driven_weight = (mass * g * w_r) + transfer + (aero_downforce * 0.6)
                else: 
                    driven_weight = mass * g + aero_downforce
                    
                driven_weight = max(driven_weight, mass * g * 0.1)
                max_grip_force = driven_weight * grip
                
                if force_wheel > max_grip_force:
                    self.slip_active = True
                    force_wheel = max_grip_force
                    calc_rpm = min(max_rpm, calc_rpm + 800) 
                
                self.current_rpm = calc_rpm
                drag = 0.5 * rho * cd * area * self.v**2
                roll = mass * g * 0.015
                net_force = force_wheel - drag - roll
                a = net_force / (mass * 1.05)
                
        self.a_prev = a
        self.v += a * dt
        self.v = max(self.v, 0.0) 

        self.tacho_drive.set_rpm(self.current_rpm)
        self.lbl_speed.config(text=f"{int(self.v * 3.6)}")
        
        if self.shift_delay > 0:
            self.lbl_gear.config(text="--", fg="yellow")
        else:
            self.lbl_gear.config(text=str(self.gear + 1), fg="white")

        if self.slip_active:
            self.lbl_tcs.config(text="SLIP", fg="black", bg="orange")
        else:
            self.lbl_tcs.config(text="TCS OK", fg="gray", bg="#222222")

        if not is_shifting_now and a < 0.01 and self.v > 15.0:
            self.top_speed_timer += 1
            if self.top_speed_timer > 10:  
                self.drive_running = False 
                self.lbl_tcs.config(text=f"MAX: {int(self.max_achieved_speed * 3.6)} km/h", fg="black", bg="lime")
                self.btn_launch.config(state=tk.NORMAL, text=self.tr("btn_retry"))
                self.btn_skip.config(state=tk.DISABLED)
                if self.time_100 is None:
                    self.lbl_0_100.config(text=f"0-100: {self.tr('msg_not_reached')}", fg="red")
        else:
            self.top_speed_timer = 0
            
        self.drive_win.after(30, self.drive_step)

    def on_drive_close(self):
        self.stop_audio_stream()
        self.drive_win.grab_release()
        self.drive_win.destroy()

    def start_audio_stream(self, is_drive=False):
        cylinders = self.vars['cylinders'].get()
        aspiration = self.vars['aspiration'].get()
        crank = self.vars['crank'].get()
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
            self.safe_log(f"Chyba při startu zvuku: {e}")

    def stop_audio_stream(self):
        if hasattr(self, 'stream') and self.stream.active:
            self.stream.stop()
            self.stream.close()

if __name__ == "__main__":
    root = tk.Tk()
    app = EngineApp(root)
    root.mainloop()