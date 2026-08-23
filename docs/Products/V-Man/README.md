# V-Man — Autonomous Manufacturing Cell

**Tier**: 2 (Platform)  
**Status**: Pre-Filing Draft  
**Version**: V1  
**Ship Target**: 18 months  

---

## Overview

V-Man is a modular, containerized robotic manufacturing cell achieving ≥95% autonomous operation (lights-out / dark factory mode). The entire factory — robots, vision, tooling, conveyors, compute, and power — ships inside a single ISO 40-foot high-cube container and deploys to production in ≤72 hours.

**Initial deployment**: V-Cell battery assembly (7,200 cells/day).  
**General capability**: Any discrete manufacturing process via software-defined recipes.

---

## Key Specifications

| Parameter | Value |
|-----------|-------|
| Form Factor | ISO 40' HC container (12.192 × 2.438 × 2.896 m) |
| Robotic Arms | 4–6 × 6-axis, 20 kg payload, ±0.02 mm repeatability |
| Vision | 3D LIDAR + RGB-D + structured light, AI-accelerated |
| Control Stack | Rust-native, EtherCAT (1 ms cycle), Vortex edge AI |
| Tool Magazine | 12 slots, RFID tracking, <5 s auto-change |
| Conveyor | 10 m precision belt, variable speed, ±0.5 mm accuracy |
| Power | 400V 3-phase, 25 kW peak / 12 kW average, UPS backup |
| Autonomy | ≥95% lights-out, ≤1 human intervention per shift |
| Setup Time | ≤72 hours delivery-to-production |
| Cost Target | $1.2M (Year 1) → $500K (Year 5) |

---

## Directory Structure

```
docs/Products/V-Man/
├── PATENT.md                          # Full patent specification (17 sections, 12 claims)
├── SOTA_VALIDATION.md                 # Three-tier honesty framework, risk matrix
├── EustressEngine_Requirements.md     # Material properties, domain state, deployment checklist
├── README.md                          # This file
└── V1/
    ├── VMan_Chassis.glb.toml          # ISO container chassis — S355J2 Steel
    ├── VMan_RoboticArm.glb.toml       # 6-axis arm — Al 7075-T6
    ├── VMan_VisionSystem.glb.toml     # LIDAR + camera array — Al 6061-T6
    ├── VMan_ToolMagazine.glb.toml     # End-effector rack — Al 6061-T6
    ├── VMan_EndEffectorKit.glb.toml   # Gripper/tool display — Al 6061-T6
    ├── VMan_Conveyor.glb.toml         # Belt transport — S355J2 Steel
    ├── VMan_ControlCabinet.glb.toml   # Compute enclosure — 316L SS
    ├── VMan_PowerDistribution.glb.toml # PDU + UPS — S235JR Steel
    ├── VMan_Pneumatics.glb.toml       # Compressor module — Al 6061-T6
    ├── VMan_SafetyEnclosure.glb.toml  # Light curtains + e-stops — Polycarbonate
    ├── VMan_SensorSuite.glb.toml      # Distributed sensors — Al 6061-T6
    ├── VMan_HMI.glb.toml              # Touchscreen panel — Gorilla Glass
    ├── VMan_StatusArray.glb.toml      # LED status bar — Polycarbonate
    └── meshes/
        ├── VMan_Chassis.glb            # 16.7 KB, 1056 verts, 99% quads
        ├── VMan_RoboticArm.glb         # 61.6 KB, 2939 verts, 94% quads
        ├── VMan_VisionSystem.glb       # 32.0 KB, 1215 verts, 91% quads
        ├── VMan_ToolMagazine.glb       # 42.9 KB, 2248 verts, 94% quads
        ├── VMan_EndEffectorKit.glb     # 15.7 KB, 636 verts, 67% quads
        ├── VMan_Conveyor.glb           # 37.0 KB, 2348 verts, 100% quads
        ├── VMan_ControlCabinet.glb     # 24.7 KB, 1048 verts, 99% quads
        ├── VMan_PowerDistribution.glb  # 20.0 KB, 896 verts, 100% quads
        ├── VMan_Pneumatics.glb         # 40.2 KB, 1703 verts, 87% quads
        ├── VMan_SafetyEnclosure.glb    # 36.5 KB, 2120 verts, 99% quads
        ├── VMan_SensorSuite.glb        # 90.7 KB, 3616 verts, 94% quads
        ├── VMan_StatusArray.glb        # 20.9 KB, 972 verts, 96% quads
        ├── VMan_HMI.glb               # 23.8 KB, 944 verts, 98% quads
        └── scripts/                    # 13 Blender Python generators
            ├── VMan_Chassis.py
            ├── VMan_RoboticArm.py
            ├── VMan_VisionSystem.py
            ├── VMan_ToolMagazine.py
            ├── VMan_EndEffectorKit.py
            ├── VMan_Conveyor.py
            ├── VMan_ControlCabinet.py
            ├── VMan_PowerDistribution.py
            ├── VMan_Pneumatics.py
            ├── VMan_SafetyEnclosure.py
            ├── VMan_SensorSuite.py
            ├── VMan_HMI.py
            └── VMan_StatusArray.py
```

---

## Component Inventory

| Component | Material | class_name | GLB KB | Verts | Quads% | Watertight |
|-----------|----------|------------|--------|-------|--------|------------|
| Chassis | S355J2 Structural Steel | AdvancedPart | 16.7 | 1,056 | 99% | ✅ |
| RoboticArm | Aluminum 7075-T6 | AdvancedPart | 61.6 | 2,939 | 94% | ✅ |
| VisionSystem | Aluminum 6061-T6 | AdvancedPart | 32.0 | 1,215 | 91% | ✅ |
| ToolMagazine | Aluminum 6061-T6 | AdvancedPart | 42.9 | 2,248 | 94% | ✅ |
| EndEffectorKit | Aluminum 6061-T6 | Part | 15.7 | 636 | 67% | 6 NM |
| Conveyor | S355J2 Structural Steel | AdvancedPart | 37.0 | 2,348 | 100% | ✅ |
| ControlCabinet | 316L Stainless Steel | AdvancedPart | 24.7 | 1,048 | 99% | ✅ |
| PowerDistribution | S235JR Steel | Part | 20.0 | 896 | 100% | ✅ |
| Pneumatics | Aluminum 6061-T6 | Part | 40.2 | 1,703 | 87% | ✅ |
| SafetyEnclosure | Polycarbonate | Part | 36.5 | 2,120 | 99% | ✅ |
| SensorSuite | Aluminum 6061-T6 | Part | 90.7 | 3,616 | 94% | ✅ |
| HMI | Gorilla Glass / Aluminum | Part | 23.8 | 944 | 98% | ✅ |
| StatusArray | Polycarbonate | Part | 20.9 | 972 | 96% | 1 NM |
| **Total** | — | — | **462.7** | **21,741** | — | **11/13** |

---

## EustressEngine Import Instructions

### Step 1: Deploy GLB Meshes

Copy all `.glb` files from `V1/meshes/` to:

```
C:\Users\miksu\Documents\Eustress\Universe1\spaces\Space1\assets\meshes\products\V-Man\
```

### Step 2: Deploy Instance Files

Copy all `.glb.toml` files from `V1/` to:

```
C:\Users\miksu\Documents\Eustress\Universe1\spaces\Space1\Workspace\
```

### Step 3: Verify

- EustressEngine auto-discovers `.glb.toml` files in `Workspace/` on load
- All `[asset] mesh` paths reference `assets/meshes/products/V-Man/VMan_{Component}.glb`
- Positions are in **meters**, Y-up
- Colors are **linear RGBA** 0.0–1.0
- Rotations are **quaternion** [x, y, z, w]
- Timestamps are **ISO 8601**

---

## Regenerating Meshes

To regenerate any mesh from its Blender script:

```powershell
$blender = "C:\Program Files\Blender Foundation\Blender 4.4\blender.exe"
& $blender --background --python "E:\Workspace\Voltec\docs\Products\V-Man\V1\meshes\scripts\VMan_Chassis.py"
```

To regenerate all meshes:

```powershell
$blender = "C:\Program Files\Blender Foundation\Blender 4.4\blender.exe"
Get-ChildItem "E:\Workspace\Voltec\docs\Products\V-Man\V1\meshes\scripts" -Filter "*.py" |
    ForEach-Object { & $blender --background --python $_.FullName }
```

---

## Related Documents

- [PATENT.md](./PATENT.md) — Full patent specification
- [SOTA_VALIDATION.md](./SOTA_VALIDATION.md) — State-of-the-art validation & risk assessment
- [EustressEngine_Requirements.md](./EustressEngine_Requirements.md) — Simulation property mapping
- [Products.md](../Products.md) — Voltec product catalog

---

*V-Man: The factory that ships in a box.*
