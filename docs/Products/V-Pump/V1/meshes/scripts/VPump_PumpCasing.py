# ============================================================================
# VPump_PumpCasing.py — Duplex SS pressure casing with flanged ends
# Multi-body assembly: thick-walled cylinder + inlet/outlet flanges + 
# mounting feet + lifting lugs + drain port
# ============================================================================
import bpy, bmesh, math, os, sys

# --- Dimensions (meters, VP-M frame DN1200) ---
BODY_RADIUS = 0.625       # Outer radius of casing body
BODY_LENGTH = 4.5          # Overall length
WALL_THICK = 0.025         # 25mm wall thickness
FLANGE_RADIUS = 0.85       # Flange outer radius
FLANGE_THICK = 0.08        # Flange thickness
FOOT_W, FOOT_H, FOOT_D = 0.4, 0.15, 0.6  # Mounting foot dims
DRAIN_R = 0.04             # Drain port radius
LUG_R = 0.06               # Lifting lug radius

# --- PBR Material ---
MAT_COLOR = (0.68, 0.70, 0.72, 1.0)  # Brushed duplex steel
MAT_METAL = 1.0
MAT_ROUGH = 0.35

# --- Output ---
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
OUT_DIR = os.path.normpath(os.path.join(SCRIPT_DIR, ".."))
OUT_FILE = os.path.join(OUT_DIR, "VPump_PumpCasing.glb")
OBJ_NAME = "VPump_PumpCasing"
SCENE_NAME = "Scene0"

# ============================================================================
# Helpers
# ============================================================================
def clean_scene():
    bpy.ops.wm.read_factory_settings(use_empty=True)
    scene = bpy.context.scene
    scene.name = SCENE_NAME

def make_material():
    mat = bpy.data.materials.new(name=f"MAT_VPump_DuplexSS")
    mat.use_nodes = True
    bsdf = mat.node_tree.nodes.get("Principled BSDF")
    bsdf.inputs["Base Color"].default_value = MAT_COLOR
    bsdf.inputs["Metallic"].default_value = MAT_METAL
    bsdf.inputs["Roughness"].default_value = MAT_ROUGH
    return mat

def add_cylinder(name, r, depth, loc=(0,0,0), rot=(0,0,0), segs=48):
    bpy.ops.mesh.primitive_cylinder_add(radius=r, depth=depth, vertices=segs, location=loc, rotation=rot)
    obj = bpy.context.active_object
    obj.name = name
    return obj

def add_cube(name, size, loc=(0,0,0)):
    bpy.ops.mesh.primitive_cube_add(size=1, location=loc, scale=size)
    obj = bpy.context.active_object
    obj.name = name
    return obj

def add_torus(name, major_r, minor_r, loc=(0,0,0), rot=(0,0,0)):
    bpy.ops.mesh.primitive_torus_add(major_radius=major_r, minor_radius=minor_r, location=loc, rotation=rot)
    obj = bpy.context.active_object
    obj.name = name
    return obj

def bool_op(target, cutter, operation='UNION'):
    mod = target.modifiers.new(name=operation, type='BOOLEAN')
    mod.operation = operation
    mod.solver = 'EXACT'
    mod.object = cutter
    bpy.context.view_layer.objects.active = target
    bpy.ops.object.modifier_apply(modifier=mod.name)
    bpy.data.objects.remove(cutter, do_unlink=True)

def create_geometry():
    # Main body — thick-walled cylinder
    outer = add_cylinder("outer", BODY_RADIUS, BODY_LENGTH)
    inner = add_cylinder("inner", BODY_RADIUS - WALL_THICK, BODY_LENGTH - 0.02)
    bool_op(outer, inner, 'DIFFERENCE')

    # Inlet flange
    fl_in = add_cylinder("fl_in", FLANGE_RADIUS, FLANGE_THICK, loc=(0, 0, -BODY_LENGTH/2 + FLANGE_THICK/2))
    bool_op(outer, fl_in, 'UNION')

    # Outlet flange
    fl_out = add_cylinder("fl_out", FLANGE_RADIUS, FLANGE_THICK, loc=(0, 0, BODY_LENGTH/2 - FLANGE_THICK/2))
    bool_op(outer, fl_out, 'UNION')

    # Mounting feet (×2)
    for x_sign in [-1, 1]:
        foot = add_cube(f"foot_{x_sign}", (FOOT_W, FOOT_D, FOOT_H), loc=(x_sign * 0.45, 0, -BODY_RADIUS - FOOT_H/2 + 0.02))
        # Rotate foot to be below casing
        foot.location = (x_sign * 0.45, 0, 0)
        foot.location.z = -BODY_RADIUS - FOOT_H/2
        bool_op(outer, foot, 'UNION')

    # Drain port (bottom, near outlet end)
    drain = add_cylinder("drain", DRAIN_R, 0.12, loc=(0, 0, 1.5), rot=(math.pi/2, 0, 0))
    drain.location.y = -BODY_RADIUS - 0.04
    bool_op(outer, drain, 'UNION')

    # Lifting lugs (×2 on top)
    for z_off in [-1.0, 1.0]:
        lug = add_torus(f"lug_{z_off}", LUG_R, 0.015, loc=(0, BODY_RADIUS + LUG_R * 0.7, z_off))
        bool_op(outer, lug, 'UNION')

    return outer

def polish(obj, mat):
    obj.name = OBJ_NAME
    obj.data.materials.append(mat)
    bpy.context.view_layer.objects.active = obj
    # Bevel hard edges
    mod = obj.modifiers.new(name="Bevel", type='BEVEL')
    mod.width = 0.003
    mod.segments = 2
    mod.limit_method = 'ANGLE'
    mod.angle_limit = math.radians(30)
    bpy.ops.object.modifier_apply(modifier=mod.name)
    # Auto smooth
    bpy.ops.object.shade_auto_smooth()
    # UV
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.mesh.select_all(action='SELECT')
    bpy.ops.uv.smart_project(angle_limit=66, island_margin=0.01)
    bpy.ops.object.mode_set(mode='OBJECT')
    # Normals
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.transform_apply(location=False, rotation=True, scale=True)

def verify(obj):
    bm = bmesh.new()
    bm.from_mesh(obj.data)
    verts = len(bm.verts)
    faces = len(bm.faces)
    quads = sum(1 for f in bm.faces if len(f.verts) == 4)
    non_manifold = sum(1 for e in bm.edges if not e.is_manifold)
    watertight = non_manifold == 0
    bm.free()
    print(f"[VPump_PumpCasing] Verts: {verts} | Faces: {faces} | Quads: {quads}/{faces} ({100*quads//max(faces,1)}%) | Non-manifold: {non_manifold} | Watertight: {'YES' if watertight else 'NO'}")

def export(obj):
    bpy.ops.object.select_all(action='DESELECT')
    obj.select_set(True)
    bpy.context.view_layer.objects.active = obj
    os.makedirs(os.path.dirname(OUT_FILE), exist_ok=True)
    bpy.ops.export_scene.gltf(
        filepath=OUT_FILE, export_format='GLB',
        use_selection=True, export_apply=True,
        export_draco_mesh_compression_enable=True
    )
    size_kb = os.path.getsize(OUT_FILE) / 1024
    print(f"[VPump_PumpCasing] Exported: {OUT_FILE} ({size_kb:.1f} KB)")

# ============================================================================
if __name__ == "__main__":
    clean_scene()
    mat = make_material()
    obj = create_geometry()
    polish(obj, mat)
    verify(obj)
    export(obj)
