# User Guide

*[Návod v češtině](NAVOD.md)*

This guide walks through the simulator in the order it is normally used. In-app tooltips provide quick per-parameter explanations; this document explains how the systems fit together.

The guide applies to **Automation DIY v4.10.2 — Branding Update**.

## 1. Overall Workflow

The simulator opens in fullscreen mode and keeps all main modes inside one application window. The branded left sidebar switches between the Garage, Dyno & Graph, Manual Throttle, Test Drive, and Track Simulation screens.

- Press **F11** to toggle fullscreen.
- Press **Esc** to close Settings or an error overlay, return from another mode to the Garage, or leave fullscreen when the Garage is already active.
- Open **Settings** to Load/Save a build, switch language, choose km/h or mph, or quit the simulator.
- The compact button in the top-right corner shows the current language and speed unit and opens the same Settings panel.
- Long builder tabs scroll automatically only when their content no longer fits the available height.
- Track Simulation scales its map to the available space and moves the information panel below the circuit on narrow windows.

Typical workflow:

1. Enter a separate **Car / Project Name** at the top of the builder.
2. Configure every required engine and vehicle field from **Blank Project**, or select an **Engine & Vehicle Preset** to load a complete starting point. A factory preset replaces the project name; you can rename it afterwards without changing the technical setup.
3. Click **Run Dyno / 1. Dyno Pull** to generate the torque and power curves.
4. Watch the live graph and telemetry, then inspect the completed curves on the Dyno screen.
5. Optionally open **Manual Throttle** for a live cooling and telemetry test.
6. Open **Test Drive** for 0–100 km/h or 0–60 mph and top-speed testing.
7. Open **Track Simulation** for a flying lap around the shared 3.605 km benchmark circuit.
8. Use **Settings → Save engine / vehicle as...** to store the named build as a portable `.json` file.

Language and speed units can be changed at runtime without resetting the current build or changing the vehicle physics. The speed-unit preference defaults to km/h on each launch.

## 2. The 7 Tabs

### Tab 1 — Block

Sets the engine's fundamental architecture.

- **Configuration**: Inline / V / Boxer.
- **V-angle**: shown only for V engines. The available choices are 60°, 90°, and 120°.
- **Cylinders**: 3, 4, 5, 6, 8, 10, 12, or 16.
- **Block material**: ranges from heavy cast iron through aluminium and AlSi variants to billet aluminium and magnesium.
- **Bore**: larger bore supports larger valves and stronger high-RPM breathing.
- **Stroke**: longer stroke favors low-end torque but raises mean piston speed and limits high-RPM operation. The slider covers 50–120 mm; special engines may use 20–150 mm by typing the value manually.
- **Radiator efficiency**: affects heat removal in Manual Throttle mode.
- **Technology level**: globally influences efficiency, breathing, friction, and knock resistance.

The calculated displacement is updated automatically from bore, stroke, and cylinder count.

### Tab 2 — Bottom End

Determines the mechanical RPM ceiling.

- **Crankshaft**, **connecting rods**, and **pistons** each have their own material-dependent RPM limit.
- The weakest of the three is the actual mechanical limit.
- **Balancer** options trade added friction and rotating mass for a higher mechanical RPM ceiling.
- When a harmonic damper or full balancer system is selected, the **balancer-mass slider** becomes visible. When **None** is selected, the hidden balancer-mass value is ignored by the physics.

Setting the RPM limiter above the weakest mechanical component intentionally destroys the engine during the dyno pull.

### Tab 3 — Top End

Controls the cylinder head, airflow behavior, valve float, and part of the knock model.

- **Head material** affects heat retention, friction, airflow tier, and knock tendency.
- **Valvetrain**: Pushrod/OHV, SOHC, DOHC, or DAOHC.
- **Valves per cylinder**: 2–5.
- **VVT** changes valve timing and broadens the usable powerband.
- **VVL** can be disabled, switched at a chosen RPM, or run as CVVL.
- Selecting VVL or CVVL reveals **VVL Profile** and **VVL RPM** controls.
- **Springs and lifters** raise the valve-float limit but increase friction.
- **Cam profile** shifts the volumetric-efficiency curve through the rev range.
- **Compression ratio** increases torque and efficiency but also raises knock risk on spark-ignition fuels.

### Tab 4 — Aspiration

- **NA**: immediate response and no boost.
- **Turbo**: exhaust-driven boost with spool behavior based on turbo size, engine displacement, bearing type, configuration, and intercooler size.
- **Supercharger**: immediate boost with parasitic losses.

Turbo controls include bearing type, Single/Twin/Quad configuration, intercooler size, turbo size, and boost pressure.

Supercharger controls include Roots, Twin-screw, or Centrifugal type, compressor size, and pulley/boost setting.

### Tab 5 — Fuel & Tune

Works together with the Top End and Aspiration tabs to determine output and knock risk.

- **Fuel delivery**: Carburetor, Mechanical Fuel Injection, Single Point EFI, EFI Multi, or Direct Injection.
- **Throttle/carburetor size** trades low-RPM response for high-RPM airflow.
- **Intake configuration**: Single, Twin, or ITB.
- **Intake manifold** and **manifold size** shape the torque curve and effective rev range.
- **Fuel type** supplies the knock-resistance baseline.
- **Fuel map** changes mixture richness separately from AFR.
- **AFR** affects power, efficiency, and lean-mixture knock risk.
- **Ignition timing** increases power but raises detonation risk when pushed too far.
- **RPM limiter** is the requested dyno redline. The slider covers 3,000–12,000 RPM; manual entry supports up to 20,000 RPM, but only a suitable race architecture can survive it.

Diesel bypasses the gasoline knock calculation, while Nitromethane receives a much higher potential power ceiling without removing the rest of the engine's physical limitations.

### Tab 6 — Exhaust

- **Architecture**: Single or Dual.
- **Headers** range from restrictive compact cast manifolds to race-oriented tubular systems.
- **Header size** and **pipe diameter** affect gas velocity and high-output flow capacity.
- **Bypass valves** open above 3500 RPM and bypass the mufflers.
- **Catalytic converter** choices trade emissions hardware for restriction.
- **Two muffler slots** allow combinations from no muffler to reverse-flow systems.

An undersized exhaust progressively chokes the upper part of the torque curve.

### Tab 7 — Vehicle & Drivetrain

These settings affect **Test Drive** and **Track Simulation**, but not the dyno curve.

The selector starts at **Blank Vehicle**, whose fields are intentionally empty. Configure all required values manually or select a vehicle preset before running the dyno. **Custom** means that one or more vehicle values no longer exactly match a built-in vehicle preset.

At the top of the whole builder, **Engine & Vehicle Preset** loads a complete engine-and-car combination. Inside Tab 7, **Vehicle Preset** changes only the vehicle. Selecting a built-in vehicle preset also disables individual custom ratios so that preset uses its intended automatic ratio set.

#### Chassis & weight distribution

- **Weight**: total vehicle mass including driver and fluids.
- **Engine Location**: Front Transverse, Front Longitudinal, Mid, or Rear. It affects vehicle balance and tire utilisation.
- **Front Weight / Rear Weight**: set the static front-axle share; the rear share is calculated automatically to total 100%. The split affects FWD/RWD traction and handling.
- **Wheelbase**: the distance between axles. A longer wheelbase reduces longitudinal load transfer.
- **Centre of Gravity Height**: a higher centre of gravity creates more load transfer and reduces tire utilisation.

#### Aerodynamics

- **Base Drag (Cd₀)**: body drag before downforce-induced drag.
- **Frontal Area**: reference area used with Cd in the drag calculation.
- **Downforce (Cl·A)**: aerodynamic downforce coefficient-area product.
- **Aerodynamic Efficiency**: controls how much extra drag is created by a chosen amount of downforce.
- **Effective Drag (Cd)**: the value actually used by Test Drive and Track Simulation. In simplified form, `effective Cd = base Cd + (effective Cl·A / frontal area)² / aerodynamic efficiency`. Ride height also changes effective downforce, so more downforce is no longer free straight-line grip.

#### Tires, suspension & brakes

- **Wheel Radius**: affects wheel force and road speed at a given engine RPM.
- **Tire Width**: wider tires handle higher load better but add rolling resistance.
- **Tire Compound**: Economy, Touring, Sport, Semi-Slick, or Slick. The choice sets base friction and rolling resistance.
- **Calculated Grip**: a read-only result derived from tire setup, suspension, centre of gravity, weight distribution, and vehicle layout.
- **Suspension Stiffness**: settings that are too soft or too stiff reduce tire utilisation; the suitable range depends on vehicle weight and downforce.
- **Ride Height**: affects floor/downforce efficiency. A very low, softly sprung car can bottom out.
- **Brake Type / Brake Diameter**: Drum, Solid Disc, Vented Disc, or Carbon Ceramic construction and its size determine the available mechanical braking force.
- **ABS**: improves use of the available tire grip under braking.

#### Drivetrain & gearbox

- **Speed Limiter**: electronic top-speed limit; `0` disables it. Its displayed value and slider range follow the selected km/h or mph setting, while the saved build keeps one canonical value.
- **Drivetrain**:
  - FWD has efficient power transmission but loses driven-axle load under acceleration.
  - RWD gains rear-axle load under acceleration.
  - AWD uses all four tires for traction but has the largest drivetrain losses.
- **Differential / LSD Locking**: an Open differential can spin an unloaded tire. An LSD improves power delivery as locking increases, although extreme locking can slightly reduce cornering willingness.
- **Gearbox Type**: Manual, Automatic, DCT, or Sequential. The type changes mechanical efficiency.
- **Gear Count**: 4–8 speeds.
- **Final Drive**: multiplies every transmission ratio. The slider covers the normal 2.0–6.0 range; special gearboxes may use 1.5–10.0 through manual entry.
- **Shift Time**: actual torque-interruption time for an upshift, used by acceleration and the track shift penalty.
- **Launch Control / Launch Control RPM**: when enabled, the system holds the selected launch RPM. Without it, the simulation uses a more cautious manual launch; excessive launch RPM can still create wheelspin.

#### Optional individual gear ratios

The **Fine-tune individual gear ratios** checkbox is disabled by default.

When it is disabled:

- the ratio editor stays hidden
- the simulator uses its built-in automatic ratio set for the selected gear count
- existing presets retain their established acceleration and top-speed behavior

When it is enabled:

- one ratio field appears for every active gear
- 4–8-speed transmissions are supported
- **Load automatic ratios** restores the default set
- ratios affect Test Drive and Track Simulation immediately after the next dyno/test run

For a sensible transmission, every higher gear should normally use a numerically smaller ratio than the gear before it.

## 3. Running the Dyno Pull

Click **Run Dyno** in the builder or **1. Dyno Pull** on the Dyno screen. The simulator validates the current inputs, switches to the Dyno screen, sweeps through the permitted RPM range, and calculates torque and HP at each point. The embedded graph, RPM counter, torque value, and power value update throughout the pull.

Two independent failure paths can stop the build:

- **Mechanical over-rev**: the RPM limiter exceeds the weakest crankshaft, conrod, or piston limit.
- **Knock/detonation**: the calculated knock index becomes excessive due to an unsafe combination of compression, boost, ignition timing, AFR, fuel map, octane, injection system, head material, or technology level.

The console explains both the failure and the main changes that can fix it.

After a successful pull:

- the completed graph remains embedded on the Dyno screen
- **Graph** can return you to that screen from elsewhere
- Manual Throttle, Test Drive, and Track Simulation become available
- when the audio backend is missing, Manual Throttle and Test Drive continue in silent mode

The dyno result is a snapshot of the engine at the time of the pull. Changing an engine parameter invalidates that result and locks the dependent modes until a new pull is completed. Vehicle-only settings can still be adjusted without regenerating the engine curve. Leaving the Dyno screen during an unfinished pull safely cancels the measurement and discards the incomplete result.


### High-RPM motorsport engines

Version 4.9 adds narrowly targeted support for extreme naturally aspirated race engines. This is not a global power multiplier: the simulator progressively evaluates whether the build genuinely matches a high-RPM architecture.

Using the range above 12,000 RPM effectively requires a combination of high Technology Level, an aggressive cam profile, strongly oversquare geometry, DAOHC valvetrain, ITBs, a Race intake manifold, naturally aspirated induction, a billet crankshaft, titanium connecting rods, and LW Forged pistons. The closer the build is to this combination, the more mechanical RPM capability, piston-speed tolerance, and high-RPM breathing it receives.

Ordinary road engines are not automatically strengthened, and the built-in presets retain their established results. Entering an extreme limiter without the required architecture can still destroy the engine.

## 4. Manual Throttle

Manual Throttle is a live free-revving telemetry test displayed inside the main application window.

Hold the throttle button to move toward the RPM limiter. Heat generation follows engine load and output, while radiator efficiency determines how quickly heat is rejected. If coolant temperature reaches the failure threshold, the head gasket fails.

This mode is separate from dyno knock and mechanical over-rev failures. Use the sidebar or **Esc** to leave it; the scheduled physics updates and audio stream are stopped safely.

## 5. Test Drive

Test Drive simulates a launch from rest, automatic shifting, either 0–100 km/h or 0–60 mph depending on the selected unit, and maximum speed.

The model uses:

- the engine's complete torque curve
- automatic or custom transmission ratios
- gearbox type, configured shift time, final drive, and wheel radius
- drivetrain efficiency, differential behavior, and optional Launch Control
- engine location, front/rear weight distribution, wheelbase, centre-of-gravity height, and longitudinal weight transfer
- tire width and compound, suspension stiffness, and ride height
- brake construction, brake diameter, and ABS
- aerodynamic drag from effective Cd and frontal area
- compound/width-dependent rolling resistance
- ride-height-adjusted aerodynamic downforce and its induced drag
- RPM and electronic speed limits

The TCS indicator reports wheel slip. Maximum speed can be limited by available power, drag, the highest gear and redline, or the electronic limiter.

The live run and **Skip to Top Speed** share one authoritative vehicle calculation, so both paths finish with the same acceleration time, top speed, and final gear. After the result is recorded, the live display releases the throttle and lets the vehicle coast down naturally while the measured maximum remains visible.

Switching between km/h and mph updates the visible speed, maximum-speed text, speed limiter, and acceleration target without changing the underlying physics.

## 6. Track Simulation

Track Simulation calculates a deterministic **flying lap**, not a standing-start lap.

### Circuit

- Length: **3.605 km**
- Three timed sectors
- A technical layout with straights, hairpins, medium-speed corners, faster bends, and linked direction changes
- The displayed track and simulated track are the same geometry

The circuit is generated from one closed curve, resampled into short distance steps. Local curvature is calculated from that geometry and converted into corner-radius information. The same points are then scaled for the on-screen map without changing the track's shape.

### Lap calculation

The lap model uses:

- the dyno torque curve
- automatic or custom gear ratios
- gearbox type, configured shift time, final drive, wheel radius, redline, and speed limiter
- mass, engine location, weight distribution, wheelbase, centre-of-gravity height, differential behavior, and drivetrain losses
- base/effective Cd, frontal area, aerodynamic efficiency, and rolling resistance
- tire width and compound, suspension stiffness, ride height, and aerodynamic downforce
- brake type, brake diameter, and ABS
- the tire friction circle, so cornering reduces the grip available for acceleration or braking
- backward passes to build braking zones before corners
- forward passes to limit acceleration between track points
- the configured upshift time and a shorter derived downshift penalty

The animation is accelerated so a long simulated lap does not require the same amount of real waiting time.

After the lap, the screen reports:

- total lap time
- sector 1, sector 2, and sector 3 times
- average speed in the selected speed unit
- maximum speed in the selected speed unit

The circuit length remains the fixed 3.605 km benchmark in either display mode.

Because the model is deterministic, identical builds produce identical lap times. This makes the circuit useful as a common benchmark for comparing cars inside the simulator.

## 7. Engine Sound

When `sounddevice` and a working PortAudio backend are available, engine sound is synthesized live from RPM, cylinder count, aspiration, throttle, and crank type.

Turbo engines include spool noise and lift-off flutter. Supercharged engines receive a speed-dependent whine.

If the audio backend is unavailable, the simulator remains fully usable. Manual Throttle and Test Drive run in silent mode, and Settings displays the `pip install -r requirements.txt` installation command.

## 8. Save and Load

Open **Settings** and use **Save engine / vehicle as...** to store the current build as JSON. Use **Load engine / vehicle...** in the same panel to restore one.

The v4.10.2 save format stores **Car / Project Name** and **Engine & Vehicle Preset** separately. It also includes all engine settings, the selected vehicle preset, the complete v4.10 vehicle-dynamics setup, the custom-gearing toggle, and every individual gear ratio. Language and the km/h/mph display preference are interface settings rather than vehicle data. The speed limiter is stored canonically and converted for display when mph is selected.

When loading:

- the simulator first restores safe factory defaults
- project name and preset identity are restored independently
- a saved vehicle preset is applied as a base before the file's explicit vehicle values are overlaid
- saved values are validated against numeric ranges and allowed dropdown choices
- Boolean fields must contain real JSON Boolean values rather than strings or numbers
- older files that do not contain newer v4.10 parameters receive compatible inferred/default values
- Czech special preset identifiers saved by v4.10 or v4.10.1 are translated to the current English internal names
- the old Boolean VVL format is converted automatically
- invalid or malformed files restore the previous active build and show an in-app error overlay instead of leaving partially applied values

## 9. Troubleshooting

- **One-off launch error in the prebuilt executable**: antivirus software may briefly lock an unsigned single-file executable during its first scan. Relaunch after the scan completes.
- **The banner or custom icon is missing**: keep `automation_diy_banner.png`, `automation_diy_icon.png`, and `automation_diy_icon.ico` beside the source script, or include them with PyInstaller as shown in `README.md`. The simulator deliberately falls back to its text header if an asset is unavailable.
- **Dyno reports an incomplete blank project/vehicle**: enter a project name and configure every required blank field, or load a complete Engine & Vehicle Preset.
- **The app is stuck in fullscreen**: press **F11**. Pressing **Esc** from the Garage also leaves fullscreen.
- **No live sound**: the simulations continue in silent mode. Run `pip install -r requirements.txt`, check PortAudio, and verify a working default output device.
- **Test Drive or Track Simulation is disabled**: run a successful Dyno Pull first. A destroyed engine cannot be tested.
- **The Dyno screen says the engine changed**: an engine parameter was edited after the last pull. Run a new Dyno Pull before opening dependent modes.
- **Custom ratios are not visible**: enable **Fine-tune individual gear ratios** in the Vehicle & Drivetrain tab.
- **A saved preset produces different performance after editing gears**: disable custom gearing or press **Load automatic ratios** to restore the original automatic set.
