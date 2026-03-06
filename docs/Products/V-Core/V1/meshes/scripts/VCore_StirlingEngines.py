"""
Blender Headless Mesh Generator
Product: V-Core  |  Component: StirlingEngines
Material: Maraging 350 Steel — 2 × free-piston Stirling engines, balanced opposed
Run: blender --background --python this_script.py
"""
import bpy, bmesh, math, os

PRODUCT = "VCore"
COMPONENT = "StirlingEngines"
MATERIAL = "Maraging350"
OUT_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT_FILE = f"{PRODUCT}_{COMPONENT}.glb"

# Each engine: Ø200mm × 450mm long, mounted side by side
ENGINE_R = 0.100
ENGINE_H = 0.450
SPACING = 0.220  # center-to-center

PBR = {
    "base_color": (0.50, 0.50, 0.52, 1.0),  # Steel grey
    "metallic": 1.0,
    "roughness": 0.35,
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
    # Engine 1 — left
    bpy.ops.mesh.primitive_cylinder_add(vertices=32, radius=ENGINE_R, depth=ENGINE_H,
                                         location=(-SPACING/2.0, 0, 0))
    engines = bpy.context.active_object

    # Engine 2 — right
    bpy.ops.mesh.primitive_cylinder_add(vertices=32, radius=ENGINE_R, depth=ENGINE_H,
                                         location=(SPACING/2.0, 0, 0))
    e2 = bpy.context.active_object
    bool_op(engines, e2, 'UNION')

    # Connecting bridge between engines (structural crossbeam)
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0, 0, 0))
    bridge = bpy.context.active_object
    bridge.scale = (SPACING/2.0, 0.030, 0.050)
    bpy.ops.object.transform_apply(scale=True)
    bool_op(engines, bridge, 'UNION')

    # Bottom flange ring on each engine (hot-side interface)
    for x_off in [-SPACING/2.0, SPACING/2.0]:
        bpy.ops.mesh.primitive_cylinder_add(vertices=32, radius=ENGINE_R + 0.015, depth=0.012,
                                             location=(x_off, -ENGINE_H/2.0 - 0.006, 0))
        flange = bpy.context.active_object
        bool_op(engines, flange, 'UNION')

    # Top flange ring (cold-side interface)
    for x_off in [-SPACING/2.0, SPACING/2.0]:
        bpy.ops.mesh.primitive_cylinder_add(vertices=32, radius=ENGINE_R + 0.015, depth=0.012,
                                             location=(x_off, ENGINE_H/2.0 + 0.006, 0))
        flange = bpy.context.active_object
        bool_op(engines, flange, 'UNION')

    # Electrical connector stubs on top
    for x_off in [-SPACING/2.0, SPACING/2.0]:
        bpy.ops.mesh.primitive_cylinder_add(vertices=12, radius=0.015, depth=0.030,
                                             location=(x_off, ENGINE_H/2.0 + 0.027, 0))
        conn = bpy.context.active_object
        bool_op(engines, conn, 'UNION')

    engines.name = f"{PRODUCT}_{COMPONENT}"
    engines.data.name = f"{PRODUCT}_{COMPONENT}_mesh"
    return engines

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
