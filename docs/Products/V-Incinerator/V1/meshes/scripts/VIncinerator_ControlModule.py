"""
V-Incinerator — Control Module  (Blender 4.4 headless)
=======================================================
FR4 PCB + V-OS embedded control electronics enclosure.
NEMA 4X rated industrial control panel. Rectangular enclosure with
hinged door panel (raised), cable gland ports on bottom,
ventilation fan grille on side, DIN rail mounting bracket,
display cutout on door, conduit entry stubs.

Run: blender --background --python this_script.py
"""
import bpy, bmesh, math, os

PRODUCT   = "VIncinerator"
COMPONENT = "ControlModule"
MATERIAL  = "PowderCoat_Steel"
OUT_DIR   = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT_FILE  = f"{PRODUCT}_{COMPONENT}.glb"

# ── Dimensions ────────────────────────────────────────────────────────
WIDTH  = 0.60        # enclosure X
DEPTH  = 0.30        # enclosure Y
HEIGHT = 0.80        # enclosure Z
WALL   = 0.003
DOOR_D = 0.004       # raised door panel
DISP_W = 0.20        # display window
DISP_H = 0.12
GLAND_R = 0.015      # cable gland radius
GLAND_L = 0.03
FAN_W  = 0.10        # ventilation grille
FAN_H  = 0.10
CONDUIT_R = 0.02
CONDUIT_L = 0.05
MOUNT_W = 0.04
MOUNT_D = 0.02
MOUNT_H = 0.06

PBR = {
    "base_color": (0.25, 0.28, 0.30, 1.0),  # dark industrial grey
    "metallic": 0.6,
    "roughness": 0.50,
    "alpha": 1.0,
    "emission": (0.0, 0.0, 0.0, 1.0),
    "emission_strength": 0.0,
}

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

def create_material():
    mat = bpy.data.materials.new(name=f"MAT_{PRODUCT}_{MATERIAL}")
    mat.use_nodes = True; mat.use_backface_culling = True
    nodes = mat.node_tree.nodes; links = mat.node_tree.links; nodes.clear()
    bsdf = nodes.new('ShaderNodeBsdfPrincipled')
    bsdf.inputs['Base Color'].default_value = PBR["base_color"]
    bsdf.inputs['Metallic'].default_value = PBR["metallic"]
    bsdf.inputs['Roughness'].default_value = PBR["roughness"]
    bsdf.inputs['Alpha'].default_value = PBR["alpha"]
    bsdf.inputs['Emission Color'].default_value = PBR["emission"]
    bsdf.inputs['Emission Strength'].default_value = PBR["emission_strength"]
    out = nodes.new('ShaderNodeOutputMaterial'); out.location = (300, 0)
    links.new(bsdf.outputs['BSDF'], out.inputs['Surface'])
    return mat

def add_cube(sx, sy, sz, loc=(0,0,0)):
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=loc)
    obj = bpy.context.active_object; obj.scale = (sx, sy, sz)
    bpy.ops.object.transform_apply(scale=True)
    return obj

def add_cyl(r, d, v=16, loc=(0,0,0), rot=(0,0,0)):
    bpy.ops.mesh.primitive_cylinder_add(vertices=v, radius=r, depth=d,
                                        location=loc, rotation=rot)
    return bpy.context.active_object

def bool_op(target, cutter, op='UNION'):
    mod = target.modifiers.new(op, 'BOOLEAN')
    mod.operation = op; mod.object = cutter; mod.solver = 'EXACT'
    bpy.context.view_layer.objects.active = target
    bpy.ops.object.modifier_apply(modifier=op)
    bpy.data.objects.remove(cutter, do_unlink=True)

def create_geometry():
    """Industrial control panel enclosure with door, glands, fan, conduits."""

    # 1) Main enclosure — hollow box
    box = add_cube(WIDTH, DEPTH, HEIGHT)
    sol = box.modifiers.new("Hollow", 'SOLIDIFY')
    sol.thickness = WALL; sol.offset = -1
    bpy.context.view_layer.objects.active = box
    bpy.ops.object.modifier_apply(modifier="Hollow")

    # 2) Door panel — raised rectangle on front face (+Y)
    door = add_cube(WIDTH * 0.92, DOOR_D, HEIGHT * 0.92,
                     (0, DEPTH/2 + DOOR_D/2, 0))
    bool_op(box, door, 'UNION')

    # 3) Display window cutout detail (raised bezel on door)
    bezel = add_cube(DISP_W + 0.02, DOOR_D * 0.8, DISP_H + 0.02,
                      (0, DEPTH/2 + DOOR_D, HEIGHT/4))
    bool_op(box, bezel, 'UNION')
    # Display glass (thin recessed panel)
    glass = add_cube(DISP_W, DOOR_D * 0.3, DISP_H,
                      (0, DEPTH/2 + DOOR_D + DOOR_D * 0.3, HEIGHT/4))
    bool_op(box, glass, 'UNION')

    # 4) Door handle
    handle = add_cube(0.06, 0.015, 0.02,
                       (WIDTH/2 * 0.7, DEPTH/2 + DOOR_D + 0.008, 0))
    bool_op(box, handle, 'UNION')

    # 5) Door hinges (2 on left side)
    for z_off in [-HEIGHT/4, HEIGHT/4]:
        hinge = add_cube(0.015, 0.02, 0.04,
                          (-WIDTH/2 * 0.85, DEPTH/2 + DOOR_D/2, z_off))
        bool_op(box, hinge, 'UNION')

    # 6) Cable gland ports (6 on bottom)
    for i in range(6):
        x = -WIDTH/3 + i * WIDTH/7.5
        gl = add_cyl(GLAND_R, GLAND_L, 12, (x, 0, -HEIGHT/2 - GLAND_L/2))
        bool_op(box, gl, 'UNION')

    # 7) Ventilation fan grille (right side, +X)
    grille = add_cube(WALL * 2, FAN_W, FAN_H,
                       (WIDTH/2 + WALL, 0, HEIGHT/4))
    bool_op(box, grille, 'UNION')
    # Grille bars (horizontal slats)
    for j in range(4):
        z_off = HEIGHT/4 - FAN_H/2 + FAN_H * (j + 0.5) / 4
        bar = add_cube(WALL * 3, FAN_W * 0.9, 0.004,
                        (WIDTH/2 + WALL, 0, z_off))
        bool_op(box, bar, 'UNION')

    # 8) Conduit entry stubs (2 on top)
    for x_off in [-WIDTH/4, WIDTH/4]:
        cond = add_cyl(CONDUIT_R, CONDUIT_L, 12,
                        (x_off, 0, HEIGHT/2 + CONDUIT_L/2))
        bool_op(box, cond, 'UNION')

    # 9) DIN rail mounting brackets on back (-Y)
    for z_off in [-HEIGHT/4, HEIGHT/4]:
        bracket = add_cube(MOUNT_W, MOUNT_D, MOUNT_H,
                            (0, -DEPTH/2 - MOUNT_D/2, z_off))
        bool_op(box, bracket, 'UNION')

    # 10) Nameplate (small raised rectangle on door)
    nameplate = add_cube(0.10, DOOR_D * 0.5, 0.03,
                          (0, DEPTH/2 + DOOR_D + DOOR_D * 0.2, -HEIGHT/4))
    bool_op(box, nameplate, 'UNION')

    box.name = f"{PRODUCT}_{COMPONENT}"
    box.data.name = f"{PRODUCT}_{COMPONENT}_mesh"
    return box

def polish(obj):
    bpy.context.view_layer.objects.active = obj
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
    f = len(bm.faces); q = sum(1 for face in bm.faces if len(face.verts) == 4)
    nm = sum(1 for e in bm.edges if not e.is_manifold)
    print(f"\n  MESH: {obj.name}  |  V:{len(bm.verts)} E:{len(bm.edges)} F:{f}")
    print(f"  Quads: {q}/{f} ({100*q/max(f,1):.0f}%)  |  Non-manifold: {nm}  |  Watertight: {'YES' if nm==0 else 'NO'}")
    bm.free()

def export(obj):
    os.makedirs(OUT_DIR, exist_ok=True)
    path = os.path.join(OUT_DIR, OUT_FILE)
    bpy.ops.object.select_all(action='DESELECT')
    obj.select_set(True); bpy.context.view_layer.objects.active = obj
    bpy.ops.export_scene.gltf(
        filepath=path, export_format='GLB', use_selection=True,
        export_apply=True, export_normals=True, export_materials='EXPORT',
        export_cameras=False, export_lights=False,
        export_animations=False, export_yup=True,
        export_draco_mesh_compression_enable=True,
        export_draco_mesh_compression_level=6)
    print(f"  EXPORTED: {path} ({os.path.getsize(path)/1024:.1f} KB)\n")

def main():
    clean_scene(); setup_scene()
    mat = create_material()
    obj = create_geometry()
    obj.data.materials.append(mat)
    polish(obj); verify(obj); export(obj)
    print(f"DONE: {PRODUCT}_{COMPONENT}")

if __name__ == "__main__":
    main()
