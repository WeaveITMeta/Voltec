# ============================================================================
# VPump_ControlModule.py — V-Mind AI control enclosure with display + cable glands
# Multi-body: NEMA 4X box + hinged door + display cutout + cable gland ports +
# ventilation grille + DIN rail brackets + conduit stubs
# ============================================================================
import bpy, bmesh, math, os

BOX_W, BOX_H, BOX_D = 0.60, 0.80, 0.35
WALL = 0.005
DOOR_INSET = 0.003
DISPLAY_W, DISPLAY_H = 0.18, 0.12
GLAND_R = 0.012; GLAND_COUNT = 8
VENT_W, VENT_H = 0.15, 0.08
CONDUIT_R = 0.02; CONDUIT_LEN = 0.08

MAT_COLOR = (0.82, 0.84, 0.86, 1.0); MAT_METAL = 1.0; MAT_ROUGH = 0.30

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
OUT_DIR = os.path.normpath(os.path.join(SCRIPT_DIR, ".."))
OUT_FILE = os.path.join(OUT_DIR, "VPump_ControlModule.glb")
OBJ_NAME = "VPump_ControlModule"; SCENE_NAME = "Scene0"

def clean_scene():
    bpy.ops.wm.read_factory_settings(use_empty=True); bpy.context.scene.name = SCENE_NAME

def make_material():
    mat = bpy.data.materials.new(name="MAT_VPump_316L_Ctrl")
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

def bool_op(target, cutter, operation='UNION'):
    mod = target.modifiers.new(name=operation, type='BOOLEAN')
    mod.operation = operation; mod.solver = 'EXACT'; mod.object = cutter
    bpy.context.view_layer.objects.active = target
    bpy.ops.object.modifier_apply(modifier=mod.name)
    bpy.data.objects.remove(cutter, do_unlink=True)

def create_geometry():
    # Outer box
    outer = add_cube("outer", (BOX_W, BOX_D, BOX_H))
    inner = add_cube("inner", (BOX_W - 2*WALL, BOX_D - 2*WALL, BOX_H - 2*WALL))
    bool_op(outer, inner, 'DIFFERENCE')
    # Door panel (front face, slightly proud)
    door = add_cube("door", (BOX_W - 0.02, WALL, BOX_H - 0.02), loc=(0, BOX_D/2 - DOOR_INSET, 0))
    bool_op(outer, door, 'UNION')
    # Display cutout in door
    display = add_cube("display", (DISPLAY_W, WALL + 0.01, DISPLAY_H), loc=(0, BOX_D/2 - DOOR_INSET, 0.12))
    bool_op(outer, display, 'DIFFERENCE')
    # Cable gland ports (bottom row)
    for i in range(GLAND_COUNT):
        x = -BOX_W/2 + 0.06 + i * (BOX_W - 0.12) / (GLAND_COUNT - 1)
        gland = add_cyl(f"gl_{i}", GLAND_R, 0.04, loc=(x, 0, -BOX_H/2 - 0.01))
        bool_op(outer, gland, 'UNION')
    # Ventilation grille (top, simplified as cutout)
    vent = add_cube("vent", (VENT_W, BOX_D * 0.5, WALL + 0.01), loc=(0, 0, BOX_H/2))
    bool_op(outer, vent, 'DIFFERENCE')
    # DIN rail mounting brackets (inside, 2x on back wall)
    for z_off in [-0.15, 0.15]:
        rail = add_cube(f"rail_{z_off}", (BOX_W * 0.8, 0.01, 0.035), loc=(0, -BOX_D/2 + WALL + 0.01, z_off))
        bool_op(outer, rail, 'UNION')
    # Conduit entry stubs (bottom, 2x)
    for x_off in [-0.15, 0.15]:
        conduit = add_cyl(f"cond_{x_off}", CONDUIT_R, CONDUIT_LEN, loc=(x_off, 0, -BOX_H/2 - CONDUIT_LEN/2))
        bool_op(outer, conduit, 'UNION')
    # Mounting bracket tabs (×4 corners on back)
    for x_sign in [-1, 1]:
        for z_sign in [-1, 1]:
            tab = add_cube(f"tab_{x_sign}_{z_sign}",
                (0.04, 0.03, 0.04),
                loc=(x_sign * (BOX_W/2 - 0.01), -BOX_D/2 - 0.01, z_sign * (BOX_H/2 - 0.03)))
            bool_op(outer, tab, 'UNION')
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
    print(f"[VPump_ControlModule] V:{v} F:{f} Q:{q}/{f} ({100*q//max(f,1)}%) NM:{nm} WT:{'YES' if nm==0 else 'NO'}")

def export(obj):
    bpy.ops.object.select_all(action='DESELECT'); obj.select_set(True)
    bpy.context.view_layer.objects.active = obj
    os.makedirs(os.path.dirname(OUT_FILE), exist_ok=True)
    bpy.ops.export_scene.gltf(filepath=OUT_FILE, export_format='GLB', use_selection=True, export_apply=True, export_draco_mesh_compression_enable=True)
    print(f"[VPump_ControlModule] Exported: {OUT_FILE} ({os.path.getsize(OUT_FILE)/1024:.1f} KB)")

if __name__ == "__main__":
    clean_scene(); mat = make_material(); obj = create_geometry(); polish(obj, mat); verify(obj); export(obj)
