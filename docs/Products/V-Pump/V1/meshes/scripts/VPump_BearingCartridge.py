# ============================================================================
# VPump_BearingCartridge.py — SiC/SiC ceramic journal bearing cartridge
# Multi-body: outer housing sleeve + inner journal + water channel grooves
# ============================================================================
import bpy, bmesh, math, os

HOUSING_OR = 0.18; HOUSING_IR = 0.12; HOUSING_LEN = 0.25
JOURNAL_OR = 0.085; JOURNAL_IR = 0.078; JOURNAL_LEN = 0.20
GROOVE_R = 0.005; GROOVE_COUNT = 6

MAT_COLOR = (0.20, 0.22, 0.25, 1.0); MAT_METAL = 0.15; MAT_ROUGH = 0.10

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
OUT_DIR = os.path.normpath(os.path.join(SCRIPT_DIR, ".."))
OUT_FILE = os.path.join(OUT_DIR, "VPump_BearingCartridge.glb")
OBJ_NAME = "VPump_BearingCartridge"; SCENE_NAME = "Scene0"

def clean_scene():
    bpy.ops.wm.read_factory_settings(use_empty=True); bpy.context.scene.name = SCENE_NAME

def make_material():
    mat = bpy.data.materials.new(name="MAT_VPump_SiC")
    mat.use_nodes = True; bsdf = mat.node_tree.nodes.get("Principled BSDF")
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
    # Outer housing sleeve
    housing = add_cyl("housing", HOUSING_OR, HOUSING_LEN)
    h_bore = add_cyl("h_bore", HOUSING_IR, HOUSING_LEN + 0.01)
    bool_op(housing, h_bore, 'DIFFERENCE')
    # Inner journal
    journal = add_cyl("journal", JOURNAL_OR, JOURNAL_LEN)
    j_bore = add_cyl("j_bore", JOURNAL_IR, JOURNAL_LEN + 0.01)
    bool_op(journal, j_bore, 'DIFFERENCE')
    # Water lubrication grooves on journal OD
    for i in range(GROOVE_COUNT):
        angle = 2 * math.pi * i / GROOVE_COUNT
        x = JOURNAL_OR * math.cos(angle)
        y = JOURNAL_OR * math.sin(angle)
        groove = add_cyl(f"gr_{i}", GROOVE_R, JOURNAL_LEN * 0.8, loc=(x, y, 0))
        bool_op(journal, groove, 'DIFFERENCE')
    bool_op(housing, journal, 'UNION')
    # Retaining lip at one end
    lip = add_cyl("lip", HOUSING_OR + 0.015, 0.02, loc=(0, 0, HOUSING_LEN/2 - 0.01))
    lip_h = add_cyl("lip_h", HOUSING_IR - 0.005, 0.025, loc=(0, 0, HOUSING_LEN/2 - 0.01))
    bool_op(lip, lip_h, 'DIFFERENCE')
    bool_op(housing, lip, 'UNION')
    return housing

def polish(obj, mat):
    obj.name = OBJ_NAME; obj.data.materials.append(mat)
    bpy.context.view_layer.objects.active = obj
    mod = obj.modifiers.new(name="Bevel", type='BEVEL')
    mod.width = 0.001; mod.segments = 2; mod.limit_method = 'ANGLE'; mod.angle_limit = math.radians(30)
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
    print(f"[VPump_BearingCartridge] V:{v} F:{f} Q:{q}/{f} ({100*q//max(f,1)}%) NM:{nm} WT:{'YES' if nm==0 else 'NO'}")

def export(obj):
    bpy.ops.object.select_all(action='DESELECT'); obj.select_set(True)
    bpy.context.view_layer.objects.active = obj
    os.makedirs(os.path.dirname(OUT_FILE), exist_ok=True)
    bpy.ops.export_scene.gltf(filepath=OUT_FILE, export_format='GLB', use_selection=True, export_apply=True, export_draco_mesh_compression_enable=True)
    print(f"[VPump_BearingCartridge] Exported: {OUT_FILE} ({os.path.getsize(OUT_FILE)/1024:.1f} KB)")

if __name__ == "__main__":
    clean_scene(); mat = make_material(); obj = create_geometry(); polish(obj, mat); verify(obj); export(obj)
