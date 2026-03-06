"""
Blender Headless Mesh Generator
Product: VSupreme  |  Component: PauldronL
Run: blender --background --python this_script.py

Left shoulder pauldron — curved armor shell over 3-DOF shoulder actuator housing,
with modular hardpoint mount boss, ventilation slots, and mounting flange.
"""
import bpy, bmesh, math, os

PRODUCT = "VSupreme"
COMPONENT = "PauldronL"
MATERIAL = "Ti6Al4V"
OUT_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT_FILE = f"{PRODUCT}_{COMPONENT}.glb"

OUTER_RX = 0.100
OUTER_RY = 0.090
OUTER_RZ = 0.110
WALL = 0.004
HARDPOINT_R = 0.018
HARDPOINT_H = 0.012
MOUNT_R = 0.030
MOUNT_H = 0.008

PBR = {
    "base_color": (1.0, 1.0, 1.0, 1.0),
    "metallic": 0.0,
    "roughness": 0.3,
    "alpha": 1.0,
    "emission": (0.0, 0.0, 0.0, 1.0),
    "emission_strength": 0.0,
}
BEVEL_WIDTH = 0.0005
BEVEL_SEGMENTS = 2

def clean_scene():
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete(use_global=False)
    for b in bpy.data.meshes:
        if b.users == 0: bpy.data.meshes.remove(b)
    for b in bpy.data.materials:
        if b.users == 0: bpy.data.materials.remove(b)

def setup_scene():
    bpy.context.scene.name = "Scene0"
    bpy.context.scene.unit_settings.system = 'METRIC'
    bpy.context.scene.unit_settings.scale_length = 1.0

def create_material(name, pbr):
    mat = bpy.data.materials.new(name=name)
    mat.use_nodes = True; mat.use_backface_culling = True
    n = mat.node_tree.nodes; l = mat.node_tree.links; n.clear()
    bsdf = n.new('ShaderNodeBsdfPrincipled')
    bsdf.inputs['Base Color'].default_value = pbr["base_color"]
    bsdf.inputs['Metallic'].default_value = pbr["metallic"]
    bsdf.inputs['Roughness'].default_value = pbr["roughness"]
    bsdf.inputs['Alpha'].default_value = pbr["alpha"]
    bsdf.inputs['Emission Color'].default_value = pbr["emission"]
    bsdf.inputs['Emission Strength'].default_value = pbr["emission_strength"]
    out = n.new('ShaderNodeOutputMaterial'); out.location = (300,0)
    l.new(bsdf.outputs['BSDF'], out.inputs['Surface'])
    return mat

def add_cyl(r, d, v=48, loc=(0,0,0), rot=(0,0,0)):
    bpy.ops.mesh.primitive_cylinder_add(vertices=v, radius=r, depth=d, location=loc, rotation=rot)
    return bpy.context.active_object

def add_cube(sx, sy, sz, loc=(0,0,0)):
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=loc)
    o = bpy.context.active_object; o.scale=(sx,sy,sz)
    bpy.ops.object.transform_apply(scale=True); return o

def bool_op(target, cutter, op='UNION'):
    mod = target.modifiers.new(op, 'BOOLEAN')
    mod.operation=op; mod.object=cutter; mod.solver='EXACT'
    bpy.context.view_layer.objects.active = target
    bpy.ops.object.modifier_apply(modifier=op)
    bpy.data.objects.remove(cutter, do_unlink=True)

def create_geometry():
    # Pauldron shell — half-ellipsoid
    bpy.ops.mesh.primitive_uv_sphere_add(segments=32, ring_count=16, radius=1.0)
    p = bpy.context.active_object
    p.scale = (OUTER_RX, OUTER_RY, OUTER_RZ)
    bpy.ops.object.transform_apply(scale=True)
    # Hollow
    sol = p.modifiers.new("Shell", 'SOLIDIFY')
    sol.thickness = WALL; sol.offset = -1
    bpy.context.view_layer.objects.active = p
    bpy.ops.object.modifier_apply(modifier="Shell")
    # Cut bottom half — open underside for arm
    cut = add_cube(0.3, OUTER_RY, 0.3, loc=(0, -OUTER_RY/2, 0))
    bool_op(p, cut, 'DIFFERENCE')
    # Cut inner side (toward torso)
    inner_cut = add_cube(0.05, 0.2, 0.3, loc=(OUTER_RX * 0.8, 0, 0))
    bool_op(p, inner_cut, 'DIFFERENCE')
    # Hardpoint boss on top
    hp = add_cyl(HARDPOINT_R, HARDPOINT_H, 24, loc=(0, OUTER_RY * 0.7, 0))
    bool_op(p, hp, 'UNION')
    # Mounting flange at inner edge
    flange = add_cyl(MOUNT_R, MOUNT_H, 32,
                     loc=(OUTER_RX * 0.6, 0.02, 0),
                     rot=(0, 0, math.radians(90)))
    bool_op(p, flange, 'UNION')
    # Ventilation slots
    for i in range(3):
        sl = add_cube(0.004, 0.025, OUTER_RZ * 0.5,
                      loc=(-OUTER_RX * 0.5, 0.03 + i * 0.015, 0))
        bool_op(p, sl, 'DIFFERENCE')

    p.name = f"{PRODUCT}_{COMPONENT}"
    p.data.name = f"{PRODUCT}_{COMPONENT}_mesh"
    return p

def polish(obj):
    bv = obj.modifiers.new("Bevel",'BEVEL')
    bv.width=BEVEL_WIDTH; bv.segments=BEVEL_SEGMENTS; bv.limit_method='ANGLE'
    bv.angle_limit=math.radians(30); bv.harden_normals=True
    bpy.context.view_layer.objects.active=obj
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
    bm = bmesh.new(); bm.from_mesh(obj.data)
    f=len(bm.faces); q=sum(1 for fc in bm.faces if len(fc.verts)==4)
    nm=sum(1 for e in bm.edges if not e.is_manifold)
    print(f"\n  MESH: {obj.name}  |  V:{len(bm.verts)} E:{len(bm.edges)} F:{f}")
    print(f"  Quads: {q}/{f} ({100*q/max(f,1):.0f}%)  |  Non-manifold: {nm}  |  Watertight: {'YES' if nm==0 else 'FIX'}")
    bm.free()

def export(obj):
    os.makedirs(OUT_DIR, exist_ok=True)
    path = os.path.join(OUT_DIR, OUT_FILE)
    bpy.ops.object.select_all(action='DESELECT')
    obj.select_set(True); bpy.context.view_layer.objects.active=obj
    bpy.ops.export_scene.gltf(filepath=path, export_format='GLB', use_selection=True,
        export_apply=True, export_normals=True, export_materials='EXPORT',
        export_cameras=False, export_lights=False, export_animations=False,
        export_yup=True, export_draco_mesh_compression_enable=True,
        export_draco_mesh_compression_level=6)
    print(f"  EXPORTED: {path} ({os.path.getsize(path)/1024:.1f} KB)\n")

def main():
    clean_scene(); setup_scene()
    mat = create_material(f"MAT_{PRODUCT}_{MATERIAL}", PBR)
    obj = create_geometry(); obj.data.materials.append(mat)
    polish(obj); verify(obj); export(obj)

if __name__ == "__main__":
    main()
