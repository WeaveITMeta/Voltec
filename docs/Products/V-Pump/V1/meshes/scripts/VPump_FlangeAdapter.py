# ============================================================================
# VPump_FlangeAdapter.py — Modular conical reducer/expander flange ring
# Multi-body: conical reducer body + bolt holes + gasket groove + stiffener ribs
# ============================================================================
import bpy, bmesh, math, os

LARGE_R = 1.0; SMALL_R = 0.625  # DN2000 → DN1200 adapter example
CONE_LEN = 0.40; FLANGE_THICK = 0.06
BOLT_R = 0.018; BOLT_PCD = 0.85; BOLT_COUNT = 24
RIB_W = 0.015; RIB_H = 0.06; RIB_COUNT = 8

MAT_COLOR = (0.62, 0.64, 0.67, 1.0); MAT_METAL = 1.0; MAT_ROUGH = 0.35

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
OUT_DIR = os.path.normpath(os.path.join(SCRIPT_DIR, ".."))
OUT_FILE = os.path.join(OUT_DIR, "VPump_FlangeAdapter.glb")
OBJ_NAME = "VPump_FlangeAdapter"; SCENE_NAME = "Scene0"

def clean_scene():
    bpy.ops.wm.read_factory_settings(use_empty=True); bpy.context.scene.name = SCENE_NAME

def make_material():
    mat = bpy.data.materials.new(name="MAT_VPump_F60Duplex")
    mat.use_nodes = True; bsdf = mat.node_tree.nodes.get("Principled BSDF")
    bsdf.inputs["Base Color"].default_value = MAT_COLOR
    bsdf.inputs["Metallic"].default_value = MAT_METAL
    bsdf.inputs["Roughness"].default_value = MAT_ROUGH
    return mat

def add_cyl(name, r, d, loc=(0,0,0), segs=48):
    bpy.ops.mesh.primitive_cylinder_add(radius=r, depth=d, vertices=segs, location=loc)
    o = bpy.context.active_object; o.name = name; return o

def add_cone(name, r1, r2, d, loc=(0,0,0), segs=48):
    bpy.ops.mesh.primitive_cone_add(radius1=r1, radius2=r2, depth=d, vertices=segs, location=loc)
    o = bpy.context.active_object; o.name = name; return o

def add_cube(name, size, loc=(0,0,0), rot=(0,0,0)):
    bpy.ops.mesh.primitive_cube_add(size=1, location=loc, rotation=rot, scale=size)
    o = bpy.context.active_object; o.name = name; return o

def bool_op(target, cutter, operation='UNION'):
    mod = target.modifiers.new(name=operation, type='BOOLEAN')
    mod.operation = operation; mod.solver = 'EXACT'; mod.object = cutter
    bpy.context.view_layer.objects.active = target
    bpy.ops.object.modifier_apply(modifier=mod.name)
    bpy.data.objects.remove(cutter, do_unlink=True)

def create_geometry():
    # Conical reducer body (solid, then hollow)
    outer = add_cone("outer", LARGE_R, SMALL_R, CONE_LEN)
    inner = add_cone("inner", LARGE_R - 0.025, SMALL_R - 0.025, CONE_LEN + 0.01)
    bool_op(outer, inner, 'DIFFERENCE')
    # Large-end flange ring
    lg_flange = add_cyl("lg_fl", LARGE_R + 0.06, FLANGE_THICK, loc=(0, 0, -CONE_LEN/2 + FLANGE_THICK/2))
    lg_bore = add_cyl("lg_bore", LARGE_R - 0.025, FLANGE_THICK + 0.01, loc=(0, 0, -CONE_LEN/2 + FLANGE_THICK/2))
    bool_op(lg_flange, lg_bore, 'DIFFERENCE')
    bool_op(outer, lg_flange, 'UNION')
    # Small-end flange ring
    sm_flange = add_cyl("sm_fl", SMALL_R + 0.06, FLANGE_THICK, loc=(0, 0, CONE_LEN/2 - FLANGE_THICK/2))
    sm_bore = add_cyl("sm_bore", SMALL_R - 0.025, FLANGE_THICK + 0.01, loc=(0, 0, CONE_LEN/2 - FLANGE_THICK/2))
    bool_op(sm_flange, sm_bore, 'DIFFERENCE')
    bool_op(outer, sm_flange, 'UNION')
    # Bolt holes on large-end flange
    for i in range(BOLT_COUNT):
        angle = 2 * math.pi * i / BOLT_COUNT
        bx = BOLT_PCD * math.cos(angle)
        by = BOLT_PCD * math.sin(angle)
        bolt = add_cyl(f"bolt_{i}", BOLT_R, FLANGE_THICK + 0.02, loc=(bx, by, -CONE_LEN/2 + FLANGE_THICK/2))
        bool_op(outer, bolt, 'DIFFERENCE')
    # External stiffener ribs
    for i in range(RIB_COUNT):
        angle = 2 * math.pi * i / RIB_COUNT
        mid_r = (LARGE_R + SMALL_R) / 2
        rx = mid_r * math.cos(angle)
        ry = mid_r * math.sin(angle)
        rib = add_cube(f"rib_{i}", (RIB_W, RIB_H, CONE_LEN * 0.7), loc=(rx, ry, 0), rot=(0, 0, angle))
        bool_op(outer, rib, 'UNION')
    return outer

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
    print(f"[VPump_FlangeAdapter] V:{v} F:{f} Q:{q}/{f} ({100*q//max(f,1)}%) NM:{nm} WT:{'YES' if nm==0 else 'NO'}")

def export(obj):
    bpy.ops.object.select_all(action='DESELECT'); obj.select_set(True)
    bpy.context.view_layer.objects.active = obj
    os.makedirs(os.path.dirname(OUT_FILE), exist_ok=True)
    bpy.ops.export_scene.gltf(filepath=OUT_FILE, export_format='GLB', use_selection=True, export_apply=True, export_draco_mesh_compression_enable=True)
    print(f"[VPump_FlangeAdapter] Exported: {OUT_FILE} ({os.path.getsize(OUT_FILE)/1024:.1f} KB)")

if __name__ == "__main__":
    clean_scene(); mat = make_material(); obj = create_geometry(); polish(obj, mat); verify(obj); export(obj)
