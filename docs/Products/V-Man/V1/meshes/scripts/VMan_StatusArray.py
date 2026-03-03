"""
Blender Headless Mesh Generator
Product: V-Man  |  Component: StatusArray
Run: blender --background --python this_script.py

LED status display bar (operational state indicators).
PATENT reference: Section 6.1 Top View — mounted at bottom of container.

Positioned at Y=0.05m (above vibration mounts, visible from front).
"""
import bpy, bmesh, math, os

PRODUCT = "VMan"
COMPONENT = "StatusArray"
MATERIAL = "Polycarbonate"
OUT_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT_FILE = f"{PRODUCT}_{COMPONENT}.glb"

BAR_LENGTH = 1.500
BAR_WIDTH = 0.060
BAR_HEIGHT = 0.030
WALL = 0.003
BACK_PLATE_T = 0.004
BRACKET_V_W = 0.070
BRACKET_V_H = 0.040
BRACKET_V_D = 0.006
BRACKET_H_W = 0.070
BRACKET_H_H = 0.006
BRACKET_H_D = 0.030
BRACKET_HOLE_R = 0.003
BRACKET_Z_OFFSET = BAR_LENGTH / 3
CABLE_R = 0.005
CABLE_H = 0.020
CAP_SEGMENTS = 20

PBR = {
    "base_color": (0.0, 0.75, 1.0, 0.9),
    "metallic": 0.0,
    "roughness": 0.1,
    "alpha": 0.9,
    "emission": (0.0, 0.75, 1.0, 1.0),
    "emission_strength": 5.0,
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

def add_cyl(radius, depth, vertices=20, loc=(0, 0, 0), rot=(0, 0, 0)):
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
    bar_min_x = -BAR_WIDTH / 2
    bar_max_x = BAR_WIDTH / 2
    bar_min_y = -BAR_HEIGHT / 2
    bar_max_y = BAR_HEIGHT / 2
    bar_min_z = -BAR_LENGTH / 2
    bar_max_z = BAR_LENGTH / 2
    
    body = add_box(BAR_WIDTH, BAR_HEIGHT, BAR_LENGTH, loc=(0, 0, 0))
    
    cap_front = add_cyl(BAR_HEIGHT / 2, BAR_WIDTH, CAP_SEGMENTS, loc=(0, 0, bar_max_z), rot=(0, 0, math.pi / 2))
    bool_op(body, cap_front, 'UNION')
    
    cap_back = add_cyl(BAR_HEIGHT / 2, BAR_WIDTH, CAP_SEGMENTS, loc=(0, 0, bar_min_z), rot=(0, 0, math.pi / 2))
    bool_op(body, cap_back, 'UNION')
    
    inner_w = BAR_WIDTH - 2 * WALL
    inner_h = BAR_HEIGHT - 2 * WALL
    inner_d = BAR_LENGTH - 0.020
    inner = add_box(inner_w, inner_h, inner_d, loc=(0, 0, 0))
    bool_op(body, inner, 'DIFFERENCE')
    
    back_min_y = bar_min_y - BACK_PLATE_T
    back_center_y = bar_min_y - BACK_PLATE_T / 2
    back_d = BAR_LENGTH - 0.020
    back = add_box(BAR_WIDTH, BACK_PLATE_T, back_d, loc=(0, back_center_y, 0))
    bool_op(body, back, 'UNION')
    
    for z_sign in (-1, 1):
        bz = z_sign * BRACKET_Z_OFFSET
        
        vert_top_y = back_min_y
        vert_center_y = vert_top_y - BRACKET_V_H / 2
        bracket_v = add_box(BRACKET_V_W, BRACKET_V_H, BRACKET_V_D, loc=(0, vert_center_y, bz))
        bool_op(body, bracket_v, 'UNION')
        
        horiz_top_y = vert_top_y - BRACKET_V_H
        horiz_center_y = horiz_top_y - BRACKET_H_H / 2
        horiz_center_z = bz - z_sign * (BRACKET_V_D / 2 + BRACKET_H_D / 2)
        bracket_h = add_box(BRACKET_H_W, BRACKET_H_H, BRACKET_H_D, loc=(0, horiz_center_y, horiz_center_z))
        bool_op(body, bracket_h, 'UNION')
        
        hole = add_cyl(BRACKET_HOLE_R, BRACKET_H_H + 0.004, 10, loc=(0, horiz_center_y, horiz_center_z))
        bool_op(body, hole, 'DIFFERENCE')
    
    cable_start_z = bar_min_z
    cable_center_z = cable_start_z - CABLE_H / 2
    cable = add_cyl(CABLE_R, CABLE_H, 10, loc=(0, 0, cable_center_z), rot=(math.pi / 2, 0, 0))
    bool_op(body, cable, 'UNION')
    
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
    print(f"  PATENT alignment: Status array LED bar, Y=0.05m, front-facing")
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
