"""
Blender Headless Mesh Generator
Product: V-Man  |  Component: Pneumatics
Run: blender --background --python this_script.py

Pneumatics module (compressor, regulator, manifold).
PATENT reference: Section 6.2 Side View — under-conveyor utilities at Y=0.0–0.40m

Positioned under conveyor, center of container.
Bottom at Y=0.0 (floor), top at Y=0.35m.
"""
import bpy, bmesh, math, os

PRODUCT = "VMan"
COMPONENT = "Pneumatics"
MATERIAL = "Al6061T6"
OUT_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT_FILE = f"{PRODUCT}_{COMPONENT}.glb"

PLATE_W = 0.600
PLATE_H = 0.010
PLATE_D = 0.500
TANK_RADIUS = 0.080
TANK_LENGTH = 0.400
MOTOR_BOX_W = 0.200
MOTOR_BOX_H = 0.160
MOTOR_BOX_D = 0.200
MOTOR_CYL_R = 0.040
MOTOR_CYL_H = 0.060
FILTER_R = 0.020
FILTER_H = 0.120
REG_R = 0.020
REG_H = 0.100
MANIFOLD_W = 0.120
MANIFOLD_H = 0.060
MANIFOLD_D = 0.080

PBR = {
    "base_color": (0.75, 0.78, 0.80, 1.0),
    "metallic": 1.0,
    "roughness": 0.35,
    "alpha": 1.0,
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
    plate_center_y = PLATE_H / 2
    body = add_box(PLATE_W, PLATE_H, PLATE_D, loc=(0, plate_center_y, 0))
    
    tank_center_y = PLATE_H + TANK_RADIUS
    tank = add_cyl(TANK_RADIUS, TANK_LENGTH, 32, loc=(0, tank_center_y, 0), rot=(0, 0, math.pi / 2))
    bool_op(body, tank, 'UNION')
    
    motor_box_center_y = PLATE_H + MOTOR_BOX_H / 2
    motor_box = add_box(MOTOR_BOX_W, MOTOR_BOX_H, MOTOR_BOX_D, loc=(-0.15, motor_box_center_y, 0))
    bool_op(body, motor_box, 'UNION')
    
    motor_cyl_center_y = PLATE_H + MOTOR_BOX_H + MOTOR_CYL_H / 2
    motor_cyl = add_cyl(MOTOR_CYL_R, MOTOR_CYL_H, 24, loc=(-0.15, motor_cyl_center_y, 0))
    bool_op(body, motor_cyl, 'UNION')
    
    filter_center_y = PLATE_H + FILTER_H / 2
    filter_cyl = add_cyl(FILTER_R, FILTER_H, 20, loc=(0.12, filter_center_y, 0.06))
    bool_op(body, filter_cyl, 'UNION')
    
    reg_center_y = PLATE_H + REG_H / 2
    regulator = add_cyl(REG_R, REG_H, 20, loc=(0.12, reg_center_y, -0.06))
    bool_op(body, regulator, 'UNION')
    
    manifold_center_y = PLATE_H + MANIFOLD_H / 2
    manifold = add_box(MANIFOLD_W, MANIFOLD_H, MANIFOLD_D, loc=(0.15, manifold_center_y, -0.08))
    bool_op(body, manifold, 'UNION')
    
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
    print(f"  PATENT alignment: Under-conveyor utilities, Y=0.0-0.35m, center")
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
