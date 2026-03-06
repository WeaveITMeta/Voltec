"""
Blender Headless Mesh Generator
Product: V-Core  |  Component: HeatPipeBundle
Material: Inconel 718 — 12 sodium heat pipes, vertical through fuel
Run: blender --background --python this_script.py
"""
import bpy, bmesh, math, os

PRODUCT = "VCore"
COMPONENT = "HeatPipeBundle"
MATERIAL = "Inconel718"
OUT_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT_FILE = f"{PRODUCT}_{COMPONENT}.glb"

PIPE_OD = 0.0159 / 2.0  # 15.9mm OD -> radius
PIPE_WALL = 0.0015
PIPE_TOTAL_H = 0.680  # evaporator 380 + adiabatic 100 + condenser 200
PIPE_ORBIT_R = 0.060  # pipes arranged on a circle inside fuel
PIPE_COUNT = 12

PBR = {
    "base_color": (0.65, 0.65, 0.60, 1.0),  # Nickel alloy
    "metallic": 1.0,
    "roughness": 0.30,
    "alpha": 1.0,
    "emission": (0.0, 0.0, 0.0, 1.0),
    "emission_strength": 0.0,
}
BEVEL_WIDTH = 0.0003
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
    # First pipe
    x0 = PIPE_ORBIT_R
    z0 = 0.0
    bpy.ops.mesh.primitive_cylinder_add(vertices=16, radius=PIPE_OD, depth=PIPE_TOTAL_H,
                                         location=(x0, 0, z0))
    bundle = bpy.context.active_object

    # Remaining 11 pipes
    for i in range(1, PIPE_COUNT):
        angle = math.radians(i * 360.0 / PIPE_COUNT)
        x = PIPE_ORBIT_R * math.cos(angle)
        z = PIPE_ORBIT_R * math.sin(angle)
        bpy.ops.mesh.primitive_cylinder_add(vertices=16, radius=PIPE_OD, depth=PIPE_TOTAL_H,
                                             location=(x, 0, z))
        pipe = bpy.context.active_object
        bool_op(bundle, pipe, 'UNION')

    # Upper manifold ring connecting all pipe tops
    bpy.ops.mesh.primitive_cylinder_add(vertices=48, radius=PIPE_ORBIT_R + 0.015, depth=0.010,
                                         location=(0, PIPE_TOTAL_H / 2.0 + 0.005, 0))
    manifold_top = bpy.context.active_object
    # Hollow it
    sol = manifold_top.modifiers.new("Shell", 'SOLIDIFY')
    sol.thickness = 0.015
    sol.offset = -1
    bpy.context.view_layer.objects.active = manifold_top
    bpy.ops.object.modifier_apply(modifier="Shell")
    bool_op(bundle, manifold_top, 'UNION')

    # Lower manifold ring
    bpy.ops.mesh.primitive_cylinder_add(vertices=48, radius=PIPE_ORBIT_R + 0.015, depth=0.010,
                                         location=(0, -PIPE_TOTAL_H / 2.0 - 0.005, 0))
    manifold_bot = bpy.context.active_object
    sol2 = manifold_bot.modifiers.new("Shell", 'SOLIDIFY')
    sol2.thickness = 0.015
    sol2.offset = -1
    bpy.context.view_layer.objects.active = manifold_bot
    bpy.ops.object.modifier_apply(modifier="Shell")
    bool_op(bundle, manifold_bot, 'UNION')

    bundle.name = f"{PRODUCT}_{COMPONENT}"
    bundle.data.name = f"{PRODUCT}_{COMPONENT}_mesh"
    return bundle

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
