"""
Blender Headless Mesh Generator
Product: VSupreme  |  Component: ThighL
Run: blender --background --python this_script.py

Left thigh — heavy-duty armored tube with 3-DOF hip joint housing at top,
1-DOF knee joint housing at bottom, cycloidal drive motor bulge,
segmented armor plates, and cable/coolant routing channels.
"""
import bpy, bmesh, math, os

PRODUCT = "VSupreme"
COMPONENT = "ThighL"
MATERIAL = "Ti6Al4V"
OUT_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT_FILE = f"{PRODUCT}_{COMPONENT}.glb"

LENGTH = 0.360; TOP_R = 0.080; BOT_R = 0.065; WALL = 0.004
HIP_JOINT_R = 0.055; HIP_JOINT_H = 0.030
KNEE_JOINT_R = 0.050; KNEE_JOINT_H = 0.025
MOTOR_BULGE_R = 0.045; MOTOR_BULGE_H = 0.060

PBR = {"base_color": (1.0, 1.0, 1.0, 1.0), "metallic": 0.0, "roughness": 0.3,
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
    # Main tube — tapered
    bpy.ops.mesh.primitive_cone_add(vertices=32, radius1=TOP_R, radius2=BOT_R, depth=LENGTH)
    thigh=bpy.context.active_object
    sol=thigh.modifiers.new("Shell",'SOLIDIFY'); sol.thickness=WALL; sol.offset=-1
    bpy.context.view_layer.objects.active=thigh; bpy.ops.object.modifier_apply(modifier="Shell")

    # Hip joint housing at top
    jt=add_cyl(HIP_JOINT_R, HIP_JOINT_H, 32, loc=(0,LENGTH/2+HIP_JOINT_H/2,0))
    jti=add_cyl(HIP_JOINT_R-0.008, HIP_JOINT_H+0.01, 32, loc=(0,LENGTH/2+HIP_JOINT_H/2,0))
    bool_op(jt, jti, 'DIFFERENCE'); bool_op(thigh, jt, 'UNION')

    # Knee joint housing at bottom
    jb=add_cyl(KNEE_JOINT_R, KNEE_JOINT_H, 32, loc=(0,-LENGTH/2-KNEE_JOINT_H/2,0))
    jbi=add_cyl(KNEE_JOINT_R-0.008, KNEE_JOINT_H+0.01, 32, loc=(0,-LENGTH/2-KNEE_JOINT_H/2,0))
    bool_op(jb, jbi, 'DIFFERENCE'); bool_op(thigh, jb, 'UNION')

    # Cycloidal drive motor bulge — on outer side
    bulge=add_cyl(MOTOR_BULGE_R, MOTOR_BULGE_H, 24, loc=(-TOP_R*0.6, LENGTH/6, 0))
    bool_op(thigh, bulge, 'UNION')

    # Segmented armor — 2 flex gaps
    for y in [-LENGTH/8, LENGTH/8]:
        g=add_cube(TOP_R*2.5, 0.002, TOP_R*2.5, loc=(0,y,0))
        bool_op(thigh, g, 'DIFFERENCE')

    # Cable channel
    ch=add_cube(0.006, LENGTH*0.6, WALL+0.005, loc=(TOP_R*0.5, 0, -TOP_R*0.3))
    bool_op(thigh, ch, 'DIFFERENCE')

    thigh.name=f"{PRODUCT}_{COMPONENT}"; thigh.data.name=f"{PRODUCT}_{COMPONENT}_mesh"; return thigh

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
