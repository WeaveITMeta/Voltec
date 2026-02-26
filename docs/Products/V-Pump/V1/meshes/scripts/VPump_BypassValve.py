# ============================================================================
# VPump_BypassValve.py — Automatic butterfly bypass valve with actuator
# Multi-body: pipe tee + butterfly disc + actuator housing + spring housing
# ============================================================================
import bpy, bmesh, math, os

PIPE_R = 0.60; PIPE_LEN = 2.5; PIPE_WALL = 0.015
DISC_R = 0.58; DISC_THICK = 0.025
ACTUATOR_R = 0.15; ACTUATOR_LEN = 0.40
SPRING_R = 0.10; SPRING_LEN = 0.30
FLANGE_R = 0.72; FLANGE_THICK = 0.05

MAT_COLOR = (0.60, 0.62, 0.65, 1.0); MAT_METAL = 1.0; MAT_ROUGH = 0.30

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
OUT_DIR = os.path.normpath(os.path.join(SCRIPT_DIR, ".."))
OUT_FILE = os.path.join(OUT_DIR, "VPump_BypassValve.glb")
OBJ_NAME = "VPump_BypassValve"; SCENE_NAME = "Scene0"

def clean_scene():
    bpy.ops.wm.read_factory_settings(use_empty=True); bpy.context.scene.name = SCENE_NAME

def make_material():
    mat = bpy.data.materials.new(name="MAT_VPump_DuplexBypass")
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
    # Main pipe body (hollow)
    pipe = add_cyl("pipe", PIPE_R, PIPE_LEN)
    pipe_bore = add_cyl("bore", PIPE_R - PIPE_WALL, PIPE_LEN + 0.01)
    bool_op(pipe, pipe_bore, 'DIFFERENCE')
    # Flanges at each end
    for z in [-PIPE_LEN/2 + FLANGE_THICK/2, PIPE_LEN/2 - FLANGE_THICK/2]:
        fl = add_cyl(f"fl_{z}", FLANGE_R, FLANGE_THICK, loc=(0, 0, z))
        fl_h = add_cyl(f"fh_{z}", PIPE_R - PIPE_WALL, FLANGE_THICK + 0.01, loc=(0, 0, z))
        bool_op(fl, fl_h, 'DIFFERENCE')
        bool_op(pipe, fl, 'UNION')
    # Butterfly disc (tilted 10° to show partially closed state)
    disc = add_cyl("disc", DISC_R, DISC_THICK, rot=(math.radians(10), 0, 0))
    bool_op(pipe, disc, 'UNION')
    # Valve stem (vertical through pipe)
    stem = add_cyl("stem", 0.025, PIPE_R * 2 + 0.3, rot=(math.pi/2, 0, 0))
    bool_op(pipe, stem, 'UNION')
    # Actuator housing (on top)
    act = add_cyl("act", ACTUATOR_R, ACTUATOR_LEN, loc=(0, PIPE_R + ACTUATOR_LEN/2 + 0.05, 0))
    bool_op(pipe, act, 'UNION')
    # Spring-return housing (smaller, on side of actuator)
    spring = add_cyl("spring", SPRING_R, SPRING_LEN, loc=(ACTUATOR_R + 0.05, PIPE_R + ACTUATOR_LEN/2 + 0.05, 0), rot=(0, math.pi/2, 0))
    bool_op(pipe, spring, 'UNION')
    # Position indicator flag (small cube on top of actuator)
    flag = add_cube("flag", (0.04, 0.08, 0.005), loc=(0, PIPE_R + ACTUATOR_LEN + 0.10, 0))
    bool_op(pipe, flag, 'UNION')
    return pipe

def polish(obj, mat):
    obj.name = OBJ_NAME; obj.data.materials.append(mat)
    bpy.context.view_layer.objects.active = obj
    mod = obj.modifiers.new(name="Bevel", type='BEVEL')
    mod.width = 0.003; mod.segments = 2; mod.limit_method = 'ANGLE'; mod.angle_limit = math.radians(30)
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
    print(f"[VPump_BypassValve] V:{v} F:{f} Q:{q}/{f} ({100*q//max(f,1)}%) NM:{nm} WT:{'YES' if nm==0 else 'NO'}")

def export(obj):
    bpy.ops.object.select_all(action='DESELECT'); obj.select_set(True)
    bpy.context.view_layer.objects.active = obj
    os.makedirs(os.path.dirname(OUT_FILE), exist_ok=True)
    bpy.ops.export_scene.gltf(filepath=OUT_FILE, export_format='GLB', use_selection=True, export_apply=True, export_draco_mesh_compression_enable=True)
    print(f"[VPump_BypassValve] Exported: {OUT_FILE} ({os.path.getsize(OUT_FILE)/1024:.1f} KB)")

if __name__ == "__main__":
    clean_scene(); mat = make_material(); obj = create_geometry(); polish(obj, mat); verify(obj); export(obj)
