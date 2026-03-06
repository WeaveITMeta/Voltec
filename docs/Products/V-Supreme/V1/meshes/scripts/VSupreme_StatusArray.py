"""
Blender Headless Mesh Generator
Product: VSupreme  |  Component: StatusArray
Run: blender --background --python this_script.py

Status array — visor-integrated LED bar with polycarbonate housing,
5 indicator LED domes, mounting clip, and connector pins.
"""
import bpy, bmesh, math, os

PRODUCT = "VSupreme"
COMPONENT = "StatusArray"
MATERIAL = "Polycarbonate"
OUT_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT_FILE = f"{PRODUCT}_{COMPONENT}.glb"

BAR_W=0.150; BAR_H=0.020; BAR_D=0.008
HOUSING_WALL=0.002
LED_R=0.005; N_LEDS=5; LED_SPACING=0.025
CLIP_W=0.015; CLIP_H=0.025; CLIP_D=0.003
PIN_R=0.001; PIN_H=0.008

PBR={"base_color":(0.05,0.05,0.05,0.8),"metallic":0.0,"roughness":0.1,
     "alpha":0.8,"emission":(0.0,0.0,0.0,1.0),"emission_strength":0.0}
PBR_LED={"base_color":(0.0,1.0,0.3,1.0),"metallic":0.0,"roughness":0.05,
         "alpha":1.0,"emission":(0.0,1.0,0.3,1.0),"emission_strength":5.0}
BEVEL_WIDTH=0.0002; BEVEL_SEGMENTS=2

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
    l.new(bsdf.outputs['BSDF'], out.inputs['Surface'])
    if pbr["alpha"] < 1.0:
        mat.blend_method = 'BLEND'
    return mat
def add_cyl(r,d,v=16,loc=(0,0,0)):
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
    # Housing bar — rounded rectangular extrusion
    bar = add_cube(BAR_W/2, BAR_H/2, BAR_D/2)
    sub=bar.modifiers.new("Sub",'SUBSURF'); sub.levels=1; sub.render_levels=1
    bpy.context.view_layer.objects.active=bar; bpy.ops.object.modifier_apply(modifier="Sub")

    # LED dome recesses + domes
    for i in range(N_LEDS):
        x = (i - (N_LEDS-1)/2) * LED_SPACING
        # Recess in housing
        recess = add_cyl(LED_R + 0.001, BAR_D, 16, loc=(x, 0, BAR_D/2 * 0.5))
        bool_op(bar, recess, 'DIFFERENCE')
        # LED dome — half sphere protruding from front
        bpy.ops.mesh.primitive_uv_sphere_add(segments=16, ring_count=8, radius=LED_R,
                                              location=(x, 0, BAR_D/2 * 0.7))
        dome = bpy.context.active_object
        # Cut back half of dome
        dome_cut = add_cube(LED_R*3, LED_R*3, LED_R, loc=(x, 0, BAR_D/2 * 0.7 - LED_R/2))
        bool_op(dome, dome_cut, 'DIFFERENCE')
        bool_op(bar, dome, 'UNION')

    # Mounting clips — 2 tabs on rear
    for side in [-1, 1]:
        clip = add_cube(CLIP_W/2, CLIP_H/2, CLIP_D/2,
                       loc=(side * BAR_W/3, 0, -BAR_D/2 - CLIP_D/2))
        bool_op(bar, clip, 'UNION')

    # Connector pins — 2 on bottom
    for side in [-1, 1]:
        pin = add_cyl(PIN_R, PIN_H, 8, loc=(side * 0.010, -BAR_H/2 - PIN_H/2, 0))
        bool_op(bar, pin, 'UNION')

    bar.name=f"{PRODUCT}_{COMPONENT}"; bar.data.name=f"{PRODUCT}_{COMPONENT}_mesh"; return bar

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
    mat_housing=create_material(f"MAT_{PRODUCT}_{MATERIAL}",PBR)
    obj=create_geometry(); obj.data.materials.append(mat_housing)
    polish(obj); verify(obj); export(obj)
if __name__=="__main__": main()
