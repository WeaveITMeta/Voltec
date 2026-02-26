# V-Cell 3D Blueprints — EustressEngine `.glb.toml` Instance Files

## Overview

This directory contains the V-Cell solid-state battery blueprint in EustressEngine's **file-system-first** architecture. Each component is a standalone `.glb.toml` instance file that references a shared mesh primitive and defines per-instance transform, visual properties, and optional realism sections (`[material]`, `[thermodynamic]`, `[electrochemical]`).

> **Deprecation note**: The `.eustressengine` RON/JSON scene format is deprecated. All new content uses `.glb.toml` instance files loaded by `instance_loader.rs`.

## Architecture

```
assets/meshes/         ← Shared mesh primitives (block.glb, ball.glb, cylinder.glb, ...)
Workspace/             ← Per-instance .glb.toml files (one file = one entity)
  ├── VCell_Housing.glb.toml
  ├── VCell_Anode_Na.glb.toml
  └── ...
```

- **Mesh assets** are reusable GLB files in `assets/meshes/`
- **Instance files** define transform, color, material class, and realism data
- The engine's `instance_loader` scans `Workspace/` and spawns each `.glb.toml` as an ECS entity
- `AdvancedPart` class entities get `MaterialProperties`, `ThermodynamicState`, and `ElectrochemicalState` components attached automatically

## Instance Files

| File | Mesh | Class | Realism Sections |
|------|------|-------|------------------|
| `VCell_Housing.glb.toml` | `block.glb` | AdvancedPart | `[material]` `[thermodynamic]` |
| `VCell_Anode_Na.glb.toml` | `block.glb` | AdvancedPart | `[material]` `[thermodynamic]` `[electrochemical]` |
| `VCell_Electrolyte_ScNASICON.glb.toml` | `block.glb` | AdvancedPart | `[material]` `[thermodynamic]` `[electrochemical]` |
| `VCell_Cathode_SulfurVACNT.glb.toml` | `block.glb` | AdvancedPart | `[material]` `[thermodynamic]` `[electrochemical]` |
| `VCell_AlHexLattice.glb.toml` | `block.glb` | AdvancedPart | `[material]` `[thermodynamic]` |
| `VCell_ThermalPad_AlN.glb.toml` | `block.glb` | AdvancedPart | `[material]` `[thermodynamic]` |
| `VCell_Terminal_Positive.glb.toml` | `cylinder.glb` | Part | — |
| `VCell_Terminal_Negative.glb.toml` | `cylinder.glb` | Part | — |
| `VCell_StatusLED.glb.toml` | `ball.glb` | Part | — |

## Import into EustressEngine

### Copy to Workspace

Copy the `glb_instances/*.glb.toml` files into any Space's `Workspace/` folder:

```
Universe1/spaces/Space1/Workspace/
  ├── Baseplate.glb.toml           (existing)
  ├── Welcome Cube.glb.toml        (existing)
  ├── VCell_Housing.glb.toml       ← copy from glb_instances/
  ├── VCell_Anode_Na.glb.toml
  ├── VCell_Electrolyte_ScNASICON.glb.toml
  ├── VCell_Cathode_SulfurVACNT.glb.toml
  ├── VCell_AlHexLattice.glb.toml
  ├── VCell_ThermalPad_AlN.glb.toml
  ├── VCell_Terminal_Positive.glb.toml
  ├── VCell_Terminal_Negative.glb.toml
  └── VCell_StatusLED.glb.toml
```

The engine auto-discovers and spawns all `.glb.toml` files on load via `load_instance_files_system`.

### Programmatic Spawn

```rust
let toml_path = workspace_path.join("VCell_Anode_Na.glb.toml");
let instance = instance_loader::load_instance_definition(&toml_path)?;
let entity = instance_loader::spawn_instance(
    &mut commands, &asset_server, &space_root, toml_path, instance,
);
```

## Coordinate System

- **Origin**: Center of V-Cell housing at `[0.0, 4.5, 0.0]` (on lab table)
- **X-axis**: Cell length (display scale: 10.0 studs ≈ 300mm)
- **Y-axis**: Cell height — up (display scale: 1.0 stud ≈ 10mm)
- **Z-axis**: Cell width (display scale: 3.33 studs ≈ 100mm)
- **Scale**: 10× for visibility; actual dimensions in `[material.custom]`

## Entity Hierarchy (flat, file-system-first)

```
Workspace/
├── VCell_Housing.glb.toml          (AdvancedPart/Block — Al 6061-T6)
├── VCell_Anode_Na.glb.toml         (AdvancedPart/Block — Sodium metal)
├── VCell_Electrolyte_ScNASICON.glb.toml  (AdvancedPart/Block — Sc-NASICON ceramic)
├── VCell_Cathode_SulfurVACNT.glb.toml    (AdvancedPart/Block — S@VACNT composite)
├── VCell_AlHexLattice.glb.toml     (AdvancedPart/Block — Al hex lattice 92% porosity)
├── VCell_ThermalPad_AlN.glb.toml   (AdvancedPart/Block — AlN thermal pad)
├── VCell_Terminal_Positive.glb.toml (Part/Cylinder — Red terminal)
├── VCell_Terminal_Negative.glb.toml (Part/Cylinder — Black terminal)
└── VCell_StatusLED.glb.toml        (Part/Ball — Neon green status indicator)
```

## Realism Components Attached

For `AdvancedPart` class entities, the instance loader automatically converts TOML sections to ECS components:

- **`[material]`** → `MaterialProperties` (14 base fields + `custom` HashMap)
- **`[thermodynamic]`** → `ThermodynamicState` (temperature, pressure, volume, entropy, ...)
- **`[electrochemical]`** → `ElectrochemicalState` (voltage, SOC, current, cycle_count, dendrite_risk, ...)

## Custom Material Extensions

The `[material.custom]` HashMap stores domain-specific properties beyond the base struct:

- **Electrochemical**: `ionic_conductivity_s_cm`, `activation_energy_ev`, `specific_capacity_mah_g`
- **Lattice geometry**: `hex_edge_length_m`, `wall_thickness_m`, `porosity`
- **Cathode**: `sulfur_capacity_mah_g`, `volume_expansion`, `sulfur_loading_wt_pct`
- **Role tags**: `role = "anode"`, `"cathode"`, `"electrolyte"`, `"current_collector"`, `"housing"`, `"thermal_management"`
