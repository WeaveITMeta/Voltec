
---
description: Create a new Voltec product from idea to patent to EustressEngine simulation files to product catalog entry. Follows the V-Cell reference pattern.
---

# Create Voltec Product — Idea → Patent → Simulation → Catalog

This workflow creates a complete Voltec product package following the V-Cell reference architecture. It takes a product idea through patent drafting, state-of-the-art validation, AAA-quality 3D mesh generation via Blender, EustressEngine simulation file generation, and product catalog registration.

**Blender Path**: `C:\Program Files\Blender Foundation\Blender 4.4\blender.exe`

## Prerequisites

- Product idea with: name, chemistry/mechanism, target specs, key innovations
- Familiarity with Voltec design language (see `docs/Voltec.md`)
- EustressEngine `.glb.toml` instance format knowledge (see any existing product's `README.md`)
- Blender 4.4+ installed at the path above

## Inputs

Gather these from the user before starting:

| Input | Example (V-Cell) | Required |
|-------|-------------------|----------|
| **Product name** | V-Cell | Yes |
| **One-line description** | Solid-state sodium-sulfur energy cell | Yes |
| **Product tier** | Tier 1: Foundation | Yes |
| **Key innovations** (2-5 bullet points) | Sc-NASICON electrolyte, Al hex lattice, S@VACNT cathode | Yes |
| **Target specs** (table of metrics vs benchmarks) | 900 Wh/kg vs 250 Wh/kg Li-Ion | Yes |
| **Bill of materials** (components with materials) | Housing (Al 6061-T6), Anode (Na), Electrolyte (Sc-NASICON), ... | Yes |
| **Physical dimensions** | 300×100×12mm prismatic | Yes |
| **Use cases / target customers** | Industrial storage, EV, grid, space | Yes |

---

## Step 1: Create Product Directory

Create the directory structure:

```
docs/Products/{ProductName}/
├── PATENT.md
├── SOTA_VALIDATION.md
├── EustressEngine_Requirements.md
├── README.md
└── V1/
    ├── meshes/
    │   └── scripts/     (Blender Python scripts)
    │   └── *.glb        (generated meshes)
    └── *.glb.toml       (instance files)
```

// turbo
```bash
mkdir -p "docs/Products/{ProductName}/V1/meshes/scripts"
```

---

## Step 2: Draft PATENT.md

Create `docs/Products/{ProductName}/PATENT.md` following this structure:

### Required Sections

1. **Title of Invention** — Formal patent title
2. **Abstract** — 1 paragraph summarizing the invention and key metrics
3. **Field of Invention** — Technical domain
4. **Background** — Limitations of current technology (comparison table), the problem, the breakthrough
5. **Summary of Invention** — Component list with materials
6. **Detailed Description** — Cross-section diagram (ASCII art), stacking/assembly configuration
7. **Core Technology Sections** (product-specific) — Chemistry/mechanism, key component deep-dives with:
   - Design rationale
   - Geometry (ASCII art where applicable)
   - Mechanical/electrical/thermal properties tables (SI units)
   - Manufacturing process for that component
8. **Thermal Management** — Heat generation model, thermal path diagram, operating envelope table
9. **Geometry & Mechanical Design** — Form factor table, housing material properties, mechanical load cases
10. **Performance Specifications** — Electrical/performance specs table, cycle/lifetime data, safety test results
11. **Manufacturing Process** — Process comparison table (vs conventional), production line steps (numbered), production targets (Year 1/3/5)
12. **Claims** — 8-12 patent claims (1 independent + dependents covering: composition, geometry, performance, method, multi-function components)
13. **EustressEngine Simulation Requirements** — Cross-reference to `EustressEngine_Requirements.md` and `SOTA_VALIDATION.md`, component→ECS mapping table, required realism properties table

### Style Rules

- All values in SI units
- Every material property must include: name, Young's modulus, Poisson's ratio, yield strength, ultimate strength, fracture toughness, hardness, thermal conductivity, specific heat, thermal expansion, melting point, density, friction (static/kinetic), restitution
- ASCII cross-section diagrams for physical products
- Comparison tables: always include current SOTA benchmark column
- Patent claims: Claim 1 independent, rest dependent; cover composition, geometry ranges, performance thresholds, manufacturing method

### Reference

Use `docs/Products/V-Cell/PATENT.md` as the gold-standard template.

---

## Step 3: Draft SOTA_VALIDATION.md

Create `docs/Products/{ProductName}/SOTA_VALIDATION.md` following this structure:

### Required Sections

1. **Preface: Honesty Framework** — Three-tier classification table (VERIFIED / PROJECTED / ASPIRATIONAL)
2. **Performance Metrics** — Each key spec rated against SOTA with tier classification
3. **Durability / Lifetime** — Cycle life, degradation model, comparison to published data
4. **Safety** — Failure modes, thermal stability, comparison
5. **Materials & Chemistry Feasibility** — Each material assessed for availability, cost, scalability
6. **Manufacturing Feasibility** — Process readiness level, equipment availability
7. **Risk Matrix** — Table: Risk | Severity | Probability | Mitigation
8. **Revised Roadmap** — Phase 1 (lab) → Phase 2 (pilot) → Phase 3 (production) with dates and milestones
9. **Conclusion** — Honest summary of what's proven vs aspirational

### Style Rules

- Every claim must have a tier tag: `VERIFIED`, `PROJECTED`, or `ASPIRATIONAL`
- Include literature citations where possible
- Risk matrix must cover at least: performance risk, manufacturing risk, supply chain risk, competitive risk, safety risk

### Reference

Use `docs/Products/V-Cell/SOTA_VALIDATION.md` as the gold-standard template.

---

## Step 4: Create EustressEngine_Requirements.md

Create `docs/Products/{ProductName}/EustressEngine_Requirements.md` mapping the product to EustressEngine's realism crate.

### Required Sections

1. **Required Crate Features** — Feature flags table
2. **MaterialProperties — Per Component** — One subsection per material with full `[material]` TOML block (14 base fields) + `[material.custom]` for domain-specific extensions. Each material must include a `role` tag.
3. **Instance File Structure** — File→Entity mapping table, standard `.glb.toml` section template, Transform layout table (position + scale for every component)
4. **Domain-Specific State** (e.g., `ElectrochemicalState`, `FluidState`, `KineticState`) — All fields with types, units, initial values, runtime update flow pseudocode
5. **ThermodynamicState** — Fields table + operating envelope table
6. **Domain Laws** (e.g., Electrochemistry Laws, Fluid Dynamics Laws) — Function reference table + calibrated constants table
7. **Realism Config** — TOML config block
8. **Structural Bundle Requirements** — Components table + priority notes for fracture-critical parts
9. **Deployment Checklist** — Copy instructions, pre-launch checks, runtime validation sanity checks with expected values

### Style Rules

- All TOML blocks must match the actual `.glb.toml` instance file format (flat `[material]`, not `[material.housing]`)
- Include `[material.custom]` with domain-specific extensions and `role` tag
- Runtime update pseudocode shows the tick-level simulation flow
- Deployment checklist includes 3+ concrete sanity-check assertions with expected values

### Reference

Use `docs/Products/V-Cell/EustressEngine_Requirements.md` as the gold-standard template.

---

## Step 5: Generate AAA Meshes via Blender

Using the PATENT.md cross-section, BOM, and dimensions, generate one `.glb` mesh per component via Blender's Python API running headlessly. Every mesh must look like it was crafted by the gods.

### 5.0 Patent Research (Required)

Before writing any Blender scripts, search Google Patents for real-world designs of each component type (e.g., "plasma gasification reactor cross section", "shell and tube heat exchanger patent", "wet scrubber tower design"). Extract:
- **Real-world form factors** — cylindrical vessels with flanges, nozzle stubs, support saddles
- **Key sub-features** — torch ports, tube sheets, stiffener rings, manways, rain caps
- **Dimensional proportions** — wall thicknesses, flange ratios, nozzle sizing

Combine patent research with PATENT.md dimensions to inform multi-body assembly scripts.

### 5.1 Generate Blender Python Scripts

Create one Python script per component at `V1/meshes/scripts/{ProductName}_{ComponentName}.py`.

Each script MUST follow these AAA standards:

#### Naming & Organization
- Mesh object named: `{ProductName}_{ComponentName}`
- Material named: `MAT_{ProductName}_{MaterialName}`
- Scene named: `Scene0` (EustressEngine convention)

#### Topology — God-Tier Standards
- **Quad-dominant** — No triangles except where geometrically required (cone tips, sphere poles)
- **Edge loops** — Clean, evenly spaced for deformation readiness
- **Subdivision-ready** — Correct at SubD level 0, 1, and 2
- **Bevel/chamfer** — ALL hard edges get a 2-segment bevel (0.3–1mm). No razor edges exist in real products
- **Manifold** — Watertight, no non-manifold edges, no duplicate verts, no interior faces
- **Normals** — All outward, auto-smooth at 30°
- **Scale applied** — All transforms applied. Scale = [1,1,1]
- **Origin** — Geometric center
- **Vertex budget** — 500–5,000 per component

#### PBR Materials — Photorealistic
- **Principled BSDF** for every material
- **Base Color** — Accurate to real material (see PBR reference table below)
- **Metallic** — 1.0 for metals, 0.0 for ceramics/polymers
- **Roughness** — Brushed metal 0.3–0.4, polished 0.05–0.15, ceramic 0.5–0.7, matte 0.8–0.95
- **Alpha** — 1.0 unless explicitly transparent
- **Emission** — Only for LEDs/indicators: strength 2.0–5.0
- No image textures — PBR values only (keeps GLB lightweight)

#### UV & Export
- Smart UV Project minimum; planar faces get planar projection
- Export: glTF Binary (.glb), Y-up, Draco compression, no cameras/lights/animations

#### Python Script Template

```python
"""
Blender Headless Mesh Generator
Product: {ProductName}  |  Component: {ComponentName}
Run: blender --background --python this_script.py
"""
import bpy, bmesh, math, os

PRODUCT = "{ProductName}"
COMPONENT = "{ComponentName}"
MATERIAL = "{MaterialName}"
OUT_DIR = r"{OutputDir}"
OUT_FILE = f"{PRODUCT}_{COMPONENT}.glb"

DIMS = {"width": 0.0, "height": 0.0, "depth": 0.0}  # meters

PBR = {
    "base_color": (0.75, 0.78, 0.80, 1.0),
    "metallic": 1.0,
    "roughness": 0.35,
    "alpha": 1.0,
    "emission": (0.0, 0.0, 0.0, 1.0),
    "emission_strength": 0.0,
}

BEVEL_WIDTH = 0.0005  # meters
BEVEL_SEGMENTS = 2

def clean_scene():
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete(use_global=False)
    for block in bpy.data.meshes:
        if block.users == 0: bpy.data.meshes.remove(block)
    for block in bpy.data.materials:
        if block.users == 0: bpy.data.materials.remove(block)

def setup_scene():
    bpy.context.scene.name = "Scene0"
    bpy.context.scene.unit_settings.system = 'METRIC'
    bpy.context.scene.unit_settings.scale_length = 1.0

def create_material():
    mat = bpy.data.materials.new(name=f"MAT_{PRODUCT}_{MATERIAL}")
    mat.use_nodes = True
    mat.use_backface_culling = True
    nodes = mat.node_tree.nodes
    links = mat.node_tree.links
    nodes.clear()
    bsdf = nodes.new('ShaderNodeBsdfPrincipled')
    bsdf.inputs['Base Color'].default_value = PBR["base_color"]
    bsdf.inputs['Metallic'].default_value = PBR["metallic"]
    bsdf.inputs['Roughness'].default_value = PBR["roughness"]
    bsdf.inputs['Alpha'].default_value = PBR["alpha"]
    bsdf.inputs['Emission Color'].default_value = PBR["emission"]
    bsdf.inputs['Emission Strength'].default_value = PBR["emission_strength"]
    output = nodes.new('ShaderNodeOutputMaterial')
    output.location = (300, 0)
    links.new(bsdf.outputs['BSDF'], output.inputs['Surface'])
    if PBR["alpha"] < 1.0:
        mat.blend_method = 'BLEND'
    return mat

def add_cyl(r, d, v=48, loc=(0,0,0), rot=(0,0,0)):
    bpy.ops.mesh.primitive_cylinder_add(vertices=v, radius=r, depth=d,
                                        location=loc, rotation=rot)
    return bpy.context.active_object

def add_cube(sx, sy, sz, loc=(0,0,0)):
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=loc)
    obj = bpy.context.active_object; obj.scale = (sx, sy, sz)
    bpy.ops.object.transform_apply(scale=True)
    return obj

def bool_op(target, cutter, op='UNION'):
    """Boolean operation — MUST use EXACT solver for clean manifold geometry."""
    mod = target.modifiers.new(op, 'BOOLEAN')
    mod.operation = op; mod.object = cutter; mod.solver = 'EXACT'
    bpy.context.view_layer.objects.active = target
    bpy.ops.object.modifier_apply(modifier=op)
    bpy.data.objects.remove(cutter, do_unlink=True)

def create_geometry():
    """CUSTOMIZE per component — use multi-body assembly with booleans.
    Build: main body → hollow with Solidify → add flanges, nozzles,
    stiffener rings, support structures via bool_op UNION.
    Reference PATENT.md dimensions + patent research for real-world form."""
    # Example: thick-walled vessel with flange
    vessel = add_cyl(OUTER_R, HEIGHT, 48)
    sol = vessel.modifiers.new("Hollow", 'SOLIDIFY')
    sol.thickness = WALL; sol.offset = -1
    bpy.context.view_layer.objects.active = vessel
    bpy.ops.object.modifier_apply(modifier="Hollow")
    # Add flanges, nozzle stubs, support saddles via bool_op(vessel, part, 'UNION')
    vessel.name = f"{PRODUCT}_{COMPONENT}"
    vessel.data.name = f"{PRODUCT}_{COMPONENT}_mesh"
    return vessel

def polish(obj):
    bevel = obj.modifiers.new("Bevel", 'BEVEL')
    bevel.width = BEVEL_WIDTH
    bevel.segments = BEVEL_SEGMENTS
    bevel.limit_method = 'ANGLE'
    bevel.angle_limit = math.radians(30)
    bevel.harden_normals = True
    bpy.context.view_layer.objects.active = obj
    bpy.ops.object.modifier_apply(modifier="Bevel")
    bpy.ops.object.shade_auto_smooth()
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.mesh.select_all(action='SELECT')
    bpy.ops.uv.smart_project(angle_limit=math.radians(66), island_margin=0.02)
    bpy.ops.mesh.normals_make_consistent(inside=False)
    bpy.ops.mesh.remove_doubles(threshold=0.0001)
    bpy.ops.object.mode_set(mode='OBJECT')
    bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
    bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY', center='BOUNDS')

def verify(obj):
    bm = bmesh.new()
    bm.from_mesh(obj.data)
    f = len(bm.faces)
    q = sum(1 for face in bm.faces if len(face.verts) == 4)
    nm = sum(1 for e in bm.edges if not e.is_manifold)
    print(f"\n  MESH: {obj.name}  |  V:{len(bm.verts)} E:{len(bm.edges)} F:{f}")
    print(f"  Quads: {q}/{f} ({100*q/max(f,1):.0f}%)  |  Non-manifold: {nm}  |  Watertight: {'YES' if nm==0 else 'FIX'}")
    bm.free()

def export(obj):
    os.makedirs(OUT_DIR, exist_ok=True)
    path = os.path.join(OUT_DIR, OUT_FILE)
    bpy.ops.object.select_all(action='DESELECT')
    obj.select_set(True)
    bpy.context.view_layer.objects.active = obj
    bpy.ops.export_scene.gltf(
        filepath=path, export_format='GLB', use_selection=True,
        export_apply=True, export_normals=True, export_materials='EXPORT',
        export_cameras=False, export_lights=False,
        export_animations=False, export_yup=True,
        export_draco_mesh_compression_enable=True,
        export_draco_mesh_compression_level=6,
    )
    print(f"  EXPORTED: {path} ({os.path.getsize(path)/1024:.1f} KB)\n")

def main():
    clean_scene()
    setup_scene()
    mat = create_material()
    obj = create_geometry()
    obj.data.materials.append(mat)
    polish(obj)
    verify(obj)
    export(obj)

if __name__ == "__main__":
    main()
```

### 5.2 Geometry Recipes

Customize `create_geometry()` per component type:

**Prismatic Housing (shell)**
```python
bpy.ops.mesh.primitive_cube_add(size=1.0)
obj = bpy.context.active_object
obj.scale = (w, h, d)
bpy.ops.object.transform_apply(scale=True)
solidify = obj.modifiers.new("Shell", 'SOLIDIFY')
solidify.thickness = wall_thickness
solidify.offset = -1
bpy.ops.object.modifier_apply(modifier="Shell")
```

**Cylindrical Terminal**
```python
bpy.ops.mesh.primitive_cylinder_add(vertices=32, radius=r, depth=h)
```

**Sphere (LED)**
```python
bpy.ops.mesh.primitive_uv_sphere_add(segments=32, ring_count=16, radius=r)
```

**Thin Membrane (electrolyte, electrode)**
```python
bpy.ops.mesh.primitive_cube_add(size=1.0)
obj = bpy.context.active_object
obj.scale = (w, thickness, d)
bpy.ops.object.transform_apply(scale=True)
bpy.ops.object.mode_set(mode='EDIT')
bpy.ops.mesh.loopcut_slide(MESH_OT_loopcut={"number_cuts": 4, "smoothness": 0})
bpy.ops.object.mode_set(mode='OBJECT')
```

**Honeycomb Hex Lattice**
```python
bm = bmesh.new()
for i in range(6):
    angle = math.radians(60 * i + 30)
    x, y = hex_radius * math.cos(angle), hex_radius * math.sin(angle)
    bm.verts.new((x, y, -depth/2))
    bm.verts.new((x, y, depth/2))
# Build faces, array modifiers for lattice pattern
```

**Tapered / Conical**
```python
bpy.ops.mesh.primitive_cone_add(vertices=32, radius1=r1, radius2=r2, depth=h)
```

### 5.3 Run Blender Headless

Execute each script — Blender runs in background, no GUI.

**IMPORTANT**: Cascade MUST run these scripts automatically. Do NOT leave mesh generation for the user. Generate the scripts, then run them, then create `.glb.toml` files referencing the generated custom meshes.

// turbo
```powershell
$blender = "C:\Program Files\Blender Foundation\Blender 4.4\blender.exe"
$scripts = Get-ChildItem "docs/Products/{ProductName}/V1/meshes/scripts" -Filter "*.py" | Sort-Object Name
foreach ($s in $scripts) {
    Write-Host "Generating: $($s.BaseName)..." -ForegroundColor Cyan
    & $blender --background --python $s.FullName 2>&1 |
        Select-String "MESH:|Quads:|EXPORTED:|DONE"
}
```

Verify each export: Quads > 80%, Non-manifold = 0, Watertight = YES.

After successful mesh generation, list all `.glb` files to confirm they exist:

// turbo
```powershell
Get-ChildItem "docs/Products/{ProductName}/V1/meshes" -Filter "*.glb" | Format-Table Name, @{N='KB';E={[math]::Round($_.Length/1024,1)}}
```

### 5.4 Create .glb.toml Instance Files from Generated Meshes

After mesh generation, create one `.glb.toml` instance file per component in `V1/`. The `.glb` meshes stay in `V1/meshes/` as the source of truth. Only `.glb.toml` files live in `V1/` — they reference the meshes via `[asset] mesh`.

The flow in one swift motion per component:
1. Read the generated `.glb` filename from `V1/meshes/`
2. Create `V1/{Product}_{Component}.glb.toml` with `[asset] mesh` pointing at the mesh
3. Add `[transform]`, `[properties]`, `[metadata]`, `[material]`, `[thermodynamic]`, and optionally `[electrochemical]` sections with realism data from PATENT.md and EustressEngine_Requirements.md

// turbo
```powershell
# Verify all meshes exist, then list the .glb.toml files that should be created
Get-ChildItem "docs/Products/{ProductName}/V1/meshes" -Filter "*.glb" | ForEach-Object {
    $toml = "docs/Products/{ProductName}/V1/$($_.BaseName).glb.toml"
    Write-Host "$($_.Name) -> $toml"
}
```

**Result**: `V1/` contains only `.glb.toml` files. `V1/meshes/` contains the `.glb` meshes + `scripts/` with the Blender Python sources.

### 5.5 PBR Material Reference — Voltec Design Language

| Material | Base Color (RGBA) | Metallic | Roughness | Notes |
|----------|-------------------|----------|-----------|-------|
| Brushed Aluminum | (0.75, 0.78, 0.80, 1.0) | 1.0 | 0.35 | Housing, structural |
| Polished Aluminum | (0.91, 0.92, 0.93, 1.0) | 1.0 | 0.08 | Terminals |
| Sodium Metal | (0.85, 0.85, 0.75, 1.0) | 1.0 | 0.4 | Soft waxy sheen |
| NASICON Ceramic | (0.95, 0.95, 0.90, 0.85) | 0.0 | 0.55 | Translucent white |
| Carbon/CNT | (0.05, 0.05, 0.05, 1.0) | 0.0 | 0.85 | Near-black matte |
| Sulfur | (0.85, 0.80, 0.15, 1.0) | 0.0 | 0.6 | Yellow crystalline |
| Aluminum Nitride | (0.85, 0.85, 0.80, 1.0) | 0.0 | 0.5 | Off-white ceramic |
| Al Hex Lattice | (0.80, 0.82, 0.85, 0.7) | 1.0 | 0.3 | Semi-transparent |
| Copper | (0.95, 0.64, 0.54, 1.0) | 1.0 | 0.25 | Warm metallic |
| Steel | (0.55, 0.56, 0.58, 1.0) | 1.0 | 0.4 | Cool grey |
| Rubber/Gasket | (0.15, 0.15, 0.15, 1.0) | 0.0 | 0.9 | Near-black rough |
| Glass/Crystal | (0.95, 0.95, 0.98, 0.3) | 0.0 | 0.05 | Transparent smooth |
| PCB (FR4) | (0.05, 0.30, 0.15, 1.0) | 0.0 | 0.7 | Dark green matte |
| Xenon Blue LED | (0.0, 0.75, 1.0, 1.0) | 0.0 | 0.1 | Emission: 5.0 |
| Status Green LED | (0.1, 0.95, 0.2, 1.0) | 0.0 | 0.1 | Emission: 3.0 |
| Status Red LED | (1.0, 0.1, 0.05, 1.0) | 0.0 | 0.1 | Emission: 3.0 |
| Voltec White | (1.0, 1.0, 1.0, 1.0) | 0.0 | 0.3 | Branding |
| Voltec Black | (0.04, 0.04, 0.04, 1.0) | 0.0 | 0.5 | Structure |

---

## Step 6: Create .glb.toml Instance Files

Create one `.glb.toml` file per physical component in `docs/Products/{ProductName}/V1/`.

### File Naming Convention

```
{ProductName}_{ComponentName}.glb.toml
```

### Asset Reference

After Step 5, point each instance at its custom mesh:

```toml
[asset]
mesh = "assets/meshes/products/{ProductName}/{ProductName}_{ComponentName}.glb"
scene = "Scene0"
```

**IMPORTANT**: Generate a Blender script for EVERY component in Step 5. Every `.glb.toml` should reference its own custom mesh. Only fall back to a primitive if the component is trivially simple (e.g., a single sphere LED):

| Mesh ID | File | Geometry | Typical Use |
|---------|------|----------|-------------|
| `block` | `assets/meshes/block.glb` | Unit cube | Housings, plates, pads |
| `ball` | `assets/meshes/ball.glb` | Unit sphere | LEDs, sensors |
| `cylinder` | `assets/meshes/cylinder.glb` | Unit cylinder | Terminals, pipes |
| `wedge` | `assets/meshes/wedge.glb` | Unit wedge | Angled elements |
| `cone` | `assets/meshes/cone.glb` | Unit cone | Nozzles |

> Primitives are unit meshes — `[transform] scale` in meters gives real-world dimensions.

### Template for AdvancedPart (with realism)

```toml
# {ProductName} {ComponentName} — {MaterialName}
# {Brief description of this component's role}

[asset]
mesh = "assets/meshes/products/{ProductName}/{ProductName}_{ComponentName}.glb"
scene = "Scene0"

[transform]
position = [x, y, z]              # meters, Y-up
rotation = [0.0, 0.0, 0.0, 1.0]  # quaternion [x, y, z, w]
scale = [w, h, d]                 # meters (real dimensions)

[properties]
color = [r, g, b, a]              # 0.0-1.0 RGBA
transparency = 0.0
anchored = true
can_collide = true
cast_shadow = true
reflectance = 0.0

[metadata]
class_name = "AdvancedPart"
archivable = true
created = "{ISO 8601 date}"
last_modified = "{ISO 8601 date}"

[material]
name = "{Material Name}"
young_modulus = 0.0       # Pa
poisson_ratio = 0.0
yield_strength = 0.0     # Pa
ultimate_strength = 0.0  # Pa
fracture_toughness = 0.0 # Pa·√m
hardness = 0.0           # HV
thermal_conductivity = 0.0  # W/(m·K)
specific_heat = 0.0      # J/(kg·K)
thermal_expansion = 0.0  # 1/K
melting_point = 0.0      # K
density = 0.0            # kg/m³
friction_static = 0.0
friction_kinetic = 0.0
restitution = 0.0

[material.custom]
role = "{component_role}"
# Add domain-specific properties here

[thermodynamic]
temperature = 298.15     # K
pressure = 101325.0      # Pa
volume = 0.0             # m³
internal_energy = 0.0    # J
entropy = 0.0            # J/K
enthalpy = 0.0           # J
moles = 1.0              # mol

# Include [electrochemical] only for electrochemically active components:
# [electrochemical]
# voltage = 0.0
# terminal_voltage = 0.0
# capacity_ah = 0.0
# soc = 1.0
# current = 0.0
# internal_resistance = 0.0
# ionic_conductivity = 0.0
# cycle_count = 0
# c_rate = 0.0
# capacity_retention = 1.0
# heat_generation = 0.0
# dendrite_risk = 0.0
```

### Template for Part (visual only, no realism)

```toml
# {ProductName} {ComponentName} — {Description}

[asset]
mesh = "assets/meshes/products/{ProductName}/{ProductName}_{ComponentName}.glb"
scene = "Scene0"

[transform]
position = [x, y, z]
rotation = [0.0, 0.0, 0.0, 1.0]
scale = [w, h, d]

[properties]
color = [r, g, b, a]
transparency = 0.0
anchored = true
can_collide = true
cast_shadow = true
reflectance = 0.0

[metadata]
class_name = "Part"
archivable = true
created = "{ISO 8601 date}"
last_modified = "{ISO 8601 date}"
```

### Layout Rules

- All position/scale values in **meters** (not studs, not centimeters)
- Place the product assembly centered at origin, Y-up
- Stack internal components along Y axis
- Terminals/connectors extend above the main body
- Status LEDs use `ball.glb`, small scale, `cast_shadow = false`
- `color` as linear RGBA floats 0.0–1.0 (not sRGB 0–255)
- `rotation` as quaternion `[x, y, z, w]` (not Euler angles)

---

## Step 7: Create README.md

Create `docs/Products/{ProductName}/README.md` documenting the `.glb.toml` blueprint package.

### Required Sections

1. **Overview** — One paragraph describing what this directory contains
2. **Architecture** — ASCII tree showing `assets/meshes/` → `Workspace/` relationship
3. **Instance Files** — Table: File | Mesh | Class | Realism Sections
4. **Import into EustressEngine** — Copy-to-Workspace instructions + programmatic spawn Rust snippet
5. **Coordinate System** — Origin, axes, scale convention
6. **Entity Hierarchy** — ASCII tree of all `.glb.toml` files with class/material annotations
7. **Realism Components Attached** — Bullet list mapping TOML sections → ECS components
8. **Custom Material Extensions** — Bullet list of `[material.custom]` keys used

### Reference

Use `docs/Products/V-Cell/README.md` as the gold-standard template.

---

## Step 8: Update Products.md

Add the new product to `docs/Products/Products.md` in the correct tier section.

### Entry Format

```markdown
### {ProductName}
**{One-Line Description}**

{2-3 sentence description connecting to the Voltec flywheel.}

| Spec | Value |
|------|-------|
| {Key Spec 1} | {Value} |
| {Key Spec 2} | {Value} |
| ... | ... |

**Use Cases**: {comma-separated list}
```

### Placement Rules

- **Tier 1: Foundation** — Products shipping now or in development for near-term revenue
- **Tier 2: Platform** — Software/platform products shipping in 18 months
- **Tier 3: Horizon** — Moonshot products 3-5 years out
- Insert alphabetically within the correct tier section
- Add a `---` separator between entries

---

## Step 9: Final Verification

After all files are created, verify:

**Documents**
- [ ] `PATENT.md` has all 13+ sections, SI units throughout, 8+ claims
- [ ] `SOTA_VALIDATION.md` has honesty tiers on every claim, risk matrix, revised roadmap
- [ ] `EustressEngine_Requirements.md` has all materials with 14 base fields, deployment checklist with sanity checks
- [ ] `README.md` documents all instance files with import instructions
- [ ] `Products.md` has the new entry in the correct tier

**Meshes (Step 5)**
- [ ] Every `.glb` file < 500 KB (Draco compressed)
- [ ] Every mesh watertight (non-manifold = 0)
- [ ] Every mesh quad-dominant (> 80% quads)
- [ ] Vertex count per component: 500–5,000
- [ ] All objects named `{ProductName}_{ComponentName}`
- [ ] All materials named `MAT_{ProductName}_{MaterialName}`
- [ ] Scene named `Scene0`
- [ ] All hard edges beveled, normals consistent, UVs unwrapped
- [ ] PBR materials match real-world appearance
- [ ] No cameras, lights, or animations in GLB files
- [ ] Y-up coordinate system (glTF/Bevy standard)

**Instance Files (Step 6)**
- [ ] `V1/` has one `.glb.toml` per physical component with correct naming
- [ ] All `.glb.toml` `[asset]` sections point to custom meshes from Step 5 (or fallback primitives)
- [ ] All `.glb.toml` files use flat `[material]` (not `[material.name]`)
- [ ] All `AdvancedPart` instances have `[material]` + `[thermodynamic]`, and `[electrochemical]` only where applicable
- [ ] Every `[material.custom]` has a `role` tag
- [ ] No references to deprecated `.eustressengine` RON/JSON format anywhere

---

## Quick Reference: File Checklist

```
docs/Products/{ProductName}/
├── PATENT.md                          # Technical patent specification
├── SOTA_VALIDATION.md                 # Claims validation & risk assessment
├── EustressEngine_Requirements.md     # Realism crate property mapping
├── README.md                          # Blueprint documentation
└── V1/                                # EustressEngine instance + mesh files
    ├── meshes/
    │   ├── scripts/                   # Blender Python scripts (one per component)
    │   │   ├── {Product}_{Comp1}.py
    │   │   └── {Product}_{Comp2}.py
    │   ├── {Product}_{Comp1}.glb      # Generated AAA meshes
    │   └── {Product}_{Comp2}.glb
    ├── {Product}_{Comp1}.glb.toml     # Instance files with realism
    └── {Product}_{Comp2}.glb.toml
```

## Quick Reference: Pipeline

```
User Idea
  ↓
[1] mkdir docs/Products/{Name}/V1/meshes/scripts
  ↓
[2] PATENT.md — dimensions, BOM, cross-section, claims
  ↓
[3] SOTA_VALIDATION.md — honesty tiers, risk matrix
  ↓
[4] EustressEngine_Requirements.md — material tables, state fields, laws
  ↓
[5] Patent research → Blender Python scripts → blender --background → AAA .glb meshes in V1/meshes/
  ↓
[6] .glb.toml instance files in V1/ → point [asset] at meshes + add realism sections
  ↓
[7] README.md — blueprint docs
  ↓
[8] Products.md — catalog entry
  ↓
[9] Verification checklist
  ↓
DONE — God-tier product ready for EustressEngine
```
