# User Guide

*[Návod v češtině](NAVOD.md)*

This guide walks through every part of the app in the order you'd typically use them. In-app tooltips (hover over any label or field) give quick per-parameter explanations — this document is the bigger-picture reference.

## 1. Overall Workflow

1. Pick a starting point from the preset dropdown at the top of the window, or start from the defaults.
2. Configure your engine across the **7 tabs**.
3. Click **"1. Dyno Pull"** to run the virtual dyno test.
4. Click **"Graph"** to view the torque/HP curve.
5. Optionally, click **"2. Manual Throttle"** for a hands-on telemetry test with cooling behavior.
6. Click **"3. Test Drive"** to see how the engine performs in an actual car (0–100 time, top speed).
7. Name your engine and use **File → Save Engine As...** to store your build as a `.json` file you can reload or share later.

Changing your language (CZ/EN radio buttons at the top) can be done at any time and doesn't affect your current build.

## 2. The 7 Tabs

### Tab 1 — Block
Sets the fundamental layout of the engine.
- **Configuration**: Inline (cheap, smooth, gets impractically long with many cylinders) / V (compact, great for 6–8 cylinders) / Boxer (opposed pistons, lowest center of gravity).
- **V-angle**: only relevant for V engines — 60° suits V6, 90° is the classic V8 angle for balance, 120° is very flat but very wide.
- **Cylinders**: 3–5 for small, cheap builds; 6–8 as the performance standard; 10–16 for exotic hypercar-tier builds.
- **Block material**: Cast Iron (heavy, indestructible) through Aluminium (standard, with Heavy/Light sub-variants for a weight-vs-durability trade-off) and AlSi (Heavy/Light — no cylinder liners, lower friction) to Aluminium Billet (machined from a single block, race-grade) and Magnesium (lowest friction, motorsport-grade).
- **Bore / Stroke**: bore controls piston diameter (bigger bore → bigger valves → better high-RPM airflow); stroke controls piston travel (bigger stroke → strong low-end torque, but physically caps how high the engine can rev).
- **Radiator efficiency**: how effectively the engine sheds heat — this is your buffer against overheating in the Manual Throttle test.
- **Technology Level (Tech Level)**: determines the era of your engine (from historic 60s engines through the modern standard of 100, up to cutting-edge 115+ builds). This acts as a global multiplier — it fundamentally affects overall combustion efficiency, engine breathing, internal friction, and crucially, the baseline knock resistance.

### Tab 2 — Bottom End
This is where the engine's mechanical RPM ceiling is decided.
- **Crankshaft / Conrods / Pistons materials** each carry their own independent RPM limit, now with finer Heavy/Light tiers within each material family (e.g. Cast crank ≈ 6500 RPM, Forged Steel Light ≈ 8800 RPM, Billet ≈ 11500 RPM; similar tiers exist for conrods and pistons, including a Hypereutectic Cast piston option for a durable, emissions-friendly middle ground). On the dyno, the **weakest of the three** determines the actual mechanical limit — upgrading just one part won't help if another is still the bottleneck.
- **Balancer**: None / Harmonic Damper (+200 RPM, small friction cost) / Full Balancers (+500 RPM, bigger friction cost). Choosing Harmonic Damper or Full Balancers reveals an extra **balancer weight slider (0–50 kg)** for continuous fine-tuning: more added weight pushes the mechanical RPM limit further up, but increases internal friction and slows the engine's throttle response.

### Tab 3 — Top End
Head and valvetrain configuration — this heavily influences knock risk.
- **Head material**: Cast Iron (Eco/Std/Perf tiers — Eco is cheap but knock-prone, Perf has better flow) retains heat and increases detonation risk; Aluminium (Eco/Std/Perf) dissipates heat and lowers it; Aluminium Billet Race is the race-grade option with the best heat dissipation and lowest friction.
- **Valvetrain**: Pushrod (OHV, chokes past ~4200 RPM) / SOHC / DOHC (best for high RPM) / DAOHC (race-only, direct actuation).
- **Valves per cylinder**: 2 (strong low-end, chokes up top) to 5 (extreme top-end, race-oriented).
- **VVT**: variable valve *timing* — None (fixed) / Intake (smooths delivery) / All (broadens the curve across the whole rev range).
- **VVL**: variable valve *lift*, now a 3-state choice — None (fixed lift) / VVL (switches to a sharper cam profile above a set RPM) / CVVL (continuously variable, smoothest and most efficient blend). Selecting VVL or CVVL reveals two extra sliders: **VVL Profile** (how aggressive the secondary cam profile is) and **VVL Switch RPM** (exactly where the engine transitions to it).
- **Valve spring stiffness**: a new slider — stiffer springs (higher values) let the engine safely rev higher without valve float (valves "bouncing" instead of closing properly), at the cost of a bit more friction and slightly reduced power.
- **Cam profile**: low values bias torque low in the rev range; high values push an aggressive, top-end-biased, rougher-idling character.
- **Compression ratio**: more compression means more power, but sharply increases knock risk (unless you're running Diesel, which ignores these limits).

### Tab 4 — Aspiration
- **Type**: NA (naturally aspirated, immediate throttle response) / Turbo (exhaust-driven, has lag) / Supercharger (belt-driven, instant response).
- **Turbo bearing**: Journal (cheap, slower spool) vs. Ball Bearing (drastically cuts turbo lag).
- **Turbo configuration**: Single (most lag) / Twin (faster spool) / Quad (fastest spool on big engines).
- **Intercooler size**: bigger protects against knock but adds a bit of lag.
- **Turbo/Supercharger size & boost pressure**: bigger units flow more air but take longer to spool (turbo) or sap more parasitic power (supercharger) just to spin up.

### Tab 5 — Fuel & Tune
This tab, together with Tab 3, drives the **knock/detonation** failure model.
- **Fuel delivery**: Carburetor (worse atomization, more knock risk) / Mechanical Fuel Injection (race-style, high fuel consumption) / Single Point EFI (basic single-injector setup) / EFI Multi-point (modern standard) / Direct Injection (cools cylinders internally, cuts knock risk, adds power). A new **carburetor/throttle body size slider** lets you fine-tune between low-RPM torque (smaller) and high-RPM breathing (larger).
- **Intake configuration**: Single / Twin / ITB (independent throttle bodies — sharp response, strong top-end).
- **Manifold**: now spans Standard (with Low/Mid sub-tiers), Performance (with Mid/High sub-tiers), Race, Compact, and Variable (broadens the effective rev range) — trading peak power for packaging or midrange. A **manifold size slider** fine-tunes intake runner width alongside the preset choice.
- **Fuel type**: octane rating, now with more granularity — Low Quality 85 and Regular 91 at the bottom, Premium 95 and Super 98 as solid middle choices, Ultimate 100/E85/Methanol/Compressed Gas/Leaded Gasoline for high-boost builds, Diesel (never detonates), and **Nitromethane** — an extreme, high-risk/high-reward fuel that unlocks a much higher power ceiling than anything else, at real risk to engine longevity.
- **Fuel map**: a new slider separate from AFR — leaning it out (0–40) trims fuel consumption but sharply raises knock risk and slightly hurts power, while richening it (60–100) helps cool the cylinders and slightly boosts power.
- **AFR (air-fuel ratio)**: 14.7 is stoichiometric/"perfect" combustion; 12.5–13.0 is a rich mixture for max power; 15+ is lean and sharply raises knock risk.
- **Ignition timing**: more advance = more power, but aggressive timing combined with high compression is a fast route to melted pistons.
- **RPM limiter**: this is the number the dyno actually enforces. If you set it above the mechanical limit from Tab 2, the engine **will** blow up on the pull — that's intentional, not a bug.

### Tab 6 — Exhaust
- **Architecture**: Single vs. Dual (dual effectively doubles total exhaust cross-section).
- **Headers**: now a finer spectrum from Compact Cast (most restrictive) through Cast (Low/Mid/Standard tiers) to Tubular (Standard/Mid/Long/Race tiers, progressively less restrictive). A **header size slider** lets you fine-tune within whichever tier you pick.
- **Pipe diameter**: too small a diameter for a high-power engine chokes the top of the curve.
- **Exhaust bypass valves**: a new option — with valves fitted, the exhaust bypasses the mufflers entirely above 3500 RPM for maximum flow at high RPM, at the cost of being louder there; below that threshold the mufflers work normally.
- **Catalytic converter**: None (max flow) through 2-way/3-way (some restriction), an Exhaust Reactor, and up to sport-oriented High Flow and Pre-Cat combinations (Three-Way + Pre-Cat, High Flow 3-Way + Pre-Cat) that recover most of the flow a plain catalytic converter would cost.
- **Mufflers (x2)**: None (straight-through, no restriction) → Straight → Baffled → Reverse Flow (quietest, most restrictive).

### Tab 7 — Drivetrain
Everything here only matters for the **Test Drive** simulation, not the dyno.
- **Vehicle preset**: quickly sets chassis values to a typical example of a vehicle category.
- **Weight**: total car + driver + fluids mass — the core F = m·a term for acceleration.
- **Drag coefficient (Cd)**: aerodynamic drag, mainly caps top speed.
- **Tire grip**: how much force the tires can put down before spinning — this limits your launch, not raw horsepower. This value also acts as an indicator for aerodynamic downforce; sporty cars (grip > 1.0) will dynamically generate downforce at high speeds, improving stability and high-speed grip.
- **Gears / Final drive**: more gears keep the engine in its ideal RPM band longer; a higher final drive ratio means shorter gearing (better acceleration, lower top speed, more shifting).
- **Drivetrain layout**: FWD (loses traction under acceleration due to weight transfer) / RWD (gains traction under acceleration) / AWD (best overall traction).

## 3. Running the Dyno Pull

Click **"1. Dyno Pull"**. The simulator sweeps RPM and computes torque/HP at each point. Two independent things can end the pull early with a failure:

- **Mechanical over-rev**: if your RPM limiter (Tab 5) is set above the weakest of crank/conrod/piston limits (Tab 2), the pull stops there and tells you exactly which part failed and how to fix it (upgrade that part, or lower the limiter).
- **Knock/detonation**: a "knock index" is computed from compression, ignition timing, AFR, fuel map, fuel octane, and head material. Past a threshold, the engine detonates and melts a piston — even at RPM well below the mechanical limit. The failure message tells you which levers to pull back (lower compression/boost/ignition, use higher octane, richer AFR/fuel map). Running Nitromethane raises the power ceiling dramatically but doesn't relax this model — it's a genuine high-risk choice, not a free upgrade.

Click **"Graph"** afterward to see the resulting torque/HP curve.

## 4. Manual Throttle (Telemetry)

This is a live, hands-on test rather than an instant sweep. Hold the throttle button down and watch coolant temperature climb in real time. Your **radiator efficiency** (Tab 1) is what determines how long you can hold wide-open throttle before overheating. If coolant temperature goes too high, you get a blown head gasket — a separate failure mode from anything on the dyno.

## 5. Test Drive

Simulates a 0–100 km/h run and top speed using your Tab 7 chassis settings combined with your engine's torque curve:
- **Launch control** manages the initial RPM to avoid bogging down.
- **Weight transfer and Aerodynamics** shifts load onto the front or rear axle under acceleration, and computes downforce at higher speeds based on the vehicle's grip and aerodynamic drag. This changes how much force your drive wheels can put down before slipping — watch the **TCS/slip indicator**.
- **Gear shifts** happen automatically near the ideal shift RPM, with a short shift-delay penalty.
- The run ends automatically once acceleration flattens out, reporting your 0–100 time and top speed.

## 6. Engine Sound

If `sounddevice` and a working PortAudio backend are available, the engine note is synthesized live — frequency and harmonic content are derived from RPM, cylinder count, and crank type, with a flutter effect on throttle lift-off for turbocharged engines. If the sound backend isn't available on your system, the sound button is disabled and everything else works exactly the same, just silently.

## 7. Save / Load

Use **File → Save Engine As...** to write your current build (every parameter across all 7 tabs) to a `.json` file, and **File → Load Engine...** to bring it back later or share it with someone else running the app. Engine files saved with older app versions (including the old on/off VVL setting) load correctly — they're automatically converted to the current format.

## 8. Troubleshooting

- **A one-off `ModuleNotFoundError` on first launch of the prebuilt `.exe`**: this is caused by antivirus software briefly locking a file during its first-time scan of the unsigned executable. Just relaunch the app — it will not recur once the antivirus has scanned and cached the file.
- **No sound at all**: confirm `sounddevice` and PortAudio are installed if running from source, or check your system's default audio output device.
