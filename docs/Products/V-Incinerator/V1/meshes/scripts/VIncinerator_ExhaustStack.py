"""
V-Incinerator — Exhaust Stack  (Blender 4.4 headless)
=====================================================
304 Stainless Steel clean gas discharge stack.
Tapered cylinder (wider at base, narrower at top) with
CEMS sampling ports, rain cap, base flange, guy wire lugs,
and aircraft warning light bracket.

Run: blender --background --python this_script.py
"""
import bpy, bmesh, math, os

PRODUCT   = "VIncinerator"
COMPONENT = "ExhaustStack"
MATERIAL  = "304SS"
OUT_DIR   = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT_FILE  = f"{PRODUCT}_{COMPONENT}.glb"

# ── Dimensions ────────────────────────────────────────────────────────
BASE_R    = 0.30         # base radius
TOP_R     = 0.20         # top radius (tapered)
HEIGHT    = 4.00         # total height
WALL      = 0.006        # 6 mm wall
FLANGE_R  = BASE_R + 0.08
FLANGE_H  = 0.035
CAP_R     = TOP_R + 0.10 # rain cap
CAP_H     = 0.08
CAP_GAP   = 0.06         # gap between stack top and cap
CEMS_R    = 0.04         # CEMS sampling port radius
CEMS_L    = 0.10

PBR = {
    "base_color": (0.68, 0.70, 0.72, 1.0),  # bright 304SS
    "metallic": 1.0,
    "roughness": 0.28,
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

def add_cone(r1, r2, d, v=48, loc=(0,0,0)):
    bpy.ops.mesh.primitive_cone_add(vertices=v, radius1=r1, radius2=r2,
                                     depth=d, location=loc)
    return bpy.context.active_object

def bool_op(target, cutter, op='UNION'):
    mod = target.modifiers.new(op, 'BOOLEAN')
    mod.operation = op; mod.object = cutter; mod.solver = 'EXACT'
    bpy.context.view_layer.objects.active = target
    bpy.ops.object.modifier_apply(modifier=op)
    bpy.data.objects.remove(cutter, do_unlink=True)

def create_geometry():
    """Tapered exhaust stack with rain cap, CEMS ports, base flange, guy wire lugs."""

    # 1) Main tapered stack — hollow cone
    stack = add_cone(BASE_R, TOP_R, HEIGHT, 48)
    sol = stack.modifiers.new("Hollow", 'SOLIDIFY')
    sol.thickness = WALL; sol.offset = -1
    bpy.context.view_layer.objects.active = stack
    bpy.ops.object.modifier_apply(modifier="Hollow")

    # 2) Base flange
    fl = add_cyl(FLANGE_R, FLANGE_H, 48, (0, 0, -HEIGHT/2 - FLANGE_H/2))
    fl_hole = add_cyl(BASE_R - WALL, FLANGE_H + 0.01, 48, (0, 0, -HEIGHT/2 - FLANGE_H/2))
    bool_op(fl, fl_hole, 'DIFFERENCE')
    bool_op(stack, fl, 'UNION')

    # 3) Rain cap — disc on supports (4 small pillars)
    cap = add_cyl(CAP_R, CAP_H, 32, (0, 0, HEIGHT/2 + CAP_GAP + CAP_H/2))
    bool_op(stack, cap, 'UNION')
    # Support pillars for rain cap
    for angle in [0, math.pi/2, math.pi, 3*math.pi/2]:
        px = (TOP_R - 0.02) * math.cos(angle)
        py = (TOP_R - 0.02) * math.sin(angle)
        pillar = add_cyl(0.012, CAP_GAP, 8, (px, py, HEIGHT/2 + CAP_GAP/2))
        bool_op(stack, pillar, 'UNION')

    # 4) CEMS sampling ports (2, at 90° apart, at 3/4 height)
    cems_z = HEIGHT/4  # 3/4 up from bottom (0 is center)
    r_at_z = BASE_R + (TOP_R - BASE_R) * (cems_z/HEIGHT + 0.5)  # linear interpolation
    for angle in [0, math.pi/2]:
        cx = (r_at_z + CEMS_L/2) * math.cos(angle)
        cy = (r_at_z + CEMS_L/2) * math.sin(angle)
        port = add_cyl(CEMS_R, CEMS_L, 16, (cx, cy, cems_z),
                        (0, math.pi/2, angle))
        # Collar
        ccx = (r_at_z + CEMS_L) * math.cos(angle)
        ccy = (r_at_z + CEMS_L) * math.sin(angle)
        collar = add_cyl(CEMS_R + 0.015, 0.015, 16, (ccx, ccy, cems_z),
                          (0, math.pi/2, angle))
        bool_op(port, collar, 'UNION')
        bool_op(stack, port, 'UNION')

    # 5) Guy wire lug brackets (3 at 120°, at 2/3 height)
    lug_z = HEIGHT/6
    r_at_lug = BASE_R + (TOP_R - BASE_R) * (lug_z/HEIGHT + 0.5)
    for i in range(3):
        angle = math.radians(120 * i + 60)
        lx = (r_at_lug + 0.03) * math.cos(angle)
        ly = (r_at_lug + 0.03) * math.sin(angle)
        lug = add_cyl(0.025, 0.015, 12, (lx, ly, lug_z))
        bool_op(stack, lug, 'UNION')

    # 6) Aircraft warning light bracket (top)
    light = add_cyl(0.03, 0.04, 12, (TOP_R + 0.05, 0, HEIGHT/2 - 0.10),
                     (0, math.pi/2, 0))
    bool_op(stack, light, 'UNION')

    stack.name = f"{PRODUCT}_{COMPONENT}"
    stack.data.name = f"{PRODUCT}_{COMPONENT}_mesh"
    return stack

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
