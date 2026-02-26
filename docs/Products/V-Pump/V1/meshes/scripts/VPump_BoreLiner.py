# ============================================================================
# VPump_BoreLiner.py — RBSiC bore liner (precision ground ceramic sleeve)
# Multi-body assembly: thick ceramic tube + wear rings at each end
# ============================================================================
import bpy, bmesh, math, os

LINER_OR = 0.60            # Outer radius
LINER_IR = 0.58            # Inner radius (2cm wall)
LINER_LEN = 4.0            # Length
RING_OR = 0.62             # Wear ring outer radius
RING_THICK = 0.06          # Wear ring axial length

MAT_COLOR = (0.25, 0.25, 0.28, 1.0)  # Dark gray SiC ceramic
MAT_METAL = 0.2
MAT_ROUGH = 0.15

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
OUT_DIR = os.path.normpath(os.path.join(SCRIPT_DIR, ".."))
OUT_FILE = os.path.join(OUT_DIR, "VPump_BoreLiner.glb")
OBJ_NAME = "VPump_BoreLiner"
SCENE_NAME = "Scene0"

def clean_scene():
    bpy.ops.wm.read_factory_settings(use_empty=True)
    bpy.context.scene.name = SCENE_NAME

def make_material():
    mat = bpy.data.materials.new(name="MAT_VPump_RBSiC")
    mat.use_nodes = True
    bsdf = mat.node_tree.nodes.get("Principled BSDF")
    bsdf.inputs["Base Color"].default_value = MAT_COLOR
    bsdf.inputs["Metallic"].default_value = MAT_METAL
    bsdf.inputs["Roughness"].default_value = MAT_ROUGH
    return mat

def add_cyl(name, r, d, loc=(0,0,0), segs=48):
    bpy.ops.mesh.primitive_cylinder_add(radius=r, depth=d, vertices=segs, location=loc)
    o = bpy.context.active_object; o.name = name; return o

def bool_op(target, cutter, operation='UNION'):
    mod = target.modifiers.new(name=operation, type='BOOLEAN')
    mod.operation = operation; mod.solver = 'EXACT'; mod.object = cutter
    bpy.context.view_layer.objects.active = target
    bpy.ops.object.modifier_apply(modifier=mod.name)
    bpy.data.objects.remove(cutter, do_unlink=True)

def create_geometry():
    outer = add_cyl("outer", LINER_OR, LINER_LEN)
    inner = add_cyl("inner", LINER_IR, LINER_LEN + 0.01)
    bool_op(outer, inner, 'DIFFERENCE')
    # Wear rings at each end
    for z in [-LINER_LEN/2 + RING_THICK/2, LINER_LEN/2 - RING_THICK/2]:
        ring = add_cyl(f"ring_{z}", RING_OR, RING_THICK, loc=(0,0,z))
        ring_hole = add_cyl(f"rh_{z}", LINER_IR, RING_THICK + 0.01, loc=(0,0,z))
        bool_op(ring, ring_hole, 'DIFFERENCE')
        bool_op(outer, ring, 'UNION')
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
    print(f"[VPump_BoreLiner] Verts:{v} Faces:{f} Quads:{q}/{f} ({100*q//max(f,1)}%) NM:{nm} WT:{'YES' if nm==0 else 'NO'}")

def export(obj):
    bpy.ops.object.select_all(action='DESELECT'); obj.select_set(True)
    bpy.context.view_layer.objects.active = obj
    os.makedirs(os.path.dirname(OUT_FILE), exist_ok=True)
    bpy.ops.export_scene.gltf(filepath=OUT_FILE, export_format='GLB', use_selection=True, export_apply=True, export_draco_mesh_compression_enable=True)
    print(f"[VPump_BoreLiner] Exported: {OUT_FILE} ({os.path.getsize(OUT_FILE)/1024:.1f} KB)")

if __name__ == "__main__":
    clean_scene(); mat = make_material(); obj = create_geometry(); polish(obj, mat); verify(obj); export(obj)
