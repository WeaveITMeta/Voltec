"""
Blender Headless Mesh Generator
Product: V-Man  |  Component: ToolMagazine
Run: blender --background --python this_script.py

Tool magazine (RFID-tagged end-effector rack).
PATENT reference: Section 10.2 — mounted on right side of container.

Positioned at Y=0.0 (floor) to Y=1.62m (above utilities, within arm reach).
"""
import bpy, bmesh, math, os

PRODUCT = "VMan"
COMPONENT = "ToolMagazine"
MATERIAL = "Al6061T6"
OUT_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT_FILE = f"{PRODUCT}_{COMPONENT}.glb"

RACK_W = 0.800
RACK_H = 1.600
RACK_D = 0.350
FRAME = 0.040
BACK_PANEL_THICK = 0.012
SLOT_COUNT = 12
SLOT_COLS = 2
SLOT_ROWS = 6
SLOT_SPACING_Y = 0.120
PEG_RADIUS = 0.012
PEG_LENGTH = 0.200
LIP_W = 0.040
LIP_H = 0.030
LIP_D = 0.016
COL_SPACING_X = 0.300
MANIFOLD_R = 0.025
MANIFOLD_L = 0.480
FITTING_R = 0.008
FITTING_H = 0.030
FITTING_COUNT = 6
BASE_THICK = 0.020

PBR = {
    "base_color": (0.75, 0.78, 0.80, 1.0),
    "metallic": 1.0,
    "roughness": 0.35,
    "alpha": 1.0,
    "emission": (0.0, 0.0, 0.0, 1.0),
    "emission_strength": 0.0,
}

BEVEL_WIDTH = 0.001
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

def add_cyl(radius, depth, vertices=24, loc=(0, 0, 0), rot=(0, 0, 0)):
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
    base_center_y = BASE_THICK / 2
    body = add_box(RACK_W, BASE_THICK, RACK_D, loc=(0, base_center_y, 0))
    
    panel_min_y = BASE_THICK
    panel_center_y = panel_min_y + RACK_H / 2
    panel = add_box(RACK_W, RACK_H, BACK_PANEL_THICK, loc=(0, panel_center_y, BACK_PANEL_THICK / 2))
    bool_op(body, panel, 'UNION')
    
    upright_d = RACK_D - BACK_PANEL_THICK
    upright_center_z = BACK_PANEL_THICK + upright_d / 2
    left_x = -RACK_W / 2 + FRAME / 2
    left_upright = add_box(FRAME, RACK_H, upright_d, loc=(left_x, panel_center_y, upright_center_z))
    bool_op(body, left_upright, 'UNION')
    
    right_x = RACK_W / 2 - FRAME / 2
    right_upright = add_box(FRAME, RACK_H, upright_d, loc=(right_x, panel_center_y, upright_center_z))
    bool_op(body, right_upright, 'UNION')
    
    first_slot_y = BASE_THICK + 0.200
    col_x = [-COL_SPACING_X / 2, COL_SPACING_X / 2]
    for col in range(SLOT_COLS):
        cx = col_x[col]
        for row in range(SLOT_ROWS):
            slot_y = first_slot_y + row * SLOT_SPACING_Y
            peg_min_z = BACK_PANEL_THICK
            peg_center_z = peg_min_z + PEG_LENGTH / 2
            peg = add_cyl(PEG_RADIUS, PEG_LENGTH, 16, loc=(cx, slot_y, peg_center_z), rot=(math.pi / 2, 0, 0))
            bool_op(body, peg, 'UNION')
            
            lip_min_z = peg_min_z + PEG_LENGTH
            lip_center_z = lip_min_z + LIP_D / 2
            lip = add_box(LIP_W, LIP_H, LIP_D, loc=(cx, slot_y, lip_center_z))
            bool_op(body, lip, 'UNION')
    
    manifold_center_y = BASE_THICK + 0.060
    manifold_center_z = RACK_D - 0.040
    manifold = add_cyl(MANIFOLD_R, MANIFOLD_L, 24, loc=(0, manifold_center_y, manifold_center_z), rot=(0, 0, math.pi / 2))
    bool_op(body, manifold, 'UNION')
    
    fitting_start_x = -MANIFOLD_L / 2 + 0.040
    fitting_spacing = (MANIFOLD_L - 0.080) / (FITTING_COUNT - 1)
    fitting_center_z = manifold_center_z + MANIFOLD_R + FITTING_H / 2
    for i in range(FITTING_COUNT):
        fx = fitting_start_x + i * fitting_spacing
        fitting = add_cyl(FITTING_R, FITTING_H, 12, loc=(fx, manifold_center_y, fitting_center_z), rot=(math.pi / 2, 0, 0))
        bool_op(body, fitting, 'UNION')
    
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
    print(f"  PATENT alignment: Tool magazine, Y=0.0-1.62m, right side")
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
