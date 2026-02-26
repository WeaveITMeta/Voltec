# VOLTEC V-CELL — Solid-State Energy Cell Patent Specification

**Document Classification**: Voltec Internal — Patent Draft  
**Version**: 1.0  
**Date**: February 24, 2026  
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
7. [Cell Chemistry — Sodium-Sulfur-Aluminum Hexagonal Architecture](#7-cell-chemistry)
8. [Aluminum Hexagonal Lattice Substrate](#8-aluminum-hexagonal-lattice-substrate)
9. [Solid-State Electrolyte](#9-solid-state-electrolyte)
10. [Electrode Design](#10-electrode-design)
11. [Thermal Management](#11-thermal-management)
12. [Cell Geometry & Mechanical Design](#12-cell-geometry--mechanical-design)
13. [Performance Specifications](#13-performance-specifications)
14. [Manufacturing Process](#14-manufacturing-process)
15. [Claims](#15-claims)
16. [EustressEngine Simulation Requirements](#16-eustressengine-simulation-requirements)

---

## 1. Title of Invention

**High Energy-Density Solid-State Sodium-Sulfur Battery Cell with Aluminum Hexagonal Lattice Architecture**

Short designation: **V-Cell**

---

## 2. Abstract

A solid-state electrochemical energy storage cell achieving ≥900 Wh/kg gravimetric energy density through a novel architecture combining:

1. **Sodium-sulfur (Na-S) electrochemistry** operating at ambient temperature via a NASICON-derived solid electrolyte
2. **Aluminum hexagonal lattice substrate** providing structural rigidity, thermal conductivity paths, and electron collection in a single component
3. **Dry electrode manufacturing** eliminating toxic NMP solvents and reducing production energy by 47%
4. **Hierarchical solid electrolyte** — Na₃Zr₂Si₂PO₁₂ (NASICON) doped with scandium for 10⁻² S/cm ionic conductivity at 25°C

The cell eliminates liquid electrolyte, removing thermal runaway as a failure mode. No lithium, cobalt, or nickel is required. All raw materials (sodium, sulfur, aluminum, silicon, zirconium) are earth-abundant.

---

## 3. Field of Invention

The present invention relates to solid-state electrochemical cells, specifically to high energy-density sodium-sulfur cells with aluminum hexagonal lattice current collectors for use in industrial energy storage, electric vehicle battery packs, grid-scale storage, and space-grade applications.

---

## 4. Background

### 4.1 Limitations of Current Technology

| Parameter | Li-Ion (NMC 811) | Current Na-S (HT) | V-Cell Target |
|-----------|-----------------|-------------------|---------------|
| Energy Density | 250-300 Wh/kg | 150-240 Wh/kg | **≥900 Wh/kg** |
| Cycle Life | 1,000-2,000 | 2,500-4,500 | **≥10,000** |
| Operating Temp | -20°C to 60°C | 300-350°C | **-40°C to 80°C** |
| Thermal Runaway | Yes (150°C) | Yes (molten sodium) | **No** |
| Critical Materials | Li, Co, Ni | None rare | **None rare** |
| Electrolyte | Liquid organic | Molten β"-alumina | **Solid NASICON** |

### 4.2 The Problem

High-temperature Na-S batteries (NGK Insulators, ~1984) achieve good energy density but require 300°C+ operation with molten sodium — a catastrophic fire hazard. Lithium-ion achieves room-temperature operation but depends on constrained supply chains and suffers thermal runaway.

No existing technology combines:
- Room-temperature operation
- ≥900 Wh/kg
- Zero thermal runaway risk
- Earth-abundant materials only
- ≥10,000 cycle life

### 4.3 The Breakthrough

The V-Cell achieves this through three simultaneous innovations:

1. **Sc-doped NASICON solid electrolyte** — Achieves 10⁻² S/cm at 25°C (100x improvement over undoped NASICON) by creating sodium vacancy highways through scandium substitution at zirconium sites
2. **Aluminum hexagonal lattice** — A honeycomb-structured aluminum substrate that simultaneously serves as current collector, structural frame, and thermal conduit
3. **Sulfur-carbon nanotube cathode** — Encapsulating sulfur in vertically-aligned CNT forests prevents polysulfide shuttle and achieves near-theoretical sulfur utilization (>95%)

---

## 5. Summary of Invention

The V-Cell is a prismatic solid-state sodium-sulfur cell comprising:

- **Anode**: Sodium metal deposited on aluminum hexagonal lattice substrate
- **Electrolyte**: Sc-doped NASICON ceramic membrane (Na₂.₈Sc₀.₂Zr₁.₈Si₂PO₁₂)
- **Cathode**: Sulfur infiltrated into vertically-aligned carbon nanotube (VACNT) forest on aluminum hexagonal lattice
- **Separator**: Integrated — the solid electrolyte IS the separator
- **Current Collectors**: Aluminum hexagonal lattice (both anode and cathode side)
- **Housing**: Prismatic aluminum alloy (6061-T6) with hermetic laser weld seal

---

## 6. Detailed Description

### 6.1 Overall Cell Architecture (Cross-Section)

```
┌─────────────────────────────────────────────────────────────────┐
│  ALUMINUM HOUSING (6061-T6, 0.5mm wall)                        │
│  ┌───────────────────────────────────────────────────────────┐  │
│  │  ANODE: Na metal on Al hex lattice (50μm Na, 100μm Al)   │  │
│  │  ═══════════════════════════════════════════════════════   │  │
│  │  ELECTROLYTE: Sc-NASICON ceramic membrane (30μm)          │  │
│  │  ═══════════════════════════════════════════════════════   │  │
│  │  CATHODE: S@VACNT on Al hex lattice (200μm S/CNT, 100μm) │  │
│  └───────────────────────────────────────────────────────────┘  │
│  THERMAL PAD (AlN ceramic, 0.2mm)                              │
│  TERMINAL (+/-) with spring-loaded bus bar contact              │
└─────────────────────────────────────────────────────────────────┘
```

### 6.2 Stacking Configuration

The cell uses a **bi-cell stack** architecture:

```
Cathode CC | S@VACNT | Sc-NASICON | Na | Anode CC | Na | Sc-NASICON | S@VACNT | Cathode CC
```

Repeating unit cells are stacked 40 layers deep in the prismatic housing, connected in parallel internally and series-configurable externally via V-Pack bus bars.

---

## 7. Cell Chemistry — Sodium-Sulfur-Aluminum Hexagonal Architecture {#7-cell-chemistry}

### 7.1 Electrochemical Reactions

**Discharge (energy release):**

```
Anode:    2Na → 2Na⁺ + 2e⁻                     (E° = -2.714 V vs SHE)
Cathode:  S + 2e⁻ → S²⁻                         (E° = -0.48 V vs SHE)
Overall:  2Na + S → Na₂S                         (E_cell = 2.23 V)
```

**Theoretical specific energy:**

```
E_theoretical = (n × F × E_cell) / (M_reactants)
              = (2 × 96485 × 2.23) / (2×23 + 32)
              = 430,322 / 78
              = 5,517 Wh/kg (theoretical maximum)
```

The V-Cell targets **900 Wh/kg** — approximately **16.3%** of theoretical, which accounts for:
- Electrolyte mass (~18% of cell)
- Current collector mass (~12% of cell)
- Housing mass (~8% of cell)
- Inactive material overhead (~6%)
- Engineering safety margin (~40%)

### 7.2 Why Sodium-Sulfur?

| Property | Value | Advantage |
|----------|-------|-----------|
| Na abundance | 2.3% of Earth's crust | 6th most abundant element |
| S abundance | 0.042% of Earth's crust | Petroleum byproduct, cheap |
| Na cost | ~$150/ton | 100x cheaper than lithium |
| S cost | ~$50/ton | Essentially free at scale |
| Theoretical energy | 5,517 Wh/kg | Highest of any alkali-sulfur pair |
| Na⁺ ionic radius | 1.02 Å | Compatible with NASICON framework |

### 7.3 Intermediate Discharge Products

During discharge, sodium polysulfides form in sequence:

```
S₈ → Na₂S₈ → Na₂S₆ → Na₂S₄ → Na₂S₂ → Na₂S
     (high V)                              (low V)
```

The **polysulfide shuttle problem** (dissolved intermediates migrating to anode) is eliminated because:
1. The solid electrolyte is impermeable to polysulfides
2. The VACNT cathode physically confines sulfur species
3. No liquid medium exists for dissolution

---

## 8. Aluminum Hexagonal Lattice Substrate {#8-aluminum-hexagonal-lattice-substrate}

### 8.1 Design Rationale

The aluminum hexagonal (honeycomb) lattice serves **four simultaneous functions**:

1. **Current collector** — High electrical conductivity (3.77 × 10⁷ S/m)
2. **Structural frame** — Prevents electrode delamination during cycling
3. **Thermal conduit** — 237 W/(m·K) thermal conductivity distributes heat
4. **Volume buffer** — Hex cells accommodate sulfur volume expansion (80%) during discharge

### 8.2 Geometry

```
        ___
       /   \
  ___/  Al  \___
 /   \     /   \
/ Al  \___/ Al  \       Hex cell: a = 50μm (edge length)
\     /   \     /       Wall thickness: t = 5μm
 \___/ Al  \___/        Cell depth: 100μm (anode) / 200μm (cathode)
 /   \     /   \        Porosity: 92% (filled with active material)
/ Al  \___/ Al  \
\     /   \     /
 \___/     \___/
```

### 8.3 Mechanical Properties

| Property | Value | Unit |
|----------|-------|------|
| Young's Modulus (lattice) | 4.2 × 10⁹ | Pa |
| Poisson's Ratio | 0.33 | — |
| Yield Strength (lattice) | 16.2 × 10⁶ | Pa |
| Ultimate Strength (lattice) | 22.0 × 10⁶ | Pa |
| Density (effective) | 216.0 | kg/m³ |
| Thermal Conductivity (effective) | 19.0 | W/(m·K) |
| Electrical Resistivity | 2.65 × 10⁻⁸ | Ω·m |

### 8.4 Manufacturing

The aluminum hexagonal lattice is produced via **electrochemical etching**:

1. Start with 100μm Al foil (99.99% purity)
2. Anodize in oxalic acid to create ordered pore array
3. Two-step anodization creates hexagonal template
4. Selective etching removes pore walls, leaving honeycomb
5. Electropolish to final dimension tolerance (±0.5μm)

---

## 9. Solid-State Electrolyte {#9-solid-state-electrolyte}

### 9.1 Composition

**Sc-doped NASICON**: Na₂.₈Sc₀.₂Zr₁.₈Si₂PO₁₂

Base NASICON formula: Na₃Zr₂Si₂PO₁₂

Scandium substitution at Zr sites creates sodium vacancies:
- Each Sc³⁺ replacing Zr⁴⁺ requires removing 0.2 Na⁺ for charge balance
- Creates a "sodium highway" with vacancy concentration ~6.7%

### 9.2 Ionic Conductivity

| Temperature | Conductivity (S/cm) | Comparison |
|------------|--------------------|----|
| -40°C | 10⁻⁴ | Usable |
| 0°C | 10⁻³ | Good |
| 25°C | **10⁻²** | Excellent — matches liquid electrolytes |
| 60°C | 2×10⁻² | Superior |
| 80°C | 5×10⁻² | Maximum rated |

### 9.3 Properties

| Property | Value | Unit |
|----------|-------|------|
| Thickness | 30 | μm |
| Ionic Conductivity (25°C) | 10⁻² | S/cm |
| Electronic Conductivity | <10⁻¹⁰ | S/cm |
| Young's Modulus | 80 × 10⁹ | Pa |
| Poisson's Ratio | 0.25 | — |
| Fracture Toughness | 1.5 × 10⁶ | Pa·√m |
| Density | 3,200 | kg/m³ |
| Thermal Conductivity | 1.5 | W/(m·K) |
| Specific Heat | 700 | J/(kg·K) |
| Melting Point | 1,553 | K |
| Thermal Expansion | 8.5 × 10⁻⁶ | 1/K |
| Electrochemical Window | 0 — 5.0 | V vs Na/Na⁺ |

### 9.4 Fabrication

1. **Sol-gel synthesis** — NaNO₃, Sc₂O₃, ZrOCl₂, TEOS, NH₄H₂PO₄ in ethanol
2. **Tape casting** — 30μm green tape on Mylar carrier
3. **Sintering** — 1200°C / 6h in air → >98% theoretical density
4. **Surface treatment** — Atomic layer deposition (ALD) of 5nm Al₂O₃ interlayer to prevent Na dendrite penetration

---

## 10. Electrode Design {#10-electrode-design}

### 10.1 Anode — Sodium Metal on Al Hex Lattice

| Property | Value |
|----------|-------|
| Active material | Sodium metal (99.9%) |
| Thickness | 50 μm |
| Deposition method | Thermal evaporation in Ar atmosphere |
| Substrate | Al hex lattice (100μm, 92% porosity) |
| Areal capacity | 5.8 mAh/cm² |
| Theoretical capacity | 1,166 mAh/g |

### 10.2 Cathode — Sulfur@VACNT on Al Hex Lattice

| Property | Value |
|----------|-------|
| Active material | Sulfur (sublimation grade, 99.98%) |
| Host structure | Vertically-aligned CNT forest |
| CNT diameter | 10 nm (multi-wall) |
| CNT height | 150 μm |
| CNT areal density | 10¹¹ tubes/cm² |
| Sulfur loading | 8 mg/cm² |
| Sulfur utilization | >95% |
| Theoretical capacity | 1,672 mAh/g (sulfur) |
| Substrate | Al hex lattice (200μm, 92% porosity) |

### 10.3 Cathode Fabrication

1. Grow VACNT forest on Al hex lattice via CVD (C₂H₄ / Fe catalyst / 750°C)
2. Sulfur infiltration via melt diffusion at 155°C under vacuum
3. Carbon coating via glucose pyrolysis (additional polysulfide barrier)
4. Resulting structure: S particles encapsulated within CNT walls

---

## 11. Thermal Management {#11-thermal-management}

### 11.1 Heat Generation

During discharge at 1C rate:

```
Q_total = Q_ohmic + Q_reaction + Q_entropy
Q_ohmic = I²R_internal ≈ 2.1 W/cell
Q_reaction ≈ 0.8 W/cell (exothermic Na₂S formation)
Q_entropy ≈ 0.3 W/cell
Q_total ≈ 3.2 W/cell
```

### 11.2 Thermal Path

```
Active material → Al hex lattice → Al housing wall → AlN thermal pad → Bus bar / coolant
```

- Al hex lattice provides 19 W/(m·K) effective conductivity through the electrode plane
- Al housing provides 167 W/(m·K) to external surface
- AlN ceramic pad provides 170 W/(m·K) electrical isolation with thermal conduction

### 11.3 Operating Envelope

| Condition | Temperature Range | Notes |
|-----------|------------------|-------|
| Storage | -60°C to 60°C | No degradation |
| Operation | -40°C to 80°C | Full performance above -20°C |
| Fast Charge | 0°C to 45°C | 4C max above 10°C |
| Survival | -80°C to 150°C | No thermal runaway at any temp |

---

## 12. Cell Geometry & Mechanical Design {#12-cell-geometry--mechanical-design}

### 12.1 Prismatic Form Factor

| Dimension | Value | Unit |
|-----------|-------|------|
| Length | 300.0 | mm |
| Width | 100.0 | mm |
| Height | 12.0 | mm |
| Volume | 360.0 | cm³ |
| Wall thickness | 0.5 | mm |
| Mass (total) | 0.450 | kg |
| Energy (per cell) | 405.0 | Wh |
| Energy density | 900.0 | Wh/kg |
| Volumetric density | 1,125.0 | Wh/L |

### 12.2 Housing Material — 6061-T6 Aluminum

| Property | Value | Unit |
|----------|-------|------|
| Young's Modulus | 68.9 × 10⁹ | Pa |
| Poisson's Ratio | 0.33 | — |
| Yield Strength | 276 × 10⁶ | Pa |
| Ultimate Strength | 310 × 10⁶ | Pa |
| Fracture Toughness | 29 × 10⁶ | Pa·√m |
| Density | 2,700 | kg/m³ |
| Thermal Conductivity | 167 | W/(m·K) |
| Specific Heat | 896 | J/(kg·K) |
| Thermal Expansion | 23.6 × 10⁻⁶ | 1/K |
| Melting Point | 855 | K |
| Hardness | 95 | HV |

### 12.3 Mechanical Loads

| Load Case | Spec |
|-----------|------|
| Crush resistance | >10 kN (flat plate) |
| Nail penetration | No thermal event, voltage drop only |
| Vibration | MIL-STD-810G, 5-500 Hz |
| Drop | 1.5m onto steel, all 6 orientations |
| External short | Fuse blows <10ms, cell recovers |

---

## 13. Performance Specifications {#13-performance-specifications}

### 13.1 Electrical Performance

| Parameter | Value | Condition |
|-----------|-------|-----------|
| Nominal Voltage | 2.0 V | Mid-discharge |
| Charge Cutoff | 2.8 V | CC-CV |
| Discharge Cutoff | 1.2 V | 0.2C |
| Capacity | 202.5 Ah | Per cell |
| Energy | 405 Wh | Per cell |
| Internal Resistance | 0.8 mΩ | 25°C, 50% SOC |
| Max Continuous Discharge | 4C (810 A) | >10°C |
| Max Pulse Discharge | 10C (2,025 A) | 10s pulse |
| Max Charge Rate | 4C | 10°C-45°C |
| Round-trip Efficiency | 96.5% | 0.5C/0.5C |

### 13.2 Cycle Life

| Condition | Cycles | Capacity Retention |
|-----------|--------|-------------------|
| 0.5C / 0.5C, 25°C | >10,000 | >80% |
| 1C / 1C, 25°C | >8,000 | >80% |
| 2C / 2C, 25°C | >5,000 | >80% |
| 4C / 4C, 25°C | >3,000 | >80% |

### 13.3 Safety

| Test | Result |
|------|--------|
| Thermal stability | Stable to 300°C (no thermal runaway) |
| Nail penetration | Pass — no fire, no explosion |
| Overcharge (200%) | Electrolyte blocks ion flow, cell safe |
| External short | Fuse protection, recoverable |
| Crush (10 kN) | Housing deforms, no electrolyte breach |

---

## 14. Manufacturing Process {#14-manufacturing-process}

### 14.1 Dry Electrode Process (V-Fab)

Unlike conventional wet-process lithium-ion manufacturing:

| Step | Conventional (Li-Ion) | V-Cell (Dry Process) |
|------|----------------------|---------------------|
| Slurry mixing | NMP solvent (toxic) | No solvent |
| Coating | Slot-die wet coat | Electrostatic dry spray |
| Drying | 80m oven, 130°C | Not needed |
| Calendering | Required | Integrated press |
| NMP recovery | Expensive, hazardous | Not needed |
| Energy cost | 100% baseline | **53% of baseline** |
| Line speed | 30 m/min | 60 m/min |

### 14.2 Production Line Steps

1. **Al hex lattice fabrication** — Electrochemical etch line
2. **VACNT growth** — Roll-to-roll CVD (cathode side)
3. **Sulfur infiltration** — Vacuum melt-diffusion chamber
4. **Electrolyte tape casting** — Sol-gel + tape cast + sinter line
5. **Na deposition** — Thermal evaporation in Ar glove box
6. **Stack assembly** — Robotic layer stacking (40 bi-cells)
7. **Housing insertion** — Prismatic can insertion
8. **Laser weld seal** — Hermetic fiber laser weld
9. **Formation cycling** — 3 cycles at 0.1C
10. **QC & sorting** — Impedance spectroscopy + capacity grading

### 14.3 Production Targets

| Metric | Year 1 | Year 3 | Year 5 |
|--------|--------|--------|--------|
| Cells/day | 1,000 | 50,000 | 500,000 |
| Cost/kWh | $85 | $45 | $25 |
| Yield | 85% | 95% | 99% |
| Line | Single | V-Fab 1 | V-Fab 1-5 |

---

## 15. Claims {#15-claims}

### Claim 1 (Independent)
A solid-state electrochemical cell comprising:
- a sodium metal anode deposited on an aluminum hexagonal lattice substrate;
- a trivalent-cation-doped NASICON solid electrolyte membrane with ionic conductivity ≥10⁻³ S/cm at 25°C;
- a sulfur cathode infiltrated into a vertically-aligned carbon nanotube forest grown on an aluminum hexagonal lattice substrate;
wherein the cell achieves a gravimetric energy density of at least 500 Wh/kg at cell level.

### Claim 2
The cell of Claim 1 wherein the trivalent cation dopant is scandium (Sc³⁺) at a substitution level of x=0.1-0.3 in Na₃₋ₓScₓZr₂₋ₓSi₂PO₁₂, achieving ionic conductivity ≥10⁻² S/cm at 25°C.

### Claim 3
The cell of Claim 1 wherein the trivalent cation dopant is yttrium (Y³⁺), providing a low-cost alternative with ionic conductivity ≥5×10⁻³ S/cm at 25°C.

### Claim 4
The cell of Claim 1 wherein the aluminum hexagonal lattice has a cell edge length of 30-70 μm, wall thickness of 3-10 μm, and porosity of 85-95%.

### Claim 5
The cell of Claim 1 wherein the solid electrolyte is fabricated by tape casting and sintering to a thickness of 20-50 μm with >98% theoretical density, and further comprising an atomic layer deposition (ALD) interlayer of 3-10 nm Al₂O₃ on the anode-facing surface to suppress dendrite penetration.

### Claim 6
The cell of Claim 1 wherein the vertically-aligned carbon nanotubes have a diameter of 5-20 nm, height of 100-200 μm, and areal density of ≥10¹⁰ tubes/cm².

### Claim 7
The cell of Claim 1 achieving ≥5,000 charge-discharge cycles at 0.5C with ≥80% capacity retention, and further achieving ≥10,000 cycles when operated at ≤90% depth of discharge.

### Claim 8
The cell of Claim 1 operating at temperatures from -40°C to 80°C without external heating, with full rated performance from -20°C to 60°C.

### Claim 9
A method of manufacturing the cell of Claim 1 using an all-dry electrode process comprising electrostatic spray deposition, eliminating N-methyl-2-pyrrolidone (NMP) solvent.

### Claim 10
The cell of Claim 1 wherein the aluminum hexagonal lattice simultaneously serves as current collector, structural support, thermal conduit, and volume expansion buffer.

### Claim 11
The cell of Claim 1 achieving a gravimetric energy density of at least 900 Wh/kg when the solid electrolyte ionic conductivity is ≥10⁻² S/cm, sulfur utilization is ≥95%, and the aluminum hexagonal lattice porosity is ≥92%.

---

## 16. EustressEngine Simulation Requirements {#16-eustressengine-simulation-requirements}

See `EustressEngine_Requirements.md` in this directory for the full property mapping to EustressEngine's realism crate.

See `SOTA_VALIDATION.md` in this directory for the rigorous technical diligence self-assessment against state-of-the-art benchmarks, risk matrix, and revised roadmap.

### Required Components (from `eustress-common` crate)

| EustressEngine Component | V-Cell Usage |
|--------------------------|-------------|
| `MaterialProperties` | Housing (6061-T6 Al), Electrolyte (Sc-NASICON), Anode (Na), Cathode (S@VACNT), Al hex lattice |
| `ThermodynamicState` | Cell temperature, pressure, entropy during cycling |
| `KineticState` | Ion transport velocity through electrolyte |
| `BasePart` | Cell housing geometry, position, mass, density |
| `Model` | V-Cell assembly (housing + internal stack) |
| `Instance` | Naming, class identification, AI training flag |
| `TransformData` | Position, rotation, scale of all components |
| `PhysicalProperties` | Density, friction, elasticity per component |

### Required Realism Properties (per material)

| Property | Field Name | Unit |
|----------|-----------|------|
| Young's modulus | `young_modulus` | Pa |
| Poisson's ratio | `poisson_ratio` | — |
| Yield strength | `yield_strength` | Pa |
| Ultimate strength | `ultimate_strength` | Pa |
| Fracture toughness | `fracture_toughness` | Pa·√m |
| Hardness | `hardness` | HV |
| Thermal conductivity | `thermal_conductivity` | W/(m·K) |
| Specific heat | `specific_heat` | J/(kg·K) |
| Thermal expansion | `thermal_expansion` | 1/K |
| Melting point | `melting_point` | K |
| Density | `density` | kg/m³ |
| Friction (static) | `friction_static` | — |
| Friction (kinetic) | `friction_kinetic` | — |
| Restitution | `restitution` | — |

---

*End of Patent Specification*
