# VOLTEC V-PUMP — Modular Inline Vacuum-Assist Pipeline Pump Patent Specification

**Document Classification**: Voltec Internal — Patent Draft  
**Version**: 1.0  
**Date**: February 25, 2026  
**Inventors**: Voltec Advanced Energy Division  
**Status**: Pre-Filing Draft  

---

## Table of Contents

1. [Title of Invention](#1-title-of-invention)
2. [Abstract](#2-abstract)
3. [Field of Invention](#3-field-of-invention)
4. [Background](#4-background)
5. [Summary of Invention](#5-summary-of-invention)
6. [Detailed Description](#6-detailed-description)
7. [Pump Core — Multi-Stage Axial-Flow Impeller Architecture](#7-pump-core)
8. [Vacuum-Assist Priming System](#8-vacuum-assist-priming-system)
9. [Modular Flange Adapter System](#9-modular-flange-adapter-system)
10. [Structural Reinforcement & 1000-Year Design Life](#10-structural-reinforcement)
11. [Thermal Management & Bearing System](#11-thermal-management)
12. [V-Mind Control & Telemetry](#12-v-mind-control)
13. [Performance Specifications](#13-performance-specifications)
14. [Manufacturing Process](#14-manufacturing-process)
15. [Claims](#15-claims)
16. [EustressEngine Simulation Requirements](#16-eustressengine-simulation-requirements)

---

## 1. Title of Invention

**Modular Inline Vacuum-Assist Pump Unit for Continuous Long-Distance Water Transport with 1000-Year Design Life**

Short designation: **V-Pump**

---

## 2. Abstract

A modular inline pump unit designed for permanent installation in large-scale water transport pipelines, capable of boosting desalinated or fresh water over unlimited distances through relay-station architecture at intervals of ≤50 km. The invention combines:

1. **Multi-stage axial-flow impeller** with vacuum-assist priming that eliminates cavitation at any altitude or suction condition
2. **Universal flange adapter system** accepting pipe diameters from DN300 (12") to DN16000 (630") through a modular reducer/expander ring set
3. **Duplex stainless steel pressure casing** with ceramic-lined bore, designed for 1,000-year continuous service under sustained hydraulic loads
4. **V-Mind AI telemetry** providing real-time pump curve optimization, predictive bearing replacement, and network-wide hydraulic grade line management

The pump operates as a self-contained inline booster unit with automatic bypass on failure, enabling N+1 redundancy in relay chains. Each unit is made to order, sized to the pipeline diameter and flow requirements using the `garbongus` fluid mechanics library for exact hydraulic calculations.

**Primary Application**: Replenishing the Indo-Gangetic Basin aquifer (Uttar Pradesh) via 990 km desalinated seawater pipeline from the Bay of Bengal — generalizable to any continental-scale water transport project.

---

## 3. Field of Invention

The present invention relates to inline pipeline pump stations for long-distance water transport, specifically to modular vacuum-assist booster pump units designed for permanent installation in large-diameter pipelines serving continental-scale aquifer recharge, inter-basin water transfer, and desalination distribution systems.

---

## 4. Background

### 4.1 The Root Problem: Aquifer Collapse

The Indo-Gangetic Basin (IGB) aquifer — the world's most stressed — is losing approximately **15 km³/year** of groundwater. This aquifer supplies drinking water and irrigation for **600 million people** across Uttar Pradesh, Bihar, West Bengal, and neighboring states. At current depletion rates, large regions face permanent water table collapse within 20-40 years.

The only physical solution is **replacing what is taken**: continuously pumping desalinated seawater from the Bay of Bengal inland to recharge the aquifer at a rate exceeding depletion.

### 4.2 The Engineering Challenge

Moving water over 990 km against terrain requires overcoming:

| Challenge | Magnitude | Physics |
|-----------|-----------|---------|
| Elevation head | 300 m maximum (Raipur plateau) | P = ρ·g·h = 2,943,000 Pa (29.4 bar) |
| Friction loss | ~1,900 Pa/km in 16m pipe at 3 m/s | Darcy-Weisbach: f·(L/D)·(ρv²/2) |
| Total pump power | ~6 GW continuous | P_pump = ρ·g·Q·H/η |
| Cavitation risk | At every pump station | P_suction > P_vapor required |
| Service life | Must operate for centuries | Infrastructure is permanent |

### 4.3 Limitations of Current Technology

| Parameter | Conventional Booster | V-Pump Target |
|-----------|---------------------|---------------|
| Max pipe diameter | DN2000 (2m) | **DN16000 (16m)** |
| Design life | 25-40 years | **1,000 years** |
| Relay interval | 5-15 km | **≤50 km** |
| Priming method | External priming pump | **Integrated vacuum-assist** |
| Bypass on failure | Manual valve operation | **Automatic butterfly bypass** |
| Modularity | Fixed diameter | **Universal DN300-DN16000** |
| AI telemetry | None / basic SCADA | **V-Mind real-time optimization** |
| Cavitation protection | Operator-dependent | **Autonomous vacuum headroom** |

No existing inline pump product simultaneously achieves:
- Universal pipe diameter compatibility (DN300-DN16000)
- 1,000-year design life with field-replaceable internals
- Integrated vacuum-assist priming with cavitation elimination
- Automatic bypass for zero-downtime relay chains
- AI-optimized pump curve tracking

### 4.4 The Breakthrough

The V-Pump achieves this through four simultaneous innovations:

1. **Vacuum-assist priming module** — An integrated rotary vane vacuum pump evacuates the pump casing before main impeller start, ensuring NPSH_available always exceeds NPSH_required. Calculation per `garbongus::vacuum::VacuumLift`:

```
h_max_atm = (P_atm - P_vapor) / (ρ·g) ≈ 10.18 m at 20°C
P_pump_required = ρ·g·H + ΔP_friction + P_vapor - P_atm
```

With vacuum-assist, the suction side is pre-evacuated to ~5 kPa absolute, providing >95 kPa of additional NPSH — eliminating cavitation regardless of installation altitude.

2. **Modular flange adapter system** — Concentric reducer/expander rings bolt to the pump's fixed core housing, adapting from DN300 to DN16000 without changing the pump internals. Made-to-order ring sets are CNC-machined per customer pipeline diameter.

3. **Duplex stainless steel + ceramic bore** — The pressure casing uses UNS S32205 duplex stainless (590 MPa yield, excellent chloride resistance for desalinated water) with a reaction-bonded silicon carbide (RBSiC) bore liner — hardness 2800 HV, virtually zero erosion over millennia.

4. **V-Mind hydraulic network intelligence** — Each V-Pump unit reports real-time discharge pressure, flow rate, vibration spectrum, bearing temperature, and NPSH margin to V-Mind. The AI optimizes VFD speed across the entire relay chain to minimize total energy consumption while maintaining the hydraulic grade line above terrain at every point.

---

## 5. Summary of Invention

The V-Pump is a modular inline pipeline booster pump unit comprising:

| Component | Material | Function |
|-----------|----------|----------|
| **Pump Casing** | UNS S32205 Duplex Stainless Steel | Pressure containment, structural backbone |
| **Bore Liner** | Reaction-Bonded Silicon Carbide (RBSiC) | Erosion/corrosion protection, 1000-year wear surface |
| **Impeller Assembly** | Super Duplex (UNS S32750) | Multi-stage axial-flow, hydraulic energy transfer |
| **Drive Shaft** | 17-4 PH Stainless Steel (H900) | Torque transmission, fatigue-rated for 10¹⁰ cycles |
| **Bearing Cartridges** | SiC/SiC ceramic journal bearings | Water-lubricated, no oil seals, field-replaceable |
| **Vacuum-Assist Module** | 316L Stainless + PTFE vanes | Integrated priming, cavitation prevention |
| **Flange Adapters** | A694 F60 Duplex Forgings | Modular DN300-DN16000 diameter adaptation |
| **Bypass Valve** | Duplex Steel + Stellite 6 seats | Automatic butterfly valve for zero-downtime bypass |
| **Motor** | Permanent Magnet Synchronous (PMSM) | Direct-drive, IP68, VFD-controlled |
| **Control Module** | V-Mind AI + IEC 61131-3 PLC | Telemetry, optimization, predictive maintenance |
| **Status Array** | IP68 LED indicators | Visual pump health status |

---

## 6. Detailed Description

### 6.1 Overall Pump Architecture (Cross-Section — Axial View)

```
                    ┌─── BYPASS BUTTERFLY VALVE ───┐
                    │    (auto-open on pump fail)   │
                    │                               │
 ═══════════════════╪═══════════════════════════════╪═══════════════
 ║  FLANGE         ║                               ║  FLANGE      ║
 ║  ADAPTER        ║   ┌───────────────────────┐   ║  ADAPTER     ║
 ║  (inlet)        ║   │ PUMP CASING (Duplex)  │   ║  (outlet)    ║
 ║                 ║   │  ┌─────────────────┐  │   ║              ║
 ║  DN300─DN16000  ║   │  │ RBSiC BORE LINER│  │   ║ DN300─DN16000║
 ║  ───────────────╫───┤  │  ┌───────────┐  │  ├───╫──────────────║
 ║  FLOW ──────────╫──►│  │  │ IMPELLER  │  │  │──►╫──── FLOW ───║
 ║                 ║   │  │  │ STAGES    │  │  │   ║              ║
 ║                 ║   │  │  │ (3-stage) │  │  │   ║              ║
 ║                 ║   │  │  └─────┬─────┘  │  │   ║              ║
 ║                 ║   │  │        │SHAFT   │  │   ║              ║
 ║                 ║   │  └────────┼────────┘  │   ║              ║
 ║                 ║   │      ┌────┴────┐      │   ║              ║
 ║                 ║   │      │ BEARING │      │   ║              ║
 ║                 ║   │      │CARTRIDGE│      │   ║              ║
 ║                 ║   └──────┴─────────┴──────┘   ║              ║
 ║                 ║          │ MOTOR │             ║              ║
 ║                 ║          │ (PMSM)│             ║              ║
 ║                 ║          └───┬───┘             ║              ║
 ═══════════════════╪═════════════╪═════════════════╪═══════════════
                    │         ┌───┴───┐             │
                    │         │V-MIND │             │
                    │         │CONTROL│             │
                    │         └───┬───┘             │
                    │         ┌───┴───┐             │
                    │         │VACUUM │             │
                    │         │ASSIST │             │
                    │         └───────┘             │
                    └───────────────────────────────┘
```

### 6.2 Relay Station Architecture (Pipeline Profile)

```
         Desal Plant         Station 1          Station 2          Station N
         (0 km, 0m)          (50 km)            (100 km)           (N×50 km)
              │                  │                  │                  │
    ──────────┼──────────────────┼──────────────────┼──────────────────┼───►
              │     V-Pump       │     V-Pump       │     V-Pump       │
              │     ΔP=+25 bar   │     ΔP=+25 bar   │     ΔP=+25 bar   │
              │                  │                  │                  │
    HGL: ─────┼──────────\───────┼──────────\───────┼──────────\───────┼───
              │           \      │           \      │           \      │
              │    friction\     │    friction\     │    friction\     │
              │     loss    \    │     loss    \    │     loss    \    │
    Terrain:  ╔══════════════════╗                                     │
              ║   Raipur Plateau ║ (300m elevation)                    │
              ╚══════════════════╝                                     │

    Each V-Pump station boosts pressure by ~25 bar (250m head equivalent),
    compensating for ~50 km of friction loss + elevation changes.
    
    Total stations for 990 km IGBWP route: 20 stations (990/50 = 19.8)
    Plus 2 additional for elevation at Raipur: 22 stations total
```

### 6.3 Made-to-Order Sizing via garbongus

Every V-Pump unit is sized precisely for its installation using the `garbongus` fluid mechanics library:

```rust
use garbongus::{fluid::Fluid, flow, pipe::DarcyWeisbach, pipeline::Pipeline, vacuum::VacuumLift};

// Step 1: Define the fluid (desalinated water, ~2 ppt residual salinity, 25°C)
let fluid = Fluid::seawater(25.0, 2.0);

// Step 2: Size the pipe for target flow
let q_target = 595.0;  // m³/s — IGBWP requirement
let v_target = 3.0;    // m/s — design velocity
let diameter = flow::required_diameter(q_target, v_target); // ≈ 15.9 m

// Step 3: Calculate friction loss per 50 km relay segment
let dw = DarcyWeisbach::new(&fluid, diameter, 50_000.0, v_target, 1.5e-6);
let segment_loss = dw.calculate();
// segment_loss.pressure_loss_pa ≈ 950,000 Pa (9.5 bar)
// segment_loss.head_loss_m ≈ 96.8 m

// Step 4: Calculate pump power per station
let head_per_station = segment_loss.head_loss_m + 10.0; // friction + 10m safety margin
let pump = flow::pump_power(fluid.density_kg_m3, q_target, head_per_station, 0.88);
// pump.shaft_mw() ≈ 710 MW per station (for the full 595 m³/s flow)

// Step 5: Verify vacuum-assist priming headroom
let vac = VacuumLift::new(fluid, diameter / 2.0, 10.0)
    .flow_velocity(v_target)
    .roughness(1.5e-6)
    .calculate();
// vac.atmospheric_max_lift_m ≈ 10.18 m — vacuum-assist adds >95 kPa headroom
```

**Key insight**: The 595 m³/s flow in a 16m pipe is a massive infrastructure project. In practice, V-Pump units would be arrayed in **parallel banks** of smaller units (e.g., 20 × DN2000 pumps each handling ~30 m³/s) rather than a single DN16000 unit. The modular flange adapter system enables either configuration.

---

## 7. Pump Core — Multi-Stage Axial-Flow Impeller Architecture {#7-pump-core}

### 7.1 Design Rationale

Axial-flow impellers are selected over centrifugal for large-diameter, high-flow applications because:

1. **Lower specific speed** — Better efficiency at Q > 1 m³/s per impeller
2. **Inline flow path** — No volute casing required, enabling true inline installation
3. **Scalable** — Same impeller geometry scales from DN300 to DN2000+ with predictable performance
4. **Multi-stage** — 3 stages in series provide 25 bar total head at moderate blade loading

### 7.2 Impeller Geometry

```
    FLOW ────────────────────────────────────────────► FLOW
              │         │         │
         ┌────┴────┐┌───┴───┐┌───┴───┐
         │ STAGE 1 ││STAGE 2││STAGE 3│
         │  Guide  ││ Guide ││ Guide │
         │  Vanes  ││ Vanes ││ Vanes │
         │    +    ││   +   ││   +   │
         │ Rotor   ││ Rotor ││ Rotor │
         │ Blades  ││ Blades││ Blades│
         └────┬────┘└───┬───┘└───┬───┘
              │         │         │
              └─────────┴─────────┘
                    SHAFT
                      │
                   ┌──┴──┐
                   │MOTOR│
                   └─────┘

    Per stage:
    - 7 rotor blades (Super Duplex S32750)
    - 11 guide vanes (cast Duplex S32205)
    - Tip clearance: 0.3 mm (controlled by RBSiC wear ring)
    - Head per stage: ~8.3 bar (83 m water column)
    - Stage efficiency: 88-91%
```

### 7.3 Impeller Material Properties — Super Duplex UNS S32750

| Property | Value | Unit |
|----------|-------|------|
| Young's Modulus | 200 × 10⁹ | Pa |
| Poisson's Ratio | 0.30 | — |
| Yield Strength (0.2%) | 550 × 10⁶ | Pa |
| Ultimate Tensile Strength | 800 × 10⁶ | Pa |
| Fracture Toughness | 150 × 10⁶ | Pa·√m |
| Hardness | 310 | HV |
| Thermal Conductivity | 17.0 | W/(m·K) |
| Specific Heat | 480 | J/(kg·K) |
| Thermal Expansion | 13.0 × 10⁻⁶ | 1/K |
| Melting Point | 1623 | K |
| Density | 7,800 | kg/m³ |
| Friction Static | 0.45 | — |
| Friction Kinetic | 0.35 | — |
| Restitution | 0.3 | — |
| Pitting Resistance (PREN) | ≥40 | — |
| Fatigue Limit (10⁸ cycles) | 280 × 10⁶ | Pa |

### 7.4 Design for 1000-Year Fatigue

The impeller is the most fatigue-critical component. At 1,450 RPM:

```
Cycles per year = 1450 × 60 × 24 × 365 = 7.62 × 10⁸
Cycles in 1000 years = 7.62 × 10¹¹
```

This is far beyond the conventional S-N curve knee (10⁸ cycles). The design addresses this through:

1. **Conservative stress ratio** — Peak blade stress ≤ 40% of fatigue limit (σ_max ≤ 112 MPa)
2. **Shot peening** — Compressive residual stress of -400 MPa on blade surfaces
3. **Hot isostatic pressing (HIP)** — Eliminates internal porosity from casting
4. **Field-replaceable impeller cartridge** — Entire rotor assembly slides out axially; replacement interval 50-100 years based on V-Mind vibration trending

---

## 8. Vacuum-Assist Priming System {#8-vacuum-assist-priming-system}

### 8.1 The Cavitation Problem

Per `garbongus::vacuum`, atmospheric pressure can only lift water ~10.18 m at 20°C. At pump stations elevated above the upstream water level, or after pipeline drainage for maintenance, the pump casing may be empty. Starting a dry pump destroys seals and bearings.

### 8.2 Solution: Integrated Vacuum-Assist

A rotary vane vacuum pump mounted to the control module evacuates the pump casing to <5 kPa absolute before main motor start:

```
Sequence:
1. Bypass valve OPEN (pipeline flow continues through bypass)
2. Vacuum pump starts → evacuates pump casing to 5 kPa
3. Water rises into casing via atmospheric pressure differential:
   h_fill = (P_atm - P_casing) / (ρ·g) = (101325 - 5000) / (998×9.81) ≈ 9.83 m
4. Casing flooded → pressure transducer confirms water presence
5. Main motor starts at 10% speed via VFD
6. NPSH verified > NPSH_required + 3m safety margin
7. VFD ramps to target speed over 60 seconds
8. Bypass valve CLOSED → pump takes full pipeline load
```

### 8.3 Vacuum Module Specifications

| Parameter | Value |
|-----------|-------|
| Type | Oil-free rotary vane |
| Ultimate vacuum | 2 kPa absolute |
| Pumping speed | 40 m³/h |
| Motor | 2.2 kW, 400V 3-phase |
| Material (body) | 316L Stainless Steel |
| Material (vanes) | PTFE composite |
| Weight | 85 kg |
| Design life | 50,000 hours (replaceable unit) |

### 8.4 NPSH Calculation per garbongus

```rust
use garbongus::{fluid::Fluid, vacuum::VacuumLift};

let fluid = Fluid::water(25.0);  // 25°C service temperature

// Case: pump at 5m above water level, with vacuum assist
let vac = VacuumLift::new(fluid, 0.5, 5.0)
    .flow_velocity(3.0)
    .roughness(1.5e-6)
    .ambient_pressure(101_325.0)
    .calculate();

// NPSH_available = (P_atm + P_vacuum_assist - P_vapor) / (ρ·g) - h_suction - h_friction
// With vacuum assist: P_vacuum_assist provides additional 96 kPa
// NPSH_available ≈ 14.7 m >> NPSH_required (typically 3-5 m)
```

---

## 9. Modular Flange Adapter System {#9-modular-flange-adapter-system}

### 9.1 Design Philosophy

The V-Pump core is manufactured in **four standard frame sizes**. Flange adapter rings adapt the core to any pipeline diameter:

| Frame | Core Bore | Pipe Range | Typical Application |
|-------|-----------|------------|---------------------|
| **VP-S** | DN500 | DN300 – DN800 | Municipal distribution, irrigation |
| **VP-M** | DN1200 | DN800 – DN2000 | Regional trunk lines, industrial |
| **VP-L** | DN2500 | DN2000 – DN4000 | Inter-basin transfer, desal mains |
| **VP-XL** | DN5000 | DN4000 – DN16000 | Continental-scale (IGBWP class) |

### 9.2 Adapter Ring Construction

```
    PIPELINE (DN_customer)           PUMP CORE (DN_frame)
    ┌──────────────────┐            ┌──────────────┐
    │                  │            │              │
    │                  │◄── ADAPTER ──►            │
    │    LARGE BORE    │   RING SET │  CORE BORE   │
    │                  │  (conical  │              │
    │                  │  reducer)  │              │
    └──────────────────┘            └──────────────┘

    Adapter ring: A694 F60 Duplex forging
    - CNC-machined conical bore with smooth transition
    - ASME B16.47 Series B bolt pattern (inlet/outlet)
    - Spiral-wound gaskets (316L/graphite)
    - Hydraulic studs for field installation
```

### 9.3 Flange Adapter Material — A694 F60 Duplex Forging

| Property | Value | Unit |
|----------|-------|------|
| Young's Modulus | 200 × 10⁹ | Pa |
| Poisson's Ratio | 0.30 | — |
| Yield Strength | 450 × 10⁶ | Pa |
| Ultimate Strength | 620 × 10⁶ | Pa |
| Fracture Toughness | 120 × 10⁶ | Pa·√m |
| Hardness | 260 | HV |
| Thermal Conductivity | 17.0 | W/(m·K) |
| Specific Heat | 480 | J/(kg·K) |
| Thermal Expansion | 13.0 × 10⁻⁶ | 1/K |
| Melting Point | 1623 | K |
| Density | 7,800 | kg/m³ |
| Friction Static | 0.45 | — |
| Friction Kinetic | 0.35 | — |
| Restitution | 0.3 | — |

---

## 10. Structural Reinforcement & 1000-Year Design Life {#10-structural-reinforcement}

### 10.1 Design Philosophy

Infrastructure is permanent. The Appian Way (312 BC) still stands after 2,300 years. Roman aqueducts delivered water for 500+ years. V-Pump is designed to the same standard: **the structure must outlast civilizations**.

The 1,000-year design life target is achieved through:

1. **Material selection** — Duplex stainless steel resists chloride-induced stress corrosion cracking (SCC), the #1 killer of conventional pump casings in desalinated water service
2. **Ceramic bore** — RBSiC has hardness 2800 HV vs 310 HV for the steel casing. Erosion rate: <0.001 mm/year at 3 m/s water velocity → <1 mm total wear in 1000 years
3. **Field-replaceable internals** — Impeller, bearings, seals, and motor are cartridge-style, removable without cutting the pipeline. Only the casing and bore liner are permanent.
4. **Cathodic protection** — Sacrificial zinc anodes on external surfaces; impressed current system for buried installations

### 10.2 Pump Casing — UNS S32205 Duplex Stainless Steel

| Property | Value | Unit |
|----------|-------|------|
| Young's Modulus | 200 × 10⁹ | Pa |
| Poisson's Ratio | 0.30 | — |
| Yield Strength | 450 × 10⁶ | Pa |
| Ultimate Strength | 620 × 10⁶ | Pa |
| Fracture Toughness | 200 × 10⁶ | Pa·√m |
| Hardness | 290 | HV |
| Thermal Conductivity | 19.0 | W/(m·K) |
| Specific Heat | 500 | J/(kg·K) |
| Thermal Expansion | 13.0 × 10⁻⁶ | 1/K |
| Melting Point | 1673 | K |
| Density | 7,800 | kg/m³ |
| Friction Static | 0.45 | — |
| Friction Kinetic | 0.35 | — |
| Restitution | 0.3 | — |
| Chloride SCC Threshold | >250°C | (immune at water temps) |
| Crevice Corrosion (PREN) | 35 | — |

### 10.3 Bore Liner — Reaction-Bonded Silicon Carbide (RBSiC)

| Property | Value | Unit |
|----------|-------|------|
| Young's Modulus | 380 × 10⁹ | Pa |
| Poisson's Ratio | 0.17 | — |
| Compressive Strength | 3,000 × 10⁶ | Pa |
| Flexural Strength | 400 × 10⁶ | Pa |
| Fracture Toughness | 4.0 × 10⁶ | Pa·√m |
| Hardness | 2,800 | HV |
| Thermal Conductivity | 120 | W/(m·K) |
| Specific Heat | 680 | J/(kg·K) |
| Thermal Expansion | 4.0 × 10⁻⁶ | 1/K |
| Melting Point | 2,730 | K |
| Density | 3,100 | kg/m³ |
| Friction Static | 0.20 | — |
| Friction Kinetic | 0.15 | — |
| Restitution | 0.5 | — |
| Erosion Rate (water, 3 m/s) | <0.001 | mm/year |

### 10.4 Stress Analysis — Pressure Containment

Design pressure: 40 bar (4.0 MPa) — 1.6× safety factor over 25 bar operating

```
Wall thickness (Barlow's formula):
t = P·D / (2·S·E)
  = 4.0e6 × 1.2 / (2 × 450e6 × 0.85)
  = 6.27 mm minimum

Design wall thickness: 25 mm (safety factor 4.0×)
```

At 25 mm wall, hoop stress at 40 bar in DN1200 casing:

```
σ_hoop = P·D / (2·t) = 4.0e6 × 1.2 / (2 × 0.025) = 96 MPa
Safety factor = 450 / 96 = 4.7× (exceeds ASME VIII Div 1 requirement of 3.5×)
```

### 10.5 Seismic Loading

For permanent buried infrastructure, seismic design per ASCE 7-22:

| Seismic Zone | Peak Ground Accel. | Design Response |
|--------------|-------------------|-----------------|
| Zone 1 (Low) | 0.1g | No special requirements |
| Zone 2 (Moderate) | 0.2g | Flexible pipe joints at pump stations |
| Zone 3 (High) | 0.4g | Isolation mounts + expansion joints |
| Zone 4 (Severe) | 0.6g | Base isolation + seismic shut-off valves |

V-Pump stations include seismic accelerometer input to V-Mind; automatic shutdown if PGA > 0.3g.

---

## 11. Thermal Management & Bearing System {#11-thermal-management}

### 11.1 Water-Lubricated Ceramic Bearings

Conventional pump bearings use oil lubrication with mechanical shaft seals — the #1 maintenance item and the first component to fail. V-Pump eliminates this entirely:

| Parameter | Conventional | V-Pump |
|-----------|-------------|--------|
| Bearing type | Steel roller, oil-lubricated | SiC/SiC ceramic journal |
| Lubrication | Oil (requires seals) | Process water (seal-less) |
| Shaft seal | Mechanical face seal | None required |
| Replacement interval | 2-5 years | 50-100 years |
| Failure mode | Seal leak → bearing failure | Vibration trending → planned replacement |

### 11.2 Bearing Material — Silicon Carbide (SiC/SiC)

| Property | Value | Unit |
|----------|-------|------|
| Young's Modulus | 410 × 10⁹ | Pa |
| Poisson's Ratio | 0.14 | — |
| Compressive Strength | 3,900 × 10⁶ | Pa |
| Flexural Strength | 550 × 10⁶ | Pa |
| Fracture Toughness | 4.5 × 10⁶ | Pa·√m |
| Hardness | 2,800 | HV |
| Thermal Conductivity | 120 | W/(m·K) |
| Specific Heat | 680 | J/(kg·K) |
| Thermal Expansion | 4.0 × 10⁻⁶ | 1/K |
| Max Service Temp | 1,650 | K |
| Density | 3,210 | kg/m³ |
| Friction (water-lubricated) | 0.05 | — |
| PV Limit | 100 | MPa·m/s |
| Wear Rate | <10⁻⁸ | mm³/(N·m) |

### 11.3 Heat Dissipation

Motor waste heat (~5% of shaft power) is absorbed by the process water flow:

```
For a VP-M unit (500 kW motor):
Q_waste = 0.05 × 500,000 = 25,000 W
Water flow through motor jacket: 2 L/s
ΔT = Q / (ṁ·c_p) = 25,000 / (2 × 4,186) = 3.0°C
```

Negligible temperature rise. No external cooling required.

---

## 12. V-Mind Control & Telemetry {#12-v-mind-control}

### 12.1 Per-Unit Sensors

| Sensor | Measurement | Purpose |
|--------|-------------|---------|
| Discharge pressure (PT) | 0-60 bar, ±0.1% | Pump curve tracking |
| Suction pressure (PT) | -1 to 40 bar, ±0.1% | NPSH monitoring |
| Flow rate (EM) | Electromagnetic, ±0.5% | Volume accounting |
| Vibration (3-axis) | 0-20 kHz, ±1% | Bearing condition |
| Bearing temperature (RTD) | PT100, ±0.1°C | Thermal trending |
| Motor current (CT) | ±0.5% | Power monitoring |
| Motor winding temp (RTD) | PT100, ±0.1°C | Thermal protection |
| Vacuum pressure (PT) | 0-200 kPa abs | Priming verification |

### 12.2 Network-Wide Optimization

V-Mind connects all V-Pump units in a relay chain and optimizes the **hydraulic grade line** (HGL) across the entire pipeline:

```
Objective: Minimize Σ(P_pump_i × Q_i / η_i) subject to:
  - HGL > terrain + 10m at every point
  - NPSH_available > NPSH_required + 3m at every station
  - Flow velocity 2.0 < v < 4.0 m/s (avoid sedimentation / erosion)
  - VFD speed range 30-100% of rated

Algorithm: Model Predictive Control (MPC) with 15-minute horizon
  - State: [P_1, P_2, ..., P_n, Q, T_bearing_1, ..., T_bearing_n]
  - Control: [RPM_1, RPM_2, ..., RPM_n]
  - Constraint: terrain profile + pipeline hydraulics (Darcy-Weisbach)
```

### 12.3 Control Module Hardware

| Component | Specification |
|-----------|---------------|
| Processor | ARM Cortex-A72, 1.5 GHz |
| OS | V-OS (real-time, Rust-based) |
| Communication | Fiber optic + 4G/5G cellular backup |
| Protocol | Modbus TCP/IP + MQTT for V-Mind cloud |
| Enclosure | IP68, NEMA 4X, 316L stainless |
| Power | 24 VDC from pump UPS |
| Display | 7" capacitive touchscreen |

---

## 13. Performance Specifications {#13-performance-specifications}

### 13.1 Frame Size Performance Matrix

| Parameter | VP-S | VP-M | VP-L | VP-XL |
|-----------|------|------|------|-------|
| Core bore | DN500 | DN1200 | DN2500 | DN5000 |
| Pipe range | DN300-800 | DN800-2000 | DN2000-4000 | DN4000-16000 |
| Max flow | 1.5 m³/s | 15 m³/s | 80 m³/s | 600 m³/s |
| Max head | 300 m | 250 m | 200 m | 150 m |
| Stages | 3 | 3 | 3 | 3 |
| Motor power | 50-500 kW | 500-5,000 kW | 5-50 MW | 50-500 MW |
| Weight (dry) | 2,500 kg | 15,000 kg | 85,000 kg | 500,000 kg |
| Overall length | 2.0 m | 4.5 m | 8.0 m | 15.0 m |
| Overall diameter | 1.2 m | 2.5 m | 5.0 m | 8.0 m |
| Design life (casing) | 1,000 years | 1,000 years | 1,000 years | 1,000 years |
| Bearing replacement | 50-100 years | 50-100 years | 50-100 years | 50-100 years |
| Impeller replacement | 100-200 years | 100-200 years | 100-200 years | 100-200 years |

### 13.2 Efficiency

| Operating Point | Efficiency |
|----------------|------------|
| BEP (Best Efficiency Point) | 88-91% |
| 75% BEP flow | 82-85% |
| 50% BEP flow | 70-75% |
| VFD range | 30-100% speed |

### 13.3 IGBWP Application Sizing

For the 990 km Indo-Gangetic Basin Water Project:

```
Pipeline diameter: 16 m (per garbongus::flow::required_diameter(595.0, 3.0))
Flow rate: 595 m³/s
Velocity: 3.0 m/s

Configuration: 10 parallel banks × 60 m³/s each
  Each bank: 3 × VP-XL in series (for 250m total head per bank)
  Total units: 10 × 3 = 30 VP-XL units per station
  Total stations: 22 (990 km / 50 km + 2 for Raipur plateau)
  Total V-Pump units: 22 × 30 = 660 VP-XL units

Power per station: 660 MW (30 × 22 MW each)
Total pipeline pump power: 14.5 GW
Annual energy: 127 TWh
Annual energy cost (at $0.05/kWh): $6.35 billion

Unit cost estimate (VP-XL): $2.5 million each
Total V-Pump hardware: $1.65 billion
  (vs $70-120B total project cost — pumps are <2.5% of total)
```

### 13.4 Generalized Sizing Formula

For any project, the number of V-Pump stations is:

```
N_stations = ceil(L_pipeline / L_relay) + ceil(H_max_elevation / H_per_station)

Where:
  L_pipeline = total pipeline length (m)
  L_relay = relay interval (default 50,000 m)
  H_max_elevation = maximum elevation gain (m)
  H_per_station = head per pump station (m) — typically 250 m for VP-XL
```

---

## 14. Manufacturing Process {#14-manufacturing-process}

### 14.1 Process Comparison

| Step | Conventional Pump | V-Pump |
|------|------------------|--------|
| Casing | Sand casting, carbon steel | Investment casting, duplex SS + HIP |
| Bore | Machined steel | Shrink-fit RBSiC liner, precision ground |
| Impeller | Sand cast, machined | Investment cast Super Duplex + HIP + shot peen |
| Bearings | Steel roller + oil seals | SiC/SiC ceramic journals, water-lubricated |
| Assembly | Manual, site-specific | Cartridge design, factory-assembled modules |
| Testing | Hydrostatic only | Hydrostatic + dynamic + vibration signature baseline |

### 14.2 Production Line Steps

1. **Casing forging** — Duplex S32205 ring forging on 10,000-ton press → solution anneal 1050°C → water quench
2. **Casing machining** — CNC boring to ±0.05 mm, bolt hole drilling, flange facing
3. **Bore liner installation** — RBSiC sleeve shrink-fit at +200°C interference fit
4. **Impeller casting** — Super Duplex S32750 investment cast → HIP at 1100°C/100 MPa → CNC 5-axis finish
5. **Shot peening** — Impeller blades peened to -400 MPa compressive residual stress
6. **Shaft manufacture** — 17-4 PH bar stock → CNC turning → H900 age-hardening → grinding to ±0.01 mm
7. **Bearing cartridge assembly** — SiC journal + SiC sleeve + 316L housing → interference fit
8. **Motor integration** — PMSM stator installed in casing rear section, rotor on shaft
9. **Flange adapter machining** — Made-to-order from F60 forging, CNC to customer DN
10. **Factory acceptance test** — Full-speed water test, vibration baseline, performance curve mapping
11. **Packaging** — Nitrogen-blanketed, corrosion-inhibited, shipping cradle

### 14.3 Production Targets

| Year | Units/Year | Revenue Target | Target Customers |
|------|-----------|----------------|-----------------|
| Year 1 | 50 | $50M | Municipal water authorities, desal plants |
| Year 3 | 500 | $400M | Regional water transfer projects |
| Year 5 | 2,000 | $2B+ | IGBWP, China South-North, California Aqueduct |

### 14.4 Economies of Scale

| Volume | Unit Cost (VP-M) | Unit Cost (VP-XL) |
|--------|-----------------|-------------------|
| 1-10 | $450K | $3.5M |
| 10-100 | $300K | $2.5M |
| 100-1000 | $200K | $1.8M |
| 1000+ | $150K | $1.2M |

At IGBWP scale (660 units), the per-unit cost drops to $1.2M — total hardware cost $792M, less than 1.2% of the $70B+ project budget.

---

## 15. Claims {#15-claims}

**Claim 1** (Independent): A modular inline pump unit for installation in a water transport pipeline, comprising:
- (a) a duplex stainless steel pressure casing with an internal reaction-bonded silicon carbide bore liner;
- (b) a multi-stage axial-flow impeller assembly mounted on a drive shaft within said bore liner;
- (c) water-lubricated silicon carbide journal bearings supporting said drive shaft;
- (d) an integrated vacuum-assist priming module capable of evacuating the pump casing to less than 5 kPa absolute;
- (e) a modular flange adapter system comprising removable conical reducer rings enabling connection to pipelines of any diameter from DN300 to DN16000;
- (f) an automatic butterfly bypass valve enabling pipeline flow continuity during pump shutdown; and
- (g) an electronic control module running V-Mind AI software providing real-time pump curve optimization and predictive maintenance.

**Claim 2**: The pump unit of Claim 1, wherein the pressure casing is manufactured from UNS S32205 duplex stainless steel with a minimum yield strength of 450 MPa and a pitting resistance equivalent number (PREN) of at least 35.

**Claim 3**: The pump unit of Claim 1, wherein the silicon carbide bore liner has a Vickers hardness of at least 2,500 HV and an erosion rate of less than 0.001 mm/year at water velocities up to 5 m/s.

**Claim 4**: The pump unit of Claim 1, wherein the impeller assembly comprises three axial-flow stages, each stage comprising a rotor with 7 blades and a stator with 11 guide vanes, manufactured from UNS S32750 super duplex stainless steel subjected to hot isostatic pressing and shot peening.

**Claim 5**: The pump unit of Claim 1, wherein the vacuum-assist priming module is an oil-free rotary vane vacuum pump achieving ultimate vacuum of less than 5 kPa absolute, enabling priming of the pump casing from dry condition without external priming systems.

**Claim 6**: The pump unit of Claim 1, wherein the modular flange adapter system comprises concentric reducer rings manufactured from ASTM A694 Grade F60 duplex stainless steel forgings, each ring set CNC-machined to a specific pipeline diameter and bolted to the pump casing using ASME B16.47 Series B bolt patterns.

**Claim 7**: The pump unit of Claim 1, configured for relay-station operation in a pipeline of length L, wherein pump units are spaced at intervals of not more than 50 km, each unit providing sufficient head to overcome friction losses and elevation changes within its relay segment.

**Claim 8**: The pump unit of Claim 7, wherein the electronic control module communicates with other pump units in the relay chain via fiber optic communication, and a network-level model predictive controller optimizes the rotational speed of each pump to minimize total energy consumption while maintaining a hydraulic grade line above terrain elevation plus a minimum safety margin at every point.

**Claim 9**: The pump unit of Claim 1, wherein the silicon carbide journal bearings are lubricated by the process water being pumped, eliminating the need for oil lubrication systems and mechanical shaft seals.

**Claim 10**: A method of sizing a modular inline pump unit for a water transport project, comprising:
- (a) determining the required flow rate Q from the water demand and recharge efficiency using Q = V_loss / (η_recharge × T);
- (b) calculating the required pipe diameter D from Q and a target velocity v using D = 2√(Q/(v·π));
- (c) calculating friction head loss per relay segment using the Darcy-Weisbach equation;
- (d) determining the number of relay stations as N = ceil(L/L_relay) + ceil(H_max/H_station);
- (e) selecting a pump frame size from the modular range (VP-S, VP-M, VP-L, VP-XL) based on the flow rate; and
- (f) manufacturing custom flange adapter rings for the calculated pipe diameter D.

**Claim 11**: The pump unit of Claim 1, having a design life of at least 1,000 years for the pressure casing and bore liner, with field-replaceable impeller, bearing, and motor cartridges having replacement intervals of 50-200 years.

**Claim 12**: The pump unit of Claim 1, further comprising seismic sensors and automatic shutdown logic, wherein the control module initiates controlled shutdown if measured peak ground acceleration exceeds 0.3g.

---

## 16. EustressEngine Simulation Requirements {#16-eustressengine-simulation-requirements}

### 16.1 Component → ECS Mapping

| Component | class_name | Domain State | Laws |
|-----------|------------|-------------|------|
| Pump Casing | AdvancedPart | ThermodynamicState | Thermodynamics |
| Bore Liner | AdvancedPart | ThermodynamicState | Thermodynamics |
| Impeller Assembly | AdvancedPart | FluidState + KineticState | Fluid Dynamics |
| Drive Shaft | AdvancedPart | KineticState | Mechanics |
| Bearing Cartridges | AdvancedPart | ThermodynamicState | Thermodynamics |
| Vacuum-Assist Module | Part | — | — |
| Flange Adapters | Part | — | — |
| Bypass Valve | Part | FluidState | Fluid Dynamics |
| Motor (PMSM) | AdvancedPart | KineticState | Electrodynamics |
| Control Module | Part | — | — |
| Status Array | Part | — | — |

### 16.2 Required Realism Properties

| Property | Source | SI Unit |
|----------|--------|---------|
| Flow rate (Q) | `garbongus::flow` | m³/s |
| Discharge pressure | `garbongus::pipe` | Pa |
| Suction pressure | `garbongus::vacuum` | Pa |
| Friction loss | `garbongus::pipe::DarcyWeisbach` | Pa |
| Pump power | `garbongus::flow::pump_power` | W |
| NPSH available | `garbongus::vacuum::VacuumResult` | m |
| Reynolds number | `garbongus::pipe::PipeFlowResult` | — |
| Water density | `garbongus::fluid::Fluid` | kg/m³ |
| Water viscosity | `garbongus::fluid::Fluid` | Pa·s |
| Hydraulic grade line | `garbongus::pipeline::Pipeline` | m |

### 16.3 Cross-Reference

- Full material property blocks: see `EustressEngine_Requirements.md`
- Validation targets: see `SOTA_VALIDATION.md`
- 3D mesh generation: see `V1/meshes/scripts/`
