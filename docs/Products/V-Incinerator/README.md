# V-Incinerator — 3D Blueprint Documentation

## Overview

This directory contains the complete V-Incinerator product package: patent specification, state-of-the-art validation, EustressEngine realism requirements, and 13 `.glb.toml` instance files defining a high-efficiency plasma gasification waste-to-energy system with four-stage exhaust purification. The V-Incinerator is designed to replace landfill infrastructure in major US cities, following the proven waste-to-energy model deployed across Japan.

## Architecture

```
EustressEngine Space Root (Universe1/spaces/Space1/)
├── assets/meshes/
│   ├── block.glb          ← shared primitive (housing, filters, beds)
│   ├── cylinder.glb       ← shared primitive (chambers, scrubber, stack)
│   └── ball.glb           ← shared primitive (status LED)
└── Workspace/
    ├── VIncinerator_Housing.glb.toml
    ├── VIncinerator_PlasmaChamber.glb.toml
    ├── VIncinerator_CombustionChamber.glb.toml
    ├── VIncinerator_HeatExchanger.glb.toml
    ├── VIncinerator_HEPAFilter.glb.toml
    ├── VIncinerator_CatalyticConverter.glb.toml
    ├── VIncinerator_CarbonBed.glb.toml
    ├── VIncinerator_WetScrubber.glb.toml
    ├── VIncinerator_ExhaustStack.glb.toml
    ├── VIncinerator_AshHopper.glb.toml
    ├── VIncinerator_WasteFeed.glb.toml
    ├── VIncinerator_ControlModule.glb.toml
    └── VIncinerator_StatusArray.glb.toml
```

## Instance Files

| File | Mesh | Class | Realism Sections |
|------|------|-------|------------------|
| `VIncinerator_Housing.glb.toml` | block.glb | AdvancedPart | material, thermodynamic |
| `VIncinerator_PlasmaChamber.glb.toml` | cylinder.glb | AdvancedPart | material, thermodynamic |
| `VIncinerator_CombustionChamber.glb.toml` | cylinder.glb | AdvancedPart | material, thermodynamic |
| `VIncinerator_HeatExchanger.glb.toml` | block.glb | AdvancedPart | material, thermodynamic |
| `VIncinerator_HEPAFilter.glb.toml` | block.glb | AdvancedPart | material, thermodynamic |
| `VIncinerator_CatalyticConverter.glb.toml` | block.glb | AdvancedPart | material, thermodynamic |
| `VIncinerator_CarbonBed.glb.toml` | block.glb | AdvancedPart | material, thermodynamic |
| `VIncinerator_WetScrubber.glb.toml` | cylinder.glb | AdvancedPart | material, thermodynamic |
| `VIncinerator_ExhaustStack.glb.toml` | cylinder.glb | Part | — |
| `VIncinerator_AshHopper.glb.toml` | block.glb | AdvancedPart | material, thermodynamic |
| `VIncinerator_WasteFeed.glb.toml` | block.glb | Part | — |
| `VIncinerator_ControlModule.glb.toml` | block.glb | Part | — |
| `VIncinerator_StatusArray.glb.toml` | ball.glb | Part | — |

## Import into EustressEngine

### Manual Copy

1. Copy all 13 `.glb.toml` files from `V1/` to `Universe1/spaces/Space1/Workspace/`
2. Ensure primitive meshes exist at `assets/meshes/` (block.glb, cylinder.glb, ball.glb)
3. Restart EustressEngine or trigger workspace rescan — entities auto-discover

### Programmatic Spawn (Rust)

```rust
use eustress::space::instance_loader::{load_instance_file, spawn_instance};

let toml_path = space_root.join("Workspace/VIncinerator_PlasmaChamber.glb.toml");
let instance = load_instance_file(&toml_path)?;
let entity = spawn_instance(&mut commands, &asset_server, &space_root, toml_path, instance);
```

## Coordinate System

- **Origin**: Geometric center of the outer housing at ground level
- **Y-axis**: Up (height)
- **X-axis**: Length (front-to-back along process flow)
- **Z-axis**: Width
- **Units**: Meters (all position and scale values)
- **Rotation**: Quaternion `[x, y, z, w]`
- **Color**: Linear RGBA `[r, g, b, a]` with values 0.0–1.0

## Entity Hierarchy

```
V-Incinerator Assembly (6.0m × 4.0m × 3.0m)
├── VIncinerator_Housing           — AdvancedPart, 316L Stainless Steel
│   │
│   ├── PROCESS CORE (vertical stack, center)
│   │   ├── VIncinerator_AshHopper             — AdvancedPart, A36 Carbon Steel
│   │   ├── VIncinerator_PlasmaChamber         — AdvancedPart, Tungsten (W)
│   │   ├── VIncinerator_CombustionChamber     — AdvancedPart, Inconel 718
│   │   └── VIncinerator_HeatExchanger         — AdvancedPart, Cu-Ni C71500
│   │
│   ├── EXHAUST PURIFICATION TRAIN (right side)
│   │   ├── VIncinerator_HEPAFilter            — AdvancedPart, Borosilicate Glass
│   │   ├── VIncinerator_CatalyticConverter    — AdvancedPart, Inconel 625 + Pt-Pd
│   │   └── VIncinerator_CarbonBed             — AdvancedPart, 304SS + GAC
│   │
│   ├── WET SCRUBBER + EXHAUST (left side)
│   │   ├── VIncinerator_WetScrubber           — AdvancedPart, Hastelloy C-276
│   │   └── VIncinerator_ExhaustStack          — Part, 304 Stainless
│   │
│   ├── INTAKE
│   │   └── VIncinerator_WasteFeed             — Part, AR400 Steel
│   │
│   └── CONTROLS
│       ├── VIncinerator_ControlModule         — Part, FR4 PCB + V-OS
│       └── VIncinerator_StatusArray           — Part, LED (Xenon Blue)
```

## Realism Components Attached

- **`[material]`** → `MaterialProperties` ECS component (14 base fields + `[material.custom]`)
- **`[thermodynamic]`** → `ThermodynamicState` ECS component (temperature, pressure, volume, energy, entropy, enthalpy, moles)
- **No `[electrochemical]`** — V-Incinerator is a thermal/mechanical system, not electrochemical

## Custom Material Extensions

Domain-specific `[material.custom]` keys used across V-Incinerator components:

- **`role`** — Component role tag (all components): `"housing"`, `"plasma_chamber"`, `"combustion_chamber"`, `"heat_exchanger"`, `"hepa_filter"`, `"catalytic_converter"`, `"carbon_bed"`, `"wet_scrubber"`, `"ash_hopper"`
- **`torch_power_kw`** — Total plasma torch power (Plasma Chamber)
- **`torch_count`** — Number of DC plasma torches (Plasma Chamber)
- **`operating_temp_max_k`** — Maximum operating temperature (Plasma Chamber)
- **`liner_thickness_m`** — Tungsten liner thickness (Plasma Chamber)
- **`plasma_erosion_rate_mm_per_1000h`** — Liner erosion rate (Plasma Chamber)
- **`creep_rupture_100kh_mpa`** — 100,000-hour creep rupture stress (Combustion Chamber)
- **`dwell_time_s`** — Gas residence time (Combustion Chamber)
- **`tube_count`**, **`thermal_duty_mw`**, **`steam_output_mw`**, **`steam_temp_k`**, **`steam_pressure_mpa`** — Heat exchanger specs
- **`filtration_efficiency_pct`**, **`mpps_um`**, **`filter_area_m2`**, **`service_life_hours`** — HEPA filter specs
- **`catalyst_pt_g_per_l`**, **`catalyst_pd_g_per_l`**, **`dioxin_destruction_pct`**, **`space_velocity_per_h`** — Catalyst specs
- **`hg_removal_pct`**, **`pb_removal_pct`**, **`cd_removal_pct`**, **`voc_removal_pct`** — Carbon bed specs
- **`scrubbing_agent`**, **`hcl_removal_pct`**, **`so2_removal_pct`**, **`hf_removal_pct`** — Wet scrubber specs
- **`slag_vitrification`** — Slag inertness classification (Ash Hopper)

## Blender Mesh Generation

Three AAA-quality Blender Python scripts are provided in `V1/meshes/scripts/`:

| Script | Component | Geometry |
|--------|-----------|----------|
| `VIncinerator_Housing.py` | Outer housing | Solidified cube shell, 12mm wall |
| `VIncinerator_PlasmaChamber.py` | Plasma chamber | Thick-walled cylinder, 23mm wall |
| `VIncinerator_ExhaustStack.py` | Exhaust stack | Tapered cone, 6mm wall |

Run all scripts headless:

```powershell
$blender = "C:\Program Files\Blender Foundation\Blender 4.4\blender.exe"
$scripts = Get-ChildItem "docs/Products/V-Incinerator/V1/meshes/scripts" -Filter "*.py"
foreach ($s in $scripts) {
    Write-Host "Generating: $($s.BaseName)..." -ForegroundColor Cyan
    & $blender --background --python $s.FullName 2>&1 |
        Select-String "MESH:|Quads:|EXPORTED:|DONE"
}
```

## Related Documents

- **PATENT.md** — Full patent specification (10 claims, ASCII cross-sections, all material properties)
- **SOTA_VALIDATION.md** — Three-tier honesty framework, risk matrix, roadmap
- **EustressEngine_Requirements.md** — Complete realism crate mapping, runtime pseudocode, deployment checklist
