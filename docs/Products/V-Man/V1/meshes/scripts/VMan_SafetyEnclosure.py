"""
Blender Headless Mesh Generator
Product: V-Man  |  Component: SafetyEnclosure
Run: blender --background --python this_script.py

Safety enclosure (light curtains, interlocked doors, e-stops).
PATENT reference: Section 6.1 Top View — perimeter frame around U-cell.

Positioned at Y=0.0 (floor) to Y=2.50m (top of container).
"""
import bpy, bmesh, math, os

PRODUCT = "VMan"
COMPONENT = "SafetyEnclosure"
MATERIAL = "Polycarbonate"
OUT_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT_FILE = f"{PRODUCT}_{COMPONENT}.glb"

ENC_LENGTH = 10.0
ENC_WIDTH = 2.20
ENC_HEIGHT = 2.50
FRAME = 0.040
LC_W = 0.040
LC_H_FRAC = 0.80
LC_D = 0.040
LC_Z_OFFSET = 2.500
LC_INSET = 0.020
DOOR_H = 2.000
DOOR_W = 0.800
DOOR_Z = -ENC_LENGTH / 2 + 1.500
ESTOP_R = 0.025
ESTOP_H = 0.040
BUTTON_R = 0.018
BUTTON_H = 0.015
ESTOP_Y_FRAC = 0.60
ESTOP_Z_INSET = 0.500
POST_COUNT = 4

PBR = {
    "base_color": (0.90, 0.90, 0.10, 0.6),
    "metallic": 0.0,
    "roughness": 0.3,
    "alpha": 0.6,
    "emission": (0.0, 0.0, 0.0, 1.0),
    "emission_strength": 0.0,
}

BEVEL_WIDTH = 0.001
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
    if PBR["alpha"] < 1.0:
        mat.blend_method = 'BLEND'
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
    enc_min_x = -ENC_WIDTH / 2
    enc_max_x = ENC_WIDTH / 2
    enc_min_y = 0.0
    enc_max_y = ENC_HEIGHT
    enc_min_z = -ENC_LENGTH / 2
    enc_max_z = ENC_LENGTH / 2
    
    rail_center_y = enc_min_y + FRAME / 2
    body = add_box(FRAME, FRAME, ENC_LENGTH, loc=(enc_min_x + FRAME / 2, rail_center_y, 0))
    
    rail_r = add_box(FRAME, FRAME, ENC_LENGTH, loc=(enc_max_x - FRAME / 2, rail_center_y, 0))
    bool_op(body, rail_r, 'UNION')
    
    top_rail_center_y = enc_max_y - FRAME / 2
    top_l = add_box(FRAME, FRAME, ENC_LENGTH, loc=(enc_min_x + FRAME / 2, top_rail_center_y, 0))
    bool_op(body, top_l, 'UNION')
    
    top_r = add_box(FRAME, FRAME, ENC_LENGTH, loc=(enc_max_x - FRAME / 2, top_rail_center_y, 0))
    bool_op(body, top_r, 'UNION')
    
    post_height = ENC_HEIGHT
    post_center_y = enc_min_y + post_height / 2
    post_margin = 1.000
    post_z_start = enc_min_z + post_margin
    post_z_step = (ENC_LENGTH - 2 * post_margin) / (POST_COUNT - 1)
    for x_pos in (enc_min_x + FRAME / 2, enc_max_x - FRAME / 2):
        for i in range(POST_COUNT):
            z_pos = post_z_start + i * post_z_step
            post = add_box(FRAME, post_height, FRAME, loc=(x_pos, post_center_y, z_pos))
            bool_op(body, post, 'UNION')
    
    for z_pos in (enc_min_z + FRAME / 2, enc_max_z - FRAME / 2):
        cross_b = add_box(ENC_WIDTH, FRAME, FRAME, loc=(0, rail_center_y, z_pos))
        bool_op(body, cross_b, 'UNION')
        cross_t = add_box(ENC_WIDTH, FRAME, FRAME, loc=(0, top_rail_center_y, z_pos))
        bool_op(body, cross_t, 'UNION')
    
    lc_height = ENC_HEIGHT * LC_H_FRAC
    lc_center_y = enc_min_y + ENC_HEIGHT * 0.50
    for z_off in (-LC_Z_OFFSET, LC_Z_OFFSET):
        for x_sign in (-1, 1):
            lc_x = x_sign * (ENC_WIDTH / 2 - LC_INSET - LC_W / 2)
            col = add_box(LC_W, lc_height, LC_D, loc=(lc_x, lc_center_y, z_off))
            bool_op(body, col, 'UNION')
    
    door_min_y = enc_min_y + FRAME
    door_center_y = door_min_y + DOOR_H / 2
    door_x = enc_min_x + FRAME / 2
    
    door_left_z = DOOR_Z - DOOR_W / 2
    door_post_l = add_box(FRAME, DOOR_H, FRAME, loc=(door_x, door_center_y, door_left_z))
    bool_op(body, door_post_l, 'UNION')
    
    door_right_z = DOOR_Z + DOOR_W / 2
    door_post_r = add_box(FRAME, DOOR_H, FRAME, loc=(door_x, door_center_y, door_right_z))
    bool_op(body, door_post_r, 'UNION')
    
    lintel_y = door_min_y + DOOR_H
    lintel_center_y = lintel_y + FRAME / 2
    door_lintel = add_box(FRAME, FRAME, DOOR_W, loc=(door_x, lintel_center_y, DOOR_Z))
    bool_op(body, door_lintel, 'UNION')
    
    estop_y = enc_min_y + ENC_HEIGHT * ESTOP_Y_FRAC
    for x_sign in (-1, 1):
        estop_x = x_sign * (ENC_WIDTH / 2 - FRAME / 2)
        for z_sign in (-1, 1):
            estop_z = z_sign * (ENC_LENGTH / 2 - ESTOP_Z_INSET)
            housing = add_cyl(ESTOP_R, ESTOP_H, 16, loc=(estop_x, estop_y, estop_z))
            bool_op(body, housing, 'UNION')
            button_min_y = estop_y + ESTOP_H / 2
            button_center_y = button_min_y + BUTTON_H / 2
            button = add_cyl(BUTTON_R, BUTTON_H, 16, loc=(estop_x, button_center_y, estop_z))
            bool_op(body, button, 'UNION')
    
    body.name = f"{PRODUCT}_{COMPONENT}"
    body.data.name = f"{PRODUCT}_{COMPONENT}_mesh"
    return body

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
    print(f"  PATENT alignment: Safety enclosure perimeter, Y=0.0-2.50m")
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
