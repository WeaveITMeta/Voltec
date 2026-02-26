# V-Incinerator — EustressEngine Requirements

## Table of Contents

1. Required Crate Features
2. MaterialProperties — Per Component
3. Instance File Structure
4. ThermodynamicState
5. Domain Laws (Combustion & Heat Transfer)
6. Realism Config
7. Structural Bundle Requirements
8. Deployment Checklist

---

## 1. Required Crate Features

| Feature Flag | Purpose |
|-------------|---------|
| `realism` | Base realism system — MaterialProperties, ThermodynamicState |
| `realism_thermodynamics` | Thermodynamic laws (heat conduction, radiation, convection) |
| `realism_structural` | Structural simulation (thermal stress, creep, fatigue) |

> **Note**: V-Incinerator does not require `realism_electrochemistry`. It is a thermal/mechanical/fluid system.

---

## 2. MaterialProperties — Per Component

### 2.1 Outer Housing — 316L Stainless Steel

```toml
[material]
name = "316L Stainless Steel"
young_modulus = 193000000000.0
poisson_ratio = 0.27
yield_strength = 170000000.0
ultimate_strength = 485000000.0
fracture_toughness = 112000000.0
hardness = 217.0
thermal_conductivity = 16.3
specific_heat = 500.0
thermal_expansion = 0.000016
melting_point = 1673.0
density = 8000.0
friction_static = 0.6
friction_kinetic = 0.42
restitution = 0.5

[material.custom]
pren = 24.2
corrosion_rate_mm_yr = 0.01
role = "housing"
```

### 2.2 Plasma Chamber — Tungsten (W)

```toml
[material]
name = "Tungsten (W)"
young_modulus = 411000000000.0
poisson_ratio = 0.28
yield_strength = 750000000.0
ultimate_strength = 980000000.0
fracture_toughness = 20000000.0
hardness = 3430.0
thermal_conductivity = 173.0
specific_heat = 132.0
thermal_expansion = 0.0000045
melting_point = 3695.0
density = 19300.0
friction_static = 0.5
friction_kinetic = 0.4
restitution = 0.3

[material.custom]
liner_thickness_m = 0.003
plasma_erosion_rate_mm_per_1000h = 0.1
torch_power_kw = 1500.0
torch_count = 3
operating_temp_max_k = 7773.0
role = "plasma_chamber"
```

### 2.3 Primary Combustion Chamber — Inconel 718

```toml
[material]
name = "Inconel 718 (Ni-Cr Superalloy)"
young_modulus = 200000000000.0
poisson_ratio = 0.30
yield_strength = 1035000000.0
ultimate_strength = 1240000000.0
fracture_toughness = 96000000.0
hardness = 388.0
thermal_conductivity = 11.4
specific_heat = 435.0
thermal_expansion = 0.000013
melting_point = 1609.0
density = 8190.0
friction_static = 0.6
friction_kinetic = 0.45
restitution = 0.4

[material.custom]
creep_rupture_100kh_mpa = 620.0
oxidation_limit_k = 1255.0
wall_thickness_m = 0.025
refractory_thickness_m = 0.1
dwell_time_s = 2.0
role = "combustion_chamber"
```

### 2.4 Heat Exchanger — Copper-Nickel C71500

```toml
[material]
name = "Copper-Nickel C71500 (70Cu-30Ni)"
young_modulus = 150000000000.0
poisson_ratio = 0.34
yield_strength = 170000000.0
ultimate_strength = 420000000.0
fracture_toughness = 65000000.0
hardness = 120.0
thermal_conductivity = 29.0
specific_heat = 380.0
thermal_expansion = 0.0000162
melting_point = 1443.0
density = 8950.0
friction_static = 0.5
friction_kinetic = 0.4
restitution = 0.35

[material.custom]
tube_count = 240
tube_od_m = 0.0254
tube_wall_m = 0.0021
thermal_duty_mw = 4.5
steam_output_mw = 3.8
steam_temp_k = 813.15
steam_pressure_mpa = 10.0
role = "heat_exchanger"
```

### 2.5 HEPA Filter Bank — Borosilicate Glass Fiber

```toml
[material]
name = "Borosilicate Glass Fiber"
young_modulus = 64000000000.0
poisson_ratio = 0.20
yield_strength = 70000000.0
ultimate_strength = 70000000.0
fracture_toughness = 700000.0
hardness = 480.0
thermal_conductivity = 1.14
specific_heat = 830.0
thermal_expansion = 0.0000033
melting_point = 1921.0
density = 2230.0
friction_static = 0.4
friction_kinetic = 0.3
restitution = 0.2

[material.custom]
filtration_efficiency_pct = 99.97
mpps_um = 0.3
filter_area_m2 = 48.0
pressure_drop_clean_pa = 250.0
pressure_drop_loaded_pa = 750.0
max_operating_temp_k = 533.15
service_life_hours = 10000.0
role = "hepa_filter"
```

### 2.6 Catalytic Converter — Pt-Pd on γ-Alumina (Inconel 625 Housing)

```toml
[material]
name = "Inconel 625 (Catalyst Housing)"
young_modulus = 205000000000.0
poisson_ratio = 0.31
yield_strength = 490000000.0
ultimate_strength = 827000000.0
fracture_toughness = 90000000.0
hardness = 250.0
thermal_conductivity = 9.8
specific_heat = 410.0
thermal_expansion = 0.0000128
melting_point = 1623.0
density = 8440.0
friction_static = 0.55
friction_kinetic = 0.42
restitution = 0.35

[material.custom]
catalyst_pt_g_per_l = 2.0
catalyst_pd_g_per_l = 1.0
substrate_cpsi = 400
washcoat_surface_area_m2_per_g = 120.0
dioxin_destruction_pct = 99.9
pah_destruction_pct = 99.5
nox_reduction_pct = 90.0
operating_temp_k = 573.15
space_velocity_per_h = 10000.0
service_life_hours = 40000.0
role = "catalytic_converter"
```

### 2.7 Activated Carbon Bed — Granular Activated Carbon (304SS Vessel)

```toml
[material]
name = "304 Stainless Steel (Carbon Bed Vessel)"
young_modulus = 193000000000.0
poisson_ratio = 0.29
yield_strength = 215000000.0
ultimate_strength = 505000000.0
fracture_toughness = 100000000.0
hardness = 201.0
thermal_conductivity = 16.2
specific_heat = 500.0
thermal_expansion = 0.0000173
melting_point = 1673.0
density = 8000.0
friction_static = 0.6
friction_kinetic = 0.42
restitution = 0.5

[material.custom]
carbon_type = "bituminous_coal_based"
iodine_number = 1000.0
bed_depth_m = 0.5
cross_section_m2 = 4.0
contact_time_s = 2.5
hg_removal_pct = 99.0
pb_removal_pct = 99.0
cd_removal_pct = 99.0
voc_removal_pct = 95.0
replacement_interval_hours = 7000.0
role = "carbon_bed"
```

### 2.8 Wet Scrubber Column — Hastelloy C-276

```toml
[material]
name = "Hastelloy C-276"
young_modulus = 205000000000.0
poisson_ratio = 0.31
yield_strength = 355000000.0
ultimate_strength = 785000000.0
fracture_toughness = 100000000.0
hardness = 235.0
thermal_conductivity = 10.2
specific_heat = 427.0
thermal_expansion = 0.0000115
melting_point = 1623.0
density = 8890.0
friction_static = 0.55
friction_kinetic = 0.42
restitution = 0.35

[material.custom]
scrubbing_agent = "NaOH"
hcl_removal_pct = 99.8
so2_removal_pct = 97.5
hf_removal_pct = 99.0
packing_type = "structured"
column_height_m = 3.0
column_diameter_m = 1.2
role = "wet_scrubber"
```

### 2.9 Exhaust Stack — 304 Stainless Steel

Uses same base material as Carbon Bed vessel (304SS) but with `role = "exhaust_stack"`.

### 2.10 Ash Collection Hopper — A36 Carbon Steel (Refractory-Lined)

```toml
[material]
name = "A36 Carbon Steel"
young_modulus = 200000000000.0
poisson_ratio = 0.26
yield_strength = 250000000.0
ultimate_strength = 400000000.0
fracture_toughness = 50000000.0
hardness = 119.0
thermal_conductivity = 50.2
specific_heat = 486.0
thermal_expansion = 0.0000119
melting_point = 1698.0
density = 7850.0
friction_static = 0.57
friction_kinetic = 0.42
restitution = 0.5

[material.custom]
refractory_lining_thickness_m = 0.05
slag_output_temp_k = 1473.0
slag_vitrification = "TCLP_inert"
role = "ash_hopper"
```

---

## 3. Instance File Structure

### File → Entity Mapping

| File | Mesh Reference | Class | Realism Sections |
|------|---------------|-------|------------------|
| `VIncinerator_Housing.glb.toml` | `block.glb` | AdvancedPart | material, thermodynamic |
| `VIncinerator_PlasmaChamber.glb.toml` | `cylinder.glb` | AdvancedPart | material, thermodynamic |
| `VIncinerator_CombustionChamber.glb.toml` | `cylinder.glb` | AdvancedPart | material, thermodynamic |
| `VIncinerator_HeatExchanger.glb.toml` | `block.glb` | AdvancedPart | material, thermodynamic |
| `VIncinerator_HEPAFilter.glb.toml` | `block.glb` | AdvancedPart | material, thermodynamic |
| `VIncinerator_CatalyticConverter.glb.toml` | `block.glb` | AdvancedPart | material, thermodynamic |
| `VIncinerator_CarbonBed.glb.toml` | `block.glb` | AdvancedPart | material, thermodynamic |
| `VIncinerator_WetScrubber.glb.toml` | `cylinder.glb` | AdvancedPart | material, thermodynamic |
| `VIncinerator_ExhaustStack.glb.toml` | `cylinder.glb` | Part | — |
| `VIncinerator_AshHopper.glb.toml` | `block.glb` | AdvancedPart | material, thermodynamic |
| `VIncinerator_WasteFeed.glb.toml` | `block.glb` | Part | — |
| `VIncinerator_ControlModule.glb.toml` | `block.glb` | Part | — |
| `VIncinerator_StatusArray.glb.toml` | `ball.glb` | Part | — |

### Transform Layout (meters, Y-up, origin at geometric center of housing)

| Component | Position [x, y, z] | Scale [x, y, z] | Notes |
|-----------|-------------------|-----------------|-------|
| Housing | [0.0, 2.0, 0.0] | [6.0, 4.0, 3.0] | Outer shell |
| Plasma Chamber | [0.0, 0.75, 0.0] | [1.2, 1.5, 1.2] | Bottom center |
| Combustion Chamber | [0.0, 2.0, 0.0] | [1.8, 3.6, 1.8] | Above plasma |
| Heat Exchanger | [0.0, 3.2, 0.0] | [1.2, 3.0, 1.2] | Above combustion |
| HEPA Filter | [2.0, 3.0, 0.0] | [1.0, 1.5, 1.5] | Side-mounted |
| Catalytic Converter | [2.0, 3.0, 1.0] | [0.8, 1.0, 0.8] | After HEPA |
| Carbon Bed | [2.0, 3.0, -1.0] | [1.0, 1.0, 1.0] | After catalyst |
| Wet Scrubber | [-2.0, 2.5, 0.0] | [1.2, 3.0, 1.2] | Side column |
| Exhaust Stack | [-2.0, 5.0, 0.0] | [0.6, 3.0, 0.6] | Above scrubber |
| Ash Hopper | [0.0, -0.5, 0.0] | [1.5, 1.0, 1.5] | Below plasma |
| Waste Feed | [-2.5, 0.75, 0.0] | [1.5, 0.8, 1.0] | Side intake |
| Control Module | [2.8, 1.5, 1.2] | [0.4, 0.6, 0.3] | Exterior panel |
| Status Array | [2.8, 2.5, 1.2] | [0.1, 0.1, 0.1] | Above control |

---

## 4. ThermodynamicState

### Fields

| Field | Type | Unit | Description |
|-------|------|------|-------------|
| `temperature` | f64 | K | Current component temperature |
| `pressure` | f64 | Pa | Internal gas/fluid pressure |
| `volume` | f64 | m³ | Component volume |
| `internal_energy` | f64 | J | Stored thermal energy |
| `entropy` | f64 | J/K | Thermodynamic entropy |
| `enthalpy` | f64 | J | Enthalpy (U + PV) |
| `moles` | f64 | mol | Gas/fluid moles in component |

### Initial Values Per Component

| Component | Temperature (K) | Pressure (Pa) | Volume (m³) |
|-----------|-----------------|---------------|-------------|
| Housing | 298.15 | 101325.0 | 72.0 |
| Plasma Chamber | 298.15 | 101325.0 | 1.696 |
| Combustion Chamber | 298.15 | 121590.0 | 9.16 |
| Heat Exchanger | 298.15 | 101325.0 | 3.39 |
| HEPA Filter | 298.15 | 101325.0 | 2.25 |
| Catalytic Converter | 298.15 | 101325.0 | 0.50 |
| Carbon Bed | 298.15 | 101325.0 | 2.0 |
| Wet Scrubber | 298.15 | 101325.0 | 3.39 |
| Ash Hopper | 298.15 | 101325.0 | 2.25 |

### Operating Envelope

| Parameter | Min | Nominal | Max | Unit |
|-----------|-----|---------|-----|------|
| Plasma chamber temperature | 4773.15 | 6273.15 | 7773.15 | K |
| Combustion chamber gas temp | 1273.15 | 1473.15 | 1673.15 | K |
| Heat exchanger inlet temp | 973.15 | 1123.15 | 1223.15 | K |
| HEPA bank operating temp | 423.15 | 473.15 | 533.15 | K |
| Catalyst bed temp | 523.15 | 573.15 | 653.15 | K |
| Scrubber outlet temp | 313.15 | 328.15 | 353.15 | K |
| Ambient range | 243.15 | 293.15 | 323.15 | K |

### Runtime Update Flow

```
for each tick:
    // 1. Compute heat input
    Q_plasma = torch_power × 3                    // 1500 kW total
    Q_waste  = waste_rate × calorific_value        // 8–12 MJ/kg × kg/s

    // 2. Plasma chamber temperature
    plasma_chamber.T = f(Q_plasma + Q_waste, mass, Cp_gas)

    // 3. Combustion chamber — secondary burn
    combustion.T = f(syngas_enthalpy, O2_enrichment, dwell_time)
    if combustion.T < 1273.15 K:
        ALARM: increase O2 or plasma power

    // 4. Heat exchanger — steam generation
    Q_recovered = 0.85 × Q_exhaust
    steam.T = 813.15 K  // superheated
    turbine_output_kw = Q_recovered × 0.38

    // 5. HEPA bank — temperature must stay < 533 K
    hepa.T = exhaust_post_hx.T
    if hepa.T > 533.15 K:
        ALARM: cooling spray activation

    // 6. Catalyst — optimal 573 K window
    catalyst.T = hepa_outlet.T + reheat_if_needed
    dioxin_destruction = f(catalyst.T, space_velocity)

    // 7. Carbon bed — must stay < 423 K
    carbon.T = catalyst_outlet.T - cooling
    hg_removal = f(contact_time, bed_saturation)

    // 8. Wet scrubber — NaOH neutralization
    scrubber.T = gas_outlet.T_saturated  // ~328 K
    hcl_removal = f(NaOH_flow, gas_flow, pH)

    // 9. Stack emissions — final check
    assert particulates < 0.03 mg/Nm³
    assert dioxins < 0.01 ng TEQ/Nm³
    assert hcl < 1.0 mg/Nm³
```

---

## 5. Domain Laws (Combustion & Heat Transfer)

### Available Functions (realism::laws::thermodynamics)

| Function | Signature | Purpose |
|----------|-----------|---------|
| `fourier_heat_conduction` | `(k, A, dT, dx) → Q` | Conductive heat flow through walls |
| `newton_cooling` | `(h, A, T_surface, T_fluid) → Q` | Convective heat transfer |
| `stefan_boltzmann_radiation` | `(ε, σ, A, T_hot, T_cold) → Q` | Radiative heat transfer (plasma + combustion) |
| `specific_heat_energy` | `(m, Cp, dT) → Q` | Energy stored in mass at temperature |

### Calibrated Constants — V-Incinerator

| Constant | Value | Unit | Source |
|----------|-------|------|--------|
| Plasma torch power (total) | 1500000.0 | W | 3 × 500 kW DC |
| MSW calorific value (nominal) | 10500000.0 | J/kg | US EPA average |
| Waste feed rate (nominal) | 0.116 | kg/s | 10 tons/day |
| Combustion air excess ratio | 1.5 | — | O₂-enriched |
| Heat exchanger effectiveness | 0.85 | — | Shell-and-tube |
| Turbine isentropic efficiency | 0.38 | — | Small-scale steam |
| HEPA max operating temperature | 533.15 | K | Borosilicate limit |
| Catalyst optimal temperature | 573.15 | K | Pt-Pd activation |
| NaOH solution concentration | 0.1 | mol/L | Scrubbing solution |
| Stefan-Boltzmann constant | 0.0000000567 | W/(m²·K⁴) | Physics |
| Tungsten emissivity (high T) | 0.35 | — | At 3000 K |
| Inconel 718 emissivity | 0.65 | — | Oxidized surface |

---

## 6. Realism Config

```toml
[realism]
enabled = true
tick_rate = 60
thermal_enabled = true
structural_enabled = true
electrochemical_enabled = false

[realism.thermal]
ambient_temperature = 293.15
simulation_scale = 1.0

[realism.structural]
gravity = [0.0, -9.81, 0.0]
enable_fracture = true
```

---

## 7. Structural Bundle Requirements

| Component | Structural Priority | Key Concern |
|-----------|-------------------|-------------|
| Plasma Chamber (W) | **Critical** | Thermal erosion, arc damage, liner integrity |
| Combustion Chamber (Inconel 718) | **Critical** | High-temperature creep, thermal fatigue, oxidation |
| Heat Exchanger (C71500) | **High** | Tube corrosion, thermal cycling fatigue |
| Wet Scrubber (Hastelloy C-276) | **High** | Acid corrosion, stress corrosion cracking |
| Housing (316L SS) | **Medium** | Seismic loads, wind loads, thermal insulation |
| Ash Hopper (A36) | **Medium** | Slag impact, refractory spalling |
| HEPA Filter (glass fiber) | **Low** | Consumable — monitor ΔP, replace |
| Catalytic Converter (Inconel 625) | **Low** | Poisoning degradation, not structural failure |
| Carbon Bed (304SS) | **Low** | Consumable bed, vessel is standard |

### Notes

- **Inconel 718 combustion chamber** is the most structurally critical component: 100,000-hour creep life at 700°C wall temperature. Annual ultrasonic inspection required.
- **Tungsten liner** erodes at ~0.1 mm/1,000 hours — 3 mm liner gives ~30,000 hours (3.4 years) before replacement.
- **C71500 heat exchanger tubes** must withstand acidic condensation on cold side — Cu-Ni alloy selected specifically for this corrosion resistance.

---

## 8. Deployment Checklist

### Copy Instance Files

1. Copy all `V1/*.glb.toml` files to `Universe1/spaces/Space1/Workspace/`
2. Ensure referenced `.glb` mesh files exist at `assets/meshes/` paths (primitives: block.glb, cylinder.glb, ball.glb)
3. Restart EustressEngine or trigger workspace rescan

### Pre-Launch Checks

- [ ] All 13 `.glb.toml` files parse without errors
- [ ] All `AdvancedPart` entities have `[material]` and `[thermodynamic]` sections
- [ ] No `[electrochemical]` sections present (V-Incinerator is thermal, not electrochemical)
- [ ] All positions in meters, Y-up coordinate system
- [ ] All material values in SI units
- [ ] `[material.custom]` fields include `role` tag on every component
- [ ] ISO 8601 timestamps in all `[metadata]` sections

### Runtime Validation — Sanity Checks

| Check | Expected Value | Tolerance |
|-------|---------------|-----------|
| Plasma chamber temperature at steady state | ~6273 K | ±1500 K |
| Combustion chamber wall temperature | ~973 K | ±100 K |
| Heat exchanger steam output temperature | ~813 K | ±30 K |
| HEPA bank gas temperature | ~473 K | ±60 K |
| Catalyst bed temperature | ~573 K | ±50 K |
| Scrubber outlet temperature | ~328 K | ±25 K |
| Total thermal input (plasma + waste) | ~5.7 MW | ±1.5 MW |
| Net electrical output | ~400 kW | ±200 kW |
| Housing surface temperature | <333 K (60°C) | Must not exceed for personnel safety |
