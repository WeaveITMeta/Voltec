"""
Blender Headless Mesh Generator
Product: VSupreme  |  Component: FusionReactor
Run: blender --background --python this_script.py

Compact aneutronic p-B11 fusion reactor core — cylindrical W-Re vessel with
YBCO superconductor coil bands, proton injector port, direct energy converter
cone, cooling flanges, and diagnostic port stubs.
Patent ref: WO2015155531A1 (compact fusion reactor cross section)
"""
import bpy, bmesh, math, os

PRODUCT = "VSupreme"
COMPONENT = "FusionReactor"
MATERIAL = "WRe_Alloy"
OUT_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT_FILE = f"{PRODUCT}_{COMPONENT}.glb"

VESSEL_R = 0.125     # 250mm diameter
VESSEL_H = 0.300     # 300mm tall
VESSEL_WALL = 0.005  # 5mm W-Re first wall
COIL_R = 0.135       # Coil outer radius
COIL_W = 0.020       # Coil band width
COIL_T = 0.008       # Coil thickness
N_COILS = 6
INJECTOR_R = 0.015
INJECTOR_H = 0.040
CONVERTER_R1 = 0.100
CONVERTER_R2 = 0.050
CONVERTER_H = 0.060
FLANGE_R = 0.020
FLANGE_H = 0.008

PBR = {
    "base_color": (0.55, 0.56, 0.58, 1.0),  # Steel grey (W-Re)
    "metallic": 1.0,
    "roughness": 0.4,
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

def add_cyl(r, d, v=48, loc=(0,0,0), rot=(0,0,0)):
    bpy.ops.mesh.primitive_cylinder_add(vertices=v, radius=r, depth=d, location=loc, rotation=rot)
    return bpy.context.active_object

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
    # Main vessel — thick-walled cylinder
    vessel = add_cyl(VESSEL_R, VESSEL_H, 48)
    sol = vessel.modifiers.new("Hollow", 'SOLIDIFY')
    sol.thickness = VESSEL_WALL
    sol.offset = -1
    bpy.context.view_layer.objects.active = vessel
    bpy.ops.object.modifier_apply(modifier="Hollow")

    # YBCO superconductor coil bands — 6 toroidal rings around vessel
    for i in range(N_COILS):
        y_pos = -VESSEL_H/2 + VESSEL_H/(N_COILS+1) * (i+1)
        coil_outer = add_cyl(COIL_R, COIL_W, 48, loc=(0, y_pos, 0))
        coil_inner = add_cyl(COIL_R - COIL_T, COIL_W + 0.002, 48, loc=(0, y_pos, 0))
        bool_op(coil_outer, coil_inner, 'DIFFERENCE')
        bool_op(vessel, coil_outer, 'UNION')

    # Proton injector port — cylinder on top
    injector = add_cyl(INJECTOR_R, INJECTOR_H, 24, loc=(0, VESSEL_H/2 + INJECTOR_H/2, 0))
    # Injector bore
    bore = add_cyl(INJECTOR_R * 0.5, INJECTOR_H + 0.01, 24,
                   loc=(0, VESSEL_H/2 + INJECTOR_H/2, 0))
    bool_op(injector, bore, 'DIFFERENCE')
    bool_op(vessel, injector, 'UNION')

    # Direct energy converter cone — truncated cone on bottom
    bpy.ops.mesh.primitive_cone_add(vertices=48, radius1=CONVERTER_R1,
                                     radius2=CONVERTER_R2, depth=CONVERTER_H,
                                     location=(0, -VESSEL_H/2 - CONVERTER_H/2, 0))
    converter = bpy.context.active_object
    # Hollow the converter
    bpy.ops.mesh.primitive_cone_add(vertices=48, radius1=CONVERTER_R1 - 0.004,
                                     radius2=CONVERTER_R2 - 0.004,
                                     depth=CONVERTER_H - 0.004,
                                     location=(0, -VESSEL_H/2 - CONVERTER_H/2, 0))
    conv_inner = bpy.context.active_object
    bool_op(converter, conv_inner, 'DIFFERENCE')
    bool_op(vessel, converter, 'UNION')

    # Cooling flanges — 4 radial port stubs
    for angle_deg in [0, 90, 180, 270]:
        angle = math.radians(angle_deg)
        x = VESSEL_R * math.cos(angle)
        z = VESSEL_R * math.sin(angle)
        flange = add_cyl(FLANGE_R, FLANGE_H, 24, loc=(x, 0, z))
        # Orient radially outward
        if angle_deg in [0, 180]:
            flange.rotation_euler = (0, 0, math.radians(90))
        else:
            flange.rotation_euler = (math.radians(90), 0, 0)
        bpy.context.view_layer.objects.active = flange
        bpy.ops.object.transform_apply(rotation=True)
        # Flange bore
        fbore = add_cyl(FLANGE_R * 0.6, FLANGE_H + 0.01, 24, loc=(x, 0, z))
        if angle_deg in [0, 180]:
            fbore.rotation_euler = (0, 0, math.radians(90))
        else:
            fbore.rotation_euler = (math.radians(90), 0, 0)
        bpy.context.view_layer.objects.active = fbore
        bpy.ops.object.transform_apply(rotation=True)
        bool_op(flange, fbore, 'DIFFERENCE')
        bool_op(vessel, flange, 'UNION')

    # Diagnostic port stubs — 2 small cylinders at 45° and 135°
    for angle_deg in [45, 135]:
        angle = math.radians(angle_deg)
        x = VESSEL_R * 0.9 * math.cos(angle)
        z = VESSEL_R * 0.9 * math.sin(angle)
        stub = add_cyl(0.008, 0.015, 16, loc=(x, 0.08, z))
        bool_op(vessel, stub, 'UNION')

    vessel.name = f"{PRODUCT}_{COMPONENT}"
    vessel.data.name = f"{PRODUCT}_{COMPONENT}_mesh"
    return vessel

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
