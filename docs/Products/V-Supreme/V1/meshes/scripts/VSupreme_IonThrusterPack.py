"""
Blender Headless Mesh Generator
Product: VSupreme  |  Component: IonThrusterPack
Run: blender --background --python this_script.py

Ion thruster pack — back-mounted unit with 2 Hall-effect thruster bells,
xenon propellant tank (cylindrical), mounting frame, propellant feed lines,
and power connector bosses.
"""
import bpy, bmesh, math, os

PRODUCT = "VSupreme"
COMPONENT = "IonThrusterPack"
MATERIAL = "MoRe_Alloy"
OUT_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT_FILE = f"{PRODUCT}_{COMPONENT}.glb"

FRAME_W=0.350; FRAME_H=0.400; FRAME_D=0.150; FRAME_WALL=0.004
TANK_R=0.060; TANK_H=0.250
BELL_R_TOP=0.050; BELL_R_BOT=0.070; BELL_H=0.080; BELL_WALL=0.003
FEED_R=0.006; CONNECTOR_R=0.012; CONNECTOR_H=0.010

PBR={"base_color":(0.55,0.56,0.58,1.0),"metallic":1.0,"roughness":0.35,
     "alpha":1.0,"emission":(0.0,0.0,0.0,1.0),"emission_strength":0.0}
BEVEL_WIDTH=0.0004; BEVEL_SEGMENTS=2

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
def add_cyl(r,d,v=32,loc=(0,0,0)):
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
    # Mounting frame — rectangular open frame
    frame = add_cube(FRAME_W/2, FRAME_H/2, FRAME_D/2)
    frame_inner = add_cube(FRAME_W/2 - FRAME_WALL, FRAME_H/2 - FRAME_WALL, FRAME_D/2 + 0.01)
    bool_op(frame, frame_inner, 'DIFFERENCE')

    # Cross braces — 2 horizontal struts
    for y in [-FRAME_H/6, FRAME_H/6]:
        brace = add_cube(FRAME_W/2 - FRAME_WALL, FRAME_WALL, FRAME_D/2,
                        loc=(0, y, 0))
        bool_op(frame, brace, 'UNION')

    # Xenon propellant tank — central cylinder
    tank = add_cyl(TANK_R, TANK_H, 32, loc=(0, 0, 0))
    tank_inner = add_cyl(TANK_R - 0.004, TANK_H - 0.008, 32, loc=(0, 0, 0))
    bool_op(tank, tank_inner, 'DIFFERENCE')
    # End caps — hemispheres
    for side in [-1, 1]:
        bpy.ops.mesh.primitive_uv_sphere_add(segments=24, ring_count=12, radius=TANK_R,
                                              location=(0, side * TANK_H/2, 0))
        cap = bpy.context.active_object
        cap_cut = add_cube(TANK_R*2, TANK_H, TANK_R*2,
                          loc=(0, side * (TANK_H/2 - TANK_R/2 - 0.001), 0))
        if side == -1:
            cap_cut.location.y = -TANK_H/2 - TANK_R/2
        else:
            cap_cut.location.y = TANK_H/2 + TANK_R/2
        # Keep hemisphere toward center
        cut_loc = (0, side * TANK_H, 0)
        cap_trim = add_cube(TANK_R*2, TANK_R, TANK_R*2, loc=cut_loc)
        bool_op(cap, cap_trim, 'DIFFERENCE')
        bool_op(tank, cap, 'UNION')
    bool_op(frame, tank, 'UNION')

    # 2 thruster bells — truncated cones at bottom left/right
    for side in [-1, 1]:
        bpy.ops.mesh.primitive_cone_add(vertices=32, radius1=BELL_R_BOT, radius2=BELL_R_TOP,
                                         depth=BELL_H,
                                         location=(side * FRAME_W/4, -FRAME_H/2 - BELL_H/2, 0))
        bell = bpy.context.active_object
        # Hollow bell
        bpy.ops.mesh.primitive_cone_add(vertices=32, radius1=BELL_R_BOT - BELL_WALL,
                                         radius2=BELL_R_TOP - BELL_WALL,
                                         depth=BELL_H - BELL_WALL,
                                         location=(side * FRAME_W/4, -FRAME_H/2 - BELL_H/2, 0))
        bell_inner = bpy.context.active_object
        bool_op(bell, bell_inner, 'DIFFERENCE')
        bool_op(frame, bell, 'UNION')

    # Propellant feed lines — thin tubes from tank to bells
    for side in [-1, 1]:
        feed = add_cyl(FEED_R, FRAME_H/3, 16,
                      loc=(side * FRAME_W/8, -FRAME_H/4, TANK_R * 0.8))
        bool_op(frame, feed, 'UNION')

    # Power connector bosses — 2 cylinders on top
    for side in [-1, 1]:
        conn = add_cyl(CONNECTOR_R, CONNECTOR_H, 16,
                      loc=(side * FRAME_W/4, FRAME_H/2 + CONNECTOR_H/2, 0))
        bool_op(frame, conn, 'UNION')

    # Mounting bolt bosses — 4 corners
    for sx in [-1, 1]:
        for sy in [-1, 1]:
            bolt = add_cyl(0.008, 0.012, 16,
                          loc=(sx * FRAME_W/2 * 0.85, sy * FRAME_H/2 * 0.85, -FRAME_D/2))
            bool_op(frame, bolt, 'UNION')

    frame.name=f"{PRODUCT}_{COMPONENT}"; frame.data.name=f"{PRODUCT}_{COMPONENT}_mesh"; return frame

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
