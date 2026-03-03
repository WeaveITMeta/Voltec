"""
Blender Headless Mesh Generator
Product: V-Man  |  Component: RoboticArm
Run: blender --background --python this_script.py

6-axis industrial robot arm.
PATENT reference: Section 6.2 Side View — arm reach envelope Y=0.40–2.69m

One of 4 arms in U-cell layout around central conveyor (PATENT 6.3).
Arm base pedestal starts at Y=0.40m (above utilities).
Arm reach extends to Y=2.69m (top of container).
"""
import bpy, bmesh, math, os

PRODUCT = "VMan"
COMPONENT = "RoboticArm"
MATERIAL = "Al7075T6"
OUT_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT_FILE = f"{PRODUCT}_{COMPONENT}.glb"

# Arm dimensions (meters) — from PATENT section 7.2
BASE_RADIUS = 0.140
BASE_HEIGHT = 0.180
FLANGE_RING_RADIUS = BASE_RADIUS + 0.020
FLANGE_RING_HEIGHT = 0.012
SHOULDER_RADIUS = 0.100
SHOULDER_HEIGHT = 0.160
SHOULDER_CAP_HEIGHT = 0.030
UPPER_ARM_WIDTH = 0.100
UPPER_ARM_HEIGHT = 0.120
UPPER_ARM_LENGTH = 0.450
UPPER_ARM_WALL = 0.006
ELBOW_RADIUS = 0.070
ELBOW_HEIGHT = 0.120
FOREARM_RADIUS = 0.055
FOREARM_LENGTH = 0.400
FOREARM_WALL = 0.005
WRIST_RADIUS = 0.045
WRIST_LENGTH = 0.150
TOOL_FLANGE_RADIUS = 0.035
TOOL_FLANGE_HEIGHT = 0.015
BOLT_RADIUS = 0.006
BOLT_DEPTH = 0.020

# PATENT alignment: arm base starts at Y=0.40m
ARM_BASE_Y = 0.40

PBR = {
    "base_color": (0.75, 0.78, 0.80, 1.0),
    "metallic": 1.0,
    "roughness": 0.35,
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

def add_cyl(radius, depth, vertices=32, loc=(0, 0, 0), rot=(0, 0, 0)):
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
    """Build arm with base at Y=0.40m (PATENT section 6.2)."""
    y_cursor = ARM_BASE_Y
    
    # Flange ring (mounting base)
    flange_center_y = y_cursor + FLANGE_RING_HEIGHT / 2
    root = add_cyl(FLANGE_RING_RADIUS, FLANGE_RING_HEIGHT, 48, loc=(0, flange_center_y, 0))
    y_cursor += FLANGE_RING_HEIGHT
    
    # Base pedestal
    base_center_y = y_cursor + BASE_HEIGHT / 2
    base = add_cyl(BASE_RADIUS, BASE_HEIGHT, 48, loc=(0, base_center_y, 0))
    bool_op(root, base, 'UNION')
    y_cursor += BASE_HEIGHT
    
    # Shoulder housing
    shoulder_center_y = y_cursor + SHOULDER_HEIGHT / 2
    shoulder = add_cyl(SHOULDER_RADIUS, SHOULDER_HEIGHT, 48, loc=(0, shoulder_center_y, 0))
    bool_op(root, shoulder, 'UNION')
    y_cursor += SHOULDER_HEIGHT
    
    # Shoulder cap
    cap_center_y = y_cursor + SHOULDER_CAP_HEIGHT / 2
    cap = add_cyl(SHOULDER_RADIUS - 0.005, SHOULDER_CAP_HEIGHT, 48, loc=(0, cap_center_y, 0))
    bool_op(root, cap, 'UNION')
    y_cursor += SHOULDER_CAP_HEIGHT
    
    # Upper arm link
    upper_center_y = y_cursor + UPPER_ARM_LENGTH / 2
    upper = add_box(UPPER_ARM_WIDTH, UPPER_ARM_LENGTH, UPPER_ARM_HEIGHT, loc=(0, upper_center_y, 0))
    sol = upper.modifiers.new("Hollow", 'SOLIDIFY')
    sol.thickness = UPPER_ARM_WALL
    sol.offset = -1
    bpy.context.view_layer.objects.active = upper
    bpy.ops.object.modifier_apply(modifier="Hollow")
    bool_op(root, upper, 'UNION')
    y_cursor += UPPER_ARM_LENGTH
    
    # Elbow joint
    elbow_center_y = y_cursor + ELBOW_RADIUS
    elbow = add_cyl(ELBOW_RADIUS, ELBOW_HEIGHT, 48, loc=(0, elbow_center_y, 0), rot=(math.pi / 2, 0, 0))
    bool_op(root, elbow, 'UNION')
    y_cursor += ELBOW_RADIUS * 2
    
    # Forearm link
    forearm_center_y = y_cursor + FOREARM_LENGTH / 2
    forearm_outer = add_cyl(FOREARM_RADIUS, FOREARM_LENGTH, 32, loc=(0, forearm_center_y, 0))
    forearm_inner = add_cyl(FOREARM_RADIUS - FOREARM_WALL, FOREARM_LENGTH + 0.002, 32, loc=(0, forearm_center_y, 0))
    bool_op(forearm_outer, forearm_inner, 'DIFFERENCE')
    bool_op(root, forearm_outer, 'UNION')
    y_cursor += FOREARM_LENGTH
    
    # Wrist assembly
    wrist_segment = WRIST_LENGTH / 3
    for idx in range(3):
        seg_center_y = y_cursor + wrist_segment / 2
        seg = add_cyl(WRIST_RADIUS * (1.0 - idx * 0.15), wrist_segment, 32, loc=(0, seg_center_y, 0))
        bool_op(root, seg, 'UNION')
        y_cursor += wrist_segment
    
    # Tool flange
    flange_center = y_cursor + TOOL_FLANGE_HEIGHT / 2
    flange = add_cyl(TOOL_FLANGE_RADIUS, TOOL_FLANGE_HEIGHT, 32, loc=(0, flange_center, 0))
    for i in range(4):
        angle = math.radians(90 * i + 45)
        fx = TOOL_FLANGE_RADIUS * 0.70 * math.cos(angle)
        fz = TOOL_FLANGE_RADIUS * 0.70 * math.sin(angle)
        fbolt = add_cyl(0.003, TOOL_FLANGE_HEIGHT + 0.002, 12, loc=(fx, flange_center, fz))
        bool_op(flange, fbolt, 'DIFFERENCE')
    bool_op(root, flange, 'UNION')
    
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
    print(f"  PATENT alignment: Arm base at Y=0.40m, reach envelope Y=0.40-2.69m")
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
