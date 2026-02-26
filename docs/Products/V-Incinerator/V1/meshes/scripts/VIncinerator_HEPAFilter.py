"""
V-Incinerator — HEPA Filter Bank  (Blender 4.4 headless)
=========================================================
Borosilicate glass fiber in 316L frame. 24 V-bank modules.
Rectangular housing with inlet/outlet plenums (duct stubs),
access panel doors on front, differential pressure port stubs,
internal divider ribs visible as external raised seams,
mounting feet.

Run: blender --background --python this_script.py
"""
import bpy, bmesh, math, os

PRODUCT   = "VIncinerator"
COMPONENT = "HEPAFilter"
MATERIAL  = "Borosilicate_Glass"
OUT_DIR   = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT_FILE  = f"{PRODUCT}_{COMPONENT}.glb"

# ── Dimensions (from PATENT.md: 48 m² filter area, 24 V-bank modules) ─
WIDTH  = 2.00       # housing width (X)
DEPTH  = 1.20       # housing depth (Y)
HEIGHT = 1.60       # housing height (Z)
WALL   = 0.006
DUCT_W = 0.80       # inlet/outlet duct width
DUCT_H = 0.70       # inlet/outlet duct height
DUCT_L = 0.25       # duct stub protrusion
DOOR_W = 0.70
DOOR_H = 1.20
DOOR_D = 0.008
RIB_W  = 0.015      # external rib (divider seam)
RIB_D  = 0.008
FOOT_W = 0.15
FOOT_D = 0.15
FOOT_H = 0.10
DP_R   = 0.02       # differential pressure port

PBR = {
    "base_color": (0.88, 0.88, 0.85, 0.92),  # off-white glass-like
    "metallic": 0.2,
    "roughness": 0.55,
    "alpha": 0.92,
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
    if PBR["alpha"] < 1.0:
        mat.blend_method = 'BLEND'
    return mat

def add_cube(sx, sy, sz, loc=(0,0,0)):
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=loc)
    obj = bpy.context.active_object; obj.scale = (sx, sy, sz)
    bpy.ops.object.transform_apply(scale=True)
    return obj

def add_cyl(r, d, v=24, loc=(0,0,0), rot=(0,0,0)):
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
    """HEPA filter bank housing with ducts, access doors, ribs, feet."""

    # 1) Main housing — hollow box
    box = add_cube(WIDTH, DEPTH, HEIGHT)
    sol = box.modifiers.new("Hollow", 'SOLIDIFY')
    sol.thickness = WALL; sol.offset = -1
    bpy.context.view_layer.objects.active = box
    bpy.ops.object.modifier_apply(modifier="Hollow")

    # 2) Inlet duct stub (left side, -X)
    duct_in = add_cube(DUCT_L, DUCT_W, DUCT_H, (-WIDTH/2 - DUCT_L/2, 0, 0))
    bool_op(box, duct_in, 'UNION')

    # 3) Outlet duct stub (right side, +X)
    duct_out = add_cube(DUCT_L, DUCT_W, DUCT_H, (WIDTH/2 + DUCT_L/2, 0, 0))
    bool_op(box, duct_out, 'UNION')

    # 4) Duct flanges (raised rim around each duct opening)
    for x_sign in [-1, 1]:
        x = x_sign * (WIDTH/2 + DUCT_L)
        flange = add_cube(0.02, DUCT_W + 0.06, DUCT_H + 0.06, (x, 0, 0))
        bool_op(box, flange, 'UNION')

    # 5) Access panel doors (front face, +Y, 3 panels side by side)
    for i in range(3):
        x_off = -WIDTH/3 + i * WIDTH/3
        frame = add_cube(DOOR_W + 0.03, DOOR_D, DOOR_H + 0.03,
                          (x_off, DEPTH/2, -HEIGHT/2 + DOOR_H/2 + 0.15))
        bool_op(box, frame, 'UNION')
        # Recessed panel
        panel = add_cube(DOOR_W, DOOR_D * 0.6, DOOR_H,
                          (x_off, DEPTH/2 + DOOR_D * 0.3, -HEIGHT/2 + DOOR_H/2 + 0.15))
        bool_op(box, panel, 'UNION')

    # 6) External ribs — horizontal divider seams (represent internal V-bank dividers)
    for z_off in [-HEIGHT/4, 0, HEIGHT/4]:
        rib = add_cube(WIDTH + 0.01, RIB_D, RIB_W, (0, DEPTH/2 + RIB_D/2, z_off))
        bool_op(box, rib, 'UNION')
        rib2 = add_cube(WIDTH + 0.01, RIB_D, RIB_W, (0, -DEPTH/2 - RIB_D/2, z_off))
        bool_op(box, rib2, 'UNION')

    # 7) Differential pressure ports (2, on top)
    for x_off in [-WIDTH/4, WIDTH/4]:
        dp = add_cyl(DP_R, 0.05, 16, (x_off, 0, HEIGHT/2 + 0.025))
        bool_op(box, dp, 'UNION')

    # 8) Mounting feet (4 at corners)
    for cx in [-WIDTH/2 + FOOT_W/2, WIDTH/2 - FOOT_W/2]:
        for cy in [-DEPTH/2 + FOOT_D/2, DEPTH/2 - FOOT_D/2]:
            foot = add_cube(FOOT_W, FOOT_D, FOOT_H,
                            (cx, cy, -HEIGHT/2 - FOOT_H/2))
            bool_op(box, foot, 'UNION')

    box.name = f"{PRODUCT}_{COMPONENT}"
    box.data.name = f"{PRODUCT}_{COMPONENT}_mesh"
    return box

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
