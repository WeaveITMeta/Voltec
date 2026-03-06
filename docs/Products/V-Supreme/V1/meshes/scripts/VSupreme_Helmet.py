"""
Blender Headless Mesh Generator
Product: VSupreme  |  Component: Helmet
Run: blender --background --python this_script.py

Mecha helmet with compound-curve visor slot, chin guard, neck ring,
ventilation channels, and sensor dome on forehead.
Patent ref: US20080009771A1 (upper body exoskeleton wearable structure)
"""
import bpy, bmesh, math, os

PRODUCT = "VSupreme"
COMPONENT = "Helmet"
MATERIAL = "Ti6Al4V"
OUT_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT_FILE = f"{PRODUCT}_{COMPONENT}.glb"

# Helmet outer shell: oblate sphere ~280mm wide × 300mm tall × 280mm deep
OUTER_RX = 0.140   # half-width
OUTER_RY = 0.150   # half-height
OUTER_RZ = 0.140   # half-depth
WALL = 0.0025       # 2.5mm Ti shell
VISOR_WIDTH = 0.20
VISOR_HEIGHT = 0.08
VISOR_DEPTH = 0.04
NECK_RING_R = 0.12
NECK_RING_H = 0.025
NECK_RING_WALL = 0.005

PBR = {
    "base_color": (1.0, 1.0, 1.0, 1.0),       # Voltec White
    "metallic": 0.0,
    "roughness": 0.3,
    "alpha": 1.0,
    "emission": (0.0, 0.0, 0.0, 1.0),
    "emission_strength": 0.0,
}

PBR_VISOR = {
    "base_color": (0.0, 0.75, 1.0, 0.6),      # Xenon blue, translucent
    "metallic": 0.0,
    "roughness": 0.05,
    "alpha": 0.6,
    "emission": (0.0, 0.75, 1.0, 1.0),
    "emission_strength": 2.0,
}

BEVEL_WIDTH = 0.0005
BEVEL_SEGMENTS = 2

def clean_scene():
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete(use_global=False)
    for block in bpy.data.meshes:
        if block.users == 0: bpy.data.meshes.remove(block)
    for block in bpy.data.materials:
        if block.users == 0: bpy.data.materials.remove(block)

def setup_scene():
    bpy.context.scene.name = "Scene0"
    bpy.context.scene.unit_settings.system = 'METRIC'
    bpy.context.scene.unit_settings.scale_length = 1.0

def create_material(name, pbr):
    mat = bpy.data.materials.new(name=name)
    mat.use_nodes = True
    mat.use_backface_culling = True
    nodes = mat.node_tree.nodes
    links = mat.node_tree.links
    nodes.clear()
    bsdf = nodes.new('ShaderNodeBsdfPrincipled')
    bsdf.inputs['Base Color'].default_value = pbr["base_color"]
    bsdf.inputs['Metallic'].default_value = pbr["metallic"]
    bsdf.inputs['Roughness'].default_value = pbr["roughness"]
    bsdf.inputs['Alpha'].default_value = pbr["alpha"]
    bsdf.inputs['Emission Color'].default_value = pbr["emission"]
    bsdf.inputs['Emission Strength'].default_value = pbr["emission_strength"]
    output = nodes.new('ShaderNodeOutputMaterial')
    output.location = (300, 0)
    links.new(bsdf.outputs['BSDF'], output.inputs['Surface'])
    if pbr["alpha"] < 1.0:
        mat.blend_method = 'BLEND'
    return mat

def add_cyl(r, d, v=48, loc=(0,0,0), rot=(0,0,0)):
    bpy.ops.mesh.primitive_cylinder_add(vertices=v, radius=r, depth=d,
                                        location=loc, rotation=rot)
    return bpy.context.active_object

def add_cube(sx, sy, sz, loc=(0,0,0)):
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=loc)
    obj = bpy.context.active_object
    obj.scale = (sx, sy, sz)
    bpy.ops.object.transform_apply(scale=True)
    return obj

def bool_op(target, cutter, op='UNION'):
    mod = target.modifiers.new(op, 'BOOLEAN')
    mod.operation = op
    mod.object = cutter
    mod.solver = 'EXACT'
    bpy.context.view_layer.objects.active = target
    bpy.ops.object.modifier_apply(modifier=op)
    bpy.data.objects.remove(cutter, do_unlink=True)

def create_geometry():
    # Main helmet shell — UV sphere, squashed slightly for oblate shape
    bpy.ops.mesh.primitive_uv_sphere_add(segments=48, ring_count=24, radius=1.0,
                                          location=(0, 0, 0))
    helmet = bpy.context.active_object
    helmet.scale = (OUTER_RX, OUTER_RY, OUTER_RZ)
    bpy.ops.object.transform_apply(scale=True)

    # Hollow it out with Solidify
    sol = helmet.modifiers.new("Shell", 'SOLIDIFY')
    sol.thickness = WALL
    sol.offset = -1
    bpy.context.view_layer.objects.active = helmet
    bpy.ops.object.modifier_apply(modifier="Shell")

    # Cut bottom flat for neck opening — cut everything below Y = -0.10
    cutter_bottom = add_cube(0.4, 0.15, 0.4, loc=(0, -0.175, 0))
    bool_op(helmet, cutter_bottom, 'DIFFERENCE')

    # Visor slot — rectangular cutout on front face
    visor_cut = add_cube(VISOR_WIDTH/2, VISOR_HEIGHT/2, VISOR_DEPTH,
                         loc=(0, 0.04, OUTER_RZ - 0.01))
    bool_op(helmet, visor_cut, 'DIFFERENCE')

    # Chin guard — small protruding wedge below visor
    chin = add_cube(0.08, 0.015, 0.04, loc=(0, -0.06, OUTER_RZ - 0.005))
    bool_op(helmet, chin, 'UNION')

    # Neck ring — cylinder at bottom
    neck_outer = add_cyl(NECK_RING_R, NECK_RING_H, 48, loc=(0, -0.10 - NECK_RING_H/2, 0))
    neck_inner = add_cyl(NECK_RING_R - NECK_RING_WALL, NECK_RING_H + 0.01, 48,
                         loc=(0, -0.10 - NECK_RING_H/2, 0))
    bool_op(neck_outer, neck_inner, 'DIFFERENCE')
    bool_op(helmet, neck_outer, 'UNION')

    # Forehead sensor dome — small half-sphere
    bpy.ops.mesh.primitive_uv_sphere_add(segments=24, ring_count=12, radius=0.015,
                                          location=(0, 0.10, OUTER_RZ - 0.01))
    sensor = bpy.context.active_object
    # Cut bottom half
    sensor_cut = add_cube(0.05, 0.05, 0.05, loc=(0, 0.10 - 0.025, OUTER_RZ - 0.01))
    bool_op(sensor, sensor_cut, 'DIFFERENCE')
    bool_op(helmet, sensor, 'UNION')

    # Side ventilation channels — small grooves on each side
    for side in [-1, 1]:
        vent = add_cube(0.005, 0.04, 0.015,
                        loc=(side * 0.13, 0.02, 0))
        bool_op(helmet, vent, 'DIFFERENCE')

    helmet.name = f"{PRODUCT}_{COMPONENT}"
    helmet.data.name = f"{PRODUCT}_{COMPONENT}_mesh"
    return helmet

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
    f = len(bm.faces)
    q = sum(1 for face in bm.faces if len(face.verts) == 4)
    nm = sum(1 for e in bm.edges if not e.is_manifold)
    print(f"\n  MESH: {obj.name}  |  V:{len(bm.verts)} E:{len(bm.edges)} F:{f}")
    print(f"  Quads: {q}/{f} ({100*q/max(f,1):.0f}%)  |  Non-manifold: {nm}  |  Watertight: {'YES' if nm==0 else 'FIX'}")
    bm.free()

def export(obj):
    os.makedirs(OUT_DIR, exist_ok=True)
    path = os.path.join(OUT_DIR, OUT_FILE)
    bpy.ops.object.select_all(action='DESELECT')
    obj.select_set(True)
    bpy.context.view_layer.objects.active = obj
    bpy.ops.export_scene.gltf(
        filepath=path, export_format='GLB', use_selection=True,
        export_apply=True, export_normals=True, export_materials='EXPORT',
        export_cameras=False, export_lights=False,
        export_animations=False, export_yup=True,
        export_draco_mesh_compression_enable=True,
        export_draco_mesh_compression_level=6,
    )
    print(f"  EXPORTED: {path} ({os.path.getsize(path)/1024:.1f} KB)\n")

def main():
    clean_scene()
    setup_scene()
    mat = create_material(f"MAT_{PRODUCT}_{MATERIAL}", PBR)
    obj = create_geometry()
    obj.data.materials.append(mat)
    polish(obj)
    verify(obj)
    export(obj)

if __name__ == "__main__":
    main()
