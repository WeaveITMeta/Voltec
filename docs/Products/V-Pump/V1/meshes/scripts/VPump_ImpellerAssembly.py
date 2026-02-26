# ============================================================================
# VPump_ImpellerAssembly.py — 3-stage axial-flow impeller with guide vanes
# Multi-body: hub cylinder + 3 rotor blade rings + 3 guide vane rings
# ============================================================================
import bpy, bmesh, math, os

HUB_R = 0.20; HUB_LEN = 3.0
BLADE_R = 0.55; BLADE_THICK = 0.012; BLADE_W = 0.15
VANE_R = 0.57; VANE_THICK = 0.008; VANE_W = 0.10
STAGE_SPACING = 0.9; NUM_BLADES = 7; NUM_VANES = 11

MAT_COLOR = (0.72, 0.74, 0.76, 1.0); MAT_METAL = 1.0; MAT_ROUGH = 0.25

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
OUT_DIR = os.path.normpath(os.path.join(SCRIPT_DIR, ".."))
OUT_FILE = os.path.join(OUT_DIR, "VPump_ImpellerAssembly.glb")
OBJ_NAME = "VPump_ImpellerAssembly"; SCENE_NAME = "Scene0"

def clean_scene():
    bpy.ops.wm.read_factory_settings(use_empty=True); bpy.context.scene.name = SCENE_NAME

def make_material():
    mat = bpy.data.materials.new(name="MAT_VPump_SuperDuplex")
    mat.use_nodes = True; bsdf = mat.node_tree.nodes.get("Principled BSDF")
    bsdf.inputs["Base Color"].default_value = MAT_COLOR
    bsdf.inputs["Metallic"].default_value = MAT_METAL
    bsdf.inputs["Roughness"].default_value = MAT_ROUGH
    return mat

def add_cyl(name, r, d, loc=(0,0,0), segs=48):
    bpy.ops.mesh.primitive_cylinder_add(radius=r, depth=d, vertices=segs, location=loc)
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
    # Central hub shaft
    hub = add_cyl("hub", HUB_R, HUB_LEN)
    # 3 stages of rotor blades + guide vanes
    for stage in range(3):
        z_center = -STAGE_SPACING + stage * STAGE_SPACING
        # Rotor blades
        for i in range(NUM_BLADES):
            angle = 2 * math.pi * i / NUM_BLADES
            x = (HUB_R + BLADE_R) / 2 * math.cos(angle)
            y = (HUB_R + BLADE_R) / 2 * math.sin(angle)
            blade = add_cube(f"bl_{stage}_{i}",
                (BLADE_THICK, (BLADE_R - HUB_R), BLADE_W),
                loc=(x, y, z_center),
                rot=(0, 0, angle + math.radians(25)))  # 25° blade angle
            bool_op(hub, blade, 'UNION')
        # Guide vane ring (slightly larger, between stages)
        z_vane = z_center + STAGE_SPACING / 2
        if stage < 2:  # No guide vane after last stage
            ring = add_cyl(f"vr_{stage}", VANE_R, VANE_W, loc=(0, 0, z_vane))
            ring_hole = add_cyl(f"vrh_{stage}", BLADE_R - 0.01, VANE_W + 0.01, loc=(0, 0, z_vane))
            bool_op(ring, ring_hole, 'DIFFERENCE')
            # Guide vane slots (simplified as thin cubes)
            for j in range(NUM_VANES):
                angle = 2 * math.pi * j / NUM_VANES
                vx = (BLADE_R + VANE_R) / 2 * math.cos(angle)
                vy = (BLADE_R + VANE_R) / 2 * math.sin(angle)
                vane = add_cube(f"gv_{stage}_{j}",
                    (VANE_THICK, (VANE_R - BLADE_R + 0.02), VANE_W * 0.8),
                    loc=(vx, vy, z_vane),
                    rot=(0, 0, angle - math.radians(15)))
                bool_op(ring, vane, 'UNION')
            bool_op(hub, ring, 'UNION')
    return hub

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
    print(f"[VPump_ImpellerAssembly] V:{v} F:{f} Q:{q}/{f} ({100*q//max(f,1)}%) NM:{nm} WT:{'YES' if nm==0 else 'NO'}")

def export(obj):
    bpy.ops.object.select_all(action='DESELECT'); obj.select_set(True)
    bpy.context.view_layer.objects.active = obj
    os.makedirs(os.path.dirname(OUT_FILE), exist_ok=True)
    bpy.ops.export_scene.gltf(filepath=OUT_FILE, export_format='GLB', use_selection=True, export_apply=True, export_draco_mesh_compression_enable=True)
    print(f"[VPump_ImpellerAssembly] Exported: {OUT_FILE} ({os.path.getsize(OUT_FILE)/1024:.1f} KB)")

if __name__ == "__main__":
    clean_scene(); mat = make_material(); obj = create_geometry(); polish(obj, mat); verify(obj); export(obj)
