# ============================================================================
# VPump_Motor.py — PMSM direct-drive motor with cooling jacket + terminal box
# Multi-body: stator housing + cooling jacket fins + terminal box + shaft stub
# ============================================================================
import bpy, bmesh, math, os

STATOR_R = 0.40; STATOR_LEN = 1.2
JACKET_R = 0.42; FIN_R = 0.44; FIN_COUNT = 20; FIN_THICK = 0.004
SHAFT_R = 0.075; SHAFT_STUB = 0.15
TERM_W, TERM_H, TERM_D = 0.25, 0.20, 0.15
END_CAP_R = 0.38; END_CAP_THICK = 0.03

MAT_COLOR = (0.12, 0.14, 0.18, 1.0); MAT_METAL = 0.9; MAT_ROUGH = 0.45

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
OUT_DIR = os.path.normpath(os.path.join(SCRIPT_DIR, ".."))
OUT_FILE = os.path.join(OUT_DIR, "VPump_Motor.glb")
OBJ_NAME = "VPump_Motor"; SCENE_NAME = "Scene0"

def clean_scene():
    bpy.ops.wm.read_factory_settings(use_empty=True); bpy.context.scene.name = SCENE_NAME

def make_material():
    mat = bpy.data.materials.new(name="MAT_VPump_PMSM")
    mat.use_nodes = True; bsdf = mat.node_tree.nodes.get("Principled BSDF")
    bsdf.inputs["Base Color"].default_value = MAT_COLOR
    bsdf.inputs["Metallic"].default_value = MAT_METAL
    bsdf.inputs["Roughness"].default_value = MAT_ROUGH
    return mat

def add_cyl(name, r, d, loc=(0,0,0), rot=(0,0,0), segs=48):
    bpy.ops.mesh.primitive_cylinder_add(radius=r, depth=d, vertices=segs, location=loc, rotation=rot)
    o = bpy.context.active_object; o.name = name; return o

def add_cube(name, size, loc=(0,0,0)):
    bpy.ops.mesh.primitive_cube_add(size=1, location=loc, scale=size)
    o = bpy.context.active_object; o.name = name; return o

def bool_op(target, cutter, operation='UNION'):
    mod = target.modifiers.new(name=operation, type='BOOLEAN')
    mod.operation = operation; mod.solver = 'EXACT'; mod.object = cutter
    bpy.context.view_layer.objects.active = target
    bpy.ops.object.modifier_apply(modifier=mod.name)
    bpy.data.objects.remove(cutter, do_unlink=True)

def create_geometry():
    # Main stator housing
    body = add_cyl("body", STATOR_R, STATOR_LEN)
    # Cooling jacket fins (circumferential rings)
    for i in range(FIN_COUNT):
        z = -STATOR_LEN/2 + 0.04 + i * (STATOR_LEN - 0.08) / (FIN_COUNT - 1)
        fin = add_cyl(f"fin_{i}", FIN_R, FIN_THICK, loc=(0, 0, z))
        fin_h = add_cyl(f"fh_{i}", STATOR_R - 0.005, FIN_THICK + 0.01, loc=(0, 0, z))
        bool_op(fin, fin_h, 'DIFFERENCE')
        bool_op(body, fin, 'UNION')
    # Drive-end cap
    de_cap = add_cyl("de_cap", END_CAP_R, END_CAP_THICK, loc=(0, 0, STATOR_LEN/2 + END_CAP_THICK/2))
    bool_op(body, de_cap, 'UNION')
    # Non-drive-end cap
    nde_cap = add_cyl("nde_cap", END_CAP_R, END_CAP_THICK, loc=(0, 0, -STATOR_LEN/2 - END_CAP_THICK/2))
    bool_op(body, nde_cap, 'UNION')
    # Shaft stub (drive end)
    stub = add_cyl("stub", SHAFT_R, SHAFT_STUB, loc=(0, 0, STATOR_LEN/2 + END_CAP_THICK + SHAFT_STUB/2))
    bool_op(body, stub, 'UNION')
    # Terminal box (top)
    term = add_cube("term", (TERM_W, TERM_D, TERM_H), loc=(0, STATOR_R + TERM_D/2, 0))
    bool_op(body, term, 'UNION')
    # Cable gland stubs (3-phase + ground = 4)
    for i in range(4):
        x = -0.08 + i * 0.055
        gland = add_cyl(f"gland_{i}", 0.015, 0.06, loc=(x, STATOR_R + TERM_D + 0.02, 0))
        bool_op(body, gland, 'UNION')
    # Mounting feet (×2)
    for x_sign in [-1, 1]:
        foot = add_cube(f"foot_{x_sign}", (0.15, 0.30, 0.04), loc=(x_sign * 0.30, 0, -STATOR_R - 0.02))
        bool_op(body, foot, 'UNION')
    return body

def polish(obj, mat):
    obj.name = OBJ_NAME; obj.data.materials.append(mat)
    bpy.context.view_layer.objects.active = obj
    mod = obj.modifiers.new(name="Bevel", type='BEVEL')
    mod.width = 0.002; mod.segments = 2; mod.limit_method = 'ANGLE'; mod.angle_limit = math.radians(30)
    bpy.ops.object.modifier_apply(modifier=mod.name)
    bpy.ops.object.shade_auto_smooth()
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.mesh.select_all(action='SELECT')
    bpy.ops.uv.smart_project(angle_limit=66, island_margin=0.01)
    bpy.ops.object.mode_set(mode='OBJECT')
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.transform_apply(location=False, rotation=True, scale=True)

def verify(obj):
    bm = bmesh.new(); bm.from_mesh(obj.data)
    v,f = len(bm.verts), len(bm.faces)
    q = sum(1 for fa in bm.faces if len(fa.verts)==4)
    nm = sum(1 for e in bm.edges if not e.is_manifold)
    bm.free()
    print(f"[VPump_Motor] V:{v} F:{f} Q:{q}/{f} ({100*q//max(f,1)}%) NM:{nm} WT:{'YES' if nm==0 else 'NO'}")

def export(obj):
    bpy.ops.object.select_all(action='DESELECT'); obj.select_set(True)
    bpy.context.view_layer.objects.active = obj
    os.makedirs(os.path.dirname(OUT_FILE), exist_ok=True)
    bpy.ops.export_scene.gltf(filepath=OUT_FILE, export_format='GLB', use_selection=True, export_apply=True, export_draco_mesh_compression_enable=True)
    print(f"[VPump_Motor] Exported: {OUT_FILE} ({os.path.getsize(OUT_FILE)/1024:.1f} KB)")

if __name__ == "__main__":
    clean_scene(); mat = make_material(); obj = create_geometry(); polish(obj, mat); verify(obj); export(obj)
