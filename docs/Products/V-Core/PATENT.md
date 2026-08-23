# VOLTEC V-CORE — Residential Micro-Nuclear Reactor Patent Specification

**Document Classification**: Voltec Internal — Patent Draft  
**Version**: 1.0  
**Date**: March 6, 2026  
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
7. [Core Technology: U-ZrH Fuel System](#7-core-technology-u-zrh-fuel-system)
8. [Core Technology: Heat Pipe Thermal Transport](#8-core-technology-heat-pipe-thermal-transport)
9. [Core Technology: Stirling Power Conversion](#9-core-technology-stirling-power-conversion)
10. [Core Technology: Reactivity Control](#10-core-technology-reactivity-control)
11. [Radiation Shielding](#11-radiation-shielding)
12. [Thermal Management](#12-thermal-management)
13. [Geometry & Mechanical Design](#13-geometry--mechanical-design)
14. [Performance Specifications](#14-performance-specifications)
15. [Manufacturing Process](#15-manufacturing-process)
16. [Claims](#16-claims)
17. [EustressEngine Simulation Requirements](#17-eustressengine-simulation-requirements)

---

## 1. Title of Invention

**Passively Safe Residential Micro-Nuclear Reactor with Uranium Zirconium Hydride Fuel, Alkali Metal Heat Pipes, and Free-Piston Stirling Power Conversion**

Short designation: **V-Core**

---

## 2. Abstract

A table-sized micro-nuclear fission reactor producing 25 kW electrical and 75 kW thermal continuous power from a sealed uranium zirconium hydride (U-ZrH₁.₆) fuel core with a 10-year refueling interval. The reactor combines:

1. **TRIGA-heritage U-ZrH₁.₆ fuel** with inherent prompt negative temperature coefficient of reactivity, providing walk-away safety without operator intervention or active cooling
2. **Sodium heat pipe thermal transport** — zero moving parts, passive two-phase heat removal from core to power conversion system
3. **Free-piston Stirling engine** power conversion achieving 30–35% thermal-to-electric efficiency with no rotating shafts, no lubricants, and 100,000-hour design life
4. **Boron carbide (B₄C) rotating control drums** for reactivity management — fail-safe by gravity to shutdown position
5. **Lead-polyethylene-boron composite shielding** reducing surface dose rate to <0.25 mR/hr (below residential background) at 1 meter

The V-Core is designed to be factory-sealed, truck-delivered, and installed on a concrete pad with no on-site nuclear assembly. Spent fuel is returned to the factory in the sealed vessel after the 10-year fuel cycle. Vortex AI provides continuous autonomous monitoring, load-following, and NRC telemetry compliance.

---

## 3. Field of Invention

The present invention relates to compact nuclear fission reactors for residential and light commercial distributed power generation, specifically to passively safe micro-reactors using uranium zirconium hydride fuel with heat pipe cooling and Stirling engine power conversion, designed for autonomous unattended operation with remote monitoring.

---

## 4. Background

### 4.1 Limitations of Current Technology

| Feature | Diesel Generator | Rooftop Solar + Battery | Natural Gas CHP | **V-Core** |
|---------|-----------------|------------------------|-----------------|------------|
| Continuous Power | 5–25 kW | 0–10 kW (intermittent) | 1–25 kW | 25 kW |
| Capacity Factor | 90% (fuel-dependent) | 15–25% | 85% | 95% |
| Fuel Supply | Diesel delivery | None (sunlight) | Gas pipeline | None (10 years sealed) |
| Noise | 65–85 dB | 0 dB | 45–55 dB | <40 dB |
| Emissions | CO₂, NOx, PM | None | CO₂, NOx | None |
| Runtime Before Refuel | 24–72 hr | N/A | Continuous (pipeline) | 87,600 hr (10 years) |
| Footprint | 2–4 m² | 30–100 m² (roof) | 1–3 m² | 0.48 m² |
| Capital Cost | $5,000–25,000 | $30,000–80,000 | $15,000–50,000 | $150,000–250,000 target |
| Fuel Cost (10 yr) | $100,000–300,000 | $0 | $50,000–150,000 | $0 (sealed) |
| Total Cost of Ownership (10 yr) | $120,000–350,000 | $30,000–80,000 | $65,000–200,000 | $150,000–250,000 |

### 4.2 The Problem

Reliable, continuous, fuel-independent residential power remains unsolved. Solar is intermittent and requires massive battery banks for 24/7 coverage. Diesel generators require fuel deliveries and produce emissions. Natural gas depends on pipeline infrastructure. Grid reliability is declining — the average US customer experienced 8.1 hours of outages in 2023 (EIA), with some regions exceeding 48 hours during extreme weather.

The ideal residential power source would:
- Produce 10–25 kW continuous (whole-home including HVAC, EV charging)
- Require zero fuel deliveries for 10+ years
- Produce zero emissions and zero noise
- Fit in a garage or backyard pad
- Operate autonomously with no human intervention
- Be inherently safe (no meltdown scenario possible)

### 4.3 The Breakthrough

V-Core achieves this by combining three proven technologies at residential scale:

- **U-ZrH₁.₆ fuel** (TRIGA heritage, 60+ years of safe operation, 66 reactors built worldwide) provides inherent passive safety — the fuel itself moderates the chain reaction and self-limits temperature rise with a prompt negative coefficient of -$1.0 × 10⁻⁴ Δk/k/°C
- **Sodium heat pipes** (Kilopower/KRUSTY heritage, successfully tested by NASA/LANL in 2018) provide passive, zero-moving-part thermal transport from core to power conversion
- **Free-piston Stirling engines** (Sunpower/Infinia heritage, 100,000+ hour demonstrated life) convert heat to electricity with no rotating shafts, no lubricants, and no wear surfaces

No individual technology is new. The innovation is the integrated residential package with factory-sealed construction, Vortex autonomous monitoring, and a regulatory pathway targeting NRC 10 CFR Part 53 (advanced reactor licensing).

---

## 5. Summary of Invention

### 5.1 Component List

| # | Component | Material | Mass (kg) | Role |
|---|-----------|----------|-----------|------|
| 1 | Reactor Vessel | 316L Stainless Steel | 85.0 | Primary containment, pressure boundary |
| 2 | Fuel Assembly | U-ZrH₁.₆ (19.75% LEU) | 42.0 | Nuclear fuel + moderator |
| 3 | Reflector Assembly | Beryllium Oxide (BeO) | 38.0 | Neutron reflector |
| 4 | Control Drum Assembly | B₄C absorber + SS304 drum body (6 drums) | 24.0 | Reactivity control |
| 5 | Heat Pipe Bundle | Sodium-charged Inconel 718 (12 pipes) | 18.0 | Passive core → hot-side thermal transport |
| 6 | Stirling Engine Assembly | Maraging 350 steel + helium working fluid (2 units) | 65.0 | Thermal-to-electric power conversion |
| 7 | Hot-Side Heat Exchanger | Inconel 718 | 12.0 | Heat pipe → Stirling interface |
| 8 | Cold-Side Radiator | Aluminum 6061-T6 + copper tubing | 35.0 | Stirling cold-side heat rejection |
| 9 | Biological Shield | Lead-polyethylene-boron composite | 280.0 | Gamma + neutron shielding to <0.25 mR/hr |
| 10 | Outer Casing | 304 Stainless Steel | 45.0 | Structural enclosure, seismic restraint |
| 11 | V-Cell Buffer | Na-S solid state (2 × V-Cell modules) | 18.5 | 16.7 kWh buffer, startup/transient/blackstart |
| 12 | Control Module | 316L SS enclosure + NVIDIA Orin | 8.0 | Vortex AI, NRC telemetry, load-following |
| 13 | Electrical Converter | SiC inverter + transformer | 22.0 | DC → 240 VAC split-phase, grid tie/island |
| 14 | Status Array | Polycarbonate + LED array | 0.5 | External status indicators |
| | **TOTAL** | | **~693 kg** | *Egg-shaped, table-sized form factor* |

### 5.2 System Architecture

```
                    ┌─────────────────┐
                    │   Vortex AI     │  NVIDIA Orin, Rust-native
                    │   Control       │  NRC telemetry, load-following
                    └───────┬─────────┘
                            │
            ┌───────────────┼───────────────┐
            ▼               ▼               ▼
    ┌──────────────┐ ┌────────────┐ ┌──────────────┐
    │  6 × Control │ │ 12 × Na    │ │  2 × V-Cell  │
    │  Drums (B₄C) │ │ Heat Pipes │ │  Buffer      │
    │  Reactivity  │ │ Passive    │ │  16.7 kWh    │
    └──────┬───────┘ └─────┬──────┘ └──────┬───────┘
           │               │               │
           ▼               ▼               ▼
    ┌──────────────────────────────┐ ┌──────────────┐
    │  U-ZrH₁.₆ Fuel Assembly    │ │  SiC Power   │
    │  75 kW thermal              │ │  Converter   │
    │  10-year sealed core        │ │  240 VAC     │
    └──────────────────────────────┘ └──────────────┘
                    │
            ┌───────┴───────┐
            ▼               ▼
    ┌──────────────┐ ┌──────────────┐
    │  2 × Stirling│ │  Cold-Side   │
    │  Engines     │ │  Radiator    │
    │  25 kW elec  │ │  50 kW heat  │
    └──────────────┘ └──────────────┘
```

---

## 6. Detailed Description

### 6.1 Cross-Section (Vertical, through centerline)

```
                    ▲ Y (up)
                    │
          ┌─────────────────────┐ ─── Status Array (top)
          │    ░░░░░░░░░░░░░    │
          │  ┌───────────────┐  │ ─── Control Module
          │  │  Vortex  SiC  │  │
          │  └───────────────┘  │
         ╱│                     │╲
        ╱ │  ┌───────────────┐  │ ╲
       ╱  │  │   Stirling    │  │  ╲ ─── Stirling Engines (×2)
      ╱   │  │   Engines     │  │   ╲
     ╱    │  └───┬───────┬───┘  │    ╲
    ╱     │  ┌───┴───┐   │     │     ╲
   │      │  │ Hot HX │   │     │      │
   │      │  └───┬───┘   │     │      │
   │      │      │        │     │      │
   │  ████│██┌───┴────────┴──┐██│████  │ ─── Biological Shield
   │  ████│██│  ┌──────────┐ │██│████  │     (Lead-PE-Boron)
   │  ████│██│  │  U-ZrH   │ │██│████  │
   │  ████│██│  │  Fuel     │ │██│████  │ ─── Fuel Assembly
   │  ████│██│  │  Assembly │ │██│████  │     (center)
   │  ████│██│  │  |||||||  │ │██│████  │ ─── Heat Pipes (vertical)
   │  ████│██│  │  |||||||  │ │██│████  │
   │  ████│██│  └──────────┘ │██│████  │
   │  ████│██│  ○ ○ ○ ○ ○ ○  │██│████  │ ─── Control Drums (6×)
   │  ████│██│   BeO Reflector│██│████  │
   │  ████│██└────────────────┘██│████  │
   │  ████│██████████████████████│████  │
   │      │                     │      │ ─── Reactor Vessel (316L)
    ╲     │  ┌───────────────┐  │     ╱
     ╲    │  │  V-Cell       │  │    ╱ ─── V-Cell Buffer
      ╲   │  │  Buffer       │  │   ╱
       ╲  │  └───────────────┘  │  ╱
        ╲ │  ┌───────────────┐  │ ╱
         ╲│  │  Cold Radiator│  │╱ ─── Cold-Side Radiator
          │  └───────────────┘  │
          │    ░░░░░░░░░░░░░    │ ─── Outer Casing
          └─────────────────────┘
                    │
                    ▼ Base pad (concrete)
```

### 6.2 Cross-Section (Horizontal, through fuel mid-plane)

```
                        ← 500 mm →

              ┌─────────────────────┐
           ╱  │  ████████████████   │  ╲
         ╱    │  ██┌───────────┐██  │    ╲
        │     │  ██│ ○       ○ │██  │     │
        │     │  ██│   ┌───┐   │██  │     │ ← BeO Reflector
        │     │  ██│ ○ │ F │ ○ │██  │     │    (annular)
        │     │  ██│   │ U │   │██  │     │
        │     │  ██│   │ E │   │██  │     │ ← Fuel Assembly
        │     │  ██│ ○ │ L │ ○ │██  │     │    (central cylinder)
        │     │  ██│   └─┼─┘   │██  │     │
        │     │  ██│ ○   │   ○ │██  │     │ ← 6 × Control Drums
         ╲    │  ██└─────┼─────┘██  │    ╱     (○ = drum positions)
           ╲  │  ████████│████████  │  ╱
              └──────────┼──────────┘
                         │
           Heat Pipes (12× vertical, through fuel)

              ○ = Control Drum (B₄C sector)
              │ = Na Heat Pipe (Inconel 718 wick)
              F,U,E,L = U-ZrH₁.₆ fuel rods
```

---

## 7. Core Technology: U-ZrH Fuel System

### 7.1 Fuel Composition

The V-Core uses uranium zirconium hydride (U-ZrH₁.₆) fuel derived from the TRIGA reactor family designed by General Atomics. The fuel consists of metallic uranium particles (8.5 wt% U, 19.75% enrichment — below the 20% HALEU threshold) dispersed in a δ-phase zirconium hydride matrix. The hydrogen atoms bound in the ZrH₁.₆ lattice serve simultaneously as:

- **Neutron moderator** — slowing fast fission neutrons to thermal energies within the fuel itself
- **Safety mechanism** — the prompt negative temperature coefficient (-1.0 × 10⁻⁴ Δk/k/°C) ensures that any temperature rise immediately reduces reactivity, making runaway power excursions physically impossible
- **Structural matrix** — the δ-ZrH₁.₆ phase is mechanically stable up to 750°C

### 7.2 Fuel Geometry

| Parameter | Value | Unit |
|-----------|-------|------|
| Fuel Rod Diameter | 37.5 | mm |
| Fuel Rod Active Length | 380 | mm |
| Cladding Material | Incoloy 800H | — |
| Cladding Thickness | 0.75 | mm |
| Number of Fuel Rods | 37 | — |
| Fuel Rod Pitch | 45.0 | mm (triangular lattice) |
| Assembly Envelope | Ø 250 | mm |
| U-235 Mass per Rod | 28.5 | g |
| Total U-235 Mass | 1,054 | g (~1.05 kg) |
| Total Fuel Assembly Mass | 42.0 | kg |
| Fuel Burnup Target | 30,000 | MWd/tHM |
| Fuel Lifetime | 10 | years at 75 kW thermal |

### 7.3 Fuel Material Properties — U-ZrH₁.₆

| Property | Value | Unit |
|----------|-------|------|
| Young's Modulus | 130 × 10⁹ | Pa |
| Poisson's Ratio | 0.32 | — |
| Yield Strength | 300 × 10⁶ | Pa |
| Ultimate Strength | 450 × 10⁶ | Pa |
| Fracture Toughness | 15 × 10⁶ | Pa·√m |
| Hardness | 250 | HV |
| Thermal Conductivity | 18 | W/(m·K) |
| Specific Heat | 350 | J/(kg·K) |
| Thermal Expansion | 7.0 × 10⁻⁶ | 1/K |
| Maximum Operating Temperature | 1,023 | K (750°C) |
| Hydrogen Dissociation Onset | 1,073 | K (800°C) |
| Density | 7,300 | kg/m³ |
| Friction (static) | 0.40 | — |
| Friction (kinetic) | 0.30 | — |
| Restitution | 0.3 | — |

### 7.4 Cladding Material Properties — Incoloy 800H

| Property | Value | Unit |
|----------|-------|------|
| Young's Modulus | 196 × 10⁹ | Pa |
| Poisson's Ratio | 0.31 | — |
| Yield Strength | 205 × 10⁶ | Pa (at 538°C) |
| Ultimate Strength | 500 × 10⁶ | Pa |
| Fracture Toughness | 80 × 10⁶ | Pa·√m |
| Hardness | 180 | HV |
| Thermal Conductivity | 11.5 | W/(m·K) |
| Specific Heat | 460 | J/(kg·K) |
| Thermal Expansion | 14.4 × 10⁻⁶ | 1/K |
| Melting Point | 1,630 | K |
| Density | 7,940 | kg/m³ |
| Friction (static) | 0.45 | — |
| Friction (kinetic) | 0.35 | — |
| Restitution | 0.35 | — |

---

## 8. Core Technology: Heat Pipe Thermal Transport

### 8.1 Design

Twelve sodium heat pipes are arrayed vertically through the fuel assembly, passing through dedicated channels in the fuel rod lattice. Each heat pipe is a sealed Inconel 718 tube with an internal sintered nickel wick structure. Liquid sodium in the evaporator section (fuel zone) absorbs heat, vaporizes, travels upward to the condenser section (hot-side heat exchanger), releases heat, condenses, and returns via capillary action in the wick. This is entirely passive — no pumps, no valves, no moving parts.

### 8.2 Heat Pipe Specifications

| Parameter | Value | Unit |
|-----------|-------|------|
| Number of Heat Pipes | 12 | — |
| Outer Diameter | 15.9 | mm |
| Wall Thickness | 1.5 | mm |
| Active Length (evaporator) | 380 | mm |
| Condenser Length | 200 | mm |
| Adiabatic Length | 100 | mm |
| Total Length | 680 | mm |
| Working Fluid | Sodium (Na) | — |
| Wick Type | Sintered nickel powder | — |
| Wick Thickness | 1.5 | mm |
| Wick Porosity | 60% | — |
| Operating Temperature | 773–973 | K (500–700°C) |
| Heat Transport per Pipe | 6.25 | kW |
| Total Heat Transport | 75 | kW |
| Startup Threshold | 500 | K (Na melts at 371 K) |
| Design Life | >100,000 | hr |

### 8.3 Heat Pipe Envelope Material — Inconel 718

| Property | Value | Unit |
|----------|-------|------|
| Young's Modulus | 200 × 10⁹ | Pa |
| Poisson's Ratio | 0.29 | — |
| Yield Strength | 1,034 × 10⁶ | Pa |
| Ultimate Strength | 1,241 × 10⁶ | Pa |
| Fracture Toughness | 95 × 10⁶ | Pa·√m |
| Hardness | 388 | HV |
| Thermal Conductivity | 11.4 | W/(m·K) |
| Specific Heat | 435 | J/(kg·K) |
| Thermal Expansion | 13.0 × 10⁻⁶ | 1/K |
| Melting Point | 1,609 | K |
| Density | 8,190 | kg/m³ |
| Friction (static) | 0.40 | — |
| Friction (kinetic) | 0.30 | — |
| Restitution | 0.35 | — |

---

## 9. Core Technology: Stirling Power Conversion

### 9.1 Design

Two free-piston Stirling engines operate in a balanced opposed configuration, canceling vibrations. Each engine produces 12.5 kW electrical from 37.5 kW thermal input (33.3% efficiency). The engines use helium as the working gas, linear alternators for electricity generation, and gas bearings — no contact surfaces, no lubricants, no rotating shafts. This eliminates wear as a life-limiting mechanism.

### 9.2 Stirling Engine Specifications

| Parameter | Value | Unit |
|-----------|-------|------|
| Number of Engines | 2 (balanced opposed) | — |
| Type | Free-piston, linear alternator | — |
| Working Fluid | Helium (He) | — |
| Mean Pressure | 6.0 | MPa |
| Hot-Side Temperature | 923 | K (650°C) |
| Cold-Side Temperature | 333 | K (60°C) |
| Thermal Input per Engine | 37.5 | kW |
| Electrical Output per Engine | 12.5 | kW |
| Efficiency | 33.3% | — |
| Frequency | 60 | Hz |
| Stroke | 25 | mm |
| Bore Diameter | 85 | mm |
| Engine Length | 450 | mm |
| Engine Diameter | 200 | mm |
| Engine Mass (each) | 32.5 | kg |
| Vibration Level | <0.1 | mm/s RMS (balanced pair) |
| Acoustic Noise | <40 | dB at 1 m |
| Design Life | 100,000 | hr (~11.4 years) |
| Maintenance Interval | None | — (sealed, no wear surfaces) |

### 9.3 Stirling Engine Housing Material — Maraging 350 Steel

| Property | Value | Unit |
|----------|-------|------|
| Young's Modulus | 190 × 10⁹ | Pa |
| Poisson's Ratio | 0.30 | — |
| Yield Strength | 2,400 × 10⁶ | Pa |
| Ultimate Strength | 2,450 × 10⁶ | Pa |
| Fracture Toughness | 35 × 10⁶ | Pa·√m |
| Hardness | 600 | HV |
| Thermal Conductivity | 25 | W/(m·K) |
| Specific Heat | 450 | J/(kg·K) |
| Thermal Expansion | 10.1 × 10⁻⁶ | 1/K |
| Melting Point | 1,686 | K |
| Density | 8,100 | kg/m³ |
| Friction (static) | 0.45 | — |
| Friction (kinetic) | 0.35 | — |
| Restitution | 0.4 | — |

---

## 10. Core Technology: Reactivity Control

### 10.1 Control Drum System

Six boron carbide (B₄C) control drums are positioned in the beryllium oxide reflector annulus surrounding the fuel assembly. Each drum is a cylinder with a 120° sector of B₄C absorber material on one face. Rotating the drums presents or hides the absorber from the neutron flux, adjusting reactivity.

### 10.2 Control Drum Specifications

| Parameter | Value | Unit |
|-----------|-------|------|
| Number of Drums | 6 | — |
| Drum Diameter | 60 | mm |
| Drum Length | 400 | mm |
| Absorber Material | B₄C (boron carbide), 120° sector | — |
| Drum Body | 304 Stainless Steel | — |
| Total Reactivity Worth | $8.00 | — |
| Shutdown Margin | >$2.00 | — |
| Rotation Range | 0–180° | — |
| Rotation Speed | 1.0 | °/s (normal), 180°/s (scram) |
| Fail-Safe Mode | Gravity drop to full-absorb position | — |
| Actuator | Stepper motor + harmonic drive (external) | — |

### 10.3 B₄C Absorber Material Properties

| Property | Value | Unit |
|----------|-------|------|
| Young's Modulus | 460 × 10⁹ | Pa |
| Poisson's Ratio | 0.17 | — |
| Yield Strength | 2,800 × 10⁶ | Pa (compressive) |
| Ultimate Strength | 350 × 10⁶ | Pa (tensile) |
| Fracture Toughness | 3.5 × 10⁶ | Pa·√m |
| Hardness | 3,000 | HV (Knoop) |
| Thermal Conductivity | 30 | W/(m·K) |
| Specific Heat | 950 | J/(kg·K) |
| Thermal Expansion | 5.0 × 10⁻⁶ | 1/K |
| Melting Point | 2,763 | K |
| Density | 2,520 | kg/m³ |
| Friction (static) | 0.35 | — |
| Friction (kinetic) | 0.25 | — |
| Restitution | 0.2 | — |
| ¹⁰B Natural Abundance | 19.9% | — |
| Thermal Neutron Absorption | 3,840 | barns (¹⁰B) |

### 10.4 Reflector Material Properties — Beryllium Oxide (BeO)

| Property | Value | Unit |
|----------|-------|------|
| Young's Modulus | 345 × 10⁹ | Pa |
| Poisson's Ratio | 0.26 | — |
| Yield Strength | 230 × 10⁶ | Pa (flexural) |
| Ultimate Strength | 250 × 10⁶ | Pa |
| Fracture Toughness | 3.0 × 10⁶ | Pa·√m |
| Hardness | 1,200 | HV (Knoop) |
| Thermal Conductivity | 260 | W/(m·K) |
| Specific Heat | 1,025 | J/(kg·K) |
| Thermal Expansion | 8.5 × 10⁻⁶ | 1/K |
| Melting Point | 2,780 | K |
| Density | 3,010 | kg/m³ |
| Friction (static) | 0.30 | — |
| Friction (kinetic) | 0.20 | — |
| Restitution | 0.25 | — |

---

## 11. Radiation Shielding

### 11.1 Shield Design

The biological shield is a graded composite surrounding the reactor vessel:

1. **Inner layer**: 50 mm lead (gamma attenuation)
2. **Middle layer**: 75 mm borated polyethylene (5 wt% B₄C, neutron moderation + capture)
3. **Outer layer**: 25 mm lead (secondary gamma from neutron capture)

### 11.2 Shielding Performance

| Parameter | Value | Unit |
|-----------|-------|------|
| Total Shield Thickness (radial) | 150 | mm |
| Shield Mass | 280 | kg |
| Dose Rate at Surface | <1.0 | mR/hr |
| Dose Rate at 1 meter | <0.25 | mR/hr |
| Annual Dose at 1 meter | <2.2 | mSv/yr |
| NRC Public Limit (10 CFR 20.1301) | 1.0 | mSv/yr at site boundary |
| Design Margin | >2× at 2 meters | — |

### 11.3 Lead Shielding Material Properties

| Property | Value | Unit |
|----------|-------|------|
| Young's Modulus | 16 × 10⁹ | Pa |
| Poisson's Ratio | 0.44 | — |
| Yield Strength | 11 × 10⁶ | Pa |
| Ultimate Strength | 17 × 10⁶ | Pa |
| Fracture Toughness | 15 × 10⁶ | Pa·√m |
| Hardness | 5.0 | HV (Brinell) |
| Thermal Conductivity | 35 | W/(m·K) |
| Specific Heat | 129 | J/(kg·K) |
| Thermal Expansion | 29.0 × 10⁻⁶ | 1/K |
| Melting Point | 600 | K |
| Density | 11,340 | kg/m³ |
| Friction (static) | 0.40 | — |
| Friction (kinetic) | 0.30 | — |
| Restitution | 0.15 | — |

### 11.4 Borated Polyethylene (5 wt% B₄C) Material Properties

| Property | Value | Unit |
|----------|-------|------|
| Young's Modulus | 0.8 × 10⁹ | Pa |
| Poisson's Ratio | 0.42 | — |
| Yield Strength | 25 × 10⁶ | Pa |
| Ultimate Strength | 33 × 10⁶ | Pa |
| Fracture Toughness | 2.0 × 10⁶ | Pa·√m |
| Hardness | 65 | Shore D |
| Thermal Conductivity | 0.40 | W/(m·K) |
| Specific Heat | 1,900 | J/(kg·K) |
| Thermal Expansion | 150 × 10⁻⁶ | 1/K |
| Maximum Operating Temperature | 393 | K (120°C) |
| Density | 1,080 | kg/m³ |
| Friction (static) | 0.35 | — |
| Friction (kinetic) | 0.25 | — |
| Restitution | 0.3 | — |

---

## 12. Thermal Management

### 12.1 Heat Flow Path

```
U-ZrH₁.₆ Fuel (750°C peak)
        │
        ▼ conduction through fuel + cladding
Na Heat Pipes (evaporator, 700°C)
        │
        ▼ sodium vapor transport (passive)
Hot-Side Heat Exchanger (650°C)
        │
   ┌────┴────┐
   ▼         ▼
Stirling   Stirling
Engine 1   Engine 2
(33.3%)    (33.3%)
   │         │
   ▼         ▼
Linear Alternators → 25 kW electrical output
   │         │
   ▼         ▼
Cold-Side Radiator (60°C)
        │
        ▼
Ambient Air (forced convection, low-speed fan)
or
CHP Water Loop (domestic hot water / space heating)
```

### 12.2 Heat Balance

| Source | Thermal Power (kW) | Notes |
|--------|-------------------|-------|
| Fission Core | 75.0 | Continuous, full power |
| → Stirling Engines (electrical) | 25.0 | 2 × 12.5 kW |
| → Cold-Side Rejection | 50.0 | Available for CHP |
| Gamma Heating in Shield | ~1.5 | Dissipated by casing convection |

### 12.3 Operating Envelope

| Parameter | Normal | Minimum | Maximum | Unit |
|-----------|--------|---------|---------|------|
| Fuel Centerline Temperature | 923 | 600 | 1,023 | K |
| Heat Pipe Vapor Temperature | 873 | 550 | 973 | K |
| Stirling Hot-Side Temperature | 923 | 500 | 973 | K |
| Stirling Cold-Side Temperature | 333 | 278 | 373 | K |
| Casing Surface Temperature | 313 | 278 | 333 | K |
| Ambient Temperature Range | 293 | 233 | 323 | K |
| Shield Maximum Temperature | 373 | 273 | 393 | K |

---

## 13. Geometry & Mechanical Design

### 13.1 Form Factor

| Parameter | Value | Unit |
|-----------|-------|------|
| Overall Shape | Prolate ellipsoid (egg) | — |
| Height | 800 | mm |
| Width (major axis) | 600 | mm |
| Depth (minor axis) | 500 | mm |
| Footprint | 0.48 | m² (600 × 800 pad) |
| Volume (external) | ~0.15 | m³ |
| Total Mass | ~693 | kg |
| Installation | Concrete pad, seismic anchors, 4 × M20 bolts | — |
| Seismic Rating | Zone 4 (0.4 g horizontal) | — |
| Flood Protection | Watertight to 2 m submersion | — |

### 13.2 Outer Casing Material — 304 Stainless Steel

| Property | Value | Unit |
|----------|-------|------|
| Young's Modulus | 193 × 10⁹ | Pa |
| Poisson's Ratio | 0.29 | — |
| Yield Strength | 215 × 10⁶ | Pa |
| Ultimate Strength | 505 × 10⁶ | Pa |
| Fracture Toughness | 100 × 10⁶ | Pa·√m |
| Hardness | 201 | HV |
| Thermal Conductivity | 16.3 | W/(m·K) |
| Specific Heat | 500 | J/(kg·K) |
| Thermal Expansion | 17.3 × 10⁻⁶ | 1/K |
| Melting Point | 1,673 | K |
| Density | 8,000 | kg/m³ |
| Friction (static) | 0.40 | — |
| Friction (kinetic) | 0.30 | — |
| Restitution | 0.4 | — |

### 13.3 Reactor Vessel Material — 316L Stainless Steel

| Property | Value | Unit |
|----------|-------|------|
| Young's Modulus | 193 × 10⁹ | Pa |
| Poisson's Ratio | 0.30 | — |
| Yield Strength | 170 × 10⁶ | Pa |
| Ultimate Strength | 485 × 10⁶ | Pa |
| Fracture Toughness | 112 × 10⁶ | Pa·√m |
| Hardness | 217 | HV |
| Thermal Conductivity | 14.6 | W/(m·K) |
| Specific Heat | 500 | J/(kg·K) |
| Thermal Expansion | 15.9 × 10⁻⁶ | 1/K |
| Melting Point | 1,673 | K |
| Density | 7,990 | kg/m³ |
| Friction (static) | 0.40 | — |
| Friction (kinetic) | 0.30 | — |
| Restitution | 0.4 | — |

---

## 14. Performance Specifications

### 14.1 Electrical Performance

| Parameter | Value | Unit |
|-----------|-------|------|
| Continuous Electrical Output | 25 | kW |
| Continuous Thermal Output | 75 | kW (CHP: 50 kW recoverable) |
| Overall Electrical Efficiency | 33.3% | — |
| CHP Efficiency (elec + heat) | >90% | — |
| Output Voltage | 240 | VAC split-phase (120/240) |
| Output Frequency | 60 | Hz (SiC inverter, grid-sync) |
| Grid Tie | Bidirectional, IEEE 1547 compliant | — |
| Islanding | Automatic, <16 ms transfer | — |
| V-Cell Buffer Capacity | 16.7 | kWh (2 × V-Cell modules) |
| Blackstart Time | <5 | min (from cold shutdown) |
| Load Following Range | 5–25 | kW (Vortex AI, drum rotation) |
| Annual Energy Production | 219,000 | kWh (at 95% capacity factor) |

### 14.2 Fuel & Lifetime

| Parameter | Value | Unit |
|-----------|-------|------|
| Fuel Load | U-ZrH₁.₆, 19.75% LEU | — |
| U-235 Mass | 1.054 | kg |
| Fuel Lifetime | 10 | years |
| Total Energy per Fuel Load | 2,190,000 | kWh electrical |
| Burnup | 30,000 | MWd/tHM |
| Refueling | Factory-return, sealed vessel swap | — |
| Decommissioning | Factory-return of entire unit | — |

### 14.3 Safety

| Parameter | Value | Notes |
|-----------|-------|-------|
| Prompt Temperature Coefficient | -1.0 × 10⁻⁴ Δk/k/°C | Inherent — physics, not engineering |
| Loss of Coolant Accident | Not credible | Heat pipes are sealed, no bulk coolant |
| Loss of Heat Sink | Safe — fuel temperature self-limits | Fuel coefficient shuts down reaction |
| Control System Failure | Safe — drums fall to absorb position | Gravity fail-safe |
| Seismic Event | Safe — no bulk liquid, no moving pipes | Solid-state thermal transport |
| Maximum Credible Accident | Loss of all Stirling engines | Fuel temp rises to ~800°C, coefficient shuts down, heat dissipates through shield to ambient |
| Emergency Evacuation Zone | 0 m (no off-site consequence) | Per NRC NUREG-1537 analysis |

---

## 15. Manufacturing Process

### 15.1 Process Comparison

| Step | Conventional Nuclear Plant | V-Core |
|------|---------------------------|--------|
| Site preparation | 3–5 years, billions $ | Concrete pad, 1 day, $5,000 |
| Construction | 7–12 years on-site | Factory-built, shipped complete |
| Fuel loading | On-site, specialized crew | Factory-sealed, never opened |
| Commissioning | 1–2 years | Vortex auto-commission, 4 hours |
| Refueling | 30-day outage, every 18 months | Swap entire unit, every 10 years |
| Decommissioning | 10–20 years, billions $ | Return to factory, vessel recycled |

### 15.2 Production Line Steps

1. **Fuel Rod Fabrication** — U-ZrH₁.₆ pellets pressed, sintered, loaded into Incoloy 800H cladding, end-cap welded, helium backfill, leak-tested
2. **Fuel Assembly Integration** — 37 fuel rods mounted in triangular grid, heat pipe channels aligned, lower grid plate welded
3. **Heat Pipe Fabrication** — Inconel 718 tubes drawn, sintered Ni wick inserted, sodium charged under argon, sealed by electron-beam weld
4. **Reflector + Control Drum Assembly** — BeO segments machined, B₄C sectors hot-pressed, drums assembled with bearings, reflector annulus assembled
5. **Reactor Vessel Assembly** — 316L vessel machined, fuel assembly + heat pipes + reflector inserted, vessel head welded, helium leak-tested, pressure-tested (2× design)
6. **Power Conversion Integration** — 2 × Stirling engines mated to hot-side heat exchanger, cold-side radiator connected, helium charged
7. **Shield Assembly** — Lead inner shell cast, borated PE middle layer molded, outer lead shell cast, all assembled around vessel
8. **Electrical Integration** — V-Cell buffer installed, SiC inverter connected, Vortex control module installed, wiring harness completed
9. **Outer Casing** — 304 SS egg-shaped casing welded, seismic mounting points installed, status array mounted
10. **Factory Acceptance Test** — Subcritical neutron source test, control drum function test, Stirling engine run-in (electric heater), full electrical integration test, Vortex commissioning

### 15.3 Production Targets

| Year | Units/Year | Unit Cost | Notes |
|------|------------|-----------|-------|
| Year 1 | 10 | $250,000 | Pilot production, NRC license pending |
| Year 3 | 100 | $200,000 | V-Man cell optimized |
| Year 5 | 1,000 | $150,000 | Full production, supply chain mature |

---

## 16. Claims

**Claim 1** (Independent): A residential micro-nuclear reactor comprising: a sealed uranium zirconium hydride fuel assembly having a prompt negative temperature coefficient of reactivity less than -5.0 × 10⁻⁵ Δk/k/°C; a plurality of alkali metal heat pipes passing through said fuel assembly for passive thermal transport; at least one free-piston Stirling engine receiving heat from said heat pipes and generating electricity; and a graded biological shield reducing surface dose rate below 1.0 mR/hr; wherein the reactor is factory-sealed and requires no on-site nuclear assembly.

**Claim 2**: The reactor of Claim 1, wherein said fuel assembly comprises 30–45 fuel rods of U-ZrH₁.₆ with uranium enrichment not exceeding 19.75% U-235, arranged in a triangular lattice within an Incoloy 800H cladding.

**Claim 3**: The reactor of Claim 1, wherein said alkali metal heat pipes number between 8 and 16, each comprising an Inconel 718 envelope with sintered nickel wick and sodium working fluid, operating between 773 K and 973 K.

**Claim 4**: The reactor of Claim 1, further comprising 4–8 rotatable control drums positioned in a neutron reflector annulus surrounding the fuel assembly, each drum having a boron carbide absorber sector covering 90–150° of arc, and arranged to fall by gravity to a full-absorb shutdown position upon loss of power.

**Claim 5**: The reactor of Claim 4, wherein said neutron reflector comprises beryllium oxide with thermal conductivity exceeding 200 W/(m·K).

**Claim 6**: The reactor of Claim 1, wherein said biological shield comprises an inner layer of lead (40–60 mm), a middle layer of borated polyethylene (60–90 mm) containing 3–7 wt% boron carbide, and an outer layer of lead (15–35 mm).

**Claim 7**: The reactor of Claim 1, wherein said Stirling engine is a free-piston type with helium working gas at 4–8 MPa mean pressure, producing 10–15 kW electrical per engine at 30–36% thermal-to-electric efficiency.

**Claim 8**: The reactor of Claim 1, further comprising: a solid-state battery buffer (V-Cell) providing 10–25 kWh of electrical storage for transient load-following and blackstart capability; and an AI control system (Vortex) providing autonomous monitoring, load-following via control drum rotation, and real-time telemetry to a regulatory monitoring facility.

**Claim 9**: The reactor of Claim 1, wherein the overall form factor has a height not exceeding 1,000 mm, a width not exceeding 700 mm, and a total mass not exceeding 800 kg.

**Claim 10**: The reactor of Claim 1, wherein the fuel assembly has a design burnup of at least 20,000 MWd/tHM, providing at least 8 years of continuous operation at rated thermal power without refueling.

**Claim 11**: A method of providing residential electrical power comprising: installing a factory-sealed micro-nuclear reactor on a residential concrete pad; connecting said reactor to a residential electrical panel; and operating said reactor autonomously via an AI control system for a period of at least 8 years without refueling, on-site maintenance, or human intervention beyond routine remote monitoring.

**Claim 12**: The method of Claim 11, wherein waste heat from the reactor is recovered via a water loop for domestic hot water heating and space heating, achieving combined heat and power efficiency exceeding 85%.

---

## 17. EustressEngine Simulation Requirements

Cross-reference: `EustressEngine_Requirements.md` and `SOTA_VALIDATION.md`

### 17.1 Component → ECS Mapping

| Component | Instance File | ECS Components |
|-----------|--------------|----------------|
| Reactor Vessel | `VCore_ReactorVessel.glb.toml` | MaterialProperties, ThermodynamicState |
| Fuel Assembly | `VCore_FuelAssembly.glb.toml` | MaterialProperties, ThermodynamicState, NuclearState |
| Reflector Assembly | `VCore_ReflectorAssembly.glb.toml` | MaterialProperties, ThermodynamicState |
| Control Drums | `VCore_ControlDrums.glb.toml` | MaterialProperties, ThermodynamicState |
| Heat Pipe Bundle | `VCore_HeatPipeBundle.glb.toml` | MaterialProperties, ThermodynamicState |
| Stirling Engines | `VCore_StirlingEngines.glb.toml` | MaterialProperties, ThermodynamicState |
| Hot-Side HX | `VCore_HotSideHX.glb.toml` | MaterialProperties, ThermodynamicState |
| Cold-Side Radiator | `VCore_ColdRadiator.glb.toml` | MaterialProperties, ThermodynamicState |
| Biological Shield | `VCore_BioShield.glb.toml` | MaterialProperties, ThermodynamicState |
| Outer Casing | `VCore_OuterCasing.glb.toml` | MaterialProperties, ThermodynamicState |
| V-Cell Buffer | `VCore_VCellBuffer.glb.toml` | MaterialProperties, ThermodynamicState, ElectrochemicalState |
| Control Module | `VCore_ControlModule.glb.toml` | MaterialProperties |
| Electrical Converter | `VCore_ElectricalConverter.glb.toml` | MaterialProperties |
| Status Array | `VCore_StatusArray.glb.toml` | MaterialProperties |

### 17.2 Required Realism Properties

| Property Domain | Fields | Applied To |
|----------------|--------|------------|
| ThermodynamicState | temperature, pressure, volume, internal_energy, entropy, enthalpy, moles | All components |
| ElectrochemicalState | voltage, capacity_ah, soc, current, internal_resistance, cycle_count | V-Cell Buffer |
| NuclearState (custom) | thermal_power_w, neutron_flux, burnup_mwd_thm, control_drum_angle_deg, fuel_temp_k, coolant_temp_k, reactivity_dk | Fuel Assembly |
| MaterialProperties | 14 base fields + [material.custom] | All components |
