"""
Blender Headless Mesh Generator
Product: V-Man  |  Component: VisionSystem
Run: blender --background --python this_script.py

Overhead vision array (LIDAR + RGB-D + structured light).
PATENT reference: Section 8.2 — mounted overhead on cable tray.

Positioned above conveyor at Y=1.25m (above sensor brackets).
"""
import bpy, bmesh, math, os

PRODUCT = "VMan"
COMPONENT = "VisionSystem"
MATERIAL = "Al6061T6"
OUT_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT_FILE = f"{PRODUCT}_{COMPONENT}.glb"

PLATE_W = 0.400
PLATE_H = 0.060
PLATE_D = 0.240
BRACKET_ARM_W = 0.030
BRACKET_ARM_H = 0.080
BRACKET_ARM_D = 0.200
BRACKET_TOP_H = 0.016
LIDAR_RADIUS = 0.040
LIDAR_BODY_H = 0.060
LIDAR_DOME_R = 0.040
CAM_W = 0.070
CAM_H = 0.050
CAM_D = 0.080
CAM_LENS_R = 0.012
CAM_LENS_H = 0.010
CAM_X_OFFSET = 0.120
SL_W = 0.320
SL_H = 0.024
SL_D = 0.030
CONDUIT_R = 0.012
CONDUIT_H = 0.050

PBR = {
    "base_color": (0.04, 0.04, 0.04, 1.0),
    "metallic": 0.0,
    "roughness": 0.5,
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

def add_cyl(radius, depth, vertices=32, loc=(0, 0, 0), rot=(0, 0, 0)):
    bpy.ops.mesh.primitive_cylinder_add(vertices=vertices, radius=radius, depth=depth, location=loc, rotation=rot)
    return bpy.context.active_object

def add_sphere(radius, loc=(0, 0, 0)):
    bpy.ops.mesh.primitive_uv_sphere_add(segments=24, ring_count=12, radius=radius, location=loc)
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
    
    bracket_arm_center_y = PLATE_H + BRACKET_ARM_H / 2
    bracket_l = add_box(BRACKET_ARM_W, BRACKET_ARM_H, BRACKET_ARM_D, loc=(-PLATE_W / 2 + BRACKET_ARM_W / 2, bracket_arm_center_y, 0))
    bool_op(body, bracket_l, 'UNION')
    
    bracket_r = add_box(BRACKET_ARM_W, BRACKET_ARM_H, BRACKET_ARM_D, loc=(PLATE_W / 2 - BRACKET_ARM_W / 2, bracket_arm_center_y, 0))
    bool_op(body, bracket_r, 'UNION')
    
    bracket_top_center_y = PLATE_H + BRACKET_ARM_H + BRACKET_TOP_H / 2
    bracket_top = add_box(PLATE_W, BRACKET_TOP_H, BRACKET_ARM_D, loc=(0, bracket_top_center_y, 0))
    bool_op(body, bracket_top, 'UNION')
    
    lidar_center_y = PLATE_H - LIDAR_BODY_H / 2
    lidar = add_cyl(LIDAR_RADIUS, LIDAR_BODY_H, 32, loc=(0, lidar_center_y, 0))
    bool_op(body, lidar, 'UNION')
    
    lidar_bottom_y = PLATE_H - LIDAR_BODY_H
    dome = add_sphere(LIDAR_DOME_R, loc=(0, lidar_bottom_y, 0))
    dome_cutter = add_box(LIDAR_DOME_R * 3, LIDAR_DOME_R * 2, LIDAR_DOME_R * 3, loc=(0, lidar_bottom_y + LIDAR_DOME_R, 0))
    bool_op(dome, dome_cutter, 'DIFFERENCE')
    bool_op(body, dome, 'UNION')
    
    cam_center_y = PLATE_H - CAM_H / 2
    cam_l = add_box(CAM_W, CAM_H, CAM_D, loc=(-CAM_X_OFFSET, cam_center_y, 0))
    bool_op(body, cam_l, 'UNION')
    
    lens_l_center_y = PLATE_H - CAM_H - CAM_LENS_H / 2
    lens_l = add_cyl(CAM_LENS_R, CAM_LENS_H, 16, loc=(-CAM_X_OFFSET, lens_l_center_y, 0))
    bool_op(body, lens_l, 'UNION')
    
    cam_r = add_box(CAM_W, CAM_H, CAM_D, loc=(CAM_X_OFFSET, cam_center_y, 0))
    bool_op(body, cam_r, 'UNION')
    
    lens_r = add_cyl(CAM_LENS_R, CAM_LENS_H, 16, loc=(CAM_X_OFFSET, lens_l_center_y, 0))
    bool_op(body, lens_r, 'UNION')
    
    sl_center_y = PLATE_H - SL_H / 2
    sl_center_z = PLATE_D / 2 - SL_D / 2
    sl_bar = add_box(SL_W, SL_H, SL_D, loc=(0, sl_center_y, sl_center_z))
    bool_op(body, sl_bar, 'UNION')
    
    conduit_center_y = PLATE_H + BRACKET_ARM_H + BRACKET_TOP_H + CONDUIT_H / 2
    conduit = add_cyl(CONDUIT_R, CONDUIT_H, 16, loc=(0, conduit_center_y, 0))
    bool_op(body, conduit, 'UNION')
    
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
    print(f"  PATENT alignment: Overhead vision array, mounted on cable tray")
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
