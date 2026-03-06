"""
Blender Headless Mesh Generator
Product: VSupreme  |  Component: ShinR
Run: blender --background --python this_script.py

Right shin — mirror of ShinL. Armored tube with knee/ankle joint housings,
shin guard plate, cable routing.
"""
import bpy, bmesh, math, os

PRODUCT = "VSupreme"
COMPONENT = "ShinR"
MATERIAL = "Ti6Al4V"
OUT_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT_FILE = f"{PRODUCT}_{COMPONENT}.glb"

LENGTH=0.400; TOP_R=0.065; BOT_R=0.055; WALL=0.004
KNEE_R=0.050; KNEE_H=0.025; ANKLE_R=0.042; ANKLE_H=0.020

PBR={"base_color":(0.04,0.04,0.04,1.0),"metallic":0.0,"roughness":0.5,
     "alpha":1.0,"emission":(0.0,0.0,0.0,1.0),"emission_strength":0.0}
BEVEL_WIDTH=0.0005; BEVEL_SEGMENTS=2

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
def add_cyl(r,d,v=48,loc=(0,0,0)):
    bpy.ops.mesh.primitive_cylinder_add(vertices=v,radius=r,depth=d,location=loc)
    return bpy.context.active_object
def add_cube(sx,sy,sz,loc=(0,0,0)):
    bpy.ops.mesh.primitive_cube_add(size=1.0,location=loc)
    o=bpy.context.active_object; o.scale=(sx,sy,sz)
    bpy.ops.object.transform_apply(scale=True); return o
def bool_op(target,cutter,op='UNION'):
    mod=target.modifiers.new(op,'BOOLEAN'); mod.operation=op; mod.object=cutter; mod.solver='EXACT'
    bpy.context.view_layer.objects.active=target; bpy.ops.object.modifier_apply(modifier=op)
    bpy.data.objects.remove(cutter,do_unlink=True)

def create_geometry():
    bpy.ops.mesh.primitive_cone_add(vertices=32,radius1=TOP_R,radius2=BOT_R,depth=LENGTH)
    s=bpy.context.active_object
    sol=s.modifiers.new("Shell",'SOLIDIFY'); sol.thickness=WALL; sol.offset=-1
    bpy.context.view_layer.objects.active=s; bpy.ops.object.modifier_apply(modifier="Shell")
    jt=add_cyl(KNEE_R,KNEE_H,32,loc=(0,LENGTH/2+KNEE_H/2,0))
    jti=add_cyl(KNEE_R-0.008,KNEE_H+0.01,32,loc=(0,LENGTH/2+KNEE_H/2,0))
    bool_op(jt,jti,'DIFFERENCE'); bool_op(s,jt,'UNION')
    jb=add_cyl(ANKLE_R,ANKLE_H,32,loc=(0,-LENGTH/2-ANKLE_H/2,0))
    jbi=add_cyl(ANKLE_R-0.006,ANKLE_H+0.01,32,loc=(0,-LENGTH/2-ANKLE_H/2,0))
    bool_op(jb,jbi,'DIFFERENCE'); bool_op(s,jb,'UNION')
    guard=add_cube(0.030,LENGTH*0.35,0.008,loc=(0,LENGTH*0.05,TOP_R*0.85))
    bool_op(s,guard,'UNION')
    for y in [-LENGTH/8, LENGTH/8]:
        g=add_cube(TOP_R*2.5,0.002,TOP_R*2.5,loc=(0,y,0)); bool_op(s,g,'DIFFERENCE')
    ch=add_cube(0.006,LENGTH*0.6,WALL+0.005,loc=(TOP_R*0.5,0,0))
    bool_op(s,ch,'DIFFERENCE')
    s.name=f"{PRODUCT}_{COMPONENT}"; s.data.name=f"{PRODUCT}_{COMPONENT}_mesh"; return s

def polish(obj):
    bv=obj.modifiers.new("Bevel",'BEVEL'); bv.width=BEVEL_WIDTH; bv.segments=BEVEL_SEGMENTS
    bv.limit_method='ANGLE'; bv.angle_limit=math.radians(30); bv.harden_normals=True
    bpy.context.view_layer.objects.active=obj; bpy.ops.object.modifier_apply(modifier="Bevel")
    bpy.ops.object.shade_auto_smooth()
    bpy.ops.object.mode_set(mode='EDIT'); bpy.ops.mesh.select_all(action='SELECT')
    bpy.ops.uv.smart_project(angle_limit=math.radians(66),island_margin=0.02)
    bpy.ops.mesh.normals_make_consistent(inside=False); bpy.ops.mesh.remove_doubles(threshold=0.0001)
    bpy.ops.object.mode_set(mode='OBJECT')
    bpy.ops.object.transform_apply(location=True,rotation=True,scale=True)
    bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY',center='BOUNDS')
def verify(obj):
    bm=bmesh.new(); bm.from_mesh(obj.data); f=len(bm.faces)
    q=sum(1 for fc in bm.faces if len(fc.verts)==4)
    nm=sum(1 for e in bm.edges if not e.is_manifold)
    print(f"\n  MESH: {obj.name}  |  V:{len(bm.verts)} E:{len(bm.edges)} F:{f}")
    print(f"  Quads: {q}/{f} ({100*q/max(f,1):.0f}%)  |  Non-manifold: {nm}  |  Watertight: {'YES' if nm==0 else 'FIX'}")
    bm.free()
def export(obj):
    os.makedirs(OUT_DIR,exist_ok=True); path=os.path.join(OUT_DIR,OUT_FILE)
    bpy.ops.object.select_all(action='DESELECT'); obj.select_set(True)
    bpy.context.view_layer.objects.active=obj
    bpy.ops.export_scene.gltf(filepath=path,export_format='GLB',use_selection=True,
        export_apply=True,export_normals=True,export_materials='EXPORT',
        export_cameras=False,export_lights=False,export_animations=False,
        export_yup=True,export_draco_mesh_compression_enable=True,export_draco_mesh_compression_level=6)
    print(f"  EXPORTED: {path} ({os.path.getsize(path)/1024:.1f} KB)\n")
def main():
    clean_scene(); setup_scene()
    mat=create_material(f"MAT_{PRODUCT}_{MATERIAL}",PBR)
    obj=create_geometry(); obj.data.materials.append(mat); polish(obj); verify(obj); export(obj)
if __name__=="__main__": main()
