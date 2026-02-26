# VOLTEC V-PUMP — EustressEngine Simulation Requirements

**Document Classification**: Voltec Internal — Simulation Specification  
**Version**: 1.0  
**Date**: February 25, 2026  
**Cross-Reference**: `PATENT.md`, `SOTA_VALIDATION.md`  

---

## 1. Required Crate Features

| Feature Flag | Crate | Purpose |
|-------------|-------|---------|
| `realism` | `eustress_common` | MaterialProperties, ThermodynamicState |
| `fluid_dynamics` | `eustress_common` | FluidState, pressure/flow simulation |
| `kinematics` | `eustress_common` | KineticState for rotating assemblies |
| `structural` | `eustress_common` | Stress/strain on pressure casing |

### External Dependency

| Crate | Version | Purpose |
|-------|---------|---------|
| `garbongus` | ≥0.2.1 | Fluid properties, Darcy-Weisbach, vacuum lift, pipeline hydraulics, pump power |

---

## 2. MaterialProperties — Per Component

### 2.1 Pump Casing — UNS S32205 Duplex Stainless Steel

```toml
[material]
name = "UNS S32205 Duplex Stainless Steel"
young_modulus = 200000000000.0
poisson_ratio = 0.30
yield_strength = 450000000.0
ultimate_strength = 620000000.0
fracture_toughness = 200000000.0
hardness = 290.0
thermal_conductivity = 19.0
specific_heat = 500.0
thermal_expansion = 0.000013
melting_point = 1673.0
density = 7800.0
friction_static = 0.45
friction_kinetic = 0.35
restitution = 0.3

[material.custom]
pren = 35.0
chloride_scc_threshold_c = 250.0
design_life_years = 1000.0
role = "pressure_casing"
```

### 2.2 Bore Liner — Reaction-Bonded Silicon Carbide (RBSiC)

```toml
[material]
name = "RBSiC Bore Liner"
young_modulus = 380000000000.0
poisson_ratio = 0.17
yield_strength = 400000000.0
ultimate_strength = 3000000000.0
fracture_toughness = 4000000.0
hardness = 2800.0
thermal_conductivity = 120.0
specific_heat = 680.0
thermal_expansion = 0.000004
melting_point = 2730.0
density = 3100.0
friction_static = 0.20
friction_kinetic = 0.15
restitution = 0.5

[material.custom]
erosion_rate_mm_per_year = 0.001
max_water_velocity_m_s = 5.0
design_life_years = 1000.0
role = "bore_liner"
```

### 2.3 Impeller Assembly — Super Duplex UNS S32750

```toml
[material]
name = "UNS S32750 Super Duplex Stainless Steel"
young_modulus = 200000000000.0
poisson_ratio = 0.30
yield_strength = 550000000.0
ultimate_strength = 800000000.0
fracture_toughness = 150000000.0
hardness = 310.0
thermal_conductivity = 17.0
specific_heat = 480.0
thermal_expansion = 0.000013
melting_point = 1623.0
density = 7800.0
friction_static = 0.45
friction_kinetic = 0.35
restitution = 0.3

[material.custom]
pren = 40.0
fatigue_limit_pa = 280000000.0
shot_peen_residual_stress_pa = -400000000.0
stages = 3
blades_per_stage = 7
guide_vanes_per_stage = 11
role = "impeller"
```

### 2.4 Drive Shaft — 17-4 PH Stainless Steel (H900)

```toml
[material]
name = "17-4 PH SS H900"
young_modulus = 196000000000.0
poisson_ratio = 0.27
yield_strength = 1170000000.0
ultimate_strength = 1310000000.0
fracture_toughness = 80000000.0
hardness = 420.0
thermal_conductivity = 18.0
specific_heat = 460.0
thermal_expansion = 0.0000108
melting_point = 1723.0
density = 7780.0
friction_static = 0.42
friction_kinetic = 0.33
restitution = 0.3

[material.custom]
fatigue_cycles_target = 7.62e11
rpm_rated = 1450.0
role = "drive_shaft"
```

### 2.5 Bearing Cartridges — SiC/SiC Ceramic Journal

```toml
[material]
name = "SiC/SiC Ceramic Journal Bearing"
young_modulus = 410000000000.0
poisson_ratio = 0.14
yield_strength = 550000000.0
ultimate_strength = 3900000000.0
fracture_toughness = 4500000.0
hardness = 2800.0
thermal_conductivity = 120.0
specific_heat = 680.0
thermal_expansion = 0.000004
melting_point = 2730.0
density = 3210.0
friction_static = 0.05
friction_kinetic = 0.03
restitution = 0.5

[material.custom]
lubrication = "process_water"
pv_limit_mpa_m_s = 100.0
wear_rate_mm3_per_nm = 1.0e-8
replacement_interval_years = 75.0
role = "bearing"
```

### 2.6 Vacuum-Assist Module — 316L Stainless Steel

```toml
[material]
name = "316L Stainless Steel"
young_modulus = 193000000000.0
poisson_ratio = 0.30
yield_strength = 170000000.0
ultimate_strength = 485000000.0
fracture_toughness = 100000000.0
hardness = 217.0
thermal_conductivity = 16.3
specific_heat = 500.0
thermal_expansion = 0.0000159
melting_point = 1673.0
density = 7990.0
friction_static = 0.45
friction_kinetic = 0.35
restitution = 0.3

[material.custom]
ultimate_vacuum_pa = 2000.0
pumping_speed_m3_h = 40.0
motor_power_kw = 2.2
role = "vacuum_module"
```

### 2.7 Flange Adapters — A694 F60 Duplex Forging

```toml
[material]
name = "A694 F60 Duplex Forging"
young_modulus = 200000000000.0
poisson_ratio = 0.30
yield_strength = 450000000.0
ultimate_strength = 620000000.0
fracture_toughness = 120000000.0
hardness = 260.0
thermal_conductivity = 17.0
specific_heat = 480.0
thermal_expansion = 0.000013
melting_point = 1623.0
density = 7800.0
friction_static = 0.45
friction_kinetic = 0.35
restitution = 0.3

[material.custom]
bolt_pattern = "ASME_B16_47_Series_B"
gasket_type = "spiral_wound_316L_graphite"
role = "flange_adapter"
```

### 2.8 Bypass Valve — Duplex Steel + Stellite 6

```toml
[material]
name = "Duplex Steel + Stellite 6 Seats"
young_modulus = 200000000000.0
poisson_ratio = 0.30
yield_strength = 450000000.0
ultimate_strength = 620000000.0
fracture_toughness = 150000000.0
hardness = 290.0
thermal_conductivity = 19.0
specific_heat = 500.0
thermal_expansion = 0.000013
melting_point = 1673.0
density = 7800.0
friction_static = 0.40
friction_kinetic = 0.30
restitution = 0.3

[material.custom]
valve_type = "butterfly"
seat_material = "Stellite_6"
seat_hardness_hv = 450.0
actuation = "spring_return_hydraulic"
role = "bypass_valve"
```

### 2.9 Motor — PMSM (Permanent Magnet Synchronous)

```toml
[material]
name = "PMSM Motor Assembly"
young_modulus = 200000000000.0
poisson_ratio = 0.30
yield_strength = 250000000.0
ultimate_strength = 400000000.0
fracture_toughness = 80000000.0
hardness = 200.0
thermal_conductivity = 25.0
specific_heat = 450.0
thermal_expansion = 0.000012
melting_point = 1600.0
density = 7500.0
friction_static = 0.40
friction_kinetic = 0.30
restitution = 0.3

[material.custom]
motor_type = "PMSM"
ip_rating = "IP68"
efficiency_percent = 96.0
vfd_speed_range_percent = "30-100"
cooling = "process_water_jacket"
role = "motor"
```

### 2.10 Control Module — 316L SS Enclosure

```toml
[material]
name = "316L Stainless Steel Enclosure"
young_modulus = 193000000000.0
poisson_ratio = 0.30
yield_strength = 170000000.0
ultimate_strength = 485000000.0
fracture_toughness = 100000000.0
hardness = 217.0
thermal_conductivity = 16.3
specific_heat = 500.0
thermal_expansion = 0.0000159
melting_point = 1673.0
density = 7990.0
friction_static = 0.45
friction_kinetic = 0.35
restitution = 0.3

[material.custom]
nema_rating = "4X"
ip_rating = "IP68"
processor = "ARM_Cortex_A72"
os = "V-OS"
communication = "fiber_optic_4G_5G"
role = "control_module"
```

### 2.11 Status Array — IP68 LED Panel

```toml
[material]
name = "Polycarbonate LED Panel"
young_modulus = 2400000000.0
poisson_ratio = 0.37
yield_strength = 62000000.0
ultimate_strength = 70000000.0
fracture_toughness = 3200000.0
hardness = 75.0
thermal_conductivity = 0.22
specific_heat = 1200.0
thermal_expansion = 0.000066
melting_point = 540.0
density = 1200.0
friction_static = 0.35
friction_kinetic = 0.28
restitution = 0.4

[material.custom]
ip_rating = "IP68"
led_count = 5
led_colors = "green_amber_red_blue_white"
role = "status_array"
```

---

## 3. Instance File Structure

### 3.1 File → Entity Mapping

| File | Entity | class_name |
|------|--------|------------|
| `VPump_PumpCasing.glb.toml` | Pressure casing (structural backbone) | AdvancedPart |
| `VPump_BoreLiner.glb.toml` | RBSiC internal wear surface | AdvancedPart |
| `VPump_ImpellerAssembly.glb.toml` | 3-stage axial-flow rotor + guide vanes | AdvancedPart |
| `VPump_DriveShaft.glb.toml` | Torque transmission shaft | AdvancedPart |
| `VPump_BearingCartridge.glb.toml` | SiC/SiC journal bearings (×2) | AdvancedPart |
| `VPump_VacuumModule.glb.toml` | Rotary vane vacuum-assist priming | Part |
| `VPump_FlangeAdapter.glb.toml` | Modular inlet/outlet reducer rings | Part |
| `VPump_BypassValve.glb.toml` | Automatic butterfly bypass | Part |
| `VPump_Motor.glb.toml` | PMSM direct-drive motor | AdvancedPart |
| `VPump_ControlModule.glb.toml` | V-Mind AI + PLC enclosure | Part |
| `VPump_StatusArray.glb.toml` | IP68 LED indicator panel | Part |

### 3.2 Transform Layout (VP-M Frame — DN1200)

All positions in meters, Y-up coordinate system. Origin at pump casing center.

| Component | Position [x, y, z] | Scale [x, y, z] | Rotation [x, y, z, w] |
|-----------|--------------------|-----------------|-----------------------|
| PumpCasing | [0.0, 0.0, 0.0] | [2.5, 2.5, 4.5] | [0.0, 0.0, 0.0, 1.0] |
| BoreLiner | [0.0, 0.0, 0.0] | [1.2, 1.2, 4.0] | [0.0, 0.0, 0.0, 1.0] |
| ImpellerAssembly | [0.0, 0.0, 0.0] | [1.0, 1.0, 3.0] | [0.0, 0.0, 0.0, 1.0] |
| DriveShaft | [0.0, 0.0, 0.0] | [0.15, 0.15, 4.5] | [0.0, 0.0, 0.0, 1.0] |
| BearingCartridge | [0.0, 0.0, -1.8] | [0.4, 0.4, 0.3] | [0.0, 0.0, 0.0, 1.0] |
| VacuumModule | [1.2, -0.8, 0.0] | [0.5, 0.5, 0.6] | [0.0, 0.0, 0.0, 1.0] |
| FlangeAdapter (inlet) | [0.0, 0.0, -2.5] | [2.8, 2.8, 0.5] | [0.0, 0.0, 0.0, 1.0] |
| FlangeAdapter (outlet) | [0.0, 0.0, 2.5] | [2.8, 2.8, 0.5] | [0.0, 0.0, 0.0, 1.0] |
| BypassValve | [0.0, 1.8, 0.0] | [2.0, 0.5, 3.0] | [0.0, 0.0, 0.0, 1.0] |
| Motor | [0.0, -1.5, 0.0] | [1.0, 1.0, 1.5] | [0.0, 0.0, 0.0, 1.0] |
| ControlModule | [1.5, 0.0, 0.0] | [0.6, 0.8, 0.4] | [0.0, 0.0, 0.0, 1.0] |
| StatusArray | [1.5, 0.5, 0.0] | [0.3, 0.15, 0.08] | [0.0, 0.0, 0.0, 1.0] |

---

## 4. Domain-Specific State — FluidState

### 4.1 Fields

| Field | Type | Unit | Initial Value | Description |
|-------|------|------|---------------|-------------|
| `flow_rate_m3s` | f64 | m³/s | 0.0 | Volume flow through pump |
| `discharge_pressure_pa` | f64 | Pa | 101325.0 | Outlet pressure |
| `suction_pressure_pa` | f64 | Pa | 101325.0 | Inlet pressure |
| `differential_pressure_pa` | f64 | Pa | 0.0 | Discharge - Suction |
| `velocity_m_s` | f64 | m/s | 0.0 | Mean flow velocity |
| `reynolds_number` | f64 | — | 0.0 | Flow regime indicator |
| `friction_loss_pa` | f64 | Pa | 0.0 | Pipe friction loss in relay segment |
| `npsh_available_m` | f64 | m | 10.18 | Net positive suction head available |
| `npsh_required_m` | f64 | m | 3.5 | Minimum NPSH to avoid cavitation |
| `cavitation_margin_m` | f64 | m | 6.68 | NPSH_a - NPSH_r |
| `water_density_kg_m3` | f64 | kg/m³ | 998.2 | From garbongus::fluid::Fluid |
| `water_viscosity_pa_s` | f64 | Pa·s | 0.001002 | From garbongus::fluid::Fluid |
| `water_temperature_c` | f64 | °C | 20.0 | Process water temperature |

### 4.2 Runtime Update Flow

```
fn tick_fluid_state(pump: &mut VPump, dt: f64) {
    // 1. Read sensors
    let p_suction = pump.sensor_suction_pressure();
    let p_discharge = pump.sensor_discharge_pressure();
    let q = pump.sensor_flow_rate();
    let t_water = pump.sensor_water_temperature();

    // 2. Update fluid properties via garbongus
    let fluid = garbongus::fluid::Fluid::water(t_water);
    pump.state.water_density_kg_m3 = fluid.density_kg_m3;
    pump.state.water_viscosity_pa_s = fluid.dynamic_viscosity_pa_s;

    // 3. Update flow state
    pump.state.flow_rate_m3s = q;
    pump.state.suction_pressure_pa = p_suction;
    pump.state.discharge_pressure_pa = p_discharge;
    pump.state.differential_pressure_pa = p_discharge - p_suction;
    pump.state.velocity_m_s = q / garbongus::flow::pipe_area(pump.bore_diameter_m);

    // 4. Calculate Reynolds number
    let re = fluid.density_kg_m3 * pump.state.velocity_m_s * pump.bore_diameter_m
             / fluid.dynamic_viscosity_pa_s;
    pump.state.reynolds_number = re;

    // 5. Calculate NPSH available
    let vac_result = garbongus::vacuum::VacuumLift::new(
        fluid, pump.bore_diameter_m / 2.0, pump.suction_elevation_m
    ).flow_velocity(pump.state.velocity_m_s)
     .roughness(1.5e-6)
     .calculate();
    pump.state.npsh_available_m = vac_result.atmospheric_max_lift_m
        + pump.vacuum_assist_pressure_pa / (fluid.density_kg_m3 * 9.80665);
    pump.state.cavitation_margin_m = pump.state.npsh_available_m - pump.state.npsh_required_m;

    // 6. Cavitation protection
    if pump.state.cavitation_margin_m < 1.0 {
        pump.reduce_speed(0.95);  // VFD speed reduction
    }
}
```

---

## 5. ThermodynamicState

### 5.1 Fields

| Field | Type | Unit | Initial Value | Description |
|-------|------|------|---------------|-------------|
| `temperature` | f64 | K | 298.15 | Pump casing temperature |
| `pressure` | f64 | Pa | 2500000.0 | Internal operating pressure (25 bar) |
| `volume` | f64 | m³ | 5.0 | Internal wetted volume (VP-M) |
| `internal_energy` | f64 | J | 0.0 | Thermal energy in casing |
| `entropy` | f64 | J/K | 0.0 | Thermodynamic entropy |
| `enthalpy` | f64 | J | 0.0 | Flow enthalpy |
| `moles` | f64 | mol | 277500.0 | Water moles in pump volume |

### 5.2 Operating Envelope

| Parameter | Min | Nominal | Max | Unit |
|-----------|-----|---------|-----|------|
| Water temperature | 274.15 | 298.15 | 313.15 | K |
| Operating pressure | 0 | 2,500,000 | 4,000,000 | Pa |
| Flow velocity | 0 | 3.0 | 5.0 | m/s |
| Motor winding temp | 293.15 | 343.15 | 393.15 | K |
| Bearing temp | 293.15 | 308.15 | 343.15 | K |

---

## 6. Domain Laws — Fluid Dynamics

### 6.1 Function Reference

| Function | Source | Formula |
|----------|--------|---------|
| `darcy_weisbach` | `garbongus::pipe::DarcyWeisbach` | ΔP = f·(L/D)·(ρv²/2) |
| `colebrook_white` | `garbongus::pipe::DarcyWeisbach` | 1/√f = -2·log₁₀(ε/(3.7D) + 2.51/(Re·√f)) |
| `pump_power` | `garbongus::flow::pump_power` | P = ρ·g·Q·H / η |
| `vacuum_lift` | `garbongus::vacuum::VacuumLift` | h = (P_atm - P_vapor) / (ρ·g) |
| `required_diameter` | `garbongus::flow::required_diameter` | D = 2·√(Q/(v·π)) |
| `bernoulli` | `garbongus::flow::bernoulli_pressure` | P₁+½ρv₁²+ρgh₁ = P₂+½ρv₂²+ρgh₂ |
| `manning` | `garbongus::manning::ManningFlow` | Q = (1/n)·A·R^(2/3)·S^(1/2) |
| `pipeline` | `garbongus::pipeline::Pipeline` | Multi-segment elevation + friction |

### 6.2 Calibrated Constants

| Constant | Value | Unit | Source |
|----------|-------|------|--------|
| g | 9.80665 | m/s² | `garbongus::fluid::G` |
| P_atm | 101,325 | Pa | `garbongus::fluid::P_ATM` |
| Pipe roughness (steel) | 1.5 × 10⁻⁶ | m | Commercial steel, Moody chart |
| Pipe roughness (concrete) | 1.5 × 10⁻³ | m | Manning n=0.012 equivalent |
| Pump efficiency (BEP) | 0.88-0.91 | — | V-Pump rated performance |
| Motor efficiency | 0.96 | — | PMSM rated |
| VFD efficiency | 0.97 | — | ABB ACS880 class |

---

## 7. Realism Config

```toml
[realism]
enabled = true
tick_rate_hz = 60.0
time_scale = 1.0

[realism.fluid_dynamics]
enabled = true
library = "garbongus"
version = ">=0.2.1"

[realism.thermodynamics]
enabled = true
ambient_temperature_k = 298.15
ambient_pressure_pa = 101325.0

[realism.structural]
enabled = true
seismic_check = true
fatigue_tracking = true
```

---

## 8. Structural Bundle Requirements

| Component | Priority | Fracture-Critical | Notes |
|-----------|----------|-------------------|-------|
| Pump Casing | P0 | YES | Primary pressure boundary, 1000-year life |
| Bore Liner | P0 | NO | Wear surface, shrink-fit retained by casing |
| Impeller Assembly | P0 | YES | Rotating, fatigue-loaded, field-replaceable |
| Drive Shaft | P0 | YES | Torque + bending, 10¹¹ cycles target |
| Bearing Cartridges | P1 | NO | Field-replaceable, 50-100 year interval |
| Flange Adapters | P0 | YES | Pressure boundary, bolted connection |
| Bypass Valve | P1 | NO | Safety-critical but fail-safe (spring-return) |
| Motor | P1 | NO | Field-replaceable |
| Vacuum Module | P2 | NO | Auxiliary, not pressure boundary |
| Control Module | P2 | NO | Electronics, replaceable |
| Status Array | P3 | NO | Visual indicator only |

---

## 9. Deployment Checklist

### 9.1 File Copy

```
Source: docs/Products/V-Pump/V1/meshes/*.glb
Target: V1/meshes/ (stays in Voltec locally)

Source: docs/Products/V-Pump/V1/*.glb.toml
Target: V1/ (stays in Voltec locally)
```

### 9.2 Pre-Launch Checks

| Check | Command/Method | Expected |
|-------|----------------|----------|
| All .glb files exist | `ls V1/meshes/*.glb` | 11 files |
| All .glb.toml files exist | `ls V1/*.glb.toml` | 11 files |
| Mesh references valid | grep `mesh =` in each .toml | Path matches actual .glb filename |
| class_name correct | grep `class_name` | "AdvancedPart" or "Part" per §3.1 |
| Positions in meters | grep `position` | All values in reasonable meter range |
| Colors in linear RGBA | grep `color` | All values 0.0-1.0 |
| SI units in material | grep `young_modulus` | Values in Pa (10⁹ range for metals) |
| Timestamps ISO 8601 | grep `created` | Format: YYYY-MM-DDTHH:MM:SSZ |

### 9.3 Runtime Sanity Checks

| Assertion | Expected Value | Tolerance |
|-----------|---------------|-----------|
| `pump.state.flow_rate_m3s > 0` at steady state | 15.0 m³/s (VP-M) | ±20% |
| `pump.state.cavitation_margin_m > 0` | 6.68 m | Must be positive |
| `pump.state.reynolds_number > 4000` | ~4.8×10⁷ | Must be turbulent |
| `pump.state.differential_pressure_pa` | ~2,500,000 Pa | ±10% |
| `pump.casing.temperature < 350 K` | ~300 K | Must be below SCC threshold |
| `pump.bearing.temperature < 343 K` | ~308 K | Below max service |
| `garbongus::flow::pump_power(998, 15, 100, 0.88).shaft_kw()` | ~16,700 kW | ±5% |
