"""
Blender Headless Mesh Generator
Product: V-Man  |  Component: EndEffectorKit
Run: blender --background --python this_script.py

Representative end-effector assembly (vacuum gripper, parallel jaw, F/T sensor).
PATENT reference: Section 10.3 — mounted on arm tool flange.

Positioned at arm TCP (varies with arm pose).
"""
import bpy, bmesh, math, os

PRODUCT = "VMan"
COMPONENT = "EndEffectorKit"
MATERIAL = "Al6061T6"
OUT_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT_FILE = f"{PRODUCT}_{COMPONENT}.glb"

ADAPTER_R = 0.035
ADAPTER_H = 0.008
BOLT_R = 0.003
BOLT_H = 0.012
BOLT_CIRCLE_R = 0.025
FT_OUTER_R = 0.032
FT_INNER_R = 0.022
FT_H = 0.012
BAR_W = 0.140
BAR_H = 0.008
BAR_D = 0.040
VAC_BODY_R = 0.025
VAC_BODY_H = 0.040
VAC_X_OFFSET = -0.060
CUP_R = 0.008
CUP_H = 0.010
BELLOW_R = 0.010
BELLOW_H = 0.003
CUP_CIRCLE_R = 0.015
CUP_COUNT = 3
FITTING_R = 0.005
FITTING_H = 0.015
GRIP_W = 0.050
GRIP_H = 0.030
GRIP_D = 0.080
GRIP_X_OFFSET = 0.060
JAW_W = 0.008
JAW_H = 0.050
JAW_D = 0.060
JAW_GAP = 0.040
RAIL_R = 0.003
RAIL_LEN = 0.060

PBR = {
    "base_color": (0.75, 0.78, 0.80, 1.0),
    "metallic": 1.0,
    "roughness": 0.30,
    "alpha": 1.0,
    "emission": (0.0, 0.0, 0.0, 1.0),
    "emission_strength": 0.0,
}

BEVEL_WIDTH = 0.0008
BEVEL_SEGMENTS = 2

def clean_scene():
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete(use_global=False)
    for block in bpy.data.meshes:
        if block.users == 0:
            bpy.data.meshes.remove(block)
    for block in bpy.data.materials:
        if block.users == 0:
            bpy.data.materials.remove(block)

def setup_scene():
    bpy.context.scene.name = "Scene0"
    bpy.context.scene.unit_settings.system = 'METRIC'
    bpy.context.scene.unit_settings.scale_length = 1.0

def create_material():
    mat = bpy.data.materials.new(name=f"MAT_{PRODUCT}_{MATERIAL}")
    mat.use_nodes = True
    mat.use_backface_culling = True
    nodes = mat.node_tree.nodes
    links = mat.node_tree.links
    nodes.clear()
    bsdf = nodes.new('ShaderNodeBsdfPrincipled')
    bsdf.inputs['Base Color'].default_value = PBR["base_color"]
    bsdf.inputs['Metallic'].default_value = PBR["metallic"]
    bsdf.inputs['Roughness'].default_value = PBR["roughness"]
    bsdf.inputs['Alpha'].default_value = PBR["alpha"]
    bsdf.inputs['Emission Color'].default_value = PBR["emission"]
    bsdf.inputs['Emission Strength'].default_value = PBR["emission_strength"]
    output = nodes.new('ShaderNodeOutputMaterial')
    output.location = (300, 0)
    links.new(bsdf.outputs['BSDF'], output.inputs['Surface'])
    return mat

def add_box(w, h, d, loc=(0, 0, 0)):
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=loc)
    obj = bpy.context.active_object
    obj.scale = (w, h, d)
    bpy.ops.object.transform_apply(scale=True)
    return obj

def add_cyl(radius, depth, vertices=24, loc=(0, 0, 0), rot=(0, 0, 0)):
    bpy.ops.mesh.primitive_cylinder_add(vertices=vertices, radius=radius, depth=depth, location=loc, rotation=rot)
    return bpy.context.active_object

def bool_op(target, cutter, operation='UNION'):
    mod = target.modifiers.new(operation, 'BOOLEAN')
    mod.operation = operation
    mod.object = cutter
    mod.solver = 'EXACT'
    bpy.context.view_layer.objects.active = target
    bpy.ops.object.modifier_apply(modifier=operation)
    bpy.data.objects.remove(cutter, do_unlink=True)

def create_geometry():
    y_cursor = 0.0
    
    adapter_center_y = y_cursor - ADAPTER_H / 2
    root = add_cyl(ADAPTER_R, ADAPTER_H, 32, loc=(0, adapter_center_y, 0))
    
    for i in range(4):
        angle = math.radians(90 * i + 45)
        bx = BOLT_CIRCLE_R * math.cos(angle)
        bz = BOLT_CIRCLE_R * math.sin(angle)
        bolt = add_cyl(BOLT_R, BOLT_H, 10, loc=(bx, adapter_center_y, bz))
        bool_op(root, bolt, 'DIFFERENCE')
    y_cursor -= ADAPTER_H
    
    ft_center_y = y_cursor - FT_H / 2
    ft_outer = add_cyl(FT_OUTER_R, FT_H, 32, loc=(0, ft_center_y, 0))
    ft_inner = add_cyl(FT_INNER_R, FT_H + 0.002, 32, loc=(0, ft_center_y, 0))
    bool_op(ft_outer, ft_inner, 'DIFFERENCE')
    bool_op(root, ft_outer, 'UNION')
    y_cursor -= FT_H
    
    bar_center_y = y_cursor - BAR_H / 2
    bar = add_box(BAR_W, BAR_H, BAR_D, loc=(0, bar_center_y, 0))
    bool_op(root, bar, 'UNION')
    y_cursor -= BAR_H
    
    vac_center_y = y_cursor - VAC_BODY_H / 2
    vac_body = add_cyl(VAC_BODY_R, VAC_BODY_H, 24, loc=(VAC_X_OFFSET, vac_center_y, 0))
    bool_op(root, vac_body, 'UNION')
    
    fitting_bottom = y_cursor
    fitting_center_y = fitting_bottom + FITTING_H / 2
    fitting = add_cyl(FITTING_R, FITTING_H, 10, loc=(VAC_X_OFFSET, fitting_center_y, 0))
    bool_op(root, fitting, 'UNION')
    
    for i in range(CUP_COUNT):
        angle = math.radians(120 * i)
        cx = VAC_X_OFFSET + CUP_CIRCLE_R * math.cos(angle)
        cz = CUP_CIRCLE_R * math.sin(angle)
        cup_top = y_cursor - VAC_BODY_H
        cup_center_y = cup_top - CUP_H / 2
        cup = add_cyl(CUP_R, CUP_H, 12, loc=(cx, cup_center_y, cz))
        bool_op(root, cup, 'UNION')
        bellow_top = cup_top - CUP_H
        bellow_center_y = bellow_top - BELLOW_H / 2
        bellow = add_cyl(BELLOW_R, BELLOW_H, 12, loc=(cx, bellow_center_y, cz))
        bool_op(root, bellow, 'UNION')
    
    grip_center_y = y_cursor - GRIP_H / 2
    grip_body = add_box(GRIP_W, GRIP_H, GRIP_D, loc=(GRIP_X_OFFSET, grip_center_y, 0))
    bool_op(root, grip_body, 'UNION')
    
    jaw_top = y_cursor - GRIP_H
    jaw_center_y = jaw_top - JAW_H / 2
    jaw_left_x = GRIP_X_OFFSET - JAW_GAP / 2
    jaw_l = add_box(JAW_W, JAW_H, JAW_D, loc=(jaw_left_x, jaw_center_y, 0))
    bool_op(root, jaw_l, 'UNION')
    
    jaw_right_x = GRIP_X_OFFSET + JAW_GAP / 2
    jaw_r = add_box(JAW_W, JAW_H, JAW_D, loc=(jaw_right_x, jaw_center_y, 0))
    bool_op(root, jaw_r, 'UNION')
    
    rail_center_y = jaw_top - 0.010
    rail = add_cyl(RAIL_R, RAIL_LEN, 10, loc=(GRIP_X_OFFSET, rail_center_y, 0.020), rot=(0, 0, math.pi / 2))
    bool_op(root, rail, 'UNION')
    
    root.name = f"{PRODUCT}_{COMPONENT}"
    root.data.name = f"{PRODUCT}_{COMPONENT}_mesh"
    return root

def polish(obj):
    bevel = obj.modifiers.new("Bevel", 'BEVEL')
    bevel.width = BEVEL_WIDTH
    bevel.segments = BEVEL_SEGMENTS
    bevel.limit_method = 'ANGLE'
    bevel.angle_limit = math.radians(30)
    bevel.harden_normals = True
    bpy.context.view_layer.objects.active = obj
    bpy.ops.object.modifier_apply(modifier="Bevel")
    bpy.ops.object.shade_auto_smooth()
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.mesh.select_all(action='SELECT')
    bpy.ops.uv.smart_project(angle_limit=math.radians(66), island_margin=0.02)
    bpy.ops.mesh.normals_make_consistent(inside=False)
    bpy.ops.mesh.remove_doubles(threshold=0.0001)
    bpy.ops.object.mode_set(mode='OBJECT')
    bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
    bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY', center='BOUNDS')

def verify(obj):
    bm = bmesh.new()
    bm.from_mesh(obj.data)
    verts = len(bm.verts)
    edges = len(bm.edges)
    faces = len(bm.faces)
    quads = sum(1 for f in bm.faces if len(f.verts) == 4)
    non_manifold = sum(1 for e in bm.edges if not e.is_manifold)
    xs = [v.co.x for v in bm.verts]
    ys = [v.co.y for v in bm.verts]
    zs = [v.co.z for v in bm.verts]
    print(f"\n  MESH: {obj.name}")
    print(f"  Verts: {verts}  Edges: {edges}  Faces: {faces}")
    print(f"  Quads: {quads}/{faces} ({100 * quads / max(faces, 1):.0f}%)")
    print(f"  Non-manifold edges: {non_manifold}  Watertight: {'YES' if non_manifold == 0 else 'FIX'}")
    print(f"  AABB min: ({min(xs):.4f}, {min(ys):.4f}, {min(zs):.4f})")
    print(f"  AABB max: ({max(xs):.4f}, {max(ys):.4f}, {max(zs):.4f})")
    print(f"  PATENT alignment: End-effector kit, mounted on arm tool flange")
    bm.free()

def export(obj):
    os.makedirs(OUT_DIR, exist_ok=True)
    path = os.path.join(OUT_DIR, OUT_FILE)
    bpy.ops.object.select_all(action='DESELECT')
    obj.select_set(True)
    bpy.context.view_layer.objects.active = obj
    bpy.ops.export_scene.gltf(filepath=path, export_format='GLB', use_selection=True, export_apply=True, export_normals=True, export_materials='EXPORT', export_cameras=False, export_lights=False, export_animations=False, export_yup=True, export_draco_mesh_compression_enable=True, export_draco_mesh_compression_level=6)
    print(f"  EXPORTED: {path} ({os.path.getsize(path) / 1024:.1f} KB)\n")

def main():
    clean_scene()
    setup_scene()
    mat = create_material()
    obj = create_geometry()
    obj.data.materials.append(mat)
    polish(obj)
    verify(obj)
    export(obj)

if __name__ == "__main__":
    main()
