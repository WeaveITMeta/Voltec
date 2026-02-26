"""
V-Incinerator — Plasma Chamber  (Blender 4.4 headless mesh generator)
=====================================================================
Tungsten-lined DC plasma arc reactor. ID 1.2 m × H 1.5 m.
3 × 500 kW torch ports at 120° spacing, water-cooling jacket,
slag tap port at bottom, syngas outlet flange at top.
Multi-body assembly: main vessel + flanges + torch stubs + slag tap.

Run: blender --background --python this_script.py
"""
import bpy, bmesh, math, os

# ── Identity ──────────────────────────────────────────────────────────
PRODUCT   = "VIncinerator"
COMPONENT = "PlasmaChamber"
MATERIAL  = "Tungsten_W"
OUT_DIR   = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT_FILE  = f"{PRODUCT}_{COMPONENT}.glb"

# ── Dimensions (meters, from PATENT.md) ───────────────────────────────
INNER_R      = 0.60        # inner radius
WALL         = 0.05        # tungsten liner + cooling jacket
OUTER_R      = INNER_R + WALL
HEIGHT       = 1.50
FLANGE_R     = OUTER_R + 0.08
FLANGE_H     = 0.04
TORCH_R      = 0.08        # torch port stub radius
TORCH_LEN    = 0.20        # how far stubs protrude
SLAG_R       = 0.10        # slag tap radius
SLAG_LEN     = 0.15

# ── PBR Material ──────────────────────────────────────────────────────
PBR = {
    "base_color": (0.58, 0.56, 0.54, 1.0),  # tungsten grey
    "metallic": 1.0,
    "roughness": 0.40,
    "alpha": 1.0,
    "emission": (0.0, 0.0, 0.0, 1.0),
    "emission_strength": 0.0,
}
BEVEL_WIDTH = 0.003
BEVEL_SEGS  = 2

# ── Helpers ───────────────────────────────────────────────────────────
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
    mat.use_nodes = True; mat.use_backface_culling = True
    nodes = mat.node_tree.nodes; links = mat.node_tree.links; nodes.clear()
    bsdf = nodes.new('ShaderNodeBsdfPrincipled')
    bsdf.inputs['Base Color'].default_value = PBR["base_color"]
    bsdf.inputs['Metallic'].default_value = PBR["metallic"]
    bsdf.inputs['Roughness'].default_value = PBR["roughness"]
    bsdf.inputs['Alpha'].default_value = PBR["alpha"]
    bsdf.inputs['Emission Color'].default_value = PBR["emission"]
    bsdf.inputs['Emission Strength'].default_value = PBR["emission_strength"]
    out = nodes.new('ShaderNodeOutputMaterial'); out.location = (300, 0)
    links.new(bsdf.outputs['BSDF'], out.inputs['Surface'])
    return mat

def add_cylinder(radius, depth, verts=64, location=(0,0,0), rotation=(0,0,0)):
    """Add a cylinder and return it."""
    bpy.ops.mesh.primitive_cylinder_add(
        vertices=verts, radius=radius, depth=depth,
        location=location, rotation=rotation)
    return bpy.context.active_object

def bool_union(target, cutter):
    """Boolean union cutter into target, then delete cutter."""
    mod = target.modifiers.new("Union", 'BOOLEAN')
    mod.operation = 'UNION'; mod.object = cutter; mod.solver = 'EXACT'
    bpy.context.view_layer.objects.active = target
    bpy.ops.object.modifier_apply(modifier="Union")
    bpy.data.objects.remove(cutter, do_unlink=True)

# ── Geometry ──────────────────────────────────────────────────────────
def create_geometry():
    """Multi-body plasma chamber with torch ports, flanges, and slag tap."""

    # 1) Main vessel — thick-walled cylinder (hollow)
    bpy.ops.mesh.primitive_cylinder_add(vertices=64, radius=OUTER_R, depth=HEIGHT)
    vessel = bpy.context.active_object
    vessel.name = "vessel_outer"
    # Hollow it out with solidify
    sol = vessel.modifiers.new("Hollow", 'SOLIDIFY')
    sol.thickness = WALL; sol.offset = -1
    bpy.context.view_layer.objects.active = vessel
    bpy.ops.object.modifier_apply(modifier="Hollow")

    # 2) Top flange ring
    top_flange = add_cylinder(FLANGE_R, FLANGE_H, 64, (0, 0, HEIGHT/2 + FLANGE_H/2))
    # Cut center hole
    top_hole = add_cylinder(INNER_R, FLANGE_H + 0.01, 64, (0, 0, HEIGHT/2 + FLANGE_H/2))
    mod = top_flange.modifiers.new("Hole", 'BOOLEAN')
    mod.operation = 'DIFFERENCE'; mod.object = top_hole; mod.solver = 'EXACT'
    bpy.context.view_layer.objects.active = top_flange
    bpy.ops.object.modifier_apply(modifier="Hole")
    bpy.data.objects.remove(top_hole, do_unlink=True)
    bool_union(vessel, top_flange)

    # 3) Bottom flange ring
    bot_flange = add_cylinder(FLANGE_R, FLANGE_H, 64, (0, 0, -HEIGHT/2 - FLANGE_H/2))
    bot_hole = add_cylinder(INNER_R, FLANGE_H + 0.01, 64, (0, 0, -HEIGHT/2 - FLANGE_H/2))
    mod = bot_flange.modifiers.new("Hole", 'BOOLEAN')
    mod.operation = 'DIFFERENCE'; mod.object = bot_hole; mod.solver = 'EXACT'
    bpy.context.view_layer.objects.active = bot_flange
    bpy.ops.object.modifier_apply(modifier="Hole")
    bpy.data.objects.remove(bot_hole, do_unlink=True)
    bool_union(vessel, bot_flange)

    # 4) Three torch port stubs at 120° spacing, at mid-height
    for i in range(3):
        angle = math.radians(120 * i)
        cx = (OUTER_R + TORCH_LEN/2) * math.cos(angle)
        cy = (OUTER_R + TORCH_LEN/2) * math.sin(angle)
        # Horizontal stub — rotated to point radially outward
        stub = add_cylinder(TORCH_R, TORCH_LEN, 32,
                            (cx, cy, 0.0),
                            (0, math.pi/2, angle))
        # Add a flange collar at the end of each stub
        fcx = (OUTER_R + TORCH_LEN) * math.cos(angle)
        fcy = (OUTER_R + TORCH_LEN) * math.sin(angle)
        collar = add_cylinder(TORCH_R + 0.03, 0.02, 32,
                              (fcx, fcy, 0.0),
                              (0, math.pi/2, angle))
        bool_union(stub, collar)
        bool_union(vessel, stub)

    # 5) Slag tap port at bottom center
    slag_stub = add_cylinder(SLAG_R, SLAG_LEN, 32,
                             (0, 0, -HEIGHT/2 - FLANGE_H - SLAG_LEN/2))
    slag_collar = add_cylinder(SLAG_R + 0.04, 0.02, 32,
                               (0, 0, -HEIGHT/2 - FLANGE_H - SLAG_LEN))
    bool_union(slag_stub, slag_collar)
    bool_union(vessel, slag_stub)

    # 6) Syngas outlet stub at top center
    gas_stub = add_cylinder(0.12, 0.18, 32,
                            (0, 0, HEIGHT/2 + FLANGE_H + 0.09))
    gas_collar = add_cylinder(0.16, 0.02, 32,
                              (0, 0, HEIGHT/2 + FLANGE_H + 0.18))
    bool_union(gas_stub, gas_collar)
    bool_union(vessel, gas_stub)

    vessel.name = f"{PRODUCT}_{COMPONENT}"
    vessel.data.name = f"{PRODUCT}_{COMPONENT}_mesh"
    return vessel

# ── Polish ────────────────────────────────────────────────────────────
def polish(obj):
    bpy.context.view_layer.objects.active = obj
    bpy.ops.object.shade_auto_smooth()
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.mesh.select_all(action='SELECT')
    bpy.ops.uv.smart_project(angle_limit=math.radians(66), island_margin=0.02)
    bpy.ops.mesh.normals_make_consistent(inside=False)
    bpy.ops.mesh.remove_doubles(threshold=0.0001)
    bpy.ops.object.mode_set(mode='OBJECT')
    bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
    bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY', center='BOUNDS')

# ── Verify ────────────────────────────────────────────────────────────
def verify(obj):
    bm = bmesh.new(); bm.from_mesh(obj.data)
    f = len(bm.faces); q = sum(1 for face in bm.faces if len(face.verts) == 4)
    nm = sum(1 for e in bm.edges if not e.is_manifold)
    print(f"\n  MESH: {obj.name}  |  V:{len(bm.verts)} E:{len(bm.edges)} F:{f}")
    print(f"  Quads: {q}/{f} ({100*q/max(f,1):.0f}%)  |  Non-manifold: {nm}  |  Watertight: {'YES' if nm==0 else 'NO'}")
    bm.free()

# ── Export ────────────────────────────────────────────────────────────
def export(obj):
    os.makedirs(OUT_DIR, exist_ok=True)
    path = os.path.join(OUT_DIR, OUT_FILE)
    bpy.ops.object.select_all(action='DESELECT')
    obj.select_set(True); bpy.context.view_layer.objects.active = obj
    bpy.ops.export_scene.gltf(
        filepath=path, export_format='GLB', use_selection=True,
        export_apply=True, export_normals=True, export_materials='EXPORT',
        export_cameras=False, export_lights=False,
        export_animations=False, export_yup=True,
        export_draco_mesh_compression_enable=True,
        export_draco_mesh_compression_level=6)
    print(f"  EXPORTED: {path} ({os.path.getsize(path)/1024:.1f} KB)\n")

def main():
    clean_scene(); setup_scene()
    mat = create_material()
    obj = create_geometry()
    obj.data.materials.append(mat)
    polish(obj); verify(obj); export(obj)
    print(f"DONE: {PRODUCT}_{COMPONENT}")

if __name__ == "__main__":
    main()
