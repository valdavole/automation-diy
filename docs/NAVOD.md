# Návod k použití

*[User Guide in English](USER_GUIDE.md)*

Tento návod prochází simulátor v pořadí, v jakém se běžně používá. Tooltips přímo v aplikaci poskytují rychlé vysvětlení jednotlivých parametrů; tento dokument ukazuje, jak do sebe jednotlivé systémy zapadají.

Návod platí pro **Automation DIY v4.10.2 — Branding Update**.

## 1. Celkový postup práce

Simulátor se otevírá v režimu celé obrazovky a všechny hlavní režimy drží uvnitř jediného okna. Brandované levé menu přepíná mezi obrazovkami Garáž, Dyno & Graf, Ruční plyn, Zkušební jízda a Simulace okruhu.

- Klávesou **F11** zapneš nebo vypneš fullscreen.
- Klávesa **Esc** zavře Nastavení nebo chybový overlay, vrátí tě z jiného režimu do Garáže, případně při otevřené Garáži opustí fullscreen.
- V **Nastavení** můžeš načíst nebo uložit build, změnit jazyk, vybrat km/h či mph nebo ukončit simulátor.
- Kompaktní tlačítko vpravo nahoře ukazuje aktuální jazyk a jednotku rychlosti a otevírá stejný panel Nastavení.
- Při menším okně se dlouhé záložky automaticky posouvají. Posuvník se zobrazí pouze tehdy, když se obsah skutečně nevejde.
- Simulace okruhu mění velikost mapy podle dostupného prostoru; v úzkém okně přesune informační panel pod mapu.

Typický postup:

1. Nahoře ve stavbě zadej samostatný **Název vozu / projektu**.
2. Z **Blank Project** ručně nastav všechna povinná pole motoru a vozidla, nebo přes **Preset motoru a vozu** načti kompletní startovní konfiguraci. Tovární preset přepíše název projektu; ten potom můžeš změnit bez zásahu do technického nastavení.
3. Klikni na **Spustit Dyno / 1. Dyno Pull** a nech vygenerovat křivku točivého momentu a výkonu.
4. Sleduj živý graf a telemetrii a poté si na obrazovce Dyna prohlédni dokončené křivky.
5. Volitelně otevři **Ruční plyn** pro živý test chlazení a telemetrie.
6. Otevři **Zkušební jízdu** pro měření 0–100 km/h nebo 0–60 mph a maximální rychlosti.
7. Otevři **Simulaci okruhu** pro letmé kolo na společném okruhu dlouhém 3,605 km.
8. Pojmenovaný build přes **Nastavení → Uložit motor / vozidlo jako...** ulož do přenositelného `.json` souboru.

Jazyk a jednotky rychlosti lze změnit za chodu bez resetování rozpracovaného buildu nebo změny fyziky vozidla. Po každém spuštění jsou jako výchozí zvoleny km/h.

## 2. Přehled 7 záložek

### Záložka 1 — Blok motoru

Určuje základní architekturu motoru.

- **Konfigurace**: Inline / V / Boxer.
- **Úhel V**: zobrazuje se pouze u V motorů. Dostupné jsou hodnoty 60°, 90° a 120°.
- **Počet válců**: 3, 4, 5, 6, 8, 10, 12 nebo 16.
- **Materiál bloku**: od těžké litiny přes varianty hliníku a AlSi až po billetový hliník a hořčík.
- **Vrtání**: větší vrtání podporuje větší ventily a lepší dýchání ve vysokých otáčkách.
- **Zdvih**: delší zdvih zvýhodňuje točivý moment dole, ale zvyšuje střední pístovou rychlost a omezuje vysoké otáčky. Slider pokrývá běžných 50–120 mm; pro speciální motory lze ručně zadat 20–150 mm.
- **Účinnost chladiče**: ovlivňuje odvod tepla v režimu Ruční plyn.
- **Technologická úroveň**: globálně ovlivňuje účinnost, průtok, tření a odolnost proti klepání.

Vypočítaný objem motoru se automaticky aktualizuje podle vrtání, zdvihu a počtu válců.

### Záložka 2 — Spodek motoru

Určuje mechanický strop otáček.

- **Kliková hřídel**, **ojnice** a **písty** mají vlastní limity podle zvoleného materiálu.
- Skutečný mechanický limit určuje nejslabší z těchto tří částí.
- **Vyvažováky** mění poměr mezi vyšším limitem otáček, třením a rotační hmotou.
- Při zvolení harmonic damperu nebo plných vyvažováků se zobrazí **slider hmotnosti vyvažováků**. Při volbě **None** fyzika skrytou hodnotu hmotnosti vyvažováků ignoruje.

Nastavení omezovače nad limit nejslabší mechanické části motor při Dyno Pullu záměrně zničí.

### Záložka 3 — Hlava a rozvody

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

### Záložka 4 — Plnění

- **NA**: okamžitá reakce bez plnicího tlaku.
- **Turbo**: přeplňování výfukovými plyny s náběhem závislým na velikosti turba, objemu motoru, ložiscích, konfiguraci a intercooleru.
- **Supercharger**: okamžitý tlak s mechanickými parazitními ztrátami.

Turbo nabízí nastavení ložisek, konfigurace Single/Twin/Quad, velikosti intercooleru, velikosti turba a plnicího tlaku.

Kompresor nabízí typ Roots, Twin-screw nebo Centrifugal, velikost jednotky a nastavení řemenice či tlaku.

### Záložka 5 — Palivo a ladění

Společně se záložkami Top End a Aspiration určuje výkon a riziko klepání.

- **Vstřikování**: Carburetor, Mechanical Fuel Injection, Single Point EFI, EFI Multi nebo Direct Injection.
- **Velikost klapky či karburátoru** mění kompromis mezi reakcí dole a průtokem nahoře.
- **Konfigurace sání**: Single, Twin nebo ITB.
- **Sací svody** a **velikost sání** tvarují křivku momentu a efektivní pásmo otáček.
- **Druh paliva** určuje základní odolnost proti klepání.
- **Palivová mapa** mění bohatost směsi nezávisle na AFR.
- **AFR** ovlivňuje výkon, účinnost a riziko klepání při chudé směsi.
- **Předstih** přidává výkon, ale při přehnaném nastavení zvyšuje riziko detonace.
- **Omezovač RPM** je požadovaná hranice Dyno Pullu. Slider pokrývá 3 000–12 000 RPM; ručně lze zadat až 20 000 RPM, ale takové otáčky přežije pouze odpovídající závodní architektura.

Nafta obchází benzínový výpočet klepání. Nitromethane získává výrazně vyšší potenciální výkonový strop, ale neodstraňuje ostatní fyzikální limity motoru.

### Záložka 6 — Výfuk

- **Architektura**: Single nebo Dual.
- **Svody** sahají od restriktivních kompaktních litinových systémů až po závodní tubular varianty.
- **Velikost svodů** a **průměr potrubí** ovlivňují rychlost plynů a schopnost odvést velké množství výfukových plynů.
- **Obtokové klapky** se nad 3500 RPM otevřou a obejdou tlumiče.
- **Katalyzátor** mění kompromis mezi emisní výbavou a restrikcí.
- **Dvě pozice tlumičů** umožňují kombinace od rovné roury po reverse-flow systémy.

Příliš malý výfuk postupně dusí horní část křivky momentu.

### Záložka 7 — Vozidlo a pohon

Tato nastavení ovlivňují **Zkušební jízdu** a **Simulaci okruhu**, nikoliv dyno křivku.

Výběr začíná na **Blank Vehicle**, kde jsou hodnoty záměrně prázdné. Před spuštěním Dyna ručně nastav všechny povinné položky nebo načti předvolbu vozu. **Custom** znamená, že jedna či více hodnot už přesně neodpovídá vestavěné předvolbě.

Nahoře nad všemi záložkami načítá **Preset motoru a vozu** kompletní kombinaci motoru a auta. **Předvolba vozu** uvnitř záložky 7 mění pouze vozidlo. Zvolení vestavěné předvolby vozu současně vypne vlastní jednotlivé převody, aby použila zamýšlenou automatickou převodovou sadu.

#### Šasi a rozložení hmotnosti

- **Hmotnost**: celková hmotnost vozidla včetně řidiče a náplní.
- **Umístění motoru**: Front Transverse, Front Longitudinal, Mid nebo Rear. Ovlivňuje vyvážení vozu a využití pneumatik.
- **Hmotnost vpředu / Hmotnost vzadu**: nastavuje se statický podíl na přední nápravě; zadní podíl se automaticky dopočítá do 100 %. Rozložení ovlivňuje trakci FWD/RWD i chování auta.
- **Rozvor**: vzdálenost mezi nápravami. Delší rozvor snižuje podélný přenos hmotnosti.
- **Výška těžiště**: vyšší těžiště vytváří větší přenos hmotnosti a zhoršuje využití pneumatik.

#### Aerodynamika

- **Základní odpor (Cd₀)**: odpor karoserie před započtením odporu vyvolaného přítlakem.
- **Čelní plocha**: referenční plocha používaná společně s Cd ve výpočtu odporu.
- **Přítlak (Cl·A)**: součin součinitele přítlaku a referenční plochy.
- **Aerodynamická účinnost**: určuje, kolik dodatečného odporu vytvoří zvolený přítlak.
- **Výsledný odpor (Cd)**: hodnota skutečně používaná Zkušební jízdou a Simulací okruhu. Zjednodušeně platí `výsledné Cd = základní Cd + (efektivní Cl·A / čelní plocha)² / aerodynamická účinnost`. Světlá výška navíc mění efektivní přítlak, takže vyšší přítlak už není bezplatná přilnavost na rovinkách.

#### Pneumatiky, odpružení a brzdy

- **Poloměr kola**: ovlivňuje sílu na kole i rychlost při daných otáčkách motoru.
- **Šířka pneumatik**: širší pneumatika lépe snáší vysoké zatížení, ale přidává valivý odpor.
- **Směs pneumatik**: Economy, Touring, Sport, Semi-Slick nebo Slick. Volba určuje základní tření i valivý odpor.
- **Vypočtená přilnavost**: hodnota odvozená ze směsi a šířky pneumatik, odpružení, těžiště, rozložení hmotnosti a koncepce vozidla.
- **Tuhost odpružení**: příliš měkké i příliš tvrdé nastavení zhoršuje využití pneumatik; vhodná oblast závisí na hmotnosti a přítlaku.
- **Světlá výška**: ovlivňuje účinnost podlahy a přítlaku. Velmi nízké měkké auto může narážet na dorazy.
- **Typ brzd / Průměr brzd**: Drum, Solid Disc, Vented Disc nebo Carbon Ceramic a jejich velikost určují dostupný mechanický brzdný účinek.
- **ABS**: zlepšuje využití dostupné přilnavosti pneumatik při brzdění.

#### Pohon a převodovka

- **Omezovač rychlosti**: elektronická maximální rychlost; hodnota `0` jej vypne. Zobrazená hodnota a rozsah slideru se řídí zvolenými km/h nebo mph, zatímco uložený build používá jednu kanonickou hodnotu.
- **Pohon nápravy**:
  - FWD má malé ztráty, ale při akceleraci se odlehčuje hnaná přední náprava.
  - RWD při akceleraci získává zatížení zadní nápravy.
  - AWD využívá trakci všech čtyř kol, ale má největší ztráty pohonu.
- **Diferenciál / Svornost LSD**: otevřený diferenciál může protočit odlehčené kolo. LSD s rostoucí svorností zlepšuje přenos síly, extrémní svornost ale může lehce zhoršit ochotu zatáčet.
- **Typ převodovky**: Manual, Automatic, DCT nebo Sequential. Typ mění mechanickou účinnost.
- **Počet převodů**: 4–8 stupňů.
- **Stálý převod**: násobí všechny převody v převodovce. Slider nabízí běžných 2,0–6,0; pro speciální převodovky lze ručně zadat 1,5–10,0.
- **Doba řazení**: skutečná doba přerušení tahu při řazení nahoru, používaná při akceleraci i v časové penalizaci na okruhu.
- **Launch control / Otáčky launch control**: při zapnutí systém při rozjezdu drží zvolené otáčky. Bez něj simulace používá opatrnější ruční rozjezd; příliš vysoké otáčky mohou stále způsobit prokluz.

#### Volitelné jemné nastavení převodů

Zaškrtávací políčko **Jemné nastavení jednotlivých převodů** je ve výchozím stavu vypnuté.

Když je vypnuté:

- editor převodů zůstává skrytý
- simulátor používá vestavěnou automatickou sadu pro zvolený počet stupňů
- existující presety si zachovávají své zavedené výsledky zrychlení a maximální rychlosti

Když je zapnuté:

- zobrazí se jedno pole pro každý aktivní převod
- podporovány jsou převodovky se 4–8 stupni
- tlačítko **Načíst automatické převody** obnoví výchozí sadu
- převody ovlivní následující Zkušební jízdu i Simulaci okruhu

U rozumně odstupňované převodovky má každý vyšší stupeň zpravidla numericky menší převodový poměr než stupeň před ním.

## 3. Spuštění Dyno Pullu

Klikni na **Spustit Dyno** ve stavbě motoru nebo na **1. Dyno Pull** na obrazovce Dyna. Simulátor zkontroluje vstupní hodnoty, přepne se na obrazovku Dyna, projede povolený rozsah otáček a v každém bodě spočítá točivý moment a výkon. Vložený graf, otáčky, moment a výkon se během měření průběžně aktualizují.

Build mohou zastavit dvě nezávislé cesty selhání:

- **Mechanické přetočení**: omezovač RPM překročí limit nejslabší klikové hřídele, ojnic nebo pístů.
- **Klepání a detonace**: vypočítaný knock index je příliš vysoký kvůli nebezpečné kombinaci komprese, plnicího tlaku, předstihu, AFR, palivové mapy, oktanového čísla, vstřikování, materiálu hlavy nebo technologické úrovně.

Konzole vysvětlí příčinu selhání i hlavní úpravy, které jej mohou odstranit.

Po úspěšném pullu:

- dokončený graf zůstane přímo na obrazovce Dyna
- tlačítko **Graf** tě na tuto obrazovku vrátí z jiného režimu
- zpřístupní se Ruční plyn, Zkušební jízda a Simulace okruhu
- pokud zvukový backend chybí, Ruční plyn a Zkušební jízda pokračují v tichém režimu

Výsledek Dyna je snímek motoru v okamžiku měření. Změna motorového parametru výsledek zneplatní a závislé režimy znovu zamkne, dokud neproběhne nový pull. Parametry samotného vozidla můžeš měnit bez nového výpočtu motorové křivky. Opuštění obrazovky Dyna během nedokončeného pullu měření bezpečně zruší a neúplný výsledek zahodí.


### Vysokootáčkové motorsportové motory

Verze 4.9 přidává úzce zaměřenou podporu extrémních atmosférických závodních motorů. Nejde o obecný násobič výkonu: simulátor postupně rozpoznává, zda build skutečně odpovídá vysokootáčkové architektuře.

Pro plné využití rozsahu nad 12 000 RPM je potřeba kombinace vysoké technologické úrovně, agresivního profilu vačky, výrazně nadčtvercové geometrie, rozvodů DAOHC, ITB, závodního sání, atmosférického plnění, billetové klikové hřídele, titanových ojnic a LW Forged pístů. Čím více se build této kombinaci blíží, tím vyšší mechanický limit, dovolenou pístovou rychlost a vysokootáčkové dýchání získá.

Běžné silniční motory tím nejsou automaticky posílené a vestavěné presety si zachovávají své dosavadní výsledky. Ručně zadaný extrémní limit bez odpovídajících dílů motor stále zničí.

## 4. Ruční plyn

Ruční plyn je živý test vytáčení motoru a chlazení zobrazený uvnitř hlavního okna aplikace.

Držením tlačítka se motor přibližuje k omezovači. Produkce tepla závisí na zatížení a výkonu motoru, zatímco účinnost chladiče určuje rychlost odvodu tepla. Při dosažení mezní teploty selže těsnění pod hlavou.

Tento režim je oddělený od dyno selhání způsobeného klepáním nebo mechanickým přetočením. Režim opustíš přes levé menu nebo klávesou **Esc**; naplánované fyzikální aktualizace a zvukový stream se bezpečně zastaví.

## 5. Zkušební jízda

Zkušební jízda simuluje start z místa, automatické řazení, zrychlení 0–100 km/h nebo 0–60 mph podle zvolených jednotek a maximální rychlost.

Model používá:

- kompletní křivku momentu motoru
- automatické nebo vlastní převody
- typ převodovky, nastavenou dobu řazení, stálý převod a poloměr kola
- účinnost pohonu, chování diferenciálu a volitelný Launch control
- umístění motoru, rozložení hmotnosti vpředu/vzadu, rozvor, výšku těžiště a podélný přenos hmotnosti
- šířku a směs pneumatik, tuhost odpružení a světlou výšku
- konstrukci a průměr brzd a ABS
- aerodynamický odpor z výsledného Cd a čelní plochy
- valivý odpor podle směsi a šířky pneumatik
- přítlak upravený světlou výškou a odpor, který tento přítlak vyvolává
- otáčkový i elektronický rychlostní limit

Indikátor TCS ukazuje prokluz kol. Maximální rychlost může omezit dostupný výkon, odpor vzduchu, nejvyšší převod a redline nebo elektronický omezovač.

Živá jízda a tlačítko **Přeskočit na max** sdílejí jeden autoritativní výpočet vozidla, takže obě cesty skončí stejným časem zrychlení, maximální rychlostí a výsledným převodem. Po zaznamenání výsledku živé zobrazení pustí plyn a nechá auto přirozeně dojíždět, zatímco naměřená maximálka zůstane viditelná.

Přepnutí mezi km/h a mph okamžitě upraví zobrazenou rychlost, text maximálky, omezovač rychlosti a cíl měření zrychlení, aniž by změnilo fyziku.

## 6. Simulace okruhu

Simulace okruhu počítá deterministické **letmé kolo**, nikoliv kolo se startem z klidu.

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
- typ převodovky, nastavenou dobu řazení, stálý převod, poloměr kola, redline a omezovač rychlosti
- hmotnost, umístění motoru, rozložení hmotnosti, rozvor, výšku těžiště, diferenciál a ztráty pohonu
- základní/výsledné Cd, čelní plochu, aerodynamickou účinnost a valivý odpor
- šířku a směs pneumatik, tuhost odpružení, světlou výšku a aerodynamický přítlak
- typ a průměr brzd a ABS
- třecí kružnici pneumatik, takže zatáčení ubírá grip dostupný pro akceleraci nebo brzdění
- zpětné průchody, které vytvoří brzdné zóny před zatáčkami
- dopředné průchody, které omezí akceleraci mezi body dráhy
- nastavenou dobu řazení nahoru a z ní odvozenou kratší penalizaci podřazení

Animace je zrychlená, aby dlouhé simulované kolo nevyžadovalo stejnou dobu skutečného čekání.

Po dokončení se zobrazí:

- celkový čas kola
- časy sektoru 1, sektoru 2 a sektoru 3
- průměrná rychlost ve zvolených jednotkách
- maximální rychlost ve zvolených jednotkách

Délka okruhu zůstává v obou režimech pevným benchmarkem 3,605 km.

Model je deterministický, takže shodný build vytvoří shodný čas. Okruh je proto vhodný jako společný benchmark pro porovnávání aut uvnitř simulátoru.

## 7. Zvuk motoru

Pokud jsou dostupné `sounddevice` a funkční PortAudio, zvuk motoru se syntetizuje živě z otáček, počtu válců, typu plnění, polohy plynu a typu klikové hřídele.

Turbo motory obsahují zvuk náběhu a flutter při ubrání. Kompresorové motory dostávají kvílení závislé na otáčkách.

Pokud zvukový backend není dostupný, simulátor zůstává plně použitelný. Ruční plyn a Zkušební jízda běží v tichém režimu a Nastavení nabídne příkaz `pip install -r requirements.txt`.

## 8. Uložení a načtení

Otevři **Nastavení** a přes **Uložit motor / vozidlo jako...** ulož aktuální build do JSON souboru. Volbou **Načíst motor / vozidlo...** ve stejném panelu jej obnovíš.

Formát v4.10.2 ukládá **Název vozu / projektu** a **Preset motoru a vozu** samostatně. Soubor dále obsahuje všechna nastavení motoru, zvolenou předvolbu vozu, kompletní dynamiku vozidla z v4.10, přepínač vlastních převodů i hodnoty všech jednotlivých převodových poměrů. Jazyk a volba km/h/mph jsou nastavení rozhraní, nikoliv data vozidla. Omezovač rychlosti se ukládá v kanonické hodnotě a při volbě mph se pouze převádí pro zobrazení.

Při načítání:

- simulátor nejprve obnoví bezpečné tovární hodnoty
- název projektu a identita presetu se obnoví nezávisle
- uložený preset vozidla se použije jako základ a explicitní hodnoty vozidla ze souboru se aplikují až nad něj
- uložené hodnoty se ověří proti číselným rozsahům a povoleným volbám rozbalovacích seznamů
- Boolean položky musí obsahovat skutečné JSON hodnoty `true` nebo `false`, ne text či číslo
- starší soubory bez parametrů z v4.10 dostanou kompatibilní odvozené nebo výchozí hodnoty
- české interní názvy speciálních presetů uložené verzemi v4.10 nebo v4.10.1 se převedou na současné anglické identifikátory
- starý Boolean formát VVL se převede automaticky
- neplatný nebo poškozený soubor obnoví předchozí aktivní build a zobrazí chybový overlay místo částečně aplikovaných hodnot

## 9. Řešení problémů

- **Jednorázová chyba při spuštění předkompilovaného exe**: antivirus může během prvního skenu krátce zamknout nepodepsaný single-file spustitelný soubor. Po dokončení kontroly aplikaci spusť znovu.
- **Chybí banner nebo vlastní ikona**: nech `automation_diy_banner.png`, `automation_diy_icon.png` a `automation_diy_icon.ico` vedle zdrojového skriptu, případně je přibal přes PyInstaller podle `README.cz.md`. Pokud obrázek není dostupný, simulátor záměrně použije textovou hlavičku.
- **Dyno hlásí neúplný prázdný projekt nebo vozidlo**: zadej název projektu a nastav všechna povinná prázdná pole, nebo načti kompletní Preset motoru a vozu.
- **Aplikace zůstala ve fullscreenu**: stiskni **F11**. Z Garáže fullscreen opustíš také klávesou **Esc**.
- **Nefunguje živý zvuk**: simulace dál fungují v tichém režimu. Spusť `pip install -r requirements.txt`, zkontroluj PortAudio a ověř funkční výchozí výstupní zařízení.
- **Zkušební jízda nebo Simulace okruhu jsou vypnuté**: nejprve dokonči úspěšný Dyno Pull. Zničený motor nelze testovat.
- **Dyno hlásí, že byl motor změněn**: po posledním pullu se upravil motorový parametr. Před otevřením závislých režimů spusť nové měření.
- **Vlastní převody nejsou vidět**: v záložce Vozidlo a pohon zapni **Jemné nastavení jednotlivých převodů**.
- **Preset po změně převodů dává jiné výsledky**: vlastní převody vypni nebo stiskni **Načíst automatické převody**.
