# ============================================================================
# VPump_DriveShaft.py — 17-4 PH stainless drive shaft with keyways + coupling
# Multi-body: main shaft + keyway slots + coupling flanges + thrust collar
# ============================================================================
import bpy, bmesh, math, os

SHAFT_R = 0.075; SHAFT_LEN = 4.5
KEY_W = 0.02; KEY_D = 0.01; KEY_LEN = 0.3
COUPLING_R = 0.12; COUPLING_THICK = 0.05
COLLAR_R = 0.10; COLLAR_THICK = 0.04

MAT_COLOR = (0.78, 0.78, 0.80, 1.0); MAT_METAL = 1.0; MAT_ROUGH = 0.20

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
OUT_DIR = os.path.normpath(os.path.join(SCRIPT_DIR, ".."))
OUT_FILE = os.path.join(OUT_DIR, "VPump_DriveShaft.glb")
OBJ_NAME = "VPump_DriveShaft"; SCENE_NAME = "Scene0"

def clean_scene():
    bpy.ops.wm.read_factory_settings(use_empty=True); bpy.context.scene.name = SCENE_NAME

def make_material():
    mat = bpy.data.materials.new(name="MAT_VPump_174PH")
    mat.use_nodes = True; bsdf = mat.node_tree.nodes.get("Principled BSDF")
    bsdf.inputs["Base Color"].default_value = MAT_COLOR
    bsdf.inputs["Metallic"].default_value = MAT_METAL
    bsdf.inputs["Roughness"].default_value = MAT_ROUGH
    return mat

def add_cyl(name, r, d, loc=(0,0,0), segs=48):
    bpy.ops.mesh.primitive_cylinder_add(radius=r, depth=d, vertices=segs, location=loc)
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
    shaft = add_cyl("shaft", SHAFT_R, SHAFT_LEN)
    # Keyway slots (×2, 180° apart)
    for angle in [0, math.pi]:
        x = (SHAFT_R - KEY_D/2) * math.cos(angle)
        y = (SHAFT_R - KEY_D/2) * math.sin(angle)
        key = add_cube(f"key_{angle}", (KEY_W, KEY_D, KEY_LEN), loc=(x, y, 0))
        bool_op(shaft, key, 'DIFFERENCE')
    # Coupling flanges at each end
    for z in [-SHAFT_LEN/2 + COUPLING_THICK/2, SHAFT_LEN/2 - COUPLING_THICK/2]:
        coup = add_cyl(f"coup_{z}", COUPLING_R, COUPLING_THICK, loc=(0,0,z))
        bool_op(shaft, coup, 'UNION')
    # Thrust collar (center)
    collar = add_cyl("collar", COLLAR_R, COLLAR_THICK)
    bool_op(shaft, collar, 'UNION')
    return shaft

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
    print(f"[VPump_DriveShaft] V:{v} F:{f} Q:{q}/{f} ({100*q//max(f,1)}%) NM:{nm} WT:{'YES' if nm==0 else 'NO'}")

def export(obj):
    bpy.ops.object.select_all(action='DESELECT'); obj.select_set(True)
    bpy.context.view_layer.objects.active = obj
    os.makedirs(os.path.dirname(OUT_FILE), exist_ok=True)
    bpy.ops.export_scene.gltf(filepath=OUT_FILE, export_format='GLB', use_selection=True, export_apply=True, export_draco_mesh_compression_enable=True)
    print(f"[VPump_DriveShaft] Exported: {OUT_FILE} ({os.path.getsize(OUT_FILE)/1024:.1f} KB)")

if __name__ == "__main__":
    clean_scene(); mat = make_material(); obj = create_geometry(); polish(obj, mat); verify(obj); export(obj)
