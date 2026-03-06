"""
Blender Headless Mesh Generator
Product: VSupreme  |  Component: VCellArray
Run: blender --background --python this_script.py

V-Cell Buffer Array — 6 prismatic Na-S solid-state battery modules arranged
3 per side in a rack tray with bus bars and cooling channels.
"""
import bpy, bmesh, math, os

PRODUCT = "VSupreme"
COMPONENT = "VCellArray"
MATERIAL = "NaS_SolidState"
OUT_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT_FILE = f"{PRODUCT}_{COMPONENT}.glb"

TRAY_W = 0.400
TRAY_H = 0.200
TRAY_D = 0.150
TRAY_WALL = 0.003
CELL_W = 0.120
CELL_H = 0.180
CELL_D = 0.060
CELL_GAP = 0.008
BUS_W = 0.380
BUS_H = 0.004
BUS_D = 0.010

PBR = {
    "base_color": (0.04, 0.04, 0.04, 1.0),
    "metallic": 0.0,
    "roughness": 0.5,
    "alpha": 1.0,
    "emission": (0.0, 0.0, 0.0, 1.0),
    "emission_strength": 0.0,
}

BEVEL_WIDTH = 0.0004
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
    # Outer tray — hollow box
    tray = add_cube(TRAY_W/2, TRAY_H/2, TRAY_D/2)
    sol = tray.modifiers.new("Shell", 'SOLIDIFY')
    sol.thickness = TRAY_WALL
    sol.offset = -1
    bpy.context.view_layer.objects.active = tray
    bpy.ops.object.modifier_apply(modifier="Shell")

    # Remove top face for open-top tray
    top_cut = add_cube(TRAY_W, 0.01, TRAY_D, loc=(0, TRAY_H/2, 0))
    bool_op(tray, top_cut, 'DIFFERENCE')

    # 6 V-Cell modules — 3 per side
    for row in range(2):
        for col in range(3):
            x = (col - 1) * (CELL_W + CELL_GAP)
            z = (row - 0.5) * (CELL_D + CELL_GAP)
            cell = add_cube(CELL_W/2, CELL_H/2, CELL_D/2,
                           loc=(x, -TRAY_H/2 + TRAY_WALL + CELL_H/2 + 0.002, z))
            bool_op(tray, cell, 'UNION')

    # Bus bars — top and bottom horizontal conductors
    for y_off in [-TRAY_H/2 + 0.008, TRAY_H/2 - 0.012]:
        bus = add_cube(BUS_W/2, BUS_H/2, BUS_D/2, loc=(0, y_off, 0))
        bool_op(tray, bus, 'UNION')

    # Cooling channel grooves — between cell rows
    channel = add_cube(TRAY_W * 0.4, TRAY_H * 0.35, 0.003,
                       loc=(0, 0, 0))
    bool_op(tray, channel, 'DIFFERENCE')

    tray.name = f"{PRODUCT}_{COMPONENT}"
    tray.data.name = f"{PRODUCT}_{COMPONENT}_mesh"
    return tray

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
