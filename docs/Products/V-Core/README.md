# V-Core — Residential Micro-Nuclear Reactor

**Product**: V-Core  
**Tier**: 3 — Horizon  
**Version**: 1.0  
**Date**: March 6, 2026  
**Dry mass**: ~693 kilograms (egg-shaped, table-sized form factor)  
**Power**: 25 kW electrical continuous, 75 kW thermal (50 kW recoverable CHP)  
**Fuel**: U-ZrH₁.₆ (TRIGA-heritage, 19.75% LEU), 10-year sealed fuel load  

---

## Overview

V-Core is a passively safe micro-nuclear fission reactor designed for residential and light commercial distributed power generation. It combines TRIGA-heritage uranium zirconium hydride fuel (inherent walk-away safety), sodium heat pipe passive thermal transport, and free-piston Stirling engine power conversion in a factory-sealed egg-shaped package that fits on a concrete pad.

No fuel deliveries. No emissions. No operator. 25 kW continuous for 10 years.

---

## Directory Structure

```
V-Core/
├── PATENT.md                          # Full patent specification (17 sections)
├── SOTA_VALIDATION.md                 # Three-tier honesty framework + risk matrix
├── EustressEngine_Requirements.md     # Material tables, state fields, deployment
├── README.md                          # This file
└── V1/
    ├── meshes/
    │   ├── scripts/                   # 14 Blender Python generators + run_all.py
    │   │   ├── VCore_OuterCasing.py
    │   │   ├── VCore_ReactorVessel.py
    │   │   ├── VCore_FuelAssembly.py
    │   │   ├── VCore_ReflectorAssembly.py
    │   │   ├── VCore_ControlDrums.py
    │   │   ├── VCore_HeatPipeBundle.py
    │   │   ├── VCore_StirlingEngines.py
    │   │   ├── VCore_HotSideHX.py
    │   │   ├── VCore_ColdRadiator.py
    │   │   ├── VCore_BioShield.py
    │   │   ├── VCore_VCellBuffer.py
    │   │   ├── VCore_ControlModule.py
    │   │   ├── VCore_ElectricalConverter.py
    │   │   ├── VCore_StatusArray.py
    │   │   └── run_all.py
    │   ├── VCore_OuterCasing.glb
    │   ├── VCore_ReactorVessel.glb
    │   ├── VCore_FuelAssembly.glb
    │   ├── VCore_ReflectorAssembly.glb
    │   ├── VCore_ControlDrums.glb
    │   ├── VCore_HeatPipeBundle.glb
    │   ├── VCore_StirlingEngines.glb
    │   ├── VCore_HotSideHX.glb
    │   ├── VCore_ColdRadiator.glb
    │   ├── VCore_BioShield.glb
    │   ├── VCore_VCellBuffer.glb
    │   ├── VCore_ControlModule.glb
    │   ├── VCore_ElectricalConverter.glb
    │   └── VCore_StatusArray.glb
    ├── VCore_ReactorVessel.glb.toml
    ├── VCore_FuelAssembly.glb.toml
    ├── VCore_ReflectorAssembly.glb.toml
    ├── VCore_ControlDrums.glb.toml
    ├── VCore_HeatPipeBundle.glb.toml
    ├── VCore_StirlingEngines.glb.toml
    ├── VCore_HotSideHX.glb.toml
    ├── VCore_ColdRadiator.glb.toml
    ├── VCore_BioShield.glb.toml
    ├── VCore_OuterCasing.glb.toml
    ├── VCore_VCellBuffer.glb.toml
    ├── VCore_ControlModule.glb.toml
    ├── VCore_ElectricalConverter.glb.toml
    └── VCore_StatusArray.glb.toml
```

---

## Component Inventory (14 Components)

| # | Component | Material | Mass (kg) | Realism Sections |
|---|-----------|----------|-----------|-----------------|
| 1 | Reactor Vessel | 316L Stainless Steel | 85.0 | material, thermodynamic |
| 2 | Fuel Assembly | U-ZrH₁.₆ (19.75% LEU) | 42.0 | material, thermodynamic (+ NuclearState via custom) |
| 3 | Reflector Assembly | Beryllium Oxide (BeO) | 38.0 | material, thermodynamic |
| 4 | Control Drums (6×) | B₄C + SS304 | 24.0 | material, thermodynamic |
| 5 | Heat Pipe Bundle (12×) | Inconel 718 + Na | 18.0 | material, thermodynamic |
| 6 | Stirling Engines (2×) | Maraging 350 Steel | 65.0 | material, thermodynamic |
| 7 | Hot-Side Heat Exchanger | Inconel 718 | 12.0 | material, thermodynamic |
| 8 | Cold-Side Radiator | Aluminum 6061-T6 | 35.0 | material, thermodynamic |
| 9 | Biological Shield | Lead-PE-Boron composite | 280.0 | material, thermodynamic |
| 10 | Outer Casing | 304 Stainless Steel | 45.0 | material, thermodynamic |
| 11 | V-Cell Buffer (2×) | Na-S Solid State | 18.5 | material, thermodynamic, **electrochemical** |
| 12 | Control Module | 316L SS + NVIDIA Orin | 8.0 | material |
| 13 | Electrical Converter | SiC Power Module | 22.0 | material |
| 14 | Status Array | Polycarbonate | 0.5 | material |
| | **TOTAL** | | **~693 kg** | |

---

## Materials Summary

| Material | Components | Key Property |
|----------|-----------|-------------|
| 316L Stainless Steel | Reactor Vessel, Control Module | ASME III Div 5, 14.6 W/(m·K) |
| U-ZrH₁.₆ | Fuel Assembly | -1.0×10⁻⁴ Δk/k/°C temp coefficient |
| Beryllium Oxide | Reflector | 260 W/(m·K), neutron moderating ratio 143 |
| Boron Carbide (B₄C) | Control Drums | 3,840 barns thermal neutron absorption |
| Inconel 718 | Heat Pipes, Hot-Side HX | 1,034 MPa yield, Na-compatible to 700°C |
| Maraging 350 Steel | Stirling Engines | 2,400 MPa yield |
| Aluminum 6061-T6 | Cold Radiator | 167 W/(m·K) |
| Lead | Biological Shield (inner/outer) | 11,340 kg/m³, gamma attenuation |
| Borated Polyethylene | Biological Shield (middle) | Neutron moderation + capture |
| 304 Stainless Steel | Outer Casing | Seismic Zone 4, flood-rated 2 m |
| Na-S Solid State | V-Cell Buffer | 900 Wh/kg, 16.7 kWh total |
| SiC | Electrical Converter | 97% efficiency, 240 VAC grid-tie |
| Polycarbonate | Status Array | 8 LEDs (green/amber/red) |

---

## Key Specifications

| Parameter | Value |
|-----------|-------|
| Electrical Output | 25 kW continuous |
| Thermal Output | 75 kW (50 kW recoverable as CHP) |
| Efficiency | 33.3% electrical, >90% CHP |
| Fuel | U-ZrH₁.₆, 19.75% LEU, 1.054 kg U-235 |
| Fuel Lifetime | 10 years (87,600 hours) |
| Form Factor | Egg-shaped, 800×600×500 mm |
| Dry Mass | ~693 kg |
| Dose at 1 m | <0.25 mR/hr |
| Noise | <40 dB at 1 m |
| Grid Connection | 240 VAC split-phase, IEEE 1547 |
| Buffer | 16.7 kWh V-Cell (blackstart <5 min) |
| AI Control | V-Mind (NVIDIA Orin), NRC telemetry |
| Seismic | Zone 4 (0.4 g horizontal) |
| Flood | Watertight to 2 m submersion |

---

## EustressEngine Integration

All 14 components have `.glb.toml` instance files in `V1/`. Key integration points:

- **class_name = "Part"** for all components (no AdvancedPart needed — realism via [material.custom])
- **1 component has [electrochemical]**: VCellBuffer
- **NuclearState** tracked via `[material.custom]` fields on FuelAssembly (engine does not yet have native NuclearState component)
- **All positions baked into GLB meshes** — TOML `[transform].position` is `[0,0,0]` for all
- **Units**: meters (position/scale), Kelvin (temperature), Pascal (pressure), SI throughout

### Deployment

```powershell
# Copy GLB meshes
$src = "E:\Workspace\Voltec\docs\Products\V-Core\V1\meshes"
$dst = "C:\Users\miksu\Documents\Eustress\Universe1\spaces\Space1\assets\meshes\products\V-Core"
New-Item -ItemType Directory -Path $dst -Force
Copy-Item "$src\*.glb" $dst

# Copy TOML instance files
$tomlSrc = "E:\Workspace\Voltec\docs\Products\V-Core\V1"
$tomlDst = "C:\Users\miksu\Documents\Eustress\Universe1\spaces\Space1\Workspace"
Copy-Item "$tomlSrc\*.glb.toml" $tomlDst
```

---

## Mesh Regeneration

Requires Blender 4.4+.

```powershell
& "C:\Program Files\Blender Foundation\Blender 4.4\blender.exe" `
  --background --python `
  "E:\Workspace\Voltec\docs\Products\V-Core\V1\meshes\scripts\run_all.py"
```

All 14 meshes are PLACEHOLDER quality (boolean primitives with EXACT solver). They need artist or AI replacement for production visuals.

---

## Patent Claims Summary

12 claims covering:
1. Factory-sealed residential micro-reactor with U-ZrH fuel + heat pipes + Stirling engines
2. Fuel rod geometry and enrichment specifications
3. Sodium heat pipe array (Inconel 718 + sintered nickel wick)
4. B₄C control drum system with gravity fail-safe
5. BeO neutron reflector
6. Graded lead-PE-boron biological shield
7. Free-piston Stirling engine specifications
8. V-Cell battery buffer + V-Mind AI control integration
9. Form factor constraints (height ≤1,000 mm, mass ≤800 kg)
10. Minimum fuel burnup and operational lifetime
11. Method of residential power via factory-sealed autonomous reactor
12. Combined heat and power recovery method

---

## Validation Status

See `SOTA_VALIDATION.md` for detailed three-tier assessment.

**Summary**:
- **VERIFIED**: U-ZrH fuel safety, heat pipe technology, Stirling engine operation, shielding materials
- **PROJECTED**: 25 kW output, 33% efficiency, 10-year life, 693 kg mass, $150K cost
- **ASPIRATIONAL**: Residential NRC licensing, egg form factor, public acceptance
