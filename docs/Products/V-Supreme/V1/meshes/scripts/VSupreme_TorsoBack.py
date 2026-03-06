"""
Blender Headless Mesh Generator
Product: VSupreme  |  Component: TorsoBack
Run: blender --background --python this_script.py

Rear torso back plate — compound-curve armor shell with thruster mount points,
spine channel, dorsal radiator fins, and cooling port flanges.
"""
import bpy, bmesh, math, os

PRODUCT = "VSupreme"
COMPONENT = "TorsoBack"
MATERIAL = "Ti6Al4V"
OUT_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT_FILE = f"{PRODUCT}_{COMPONENT}.glb"

WIDTH = 0.500
HEIGHT = 0.550
DEPTH = 0.180
WALL = 0.014

PBR = {
    "base_color": (0.04, 0.04, 0.04, 1.0),  # Voltec Black
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
    return mat

def add_cyl(r, d, v=48, loc=(0,0,0), rot=(0,0,0)):
    bpy.ops.mesh.primitive_cylinder_add(vertices=v, radius=r, depth=d, location=loc, rotation=rot)
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
    # Main back plate — curved shell
    back = add_cube(WIDTH/2, HEIGHT/2, DEPTH/2)
    cast = back.modifiers.new("Curve", 'CAST')
    cast.cast_type = 'SPHERE'
    cast.factor = 0.15
    bpy.context.view_layer.objects.active = back
    bpy.ops.object.modifier_apply(modifier="Curve")

    sub = back.modifiers.new("Sub", 'SUBSURF')
    sub.levels = 2
    sub.render_levels = 2
    bpy.ops.object.modifier_apply(modifier="Sub")

    sol = back.modifiers.new("Shell", 'SOLIDIFY')
    sol.thickness = WALL
    sol.offset = -1
    bpy.ops.object.modifier_apply(modifier="Shell")

    # Cut front face flat
    front_cut = add_cube(0.6, 0.7, DEPTH, loc=(0, 0, DEPTH/2 + 0.005))
    bool_op(back, front_cut, 'DIFFERENCE')

    # Spine channel — groove down center of back
    spine_groove = add_cube(0.02, HEIGHT * 0.4, WALL + 0.01,
                            loc=(0, 0, -DEPTH/2 * 0.7))
    bool_op(back, spine_groove, 'DIFFERENCE')

    # Thruster mount points — 4 boss cylinders for Ion Thruster Pack
    mount_positions = [(-0.08, 0.10), (0.08, 0.10), (-0.08, -0.05), (0.08, -0.05)]
    for mx, my in mount_positions:
        boss = add_cyl(0.015, 0.012, 24, loc=(mx, my, -DEPTH/2 * 0.8))
        bool_op(back, boss, 'UNION')

    # Dorsal radiator fins — 5 thin horizontal fins
    for i in range(5):
        y_pos = -0.08 + i * 0.04
        fin = add_cube(WIDTH/2 * 0.6, 0.002, 0.015,
                       loc=(0, y_pos, -DEPTH/2 * 0.9))
        bool_op(back, fin, 'UNION')

    # Cooling port flanges — 2 circular ports
    for side in [-1, 1]:
        port_flange = add_cyl(0.02, 0.008, 24,
                              loc=(side * 0.15, -0.10, -DEPTH/2 * 0.5))
        port_hole = add_cyl(0.012, 0.02, 24,
                            loc=(side * 0.15, -0.10, -DEPTH/2 * 0.5))
        bool_op(port_flange, port_hole, 'DIFFERENCE')
        bool_op(back, port_flange, 'UNION')

    # Neck opening
    neck_cut = add_cyl(0.08, 0.05, 32, loc=(0, HEIGHT/2 * 0.85, 0))
    bool_op(back, neck_cut, 'DIFFERENCE')

    back.name = f"{PRODUCT}_{COMPONENT}"
    back.data.name = f"{PRODUCT}_{COMPONENT}_mesh"
    return back

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
