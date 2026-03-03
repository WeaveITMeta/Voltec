"""
Blender Headless Mesh Generator
Product: V-Man  |  Component: ControlCabinet
Run: blender --background --python this_script.py

Control cabinet (Rust CPU, GPU, EtherCAT master, safety PLC).
PATENT reference: Section 6.2 Side View — under-conveyor utilities at Y=0.0–0.40m

Positioned under conveyor, right side of container.
Bottom at Y=0.0 (floor), top at Y=0.35m.
"""
import bpy, bmesh, math, os

PRODUCT = "VMan"
COMPONENT = "ControlCabinet"
MATERIAL = "316L_SS"
OUT_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT_FILE = f"{PRODUCT}_{COMPONENT}.glb"

CAB_W = 0.600
CAB_H = 0.350
CAB_D = 0.500
WALL = 0.002
FOOT_W = 0.050
FOOT_H = 0.010
FOOT_D = 0.050
FOOT_INSET = 0.040
DOOR_INSET = 0.020
DOOR_THICK = 0.006
HANDLE_R = 0.006
HANDLE_LEN = 0.120
WINDOW_W = 0.200
WINDOW_H = 0.180
HINGE_R = 0.008
HINGE_LEN = 0.040

PBR = {
    "base_color": (0.55, 0.56, 0.58, 1.0),
    "metallic": 1.0,
    "roughness": 0.40,
    "alpha": 1.0,
    "emission": (0.0, 0.0, 0.0, 1.0),
    "emission_strength": 0.0,
}

BEVEL_WIDTH = 0.0015
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
    foot_center_y = FOOT_H / 2
    cab_center_y = FOOT_H + CAB_H / 2
    cab_min_x = 0.4
    cab_max_x = cab_min_x + CAB_W
    cab_min_z = -5.0
    cab_max_z = cab_min_z + CAB_D
    
    body = add_box(CAB_W, CAB_H, CAB_D, loc=((cab_min_x + cab_max_x) / 2, cab_center_y, (cab_min_z + cab_max_z) / 2))
    sol = body.modifiers.new("Hollow", 'SOLIDIFY')
    sol.thickness = WALL
    sol.offset = -1
    bpy.context.view_layer.objects.active = body
    bpy.ops.object.modifier_apply(modifier="Hollow")
    
    for x_sign in (-1, 1):
        for z_sign in (-1, 1):
            fx = cab_min_x + (FOOT_INSET if x_sign == -1 else CAB_W - FOOT_INSET)
            fz = cab_min_z + (FOOT_INSET if z_sign == -1 else CAB_D - FOOT_INSET)
            foot = add_box(FOOT_W, FOOT_H, FOOT_D, loc=(fx, foot_center_y, fz))
            bool_op(body, foot, 'UNION')
    
    door_w = CAB_W - 2 * DOOR_INSET
    door_h = CAB_H - 2 * DOOR_INSET
    door_center_y = cab_center_y
    door_center_z = cab_max_z + DOOR_THICK / 2
    door = add_box(door_w, door_h, DOOR_THICK, loc=((cab_min_x + cab_max_x) / 2, door_center_y, door_center_z))
    bool_op(body, door, 'UNION')
    
    handle_center_x = cab_max_x - DOOR_INSET - 0.040
    handle_center_z = door_center_z + DOOR_THICK / 2 + HANDLE_R
    handle = add_cyl(HANDLE_R, HANDLE_LEN, 16, loc=(handle_center_x, cab_center_y, handle_center_z))
    bool_op(body, handle, 'UNION')
    
    window_center_y = FOOT_H + CAB_H * 0.70
    window_center_z = door_center_z
    window = add_box(WINDOW_W, WINDOW_H, DOOR_THICK + 0.010, loc=((cab_min_x + cab_max_x) / 2, window_center_y, window_center_z))
    bool_op(body, window, 'DIFFERENCE')
    
    for y_fraction in (0.30, 0.70):
        hinge_y = FOOT_H + CAB_H * y_fraction
        hinge_x = cab_min_x + DOOR_INSET + 0.010
        hinge_z = door_center_z + DOOR_THICK / 2 + HINGE_R
        hinge = add_cyl(HINGE_R, HINGE_LEN, 12, loc=(hinge_x, hinge_y, hinge_z))
        bool_op(body, hinge, 'UNION')
    
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
    print(f"  PATENT alignment: Under-conveyor utilities, Y=0.0-0.35m, right side")
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
