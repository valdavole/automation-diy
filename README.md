# Automation DIY — Engine & Vehicle Simulator

*[Čti v češtině / Read in Czech](README.cz.md)*

A homemade, open-source engine-building, dyno, vehicle, and lap-time simulator inspired by the "Automation"-style car tycoon genre.

Build an engine from the crankshaft up, run it on a virtual dyno, test its cooling under manual throttle, measure 0–100 km/h and top speed, then send the car around a fully simulated 3.605 km test track. Engine sound is generated procedurally and reacts live to RPM, throttle, cylinder count, aspiration, and crank type.

> **Current release: v4.7 — Custom Gearing & Test Track**

![screenshot placeholder](docs/screenshot.png)

## Features

- **7-tab engine and vehicle builder**: Block, Bottom End, Top End, Aspiration, Fuel & Tune, Exhaust, Drivetrain
- **Physics-based dyno simulation** with generated torque and HP curves
- **Independent engine failure models**:
  - mechanical over-rev, determined by the weakest crankshaft, connecting rod, or piston limit
  - knock/detonation, influenced by compression, boost, ignition timing, AFR, fuel map, octane, injection, head material, and technology level
- **Manual throttle telemetry mode** with live coolant temperature and head-gasket failure from overheating
- **0–100 km/h and top-speed simulation** with:
  - drivetrain losses and FWD/RWD/AWD traction behavior
  - longitudinal weight transfer
  - tire-grip limits
  - frontal area, drag coefficient, wheel radius, rolling resistance, and aerodynamic downforce
  - electronic speed limiting and RPM/gearing-limited top speed
- **Optional individual gear-ratio tuning** for 4–8-speed transmissions
  - leave it disabled to retain the original automatic ratio sets
  - enable it to edit every ratio independently
  - built-in presets keep automatic gearing by default, preserving their established performance
- **3.605 km test track with a flying-lap simulation**
  - three timed sectors
  - live speed, gear, sector, and lap-time telemetry
  - braking zones, corner-speed limits, tire friction-circle behavior, acceleration, drag, downforce, and shift penalties
  - one shared track geometry for both physics and rendering, so the displayed circuit is the circuit being simulated
- **Procedurally generated engine audio** with no prerecorded engine samples
- **Built-in tooltips** explaining the engineering effect of each parameter
- **Safe Save/Load** of portable JSON engine configurations, including compatibility defaults for older files
- **Real-world-inspired presets** for quick starting points
- **Bilingual UI**: English and Czech, switchable at runtime

## Getting Started

### Option A — Prebuilt Windows executable

Download the latest `.exe` from the [Releases](../../releases) page and run it directly. No Python installation is required.

> **Known issue:** on first launch, antivirus software such as Microsoft Defender or AVG may briefly lock a file while scanning an unsigned single-file executable. This can surface as a one-off launch error. Relaunching the app usually resolves it after the first scan is complete.

### Option B — Run from source

Requires Python 3.10+.

```bash
pip install numpy matplotlib sounddevice
python engine_sim.py
```

`tkinter` is included with most standard Windows Python installations. On some Linux distributions it may need to be installed separately through the system package manager.

`sounddevice` and its PortAudio backend are optional. If they are unavailable, the simulator still runs normally, but live engine-audio controls are disabled.

## Typical Workflow

1. Select a preset or start from the default build.
2. Configure the engine across the seven tabs.
3. Run **1. Dyno Pull**.
4. Inspect the torque and power graph.
5. Optionally run **2. Manual Throttle**.
6. Run **3. Test Drive** for 0–100 km/h and top speed.
7. Run **4. Test Track** for a comparable flying-lap result.
8. Save the build as JSON when you are happy with it.

For a complete explanation of every tab, simulation mode, failure model, custom gearing, and the test track, see **[USER_GUIDE.md](docs/USER_GUIDE.md)**.

## Simulation Scope

Automation DIY is designed as an accessible game-style engineering simulator, not as a replacement for professional engine-cycle, CFD, multibody vehicle-dynamics, or motorsport lap-simulation software.

The output is deterministic and useful for comparing builds inside the simulator, but real-world results also depend on factors that are outside the model, including tire temperature, suspension geometry, road surface, weather, driver behavior, transient turbo response, component tolerances, and detailed combustion behavior.

## Disclaimer

Some built-in presets reference real manufacturers and models as illustrative performance benchmarks. They are unofficial, fan-made approximations included for educational and entertainment purposes. This project is not affiliated with, endorsed by, or sourced from the referenced manufacturers.

## Credits

Inspired by the *Automation: The Car Company Tycoon Game* genre. This is an independent hobby project with no affiliation to that title or its developers.

## Contributing

The project grew from one evolving script through many iterative versions, so the current codebase still lives mainly in one large file.

Pull requests are welcome. Splitting the project into modules such as `physics.py`, `audio.py`, `gui.py`, `track.py`, and `presets.py` would be a valuable first contribution toward easier maintenance and testing.
