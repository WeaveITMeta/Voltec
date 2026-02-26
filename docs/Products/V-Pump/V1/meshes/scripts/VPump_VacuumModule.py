# ============================================================================
# VPump_VacuumModule.py — Oil-free rotary vane vacuum-assist priming unit
# Multi-body: cylindrical body + inlet/outlet ports + motor housing + base plate
# ============================================================================
import bpy, bmesh, math, os

BODY_R = 0.18; BODY_LEN = 0.45
PORT_R = 0.03; PORT_LEN = 0.10
MOTOR_R = 0.12; MOTOR_LEN = 0.25
BASE_W, BASE_D, BASE_H = 0.50, 0.40, 0.02

MAT_COLOR = (0.65, 0.67, 0.70, 1.0); MAT_METAL = 1.0; MAT_ROUGH = 0.40

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
OUT_DIR = os.path.normpath(os.path.join(SCRIPT_DIR, ".."))
OUT_FILE = os.path.join(OUT_DIR, "VPump_VacuumModule.glb")
OBJ_NAME = "VPump_VacuumModule"; SCENE_NAME = "Scene0"

def clean_scene():
    bpy.ops.wm.read_factory_settings(use_empty=True); bpy.context.scene.name = SCENE_NAME

def make_material():
    mat = bpy.data.materials.new(name="MAT_VPump_316L_Vac")
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
    # Main pump body (horizontal cylinder)
    body = add_cyl("body", BODY_R, BODY_LEN, rot=(math.pi/2, 0, 0))
    # Inlet port (top)
    inlet = add_cyl("inlet", PORT_R, PORT_LEN, loc=(0, BODY_R + PORT_LEN/2, -0.1))
    bool_op(body, inlet, 'UNION')
    # Outlet port (side)
    outlet = add_cyl("outlet", PORT_R, PORT_LEN, loc=(BODY_R + PORT_LEN/2, 0, 0.1), rot=(0, math.pi/2, 0))
    bool_op(body, outlet, 'UNION')
    # Motor housing (rear)
    motor = add_cyl("motor", MOTOR_R, MOTOR_LEN, rot=(math.pi/2, 0, 0), loc=(0, -BODY_LEN/2 - MOTOR_LEN/2, 0))
    bool_op(body, motor, 'UNION')
    # Cooling fins on motor (5 rings)
    for i in range(5):
        y = -BODY_LEN/2 - 0.05 - i * 0.04
        fin = add_cyl(f"fin_{i}", MOTOR_R + 0.015, 0.005, rot=(math.pi/2, 0, 0), loc=(0, y, 0))
        bool_op(body, fin, 'UNION')
    # Base mounting plate
    base = add_cube("base", (BASE_W, BASE_D, BASE_H), loc=(0, 0, -BODY_R - BASE_H/2))
    bool_op(body, base, 'UNION')
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
    print(f"[VPump_VacuumModule] V:{v} F:{f} Q:{q}/{f} ({100*q//max(f,1)}%) NM:{nm} WT:{'YES' if nm==0 else 'NO'}")

def export(obj):
    bpy.ops.object.select_all(action='DESELECT'); obj.select_set(True)
    bpy.context.view_layer.objects.active = obj
    os.makedirs(os.path.dirname(OUT_FILE), exist_ok=True)
    bpy.ops.export_scene.gltf(filepath=OUT_FILE, export_format='GLB', use_selection=True, export_apply=True, export_draco_mesh_compression_enable=True)
    print(f"[VPump_VacuumModule] Exported: {OUT_FILE} ({os.path.getsize(OUT_FILE)/1024:.1f} KB)")

if __name__ == "__main__":
    clean_scene(); mat = make_material(); obj = create_geometry(); polish(obj, mat); verify(obj); export(obj)
