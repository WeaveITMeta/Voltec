"""
Blender Headless Mesh Generator
Product: V-Core  |  Component: OuterCasing
Material: 304 Stainless Steel — egg-shaped prolate ellipsoid enclosure
Run: blender --background --python this_script.py
"""
import bpy, bmesh, math, os

PRODUCT = "VCore"
COMPONENT = "OuterCasing"
MATERIAL = "304SS"
OUT_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT_FILE = f"{PRODUCT}_{COMPONENT}.glb"

# Dimensions from PATENT.md §13.1 — prolate ellipsoid (egg)
# Height 800mm, Width 600mm, Depth 500mm
HEIGHT = 0.800
WIDTH = 0.600
DEPTH = 0.500
WALL = 0.004  # 4mm wall thickness

PBR = {
    "base_color": (0.55, 0.56, 0.58, 1.0),  # Steel
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
    # Outer egg shape — UV sphere scaled to prolate ellipsoid
    bpy.ops.mesh.primitive_uv_sphere_add(segments=48, ring_count=24, radius=1.0, location=(0, 0, 0))
    outer = bpy.context.active_object
    outer.scale = (WIDTH / 2.0, HEIGHT / 2.0, DEPTH / 2.0)
    bpy.ops.object.transform_apply(scale=True)

    # Slightly egg-shaped: scale top half taller, bottom half shorter
    # Apply proportional edit via mesh editing for egg shape
    bpy.ops.object.mode_set(mode='EDIT')
    bm = bmesh.from_edit_mesh(outer.data)
    # Make it egg-shaped: compress bottom, stretch top
    for v in bm.verts:
        if v.co.y > 0:
            # Top half — stretch slightly
            v.co.y *= 1.1
        else:
            # Bottom half — compress slightly
            v.co.y *= 0.9
    bmesh.update_edit_mesh(outer.data)
    bpy.ops.object.mode_set(mode='OBJECT')

    # Hollow it out with solidify
    sol = outer.modifiers.new("Shell", 'SOLIDIFY')
    sol.thickness = WALL
    sol.offset = -1
    bpy.context.view_layer.objects.active = outer
    bpy.ops.object.modifier_apply(modifier="Shell")

    # Add a flat base pad for mounting (small cylinder at bottom)
    bpy.ops.mesh.primitive_cylinder_add(vertices=48, radius=0.15, depth=0.015,
                                         location=(0, -HEIGHT * 0.45 - 0.005, 0))
    base = bpy.context.active_object
    bool_op(outer, base, 'UNION')

    # Add 4 mounting bolt bosses at base
    for angle in [0, 90, 180, 270]:
        rad = math.radians(angle)
        x = 0.12 * math.cos(rad)
        z = 0.12 * math.sin(rad)
        bpy.ops.mesh.primitive_cylinder_add(vertices=16, radius=0.012, depth=0.020,
                                             location=(x, -HEIGHT * 0.45 - 0.005, z))
        bolt = bpy.context.active_object
        bool_op(outer, bolt, 'UNION')

    outer.name = f"{PRODUCT}_{COMPONENT}"
    outer.data.name = f"{PRODUCT}_{COMPONENT}_mesh"
    return outer

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
