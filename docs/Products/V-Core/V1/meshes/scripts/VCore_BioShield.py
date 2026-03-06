"""
Blender Headless Mesh Generator
Product: V-Core  |  Component: BioShield
Material: Lead-Polyethylene-Boron composite — graded biological shield
Run: blender --background --python this_script.py
"""
import bpy, bmesh, math, os

PRODUCT = "VCore"
COMPONENT = "BioShield"
MATERIAL = "LeadPEBoron"
OUT_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT_FILE = f"{PRODUCT}_{COMPONENT}.glb"

# Cylindrical shield: inner Ø310mm (just outside vessel), outer Ø610mm, height 550mm
INNER_R = 0.155
OUTER_R = 0.305  # 150mm total radial thickness
HEIGHT = 0.550

PBR = {
    "base_color": (0.35, 0.35, 0.38, 1.0),  # Dark lead grey
    "metallic": 0.8,
    "roughness": 0.60,
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
    # Outer cylinder
    bpy.ops.mesh.primitive_cylinder_add(vertices=48, radius=OUTER_R, depth=HEIGHT, location=(0, 0, 0))
    shield = bpy.context.active_object

    # Cut inner bore
    bpy.ops.mesh.primitive_cylinder_add(vertices=48, radius=INNER_R, depth=HEIGHT + 0.01, location=(0, 0, 0))
    bore = bpy.context.active_object
    bool_op(shield, bore, 'DIFFERENCE')

    # Top cap (solid disk with center hole for heat pipe passage)
    bpy.ops.mesh.primitive_cylinder_add(vertices=48, radius=OUTER_R, depth=0.030,
                                         location=(0, HEIGHT/2.0 + 0.015, 0))
    top_cap = bpy.context.active_object
    bpy.ops.mesh.primitive_cylinder_add(vertices=48, radius=0.100, depth=0.031,
                                         location=(0, HEIGHT/2.0 + 0.015, 0))
    hole = bpy.context.active_object
    bool_op(top_cap, hole, 'DIFFERENCE')
    bool_op(shield, top_cap, 'UNION')

    # Bottom cap (solid)
    bpy.ops.mesh.primitive_cylinder_add(vertices=48, radius=OUTER_R, depth=0.030,
                                         location=(0, -HEIGHT/2.0 - 0.015, 0))
    bot_cap = bpy.context.active_object
    bool_op(shield, bot_cap, 'UNION')

    shield.name = f"{PRODUCT}_{COMPONENT}"
    shield.data.name = f"{PRODUCT}_{COMPONENT}_mesh"
    return shield

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
