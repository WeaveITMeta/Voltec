# V-Cell — EustressEngine Requirements Export

**Purpose**: Maps every V-Cell component to EustressEngine's realism crate properties and `.glb.toml` instance format.  
**Source Crate**: `eustress-common` → `src/realism/`  
**Instance Format**: File-system-first `.glb.toml` — see `blueprints/glb_instances/`  
**Format**: All values in SI units per EustressEngine convention.

---

## Table of Contents

1. [Required Crate Features](#1-required-crate-features)
2. [MaterialProperties — Per Component](#2-materialproperties--per-component)
3. [Instance File Structure](#3-instance-file-structure)
4. [ElectrochemicalState](#4-electrochemicalstate)
5. [ThermodynamicState](#5-thermodynamicstate)
6. [Electrochemistry Laws](#6-electrochemistry-laws)
7. [Realism Config](#7-realism-config)
8. [Structural Bundle Requirements](#8-structural-bundle-requirements)
9. [Deployment Checklist](#9-deployment-checklist)

---

## 1. Required Crate Features

From `eustress-common/Cargo.toml`:

| Feature Flag | Required | Purpose |
|-------------|----------|---------|
| `realism` | **Yes** | Core physics — MaterialProperties, thermodynamics, mechanics |
| `realism-full` | Recommended | Adds deformation, fracture, stress-strain |
| `realism-gpu` | Optional | GPU-accelerated thermal simulation |
| `realism-symbolic` | Optional | Symbolica for equation solving (Nernst, PV=nRT) |
| `realism-scripting` | Optional | Rune scripting for dynamic behavior |
| `realism-quantum` | Optional | Bose-Einstein / Fermi-Dirac for ion statistics |

> **Note**: As of Bevy 0.18, all `realism` features are gated and disabled. Electrochemistry functions in `realism::laws::electrochemistry` are pure `f32` math with no Bevy dependency and compile regardless.

---

## 2. MaterialProperties — Per Component

Each material maps to `realism::materials::properties::MaterialProperties` and is embedded inline in the `[material]` section of each `.glb.toml` instance file. Domain-specific extensions go in `[material.custom]`.

### 2.1 Housing — Aluminum 6061-T6

```toml
[material]
name = "Aluminum 6061-T6"
young_modulus = 68.9e9         # Pa
poisson_ratio = 0.33
yield_strength = 276.0e6      # Pa
ultimate_strength = 310.0e6   # Pa
fracture_toughness = 29.0e6   # Pa·√m
hardness = 95.0               # HV
thermal_conductivity = 167.0  # W/(m·K)
specific_heat = 896.0         # J/(kg·K)
thermal_expansion = 23.6e-6   # 1/K
melting_point = 855.0         # K
density = 2700.0              # kg/m³
friction_static = 0.61
friction_kinetic = 0.47
restitution = 0.7

[material.custom]
electrical_conductivity = 25.0e6  # S/m
role = "housing"
```

### 2.2 Solid Electrolyte — Sc-doped NASICON

```toml
[material]
name = "Sc-NASICON Electrolyte"
young_modulus = 80.0e9        # Pa
poisson_ratio = 0.25
yield_strength = 120.0e6     # Pa (compressive)
ultimate_strength = 150.0e6  # Pa
fracture_toughness = 1.5e6   # Pa·√m — brittle ceramic
hardness = 600.0              # HV
thermal_conductivity = 1.5    # W/(m·K)
specific_heat = 700.0         # J/(kg·K)
thermal_expansion = 8.5e-6    # 1/K
melting_point = 1553.0        # K
density = 3200.0              # kg/m³
friction_static = 0.5
friction_kinetic = 0.4
restitution = 0.3

[material.custom]
ionic_conductivity_s_cm = 0.01      # S/cm — target at 25°C
activation_energy_ev = 0.22         # eV
activation_energy_j_mol = 21224.0   # J/mol
arrhenius_prefactor = 1500.0        # S/cm
electronic_conductivity = 1.0e-10   # S/cm — must be negligible
vacancy_fraction = 0.067            # from x=0.2 Sc substitution
window_min_v = 0.0                  # V vs Na/Na⁺
window_max_v = 5.0                  # V vs Na/Na⁺
role = "electrolyte"
```

### 2.3 Anode — Sodium Metal

```toml
[material]
name = "Sodium Metal (Na)"
young_modulus = 10.0e9        # Pa — very soft
poisson_ratio = 0.29
yield_strength = 0.3e6       # Pa — extremely soft
ultimate_strength = 2.0e6    # Pa
fracture_toughness = 10.0e6  # Pa·√m — ductile
hardness = 0.5                # HV
thermal_conductivity = 142.0  # W/(m·K)
specific_heat = 1228.0        # J/(kg·K)
thermal_expansion = 71.0e-6   # 1/K
melting_point = 370.95        # K (97.8°C)
density = 971.0               # kg/m³
friction_static = 0.8
friction_kinetic = 0.6
restitution = 0.1

[material.custom]
electrical_conductivity = 21.0e6   # S/m
specific_capacity_mah_g = 1166.0   # mAh/g
standard_potential_she = -2.714    # V vs SHE
role = "anode"
```

### 2.4 Cathode — Sulfur@VACNT Composite

```toml
[material]
name = "Sulfur@VACNT Cathode"
young_modulus = 50.0e9        # Pa — CNT-dominated
poisson_ratio = 0.24
yield_strength = 25.0e6      # Pa
ultimate_strength = 35.0e6   # Pa
fracture_toughness = 2.0e6   # Pa·√m
hardness = 40.0               # HV (effective)
thermal_conductivity = 15.0   # W/(m·K) — CNT-enhanced
specific_heat = 705.0         # J/(kg·K)
thermal_expansion = 10.0e-6   # 1/K
melting_point = 388.36        # K (115.2°C — sulfur melting)
density = 1075.0              # kg/m³ — composite bulk
friction_static = 0.3
friction_kinetic = 0.2
restitution = 0.3

[material.custom]
sulfur_capacity_mah_g = 1672.0   # mAh/g
volume_expansion = 0.80          # S → Na₂S full discharge
sulfur_loading_wt_pct = 70.0     # wt% sulfur in composite
cnt_height_um = 200.0            # μm VACNT height
role = "cathode"
```

### 2.5 Current Collector — Aluminum Hexagonal Lattice

```toml
[material]
name = "Al Hex Lattice (92% porosity)"
young_modulus = 4.2e9         # Pa — reduced by porosity
poisson_ratio = 0.33
yield_strength = 16.2e6      # Pa — reduced by porosity
ultimate_strength = 22.0e6   # Pa
fracture_toughness = 2.3e6   # Pa·√m
hardness = 7.6                # HV (effective)
thermal_conductivity = 19.0   # W/(m·K) — effective
specific_heat = 897.0         # J/(kg·K)
thermal_expansion = 23.1e-6   # 1/K
melting_point = 933.47        # K (660.3°C)
density = 216.0               # kg/m³ — 8% of bulk Al
friction_static = 0.5
friction_kinetic = 0.35
restitution = 0.5

[material.custom]
hex_edge_length_m = 50.0e-6   # m — 50μm cells
wall_thickness_m = 5.0e-6     # m — 5μm walls
porosity = 0.92
electrical_conductivity = 2.9e6  # S/m — effective
role = "current_collector"
```

### 2.6 Thermal Pad — Aluminum Nitride (AlN)

```toml
[material]
name = "Aluminum Nitride (AlN)"
young_modulus = 310.0e9       # Pa
poisson_ratio = 0.24
yield_strength = 300.0e6     # Pa (flexural)
ultimate_strength = 350.0e6  # Pa
fracture_toughness = 3.0e6   # Pa·√m
hardness = 1200.0             # HV
thermal_conductivity = 170.0  # W/(m·K) — excellent thermal bridge
specific_heat = 740.0         # J/(kg·K)
thermal_expansion = 4.6e-6    # 1/K
melting_point = 2473.0        # K
density = 3260.0              # kg/m³
friction_static = 0.4
friction_kinetic = 0.3
restitution = 0.4

[material.custom]
role = "thermal_management"
```

---

## 3. Instance File Structure

EustressEngine uses the **file-system-first** `.glb.toml` format. Each V-Cell component is a standalone file in `Workspace/`. The instance loader (`instance_loader.rs`) scans `Workspace/` on startup and spawns each file as a Bevy ECS entity.

### File → Entity Mapping

| `.glb.toml` File | Mesh | `class_name` | Components Attached |
|---|---|---|---|
| `VCell_Housing.glb.toml` | `block.glb` | `AdvancedPart` | `MaterialProperties` + `ThermodynamicState` |
| `VCell_Anode_Na.glb.toml` | `block.glb` | `AdvancedPart` | `MaterialProperties` + `ThermodynamicState` + `ElectrochemicalState` |
| `VCell_Electrolyte_ScNASICON.glb.toml` | `block.glb` | `AdvancedPart` | `MaterialProperties` + `ThermodynamicState` + `ElectrochemicalState` |
| `VCell_Cathode_SulfurVACNT.glb.toml` | `block.glb` | `AdvancedPart` | `MaterialProperties` + `ThermodynamicState` + `ElectrochemicalState` |
| `VCell_AlHexLattice.glb.toml` | `block.glb` | `AdvancedPart` | `MaterialProperties` + `ThermodynamicState` |
| `VCell_ThermalPad_AlN.glb.toml` | `block.glb` | `AdvancedPart` | `MaterialProperties` + `ThermodynamicState` |
| `VCell_Terminal_Positive.glb.toml` | `cylinder.glb` | `Part` | — |
| `VCell_Terminal_Negative.glb.toml` | `cylinder.glb` | `Part` | — |
| `VCell_StatusLED.glb.toml` | `ball.glb` | `Part` | — |

### Standard Sections

```toml
[asset]
mesh = "assets/meshes/block.glb"   # shared primitive
scene = "Scene0"

[transform]
position = [x, y, z]               # studs, world space
rotation = [0.0, 0.0, 0.0, 1.0]   # quaternion
scale = [width, height, depth]     # studs

[properties]
color = [r, g, b, a]
transparency = 0.0
anchored = true
can_collide = true
cast_shadow = true
reflectance = 0.0

[metadata]
class_name = "AdvancedPart"        # or "Part"
archivable = true
created = "..."
last_modified = "..."

[material]        # AdvancedPart only — see Section 2
[thermodynamic]   # AdvancedPart only — see Section 5
[electrochemical] # AdvancedPart only — see Section 4
```

### Transform — V-Cell Stack Layout

All positions relative to world origin. Components stacked along Y at table height (4.0 studs). Display scale = 10× actual dimensions.

| Component | `position` [x,y,z] | `scale` [w,h,d] | Actual thickness |
|---|---|---|---|
| Housing | [0.0, 4.5, 0.0] | [10.0, 1.0, 3.33] | 10mm |
| AlN Thermal Pad | [0.0, 4.0, 0.0] | [9.5, 0.02, 3.0] | 0.2mm |
| Na Anode | [0.0, 4.25, 0.0] | [9.0, 0.05, 2.8] | 50μm |
| Sc-NASICON | [0.0, 4.50, 0.0] | [9.0, 0.03, 2.8] | 30μm |
| Al Hex Lattice | [0.0, 4.50, 0.0] | [9.0, 0.20, 2.8] | 200μm |
| S@VACNT Cathode | [0.0, 4.75, 0.0] | [9.0, 0.15, 2.8] | 150μm |
| Terminal (+) | [5.5, 5.15, 0.0] | [0.8, 0.3, 0.8] | — |
| Terminal (−) | [−5.5, 5.15, 0.0] | [0.8, 0.3, 0.8] | — |
| Status LED | [4.0, 5.2, 1.5] | [0.3, 0.3, 0.3] | — |

---

## 4. ElectrochemicalState

From `realism::particles::components::ElectrochemicalState` — attached to `AdvancedPart` entities with an `[electrochemical]` section. Maps to `TomlElectrochemicalState` in `instance_loader.rs`.

| Field | Type | Initial Value | Unit | Notes |
|---|---|---|---|---|
| `voltage` | `f32` | 2.23 | V | Na-S standard potential |
| `terminal_voltage` | `f32` | 2.23 | V | Computed at runtime |
| `capacity_ah` | `f32` | 202.5 | Ah | Full cell nominal |
| `soc` | `f32` | 1.0 | — | 0.0 = empty, 1.0 = full |
| `current` | `f32` | 0.0 | A | Positive = discharge |
| `internal_resistance` | `f32` | 0.003 | Ω | Electrolyte dominant |
| `ionic_conductivity` | `f32` | 0.01 | S/cm | Sc-NASICON at 25°C |
| `cycle_count` | `u32` | 0 | — | Incremented per cycle |
| `c_rate` | `f32` | 0.0 | h⁻¹ | I / Q_nom |
| `capacity_retention` | `f32` | 1.0 | — | 1.0 = fresh, 0.8 = EOL |
| `heat_generation` | `f32` | 0.0 | W | Total Q_ohm + Q_rxn + Q_entropy |
| `dendrite_risk` | `f32` | 0.0 | — | 0.0 = safe, ≥1.0 = risk |

### Runtime Update Flow

```
tick:
  soc          ← state_of_charge(soc, Δq, capacity_ah)
  voltage      ← na_s_ocv_temp_corrected(soc, temperature)
  η_ohm        ← ohmic_overpotential(current, internal_resistance)
  terminal_voltage ← terminal_voltage(voltage, η_ohm, η_ct, 0.0, is_discharge)
  heat_generation  ← total_heat_generation(current, internal_resistance, η_ct, temperature, dE_dT)
  capacity_retention ← vcell_capacity_at_cycle(1.0, cycle_count as f32, c_rate)
  dendrite_risk    ← vcell_dendrite_risk(current / electrode_area, temperature)
  ionic_conductivity ← sc_nasicon_conductivity(temperature)  # S/cm
```

---

## 5. ThermodynamicState

From `realism::particles::components::ThermodynamicState` — attached to all `AdvancedPart` entities via `[thermodynamic]` section.

| Field | Type | Initial Value | Unit | Notes |
|---|---|---|---|---|
| `temperature` | `f32` | 298.15 | K | Ambient (25°C) |
| `pressure` | `f32` | 101325.0 | Pa | 1 atm |
| `volume` | `f32` | 3.6e-4 | m³ | 360 cm³ total cell |
| `internal_energy` | `f32` | 0.0 | J | Computed from Q·V |
| `entropy` | `f32` | 0.0 | J/K | Computed at runtime |
| `enthalpy` | `f32` | 0.0 | J | Computed at runtime |
| `moles` | `f32` | 1.0 | mol | Per active material |

### Operating Envelope

| Condition | Min | Max | Unit |
|---|---|---|---|
| Temperature (full performance) | 253.15 | 333.15 | K (−20°C to 60°C) |
| Temperature (operational) | 233.15 | 353.15 | K (−40°C to 80°C) |
| Pressure | 80,000 | 120,000 | Pa |
| SOC operating range | 0.10 | 0.95 | — |

---

## 6. Electrochemistry Laws

From `realism::laws::electrochemistry` — pure functions, no Bevy dependency.

### Available Functions

| Function | Signature | Purpose |
|---|---|---|
| `nernst_potential` | `(e°, n, T, Q) → V` | Equilibrium potential |
| `butler_volmer_current` | `(j₀, η, αₐ, αc, T) → A/m²` | Charge transfer kinetics |
| `butler_volmer_symmetric` | `(j₀, η, T) → A/m²` | Simplified (α=0.5) |
| `tafel_overpotential` | `(j, j₀, α, T) → V` | High-η limit |
| `ohmic_overpotential` | `(I, R) → V` | IR drop |
| `terminal_voltage` | `(OCV, η_ohm, η_ct, η_diff, discharge) → V` | Full voltage model |
| `round_trip_efficiency` | `(V_dis, V_chg) → —` | Coulombic × voltage eff. |
| `arrhenius_conductivity` | `(σ₀, Eₐ, T) → S/cm` | Temperature-dependent σ |
| `sc_nasicon_conductivity` | `(T) → S/cm` | Pre-calibrated for V-Cell |
| `sc_nasicon_asr` | `(thickness, T) → Ω·m²` | ASR from conductivity |
| `vcell_electrolyte_resistance` | `(T, area) → Ω` | Cell-level R at 30μm |
| `total_heat_generation` | `(I, R, η_ct, T, dE/dT) → W` | Q_ohm + Q_rxn + Q_entropy |
| `na_s_ocv` | `(SOC) → V` | Piecewise 2-plateau OCV |
| `na_s_ocv_temp_corrected` | `(SOC, T) → V` | With dE/dT correction |
| `sulfur_utilization` | `(Q_mah, m_S) → —` | Fraction of 1672 mAh/g |
| `capacity_retention_power_law` | `(N, α, β) → —` | `1 − α·N^β` |
| `vcell_degradation_params` | `(C_rate) → (α, β)` | C-rate calibrated params |
| `vcell_capacity_at_cycle` | `(Q₀, N, C) → Ah` | Convenience wrapper |
| `state_of_charge` | `(SOC₀, Q_out, Q_nom) → —` | Coulomb counting |
| `c_rate` | `(I, Q_nom) → h⁻¹` | Normalized current |
| `sands_time` | `(D, c, j) → s` | Dendrite onset time |
| `monroe_newman_critical_current` | `(G_e, δ) → A/m²` | Mechanical dendrite limit |
| `vcell_dendrite_risk` | `(j, T) → —` | Risk factor 0–∞ |

### V-Cell Calibrated Constants

| Constant | Value | Unit | Source |
|---|---|---|---|
| `na_s::STANDARD_POTENTIAL` | 2.23 | V | Electrochemistry |
| `na_s::SULFUR_CAPACITY_MAH_G` | 1672.0 | mAh/g | Theoretical |
| `na_s::SULFUR_VOLUME_EXPANSION` | 0.80 | — | S → Na₂S |
| `na_s::ENTROPY_COEFFICIENT` | −1.5e-4 | V/K | dE/dT |
| `sc_nasicon::IONIC_CONDUCTIVITY_TARGET` | 1.0e-2 | S/cm | Target |
| `sc_nasicon::ACTIVATION_ENERGY_J_MOL` | 21,224 | J/mol | Literature |
| `sc_nasicon::ARRHENIUS_PREFACTOR` | 1,500 | S/cm | Calibrated |

---

## 7. Realism Config

From `realism::RealismConfig` — set as a Bevy `Resource`:

```toml
[realism_config]
thermodynamics_enabled = true
materials_enabled = true
fluids_enabled = false       # no liquid phase in solid-state cell
visualizers_enabled = true   # temperature + stress overlays
time_scale = 1.0             # real-time
max_fluid_particles = 0
spatial_cell_size = 0.01     # 1cm thermal grid
parallel_enabled = true
```

---

## 8. Structural Bundle Requirements

From `realism::materials::properties::StructuralBundle` — attached to deformable `AdvancedPart` entities (housing, electrolyte).

| Component | Initial Value | Notes |
|---|---|---|
| `MaterialProperties` | See Section 2 | Per-material preset |
| `StressTensor` | Zero | Updated by `update_stress_strain` system |
| `StrainTensor` | Zero | Updated by `update_stress_strain` system |
| `FractureState` | Default | Crack tracking — critical for brittle Sc-NASICON |
| `DeformationState` | Default | Elastic/plastic deformation |

**Priority components for fracture monitoring**:
- `VCell_Electrolyte_ScNASICON` — K_IC = 1.5 MPa·√m, brittle ceramic, fracture must be checked
- `VCell_Housing` — ductile Al 6061-T6, deformation tracking for pressure cycling

---

## 9. Deployment Checklist

### Copy instance files to Space Workspace

```
Universe1/spaces/Space1/Workspace/
  ├── VCell_Housing.glb.toml
  ├── VCell_Anode_Na.glb.toml
  ├── VCell_Electrolyte_ScNASICON.glb.toml
  ├── VCell_Cathode_SulfurVACNT.glb.toml
  ├── VCell_AlHexLattice.glb.toml
  ├── VCell_ThermalPad_AlN.glb.toml
  ├── VCell_Terminal_Positive.glb.toml
  ├── VCell_Terminal_Negative.glb.toml
  └── VCell_StatusLED.glb.toml
```

Source: `E:\Workspace\Voltec\docs\Products\V-Cell\blueprints\glb_instances\`

### Pre-launch Checks

- [ ] All 9 `.glb.toml` files present in `Workspace/`
- [ ] `assets/meshes/block.glb`, `cylinder.glb`, `ball.glb` present in Space assets
- [ ] `eustress-common` compiled (realism gated — pure electrochemistry functions still available)
- [ ] `ElectrochemicalState` component registered in Bevy `App` (via `MaterialsPlugin`)
- [ ] `sc_nasicon_conductivity(298.15)` returns > 1e-4 S/cm (sanity check)
- [ ] `vcell_dendrite_risk(1.0, 298.15)` returns < 0.01 at rest current

### Runtime Validation

- [ ] OCV at full SOC ≈ 2.35 V: `na_s_ocv(1.0)` → 2.80 V (open circuit)
- [ ] Capacity retention at 10,000 cycles (0.5C) ≈ 80%: `vcell_capacity_at_cycle(1.0, 10000.0, 0.5)` → ~0.80
- [ ] Electrolyte ASR at 25°C with 30μm membrane: `sc_nasicon_asr(30e-6, 298.15)` → ~3 Ω·cm²

---

*End of EustressEngine Requirements Export*
