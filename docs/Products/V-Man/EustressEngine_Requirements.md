# VOLTEC V-MAN — EustressEngine Simulation Requirements

**Document Classification**: Voltec Internal — Simulation Specification  
**Version**: 1.0  
**Date**: March 2, 2026  
**Authors**: Voltec Advanced Manufacturing Division  
**Status**: Active  

---

## Table of Contents

1. [Required Crate Features](#1-required-crate-features)
2. [MaterialProperties — Per Component](#2-materialproperties--per-component)
3. [Instance File Structure](#3-instance-file-structure)
4. [Domain-Specific State: KineticState](#4-domain-specific-state-kineticstate)
5. [ThermodynamicState](#5-thermodynamicstate)
6. [Domain Laws: Kinematics & Thermal](#6-domain-laws-kinematics--thermal)
7. [Realism Config](#7-realism-config)
8. [Structural Bundle Requirements](#8-structural-bundle-requirements)
9. [Deployment Checklist](#9-deployment-checklist)

---

## 1. Required Crate Features

| Feature Flag | Crate | Purpose |
|-------------|-------|---------|
| `realism` | `eustress-common` | Enable MaterialProperties, ThermodynamicState |
| `kinetics` | `eustress-common` | Enable KineticState for arm/conveyor motion |
| `structural` | `eustress-common` | Enable StructuralBundle for stress analysis |
| `thermodynamics` | `eustress-common` | Enable thermal simulation (heat dissipation) |

---

## 2. MaterialProperties — Per Component

### 2.1 Chassis — S355J2 Structural Steel

```toml
[material]
name = "S355J2 Structural Steel"
young_modulus = 210.0e9
poisson_ratio = 0.30
yield_strength = 355.0e6
ultimate_strength = 510.0e6
fracture_toughness = 60.0e6
hardness = 160.0
thermal_conductivity = 50.0
specific_heat = 480.0
thermal_expansion = 12.0e-6
melting_point = 1793.0
density = 7850.0
friction_static = 0.74
friction_kinetic = 0.57
restitution = 0.20

[material.custom]
role = "structural_chassis"
container_standard = "ISO 668 / ISO 1496"
wall_thickness_mm = 2.0
corrosion_protection = "hot-dip galvanized + powder coat"
vibration_isolation_hz = 2.5
```

### 2.2 Robotic Arm Array — Aluminum 7075-T6

```toml
[material]
name = "Aluminum 7075-T6"
young_modulus = 71.7e9
poisson_ratio = 0.33
yield_strength = 503.0e6
ultimate_strength = 572.0e6
fracture_toughness = 29.0e6
hardness = 175.0
thermal_conductivity = 130.0
specific_heat = 960.0
thermal_expansion = 23.6e-6
melting_point = 750.0
density = 2810.0
friction_static = 0.47
friction_kinetic = 0.35
restitution = 0.30

[material.custom]
role = "robotic_arm_structure"
axes = 6.0
payload_kg = 20.0
repeatability_mm = 0.02
reach_mm = 1300.0
max_joint_speed_deg_per_s = 300.0
max_tcp_speed_mm_per_s = 2000.0
ip_rating = "IP67"
mtbf_hours = 80000.0
power_peak_w = 1200.0
power_avg_w = 400.0
```

### 2.3 Vision System Housing — Aluminum 6061-T6

```toml
[material]
name = "Aluminum 6061-T6"
young_modulus = 68.9e9
poisson_ratio = 0.33
yield_strength = 276.0e6
ultimate_strength = 310.0e6
fracture_toughness = 29.0e6
hardness = 95.0
thermal_conductivity = 167.0
specific_heat = 896.0
thermal_expansion = 23.6e-6
melting_point = 855.0
density = 2700.0
friction_static = 0.42
friction_kinetic = 0.30
restitution = 0.30

[material.custom]
role = "vision_system_housing"
lidar_wavelength_nm = 905.0
lidar_accuracy_mm = 1.0
lidar_points_per_s = 300000.0
rgbd_resolution = "3840x2160"
rgbd_fps = 60.0
structured_light_resolution_um = 10.0
inference_latency_ms = 50.0
```

### 2.4 Tool Magazine — Aluminum 6061-T6

```toml
[material]
name = "Aluminum 6061-T6"
young_modulus = 68.9e9
poisson_ratio = 0.33
yield_strength = 276.0e6
ultimate_strength = 310.0e6
fracture_toughness = 29.0e6
hardness = 95.0
thermal_conductivity = 167.0
specific_heat = 896.0
thermal_expansion = 23.6e-6
melting_point = 855.0
density = 2700.0
friction_static = 0.42
friction_kinetic = 0.30
restitution = 0.30

[material.custom]
role = "tool_magazine"
capacity_slots = 12.0
tool_change_time_s = 5.0
coupling_type = "ISO 9409-1 + kinematic pin"
locking_mechanism = "pneumatic 6 bar fail-safe"
rfid_standard = "ISO 14443A"
position_repeatability_mm = 0.005
max_tool_weight_kg = 8.0
```

### 2.5 Conveyor Module — S355J2 Structural Steel

```toml
[material]
name = "S355J2 Structural Steel"
young_modulus = 210.0e9
poisson_ratio = 0.30
yield_strength = 355.0e6
ultimate_strength = 510.0e6
fracture_toughness = 60.0e6
hardness = 160.0
thermal_conductivity = 50.0
specific_heat = 480.0
thermal_expansion = 12.0e-6
melting_point = 1793.0
density = 7850.0
friction_static = 0.74
friction_kinetic = 0.57
restitution = 0.20

[material.custom]
role = "conveyor_frame"
conveyor_length_m = 10.0
conveyor_width_m = 0.60
work_surface_height_m = 0.85
speed_range_min_m_per_s = 0.01
speed_range_max_m_per_s = 0.50
position_accuracy_mm = 0.5
max_part_weight_kg = 50.0
belt_material = "antistatic PU"
drive_power_kw = 0.75
```

### 2.6 Control Cabinet — 316L Stainless Steel

```toml
[material]
name = "316L Stainless Steel"
young_modulus = 193.0e9
poisson_ratio = 0.27
yield_strength = 170.0e6
ultimate_strength = 485.0e6
fracture_toughness = 112.0e6
hardness = 217.0
thermal_conductivity = 16.3
specific_heat = 500.0
thermal_expansion = 15.9e-6
melting_point = 1673.0
density = 8000.0
friction_static = 0.60
friction_kinetic = 0.40
restitution = 0.25

[material.custom]
role = "control_cabinet"
cpu = "AMD EPYC Embedded 3255"
cpu_cores = 8.0
ram_gb = 64.0
gpu = "NVIDIA Jetson AGX Orin"
gpu_tops = 275.0
storage_tb = 2.0
ethercat_cycle_ms = 1.0
ip_rating = "IP65"
ups_kva = 5.0
ups_runtime_min = 15.0
```

### 2.7 Power Distribution Unit — S235JR Steel

```toml
[material]
name = "S235JR Steel"
young_modulus = 210.0e9
poisson_ratio = 0.30
yield_strength = 235.0e6
ultimate_strength = 360.0e6
fracture_toughness = 50.0e6
hardness = 120.0
thermal_conductivity = 50.0
specific_heat = 480.0
thermal_expansion = 12.0e-6
melting_point = 1793.0
density = 7850.0
friction_static = 0.74
friction_kinetic = 0.57
restitution = 0.20

[material.custom]
role = "power_distribution"
input_voltage = "400V 3-phase AC"
total_capacity_kva = 30.0
peak_power_kw = 25.0
avg_power_kw = 12.0
ups_backup = true
surge_protection = true
energy_monitoring = true
```

### 2.8 Pneumatics Module — Aluminum 6061-T6

```toml
[material]
name = "Aluminum 6061-T6"
young_modulus = 68.9e9
poisson_ratio = 0.33
yield_strength = 276.0e6
ultimate_strength = 310.0e6
fracture_toughness = 29.0e6
hardness = 95.0
thermal_conductivity = 167.0
specific_heat = 896.0
thermal_expansion = 23.6e-6
melting_point = 855.0
density = 2700.0
friction_static = 0.42
friction_kinetic = 0.30
restitution = 0.30

[material.custom]
role = "pneumatics_module"
operating_pressure_bar = 6.0
compressor_power_kw = 1.5
tank_volume_l = 50.0
flow_rate_l_per_min = 200.0
filtration_um = 5.0
dew_point_c = -20.0
```

### 2.9 Safety Enclosure — Polycarbonate

```toml
[material]
name = "Polycarbonate"
young_modulus = 2.4e9
poisson_ratio = 0.37
yield_strength = 62.0e6
ultimate_strength = 72.0e6
fracture_toughness = 3.5e6
hardness = 85.0
thermal_conductivity = 0.20
specific_heat = 1200.0
thermal_expansion = 65.0e-6
melting_point = 540.0
density = 1200.0
friction_static = 0.50
friction_kinetic = 0.38
restitution = 0.35

[material.custom]
role = "safety_enclosure"
ip_rating = "IP65"
light_curtain_resolution_mm = 14.0
safety_standard = "ISO 10218-2"
performance_level = "PLe"
estop_channels = 4.0
interlock_type = "electromagnetic"
transmittance = 0.88
```

### 2.10 Sensor Suite Housing — Aluminum 6061-T6

```toml
[material]
name = "Aluminum 6061-T6"
young_modulus = 68.9e9
poisson_ratio = 0.33
yield_strength = 276.0e6
ultimate_strength = 310.0e6
fracture_toughness = 29.0e6
hardness = 95.0
thermal_conductivity = 167.0
specific_heat = 896.0
thermal_expansion = 23.6e-6
melting_point = 855.0
density = 2700.0
friction_static = 0.42
friction_kinetic = 0.30
restitution = 0.30

[material.custom]
role = "sensor_suite"
force_torque_axes = 6.0
force_range_n = 500.0
torque_range_nm = 50.0
force_resolution_n = 0.01
proximity_range_m = 4.0
temperature_sensors = 8.0
vibration_range_g = 50.0
vibration_bandwidth_hz = 10000.0
```

### 2.11 Human-Machine Interface — Gorilla Glass + Aluminum

```toml
[material]
name = "Gorilla Glass / Aluminum"
young_modulus = 70.0e9
poisson_ratio = 0.22
yield_strength = 400.0e6
ultimate_strength = 500.0e6
fracture_toughness = 0.7e6
hardness = 600.0
thermal_conductivity = 1.0
specific_heat = 840.0
thermal_expansion = 7.0e-6
melting_point = 1873.0
density = 2500.0
friction_static = 0.40
friction_kinetic = 0.30
restitution = 0.30

[material.custom]
role = "human_machine_interface"
screen_size_in = 15.6
resolution = "1920x1080"
touch_type = "capacitive"
ip_rating = "IP65"
brightness_nits = 1000.0
operating_temp_min_c = 0.0
operating_temp_max_c = 50.0
```

### 2.12 StatusArray — Polycarbonate

```toml
[material]
name = "Polycarbonate"
young_modulus = 2.4e9
poisson_ratio = 0.37
yield_strength = 62.0e6
ultimate_strength = 72.0e6
fracture_toughness = 3.5e6
hardness = 85.0
thermal_conductivity = 0.20
specific_heat = 1200.0
thermal_expansion = 65.0e-6
melting_point = 540.0
density = 1200.0
friction_static = 0.50
friction_kinetic = 0.38
restitution = 0.35

[material.custom]
role = "status_display"
led_type = "addressable RGB"
led_count = 64.0
max_brightness_cd_per_m2 = 5000.0
refresh_rate_hz = 120.0
voltage = 24.0
power_w = 15.0
```

---

## 3. Instance File Structure

### 3.1 File → Entity Mapping

| File | Entity | Mesh | Class |
|------|--------|------|-------|
| `VMan_Chassis.glb.toml` | Container chassis | `VMan_Chassis.glb` | AdvancedPart |
| `VMan_RoboticArm.glb.toml` | Single arm (×4 instances) | `VMan_RoboticArm.glb` | AdvancedPart |
| `VMan_VisionSystem.glb.toml` | LIDAR + camera array | `VMan_VisionSystem.glb` | AdvancedPart |
| `VMan_ToolMagazine.glb.toml` | End-effector storage rack | `VMan_ToolMagazine.glb` | AdvancedPart |
| `VMan_Conveyor.glb.toml` | Belt/roller transport | `VMan_Conveyor.glb` | AdvancedPart |
| `VMan_ControlCabinet.glb.toml` | Compute + PLC enclosure | `VMan_ControlCabinet.glb` | AdvancedPart |
| `VMan_PowerDistribution.glb.toml` | PDU + UPS | `VMan_PowerDistribution.glb` | Part |
| `VMan_Pneumatics.glb.toml` | Compressor + regulators | `VMan_Pneumatics.glb` | Part |
| `VMan_SafetyEnclosure.glb.toml` | Light curtains + doors | `VMan_SafetyEnclosure.glb` | Part |
| `VMan_SensorSuite.glb.toml` | Distributed sensor array | `VMan_SensorSuite.glb` | Part |
| `VMan_HMI.glb.toml` | Touchscreen panel | `VMan_HMI.glb` | Part |
| `VMan_StatusArray.glb.toml` | LED status display | `VMan_StatusArray.glb` | Part |

### 3.2 Standard .glb.toml Section Template

```toml
# V-Man {ComponentName} — {MaterialName}
# {Brief description}

[asset]
mesh = "assets/meshes/products/V-Man/VMan_{ComponentName}.glb"
scene = "Scene0"

[transform]
position = [x, y, z]              # meters, Y-up
rotation = [0.0, 0.0, 0.0, 1.0]  # quaternion [x, y, z, w]
scale = [1.0, 1.0, 1.0]          # unit scale (mesh is pre-scaled)

[properties]
color = [r, g, b, a]              # linear RGBA 0.0–1.0
transparency = 0.0
anchored = true
can_collide = true
cast_shadow = true
reflectance = 0.0

[metadata]
class_name = "AdvancedPart"       # or "Part"
archivable = true
created = "2026-03-02T00:00:00Z"
last_modified = "2026-03-02T00:00:00Z"

[material]
# ... (14 base fields from Section 2)

[material.custom]
# ... (domain-specific extensions)

[thermodynamic]
temperature = 298.15
pressure = 101325.0
volume = 0.0
internal_energy = 0.0
entropy = 0.0
enthalpy = 0.0
moles = 1.0
```

### 3.3 Transform Layout Table

Assembly centered at origin, Y-up. Container long axis along Z. Width along X. Height along Y.

| Component | Position [x, y, z] (m) | Scale [x, y, z] (m) | Notes |
|-----------|------------------------|---------------------|-------|
| Chassis | [0.0, 1.448, 0.0] | [1.0, 1.0, 1.0] | Centered at half-height |
| RoboticArm (1) | [-0.6, 0.85, -3.0] | [1.0, 1.0, 1.0] | Left side, near input |
| RoboticArm (2) | [-0.6, 0.85, -1.0] | [1.0, 1.0, 1.0] | Left side, center-front |
| RoboticArm (3) | [0.6, 0.85, -1.0] | [1.0, 1.0, 1.0] | Right side, center-front |
| RoboticArm (4) | [0.6, 0.85, -3.0] | [1.0, 1.0, 1.0] | Right side, near input |
| VisionSystem | [0.0, 2.50, -2.0] | [1.0, 1.0, 1.0] | Overhead, center of work zone |
| ToolMagazine | [0.0, 1.20, 4.5] | [1.0, 1.0, 1.0] | Rear of container |
| Conveyor | [0.0, 0.425, 0.0] | [1.0, 1.0, 1.0] | Centered, 0.85m work height |
| ControlCabinet | [-1.0, 1.20, -5.0] | [1.0, 1.0, 1.0] | Front-left corner |
| PowerDistribution | [-1.0, 0.30, -5.0] | [1.0, 1.0, 1.0] | Under control cabinet |
| Pneumatics | [1.0, 0.30, 4.5] | [1.0, 1.0, 1.0] | Rear-right, floor level |
| SafetyEnclosure | [0.0, 1.448, 0.0] | [1.0, 1.0, 1.0] | Coincident with chassis |
| SensorSuite | [0.0, 2.00, -2.0] | [1.0, 1.0, 1.0] | Distributed, represented at center |
| HMI | [-1.1, 1.50, -4.0] | [1.0, 1.0, 1.0] | Left wall, near personnel door |
| StatusArray | [0.0, 2.80, -6.0] | [1.0, 1.0, 1.0] | Front face of container, top |

---

## 4. Domain-Specific State: KineticState

V-Man's simulation requires KineticState for arm motion and conveyor dynamics.

### 4.1 KineticState Fields

| Field | Type | Unit | Initial Value | Description |
|-------|------|------|---------------|-------------|
| `linear_velocity` | `[f64; 3]` | m/s | [0.0, 0.0, 0.0] | TCP linear velocity |
| `angular_velocity` | `[f64; 3]` | rad/s | [0.0, 0.0, 0.0] | TCP angular velocity |
| `linear_acceleration` | `[f64; 3]` | m/s² | [0.0, 0.0, 0.0] | TCP linear acceleration |
| `angular_acceleration` | `[f64; 3]` | rad/s² | [0.0, 0.0, 0.0] | TCP angular acceleration |
| `joint_positions` | `[f64; 6]` | rad | [0.0; 6] | Per-axis joint angles |
| `joint_velocities` | `[f64; 6]` | rad/s | [0.0; 6] | Per-axis joint velocities |
| `joint_torques` | `[f64; 6]` | Nm | [0.0; 6] | Per-axis joint torques |
| `payload_mass` | `f64` | kg | 0.0 | Current payload at TCP |
| `tcp_force` | `[f64; 3]` | N | [0.0, 0.0, 0.0] | Force at tool center point |
| `tcp_torque` | `[f64; 3]` | Nm | [0.0, 0.0, 0.0] | Torque at tool center point |
| `conveyor_speed` | `f64` | m/s | 0.0 | Belt linear speed |
| `cycle_time` | `f64` | s | 12.0 | Current assembly cycle time |
| `parts_produced` | `u64` | — | 0 | Cumulative count |
| `oee` | `f64` | — | 0.0 | Overall equipment effectiveness (0.0–1.0) |

### 4.2 Runtime Update Flow

```
fn update_kinetic_state(dt: f64, state: &mut KineticState, recipe: &Recipe) {
    // 1. Read current joint positions from EtherCAT
    state.joint_positions = ethercat_read_joints();

    // 2. Compute forward kinematics → TCP pose
    let tcp_pose = forward_kinematics(&state.joint_positions);

    // 3. Compute velocities via finite difference
    state.linear_velocity = (tcp_pose.position - prev_position) / dt;
    state.angular_velocity = (tcp_pose.rotation - prev_rotation) / dt;

    // 4. Compute accelerations
    state.linear_acceleration = (state.linear_velocity - prev_velocity) / dt;

    // 5. Read force/torque sensor
    state.tcp_force = ft_sensor_read_force();
    state.tcp_torque = ft_sensor_read_torque();

    // 6. Update conveyor speed from VFD feedback
    state.conveyor_speed = vfd_read_speed();

    // 7. Update production counters
    if step_complete(recipe.current_step) {
        state.parts_produced += 1;
        state.cycle_time = elapsed_since_cycle_start();
    }

    // 8. Compute OEE = Availability × Performance × Quality
    state.oee = compute_oee(
        uptime_hours, planned_hours,
        actual_cycle_time, ideal_cycle_time,
        good_parts, total_parts
    );
}
```

---

## 5. ThermodynamicState

### 5.1 Fields Table

| Field | Type | Unit | Initial Value | Description |
|-------|------|------|---------------|-------------|
| `temperature` | `f64` | K | 298.15 | Component temperature |
| `pressure` | `f64` | Pa | 101325.0 | Ambient pressure |
| `volume` | `f64` | m³ | (per component) | Component volume |
| `internal_energy` | `f64` | J | 0.0 | Thermal energy stored |
| `entropy` | `f64` | J/K | 0.0 | Thermodynamic entropy |
| `enthalpy` | `f64` | J | 0.0 | Enthalpy |
| `moles` | `f64` | mol | 1.0 | Molar quantity |

### 5.2 Operating Envelope

| Condition | Temperature Range | Power Dissipation | Cooling |
|-----------|------------------|-------------------|---------|
| Idle | 293–303 K | 200 W | Natural convection |
| Production (nominal) | 298–318 K | 3,000 W | Forced air (500 m³/h) |
| Production (peak) | 298–328 K | 5,000 W | Forced air + liquid GPU cooling |
| Storage | 233–343 K | 0 W | None |

### 5.3 Per-Component Thermal Budget

| Component | Heat Generation (W) | Volume (m³) | Thermal Mass (J/K) |
|-----------|--------------------|-----------|--------------------|
| Chassis | 0 (passive) | 0.85 | 3,200,000 |
| Arms (×4) | 1,600 (total) | 0.012 each | 32,300 each |
| Vision System | 50 | 0.008 | 17,200 |
| Control Cabinet | 800 | 0.15 | 60,000 |
| Conveyor | 200 | 0.30 | 112,800 |
| PDU | 150 | 0.08 | 30,100 |
| Pneumatics | 150 | 0.05 | 10,750 |
| StatusArray | 15 | 0.002 | 2,880 |
| **Total** | **~3,000** | — | — |

---

## 6. Domain Laws: Kinematics & Thermal

### 6.1 Kinematic Laws Reference

| Function | Domain | Formula | Crate Path |
|----------|--------|---------|-----------|
| `forward_kinematics` | Robotics | Denavit-Hartenberg chain: T = A1·A2·...·A6 | `crates/common/src/realism/laws/kinematics.rs` |
| `inverse_kinematics` | Robotics | Analytical 6R solution (Pieper's method) | `crates/common/src/realism/laws/kinematics.rs` |
| `jacobian` | Robotics | J = ∂x/∂q (6×6 geometric Jacobian) | `crates/common/src/realism/laws/kinematics.rs` |
| `dynamic_model` | Robotics | τ = M(q)q̈ + C(q,q̇)q̇ + g(q) | `crates/common/src/realism/laws/kinematics.rs` |
| `conveyor_transport` | Material handling | x(t) = x₀ + v·t | `crates/common/src/realism/laws/kinematics.rs` |

### 6.2 Thermal Laws Reference

| Function | Domain | Formula | Crate Path |
|----------|--------|---------|-----------|
| `heat_conduction` | Thermodynamics | Q = k·A·ΔT/L (Fourier's law) | `crates/common/src/realism/laws/thermodynamics.rs` |
| `forced_convection` | Thermodynamics | Q = h·A·ΔT (Newton's cooling) | `crates/common/src/realism/laws/thermodynamics.rs` |
| `thermal_mass` | Thermodynamics | ΔT = Q/(m·c_p) | `crates/common/src/realism/laws/thermodynamics.rs` |
| `airflow_cooling` | Thermodynamics | Q = ṁ·c_p·ΔT (air mass flow) | `crates/common/src/realism/laws/thermodynamics.rs` |

### 6.3 Calibrated Constants

| Constant | Value | Unit | Usage |
|----------|-------|------|-------|
| Air density (25°C) | 1.184 | kg/m³ | Airflow cooling calculation |
| Air specific heat | 1,005 | J/(kg·K) | Airflow cooling calculation |
| Airflow rate (HEPA fans) | 0.139 | m³/s (500 m³/h) | Forced convection |
| Convection coefficient (forced air) | 25.0 | W/(m²·K) | Container surface cooling |
| Convection coefficient (natural) | 5.0 | W/(m²·K) | Idle/storage condition |
| Container surface area (internal) | 92.0 | m² | Heat rejection surface |
| Ambient temperature (reference) | 298.15 | K | 25°C standard |

---

## 7. Realism Config

```toml
[realism]
enabled = true
time_scale = 1.0
gravity = [0.0, -9.81, 0.0]
ambient_temperature = 298.15
ambient_pressure = 101325.0

[realism.features]
materials = true
thermodynamics = true
kinetics = true
structural = true

[realism.kinetics]
servo_cycle_ms = 1.0
motion_planning_hz = 200.0
vision_inference_hz = 20.0
force_control_hz = 1000.0

[realism.thermal]
cooling_mode = "forced_air"
airflow_rate_m3_per_s = 0.139
hepa_filter_class = "ISO_Class_8"
```

---

## 8. Structural Bundle Requirements

### 8.1 Components Table

| Component | Priority | Structural Role | Failure Mode |
|-----------|----------|----------------|--------------|
| Chassis | **Critical** | Primary load path; supports all subsystems + transport loads | Fatigue crack at weld joints |
| Robotic Arm (links) | **Critical** | Cantilevered payload; cyclic joint loading | Fatigue at joint housings |
| Conveyor Frame | High | Supports moving parts + workpieces | Deflection under load |
| Tool Magazine | Medium | Static storage; kinematic alignment | Misalignment from thermal expansion |
| Control Cabinet | Medium | Houses sensitive electronics | Vibration-induced connector failures |
| Vibration Mounts | **Critical** | Isolates cell from ground vibration | Mount fatigue → resonance |

### 8.2 Priority Notes

- **Chassis welds** are the single most fracture-critical feature. ISO 1496 requires proof loading at 1.8× gross weight. All longitudinal welds must be full-penetration, UT-inspected.
- **Arm joint housings** experience ~10⁸ load cycles over 80,000-hour MTBF. Harmonic drive housings are pre-qualified by vendor (FANUC/Yaskawa).
- **Vibration mounts** degrade with UV and ozone exposure. Replacement interval: 5 years or per condition monitoring.

---

## 9. Deployment Checklist

### 9.1 Copy Instructions

1. Copy all `.glb` mesh files from `docs/Products/V-Man/V1/meshes/` to:
   ```
   C:\Users\miksu\Documents\Eustress\Universe1\spaces\Space1\assets\meshes\products\V-Man\
   ```

2. Copy all `.glb.toml` instance files from `docs/Products/V-Man/V1/` to:
   ```
   C:\Users\miksu\Documents\Eustress\Universe1\spaces\Space1\Workspace\
   ```

### 9.2 Pre-Launch Checks

- [ ] All 12 `.glb.toml` files present in `Workspace/`
- [ ] All 12 `.glb` mesh files present in `assets/meshes/products/V-Man/`
- [ ] Every `[asset] mesh` path resolves to an existing `.glb` file
- [ ] Every `[transform]` uses meters (Y-up) — no studs, no centimeters
- [ ] Every `[properties] color` uses linear RGBA 0.0–1.0 — no sRGB 0–255
- [ ] Every `[metadata] class_name` is exactly `"Part"` or `"AdvancedPart"`
- [ ] Every `AdvancedPart` has `[material]` with 14 base fields
- [ ] Every `[material.custom]` has a `role` tag
- [ ] ISO 8601 timestamps in all `[metadata]`

### 9.3 Runtime Validation Sanity Checks

| Check | Expected Value | Tolerance |
|-------|---------------|-----------|
| Chassis density | 7,850 kg/m³ | ±50 |
| Arm material density | 2,810 kg/m³ | ±20 |
| Total heat generation at nominal load | ~3,000 W | ±500 |
| Chassis temperature at steady state (25°C ambient, forced air) | ~308 K (35°C) | ±5 K |
| Arm joint velocity (J1, max) | 200 °/s = 3.49 rad/s | ±0.1 rad/s |
| Conveyor belt speed (nominal) | 0.10 m/s | ±0.01 |
| OEE (target) | 0.85 | ±0.05 |
| Parts produced per 24h (V-Cell) | 7,200 | ±500 |

---

*End of EustressEngine Requirements*
