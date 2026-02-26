# ============================================================================
# VPump_StatusArray.py — IP68 LED status indicator panel (5 LEDs)
# Multi-body: panel body + recessed LED dome lenses + mounting tabs + cable grommet
# ============================================================================
import bpy, bmesh, math, os

PANEL_W, PANEL_H, PANEL_D = 0.30, 0.08, 0.035
LED_R = 0.008; LED_COUNT = 5; LED_SPACING = 0.045
RECESS_DEPTH = 0.005
TAB_W, TAB_H, TAB_D = 0.025, 0.015, 0.035
GROMMET_R = 0.010

MAT_COLOR = (0.10, 0.10, 0.12, 1.0); MAT_METAL = 0.6; MAT_ROUGH = 0.25

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
OUT_DIR = os.path.normpath(os.path.join(SCRIPT_DIR, ".."))
OUT_FILE = os.path.join(OUT_DIR, "VPump_StatusArray.glb")
OBJ_NAME = "VPump_StatusArray"; SCENE_NAME = "Scene0"

def clean_scene():
    bpy.ops.wm.read_factory_settings(use_empty=True); bpy.context.scene.name = SCENE_NAME

def make_material():
    mat = bpy.data.materials.new(name="MAT_VPump_StatusPC")
    mat.use_nodes = True; bsdf = mat.node_tree.nodes.get("Principled BSDF")
    bsdf.inputs["Base Color"].default_value = MAT_COLOR
    bsdf.inputs["Metallic"].default_value = MAT_METAL
    bsdf.inputs["Roughness"].default_value = MAT_ROUGH
    return mat

def add_cube(name, size, loc=(0,0,0)):
    bpy.ops.mesh.primitive_cube_add(size=1, location=loc, scale=size)
    o = bpy.context.active_object; o.name = name; return o

def add_cyl(name, r, d, loc=(0,0,0), rot=(0,0,0), segs=24):
    bpy.ops.mesh.primitive_cylinder_add(radius=r, depth=d, vertices=segs, location=loc, rotation=rot)
    o = bpy.context.active_object; o.name = name; return o

def add_sphere(name, r, loc=(0,0,0), segs=16, rings=8):
    bpy.ops.mesh.primitive_uv_sphere_add(radius=r, segments=segs, ring_count=rings, location=loc)
    o = bpy.context.active_object; o.name = name; return o

def bool_op(target, cutter, operation='UNION'):
    mod = target.modifiers.new(name=operation, type='BOOLEAN')
    mod.operation = operation; mod.solver = 'EXACT'; mod.object = cutter
    bpy.context.view_layer.objects.active = target
    bpy.ops.object.modifier_apply(modifier=mod.name)
    bpy.data.objects.remove(cutter, do_unlink=True)

def create_geometry():
    # Panel body
    panel = add_cube("panel", (PANEL_W, PANEL_D, PANEL_H))
    # LED recesses + dome lenses
    start_x = -(LED_COUNT - 1) * LED_SPACING / 2
    for i in range(LED_COUNT):
        x = start_x + i * LED_SPACING
        # Recess hole
        recess = add_cyl(f"rec_{i}", LED_R + 0.002, RECESS_DEPTH + 0.001,
            loc=(x, PANEL_D/2 - RECESS_DEPTH/2, 0))
        bool_op(panel, recess, 'DIFFERENCE')
        # LED dome lens (hemisphere)
        dome = add_sphere(f"led_{i}", LED_R, loc=(x, PANEL_D/2 - RECESS_DEPTH + LED_R * 0.4, 0))
        bool_op(panel, dome, 'UNION')
    # Mounting tabs (×2, one each side)
    for x_sign in [-1, 1]:
        tab = add_cube(f"tab_{x_sign}", (TAB_W, TAB_D, TAB_H),
            loc=(x_sign * (PANEL_W/2 + TAB_W/2), 0, 0))
        # Mounting hole in tab
        hole = add_cyl(f"hole_{x_sign}", 0.003, TAB_D + 0.01,
            loc=(x_sign * (PANEL_W/2 + TAB_W/2), 0, 0),
            rot=(math.pi/2, 0, 0))
        bool_op(tab, hole, 'DIFFERENCE')
        bool_op(panel, tab, 'UNION')
    # Cable entry grommet (bottom center)
    grommet = add_cyl("grommet", GROMMET_R, 0.02,
        loc=(0, 0, -PANEL_H/2 - 0.008))
    bool_op(panel, grommet, 'UNION')
    return panel

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
    print(f"[VPump_StatusArray] V:{v} F:{f} Q:{q}/{f} ({100*q//max(f,1)}%) NM:{nm} WT:{'YES' if nm==0 else 'NO'}")

def export(obj):
    bpy.ops.object.select_all(action='DESELECT'); obj.select_set(True)
    bpy.context.view_layer.objects.active = obj
    os.makedirs(os.path.dirname(OUT_FILE), exist_ok=True)
    bpy.ops.export_scene.gltf(filepath=OUT_FILE, export_format='GLB', use_selection=True, export_apply=True, export_draco_mesh_compression_enable=True)
    print(f"[VPump_StatusArray] Exported: {OUT_FILE} ({os.path.getsize(OUT_FILE)/1024:.1f} KB)")

if __name__ == "__main__":
    clean_scene(); mat = make_material(); obj = create_geometry(); polish(obj, mat); verify(obj); export(obj)
