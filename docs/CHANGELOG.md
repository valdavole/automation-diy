# Changelog

## v4.8.5 (Fullscreen & Settings Update + Tweaks)

* **Fullscreen single-window interface:** Rebuilt the GUI around one fullscreen application shell with a permanent sidebar, top status bar, embedded mode screens, a consistent dark theme, and larger responsive layouts.
* **Keyboard navigation:** Added **F11** fullscreen toggling and context-aware **Esc** behavior for closing overlays, returning to the Garage, and leaving fullscreen.
* **Central Settings panel:** Replaced the native menu bar and top-level language selector with an in-app Settings overlay containing Load, Save, language, speed-unit, Close, and Quit controls.
* **Selectable speed units:** Added live km/h ↔ mph display switching for Test Drive, Test Track, top-speed results, and the speed-limiter control. The mph mode reports **0–60 mph**, while metric mode reports **0–100 km/h**.
* **Canonical limiter storage:** The speed limiter remains stored internally in km/h and is converted safely for display and editing in mph.
* **Embedded live dyno graph:** Added an in-app Matplotlib canvas with torque and HP curves drawn progressively during the pull, plus live RPM, torque, power, status, and console telemetry.
* **Stale-result protection:** Editing an engine parameter now invalidates the previous dyno result and disables dependent modes until a fresh pull completes. Vehicle-only changes do not unnecessarily regenerate the engine curve.
* **Safe screen lifecycle:** Replaced separate modal Toplevel windows with embedded screens and added centralized cleanup for scheduled callbacks, audio streams, temporary dyno WAV files, and interrupted runs.
* **Unified Test Drive result:** The live animation and **Skip to Top Speed** now share one authoritative vehicle calculation, producing the same acceleration time, top speed, and final gear.
* **Drive presentation fixes:** Added unit-aware acceleration labels, natural coast-down after measurement, and a clutch/RPM wobble that is visual and audible only, so it no longer changes performance results.
* **Stronger validation:** Added allowed-value checks for dropdowns, strict JSON Boolean handling, finite/positive engine-curve checks, and rollback-safe loading of malformed configurations.
* **Preset loading fix:** Vehicle presets now apply their intended final drive, disable custom gearing, and load as a base before explicit saved chassis values are restored.
* **Engine calculation fixes:** Hidden balancer mass is ignored when no balancer is fitted, and the RPM array now always includes the exact requested or mechanical limiter even when it is not divisible by 100.

## v4.7 (Custom Gearing & Test Track Update)

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

## v4.3.1 (Material & Tuning Expansion)

* **Expanded component options:** Added Heavy/Light variants for the block, crankshaft, connecting rods, and pistons. Added Eco/Std/Perf tiers for cast-iron and aluminium heads, plus Aluminium Billet Race.
* **New mechanical systems:** Added continuously adjustable balancer mass, valve-spring stiffness, and exhaust bypass valves.
* **Fuel Map and Tuning:** Added a separate Fuel Map control and expanded the available fuel types.
* **VVL Rework:** Replaced the old Boolean VVL setting with None/VVL/CVVL modes, a separate high-lift profile, a configurable switch RPM, and smooth curve blending.
