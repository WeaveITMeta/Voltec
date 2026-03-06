# V-Core — EustressEngine Simulation Requirements

**Document Classification**: Voltec Internal — Simulation Specification  
**Version**: 1.0  
**Date**: March 6, 2026  
**Cross-References**: `PATENT.md`, `SOTA_VALIDATION.md`

---

## 1. Required Crate Features

| Feature Flag | Purpose | Required By |
|-------------|---------|-------------|
| `material_properties` | 14-field material property tables per component | All components |
| `thermodynamic_state` | Temperature, pressure, volume, internal energy, entropy, enthalpy, moles | All components |
| `electrochemical_state` | Voltage, capacity, SOC, current, resistance, cycle count | V-Cell Buffer |
| `structural_bundle` | Stress-strain, fracture monitoring, fatigue tracking | Reactor Vessel, Fuel Assembly, Heat Pipes |
| `custom_material` | Domain-specific extensions via `[material.custom]` HashMap | All components |

---

## 2. MaterialProperties — Per Component

### 2.1 316L Stainless Steel (Reactor Vessel)

```toml
[material]
name = "316L Stainless Steel"
young_modulus = 193000000000.0
poisson_ratio = 0.30
yield_strength = 170000000.0
ultimate_strength = 485000000.0
fracture_toughness = 112000000.0
hardness = 217.0
thermal_conductivity = 14.6
specific_heat = 500.0
thermal_expansion = 0.0000159
melting_point = 1673.0
density = 7990.0
friction_static = 0.40
friction_kinetic = 0.30
restitution = 0.4

[material.custom]
role = "reactor_vessel"
asme_code = "Section_III_Division_5"
pressure_boundary = true
fracture_critical = true
fatigue_monitored = true
```

### 2.2 U-ZrH₁.₆ (Fuel Assembly)

```toml
[material]
name = "U-ZrH1.6 (Uranium Zirconium Hydride)"
young_modulus = 130000000000.0
poisson_ratio = 0.32
yield_strength = 300000000.0
ultimate_strength = 450000000.0
fracture_toughness = 15000000.0
hardness = 250.0
thermal_conductivity = 18.0
specific_heat = 350.0
thermal_expansion = 0.000007
melting_point = 1023.0
density = 7300.0
friction_static = 0.40
friction_kinetic = 0.30
restitution = 0.3

[material.custom]
role = "nuclear_fuel"
enrichment_pct = 19.75
u235_mass_kg = 1.054
fuel_rods = 37
rod_diameter_mm = 37.5
active_length_mm = 380.0
burnup_target_mwd_thm = 30000.0
temp_coefficient_dk_per_c = -0.0001
max_operating_temp_k = 1023.0
h_dissociation_onset_k = 1073.0
```

### 2.3 Beryllium Oxide (Reflector Assembly)

```toml
[material]
name = "Beryllium Oxide (BeO)"
young_modulus = 345000000000.0
poisson_ratio = 0.26
yield_strength = 230000000.0
ultimate_strength = 250000000.0
fracture_toughness = 3000000.0
hardness = 1200.0
thermal_conductivity = 260.0
specific_heat = 1025.0
thermal_expansion = 0.0000085
melting_point = 2780.0
density = 3010.0
friction_static = 0.30
friction_kinetic = 0.20
restitution = 0.25

[material.custom]
role = "neutron_reflector"
neutron_moderating_ratio = 143.0
toxic_dust_hazard = true
```

### 2.4 Boron Carbide (Control Drum Absorber)

```toml
[material]
name = "Boron Carbide (B4C)"
young_modulus = 460000000000.0
poisson_ratio = 0.17
yield_strength = 2800000000.0
ultimate_strength = 350000000.0
fracture_toughness = 3500000.0
hardness = 3000.0
thermal_conductivity = 30.0
specific_heat = 950.0
thermal_expansion = 0.000005
melting_point = 2763.0
density = 2520.0
friction_static = 0.35
friction_kinetic = 0.25
restitution = 0.2

[material.custom]
role = "neutron_absorber"
b10_abundance_pct = 19.9
thermal_absorption_barns = 3840.0
drum_count = 6
drum_arc_deg = 120.0
total_reactivity_worth_dollars = 8.0
```

### 2.5 Inconel 718 (Heat Pipe Bundle + Hot-Side Heat Exchanger)

```toml
[material]
name = "Inconel 718"
young_modulus = 200000000000.0
poisson_ratio = 0.29
yield_strength = 1034000000.0
ultimate_strength = 1241000000.0
fracture_toughness = 95000000.0
hardness = 388.0
thermal_conductivity = 11.4
specific_heat = 435.0
thermal_expansion = 0.000013
melting_point = 1609.0
density = 8190.0
friction_static = 0.40
friction_kinetic = 0.30
restitution = 0.35

[material.custom]
role = "heat_pipe_envelope"
working_fluid = "sodium"
pipe_count = 12
pipe_od_mm = 15.9
heat_per_pipe_kw = 6.25
wick_type = "sintered_nickel"
wick_porosity = 0.60
```

### 2.6 Maraging 350 Steel (Stirling Engine Assembly)

```toml
[material]
name = "Maraging 350 Steel"
young_modulus = 190000000000.0
poisson_ratio = 0.30
yield_strength = 2400000000.0
ultimate_strength = 2450000000.0
fracture_toughness = 35000000.0
hardness = 600.0
thermal_conductivity = 25.0
specific_heat = 450.0
thermal_expansion = 0.0000101
melting_point = 1686.0
density = 8100.0
friction_static = 0.45
friction_kinetic = 0.35
restitution = 0.4

[material.custom]
role = "stirling_engine_housing"
engine_count = 2
working_gas = "helium"
mean_pressure_mpa = 6.0
hot_side_temp_k = 923.0
cold_side_temp_k = 333.0
electrical_output_kw = 12.5
efficiency_pct = 33.3
frequency_hz = 60.0
design_life_hr = 100000
```

### 2.7 Aluminum 6061-T6 (Cold-Side Radiator)

```toml
[material]
name = "Aluminum 6061-T6"
young_modulus = 68900000000.0
poisson_ratio = 0.33
yield_strength = 276000000.0
ultimate_strength = 310000000.0
fracture_toughness = 29000000.0
hardness = 107.0
thermal_conductivity = 167.0
specific_heat = 896.0
thermal_expansion = 0.0000236
melting_point = 855.0
density = 2700.0
friction_static = 0.35
friction_kinetic = 0.25
restitution = 0.4

[material.custom]
role = "cold_side_radiator"
heat_rejection_kw = 50.0
chp_water_loop = true
air_cooled_backup = true
fan_noise_db = 35.0
```

### 2.8 Lead (Biological Shield — Inner/Outer Layers)

```toml
[material]
name = "Lead (Pb)"
young_modulus = 16000000000.0
poisson_ratio = 0.44
yield_strength = 11000000.0
ultimate_strength = 17000000.0
fracture_toughness = 15000000.0
hardness = 5.0
thermal_conductivity = 35.0
specific_heat = 129.0
thermal_expansion = 0.000029
melting_point = 600.0
density = 11340.0
friction_static = 0.40
friction_kinetic = 0.30
restitution = 0.15

[material.custom]
role = "gamma_shield"
inner_thickness_mm = 50.0
outer_thickness_mm = 25.0
gamma_attenuation = true
```

### 2.9 Borated Polyethylene (Biological Shield — Middle Layer)

```toml
[material]
name = "Borated Polyethylene (5 wt% B4C)"
young_modulus = 800000000.0
poisson_ratio = 0.42
yield_strength = 25000000.0
ultimate_strength = 33000000.0
fracture_toughness = 2000000.0
hardness = 65.0
thermal_conductivity = 0.40
specific_heat = 1900.0
thermal_expansion = 0.00015
melting_point = 393.0
density = 1080.0
friction_static = 0.35
friction_kinetic = 0.25
restitution = 0.3

[material.custom]
role = "neutron_shield"
b4c_weight_pct = 5.0
thickness_mm = 75.0
max_operating_temp_k = 393.0
neutron_moderation = true
neutron_capture = true
```

### 2.10 304 Stainless Steel (Outer Casing)

```toml
[material]
name = "304 Stainless Steel"
young_modulus = 193000000000.0
poisson_ratio = 0.29
yield_strength = 215000000.0
ultimate_strength = 505000000.0
fracture_toughness = 100000000.0
hardness = 201.0
thermal_conductivity = 16.3
specific_heat = 500.0
thermal_expansion = 0.0000173
melting_point = 1673.0
density = 8000.0
friction_static = 0.40
friction_kinetic = 0.30
restitution = 0.4

[material.custom]
role = "outer_casing"
seismic_rating = "Zone_4"
flood_rated_m = 2.0
tamper_evident = true
```

### 2.11 Na-S Solid State (V-Cell Buffer)

```toml
[material]
name = "Na-S Solid State (V-Cell)"
young_modulus = 40000000000.0
poisson_ratio = 0.30
yield_strength = 100000000.0
ultimate_strength = 150000000.0
fracture_toughness = 5000000.0
hardness = 120.0
thermal_conductivity = 1.5
specific_heat = 800.0
thermal_expansion = 0.000012
melting_point = 570.0
density = 2800.0
friction_static = 0.35
friction_kinetic = 0.25
restitution = 0.3

[material.custom]
role = "energy_buffer"
module_count = 2
module_capacity_kwh = 8.33
total_capacity_kwh = 16.67
energy_density_wh_kg = 900.0
nominal_voltage_vdc = 600.0
```

### 2.12 Polycarbonate (Status Array)

```toml
[material]
name = "Polycarbonate"
young_modulus = 2400000000.0
poisson_ratio = 0.37
yield_strength = 62000000.0
ultimate_strength = 70000000.0
fracture_toughness = 3200000.0
hardness = 75.0
thermal_conductivity = 0.22
specific_heat = 1200.0
thermal_expansion = 0.000065
melting_point = 540.0
density = 1200.0
friction_static = 0.35
friction_kinetic = 0.25
restitution = 0.4

[material.custom]
role = "status_display"
led_count = 8
led_color_idle = "green"
led_color_warning = "amber"
led_color_fault = "red"
```

### 2.13 316L Stainless Steel (Control Module Enclosure)

Uses same base material as §2.1 with different `[material.custom]`:

```toml
[material.custom]
role = "control_module"
processor = "NVIDIA_Jetson_Orin"
ai_system = "V-Mind"
nrc_telemetry = true
ethernet = true
wifi = false
air_gapped_safety = true
```

### 2.14 SiC Power Electronics (Electrical Converter)

```toml
[material]
name = "Silicon Carbide (SiC) Power Module"
young_modulus = 410000000000.0
poisson_ratio = 0.14
yield_strength = 3440000000.0
ultimate_strength = 3500000000.0
fracture_toughness = 3400000.0
hardness = 2800.0
thermal_conductivity = 120.0
specific_heat = 690.0
thermal_expansion = 0.0000041
melting_point = 3100.0
density = 3210.0
friction_static = 0.30
friction_kinetic = 0.20
restitution = 0.25

[material.custom]
role = "electrical_converter"
input_voltage_vdc = 600.0
output_voltage_vac = 240.0
output_frequency_hz = 60.0
grid_tie = true
islanding = true
transfer_time_ms = 16.0
efficiency_pct = 97.0
```

---

## 3. Instance File Structure

### 3.1 File → Entity Mapping

| Instance File | Mesh Reference | class_name | Realism Sections |
|--------------|---------------|------------|-----------------|
| `VCore_ReactorVessel.glb.toml` | `meshes/VCore_ReactorVessel.glb` | Part | material, thermodynamic |
| `VCore_FuelAssembly.glb.toml` | `meshes/VCore_FuelAssembly.glb` | Part | material, thermodynamic |
| `VCore_ReflectorAssembly.glb.toml` | `meshes/VCore_ReflectorAssembly.glb` | Part | material, thermodynamic |
| `VCore_ControlDrums.glb.toml` | `meshes/VCore_ControlDrums.glb` | Part | material, thermodynamic |
| `VCore_HeatPipeBundle.glb.toml` | `meshes/VCore_HeatPipeBundle.glb` | Part | material, thermodynamic |
| `VCore_StirlingEngines.glb.toml` | `meshes/VCore_StirlingEngines.glb` | Part | material, thermodynamic |
| `VCore_HotSideHX.glb.toml` | `meshes/VCore_HotSideHX.glb` | Part | material, thermodynamic |
| `VCore_ColdRadiator.glb.toml` | `meshes/VCore_ColdRadiator.glb` | Part | material, thermodynamic |
| `VCore_BioShield.glb.toml` | `meshes/VCore_BioShield.glb` | Part | material, thermodynamic |
| `VCore_OuterCasing.glb.toml` | `meshes/VCore_OuterCasing.glb` | Part | material, thermodynamic |
| `VCore_VCellBuffer.glb.toml` | `meshes/VCore_VCellBuffer.glb` | Part | material, thermodynamic, electrochemical |
| `VCore_ControlModule.glb.toml` | `meshes/VCore_ControlModule.glb` | Part | material |
| `VCore_ElectricalConverter.glb.toml` | `meshes/VCore_ElectricalConverter.glb` | Part | material |
| `VCore_StatusArray.glb.toml` | `meshes/VCore_StatusArray.glb` | Part | material |

### 3.2 Standard .glb.toml Section Template

```toml
# V-Core {ComponentName} — {MaterialName}
# {Brief description}

[asset]
mesh = "meshes/VCore_{ComponentName}.glb"

[transform]
position = [0.0, 0.0, 0.0]
rotation = [0.0, 0.0, 0.0, 1.0]
scale = [1.0, 1.0, 1.0]

[properties]
name = "VCore_{ComponentName}"
class_name = "Part"
color = [r, g, b, a]
transparency = 0.0
cast_shadow = true
can_collide = true
anchored = true

[metadata]
class_name = "Part"
archivable = true
created = "2026-03-06T00:00:00Z"
last_modified = "2026-03-06T00:00:00Z"

[material]
# ... 14 base fields from §2 ...

[material.custom]
# ... domain-specific extensions ...

[thermodynamic]
temperature = 298.15
pressure = 101325.0
volume = 0.0
internal_energy = 0.0
entropy = 0.0
enthalpy = 0.0
moles = 0.0
```

### 3.3 Transform Layout (Assembly Positions)

All positions are baked into GLB meshes via `assemble_all.py`. TOML `[transform].position` is `[0.0, 0.0, 0.0]` for all components.

| Component | Assembly Position (Y-up, meters) | Notes |
|-----------|----------------------------------|-------|
| Outer Casing | [0.0, 0.0, 0.0] | Origin — egg-shaped enclosure |
| Biological Shield | [0.0, 0.05, 0.0] | Inside casing, centered vertically |
| Reactor Vessel | [0.0, 0.05, 0.0] | Inside shield, centered |
| Fuel Assembly | [0.0, 0.05, 0.0] | Center of vessel |
| Reflector Assembly | [0.0, 0.05, 0.0] | Annulus around fuel |
| Control Drums | [0.0, 0.05, 0.0] | Inside reflector annulus |
| Heat Pipe Bundle | [0.0, 0.15, 0.0] | Through fuel, extending up |
| Hot-Side HX | [0.0, 0.25, 0.0] | Above vessel, heat pipe condenser |
| Stirling Engines | [0.0, 0.30, 0.0] | Above hot-side HX |
| Cold-Side Radiator | [0.0, -0.25, 0.0] | Below vessel, bottom of egg |
| V-Cell Buffer | [0.0, -0.20, 0.0] | Below vessel, above radiator |
| Control Module | [0.0, 0.35, 0.0] | Top section |
| Electrical Converter | [0.15, 0.30, 0.0] | Adjacent to Stirling engines |
| Status Array | [0.0, 0.40, 0.0] | Top of egg |

---

## 4. Domain-Specific State: NuclearState

V-Core's fuel assembly requires a custom `NuclearState` tracked via `[material.custom]` fields (EustressEngine does not yet have a native NuclearState component — these fields enable future implementation).

### 4.1 NuclearState Fields

| Field | Type | Unit | Initial Value | Description |
|-------|------|------|---------------|-------------|
| `thermal_power_w` | f64 | W | 75000.0 | Fission thermal power output |
| `neutron_flux` | f64 | n/(cm²·s) | 1.0 × 10¹² | Average thermal neutron flux |
| `burnup_mwd_thm` | f64 | MWd/tHM | 0.0 | Cumulative fuel burnup |
| `control_drum_angle_deg` | f64 | ° | 90.0 | Average drum rotation (0=full absorb, 180=full reflect) |
| `fuel_temp_k` | f64 | K | 923.0 | Fuel centerline temperature |
| `coolant_temp_k` | f64 | K | 873.0 | Heat pipe vapor temperature |
| `reactivity_dk` | f64 | Δk/k | 0.0 | Excess reactivity |
| `keff` | f64 | — | 1.0000 | Effective multiplication factor |
| `shutdown_margin_dollars` | f64 | $ | 2.0 | Margin to criticality with strongest drum stuck |

### 4.2 Runtime Update Flow (Pseudocode)

```
fn nuclear_tick(fuel: &mut FuelAssembly, drums: &ControlDrums, dt: f64) {
    // 1. Calculate reactivity from drum position
    let drum_reactivity = drums.reactivity_curve(drums.angle_deg);

    // 2. Apply temperature coefficient feedback
    let temp_feedback = fuel.temp_coefficient * (fuel.fuel_temp_k - 923.0);

    // 3. Net reactivity
    fuel.reactivity_dk = drum_reactivity + temp_feedback;

    // 4. Point kinetics: power change
    let power_change = fuel.thermal_power_w * fuel.reactivity_dk / NEUTRON_LIFETIME;
    fuel.thermal_power_w += power_change * dt;
    fuel.thermal_power_w = fuel.thermal_power_w.clamp(0.0, 100000.0);

    // 5. Update fuel temperature from power balance
    let heat_removed = heat_pipes.transport_rate(fuel.coolant_temp_k);
    let net_heat = fuel.thermal_power_w - heat_removed;
    fuel.fuel_temp_k += net_heat * dt / (fuel.mass_kg * fuel.specific_heat);

    // 6. Burnup accumulation
    fuel.burnup_mwd_thm += fuel.thermal_power_w * dt / (86400.0 * fuel.heavy_metal_mass_t * 1e6);

    // 7. Update keff
    fuel.keff = 1.0 + fuel.reactivity_dk;
}
```

---

## 5. ThermodynamicState

### 5.1 Fields

| Field | Type | Unit | Description |
|-------|------|------|-------------|
| `temperature` | f64 | K | Component bulk temperature |
| `pressure` | f64 | Pa | Internal pressure (vessel: helium cover gas) |
| `volume` | f64 | m³ | Component volume |
| `internal_energy` | f64 | J | Thermal energy content |
| `entropy` | f64 | J/K | Thermodynamic entropy |
| `enthalpy` | f64 | J | Enthalpy (H = U + PV) |
| `moles` | f64 | mol | Molar quantity of primary material |

### 5.2 Operating Envelope

| Component | T_normal (K) | T_min (K) | T_max (K) | P_normal (Pa) | Notes |
|-----------|-------------|-----------|-----------|---------------|-------|
| Fuel Assembly | 923 | 600 | 1023 | 101325 | Fuel centerline |
| Heat Pipe Bundle | 873 | 550 | 973 | ~100000 | Na vapor pressure at operating temp |
| Hot-Side HX | 923 | 500 | 973 | 101325 | Stirling interface |
| Stirling Engines | 628 | 333 | 923 | 6000000 | Average of hot/cold sides; He at 6 MPa |
| Cold-Side Radiator | 333 | 278 | 373 | 101325 | Water loop or air cooling |
| Reactor Vessel | 773 | 400 | 973 | 200000 | Helium cover gas |
| Biological Shield | 373 | 273 | 393 | 101325 | PE limit: 120°C |
| Outer Casing | 313 | 278 | 333 | 101325 | Touched by occupants |
| V-Cell Buffer | 298 | 253 | 333 | 101325 | Ambient-temperature Na-S cells |

---

## 6. ElectrochemicalState (V-Cell Buffer Only)

### 6.1 Fields

| Field | Type | Unit | Initial Value |
|-------|------|------|---------------|
| `voltage` | f64 | V | 600.0 |
| `terminal_voltage` | f64 | V | 600.0 |
| `capacity_ah` | f64 | Ah | 27.8 |
| `soc` | f64 | — | 1.0 |
| `current` | f64 | A | 0.0 |
| `internal_resistance` | f64 | Ω | 0.015 |
| `ionic_conductivity` | f64 | S/m | 0.01 |
| `cycle_count` | u32 | — | 0 |
| `c_rate` | f64 | — | 0.0 |
| `capacity_retention` | f64 | — | 1.0 |
| `heat_generation` | f64 | W | 0.0 |
| `dendrite_risk` | f64 | — | 0.0 |

---

## 7. Thermal Transport Laws

### 7.1 Heat Pipe Transport Model

```
fn heat_pipe_transport(t_evap: f64, t_cond: f64, pipe_count: usize) -> f64 {
    // Simplified sodium heat pipe conductance model
    // Real implementation would use Dunn & Reay correlations
    let conductance_per_pipe = 500.0; // W/K (effective, includes wick + vapor)
    let dt = t_evap - t_cond;
    (pipe_count as f64) * conductance_per_pipe * dt
}
```

### 7.2 Stirling Engine Model

```
fn stirling_power(t_hot: f64, t_cold: f64, efficiency_fraction: f64, q_in: f64) -> f64 {
    let carnot_efficiency = 1.0 - (t_cold / t_hot);
    let actual_efficiency = efficiency_fraction * carnot_efficiency;
    q_in * actual_efficiency.min(efficiency_fraction)
}
```

### 7.3 Shield Temperature Model

```
fn shield_temperature(q_gamma: f64, t_ambient: f64, shield_conductivity: f64, thickness: f64, area: f64) -> f64 {
    // Steady-state conduction through composite shield
    let r_thermal = thickness / (shield_conductivity * area);
    t_ambient + q_gamma * r_thermal
}
```

---

## 8. Realism Config

```toml
[realism]
enable_material = true
enable_thermodynamic = true
enable_electrochemical = true
enable_structural = true
tick_rate_hz = 10.0
temperature_model = "conduction_convection"
nuclear_model = "point_kinetics"

[realism.nuclear]
neutron_lifetime_s = 0.0001
delayed_neutron_fraction = 0.0065
temp_coefficient_dk_per_k = -0.0001
max_thermal_power_w = 100000.0
```

---

## 9. Structural Bundle Requirements

| Component | Priority | Fracture Critical | Fatigue Monitored | Strain Gauges |
|-----------|----------|-------------------|-------------------|---------------|
| Reactor Vessel | **Critical** | Yes | Yes | 8 |
| Fuel Assembly | **Critical** | Yes | Yes | 0 (sealed) |
| Heat Pipe Bundle | **High** | Yes | Yes | 4 |
| Hot-Side HX | **High** | Yes | Yes | 4 |
| Stirling Engines | **High** | No | Yes | 4 |
| Biological Shield | **Medium** | No | No | 0 |
| Outer Casing | **Medium** | No | Yes | 4 |
| Cold-Side Radiator | **Low** | No | No | 0 |
| V-Cell Buffer | **Low** | No | No | 0 |
| Control Drums | **Medium** | No | Yes | 0 |
| Reflector Assembly | **Medium** | Yes (BeO brittle) | No | 0 |
| Control Module | **Low** | No | No | 0 |
| Electrical Converter | **Low** | No | No | 0 |
| Status Array | **Low** | No | No | 0 |

---

## 10. Deployment Checklist

### 10.1 Copy Instructions

```powershell
# Copy GLB meshes to EustressEngine asset path
$src = "E:\Workspace\Voltec\docs\Products\V-Core\V1\meshes"
$dst = "C:\Users\miksu\Documents\Eustress\Universe1\spaces\Space1\assets\meshes\products\V-Core"
New-Item -ItemType Directory -Path $dst -Force
Copy-Item "$src\*.glb" $dst

# Copy TOML instance files to Workspace
$tomlSrc = "E:\Workspace\Voltec\docs\Products\V-Core\V1"
$tomlDst = "C:\Users\miksu\Documents\Eustress\Universe1\spaces\Space1\Workspace"
Copy-Item "$tomlSrc\*.glb.toml" $tomlDst
```

### 10.2 Pre-Launch Checks

- [ ] All 14 `.glb.toml` files present in Workspace
- [ ] All 14 `.glb` meshes present in `assets/meshes/products/V-Core/`
- [ ] Every `[asset] mesh` path resolves to an existing `.glb` file
- [ ] Every `[material]` section has exactly 14 base fields
- [ ] Every `[material.custom]` has a `role` tag
- [ ] V-Cell Buffer has `[electrochemical]` section
- [ ] All temperatures in Kelvin, pressures in Pascal, lengths in meters

### 10.3 Runtime Sanity Checks

| Check | Expected Value | Tolerance |
|-------|---------------|-----------|
| Fuel Assembly `[thermodynamic].temperature` | 923.0 K | ±100 K |
| Heat Pipe Bundle `[thermodynamic].temperature` | 873.0 K | ±100 K |
| V-Cell Buffer `[electrochemical].voltage` | 600.0 V | ±50 V |
| V-Cell Buffer `[electrochemical].soc` | 0.0–1.0 | Must not exceed bounds |
| Outer Casing `[thermodynamic].temperature` | 313.0 K | ±20 K |
| Biological Shield `[thermodynamic].temperature` | <393.0 K | Must not exceed PE limit |
