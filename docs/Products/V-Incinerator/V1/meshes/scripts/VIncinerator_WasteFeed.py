"""
V-Incinerator — Waste Feed System  (Blender 4.4 headless)
==========================================================
AR400 Abrasion-Resistant Steel ram-fed intake with double airlock.
Rectangular hopper funnel at top, horizontal feed chute body,
double airlock doors (raised panel detail), hydraulic ram housing
stub at rear, discharge flange at front, support skid frame.

Run: blender --background --python this_script.py
"""
import bpy, bmesh, math, os

PRODUCT   = "VIncinerator"
COMPONENT = "WasteFeed"
MATERIAL  = "AR400_Steel"
OUT_DIR   = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT_FILE  = f"{PRODUCT}_{COMPONENT}.glb"

# ── Dimensions ────────────────────────────────────────────────────────
CHUTE_W   = 1.20       # feed chute width (X)
CHUTE_D   = 0.80       # feed chute depth (Y)
CHUTE_H   = 0.80       # feed chute height (Z)
CHUTE_L   = 2.40       # total chute length along X
WALL      = 0.012
HOPPER_W  = 1.60       # hopper top opening
HOPPER_D  = 1.20
HOPPER_H  = 0.80       # hopper taper height
RAM_W     = 0.40       # hydraulic ram housing
RAM_D     = 0.40
RAM_L     = 0.60
FLANGE_T  = 0.04       # discharge flange thickness
AIRLOCK_W = 0.06       # raised airlock door panels
SKID_W    = 0.08
SKID_H    = 0.15

PBR = {
    "base_color": (0.40, 0.38, 0.35, 1.0),  # AR400 dark steel
    "metallic": 1.0,
    "roughness": 0.60,
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

def add_cube(sx, sy, sz, loc=(0,0,0)):
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=loc)
    obj = bpy.context.active_object; obj.scale = (sx, sy, sz)
    bpy.ops.object.transform_apply(scale=True)
    return obj

def add_cone(r1, r2, d, v=32, loc=(0,0,0)):
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
    """Waste feed system with hopper, chute, airlock panels, ram housing, skid."""

    # 1) Main horizontal feed chute — hollow box
    chute = add_cube(CHUTE_L, CHUTE_D, CHUTE_H)
    sol = chute.modifiers.new("Hollow", 'SOLIDIFY')
    sol.thickness = WALL; sol.offset = -1
    bpy.context.view_layer.objects.active = chute
    bpy.ops.object.modifier_apply(modifier="Hollow")

    # 2) Hopper funnel on top (tapered from wide opening to chute width)
    # Approximate as a cone from large to small
    hopper = add_cone(max(HOPPER_W, HOPPER_D)/2, max(CHUTE_W, CHUTE_D)/2,
                       HOPPER_H, 4,  # 4-sided to approximate rectangular taper
                       (-CHUTE_L/4, 0, CHUTE_H/2 + HOPPER_H/2))
    sol2 = hopper.modifiers.new("Hollow", 'SOLIDIFY')
    sol2.thickness = WALL; sol2.offset = -1
    bpy.context.view_layer.objects.active = hopper
    bpy.ops.object.modifier_apply(modifier="Hollow")
    bool_op(chute, hopper, 'UNION')

    # 3) Hopper rim flange
    rim = add_cube(HOPPER_W + 0.08, HOPPER_D + 0.08, FLANGE_T,
                    (-CHUTE_L/4, 0, CHUTE_H/2 + HOPPER_H + FLANGE_T/2))
    rim_hole = add_cube(HOPPER_W - 0.02, HOPPER_D - 0.02, FLANGE_T + 0.01,
                         (-CHUTE_L/4, 0, CHUTE_H/2 + HOPPER_H + FLANGE_T/2))
    bool_op(rim, rim_hole, 'DIFFERENCE')
    bool_op(chute, rim, 'UNION')

    # 4) Discharge flange at front (+X end)
    d_fl = add_cube(FLANGE_T, CHUTE_D + 0.06, CHUTE_H + 0.06,
                     (CHUTE_L/2 + FLANGE_T/2, 0, 0))
    d_hole = add_cube(FLANGE_T + 0.01, CHUTE_D - 0.04, CHUTE_H - 0.04,
                       (CHUTE_L/2 + FLANGE_T/2, 0, 0))
    bool_op(d_fl, d_hole, 'DIFFERENCE')
    bool_op(chute, d_fl, 'UNION')

    # 5) Hydraulic ram housing at rear (-X end)
    ram = add_cube(RAM_L, RAM_W, RAM_D,
                    (-CHUTE_L/2 - RAM_L/2, 0, 0))
    bool_op(chute, ram, 'UNION')
    # Ram piston rod stub
    rod = add_cube(0.08, 0.08, 0.08,
                    (-CHUTE_L/2 - RAM_L - 0.04, 0, 0))
    bool_op(chute, rod, 'UNION')

    # 6) Double airlock door panels (2 raised panels on top of chute)
    for x_off in [CHUTE_L/6, CHUTE_L/3]:
        door = add_cube(AIRLOCK_W, CHUTE_D * 0.9, CHUTE_H * 0.6,
                         (x_off, 0, CHUTE_H/2 + AIRLOCK_W/2))
        bool_op(chute, door, 'UNION')

    # 7) External reinforcement ribs along chute (3 vertical ribs per side)
    for y_sign in [1, -1]:
        for x_off in [-CHUTE_L/4, 0, CHUTE_L/4]:
            rib = add_cube(0.012, 0.008, CHUTE_H * 0.7,
                           (x_off, y_sign * (CHUTE_D/2 + 0.004), 0))
            bool_op(chute, rib, 'UNION')

    # 8) Support skid frame (2 rails running length of chute)
    for cy in [-CHUTE_D/3, CHUTE_D/3]:
        rail = add_cube(CHUTE_L + RAM_L, SKID_W, SKID_H,
                         (-RAM_L/2, cy, -CHUTE_H/2 - SKID_H/2))
        bool_op(chute, rail, 'UNION')
    # Cross members
    for x_off in [-CHUTE_L/3, 0, CHUTE_L/3]:
        xm = add_cube(SKID_W, CHUTE_D * 0.8, SKID_H * 0.6,
                        (x_off, 0, -CHUTE_H/2 - SKID_H/2))
        bool_op(chute, xm, 'UNION')

    chute.name = f"{PRODUCT}_{COMPONENT}"
    chute.data.name = f"{PRODUCT}_{COMPONENT}_mesh"
    return chute

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
