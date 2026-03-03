"""
Blender Headless Mesh Generator
Product: V-Man  |  Component: HMI
Run: blender --background --python this_script.py

Industrial touchscreen HMI panel.
PATENT reference: Section 9.4 — mounted on control cabinet.

Positioned at Y=1.0m (operator eye level).
"""
import bpy, bmesh, math, os

PRODUCT = "VMan"
COMPONENT = "HMI"
MATERIAL = "GorillaGlass_Al"
OUT_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT_FILE = f"{PRODUCT}_{COMPONENT}.glb"

SCREEN_W = 0.365
SCREEN_H = 0.228
BEZEL = 0.012
DEPTH = 0.035
GLASS_T = 0.002
BODY_W = SCREEN_W + 2 * BEZEL
BODY_H = SCREEN_H + 2 * BEZEL
GASKET_EXTRA = 0.002
GASKET_T = 0.004
VESA_SPACING = 0.100
STANDOFF_R = 0.006
STANDOFF_H = 0.015
VESA_PLATE_W = 0.120
VESA_PLATE_H = 0.120
VESA_PLATE_T = 0.004
CABLE_R = 0.008
CABLE_H = 0.020
LED_R = 0.003
LED_H = 0.003

PBR = {
    "base_color": (0.04, 0.04, 0.04, 1.0),
    "metallic": 0.0,
    "roughness": 0.1,
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
    body = add_box(BODY_W, BODY_H, DEPTH, loc=(0, 0, 0))
    
    glass_center_z = DEPTH / 2 + GLASS_T / 2
    glass = add_box(SCREEN_W, SCREEN_H, GLASS_T, loc=(0, 0, glass_center_z))
    bool_op(body, glass, 'UNION')
    
    rim_outer_w = BODY_W + 2 * GASKET_EXTRA
    rim_outer_h = BODY_H + 2 * GASKET_EXTRA
    rim_center_z = DEPTH / 2 + GASKET_T / 2
    rim_outer = add_box(rim_outer_w, rim_outer_h, GASKET_T, loc=(0, 0, rim_center_z))
    rim_inner = add_box(SCREEN_W + 0.002, SCREEN_H + 0.002, GASKET_T + 0.004, loc=(0, 0, rim_center_z))
    bool_op(rim_outer, rim_inner, 'DIFFERENCE')
    bool_op(body, rim_outer, 'UNION')
    
    for x_sign in (-1, 1):
        for y_sign in (-1, 1):
            so_x = x_sign * VESA_SPACING / 2
            so_y = y_sign * VESA_SPACING / 2
            so_front_z = -DEPTH / 2
            so_center_z = so_front_z - STANDOFF_H / 2
            standoff = add_cyl(STANDOFF_R, STANDOFF_H, 12, loc=(so_x, so_y, so_center_z), rot=(math.pi / 2, 0, 0))
            bool_op(body, standoff, 'UNION')
    
    plate_front_z = -DEPTH / 2 - STANDOFF_H
    plate_center_z = plate_front_z - VESA_PLATE_T / 2
    vesa_plate = add_box(VESA_PLATE_W, VESA_PLATE_H, VESA_PLATE_T, loc=(0, 0, plate_center_z))
    bool_op(body, vesa_plate, 'UNION')
    
    cable_top_y = -BODY_H / 2
    cable_center_y = cable_top_y - CABLE_H / 2
    cable_center_z = -DEPTH / 4
    cable = add_cyl(CABLE_R, CABLE_H, 12, loc=(0, cable_center_y, cable_center_z))
    bool_op(body, cable, 'UNION')
    
    led_x = BODY_W / 2 - BEZEL - 0.010
    led_y = BODY_H / 2 - BEZEL - 0.010
    led_back_z = DEPTH / 2 + GLASS_T / 2
    led_center_z = led_back_z + LED_H / 2
    led = add_cyl(LED_R, LED_H, 10, loc=(led_x, led_y, led_center_z), rot=(math.pi / 2, 0, 0))
    bool_op(body, led, 'UNION')
    
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
    print(f"  PATENT alignment: HMI panel, Y=1.0m, operator eye level")
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
