"""
Blender Headless Mesh Generator
Product: V-Man  |  Component: SensorSuite
Run: blender --background --python this_script.py

Distributed sensor array (vibration, temperature, proximity, F/T).
PATENT reference: Section 8.3 — mounted on chassis interior.

Positioned at Y=1.0m (above utilities, within arm reach).
"""
import bpy, bmesh, math, os

PRODUCT = "VMan"
COMPONENT = "SensorSuite"
MATERIAL = "Al6061T6"
OUT_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT_FILE = f"{PRODUCT}_{COMPONENT}.glb"

JB_W = 0.240
JB_H = 0.160
JB_D = 0.120
GLAND_R = 0.006
GLAND_H = 0.020
GLAND_COUNT = 4
STALK_R = 0.004
STALK_LENGTH = 0.120
POD_R = 0.012
POD_H = 0.020
VIB_Y_OFFSET = 0.0
VIB_Z_OFFSETS = [0.060, -0.060]
VIB_X_SIGNS = [-1, 1]
PROX_R = 0.015
PROX_H = 0.010
PROX_X_SPACING = 0.100
TRUNK_W = 0.030
TRUNK_H = 0.030
TRUNK_D = 0.500

PBR = {
    "base_color": (0.04, 0.04, 0.04, 1.0),
    "metallic": 0.0,
    "roughness": 0.5,
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
    body = add_box(JB_W, JB_H, JB_D, loc=(0, 0, 0))
    
    gland_spacing = JB_W / (GLAND_COUNT + 1)
    for i in range(GLAND_COUNT):
        gx = -JB_W / 2 + (i + 1) * gland_spacing
        gland = add_cyl(GLAND_R, GLAND_H, 12, loc=(gx, -JB_H / 2 - GLAND_H / 2, 0))
        bool_op(body, gland, 'UNION')
    
    for x_sign in VIB_X_SIGNS:
        jb_face_x = x_sign * JB_W / 2
        stalk_end_x = jb_face_x + x_sign * STALK_LENGTH
        stalk_center_x = (jb_face_x + stalk_end_x) / 2.0
        
        for z_off in VIB_Z_OFFSETS:
            stalk = add_cyl(STALK_R, STALK_LENGTH, 10, loc=(stalk_center_x, 0, z_off), rot=(0, 0, math.pi / 2))
            bool_op(body, stalk, 'UNION')
            
            pod = add_cyl(POD_R, POD_H, 16, loc=(stalk_end_x, 0, z_off))
            bool_op(body, pod, 'UNION')
    
    for x_off in (-PROX_X_SPACING / 2, PROX_X_SPACING / 2):
        disc = add_cyl(PROX_R, PROX_H, 16, loc=(x_off, JB_H / 2 + PROX_H / 2, 0))
        bool_op(body, disc, 'UNION')
    
    trunk = add_box(TRUNK_W, TRUNK_H, TRUNK_D, loc=(0, JB_H / 2 + TRUNK_H / 2, 0))
    bool_op(body, trunk, 'UNION')
    
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
    print(f"  PATENT alignment: Sensor suite, Y=1.0m, interior mounted")
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
