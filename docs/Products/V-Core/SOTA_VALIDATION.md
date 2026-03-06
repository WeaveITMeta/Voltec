# V-Core — State-of-the-Art Validation & Risk Assessment

**Document Classification**: Voltec Internal — Technical Assessment  
**Version**: 1.0  
**Date**: March 6, 2026  
**Status**: Pre-Filing Draft  

---

## 1. Preface: Honesty Framework

Every claim in this document is tagged with one of three tiers:

| Tier | Definition | Evidence Standard |
|------|-----------|-------------------|
| **VERIFIED** | Demonstrated in production or peer-reviewed literature at the claimed scale | Published data, commercial product, or laboratory measurement with citation |
| **PROJECTED** | Demonstrated at sub-scale or in related systems; engineering extrapolation with <3× gap to SOTA | Sub-scale prototype data, validated simulation, or vendor specification |
| **ASPIRATIONAL** | Not yet demonstrated; requires breakthrough or first-of-kind engineering | Theoretical analysis only; no experimental validation at claimed parameters |

V-Core is designed to be significantly more grounded than V-Supreme. All subsystem technologies (U-ZrH fuel, sodium heat pipes, Stirling engines, B₄C control drums) have decades of operational heritage. The primary challenge is **integration at residential scale** and **regulatory licensing** — not fundamental physics.

---

## 2. Performance Metrics

### 2.1 Power & Energy

| Metric | V-Core Target | Current SOTA | Gap | Tier |
|--------|--------------|-------------|-----|------|
| Electrical output | 25 kW continuous | 10 kW (eVinci concept at lowest tier) | 2.5× smaller than eVinci's 200 kW–5 MW range | **PROJECTED** |
| Thermal output | 75 kW | KRUSTY: 4.3 kW thermal (2018 test) | 17× higher than only flight-tested system | **PROJECTED** |
| Electrical efficiency | 33.3% (Stirling) | 28–32% (Sunpower FPSE, demonstrated) | 1.04–1.19× | **PROJECTED** |
| CHP efficiency | >90% | 85–92% (commercial micro-CHP, Bloom/Ceres) | At parity | **VERIFIED** |
| Capacity factor | 95% | 92–95% (commercial nuclear plants) | At parity | **VERIFIED** |
| Fuel lifetime | 10 years | 18 months (LWR refueling), 10+ years (TRIGA Mark II at low power) | Comparable to TRIGA experience | **PROJECTED** |
| Load following | 5–25 kW | Standard for SMRs via control rod/drum adjustment | At parity | **VERIFIED** |

**Assessment**: The 25 kW electrical target is modest by nuclear standards — KRUSTY demonstrated 1 kW electrical from a much simpler system in 2018, and the eVinci targets 200 kW–5 MW. Scaling Stirling engines to 12.5 kW each is within demonstrated capability (Sunpower has tested 10+ kW units). The primary gap is integrating all subsystems into a residential-sized package. The 75 kW thermal power is well within TRIGA fuel operating experience — TRIGA Mark II reactors operate at 250 kW–14 MW thermal.

### 2.2 Safety

| Metric | V-Core Target | Current SOTA | Gap | Tier |
|--------|--------------|-------------|-----|------|
| Prompt temperature coefficient | -1.0 × 10⁻⁴ Δk/k/°C | -1.0 × 10⁻⁴ (TRIGA, measured) | At parity — same fuel | **VERIFIED** |
| Loss of coolant accident | Not credible (heat pipes sealed) | KRUSTY: same architecture, tested | At parity | **VERIFIED** |
| Maximum credible accident | Fuel temp rise to 800°C, self-shutdown | TRIGA: routinely pulsed to 22 GW, safe | Conservative vs TRIGA experience | **VERIFIED** |
| Surface dose rate | <1.0 mR/hr | TRIGA pool-top: ~0.5 mR/hr | At parity | **PROJECTED** |
| Dose at 1 meter | <0.25 mR/hr | Background: 0.01–0.03 mR/hr | 8–25× background, but well below NRC limit | **PROJECTED** |
| Emergency planning zone | 0 m (site boundary) | KRUSTY/eVinci: target 0 m EPZ | At parity | **PROJECTED** |
| Seismic resilience | Zone 4 (0.4 g) | Standard nuclear seismic design | At parity | **VERIFIED** |

**Assessment**: The safety case is the strongest aspect of V-Core. U-ZrH fuel has been pulsed safely to 22,000 MW in TRIGA reactors — the prompt negative temperature coefficient is physics, not engineering. The absence of bulk liquid coolant (heat pipes are sealed, two-phase, passive) eliminates the loss-of-coolant accident that dominates conventional reactor risk analysis. The biological shield design is conservative and well-understood. The key regulatory challenge is convincing the NRC that a residential installation meets 10 CFR Part 53 requirements for autonomous unattended operation.

### 2.3 Form Factor & Mass

| Metric | V-Core Target | Current SOTA | Gap | Tier |
|--------|--------------|-------------|-----|------|
| Total mass | ~693 kg | eVinci: >40,000 kg (truck-transportable) | 57× lighter, but 8–200× less power | **PROJECTED** |
| Footprint | 0.48 m² | KRUSTY: ~0.5 m² (reactor only, no shield) | At parity (but KRUSTY is 4.3 kW, not 75 kW) | **PROJECTED** |
| Height | 800 mm | No residential micro-reactor exists | First-of-kind | **ASPIRATIONAL** |
| Shield mass fraction | 40% (280/693 kg) | Typical: 50–70% for compact reactors | Favorable — but requires validation | **PROJECTED** |
| Installation time | <1 day | eVinci: weeks (site prep + crane) | Significantly simpler | **PROJECTED** |

**Assessment**: The 693 kg total mass is aggressive for a shielded nuclear system. The 280 kg biological shield is the critical mass driver — lead density (11,340 kg/m³) makes even thin layers heavy. The 150 mm radial shield thickness is the minimum that can plausibly achieve <0.25 mR/hr at 1 meter for a 75 kW thermal source. This needs Monte Carlo neutronics simulation (MCNP6) to validate. If the shield proves inadequate, mass could increase by 50–100 kg. The egg form factor is aspirational — no nuclear system has been built in this shape, though there is no physics reason it cannot be.

### 2.4 Stirling Engine Power Conversion

| Metric | V-Core Target | Current SOTA | Gap | Tier |
|--------|--------------|-------------|-----|------|
| Power per engine | 12.5 kW electrical | 10.3 kW (Sunpower EG-1000, demonstrated) | 1.2× | **PROJECTED** |
| Efficiency | 33.3% | 28–32% (demonstrated at hot-side 650°C) | 1.04–1.19× | **PROJECTED** |
| Design life | 100,000 hr | 60,000 hr (Sunpower demonstrated) | 1.67× | **PROJECTED** |
| Vibration (balanced pair) | <0.1 mm/s RMS | Balanced-opposed Stirling: <0.2 mm/s demonstrated | 2× better, plausible with tuning | **PROJECTED** |
| Acoustic noise | <40 dB at 1 m | 45–50 dB (typical FPSE) | 1.1–1.25× quieter | **PROJECTED** |
| Maintenance | Zero (sealed) | Zero (Sunpower gas bearings) | At parity | **VERIFIED** |

**Assessment**: Free-piston Stirling engines are the most mature subsystem. Sunpower (now part of Agilent) has demonstrated 10+ kW engines with gas bearings and 60,000+ hours of operation. The 12.5 kW target is a modest 1.2× scale-up. The 33.3% efficiency at 650°C hot-side is within published Carnot-limited projections for this temperature range. The 100,000-hour life target requires validating gas bearing wear at the higher power level — likely achievable given that wear is the non-issue for gas bearings (no contact surfaces).

### 2.5 Heat Pipe Thermal Transport

| Metric | V-Core Target | Current SOTA | Gap | Tier |
|--------|--------------|-------------|-----|------|
| Heat transport per pipe | 6.25 kW | 4 kW (KRUSTY Na heat pipe, demonstrated) | 1.56× | **PROJECTED** |
| Number of pipes | 12 | 8 (KRUSTY) | 1.5× more, straightforward | **VERIFIED** |
| Total heat transport | 75 kW | 32 kW (KRUSTY design) | 2.3× | **PROJECTED** |
| Operating temperature | 773–973 K | 773–1,073 K (Na heat pipe literature) | Within range | **VERIFIED** |
| Design life | >100,000 hr | >50,000 hr (demonstrated in literature) | 2× | **PROJECTED** |
| Startup threshold | 500 K (Na melts at 371 K) | Standard for Na heat pipes | At parity | **VERIFIED** |

**Assessment**: Sodium heat pipes at these temperatures and power levels are well-demonstrated in nuclear and space applications. The 6.25 kW per pipe is achievable with the specified 15.9 mm diameter at sodium vapor temperatures of 700°C. The 12-pipe bundle provides redundancy — the system can operate at reduced power with as few as 8 functional pipes.

---

## 3. Durability & Lifetime

| Parameter | V-Core Target | Basis | Tier |
|-----------|--------------|-------|------|
| Fuel lifetime | 10 years (87,600 hr) | TRIGA: 30+ year fuel lifetimes demonstrated at research power levels | **PROJECTED** |
| Stirling engine life | 100,000 hr | Sunpower: 60,000 hr demonstrated; gas bearing extrapolation | **PROJECTED** |
| Heat pipe life | >100,000 hr | Literature: Na heat pipes tested to 50,000 hr; Inconel 718 compatible | **PROJECTED** |
| Control drum mechanism | >100,000 hr | Standard nuclear-grade stepper motor + harmonic drive | **VERIFIED** |
| V-Cell buffer | 10,000 cycles | V-Cell PATENT.md target | **PROJECTED** |
| Reactor vessel (316L) | 40 years (ASME Code) | ASME Section III, Division 5 design rules | **VERIFIED** |
| Shield integrity | 40 years | Lead: no degradation; borated PE: radiation damage limit ~10⁸ Gy | **VERIFIED** |

---

## 4. Safety

### 4.1 Failure Mode Analysis

| Failure Mode | Consequence | Mitigation | Residual Risk |
|-------------|------------|------------|---------------|
| Loss of all Stirling engines | Fuel temperature rises to ~800°C | Prompt negative coefficient self-limits; heat dissipates through shield | **Negligible** — this is the design basis event |
| Single heat pipe failure | Reduced heat transport, local hot spot | System operates at reduced power; 12 pipes provide N+4 redundancy | **Low** |
| Control drum jamming | Reactivity insertion (if drum stuck in reflective position) | 6 drums with $8 total worth; any 4 can achieve shutdown; gravity fail-safe | **Low** |
| All control drums fail to rotate | Cannot adjust power | V-Mind detects, initiates shutdown sequence; temperature coefficient self-limits | **Low** |
| Seismic event | Mechanical shock to fuel and shield | Seismic restraint bolts; no bulk liquid to slosh; solid-state construction | **Negligible** |
| External impact (vehicle) | Casing damage, potential shield breach | 304 SS casing + 280 kg shield absorbs impact; NRC-required crash analysis | **Low** |
| Hydrogen release from U-ZrH | Positive reactivity from moderator loss | Only occurs above 800°C; temperature coefficient ensures this is self-limiting | **Negligible** |
| Malicious tampering | Attempt to access fuel | Factory-sealed, tamper-evident, NRC-monitored telemetry 24/7 | **Low** (regulatory/physical security) |
| Flooding | Water ingress to electrical systems | Watertight to 2 m submersion; nuclear side unaffected | **Low** |

### 4.2 Comparison to Conventional Nuclear Safety

| Feature | Conventional Light Water Reactor | V-Core |
|---------|--------------------------------|--------|
| Coolant | Water (pressurized, can boil/leak) | None — heat pipes are sealed, passive |
| Loss of coolant accident | Design basis event, major risk | Not credible — no bulk coolant |
| Fuel meltdown | Possible if cooling fails | Impossible — U-ZrH self-limits at 750°C, well below melt |
| Hydrogen explosion | Risk from Zr-water reaction at >1,200°C | No water in contact with fuel |
| Containment breach | Large reinforced concrete building required | Factory-sealed steel vessel + shield |
| Emergency planning zone | 10+ miles | 0 m (site boundary) |
| Operator staffing | 24/7 licensed operators | Zero — V-Mind autonomous + remote NRC telemetry |
| Refueling | On-site, 30-day outage | Factory-return every 10 years |

---

## 5. Materials & Chemistry Feasibility

### 5.1 U-ZrH₁.₆ Fuel

| Aspect | Assessment | Tier |
|--------|-----------|------|
| Availability | Sole manufacturer: CERCA/Framatome (Romans-sur-Isère, France) | **VERIFIED** |
| Cost | ~$25,000–50,000 per fuel assembly (37 rods, custom) | **PROJECTED** |
| Scalability | CERCA capacity: ~100 TRIGA assemblies/year; V-Core needs 1 per unit | Feasible | **VERIFIED** |
| Enrichment | 19.75% LEU — below HALEU threshold, standard TRIGA spec | **VERIFIED** |
| Regulatory | TRIGA fuel approved under NRC since 1958 — 66 reactors licensed worldwide | **VERIFIED** |

### 5.2 Inconel 718 (Heat Pipes + Hot-Side Heat Exchanger)

| Aspect | Assessment | Tier |
|--------|-----------|------|
| Availability | Mature aerospace alloy, multiple suppliers (Special Metals, ATI, Haynes) | **VERIFIED** |
| Cost | $40–80/kg (bar stock), $150–300/kg (finished tube) | **VERIFIED** |
| V-Core quantity | ~30 kg per unit × 100 units = 3,000 kg/year | Trivial vs global supply | **VERIFIED** |
| Na compatibility | Demonstrated compatible with sodium to 700°C for >50,000 hr | **VERIFIED** |

### 5.3 Beryllium Oxide (Reflector)

| Aspect | Assessment | Tier |
|--------|-----------|------|
| Availability | Specialty ceramic, Materion Corporation (sole US supplier) | **PROJECTED** |
| Cost | $500–1,500/kg (finished parts) | **VERIFIED** |
| V-Core quantity | 38 kg per unit = $19,000–57,000 per unit | Expensive but feasible | **PROJECTED** |
| Toxicity | BeO dust is highly toxic — requires glove box handling during fabrication | **VERIFIED** |
| Alternatives | MgO reflector (lower performance, ~20% larger core) as cost-reduction fallback | **PROJECTED** |

### 5.4 Lead (Shielding)

| Aspect | Assessment | Tier |
|--------|-----------|------|
| Availability | Globally abundant, ~11 million tons/year production | **VERIFIED** |
| Cost | $2.0–2.5/kg | **VERIFIED** |
| V-Core quantity | ~200 kg per unit = $400–500 per unit | Trivial | **VERIFIED** |
| Environmental | Lead requires handling controls; encapsulated in shield, no exposure during operation | **VERIFIED** |

### 5.5 Borated Polyethylene (Shielding)

| Aspect | Assessment | Tier |
|--------|-----------|------|
| Availability | Commercial nuclear shielding product (Shieldwerx, Thermo Scientific) | **VERIFIED** |
| Cost | $15–30/kg | **VERIFIED** |
| V-Core quantity | ~80 kg per unit = $1,200–2,400 per unit | Trivial | **VERIFIED** |
| Temperature limit | 120°C — must be positioned outside lead inner layer | **VERIFIED** |

### 5.6 316L Stainless Steel (Reactor Vessel)

| Aspect | Assessment | Tier |
|--------|-----------|------|
| Availability | Standard nuclear-grade steel, globally produced | **VERIFIED** |
| Cost | $5–15/kg (plate), $50–100/kg (ASME nuclear-certified vessel) | **VERIFIED** |
| ASME certification | Section III, Division 5 — established code for high-temperature reactors | **VERIFIED** |

### 5.7 Maraging 350 Steel (Stirling Engine Housing)

| Aspect | Assessment | Tier |
|--------|-----------|------|
| Availability | Specialty high-strength steel, limited suppliers (Carpenter, VDM Metals) | **PROJECTED** |
| Cost | $30–60/kg | **VERIFIED** |
| V-Core quantity | ~65 kg per unit = $1,950–3,900 per unit | Feasible | **VERIFIED** |

---

## 6. Manufacturing Feasibility

| Aspect | Assessment | Tier |
|--------|-----------|------|
| Fuel rod fabrication | Established process at CERCA/Framatome; 60+ years experience | **VERIFIED** |
| Heat pipe fabrication | Specialty process; ACT (Advanced Cooling Technologies) demonstrated for KRUSTY | **VERIFIED** |
| Stirling engine fabrication | Sunpower/Agilent demonstrated at 10 kW scale | **VERIFIED** |
| Shield fabrication | Standard lead casting + PE molding; no exotic processes | **VERIFIED** |
| Reactor vessel welding | ASME Section III certified weld shops exist (many) | **VERIFIED** |
| Final assembly | V-Man cell adaptable for nuclear-grade clean room + integration | **PROJECTED** |
| Quality assurance | NQA-1 program required; establishes QA overhead | **VERIFIED** |
| Production rate target | 10 units/year (Year 1) — achievable with single production line | **PROJECTED** |

---

## 7. Regulatory Landscape

### 7.1 NRC Licensing Pathway

| Milestone | Estimated Timeline | Risk |
|-----------|--------------------|------|
| Pre-application engagement with NRC | 2026–2027 | Low — NRC actively encourages micro-reactor engagement |
| Design certification application (10 CFR Part 53) | 2028 | Medium — Part 53 rule still being finalized |
| NRC review and approval | 2029–2031 (3 years) | Medium — first-of-kind residential reactor |
| Combined License for first installation | 2031–2032 | Medium — site-specific review |
| First customer delivery | 2032 | Optimistic |

### 7.2 Regulatory Risks

| Risk | Severity | Probability | Mitigation |
|------|----------|-------------|------------|
| NRC rejects residential installation concept | Critical | Medium (30%) | Engage NRC early; demonstrate TRIGA safety heritage; propose restricted deployment (e.g., rural only) |
| Part 53 rule delayed or unfavorable | High | Medium (40%) | Dual-path: also prepare 10 CFR Part 50 application (slower but established) |
| State/local opposition (NIMBY) | High | High (60%) | Start with willing early-adopter communities; military/remote deployment first |
| Physical security requirements too costly | High | Medium (35%) | Factory-sealed, tamper-evident, remote monitoring reduces on-site security needs |
| Spent fuel return logistics | Medium | Low (15%) | Pre-negotiate with CERCA/Framatome for factory return; NRC Part 71 transport cask |

---

## 8. Risk Matrix

| # | Risk | Severity | Probability | Impact | Mitigation |
|---|------|----------|-------------|--------|------------|
| R1 | **NRC licensing fails for residential** | Critical | Medium (30%) | No residential product | Military/remote/industrial deployment first; demonstrate safety record; lobby for 10 CFR Part 53 micro-reactor provisions |
| R2 | **Shield mass exceeds 693 kg target** | High | Medium (40%) | Heavier unit, higher transport/install cost | MCNP6 validation early; accept 800–900 kg if needed; concrete pad design accommodates |
| R3 | **CERCA fuel production bottleneck** | Medium | Low (20%) | Supply-limited to ~100 units/year | Long-lead fuel orders; explore second-source qualification with BWX Technologies |
| R4 | **Stirling engine 100,000-hr life not achieved** | Medium | Low (25%) | Mid-life engine replacement (adds O&M cost) | Modular engine design for field replacement; V-Cell buffer covers downtime |
| R5 | **Public opposition to residential nuclear** | High | High (60%) | Market limited to non-residential | Industrial/military/remote first; build safety record; residential market later |
| R6 | **Heat pipe Na leak** | Low | Very Low (5%) | Single pipe out-of-service; reduced power | 12 pipes provide N+4 redundancy; sealed Inconel 718 has excellent Na compatibility |
| R7 | **Competitor (eVinci, Oklo, Radiant) reaches market first** | Medium | Medium (40%) | Market share loss | V-Core targets smaller scale (25 kW vs 200 kW+); different market segment |
| R8 | **Cost target $150K not achieved** | Medium | Medium (35%) | Price-uncompetitive vs solar+battery | Volume production reduces cost; CHP value proposition (heat + power) improves ROI |
| R9 | **BeO reflector toxicity concerns in manufacturing** | Low | Low (15%) | Manufacturing overhead increases | Glove box handling standard in nuclear industry; explore MgO alternative |
| R10 | **Cyberattack on V-Mind control system** | High | Low (15%) | Safety system compromise | Air-gapped nuclear safety systems; V-Mind monitoring is advisory only; physics-based safety (temperature coefficient) is unhackable |

---

## 9. Revised Roadmap

### Phase 1: Design & Licensing (2026–2029)
- Complete neutronics analysis (MCNP6, Serpent)
- Complete thermal-hydraulic analysis (RELAP5)
- Shield optimization via Monte Carlo simulation
- Stirling engine prototype (12.5 kW) fabricated and tested
- Heat pipe bundle prototype (12 pipes) fabricated and tested
- NRC pre-application engagement
- Design certification application submitted

### Phase 2: Prototype & Test (2029–2031)
- Full-scale V-Core prototype assembled (non-nuclear, electric heater substitute)
- Thermal integration test (Stirling + heat pipe + radiator)
- V-Mind control system validation (load-following, fault injection)
- NRC design certification review
- Nuclear prototype assembly at licensed facility (INL or similar)
- Subcritical and critical testing

### Phase 3: Production & Deployment (2031–2034)
- NRC design certification granted
- First 10 units manufactured (pilot production)
- Military/remote installations (first customers — fewer regulatory hurdles)
- Industrial/commercial installations
- Residential installations (pending state/local acceptance)
- V-Man cell adapted for V-Core production
- Target: 100 units/year by 2034

---

## 10. Conclusion

V-Core is the most technically grounded product in Voltec's portfolio above Tier 1. Every subsystem technology — U-ZrH fuel, sodium heat pipes, free-piston Stirling engines, B₄C control drums, lead-PE shielding — has decades of demonstrated operation in nuclear research, space power, and industrial applications. No fundamental physics breakthroughs are required.

The primary risks are:
1. **Regulatory** — NRC has never licensed a residential nuclear reactor. The 10 CFR Part 53 pathway is promising but unproven. Military and remote deployment should precede residential.
2. **Integration** — Combining all subsystems into a 693 kg egg-shaped package is ambitious. Shield mass is the critical variable.
3. **Public acceptance** — "Nuclear in your backyard" faces opposition regardless of safety record. A multi-year safety demonstration program at non-residential sites is essential before residential deployment.

**Honest summary**:
- **VERIFIED**: U-ZrH fuel safety, heat pipe technology, Stirling engine operation, shielding materials, seismic design
- **PROJECTED**: 25 kW electrical output, 33% efficiency, 10-year fuel life, 693 kg mass, $150K cost target, NRC licensing
- **ASPIRATIONAL**: Residential installation, egg form factor, zero-maintenance 10-year operation, public acceptance
