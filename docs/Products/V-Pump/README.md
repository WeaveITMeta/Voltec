# VOLTEC V-PUMP — Modular Inline Vacuum-Assist Pipeline Pump

## Blueprint Documentation

---

## Overview

The V-Pump is a modular inline booster pump unit designed for permanent installation in large-scale water transport pipelines. It moves water over unlimited distances through relay-station architecture at intervals of ≤50 km, with a 1,000-year design life for the structural casing.

**Primary application**: Replenishing the Indo-Gangetic Basin aquifer via 990 km desalinated seawater pipeline — generalizable to any continental-scale water project.

---

## Key Specifications

| Spec | Value |
|------|-------|
| Core Technology | Multi-stage axial-flow impeller with vacuum-assist priming |
| Casing Material | UNS S32205 Duplex Stainless Steel |
| Bore Liner | Reaction-Bonded Silicon Carbide (RBSiC) |
| Impeller Material | UNS S32750 Super Duplex SS |
| Bearings | SiC/SiC ceramic journal, water-lubricated |
| Motor | Permanent Magnet Synchronous (PMSM), IP68 |
| Frame Sizes | VP-S (DN300-800), VP-M (DN800-2000), VP-L (DN2000-4000), VP-XL (DN4000-16000) |
| Max Flow | 600 m³/s (VP-XL, parallel bank) |
| Max Head | 300 m (3-stage) |
| BEP Efficiency | 88-91% |
| Design Life (casing) | 1,000 years |
| Bearing Replacement | 50-100 years |
| Priming | Integrated vacuum-assist (oil-free rotary vane) |
| Bypass | Automatic butterfly valve (fail-open) |
| AI Telemetry | V-Mind real-time optimization |
| Fluid Mechanics Library | `garbongus` ≥0.2.1 |

---

## Component Inventory (11 Components)

| # | Component | Material | class_name | .glb KB |
|---|-----------|----------|------------|---------|
| 1 | Pump Casing | UNS S32205 Duplex SS | AdvancedPart | 83.0 |
| 2 | Bore Liner | RBSiC Ceramic | AdvancedPart | 27.6 |
| 3 | Impeller Assembly | UNS S32750 Super Duplex | AdvancedPart | 53.2 |
| 4 | Drive Shaft | 17-4 PH SS H900 | AdvancedPart | 28.6 |
| 5 | Bearing Cartridge | SiC/SiC Ceramic | AdvancedPart | 60.8 |
| 6 | Vacuum Module | 316L SS + PTFE | Part | 71.0 |
| 7 | Flange Adapter | A694 F60 Duplex | Part | 51.7 |
| 8 | Bypass Valve | Duplex + Stellite 6 | Part | 71.0 |
| 9 | Motor (PMSM) | Steel + NdFeB | AdvancedPart | 248.4 |
| 10 | Control Module | 316L SS Enclosure | Part | 57.7 |
| 11 | Status Array | Polycarbonate | Part | 40.0 |

**Total mesh size**: 793 KB (Draco-compressed GLB)

---

## File Structure

```
docs/Products/V-Pump/
├── PATENT.md                           # 16-section patent specification
├── SOTA_VALIDATION.md                  # Three-tier honesty framework + risk matrix
├── EustressEngine_Requirements.md      # Material tables, domain state, laws reference
├── README.md                           # This file
└── V1/
    ├── VPump_PumpCasing.glb.toml       # Instance files (11 total)
    ├── VPump_BoreLiner.glb.toml
    ├── VPump_ImpellerAssembly.glb.toml
    ├── VPump_DriveShaft.glb.toml
    ├── VPump_BearingCartridge.glb.toml
    ├── VPump_VacuumModule.glb.toml
    ├── VPump_FlangeAdapter.glb.toml
    ├── VPump_BypassValve.glb.toml
    ├── VPump_Motor.glb.toml
    ├── VPump_ControlModule.glb.toml
    ├── VPump_StatusArray.glb.toml
    └── meshes/
        ├── VPump_PumpCasing.glb        # GLB meshes (11 total)
        ├── VPump_BoreLiner.glb
        ├── VPump_ImpellerAssembly.glb
        ├── VPump_DriveShaft.glb
        ├── VPump_BearingCartridge.glb
        ├── VPump_VacuumModule.glb
        ├── VPump_FlangeAdapter.glb
        ├── VPump_BypassValve.glb
        ├── VPump_Motor.glb
        ├── VPump_ControlModule.glb
        ├── VPump_StatusArray.glb
        └── scripts/                    # Blender Python scripts (11 total)
            ├── VPump_PumpCasing.py
            ├── VPump_BoreLiner.py
            ├── VPump_ImpellerAssembly.py
            ├── VPump_DriveShaft.py
            ├── VPump_BearingCartridge.py
            ├── VPump_VacuumModule.py
            ├── VPump_FlangeAdapter.py
            ├── VPump_BypassValve.py
            ├── VPump_Motor.py
            ├── VPump_ControlModule.py
            └── VPump_StatusArray.py
```

---

## Hydraulic Sizing via garbongus

All V-Pump units are sized using the `garbongus` fluid mechanics library (Rust, pure, `no_std`):

```rust
use garbongus::{fluid::Fluid, flow, pipe::DarcyWeisbach, vacuum::VacuumLift};

// 1. Fluid properties
let fluid = Fluid::seawater(25.0, 2.0);  // Desalinated, ~2 ppt residual

// 2. Pipe sizing
let d = flow::required_diameter(595.0, 3.0);  // 595 m³/s at 3 m/s → ~16m

// 3. Friction loss per relay segment
let dw = DarcyWeisbach::new(&fluid, d, 50_000.0, 3.0, 1.5e-6);
let loss = dw.calculate();  // ~9.5 bar per 50 km

// 4. Pump power
let pump = flow::pump_power(fluid.density_kg_m3, 595.0, 107.0, 0.88);
// pump.shaft_mw() ≈ 710 MW per station

// 5. Vacuum-assist headroom
let vac = VacuumLift::new(fluid, d / 2.0, 10.0).calculate();
// vac.atmospheric_max_lift_m ≈ 10.18 m
```

---

## Regenerating Meshes

All meshes are generated via Blender 4.4 headless Python scripts:

```powershell
# Regenerate a single mesh
& "C:\Program Files\Blender Foundation\Blender 4.4\blender.exe" --background --python "V1\meshes\scripts\VPump_PumpCasing.py"

# Regenerate all meshes
Get-ChildItem "V1\meshes\scripts\*.py" | ForEach-Object {
    & "C:\Program Files\Blender Foundation\Blender 4.4\blender.exe" --background --python $_.FullName
}
```

---

## Design Principles

1. **Zero Ornament** — Every feature serves an engineering purpose
2. **1000-Year Design** — Casing and bore liner outlast civilizations
3. **Field-Replaceable Cartridges** — Impeller, bearings, motor swap without pipeline cut
4. **Automatic Bypass** — Zero-downtime relay chains via fail-open butterfly valve
5. **AI-Optimized** — V-Mind manages hydraulic grade line across entire pipeline
6. **Made-to-Order** — Universal frame + custom flange adapters for any pipe diameter
7. **garbongus-Validated** — Every hydraulic calculation traceable to physics library

---

## Cross-References

| Document | Purpose |
|----------|---------|
| `PATENT.md` | Full patent specification, 12 claims |
| `SOTA_VALIDATION.md` | Honesty tiers (60% verified, 30% projected, 10% aspirational) |
| `EustressEngine_Requirements.md` | Material tables, FluidState, ThermodynamicState, garbongus laws |
| `Products.md` | Voltec product catalog entry (Tier 1) |
