"""
Blender Headless Mesh Generator
Product: V-Core  |  Component: ReactorVessel
Material: 316L Stainless Steel — cylindrical pressure boundary with flanged head
Run: blender --background --python this_script.py
"""
import bpy, bmesh, math, os

PRODUCT = "VCore"
COMPONENT = "ReactorVessel"
MATERIAL = "316LSS"
OUT_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT_FILE = f"{PRODUCT}_{COMPONENT}.glb"

# Cylindrical vessel: Ø300mm × 500mm tall, 8mm wall
OUTER_R = 0.150
HEIGHT = 0.500
WALL = 0.008
FLANGE_R = 0.175
FLANGE_H = 0.015

PBR = {
    "base_color": (0.60, 0.61, 0.63, 1.0),
    "metallic": 1.0,
    "roughness": 0.30,
    "alpha": 1.0,
    "emission": (0.0, 0.0, 0.0, 1.0),
    "emission_strength": 0.0,
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

def bool_op(target, cutter, op='UNION'):
    mod = target.modifiers.new(op, 'BOOLEAN')
    mod.operation = op
    mod.object = cutter
    mod.solver = 'EXACT'
    bpy.context.view_layer.objects.active = target
    bpy.ops.object.modifier_apply(modifier=op)
    bpy.data.objects.remove(cutter, do_unlink=True)

def create_geometry():
    # Main cylindrical vessel body
    bpy.ops.mesh.primitive_cylinder_add(vertices=48, radius=OUTER_R, depth=HEIGHT, location=(0, 0, 0))
    vessel = bpy.context.active_object

    # Hollow it out
    sol = vessel.modifiers.new("Shell", 'SOLIDIFY')
    sol.thickness = WALL
    sol.offset = -1
    bpy.context.view_layer.objects.active = vessel
    bpy.ops.object.modifier_apply(modifier="Shell")

    # Top flange ring
    bpy.ops.mesh.primitive_cylinder_add(vertices=48, radius=FLANGE_R, depth=FLANGE_H,
                                         location=(0, HEIGHT/2.0 + FLANGE_H/2.0, 0))
    top_flange = bpy.context.active_object
    # Hollow the flange
    sf = top_flange.modifiers.new("Shell", 'SOLIDIFY')
    sf.thickness = FLANGE_R - OUTER_R
    sf.offset = -1
    bpy.context.view_layer.objects.active = top_flange
    bpy.ops.object.modifier_apply(modifier="Shell")
    bool_op(vessel, top_flange, 'UNION')

    # Bottom flange ring
    bpy.ops.mesh.primitive_cylinder_add(vertices=48, radius=FLANGE_R, depth=FLANGE_H,
                                         location=(0, -HEIGHT/2.0 - FLANGE_H/2.0, 0))
    bot_flange = bpy.context.active_object
    sf2 = bot_flange.modifiers.new("Shell", 'SOLIDIFY')
    sf2.thickness = FLANGE_R - OUTER_R
    sf2.offset = -1
    bpy.context.view_layer.objects.active = bot_flange
    bpy.ops.object.modifier_apply(modifier="Shell")
    bool_op(vessel, bot_flange, 'UNION')

    # Domed head (top) — hemisphere cap
    bpy.ops.mesh.primitive_uv_sphere_add(segments=32, ring_count=16, radius=OUTER_R,
                                          location=(0, HEIGHT/2.0 + FLANGE_H, 0))
    dome = bpy.context.active_object
    # Cut bottom half
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0, HEIGHT/2.0 + FLANGE_H - 0.25, 0))
    cutter = bpy.context.active_object
    cutter.scale = (0.5, 0.5, 0.5)
    bpy.ops.object.transform_apply(scale=True)
    bool_op(dome, cutter, 'DIFFERENCE')
    # Hollow dome
    sd = dome.modifiers.new("Shell", 'SOLIDIFY')
    sd.thickness = WALL
    sd.offset = -1
    bpy.context.view_layer.objects.active = dome
    bpy.ops.object.modifier_apply(modifier="Shell")
    bool_op(vessel, dome, 'UNION')

    # Heat pipe penetration stubs (12 small cylinders on top dome)
    for i in range(12):
        angle = math.radians(i * 30)
        x = 0.08 * math.cos(angle)
        z = 0.08 * math.sin(angle)
        bpy.ops.mesh.primitive_cylinder_add(vertices=16, radius=0.010, depth=0.030,
                                             location=(x, HEIGHT/2.0 + FLANGE_H + OUTER_R * 0.6, z))
        stub = bpy.context.active_object
        bool_op(vessel, stub, 'UNION')

    vessel.name = f"{PRODUCT}_{COMPONENT}"
    vessel.data.name = f"{PRODUCT}_{COMPONENT}_mesh"
    return vessel

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
    mat = create_material()
    obj = create_geometry()
    obj.data.materials.append(mat)
    polish(obj)
    verify(obj)
    export(obj)

if __name__ == "__main__":
    main()
