# Changelog

## v4.5 (Aero & Dynamics Update)
* **Aerodynamic Downforce:** Added a realistic downforce model in the Test Drive simulation based on vehicle speed, drag coefficient (Cd), and an `aero_factor` derived from tire grip. High-performance vehicles now stick to the road much better at high speeds.
* **Tire Grip Limits:** Wheel force during acceleration is now strictly capped by the physical limits of tire adhesion (`min(force_wheel, max_grip_force)`).
* **Traction Control System (TCS):** Improved wheel slip logic and UI indication. The simulator now accurately registers slip and adjusts engine RPM dynamically when wheels break traction.
* **State Management Fix:** Added a `snapshot_factory_defaults()` function to cleanly reset all UI elements before loading a saved engine or applying a preset, completely eliminating previous "state leakage" bugs.
* **UI Stability:** The Telemetry (Manual Throttle) and Test Drive windows are now properly configured as modal dialogs, preventing users from interacting with the main window and accidentally causing crashes or audio bugs.
* **Audio Engine Improvements:** Removed mathematical loops from audio phases to eliminate popping/clicking during rapid RPM changes, and implemented a fixed `blocksize` of 2048 for smoother audio buffer generation.
* **Preset Update:** Renamed 'Bugatti Veyron 16.4' to 'Bugatti Veyron 16.4 Super Sport' for accuracy.

## v4.4 (Tech Level & Curve Tune Update)
* **Technology Level:** Added a "Tech Level" slider to the Block tab that globally influences overall engine efficiency, friction, and breathing capabilities depending on the era.
* **Turbo Spool Smoothness:** Replaced the sharp mathematical cut-in for turbochargers with a smooth sigmoid curve for a more realistic boost onset.
* **Dynamic V-Angle:** The V-Angle selection is now correctly hidden when an Inline or Boxer configuration is selected.
* **Improved Base Curves:** Adjusted base volumetric efficiency (VE) curves to respond better to tuning modifications across the board.

## v4.3.1 (Material & Tuning Expansion)
* **Expanded component options:** Added Heavy/Light variants for block, crank, connecting rods, and pistons. Added Eco/Std/Perf tiers for cast iron and aluminum heads, plus Aluminum Billet Race.
* **New mechanical systems:** Added continuously adjustable balancer weight (0-50 kg), valve spring stiffness model, and exhaust bypass flaps.
* **Fuel map and Tuning:** Added a separate slider for Fuel Map (lean/rich mixture). Expanded fuel types including Regular 91, Super 98, Leaded Gasoline, Compressed Gas, and Nitromethane.
* **VVL Rework:** Redesigned VVL into 3 states (None/VVL/CVVL) with its own profile and switching RPMs, featuring smooth curve blending.
