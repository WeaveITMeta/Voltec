# VOLTEC — Product Catalog

## The V-Series: Intelligent Energy & Industrial Infrastructure

Every product runs V-OS. Every device is a node in the Voltec intelligence network.

---

## Tier 1: Foundation — Shipping Now

### V-Cell
**Solid-State Energy Cell**

The fundamental unit. Everything at Voltec is built on V-Cell.

| Spec | Value |
|------|-------|
| Chemistry | Solid-state (sodium-sulfur variant) |
| Energy Density | 900 Wh/kg target |
| Cycle Life | 10,000+ cycles |
| Thermal Stability | Stable to 300°C |
| Form Factor | Prismatic, pouch |
| Manufacturing | Dry electrode, V-Man automated |
| Raw Materials | Abundant. No lithium/cobalt dependency. |

**Use Cases**: Industrial storage, EV packs, grid-scale, space-grade (V-Shield variant)

---

### V-Pack
**Modular Battery System**

V-Cells assembled into intelligent, self-monitoring packs with integrated BMS and Vortex telemetry.

| Configuration | Capacity | Target Customer |
|--------------|----------|----------------|
| **V-Pack S** | 5-50 kWh | Commercial / light industrial |
| **V-Pack M** | 50-500 kWh | Manufacturing, data centers |
| **V-Pack L** | 500 kWh - 5 MWh | Heavy industry, municipal |
| **V-Pack Defense** | Custom | Military, hardened installations |

**Key Feature**: Vortex integration predicts failures 72 hours in advance at 99.7% accuracy. Unplanned downtime costs $260K/hr — V-Pack eliminates it.

---

### V-Grid
**Distributed Energy Platform**

Networks thousands of V-Packs into a self-optimizing energy mesh. The first energy storage platform that thinks.

| Configuration | Scale | Target Customer |
|--------------|-------|----------------|
| **V-Grid Industrial** | 1 MW - 100 MW | Factories, data centers |
| **V-Grid Municipal** | 100 MW - 1 GW | City infrastructure, utilities |
| **V-Grid Defense** | Custom | Military, air-gapped, autonomous |

**Key Feature**: AI-optimized load balancing. Predicts demand, shifts loads, self-heals. No human intervention required.

**Pricing**: Per kWh of managed capacity. Service contracts guarantee 99.99% uptime.

---

### V-Incinerator
**High-Efficiency Plasma Gasification Waste-to-Energy System**

Plasma arc gasification at 5,000–7,000°C with four-stage exhaust purification, converting unsorted municipal solid waste to clean electricity and inert vitrified slag. Vortex AI controls combustion in real-time. Emissions 10–100× below the strictest global standards. Modular 6m × 3m × 4m units ship in two ISO containers and install in under two weeks. Japan proved waste-to-energy works — V-Incinerator brings it to America, cleaner than anyone thought possible.

| Spec | Value |
|------|-------|
| Core Technology | DC plasma arc gasification (3 × 500 kW torches) |
| Operating Temperature | 5,000–7,000°C (plasma), 1,100°C+ (secondary) |
| Waste Volume Reduction | ≥95% |
| Dioxin/Furan Emissions | <0.01 ng TEQ/Nm³ (100× below EU limit) |
| Particulate Emissions | <0.03 mg/Nm³ (300× below EU limit) |
| Net Electrical Output | ≥400 kW (self-sustaining + grid export) |
| Waste Throughput | 10 tons/day per unit |
| Preprocessing Required | None — accepts unsorted MSW |
| Footprint | 6.0m × 3.0m × 4.0m (modular) |
| Exhaust Purification | 4-stage: HEPA + Catalytic + Carbon + Wet Scrubber |
| Residue | Vitrified slag — TCLP inert, saleable as aggregate |
| AI Control | Vortex real-time combustion optimization |

**Use Cases**: Municipal solid waste processing, industrial waste reduction, medical waste disposal, disaster debris processing, landfill diversion, military forward operating bases

---

### V-Pump
**Modular Inline Vacuum-Assist Pipeline Pump**

Modular inline booster pump for permanent installation in large-scale water transport pipelines. Vacuum-assist priming eliminates cavitation. Universal flange adapters fit DN300–DN16000. Duplex stainless steel casing with RBSiC bore liner designed for 1,000-year continuous service. Vortex AI optimizes the hydraulic grade line across entire relay chains. Sized per-project using the `garbongus` fluid mechanics library. The pump that refills continents.

| Spec | Value |
|------|-------|
| Core Technology | Multi-stage axial-flow impeller + vacuum-assist priming |
| Casing Material | UNS S32205 Duplex Stainless Steel + RBSiC bore liner |
| Frame Sizes | VP-S (DN300-800), VP-M (DN800-2000), VP-L (DN2000-4000), VP-XL (DN4000-16000) |
| Max Flow | 600 m³/s (parallel VP-XL bank) |
| Max Head | 300 m (3-stage) |
| BEP Efficiency | 88–91% |
| Design Life (casing) | 1,000 years |
| Bearings | SiC/SiC ceramic journal, water-lubricated, 50–100 year replacement |
| Bypass | Automatic butterfly valve (fail-open, zero-downtime) |
| AI Control | Vortex real-time hydraulic grade line optimization |
| Relay Interval | ≤50 km between stations |
| Sizing Library | `garbongus` ≥0.2.1 (Darcy-Weisbach, vacuum lift, pump power) |

**Use Cases**: Continental-scale aquifer recharge (IGBWP), inter-basin water transfer, desalination distribution, municipal trunk mains, irrigation infrastructure

---

## Tier 2: Platform — Shipping in 18 Months

### V-OS
**The Industrial Operating System**

Every Voltec device runs V-OS. Third-party developers build on it. Open-source kernel, proprietary AI and data layers.

| Feature | Description |
|---------|-------------|
| Real-time OS | Sub-millisecond control loops for energy and automation |
| Open API Layer | REST + gRPC. Full SDK. Cloud simulator. |
| OTA Updates | Push firmware and model updates to every connected device |
| Security | Zero-trust architecture. Hardware root of trust. |

**Developer Program**: Free SDK, cloud simulator, V-Store marketplace (80/20 revenue split).

---

### Vortex
**AI/ML Intelligence Engine**

The brain of the Voltec network. Runs on every V-OS device. Gets smarter with every connected node.

| Capability | Description |
|-----------|-------------|
| Predictive Maintenance | 72-hour failure prediction, 99.7% accuracy |
| Energy Optimization | Real-time load balancing across distributed nodes |
| Anomaly Detection | Pattern recognition across millions of sensor streams |
| Autonomous Control | Closed-loop decision-making without cloud dependency |

**Data Flywheel**: 10,000 connected devices = 10,000x the training data. The network effect is the moat.

---

### V-Man
**Autonomous Manufacturing Cell**

Modular, containerized robotic manufacturing cell achieving ≥95% autonomous operation (lights-out / dark factory mode). The entire factory — 4–6 robotic arms, 3D vision, automatic tooling, precision conveyor, edge AI compute, and power distribution — ships inside a single ISO 40-foot high-cube container and deploys to production in ≤72 hours. Rust-native real-time control stack with software-defined manufacturing recipes. Built to manufacture V-Cells internally first, then sold externally as a general-purpose manufacturing platform.

| Spec | Value |
|------|-------|
| Form Factor | ISO 40' high-cube container (12.192 × 2.438 × 2.896 m) |
| Robotic Arms | 4–6 × 6-axis, 20 kg payload, ±0.02 mm repeatability |
| Vision System | 3D LIDAR + RGB-D + structured light, AI-accelerated (zero ambient light) |
| Control Stack | Rust-native, EtherCAT (1 ms cycle), Vortex edge AI (NVIDIA Jetson AGX Orin) |
| Tool Magazine | 12 slots, RFID tracking, <5 s pneumatic auto-change, ±0.005 mm repeatability |
| Conveyor | 10 m precision belt, 0.01–0.50 m/s, ±0.5 mm position accuracy |
| Power | 400V 3-phase AC, 25 kW peak / 12 kW average, 5 kVA UPS backup |
| Autonomy | ≥95% lights-out, ≤1 human intervention per shift |
| Setup Time | ≤72 hours delivery-to-production (container pad + power + data) |
| Output (V-Cell) | 7,200 cells/day (12 s cycle, 24h), ≥99.2% first-pass yield |
| Product Changeover | ≤4 hours via software recipe upload (TOML) |
| Safety | ISO 10218, ISO 13849-1 PLe, IEC 62443 |
| Cost Target | $1.2M (Year 1) → $500K (Year 5) |
| Components | 13 subsystems, 462 KB total mesh, 21,741 verts |

**Strategy**: The Amazon AWS playbook for manufacturing. V-Man's first customer is Voltec itself (V-Cell production). External sales begin only after internal validation. Every unit generates production data that makes Vortex smarter — the manufacturing data flywheel.

---

## Tier 3: Horizon — Shipping in 3-5 Years

### V-Shield
**Space-Grade Electronics Platform**

Radiation-hardened V-Cells and electronics for orbital and deep-space deployment.

| Spec | Value |
|------|-------|
| Radiation Tolerance | 100 krad TID |
| Temperature Range | -40°C to +125°C |
| Qualification | MIL-STD-883, ECSS-Q-ST |
| Cost Target | 10x current space-grade (not 100x) |

**Market**: Satellite constellations, lunar infrastructure, deep-space probes.

---

### V-Orbit
**Space-Grade Energy Packs**

V-Shield cells assembled into orbital-qualified power systems for satellite buses and space stations.

| Configuration | Capacity | Application |
|--------------|----------|-------------|
| **V-Orbit Nano** | 100 Wh | CubeSats, small-sats |
| **V-Orbit Standard** | 1-10 kWh | LEO constellation nodes |
| **V-Orbit Heavy** | 10-100 kWh | GEO platforms, stations |

---

## Tier 3: Horizon — Near-Term Advanced Systems

### V-Core
**Residential Micro-Nuclear Reactor**

Passively safe micro-fission reactor producing 25 kW electrical and 75 kW thermal continuous power from a sealed TRIGA-heritage uranium zirconium hydride (U-ZrH₁.₆) fuel core with a 10-year refueling interval. Sodium heat pipe passive thermal transport to free-piston Stirling engines. Factory-sealed, truck-delivered, installed on a concrete pad. Vortex AI provides autonomous monitoring, load-following, and NRC telemetry compliance. Zero fuel deliveries, zero emissions, zero operator intervention for a decade.

| Spec | Value |
|------|-------|
| Core Technology | U-ZrH₁.₆ fission fuel (TRIGA heritage, 19.75% LEU) |
| Electrical Output | 25 kW continuous (240 VAC split-phase, IEEE 1547 grid-tie) |
| Thermal Output | 75 kW (50 kW recoverable CHP for hot water/space heating) |
| Efficiency | 33.3% electrical, >90% CHP |
| Fuel Lifetime | 10 years (87,600 hours), factory-return refueling |
| Form Factor | Egg-shaped prolate ellipsoid, 800 × 600 × 500 mm |
| Dry Mass | ~693 kg (280 kg biological shield, 413 kg reactor + power systems) |
| Heat Transport | 12 × sodium heat pipes (Inconel 718, passive, zero moving parts) |
| Power Conversion | 2 × free-piston Stirling engines (Maraging 350, balanced opposed) |
| Reactivity Control | 6 × B₄C rotating control drums (gravity fail-safe) |
| Shielding | Lead-polyethylene-boron composite, <0.25 mR/hr at 1 meter |
| Buffer | 16.7 kWh V-Cell Na-S solid state (blackstart <5 minutes) |
| AI Control | Vortex (NVIDIA Orin), NRC telemetry, autonomous load-following |
| Noise | <40 dB at 1 meter |
| Components | 14 subsystems, 14 materials, Draco-compressed GLB meshes |
| Validation Tier | PROJECTED — all subsystems proven individually; integration at residential scale is first-of-kind |

**Use Cases**: Off-grid residential, remote communities, military forward operating bases, disaster relief, light commercial, data center backup, island/microgrid anchor

---

## Tier 4: Beyond — Research & Development

### V-Supreme
**Fusion-Powered Full-Body Mecha Platform**

Full-body powered exoskeleton platform for extreme-environment industrial, defense, and space operations. Aneutronic proton-boron-11 compact fusion reactor provides 500 kW continuous power. 42 degrees of freedom articulated joint architecture with 1 kHz closed-loop control. Integrated directed energy systems and Hall-effect ion thrusters. V-Cell Na-S solid state buffer array provides 50 kWh burst capacity. Vortex AI handles balance control, inverse kinematics, and operator intent prediction. The suit that makes the impossible routine.

| Spec | Value |
|------|-------|
| Core Technology | Aneutronic p-B11 compact fusion reactor (YBCO toroidal confinement) |
| Power Output | 500 kW continuous (600 VDC bus) |
| Buffer Capacity | 50 kWh (6 × V-Cell Na-S solid state modules) |
| Standing Height | ~2.2 m |
| Dry Mass | ~400 kg (339 kg components + 61 kg wiring/fasteners/coolant) |
| Degrees of Freedom | 42 (neck 3, arms 24, spine 3, legs 12) |
| Max Joint Torque | 800 N·m (hip/knee cycloidal drives) |
| Control Loop | 1 kHz EtherCAT, PID + Vortex motion planning |
| Primary Structure | Ti-6Al-4V (Grade 5 Titanium) |
| Reactor Vessel | W-25Re Alloy (Tungsten-Rhenium) |
| Thruster Pack | Mo-47.5Re Alloy, 2 × Hall-effect (xenon), 1,600 s specific impulse |
| Directed Energy | Left forearm plasma cutter, right forearm DEP emitter |
| Weapons Cooling | Dual-loop Therminol HT-55 (2.0 + 1.5 L/s) |
| AI Control | Vortex balance, inverse kinematics, operator intent prediction |
| Components | 23 subsystems, ~762 KB total mesh (placeholder), 5 material systems |
| Validation Tier | ASPIRATIONAL — requires breakthrough advances in compact fusion |

**Use Cases**: Deep-space extravehicular activity, nuclear decommissioning, deep-sea infrastructure, disaster response in contaminated environments, heavy industrial construction, defense operations

---

## Accessories & Services

| Item | Description |
|------|-------------|
| **V-Link** | Mesh communication module. Low-latency, jamming-resistant. Connects V-OS devices. |
| **V-Sense** | Multi-modal sensor array (thermal, vibration, electrical). Feeds Vortex. |
| **V-Dock** | Charging and diagnostic station for V-Pack maintenance. |
| **Deployment Services** | Site survey, installation, integration, commissioning. |
| **V-Care** | Ongoing monitoring, predictive maintenance, guaranteed uptime SLAs. |

---

## Datasheets

All products ship with full technical datasheets. No marketing fluff.

Request datasheets at **voltec.dev/datasheets** or contact **sales@voltec.dev**.
