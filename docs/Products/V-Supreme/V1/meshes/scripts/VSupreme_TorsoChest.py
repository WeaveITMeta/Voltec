"""
Blender Headless Mesh Generator
Product: VSupreme  |  Component: TorsoChest
Run: blender --background --python this_script.py

Front torso chest plate — compound-curve armor shell with reactor cavity,
VOLTEC branding boss, shoulder mount flanges, and ventilation slots.
Multi-layer armor: 2.5mm Ti + 5mm Al2O3 + 3mm UHMWPE + 2mm CFRP + 1.5mm Ti = 14mm total
Patent ref: US20170319421A1 (exoskeleton torso structure)
"""
import bpy, bmesh, math, os

PRODUCT = "VSupreme"
COMPONENT = "TorsoChest"
MATERIAL = "Ti6Al4V"
OUT_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT_FILE = f"{PRODUCT}_{COMPONENT}.glb"

# Chest plate: 500mm wide × 550mm tall × 180mm deep (front half of torso)
WIDTH = 0.500
HEIGHT = 0.550
DEPTH = 0.180
WALL = 0.014   # 14mm composite armor stack
SHOULDER_BOSS_R = 0.025
SHOULDER_BOSS_H = 0.015

PBR = {
    "base_color": (1.0, 1.0, 1.0, 1.0),
    "metallic": 0.0,
    "roughness": 0.3,
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
    # Main chest plate — rounded box shape
    # Start with a cube, then use subdivision + cast to sphere for compound curve
    chest = add_cube(WIDTH/2, HEIGHT/2, DEPTH/2)

    # Add slight convexity with a cast modifier toward sphere
    cast = chest.modifiers.new("Curve", 'CAST')
    cast.cast_type = 'SPHERE'
    cast.factor = 0.15
    bpy.context.view_layer.objects.active = chest
    bpy.ops.object.modifier_apply(modifier="Curve")

    # Subdivide for smoother form
    sub = chest.modifiers.new("Sub", 'SUBSURF')
    sub.levels = 2
    sub.render_levels = 2
    bpy.ops.object.modifier_apply(modifier="Sub")

    # Hollow out — solidify
    sol = chest.modifiers.new("Shell", 'SOLIDIFY')
    sol.thickness = WALL
    sol.offset = -1
    bpy.ops.object.modifier_apply(modifier="Shell")

    # Cut the back face flat — remove everything behind Z < -0.01
    back_cut = add_cube(0.6, 0.7, DEPTH, loc=(0, 0, -DEPTH/2 - 0.005))
    bool_op(chest, back_cut, 'DIFFERENCE')

    # Shoulder mount bosses — cylindrical protrusions at top corners
    for side in [-1, 1]:
        boss = add_cyl(SHOULDER_BOSS_R, SHOULDER_BOSS_H, 32,
                       loc=(side * WIDTH/2 * 0.8, HEIGHT/2 * 0.7, 0.02),
                       rot=(math.radians(90), 0, 0))
        bool_op(chest, boss, 'UNION')

    # Center reactor access port — circular hole in inner face
    port = add_cyl(0.06, WALL + 0.02, 32, loc=(0, 0.05, -0.01),
                   rot=(math.radians(90), 0, 0))
    bool_op(chest, port, 'DIFFERENCE')

    # Ventilation slots — 3 horizontal slots across lower chest
    for i in range(3):
        y_pos = -HEIGHT/2 * 0.3 + i * 0.03
        slot = add_cube(WIDTH/2 * 0.4, 0.003, WALL + 0.01,
                        loc=(0, y_pos, DEPTH/2 * 0.5))
        bool_op(chest, slot, 'DIFFERENCE')

    # Branding boss — raised rectangular pad in center chest
    brand = add_cube(0.08, 0.02, 0.003,
                     loc=(0, 0.08, DEPTH/2 * 0.85))
    bool_op(chest, brand, 'UNION')

    # Neck opening — cut top center
    neck_cut = add_cyl(0.08, 0.05, 32, loc=(0, HEIGHT/2 * 0.85, 0))
    bool_op(chest, neck_cut, 'DIFFERENCE')

    chest.name = f"{PRODUCT}_{COMPONENT}"
    chest.data.name = f"{PRODUCT}_{COMPONENT}_mesh"
    return chest

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
