"""
Blender Headless Mesh Generator
Product: V-Core  |  Component: FuelAssembly
Material: U-ZrH1.6 — 37 fuel rods in triangular lattice, Ø250mm × 380mm
Run: blender --background --python this_script.py
"""
import bpy, bmesh, math, os

PRODUCT = "VCore"
COMPONENT = "FuelAssembly"
MATERIAL = "UZrH"
OUT_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT_FILE = f"{PRODUCT}_{COMPONENT}.glb"

ROD_R = 0.01875  # 37.5mm diameter / 2
ROD_H = 0.380    # active length
PITCH = 0.045    # rod pitch (triangular)
ASSEMBLY_R = 0.125  # Ø250mm / 2

PBR = {
    "base_color": (0.45, 0.45, 0.40, 1.0),  # Dark grey-green (fuel alloy)
    "metallic": 1.0,
    "roughness": 0.50,
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

def hex_ring_positions(ring, pitch):
    """Generate positions for a hexagonal ring of fuel rods."""
    if ring == 0:
        return [(0.0, 0.0)]
    positions = []
    for side in range(6):
        angle_start = math.radians(60 * side)
        angle_next = math.radians(60 * (side + 1))
        for i in range(ring):
            t = i / ring
            x = ring * pitch * math.cos(angle_start) * (1 - t) + ring * pitch * math.cos(angle_next) * t
            z = ring * pitch * math.sin(angle_start) * (1 - t) + ring * pitch * math.sin(angle_next) * t
            positions.append((x, z))
    return positions

def create_geometry():
    # Generate fuel rod positions: center + 3 hexagonal rings = 1+6+12+18 = 37 rods
    positions = []
    for ring in range(4):
        positions.extend(hex_ring_positions(ring, PITCH))

    # Create first rod as the base object
    first_pos = positions[0]
    bpy.ops.mesh.primitive_cylinder_add(vertices=12, radius=ROD_R, depth=ROD_H,
                                         location=(first_pos[0], 0, first_pos[1]))
    assembly = bpy.context.active_object

    # Union remaining rods
    for pos in positions[1:]:
        bpy.ops.mesh.primitive_cylinder_add(vertices=12, radius=ROD_R, depth=ROD_H,
                                             location=(pos[0], 0, pos[1]))
        rod = bpy.context.active_object
        bool_op(assembly, rod, 'UNION')

    # Lower grid plate (thin disk)
    bpy.ops.mesh.primitive_cylinder_add(vertices=48, radius=ASSEMBLY_R, depth=0.008,
                                         location=(0, -ROD_H/2.0 - 0.004, 0))
    grid = bpy.context.active_object
    bool_op(assembly, grid, 'UNION')

    # Upper grid plate
    bpy.ops.mesh.primitive_cylinder_add(vertices=48, radius=ASSEMBLY_R, depth=0.008,
                                         location=(0, ROD_H/2.0 + 0.004, 0))
    grid2 = bpy.context.active_object
    bool_op(assembly, grid2, 'UNION')

    assembly.name = f"{PRODUCT}_{COMPONENT}"
    assembly.data.name = f"{PRODUCT}_{COMPONENT}_mesh"
    return assembly

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
