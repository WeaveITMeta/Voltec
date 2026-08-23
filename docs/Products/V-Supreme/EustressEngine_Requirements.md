# EustressEngine Requirements — V-Supreme: Fusion-Powered Full-Body Mecha Platform

## 1. Required Crate Features

| Feature Flag | Crate | Purpose |
|-------------|-------|---------|
| `realism` | `common` | Enable MaterialProperties, ThermodynamicState components |
| `electrochemistry` | `common` | Enable ElectrochemicalState for Reactor + V-Cell Array |
| `structural` | `common` | Enable StructuralBundle (fracture, fatigue tracking) |
| `kinematic` | `common` | Enable KineticState for 42-DOF joint simulation |
| `thermal` | `common` | Enable ThermodynamicState + heat transfer laws |

---

## 2. MaterialProperties — Per Component

### 2.1 Ti-6Al-4V (Grade 5 Titanium) — Primary Structure

**Used by**: Helmet, Torso Chest Plate, Torso Back Plate, Shoulder Pauldron Left, Shoulder Pauldron Right, Upper Arm Left, Upper Arm Right, Forearm Left, Forearm Right, Gauntlet Left, Gauntlet Right, Hip Assembly, Thigh Left, Thigh Right, Shin Left, Shin Right, Boot Left, Boot Right, Spine Assembly

```toml
[material]
name = "Ti-6Al-4V (Grade 5 Titanium)"
young_modulus = 113800000000.0
poisson_ratio = 0.342
yield_strength = 880000000.0
ultimate_strength = 950000000.0
fracture_toughness = 75000000.0
hardness = 349.0
thermal_conductivity = 6.7
specific_heat = 526.0
thermal_expansion = 0.0000086
melting_point = 1933.0
density = 4430.0
friction_static = 0.36
friction_kinetic = 0.30
restitution = 0.4
```

### 2.2 W-25Re Alloy (Tungsten-Rhenium) — Fusion Reactor Vessel

**Used by**: Fusion Reactor Core

```toml
[material]
name = "W-25Re Alloy (Tungsten-Rhenium)"
young_modulus = 400000000000.0
poisson_ratio = 0.29
yield_strength = 1400000000.0
ultimate_strength = 1800000000.0
fracture_toughness = 25000000.0
hardness = 450.0
thermal_conductivity = 65.0
specific_heat = 140.0
thermal_expansion = 0.0000052
melting_point = 3350.0
density = 20600.0
friction_static = 0.45
friction_kinetic = 0.35
restitution = 0.3
```

### 2.3 Na-S Solid State (V-Cell) — Buffer Array

**Used by**: V-Cell Buffer Array

```toml
[material]
name = "V-Cell Na-S Solid State (Sc-NASICON)"
young_modulus = 100000000000.0
poisson_ratio = 0.25
yield_strength = 200000000.0
ultimate_strength = 280000000.0
fracture_toughness = 2500000.0
hardness = 650.0
thermal_conductivity = 3.0
specific_heat = 800.0
thermal_expansion = 0.00001
melting_point = 1800.0
density = 3200.0
friction_static = 0.40
friction_kinetic = 0.30
restitution = 0.2
```

### 2.4 Mo-47.5Re Alloy (Molybdenum-Rhenium) — Ion Thruster Chamber

**Used by**: Ion Thruster Pack

```toml
[material]
name = "Mo-47.5Re Alloy (Molybdenum-Rhenium)"
young_modulus = 360000000000.0
poisson_ratio = 0.30
yield_strength = 1100000000.0
ultimate_strength = 1400000000.0
fracture_toughness = 20000000.0
hardness = 350.0
thermal_conductivity = 50.0
specific_heat = 250.0
thermal_expansion = 0.0000055
melting_point = 2900.0
density = 14500.0
friction_static = 0.40
friction_kinetic = 0.30
restitution = 0.3
```

### 2.5 Polycarbonate + LED — Status Array

**Used by**: Status Array

```toml
[material]
name = "Polycarbonate + LED Array"
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
```

---

## 3. Instance File Structure

### 3.1 File → Entity Mapping

| Instance File | Mesh File | Entity | Material |
|--------------|-----------|--------|----------|
| VSupreme_Helmet.glb.toml | meshes/VSupreme_Helmet.glb | Helmet | Ti-6Al-4V |
| VSupreme_TorsoChest.glb.toml | meshes/VSupreme_TorsoChest.glb | Torso Chest Plate | Ti-6Al-4V |
| VSupreme_TorsoBack.glb.toml | meshes/VSupreme_TorsoBack.glb | Torso Back Plate | Ti-6Al-4V |
| VSupreme_FusionReactor.glb.toml | meshes/VSupreme_FusionReactor.glb | Fusion Reactor Core | W-25Re |
| VSupreme_VCellArray.glb.toml | meshes/VSupreme_VCellArray.glb | V-Cell Buffer Array | Na-S Solid State |
| VSupreme_PauldronL.glb.toml | meshes/VSupreme_PauldronL.glb | Shoulder Pauldron Left | Ti-6Al-4V |
| VSupreme_PauldronR.glb.toml | meshes/VSupreme_PauldronR.glb | Shoulder Pauldron Right | Ti-6Al-4V |
| VSupreme_UpperArmL.glb.toml | meshes/VSupreme_UpperArmL.glb | Upper Arm Left | Ti-6Al-4V |
| VSupreme_UpperArmR.glb.toml | meshes/VSupreme_UpperArmR.glb | Upper Arm Right | Ti-6Al-4V |
| VSupreme_ForearmL.glb.toml | meshes/VSupreme_ForearmL.glb | Forearm Left | Ti-6Al-4V |
| VSupreme_ForearmR.glb.toml | meshes/VSupreme_ForearmR.glb | Forearm Right | Ti-6Al-4V |
| VSupreme_GauntletL.glb.toml | meshes/VSupreme_GauntletL.glb | Gauntlet Left | Ti-6Al-4V |
| VSupreme_GauntletR.glb.toml | meshes/VSupreme_GauntletR.glb | Gauntlet Right | Ti-6Al-4V |
| VSupreme_HipAssembly.glb.toml | meshes/VSupreme_HipAssembly.glb | Hip Assembly | Ti-6Al-4V |
| VSupreme_ThighL.glb.toml | meshes/VSupreme_ThighL.glb | Thigh Left | Ti-6Al-4V |
| VSupreme_ThighR.glb.toml | meshes/VSupreme_ThighR.glb | Thigh Right | Ti-6Al-4V |
| VSupreme_ShinL.glb.toml | meshes/VSupreme_ShinL.glb | Shin Left | Ti-6Al-4V |
| VSupreme_ShinR.glb.toml | meshes/VSupreme_ShinR.glb | Shin Right | Ti-6Al-4V |
| VSupreme_BootL.glb.toml | meshes/VSupreme_BootL.glb | Boot Left | Ti-6Al-4V |
| VSupreme_BootR.glb.toml | meshes/VSupreme_BootR.glb | Boot Right | Ti-6Al-4V |
| VSupreme_Spine.glb.toml | meshes/VSupreme_Spine.glb | Spine Assembly | Ti-6Al-4V |
| VSupreme_IonThrusterPack.glb.toml | meshes/VSupreme_IonThrusterPack.glb | Ion Thruster Pack | Mo-47.5Re |
| VSupreme_StatusArray.glb.toml | meshes/VSupreme_StatusArray.glb | Status Array | Polycarbonate |

### 3.2 Standard .glb.toml Section Template

```toml
# V-Supreme {ComponentName} — {MaterialName}
# {Brief role description}

[asset]
mesh = "meshes/VSupreme_{ComponentName}.glb"

[transform]
position = [x, y, z]              # meters, Y-up, AABB origin-centric offset
rotation = [0.0, 0.0, 0.0, 1.0]  # quaternion [x, y, z, w]
scale = [1.0, 1.0, 1.0]          # unity (mesh is real-world scale)

[properties]
name = "VSupreme_{ComponentName}"
class_name = "Part"
color = [r, g, b, a]              # linear RGBA 0.0–1.0
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
# 14 base fields (SI units)

[material.custom]
role = "{component_role}"
# domain-specific extensions

[thermodynamic]
temperature = 298.15
pressure = 101325.0
volume = 0.0
internal_energy = 0.0
entropy = 0.0
enthalpy = 0.0
moles = 1.0

# [electrochemical] — only for Fusion Reactor Core + V-Cell Buffer Array
```

### 3.3 Transform Layout — AABB Origin-Centric Positions (Y-Up)

All positions are relative to the mecha's geometric center at ground level (origin at feet center, Y-up). The assembly is centered at X=0, Z=0. Y=0 is ground contact.

| Component | Position [x, y, z] (m) | AABB Dimensions [w, h, d] (m) | Notes |
|-----------|------------------------|-------------------------------|-------|
| Helmet | [0.0, 2.05, 0.0] | [0.28, 0.30, 0.28] | Top of assembly |
| Torso Chest Plate | [0.0, 1.45, 0.08] | [0.50, 0.55, 0.18] | Front torso |
| Torso Back Plate | [0.0, 1.45, -0.08] | [0.50, 0.55, 0.18] | Rear torso |
| Fusion Reactor Core | [0.0, 1.50, 0.0] | [0.25, 0.30, 0.25] | Center of chest cavity |
| V-Cell Buffer Array | [0.0, 1.30, 0.0] | [0.40, 0.20, 0.15] | Below reactor, 3 per side |
| Shoulder Pauldron Left | [-0.35, 1.70, 0.0] | [0.20, 0.18, 0.22] | Left shoulder |
| Shoulder Pauldron Right | [0.35, 1.70, 0.0] | [0.20, 0.18, 0.22] | Right shoulder |
| Upper Arm Left | [-0.40, 1.45, 0.0] | [0.12, 0.30, 0.12] | Left upper arm |
| Upper Arm Right | [0.40, 1.45, 0.0] | [0.12, 0.30, 0.12] | Right upper arm |
| Forearm Left | [-0.42, 1.10, 0.05] | [0.11, 0.28, 0.11] | Left forearm (plasma cutter) |
| Forearm Right | [0.42, 1.10, 0.05] | [0.11, 0.28, 0.11] | Right forearm (DEP emitter) |
| Gauntlet Left | [-0.43, 0.82, 0.05] | [0.10, 0.18, 0.12] | Left hand |
| Gauntlet Right | [0.43, 0.82, 0.05] | [0.10, 0.18, 0.12] | Right hand |
| Hip Assembly | [0.0, 0.95, 0.0] | [0.45, 0.18, 0.25] | Waist ring |
| Thigh Left | [-0.15, 0.68, 0.0] | [0.16, 0.36, 0.16] | Left thigh |
| Thigh Right | [0.15, 0.68, 0.0] | [0.16, 0.36, 0.16] | Right thigh |
| Shin Left | [-0.15, 0.30, 0.0] | [0.13, 0.40, 0.14] | Left shin |
| Shin Right | [0.15, 0.30, 0.0] | [0.13, 0.40, 0.14] | Right shin |
| Boot Left | [-0.15, 0.06, 0.02] | [0.14, 0.12, 0.30] | Left boot |
| Boot Right | [0.15, 0.06, 0.02] | [0.14, 0.12, 0.30] | Right boot |
| Spine Assembly | [0.0, 1.35, -0.05] | [0.08, 0.60, 0.08] | Central spine column |
| Ion Thruster Pack | [0.0, 1.55, -0.20] | [0.35, 0.40, 0.15] | Back-mounted |
| Status Array | [0.0, 2.08, 0.10] | [0.15, 0.08, 0.02] | Visor-integrated |

---

## 4. Domain-Specific State — KineticState (42-DOF Joint Simulation)

### 4.1 KineticState Fields

| Field | Type | Unit | Initial Value | Description |
|-------|------|------|---------------|-------------|
| `joint_angles` | `[f64; 42]` | rad | `[0.0; 42]` | Current angle of each DOF |
| `joint_velocities` | `[f64; 42]` | rad/s | `[0.0; 42]` | Angular velocity per DOF |
| `joint_torques` | `[f64; 42]` | N·m | `[0.0; 42]` | Applied torque per DOF |
| `joint_temperatures` | `[f64; 42]` | K | `[298.15; 42]` | Actuator motor temperature |
| `payload_mass` | `f64` | kg | `0.0` | Current external payload |
| `total_power_draw` | `f64` | W | `0.0` | Summed actuator power consumption |
| `gait_phase` | `String` | — | `"standing"` | Current locomotion phase |
| `center_of_mass` | `[f64; 3]` | m | `[0.0, 1.1, 0.0]` | World-space COM position |

### 4.2 Joint Index Map

| Index | Joint | DOF | Max Torque (N·m) | Max Angle (rad) |
|-------|-------|-----|-----------------|-----------------|
| 0–2 | Neck (tilt_lateral, tilt_forward, rotation) | 3 | 80 | ±0.79 (±45°) |
| 3–5 | Left Shoulder (abduction, flexion, rotation) | 3 | 200 | ±3.14 (±180°) |
| 6 | Left Elbow (flexion) | 1 | 200 | 0 to 2.62 (0–150°) |
| 7–9 | Left Wrist (flexion, deviation, pronation) | 3 | 80 | ±1.57 (±90°) |
| 10–14 | Left Hand (thumb + 4 fingers) | 5 | 20 (tip force N) | 0 to 1.57 (0–90°) |
| 15–17 | Right Shoulder | 3 | 200 | ±3.14 |
| 18 | Right Elbow | 1 | 200 | 0 to 2.62 |
| 19–21 | Right Wrist | 3 | 80 | ±1.57 |
| 22–26 | Right Hand | 5 | 20 | 0 to 1.57 |
| 27–29 | Spine (lateral, forward, rotation) | 3 | 350 | ±0.52 (±30°) |
| 30–32 | Left Hip (flexion, abduction, rotation) | 3 | 800 | ±2.09 (±120°) |
| 33 | Left Knee (flexion) | 1 | 800 | 0 to 2.62 |
| 34–35 | Left Ankle (dorsiflexion, inversion) | 2 | 350 | ±0.79 |
| 36–38 | Right Hip | 3 | 800 | ±2.09 |
| 39 | Right Knee | 1 | 800 | 0 to 2.62 |
| 40–41 | Right Ankle | 2 | 350 | ±0.79 |

### 4.3 Runtime Update Flow

```
every tick (1 ms):
  1. Read operator input (harness sensors → desired joint_angles)
  2. Vortex motion planner:
     a. Compute inverse kinematics for desired end-effector pose
     b. Apply force/torque limits per joint
     c. Apply collision avoidance (proximity sensors)
     d. Compute center_of_mass for balance control
  3. For each joint i in 0..42:
     a. error = desired_angle[i] - joint_angles[i]
     b. torque = PID(error, joint_velocities[i])
     c. clamp torque to [-max_torque[i], max_torque[i]]
     d. Apply current limit (hardware safety)
     e. Send torque command via EtherCAT
  4. Read encoder feedback → update joint_angles, joint_velocities
  5. Read force/torque sensors → update joint_torques (measured)
  6. Compute total_power_draw = sum(|torque[i] * velocity[i]|)
  7. Update joint_temperatures via thermal model (I²R heating - conduction cooling)
  8. If any joint_temperature > 380 K → derate that joint to 50% torque
  9. If any joint_temperature > 400 K → lock that joint (thermal protection)
  10. Update gait_phase based on foot contact sensors
```

---

## 5. ThermodynamicState

### 5.1 Fields

| Field | Type | Unit | Initial Value | Description |
|-------|------|------|---------------|-------------|
| `temperature` | `f64` | K | `298.15` | Component bulk temperature |
| `pressure` | `f64` | Pa | `101325.0` | Internal/ambient pressure |
| `volume` | `f64` | m³ | (per component) | Physical volume |
| `internal_energy` | `f64` | J | `0.0` | Stored thermal energy |
| `entropy` | `f64` | J/K | `0.0` | Thermodynamic entropy |
| `enthalpy` | `f64` | J | `0.0` | Enthalpy |
| `moles` | `f64` | mol | (per component) | Material quantity |

### 5.2 Component Volumes and Initial Thermodynamic State

| Component | Volume (m³) | Moles | Notes |
|-----------|------------|-------|-------|
| Helmet | 0.0024 | 0.20 | Shell volume (hollow) |
| Torso Chest Plate | 0.0050 | 0.42 | Armor composite stack |
| Torso Back Plate | 0.0050 | 0.42 | Armor composite stack |
| Fusion Reactor Core | 0.0147 | 14.7 | Ø250 × 300 mm cylinder |
| V-Cell Buffer Array | 0.0120 | 12.0 | 6 modules |
| Shoulder Pauldron (each) | 0.0008 | 0.07 | Shell |
| Upper Arm (each) | 0.0034 | 0.28 | Tube + actuators |
| Forearm (each) | 0.0027 | 0.22 | Tube + weapon housing |
| Gauntlet (each) | 0.0022 | 0.18 | Hand mechanism |
| Hip Assembly | 0.0020 | 0.17 | Ring structure |
| Thigh (each) | 0.0073 | 0.60 | Tube + actuators |
| Shin (each) | 0.0058 | 0.48 | Tube + actuators |
| Boot (each) | 0.0050 | 0.42 | Shell + shock absorber |
| Spine Assembly | 0.0024 | 0.20 | Vertebrae column |
| Ion Thruster Pack | 0.0210 | 1.45 | Tanks + thrusters |
| Status Array | 0.0002 | 0.002 | LED array |

### 5.3 Operating Envelope

| Environment | Component | Temp (K) | Pressure (Pa) |
|-------------|-----------|----------|---------------|
| Terrestrial nominal | All structural | 298–320 | 101,325 |
| Terrestrial nominal | Reactor core | 350 | 101,325 |
| Space (sunlit) | Armor skin | 390 | 0 (vacuum) |
| Space (shadow) | Armor skin | 120 | 0 (vacuum) |
| Underwater (200 m) | All external | 277 | 2,068,500 |
| Reactor idle | Reactor core | 300 | 101,325 |
| Reactor full power | Reactor core | 350 | Internal plasma: ~10⁵ |

---

## 6. ElectrochemicalState (Fusion Reactor + V-Cell Array Only)

### 6.1 Fields

| Field | Type | Unit | Initial Value | Description |
|-------|------|------|---------------|-------------|
| `open_circuit_voltage` | `f64` | V | (per component) | Open-circuit voltage |
| `state_of_charge` | `f64` | — | `1.0` | 0.0 = empty, 1.0 = full |
| `capacity_ah` | `f64` | Ah | (per component) | Total capacity |
| `internal_resistance` | `f64` | Ω | (per component) | Internal resistance |
| `cycle_count` | `u32` | — | `0` | Charge/discharge cycles |
| `coulombic_efficiency` | `f64` | — | (per component) | Charge transfer efficiency |

### 6.2 Fusion Reactor Core — Electrochemical State

```toml
[electrochemical]
open_circuit_voltage = 600.0
state_of_charge = 1.0
capacity_ah = 833.3
internal_resistance = 0.001
cycle_count = 0
coulombic_efficiency = 0.70
```

**Notes**: For the fusion reactor, `open_circuit_voltage` represents the direct converter output (600 VDC bus). `capacity_ah` is a notional representation of fuel load (833.3 Ah × 600 V = 500 kWh equivalent for the fuel load). `coulombic_efficiency` of 0.70 represents the direct energy conversion efficiency.

### 6.3 V-Cell Buffer Array — Electrochemical State

```toml
[electrochemical]
open_circuit_voltage = 600.0
state_of_charge = 1.0
capacity_ah = 83.3
internal_resistance = 0.005
cycle_count = 0
coulombic_efficiency = 0.999
```

**Notes**: 6 × V-Cell modules in series-parallel. 50 kWh / 600 V = 83.3 Ah total. Internal resistance of 0.005 Ω allows 10C discharge (833 A × 600 V = 500 kW burst).

---

## 7. Domain Laws — Kinematic & Thermal

### 7.1 Kinematic Laws Reference

| Law | Function | Inputs | Output | Crate Path |
|-----|----------|--------|--------|------------|
| Forward Kinematics | `compute_fk(joint_angles) → end_effector_poses` | 42 joint angles | 23 body segment transforms | `crates/common/src/realism/laws/kinematics.rs` |
| Inverse Kinematics | `compute_ik(target_pose) → joint_angles` | Target end-effector pose | 42 joint angles | `crates/common/src/realism/laws/kinematics.rs` |
| Dynamics (Newton-Euler) | `compute_dynamics(angles, velocities, accelerations, external_forces) → torques` | State vector + forces | 42 required torques | `crates/common/src/realism/laws/dynamics.rs` |
| Balance Control | `compute_zmp(com, support_polygon) → stable` | Center of mass, foot contacts | Boolean stability + correction vector | `crates/common/src/realism/laws/balance.rs` |
| Collision Detection | `check_self_collision(joint_angles) → contacts` | 42 joint angles | Contact point list | `crates/common/src/realism/laws/collision.rs` |

### 7.2 Thermal Laws Reference

| Law | Function | Inputs | Output |
|-----|----------|--------|--------|
| Actuator Heating | `Q_gen = I² × R_winding` | Current, winding resistance | Heat generated (W) |
| Conduction (frame) | `Q_cond = k × A × ΔT / L` | Conductivity, area, temp diff, length | Heat flow (W) |
| Convection (armor skin) | `Q_conv = h × A × (T_skin - T_ambient)` | h=10–25 W/(m²·K) for forced air | Heat rejection (W) |
| Radiation (space) | `Q_rad = ε × σ × A × (T⁴ - T_env⁴)` | Emissivity, Stefan-Boltzmann, area | Heat rejection (W) |
| Coolant Loop | `Q_coolant = ṁ × c_p × ΔT` | Mass flow rate, specific heat, temp diff | Heat transport (W) |

### 7.3 Calibrated Constants

| Constant | Value | Unit | Context |
|----------|-------|------|---------|
| Reactor waste heat fraction | 0.30 | — | 30% of fusion power → heat |
| Actuator efficiency | 0.85 | — | 15% of electrical input → heat |
| Armor emissivity (Ti-6Al-4V, oxidized) | 0.60 | — | Radiative cooling in space |
| Convection coefficient (walking, air) | 15.0 | W/(m²·K) | Forced convection over armor |
| Convection coefficient (underwater) | 500.0 | W/(m²·K) | Water convection over armor |
| Coolant flow rate (Loop 1) | 2.0 | L/s | Reactor loop |
| Coolant flow rate (Loop 2) | 1.5 | L/s | Weapons loop |
| Coolant specific heat (Therminol HT-55) | 1850.0 | J/(kg·K) | Synthetic hydrocarbon |
| PCM latent heat (paraffin pads) | 200000.0 | J/kg | Phase change buffer |

---

## 8. Realism Config

```toml
[realism]
enabled = true
time_scale = 1.0
gravity = [0.0, -9.81, 0.0]

[realism.features]
materials = true
thermodynamics = true
electrochemistry = true
structural = true
kinematics = true

[realism.thermal]
ambient_temperature = 298.15
ambient_pressure = 101325.0
convection_coefficient = 15.0
radiation_enabled = true

[realism.kinematic]
dof_count = 42
control_loop_hz = 1000
actuator_model = "bldc_harmonic_drive"
balance_control = true
self_collision = true

[realism.electrochemical]
reactor_model = "aneutronic_p_b11"
reactor_power_kw = 500.0
buffer_capacity_kwh = 50.0
bus_voltage_vdc = 600.0
```

---

## 9. Structural Bundle Requirements

### 9.1 Components Table

| Component | Fracture-Critical | Fatigue-Monitored | Strain Gauges | Priority |
|-----------|------------------|-------------------|---------------|----------|
| Helmet | No | No | 0 | Low |
| Torso Chest Plate | Yes | Yes | 4 | Critical |
| Torso Back Plate | Yes | Yes | 4 | Critical |
| Fusion Reactor Core | Yes | Yes | 2 | Critical |
| V-Cell Buffer Array | No | No | 0 | Medium |
| Shoulder Pauldron (each) | No | Yes | 1 | Medium |
| Upper Arm (each) | No | Yes | 2 | High |
| Forearm (each) | No | Yes | 2 | High |
| Gauntlet (each) | No | Yes | 2 | High |
| Hip Assembly | Yes | Yes | 4 | Critical |
| Thigh (each) | Yes | Yes | 3 | Critical |
| Shin (each) | Yes | Yes | 3 | Critical |
| Boot (each) | No | Yes | 2 | High |
| Spine Assembly | Yes | Yes | 4 | Critical |
| Ion Thruster Pack | No | No | 1 | Low |
| Status Array | No | No | 0 | Low |

**Priority Notes**:
- **Critical**: Load-bearing structural members that carry operator + payload weight. Failure = loss of structural integrity. Requires real-time Miner's rule fatigue accumulation via Vortex.
- **High**: Secondary load-bearing members. Failure = loss of function but not catastrophic.
- **Medium**: Protective/functional components. Failure = degraded capability.
- **Low**: Non-structural components. Failure = aesthetic/informational loss only.

---

## 10. Deployment Checklist

### 10.1 Copy Instructions

```powershell
# Copy instance files (.glb.toml) to Workspace
Copy-Item "docs/Products/V-Supreme/V1/*.glb.toml" `
  "C:\Users\miksu\Documents\Eustress\Universe1\spaces\Space1\Workspace\" -Force

# Copy mesh files (.glb) to product asset folder
$dest = "C:\Users\miksu\Documents\Eustress\Universe1\spaces\Space1\assets\meshes\products\V-Supreme\"
New-Item -ItemType Directory -Path $dest -Force
Copy-Item "docs/Products/V-Supreme/V1/meshes/*.glb" $dest -Force
```

### 10.2 Pre-Launch Checks

- [ ] All 23 `.glb.toml` files present in `Workspace/`
- [ ] All 23 `.glb` mesh files present in `assets/meshes/products/V-Supreme/`
- [ ] Every `[asset] mesh` path resolves to an existing `.glb` file
- [ ] Every `class_name = "Part"` (no `AdvancedPart`)
- [ ] Every `[transform] position` uses meters, Y-up, AABB origin-centric
- [ ] Every `[transform] scale = [1.0, 1.0, 1.0]`
- [ ] Every `[transform] rotation` is valid quaternion `[x, y, z, w]`
- [ ] Every `color` is linear RGBA `[0.0–1.0]`
- [ ] Every `[material]` has all 14 base fields in SI units
- [ ] Every `[material.custom]` has a `role` tag
- [ ] Fusion Reactor Core has `[electrochemical]` section
- [ ] V-Cell Buffer Array has `[electrochemical]` section
- [ ] All 22 thermodynamic components have `[thermodynamic]` section
- [ ] No references to deprecated `.eustressengine` format
- [ ] ISO 8601 timestamps in all `[metadata]`

### 10.3 Runtime Validation Sanity Checks

| Check | Expected Value | Tolerance |
|-------|---------------|-----------|
| Reactor `open_circuit_voltage` | 600.0 V | ±1.0 V |
| V-Cell Array `capacity_ah` | 83.3 Ah | ±0.5 Ah |
| Helmet `density` | 4430.0 kg/m³ | ±10 kg/m³ |
| Hip Assembly `yield_strength` | 880 × 10⁶ Pa | ±5 × 10⁶ Pa |
| Total component count | 23 | Exact |
| Components with `[electrochemical]` | 2 | Exact |
| Components with `[thermodynamic]` | 22 | Exact |
| Mecha overall height (helmet top Y) | ~2.2 m | ±0.1 m |
| Ground contact Y (boot bottom) | 0.0 m | ±0.01 m |
