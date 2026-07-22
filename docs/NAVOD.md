# Návod k použití

*[User Guide in English](USER_GUIDE.md)*

Tento návod prochází appku v pořadí, v jakém ji typicky používáš. Tooltips přímo v appce (najetí myší na jakýkoliv popisek nebo pole) dávají rychlé vysvětlení k jednotlivým parametrům — tenhle dokument slouží jako přehled souvislostí.

## 1. Celkový postup práce

1. Vyber startovní bod z rozbalovacího seznamu předvoleb nahoře, nebo začni od výchozích hodnot.
2. Nastav motor napříč **7 záložkami**.
3. Klikni na **"1. Dyno Pull"** a spusť virtuální dyno test.
4. Klikni na **"Graf"** a zobraz si křivku točivého momentu a výkonu.
5. Volitelně klikni na **"2. Ruční plyn"** pro praktický test s telemetrií a chlazením.
6. Klikni na **"3. Zkušební Jízda"** a podívej se, jak si motor vede v reálném autě (čas 0-100, maximálka).
7. Pojmenuj svůj motor a přes **Soubor → Uložit motor jako...** si build ulož do `.json` souboru, ke kterému se můžeš vrátit nebo ho poslat dál.

Jazyk appky (přepínač CZ/EN nahoře) můžeš měnit kdykoliv za chodu, aniž by to ovlivnilo rozpracovaný build.

## 2. Přehled 7 záložek

### Záložka 1 — Block
Základní koncepce motoru.
- **Konfigurace**: Inline (levné, plynulé, u mnoha válců nepraktricky dlouhé) / V (kompaktní, skvělé pro 6–8 válců) / Boxer (protiběžné písty, nejnižší těžiště).
- **Úhel V**: relevantní jen u V motorů — 60° pro V6, 90° klasika pro V8 kvůli vyvážení, 120° velmi ploché, ale extrémně široké.
- **Počet válců**: 3–5 pro malé, levné buildy; 6–8 jako výkonnostní standard; 10–16 pro exotické supersporty.
- **Materiál bloku**: Litina (těžká, nezničitelná) přes Hliník (standard, s podvarianty Heavy/Light pro poměr váha/odolnost) a AlSi (Heavy/Light — bez vložek válců, nižší tření) až po Aluminium Billet (frézovaný z jednoho kusu, závodní úroveň) a Hořčík (nejnižší tření, motorsportová úroveň).
- **Vrtání / Zdvih**: vrtání určuje průměr pístu (větší vrtání → větší ventily → lepší průtok při vysokých otáčkách); zdvih určuje dráhu pístu (větší zdvih → silný točivý moment dole, ale fyzicky omezuje maximální otáčky).
- **Účinnost chladiče**: jak efektivně motor odvádí teplo — tohle je tvá rezerva proti přehřátí v testu s ručním plynem.
- **Technologická úroveň (Tech Level)**: určuje éru tvého motoru (od historických motorů z 60. let přes moderní standard s hodnotou 100 až po špičkové high-tech motory 115+). Tento parametr funguje jako globální násobič – zásadně ovlivňuje celkovou účinnost spalování, dýchání motoru, vnitřní tření a hlavně základní odolnost proti klepání.

### Záložka 2 — Bottom End
Tady se rozhoduje o mechanickém stropu otáček motoru.
- **Materiál klikovky / ojnic / pístů** má každý svůj vlastní nezávislý limit otáček, teď s jemnějšími Heavy/Light úrovněmi v rámci každé materiálové rodiny (např. sériová klikovka ≈ 6500 RPM, Forged Steel Light ≈ 8800 RPM, billet ≈ 11500 RPM; podobné úrovně platí i pro ojnice a písty, včetně nové varianty Hypereutectic Cast pístu jako odolného kompromisu vhodného i na emise). Na dynu rozhoduje **nejslabší ze tří dílů** — vylepšení jen jednoho dílu nepomůže, pokud je úzkým hrdlem jiný.
- **Vyvažováky**: Žádné / Harmonic Damper (+200 RPM, malé tření navíc) / Full Balancers (+500 RPM, větší tření navíc). Při volbě Harmonic Damper nebo Full Balancers se odkryje nový **slider váhy vyvažováků (0–50 kg)** pro plynulé doladění: víc přidané váhy dál zvedá mechanický limit otáček, ale zvyšuje vnitřní tření a zpomaluje reakci motoru na plyn.

### Záložka 3 — Top End
Hlava a rozvody — tohle výrazně ovlivňuje riziko klepání.
- **Materiál hlavy**: Litina (úrovně Eco/Std/Perf — Eco je levná, ale náchylná ke klepání, Perf má lepší průtok) drží teplo a zvyšuje riziko detonace; Hliník (Eco/Std/Perf) teplo odvádí a riziko snižuje; Alu Billet Race je závodní varianta s nejlepším odvodem tepla a nejnižším třením.
- **Rozvody**: Pushrod/OHV (dusí se nad ~4200 RPM) / SOHC / DOHC (nejlepší pro vysoké otáčky) / DAOHC (čistě závodní, přímé ovládání).
- **Ventilů na válec**: 2 (silné dole, dusí se nahoře) až 5 (extrémní výkon nahoře, závodně orientované).
- **VVT**: variabilní **časování** ventilů — Žádné (pevné) / Intake (vyhladí dodávku výkonu) / All (rozšíří křivku přes celé spektrum otáček).
- **VVL**: variabilní **zdvih** ventilů, teď jako volba ze 3 stavů — Žádný (pevný zdvih) / VVL (přepne na ostřejší profil vačky nad danými otáčkami) / CVVL (plynule variabilní, nejhladší a nejúčinnější přechod). Volbou VVL nebo CVVL se odkryjí dva další slidery: **VVL Profil** (jak agresivní je druhý, ostřejší profil vačky) a **VVL Otáčky** (přesně kde k přepnutí dojde).
- **Tuhost pružin ventilů**: nový slider — tvrdší pružiny (vyšší hodnoty) umožní motoru bezpečně točit vyšší otáčky bez odskakování ventilů (valve float), za cenu trochu vyššího tření a mírně nižšího výkonu.
- **Profil vačky**: nízké hodnoty posouvají moment do nízkých otáček; vysoké hodnoty dávají agresivní charakter s výkonem nahoře a nepravidelným volnoběhem.
- **Kompresní poměr**: víc komprese = víc výkonu, ale prudce roste riziko klepání (kromě nafty, ta tyhle limity ignoruje).

### Záložka 4 — Aspiration
- **Typ**: NA (atmosférický, okamžitá reakce) / Turbo (poháněné výfukem, má lag) / Kompresor (poháněný řemenem, okamžitá reakce).
- **Ložiska turba**: Kluzná (levná, pomalejší náběh) vs. Kuličková (razantně zkracují turbo lag).
- **Konfigurace turba**: Single (nejvíc lagu) / Twin (rychlejší roztočení) / Quad (nejrychlejší reakce u velkých motorů).
- **Velikost intercooleru**: větší chrání před klepáním, ale mírně zvětšuje lag.
- **Velikost turba/kompresoru a tlak**: větší jednotky nafouknou víc vzduchu, ale déle se roztáčí (turbo), nebo si berou víc výkonu jen na to, aby se vůbec roztočily (kompresor).

### Záložka 5 — Fuel & Tune
Tahle záložka spolu se záložkou 3 pohání model **klepání/detonace**.
- **Vstřikování**: Karburátor (horší odpařování, víc klepání) / Mechanical Fuel Injection (závodní, obří spotřeba) / Single Point EFI (základní jednotryskové vstřikování) / EFI Multi-point (moderní standard) / Přímý vstřik (chladí válce zevnitř, snižuje klepání, přidává výkon). Nový **slider velikosti karburátoru/škrticí klapky** umožňuje doladit mezi krouťákem dole (menší) a dýcháním nahoře (větší).
- **Konfigurace sání**: Single / Twin / ITB (nezávislé klapky — ostrá odezva, silný výkon nahoře).
- **Sací svody**: teď zahrnují Standard (s podúrovněmi Low/Mid), Performance (s podúrovněmi Mid/High), Race, Compact a Variable (rozšíří efektivní pásmo otáček) — mění poměr špičkového výkonu vůči zabudovatelnosti nebo výkonu uprostřed. **Slider velikosti sání** dolaďuje šířku sacích kanálů nezávisle na zvolené úrovni.
- **Druh paliva**: oktanové číslo, teď s jemnějším odstupňováním — Low Quality 85 a Regular 91 jako nejhorší volby, Premium 95 a Super 98 jako solidní střed, Ultimate 100/E85/Metanol/Compressed Gas/Leaded Gasoline pro velká turba, nafta (nikdy nedetonuje) a **Nitromethane** — extrémní palivo s vysokým rizikem i odměnou, které odemyká výrazně vyšší výkonový strop než cokoliv jiného, ale za reálné riziko životnosti motoru.
- **Fuel map**: nový slider oddělený od AFR — ochuzení směsi (0–40) snižuje spotřebu, ale prudce zvyšuje riziko klepání a mírně ubírá výkon; obohacení (60–100) pomáhá chladit válce a mírně přidá výkon.
- **Směs (AFR)**: 14,7 je stechiometrické/"dokonalé" spalování; 12,5–13,0 je bohatá směs pro maximální výkon; 15+ je chudá směs a prudce zvyšuje riziko klepání.
- **Předstih**: víc předstihu = víc výkonu, ale agresivní předstih spolu s vysokou kompresí rychle roztaví písty.
- **Omezovač RPM**: tohle číslo dyno skutečně vynucuje. Pokud ho nastavíš nad mechanický limit ze záložky 2, motor na pullu **vybuchne** — to je záměr, ne chyba.

### Záložka 6 — Exhaust
- **Architektura**: Single vs. Dual (Dual efektivně zdvojnásobí celkový průřez výfuku).
- **Svody**: teď jemnější spektrum od Compact Cast (nejvíc restriktivní) přes Cast (úrovně Low/Mid/Standard) až po Tubular (úrovně Standard/Mid/Long/Race, postupně méně restriktivní). **Slider velikosti svodů** umožňuje doladit v rámci zvolené úrovně.
- **Průměr potrubí**: příliš malý průměr u výkonného motoru udusí vršek křivky.
- **Výfukové obtokové klapky**: nová volba — s klapkami výfuk nad 3500 RPM úplně obejde tlumiče kvůli maximálnímu průtoku, za cenu vyšší hlučnosti v tomhle pásmu; pod touto hranicí fungují tlumiče normálně.
- **Katalyzátor**: Žádný (max průtok) přes 2-way/3-way (mírná restrikce), Exhaust Reactor, až po sportovní High Flow a Pre-Cat kombinace (Three-Way + Pre-Cat, High Flow 3-Way + Pre-Cat), které vrátí většinu průtoku, co by klasický katalyzátor stál.
- **Tlumiče (2x)**: Žádný (rovná roura, bez restrikce) → Straight → Baffled → Reverse Flow (nejtišší, nejvíc restriktivní).

### Záložka 7 — Drivetrain
Vše zde má vliv jen na simulaci **Zkušební jízdy**, ne na dyno.
- **Předvolba vozu**: rychle nastaví hodnoty šasi podle typického zástupce dané kategorie.
- **Váha**: celková hmotnost auta + řidiče + náplní — základní člen F = m·a pro zrychlení.
- **Odpor vzduchu (Cd)**: aerodynamický odpor, hlavně omezuje maximální rychlost.
- **Trakce pneumatik**: kolik síly dokážou pneumatiky přenést, než se protočí — tohle omezuje tvůj start z místa, ne surový výkon. Tato hodnota nově figuruje i ve výpočtu aerodynamického přítlaku; sportovní vozy (grip > 1.0) ve vyšších rychlostech dynamicky generují přítlak k silnici.
- **Převody / Stálý převod**: víc rychlostních stupňů udrží motor déle v ideálním pásmu otáček; vyšší stálý převod znamená kratší převody (lepší zrychlení, nižší maximálka, víc řazení).
- **Pohon nápravy**: FWD (ztrácí trakci při zrychlení kvůli přenosu váhy) / RWD (získává trakci při zrychlení) / AWD (nejlepší celková trakce).

## 3. Spuštění Dyno Pull

Klikni na **"1. Dyno Pull"**. Simulátor projede rozsah otáček a v každém bodě spočítá točivý moment a výkon. Pull může předčasně skončit selháním ze dvou nezávislých důvodů:

- **Mechanické přetočení**: pokud je tvůj omezovač RPM (záložka 5) nastavený nad nejslabší ze tří limitů klikovka/ojnice/písty (záložka 2), pull se tam zastaví a řekne ti přesně, který díl selhal a jak to opravit (vylepšit daný díl, nebo snížit omezovač).
- **Klepání/detonace**: "knock index" se počítá z komprese, předstihu, směsi AFR, fuel map, oktanového čísla paliva a materiálu hlavy. Po překročení prahu motor zdetonuje a roztaví píst — klidně i výrazně pod mechanickým limitem otáček. Hlášení o selhání ti řekne, které páky zatáhnout zpátky (snížit kompresi/boost/předstih, použít vyšší oktany, obohatit směs/fuel map). Nitromethane sice dramaticky zvedne výkonový strop, ale model klepání kvůli tomu nijak nepoleví — je to reálně rizikové palivo, ne zadarmo dané vylepšení.

Poté klikni na **"Graf"** a zobraz si výslednou křivku točivého momentu a výkonu.

## 4. Ruční plyn (Telemetrie)

Tohle je živý, praktický test místo okamžitého sweepu. Drž tlačítko plynu a sleduj, jak v reálném čase roste teplota chladicí kapaliny. Tvoje **účinnost chladiče** (záložka 1) určuje, jak dlouho vydržíš na plný plyn, než se motor přehřeje. Pokud teplota kapaliny vyleze moc vysoko, praskne těsnění hlavy — samostatný mód selhání, odlišný od čehokoliv na dynu.

## 5. Zkušební Jízda

Simuluje zrychlení 0–100 km/h a maximální rychlost pomocí nastavení šasi ze záložky 7 v kombinaci s křivkou točivého momentu tvého motoru:
- **Launch control** řídí počáteční otáčky, aby motor "nezadusil".
- **Přenos váhy a aerodynamika** posouvá zátěž na přední nebo zadní nápravu při zrychlení, a ve vysokých rychlostech počítá s přítlakem, což mění, kolik síly dokážou hnaná kola přenést, než se protočí — sleduj **indikátor TCS/prokluzu**.
- **Řazení** probíhá automaticky blízko ideálních otáček pro řazení, s krátkým postihem za dobu řazení.
- Jízda se automaticky ukončí, jakmile zrychlení splasne, a appka ti nahlásí čas 0–100 a maximální rychlost.

## 6. Zvuk motoru

Pokud je dostupný `sounddevice` a funkční PortAudio backend, tón motoru se syntetizuje živě — frekvence a harmonické složky se odvíjí od otáček, počtu válců a typu klikovky, s efektem "flutter" při ubrání plynu u přeplňovaných motorů. Pokud zvukový backend na tvém systému není dostupný, tlačítko zvuku je vypnuté a všechno ostatní funguje úplně stejně, jen potichu.

## 7. Uložení / Načtení

Přes **Soubor → Uložit motor jako...** ulož aktuální build (všechny parametry napříč všemi 7 záložkami) do `.json` souboru, a přes **Soubor → Načíst motor...** ho zase načti, nebo ho pošli někomu dalšímu, kdo appku používá. Motory uložené ve starších verzích appky (včetně starého zapnuto/vypnuto nastavení VVL) se načtou správně — automaticky se převedou do aktuálního formátu.

## 8. Řešení problémů

- **Jednorázový `ModuleNotFoundError` při prvním spuštění přeloženého `.exe`**: způsobuje ho antivirus, který krátce zamkne soubor při jeho prvním skenování u nepodepsaného exe. Stačí appku spustit znovu — jakmile antivirus soubor jednou proskenuje a zapamatuje si ho, problém se znovu neobjeví.
- **Žádný zvuk**: pokud appku spouštíš ze zdrojáku, ověř, že máš nainstalovaný `sounddevice` a PortAudio, případně zkontroluj výchozí výstupní zvukové zařízení systému.
