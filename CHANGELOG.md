# Changelog

## v4.10.2 (Branding Update)

* **In-app branding:** Added the Automation DIY banner to the sidebar and applied the new icon to the application window and Windows taskbar.
* **Source and bundled asset loading:** Branding files are resolved next to the Python script, from an `assets` folder, from the PyInstaller bundle, or next to a frozen executable.
* **Safe visual fallback:** If a branding asset is missing or cannot be loaded, the simulator falls back to its original text header and continues running.
* **English internal preset names:** Renamed the special project and vehicle states to **Blank Project**, **Custom Setup**, **Blank Vehicle**, and **Custom** so saved identifiers remain understandable in both UI languages.
* **Legacy save compatibility:** Czech identifiers written by v4.10 and v4.10.1 are still recognized and translated to the current internal names while loading.
* **Version alignment:** Updated the application title, sidebar label, save-file format marker, source package, and documentation for v4.10.2.

## v4.10.1 (Blank Project Update)

* **Truly blank startup:** The simulator now starts with **Blank Project** and **Blank Vehicle** instead of silently loading the Mazda 6 engine and chassis values.
* **Required from-scratch configuration:** Blank engine and vehicle fields must be configured manually or filled by selecting a factory preset before a dyno pull can begin.
* **Separate project naming:** Added a dedicated **Car / Project Name** field independent from the **Engine & Vehicle Preset** selector.
* **Clear preset behavior:** Selecting a factory preset loads its complete engine and vehicle configuration and replaces the project name; the name can then be edited freely without applying another preset.
* **Custom-state tracking:** Editing technical values changes the preset indicator to **Custom Setup** or the vehicle selector to **Custom** without overwriting the chosen project name.
* **Save/load compatibility:** Project name and preset identity are stored separately, with inference and aliases for older save files.

## v4.10 (Vehicle Dynamics Update)

* **Vehicle architecture:** Added engine location, front/rear weight distribution, wheelbase, and centre-of-gravity height.
* **Detailed tires:** Replaced the single grip value for new builds with tire width and selectable Economy, Touring, Sport, Semi-Slick, or Slick compounds.
* **Braking system:** Added brake construction, brake diameter, and optional ABS, all used by braking calculations.
* **Suspension setup:** Added suspension stiffness and ride height, including tire-utilisation and floor/downforce-efficiency effects.
* **Differentials:** Added Open and LSD options with adjustable locking and traction/cornering trade-offs.
* **Transmission behavior:** Added Manual, Automatic, DCT, and Sequential gearbox types with real shift-interruption time.
* **Launch Control:** Added an independent Launch Control switch and target RPM for standing starts.
* **Induced aerodynamic drag:** Downforce now raises effective drag according to aerodynamic efficiency, so high-downforce setups gain cornering performance at the cost of straight-line speed.
* **Shared vehicle model:** Test Drive and Track Simulation now use the same resolved tire, aero, braking, suspension, differential, weight-transfer, gearing, and launch parameters.
* **Preset preservation:** Built-in presets were expanded with representative v4.10 vehicle values while retaining their established engine curves and benchmark performance.

## v4.9.1 (Localization & Tooltip Stability Update)

* **Complete runtime localization:** Finished Czech and English translation coverage across the builder, dyno graph, live telemetry, Test Drive, Track Simulation, result panels, status messages, buttons, and keyboard hints.
* **Live language switching:** Dynamic and already-completed screens now refresh immediately when the language changes, including the builder's **Run Dyno** button.
* **Stable tooltip lifecycle:** Only one tooltip can exist at a time. Tooltips are now reliably closed when the pointer leaves a control, another tooltip opens, the language changes, an overlay appears, or the active screen changes.
* **Version alignment:** Updated the application title, sidebar version label, and documentation for the public v4.9.1 release.

## v4.9 (High-RPM Motorsport Calibration Update)

* **High-RPM race-engine support:** Added a narrowly targeted motorsport model for extreme naturally aspirated, short-stroke, high-technology engines instead of applying a global power multiplier.
* **Manual RPM entry up to 20,000 RPM:** The normal slider remains focused on 3,000–12,000 RPM, while suitable race builds may enter a higher limiter manually.
* **Motorsport architecture detection:** High-RPM capability depends on a demanding combination of technology level, cam profile, oversquare geometry, DAOHC valvetrain, ITBs, race intake, NA aspiration, billet crankshaft, titanium connecting rods, and lightweight forged pistons.
* **Race-specific mechanical limits:** Qualifying motorsport builds receive progressive component and piston-speed limits suitable for engines approaching Formula-style RPM levels.
* **High-RPM breathing calibration:** Extreme race engines retain volumetric efficiency and power closer to the limiter, producing a realistic high-revving curve rather than peaking like a conventional road engine.
* **Expert manual ranges:** Slider ranges remain convenient for ordinary builds, while manual entry supports special values such as 20–150 mm stroke, 0.3–2.5 tire grip, and 1.5–10.0 final drive.
* **F1-style reference build:** Added support for a 3.0-litre V10 configuration producing roughly 940 HP near 19,000 RPM when correctly configured.
* **Road-car compatibility:** Existing built-in presets retain their established engine curves and vehicle performance.

## v4.8.x (Fullscreen, Responsiveness & Accessibility Updates)

* **Fullscreen single-window interface:** Rebuilt the GUI around one application shell with a permanent sidebar, embedded simulation screens, a consistent dark theme, and F11/Esc navigation.
* **Central Settings panel:** Added in-app Load, Save, language, speed-unit, audio-status, Close, and Quit controls.
* **Selectable speed units:** Added live km/h ↔ mph switching, including 0–100 km/h / 0–60 mph timing and canonical speed-limiter storage.
* **Embedded live dyno graph:** Torque and horsepower curves now draw progressively during the pull alongside live telemetry and the dyno console.
* **Unified Test Drive physics:** The live run and **Skip to Top Speed** use the same authoritative calculation, with matching acceleration, top speed, final gear, launch behavior, and natural coast-down.
* **Safe screen lifecycle:** Screen changes now cancel callbacks, audio, temporary files, interrupted pulls, active laps, and running vehicle simulations cleanly.
* **Responsive builder:** All seven tabs use adaptive vertical scrolling only when their content no longer fits the available height.
* **Responsive Track Simulation:** The circuit canvas scales to the available space; on narrow windows the information panel moves below the map and scroll activates only when required.
* **Silent audio fallback:** Manual Throttle and Test Drive remain usable when `sounddevice` or PortAudio is unavailable, with a visible installation guide and `requirements.txt`.
* **Stronger save/load and validation:** Added rollback-safe loading, dropdown and Boolean validation, exact limiter handling, preset final-drive fixes, and compatibility with older configurations.
* **Expert-value loading:** Special manually entered values are no longer rejected merely because they sit outside a slider's ordinary convenience range.
* **Presentation cleanup:** Renamed the automated circuit mode to **Track Simulation** and expanded Czech localization across the builder.

## v4.7.x (Custom Gearing & Test Track Update)

* **Optional individual gear ratios:** Added a hidden-by-default fine-tuning panel for 4–8-speed transmissions. When disabled, the simulator uses the original automatic ratio sets exactly as before.
* **Preset-safe gearing:** Selecting a built-in vehicle preset disables custom ratios, preserving the preset's established acceleration and top-speed behavior.
* **Shared transmission model:** Automatic and custom ratios are now used consistently by the 0–100/top-speed calculation, the animated Test Drive, and the Test Track.
* **3.605 km Test Track:** Added a deterministic flying-lap benchmark with three timed sectors, live speed/gear/sector telemetry, average speed, maximum speed, and an accelerated lap animation.
* **Geometry-based circuit physics:** Replaced the separate cosmetic track map and abstract corner list with one closed circuit geometry used for both rendering and simulation.
* **Curvature-derived corner limits:** The circuit is resampled into short distance steps; local curvature is converted into corner radii and used to calculate corner-speed limits.
* **Braking and acceleration passes:** Added cyclic backward passes for braking zones and forward passes for achievable acceleration around the complete closed lap.
* **Friction-circle behavior:** Cornering load reduces the tire grip available for acceleration and braking.
* **Track gearing and aero:** Lap time responds to engine torque, individual ratios, final drive, drivetrain losses, wheel radius, redline, speed limiter, weight, Cd, frontal area, tire grip, downforce, rolling resistance, and shift penalties.
* **Accurate track animation:** The animated car now follows the exact same points and distance scale used by the lap-time physics.

## v4.6 (Reviewed Physics & Stability Update)

* **Runtime stability:** Fixed a `math domain error` that could occur when extreme supercharger losses produced negative torque before the exhaust-sizing calculation.
* **Input validation:** Added bounded numeric validation for simulator and vehicle parameters instead of silently accepting invalid or empty values.
* **Safe JSON loading:** Loading now restores factory defaults before applying saved values, handles malformed files cleanly, and preserves backward compatibility with older configurations.
* **Tkinter thread safety:** Moved dyno UI animation back to the main Tkinter event loop instead of reading and updating Tk variables from a worker thread.
* **Slider precision:** Slider values now respect their declared resolution instead of producing arbitrary intermediate values.
* **Temporary audio files:** Dyno WAV generation now uses safe temporary files rather than one fixed global filename.
* **Reworked engine curves:** Improved gasoline and diesel volumetric-efficiency curves, high-RPM falloff, turbo spool behavior, intercooler influence, and forced-induction scaling.
* **Corrected output and limits:** Improved horsepower conversion, negative-torque handling, RPM/redline behavior, and top-speed enforcement.
* **Expanded vehicle model:** Added separate frontal area, wheel radius, electronic speed limiter, and aerodynamic downforce (`Cl·A`) parameters.
* **Grip/downforce separation:** Tire grip no longer acts as a proxy for aerodynamic downforce.
* **Drivetrain refinement:** Added layout-dependent transmission losses and improved gearing-limited maximum-speed behavior.
* **Preset calibration:** Updated built-in engine and vehicle presets against the revised model while retaining their intended character.

## v4.5 (Aero & Dynamics Update)

* **Aerodynamic Downforce:** Added a downforce model to the Test Drive simulation based on vehicle speed, drag coefficient, and an `aero_factor` derived from tire grip.
* **Tire Grip Limits:** Wheel force during acceleration is strictly capped by the physical limits of tire adhesion (`min(force_wheel, max_grip_force)`).
* **Traction Control System (TCS):** Improved wheel-slip logic and UI indication. The simulator registers slip and adjusts engine RPM dynamically when the tires exceed available traction.
* **State Management Fix:** Added `snapshot_factory_defaults()` to reset UI values before loading a saved engine or applying a preset, eliminating previous state-leakage bugs.
* **UI Stability:** Configured the Manual Throttle and Test Drive windows as modal dialogs to prevent conflicting interaction with the main window.
* **Audio Engine Improvements:** Removed phase-wrapping loops that caused popping during rapid RPM changes and introduced a fixed audio block size.

## v4.4 (Tech Level & Curve Tune Update)

* **Technology Level:** Added a Technology Level slider to the Block tab that globally influences engine efficiency, friction, breathing, and knock resistance.
* **Turbo Spool Smoothness:** Replaced the sharp turbo cut-in with a smooth sigmoid boost curve.
* **Dynamic V-Angle:** The V-angle selector is hidden correctly for Inline and Boxer engines.
* **Improved Base Curves:** Adjusted base volumetric-efficiency curves to respond more consistently to tuning changes.

## v4.3.x (Material & Tuning Expansion)

* **Expanded component options:** Added Heavy/Light variants for the block, crankshaft, connecting rods, and pistons. Added Eco/Std/Perf tiers for cast-iron and aluminium heads, plus Aluminium Billet Race.
* **New mechanical systems:** Added continuously adjustable balancer mass, valve-spring stiffness, and exhaust bypass valves.
* **Fuel Map and Tuning:** Added a separate Fuel Map control and expanded the available fuel types.
* **VVL Rework:** Replaced the old Boolean VVL setting with None/VVL/CVVL modes, a separate high-lift profile, a configurable switch RPM, and smooth curve blending.
