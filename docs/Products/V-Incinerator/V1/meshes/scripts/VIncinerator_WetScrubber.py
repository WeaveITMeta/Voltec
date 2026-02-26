"""
V-Incinerator — Wet Scrubber Column  (Blender 4.4 headless)
============================================================
Hastelloy C-276 counter-current packed column for acid gas neutralization.
Tall vertical cylinder with gas inlet at bottom, spray nozzle stubs at top,
liquid drain at bottom, packed bed section (external rings visible),
mist eliminator zone, access manway, support skirt.

Run: blender --background --python this_script.py
"""
import bpy, bmesh, math, os

PRODUCT   = "VIncinerator"
COMPONENT = "WetScrubber"
MATERIAL  = "Hastelloy_C276"
OUT_DIR   = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT_FILE  = f"{PRODUCT}_{COMPONENT}.glb"

# ── Dimensions ────────────────────────────────────────────────────────
SHELL_R   = 0.50
WALL      = 0.012
OUTER_R   = SHELL_R + WALL
HEIGHT    = 3.00
FLANGE_R  = OUTER_R + 0.06
FLANGE_H  = 0.035
GAS_IN_R  = 0.12           # gas inlet nozzle
GAS_IN_L  = 0.18
GAS_OUT_R = 0.10           # clean gas outlet (top)
GAS_OUT_L = 0.20
DRAIN_R   = 0.06           # liquid drain
DRAIN_L   = 0.12
MANWAY_R  = 0.20           # access manway
MANWAY_L  = 0.10
SKIRT_R   = OUTER_R + 0.04 # support skirt
SKIRT_H   = 0.40
RING_R    = OUTER_R + 0.015 # external stiffener rings
RING_H    = 0.025

PBR = {
    "base_color": (0.60, 0.62, 0.60, 1.0),  # Hastelloy grey-green
    "metallic": 1.0,
    "roughness": 0.35,
    "alpha": 1.0,
    "emission": (0.0, 0.0, 0.0, 1.0),
    "emission_strength": 0.0,
}

def clean_scene():
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete(use_global=False)
    for b in bpy.data.meshes:
        if b.users == 0: bpy.data.meshes.remove(b)
    for b in bpy.data.materials:
        if b.users == 0: bpy.data.materials.remove(b)

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

def add_cyl(r, d, v=48, loc=(0,0,0), rot=(0,0,0)):
    bpy.ops.mesh.primitive_cylinder_add(vertices=v, radius=r, depth=d,
                                        location=loc, rotation=rot)
    return bpy.context.active_object

def bool_op(target, cutter, op='UNION'):
    mod = target.modifiers.new(op, 'BOOLEAN')
    mod.operation = op; mod.object = cutter; mod.solver = 'EXACT'
    bpy.context.view_layer.objects.active = target
    bpy.ops.object.modifier_apply(modifier=op)
    bpy.data.objects.remove(cutter, do_unlink=True)

def create_geometry():
    """Wet scrubber column with nozzles, stiffener rings, manway, skirt."""

    # 1) Main column — hollow vertical cylinder
    col = add_cyl(OUTER_R, HEIGHT, 48)
    sol = col.modifiers.new("Hollow", 'SOLIDIFY')
    sol.thickness = WALL; sol.offset = -1
    bpy.context.view_layer.objects.active = col
    bpy.ops.object.modifier_apply(modifier="Hollow")

    # 2) Top and bottom flanges
    for z, sign in [(HEIGHT/2 + FLANGE_H/2, 1), (-HEIGHT/2 - FLANGE_H/2, -1)]:
        fl = add_cyl(FLANGE_R, FLANGE_H, 48, (0, 0, z))
        hole = add_cyl(SHELL_R, FLANGE_H + 0.01, 48, (0, 0, z))
        bool_op(fl, hole, 'DIFFERENCE')
        bool_op(col, fl, 'UNION')

    # 3) External stiffener rings (4 evenly spaced)
    for i in range(4):
        z = -HEIGHT/2 + HEIGHT * (i + 1) / 5
        ring = add_cyl(RING_R, RING_H, 48, (0, 0, z))
        ring_hole = add_cyl(OUTER_R - 0.001, RING_H + 0.01, 48, (0, 0, z))
        bool_op(ring, ring_hole, 'DIFFERENCE')
        bool_op(col, ring, 'UNION')

    # 4) Gas inlet nozzle (bottom side, horizontal)
    gi = add_cyl(GAS_IN_R, GAS_IN_L, 32,
                 (OUTER_R + GAS_IN_L/2, 0, -HEIGHT/2 + 0.40),
                 (0, math.pi/2, 0))
    gi_col = add_cyl(GAS_IN_R + 0.03, 0.02, 32,
                     (OUTER_R + GAS_IN_L, 0, -HEIGHT/2 + 0.40),
                     (0, math.pi/2, 0))
    bool_op(gi, gi_col, 'UNION')
    bool_op(col, gi, 'UNION')

    # 5) Clean gas outlet (top, vertical)
    go = add_cyl(GAS_OUT_R, GAS_OUT_L, 32, (0, 0, HEIGHT/2 + FLANGE_H + GAS_OUT_L/2))
    go_col = add_cyl(GAS_OUT_R + 0.03, 0.02, 32, (0, 0, HEIGHT/2 + FLANGE_H + GAS_OUT_L))
    bool_op(go, go_col, 'UNION')
    bool_op(col, go, 'UNION')

    # 6) Liquid drain (bottom, vertical down)
    dr = add_cyl(DRAIN_R, DRAIN_L, 24, (0, 0, -HEIGHT/2 - FLANGE_H - DRAIN_L/2))
    dr_col = add_cyl(DRAIN_R + 0.02, 0.015, 24, (0, 0, -HEIGHT/2 - FLANGE_H - DRAIN_L))
    bool_op(dr, dr_col, 'UNION')
    bool_op(col, dr, 'UNION')

    # 7) Two spray nozzle stubs (near top, horizontal, 180° apart)
    for angle in [0, math.pi]:
        sx = (OUTER_R + 0.06) * math.cos(angle)
        sy = (OUTER_R + 0.06) * math.sin(angle)
        sn = add_cyl(0.04, 0.12, 24,
                      (sx, sy, HEIGHT/2 - 0.30),
                      (0, math.pi/2, angle))
        bool_op(col, sn, 'UNION')

    # 8) Access manway (mid-height, horizontal)
    mw = add_cyl(MANWAY_R, MANWAY_L, 32,
                 (0, OUTER_R + MANWAY_L/2, 0),
                 (math.pi/2, 0, 0))
    mw_col = add_cyl(MANWAY_R + 0.04, 0.025, 32,
                     (0, OUTER_R + MANWAY_L, 0),
                     (math.pi/2, 0, 0))
    bool_op(mw, mw_col, 'UNION')
    bool_op(col, mw, 'UNION')

    # 9) Support skirt (conical base)
    skirt = add_cyl(SKIRT_R, SKIRT_H, 48, (0, 0, -HEIGHT/2 - FLANGE_H - DRAIN_L - SKIRT_H/2))
    sk_hole = add_cyl(SKIRT_R - 0.015, SKIRT_H + 0.01, 48,
                      (0, 0, -HEIGHT/2 - FLANGE_H - DRAIN_L - SKIRT_H/2))
    bool_op(skirt, sk_hole, 'DIFFERENCE')
    bool_op(col, skirt, 'UNION')

    col.name = f"{PRODUCT}_{COMPONENT}"
    col.data.name = f"{PRODUCT}_{COMPONENT}_mesh"
    return col

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

def verify(obj):
    bm = bmesh.new(); bm.from_mesh(obj.data)
    f = len(bm.faces); q = sum(1 for face in bm.faces if len(face.verts) == 4)
    nm = sum(1 for e in bm.edges if not e.is_manifold)
    print(f"\n  MESH: {obj.name}  |  V:{len(bm.verts)} E:{len(bm.edges)} F:{f}")
    print(f"  Quads: {q}/{f} ({100*q/max(f,1):.0f}%)  |  Non-manifold: {nm}  |  Watertight: {'YES' if nm==0 else 'NO'}")
    bm.free()

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
