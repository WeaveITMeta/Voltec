"""
Blender Headless Mesh Generator
Product: VSupreme  |  Component: HipAssembly
Run: blender --background --python this_script.py

Hip assembly — load distribution ring with 3-DOF hip actuator housings
(left and right), spine attachment boss, leg mount flanges, and utility routing.
"""
import bpy, bmesh, math, os

PRODUCT = "VSupreme"
COMPONENT = "HipAssembly"
MATERIAL = "Ti6Al4V"
OUT_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT_FILE = f"{PRODUCT}_{COMPONENT}.glb"

RING_R_OUTER = 0.225; RING_R_INNER = 0.180; RING_H = 0.180
HIP_JOINT_R = 0.055; HIP_JOINT_H = 0.040
SPINE_BOSS_R = 0.030; SPINE_BOSS_H = 0.020

PBR = {"base_color": (0.04, 0.04, 0.04, 1.0), "metallic": 0.0, "roughness": 0.5,
       "alpha": 1.0, "emission": (0.0, 0.0, 0.0, 1.0), "emission_strength": 0.0}
BEVEL_WIDTH = 0.0005; BEVEL_SEGMENTS = 2

def clean_scene():
    bpy.ops.object.select_all(action='SELECT'); bpy.ops.object.delete(use_global=False)
    for b in bpy.data.meshes:
        if b.users==0: bpy.data.meshes.remove(b)
    for b in bpy.data.materials:
        if b.users==0: bpy.data.materials.remove(b)

def setup_scene():
    bpy.context.scene.name="Scene0"; bpy.context.scene.unit_settings.system='METRIC'

def create_material(name, pbr):
    mat=bpy.data.materials.new(name=name); mat.use_nodes=True; mat.use_backface_culling=True
    n=mat.node_tree.nodes; l=mat.node_tree.links; n.clear()
    bsdf=n.new('ShaderNodeBsdfPrincipled')
    bsdf.inputs['Base Color'].default_value=pbr["base_color"]
    bsdf.inputs['Metallic'].default_value=pbr["metallic"]
    bsdf.inputs['Roughness'].default_value=pbr["roughness"]
    bsdf.inputs['Alpha'].default_value=pbr["alpha"]
    bsdf.inputs['Emission Color'].default_value=pbr["emission"]
    bsdf.inputs['Emission Strength'].default_value=pbr["emission_strength"]
    out=n.new('ShaderNodeOutputMaterial'); out.location=(300,0)
    l.new(bsdf.outputs['BSDF'], out.inputs['Surface']); return mat

def add_cyl(r, d, v=48, loc=(0,0,0)):
    bpy.ops.mesh.primitive_cylinder_add(vertices=v, radius=r, depth=d, location=loc)
    return bpy.context.active_object

def add_cube(sx, sy, sz, loc=(0,0,0)):
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=loc)
    o=bpy.context.active_object; o.scale=(sx,sy,sz)
    bpy.ops.object.transform_apply(scale=True); return o

def bool_op(target, cutter, op='UNION'):
    mod=target.modifiers.new(op,'BOOLEAN'); mod.operation=op; mod.object=cutter; mod.solver='EXACT'
    bpy.context.view_layer.objects.active=target; bpy.ops.object.modifier_apply(modifier=op)
    bpy.data.objects.remove(cutter, do_unlink=True)

def create_geometry():
    # Main ring — thick-walled cylinder
    ring = add_cyl(RING_R_OUTER, RING_H, 48)
    inner = add_cyl(RING_R_INNER, RING_H + 0.01, 48)
    bool_op(ring, inner, 'DIFFERENCE')

    # Front armor panel — curved plate over abdomen
    front_panel = add_cube(RING_R_OUTER * 0.8, RING_H/2 * 0.9, 0.008,
                           loc=(0, 0, RING_R_OUTER * 0.85))
    bool_op(ring, front_panel, 'UNION')

    # Hip joint housings — left and right
    for side in [-1, 1]:
        jh = add_cyl(HIP_JOINT_R, HIP_JOINT_H, 32,
                     loc=(side * RING_R_OUTER * 0.7, -RING_H/4, 0))
        jhi = add_cyl(HIP_JOINT_R - 0.008, HIP_JOINT_H + 0.01, 32,
                      loc=(side * RING_R_OUTER * 0.7, -RING_H/4, 0))
        bool_op(jh, jhi, 'DIFFERENCE')
        bool_op(ring, jh, 'UNION')

    # Spine attachment boss — top center rear
    spine = add_cyl(SPINE_BOSS_R, SPINE_BOSS_H, 24,
                    loc=(0, RING_H/2, -RING_R_OUTER * 0.6))
    bool_op(ring, spine, 'UNION')

    # Utility routing channels — 2 grooves
    for side in [-1, 1]:
        ch = add_cube(0.008, RING_H * 0.6, 0.008,
                      loc=(side * RING_R_OUTER * 0.5, 0, -RING_R_OUTER * 0.3))
        bool_op(ring, ch, 'DIFFERENCE')

    # Belt-line armor ridge
    ridge = add_cyl(RING_R_OUTER + 0.005, 0.015, 48, loc=(0, RING_H/4, 0))
    ridge_inner = add_cyl(RING_R_OUTER - 0.002, 0.020, 48, loc=(0, RING_H/4, 0))
    bool_op(ridge, ridge_inner, 'DIFFERENCE')
    bool_op(ring, ridge, 'UNION')

    ring.name=f"{PRODUCT}_{COMPONENT}"; ring.data.name=f"{PRODUCT}_{COMPONENT}_mesh"; return ring

def polish(obj):
    bv=obj.modifiers.new("Bevel",'BEVEL'); bv.width=BEVEL_WIDTH; bv.segments=BEVEL_SEGMENTS
    bv.limit_method='ANGLE'; bv.angle_limit=math.radians(30); bv.harden_normals=True
    bpy.context.view_layer.objects.active=obj; bpy.ops.object.modifier_apply(modifier="Bevel")
    bpy.ops.object.shade_auto_smooth()
    bpy.ops.object.mode_set(mode='EDIT'); bpy.ops.mesh.select_all(action='SELECT')
    bpy.ops.uv.smart_project(angle_limit=math.radians(66), island_margin=0.02)
    bpy.ops.mesh.normals_make_consistent(inside=False); bpy.ops.mesh.remove_doubles(threshold=0.0001)
    bpy.ops.object.mode_set(mode='OBJECT')
    bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
    bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY', center='BOUNDS')

def verify(obj):
    bm=bmesh.new(); bm.from_mesh(obj.data); f=len(bm.faces)
    q=sum(1 for fc in bm.faces if len(fc.verts)==4)
    nm=sum(1 for e in bm.edges if not e.is_manifold)
    print(f"\n  MESH: {obj.name}  |  V:{len(bm.verts)} E:{len(bm.edges)} F:{f}")
    print(f"  Quads: {q}/{f} ({100*q/max(f,1):.0f}%)  |  Non-manifold: {nm}  |  Watertight: {'YES' if nm==0 else 'FIX'}")
    bm.free()

def export(obj):
    os.makedirs(OUT_DIR, exist_ok=True); path=os.path.join(OUT_DIR, OUT_FILE)
    bpy.ops.object.select_all(action='DESELECT'); obj.select_set(True)
    bpy.context.view_layer.objects.active=obj
    bpy.ops.export_scene.gltf(filepath=path, export_format='GLB', use_selection=True,
        export_apply=True, export_normals=True, export_materials='EXPORT',
        export_cameras=False, export_lights=False, export_animations=False,
        export_yup=True, export_draco_mesh_compression_enable=True, export_draco_mesh_compression_level=6)
    print(f"  EXPORTED: {path} ({os.path.getsize(path)/1024:.1f} KB)\n")

def main():
    clean_scene(); setup_scene()
    mat=create_material(f"MAT_{PRODUCT}_{MATERIAL}", PBR)
    obj=create_geometry(); obj.data.materials.append(mat); polish(obj); verify(obj); export(obj)

if __name__=="__main__": main()
