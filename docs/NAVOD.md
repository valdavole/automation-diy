# Návod k použití

*[User Guide in English](USER_GUIDE.md)*

Tento návod prochází simulátor v pořadí, v jakém se běžně používá. Tooltips přímo v aplikaci poskytují rychlé vysvětlení jednotlivých parametrů; tento dokument ukazuje, jak do sebe jednotlivé systémy zapadají.

Návod platí pro **Automation DIY v4.7 — Custom Gearing & Test Track**.

## 1. Celkový postup práce

1. Vyber startovní bod z rozbalovacího seznamu presetů nahoře, nebo začni od výchozích hodnot.
2. Nastav motor a vozidlo napříč **7 záložkami**.
3. Klikni na **1. Dyno Pull** a nech vygenerovat křivku točivého momentu a výkonu.
4. Klikni na **Graf** a výsledek si prohlédni.
5. Volitelně spusť **2. Ruční plyn** pro živý test chlazení a telemetrie.
6. Spusť **3. Zkušební jízdu** pro měření 0–100 km/h a maximální rychlosti.
7. Spusť **4. Testovací dráhu** pro letmé kolo na společném okruhu dlouhém 3,605 km.
8. Build pojmenuj a přes **Soubor → Uložit motor jako...** ho ulož do přenositelného `.json` souboru.

Přepínač jazyka CZ/EN lze změnit kdykoliv bez resetování rozpracovaného buildu.

## 2. Přehled 7 záložek

### Záložka 1 — Block

Určuje základní architekturu motoru.

- **Konfigurace**: Inline / V / Boxer.
- **Úhel V**: zobrazuje se pouze u V motorů. Dostupné jsou hodnoty 60°, 90° a 120°.
- **Počet válců**: 3, 4, 5, 6, 8, 10, 12 nebo 16.
- **Materiál bloku**: od těžké litiny přes varianty hliníku a AlSi až po billetový hliník a hořčík.
- **Vrtání**: větší vrtání podporuje větší ventily a lepší dýchání ve vysokých otáčkách.
- **Zdvih**: delší zdvih zvýhodňuje točivý moment dole, ale zvyšuje střední pístovou rychlost a omezuje vysoké otáčky.
- **Účinnost chladiče**: ovlivňuje odvod tepla v režimu Ruční plyn.
- **Technologická úroveň**: globálně ovlivňuje účinnost, průtok, tření a odolnost proti klepání.

Vypočítaný objem motoru se automaticky aktualizuje podle vrtání, zdvihu a počtu válců.

### Záložka 2 — Bottom End

Určuje mechanický strop otáček.

- **Kliková hřídel**, **ojnice** a **písty** mají vlastní limity podle zvoleného materiálu.
- Skutečný mechanický limit určuje nejslabší z těchto tří částí.
- **Vyvažováky** mění poměr mezi vyšším limitem otáček, třením a rotační hmotou.
- Při zvolení harmonic damperu nebo plných vyvažováků se zobrazí **slider hmotnosti vyvažováků**.

Nastavení omezovače nad limit nejslabší mechanické části motor při Dyno Pullu záměrně zničí.

### Záložka 3 — Top End

Řídí hlavu válců, proudění, valve float a část modelu klepání.

- **Materiál hlavy** ovlivňuje držení tepla, tření, úroveň průtoku a sklon ke klepání.
- **Rozvody**: Pushrod/OHV, SOHC, DOHC nebo DAOHC.
- **Ventilů na válec**: 2–5.
- **VVT** mění časování ventilů a rozšiřuje využitelné pásmo výkonu.
- **VVL** může být vypnuté, přepínané v daných otáčkách nebo řešené jako CVVL.
- Volba VVL nebo CVVL zobrazí nastavení **VVL Profil** a **VVL Otáčky**.
- **Pružiny a zdvihátka** posouvají limit valve floatu, ale přidávají tření.
- **Profil vačky** posouvá křivku objemové účinnosti v rozsahu otáček.
- **Kompresní poměr** přidává moment a účinnost, ale u zážehových paliv také zvyšuje riziko klepání.

### Záložka 4 — Aspiration

- **NA**: okamžitá reakce bez plnicího tlaku.
- **Turbo**: přeplňování výfukovými plyny s náběhem závislým na velikosti turba, objemu motoru, ložiscích, konfiguraci a intercooleru.
- **Supercharger**: okamžitý tlak s mechanickými parazitními ztrátami.

Turbo nabízí nastavení ložisek, konfigurace Single/Twin/Quad, velikosti intercooleru, velikosti turba a plnicího tlaku.

Kompresor nabízí typ Roots, Twin-screw nebo Centrifugal, velikost jednotky a nastavení řemenice či tlaku.

### Záložka 5 — Fuel & Tune

Společně se záložkami Top End a Aspiration určuje výkon a riziko klepání.

- **Vstřikování**: Carburetor, Mechanical Fuel Injection, Single Point EFI, EFI Multi nebo Direct Injection.
- **Velikost klapky či karburátoru** mění kompromis mezi reakcí dole a průtokem nahoře.
- **Konfigurace sání**: Single, Twin nebo ITB.
- **Sací svody** a **velikost sání** tvarují křivku momentu a efektivní pásmo otáček.
- **Druh paliva** určuje základní odolnost proti klepání.
- **Palivová mapa** mění bohatost směsi nezávisle na AFR.
- **AFR** ovlivňuje výkon, účinnost a riziko klepání při chudé směsi.
- **Předstih** přidává výkon, ale při přehnaném nastavení zvyšuje riziko detonace.
- **Omezovač RPM** je požadovaná hranice Dyno Pullu a musí zůstat v mechanických limitech, pokud není selhání záměrné.

Nafta obchází benzínový výpočet klepání. Nitromethane získává výrazně vyšší potenciální výkonový strop, ale neodstraňuje ostatní fyzikální limity motoru.

### Záložka 6 — Exhaust

- **Architektura**: Single nebo Dual.
- **Svody** sahají od restriktivních kompaktních litinových systémů až po závodní tubular varianty.
- **Velikost svodů** a **průměr potrubí** ovlivňují rychlost plynů a schopnost odvést velké množství výfukových plynů.
- **Obtokové klapky** se nad 3500 RPM otevřou a obejdou tlumiče.
- **Katalyzátor** mění kompromis mezi emisní výbavou a restrikcí.
- **Dvě pozice tlumičů** umožňují kombinace od rovné roury po reverse-flow systémy.

Příliš malý výfuk postupně dusí horní část křivky momentu.

### Záložka 7 — Drivetrain

Tato nastavení ovlivňují **Zkušební jízdu** a **Testovací dráhu**, nikoliv dyno křivku.

- **Předvolba vozu** vyplní hodnoty šasi reprezentativním nastavením. Zvolení předvolby současně vypne vlastní převody, aby preset zachoval automatickou převodovou sadu.
- **Váha**: celková hmotnost vozidla včetně řidiče a náplní.
- **Odpor vzduchu (Cd)**: bezrozměrný součinitel aerodynamického odporu.
- **Čelní plocha**: referenční plocha používaná společně s Cd ve výpočtu odporu.
- **Poloměr kola**: ovlivňuje sílu na kole i rychlost při daných otáčkách motoru.
- **Omezovač rychlosti**: elektronická maximální rychlost; hodnota `0` jej vypne.
- **Přítlak (Cl·A)**: součin součinitele přítlaku a plochy. Je oddělený od přilnavosti pneumatik.
- **Trakce pneumatik**: základní koeficient tření dostupný pro akceleraci, brzdění a zatáčení.
- **Počet převodů**: 4–8 stupňů.
- **Stálý převod**: násobí všechny převody v převodovce.
- **Pohon**:
  - FWD má malé ztráty, ale při akceleraci se odlehčuje hnaná přední náprava.
  - RWD při akceleraci získává zatížení zadní nápravy.
  - AWD využívá trakci všech čtyř kol, ale má největší ztráty pohonu.

#### Volitelné jemné nastavení převodů

Zaškrtávací políčko **Jemné nastavení jednotlivých převodů** je ve výchozím stavu vypnuté.

Když je vypnuté:

- editor převodů zůstává skrytý
- simulátor používá vestavěnou automatickou sadu pro zvolený počet stupňů
- existující presety si zachovávají své zavedené výsledky 0–100 km/h a maximální rychlosti

Když je zapnuté:

- zobrazí se jedno pole pro každý aktivní převod
- podporovány jsou převodovky se 4–8 stupni
- tlačítko **Načíst automatické převody** obnoví výchozí sadu
- převody ovlivní následující Zkušební jízdu i Testovací dráhu

U rozumně odstupňované převodovky má každý vyšší stupeň zpravidla numericky menší převodový poměr než stupeň před ním.

## 3. Spuštění Dyno Pullu

Klikni na **1. Dyno Pull**. Simulátor zkontroluje vstupní hodnoty, projede povolený rozsah otáček a v každém bodě spočítá točivý moment a výkon.

Build mohou zastavit dvě nezávislé cesty selhání:

- **Mechanické přetočení**: omezovač RPM překročí limit nejslabší klikové hřídele, ojnic nebo pístů.
- **Klepání a detonace**: vypočítaný knock index je příliš vysoký kvůli nebezpečné kombinaci komprese, plnicího tlaku, předstihu, AFR, palivové mapy, oktanového čísla, vstřikování, materiálu hlavy nebo technologické úrovně.

Konzole vysvětlí příčinu selhání i hlavní úpravy, které jej mohou odstranit.

Po úspěšném pullu:

- zpřístupní se **Graf**
- při dostupném zvukovém backendu se zpřístupní Ruční plyn
- zpřístupní se **Zkušební jízda** a **Testovací dráha**

## 4. Ruční plyn

Ruční plyn je živý test vytáčení motoru a chlazení.

Držením tlačítka se motor přibližuje k omezovači. Produkce tepla závisí na zatížení a výkonu motoru, zatímco účinnost chladiče určuje rychlost odvodu tepla. Při dosažení mezní teploty selže těsnění pod hlavou.

Tento režim je oddělený od dyno selhání způsobeného klepáním nebo mechanickým přetočením.

## 5. Zkušební jízda

Zkušební jízda simuluje start z místa, automatické řazení, zrychlení 0–100 km/h a maximální rychlost.

Model používá:

- kompletní křivku momentu motoru
- automatické nebo vlastní převody
- stálý převod a poloměr kola
- účinnost pohonného ústrojí
- podélný přenos hmotnosti
- limity trakce pneumatik
- aerodynamický odpor z Cd a čelní plochy
- valivý odpor
- aerodynamický přítlak
- otáčkový i elektronický rychlostní limit

Indikátor TCS ukazuje prokluz kol. Maximální rychlost může omezit dostupný výkon, odpor vzduchu, nejvyšší převod a redline nebo elektronický omezovač.

Tlačítko **Přeskočit na max** použije stejný model vozidla, ale urychlí výpočet a přesune zobrazení přímo na výsledek.

## 6. Testovací dráha

Testovací dráha počítá deterministické **letmé kolo**, nikoliv kolo se startem z klidu.

### Okruh

- Délka: **3,605 km**
- Tři měřené sektory
- Technická kombinace rovinek, vracáků, středně rychlých zatáček, rychlejších oblouků a navazujících změn směru
- Zobrazená dráha a fyzikálně simulovaná dráha používají tutéž geometrii

Okruh vzniká z jediné uzavřené křivky, která je převzorkována na krátké úseky. Z její lokální křivosti se vypočítají informace o poloměrech zatáček. Stejné body se následně pouze přeškálují na mapu v okně, aniž by se změnil tvar dráhy.

### Výpočet kola

Model kola používá:

- dyno křivku točivého momentu
- automatické nebo vlastní převody
- stálý převod, poloměr kola, redline a omezovač rychlosti
- hmotnost a ztráty pohonu
- Cd, čelní plochu a valivý odpor
- přilnavost pneumatik a aerodynamický přítlak
- třecí kružnici pneumatik, takže zatáčení ubírá grip dostupný pro akceleraci nebo brzdění
- zpětné průchody, které vytvoří brzdné zóny před zatáčkami
- dopředné průchody, které omezí akceleraci mezi body dráhy
- pevné časové ztráty za řazení nahoru a dolů

Animace je zrychlená, aby dlouhé simulované kolo nevyžadovalo stejnou dobu skutečného čekání.

Po dokončení se zobrazí:

- celkový čas kola
- časy sektoru 1, sektoru 2 a sektoru 3
- průměrná rychlost
- maximální rychlost

Model je deterministický, takže shodný build vytvoří shodný čas. Okruh je proto vhodný jako společný benchmark pro porovnávání aut uvnitř simulátoru.

## 7. Zvuk motoru

Pokud jsou dostupné `sounddevice` a funkční PortAudio, zvuk motoru se syntetizuje živě z otáček, počtu válců, typu plnění, polohy plynu a typu klikové hřídele.

Turbo motory obsahují zvuk náběhu a flutter při ubrání. Kompresorové motory dostávají kvílení závislé na otáčkách.

Pokud zvukový backend není dostupný, simulátor zůstává plně použitelný bez živého zvuku.

## 8. Uložení a načtení

Přes **Soubor → Uložit motor jako...** ulož aktuální build do JSON souboru.

Uložený soubor obsahuje nastavení motoru, šasi, přepínač vlastních převodů i hodnoty všech jednotlivých převodových poměrů.

Při načítání:

- simulátor nejprve obnoví bezpečné tovární hodnoty
- následně aplikuje hodnoty ze souboru
- starší soubory bez novějších parametrů dostanou rozumné výchozí hodnoty
- starý Boolean formát VVL se převede automaticky
- neplatný nebo poškozený soubor zobrazí chybu místo částečného poškození aktivního buildu

## 9. Řešení problémů

- **Jednorázová chyba při spuštění předkompilovaného exe**: antivirus může během prvního skenu krátce zamknout nepodepsaný single-file spustitelný soubor. Po dokončení kontroly aplikaci spusť znovu.
- **Nefunguje živý zvuk**: zkontroluj `sounddevice`, PortAudio a funkční výchozí výstupní zařízení.
- **Zkušební jízda nebo Testovací dráha jsou vypnuté**: nejprve dokonči úspěšný Dyno Pull. Zničený motor nelze testovat.
- **Vlastní převody nejsou vidět**: v záložce Drivetrain zapni **Jemné nastavení jednotlivých převodů**.
- **Preset po změně převodů dává jiné výsledky**: vlastní převody vypni nebo stiskni **Načíst automatické převody**.
