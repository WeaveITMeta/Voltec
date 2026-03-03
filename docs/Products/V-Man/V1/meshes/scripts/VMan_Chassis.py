"""
Blender Headless Mesh Generator
Product: V-Man  |  Component: Chassis
Run: blender --background --python this_script.py

ISO 40-foot high-cube shipping container chassis.
PATENT reference: Section 6.2 Side View (Cross-Section)

External dimensions: 12.192m (L) × 2.438m (W) × 2.896m (H)
Internal working space: 12.0m (L) × 2.2m (W) × 2.69m (H)

Layout (from PATENT):
  - Overhead cable tray (EtherCAT) at top
  - Arm reach envelope: 4 arms mounted on pedestals, 1.3m reach
  - Conveyor at 0.85m height (center of belt surface)
  - Under-conveyor utilities: PDU, compressor, UPS, GPU
  - Vibration damping mounts at base

Table of Contents:
  1. Constants — ISO 40' HC dimensions, wall thickness, PBR
  2. Helpers  — add_box, add_cyl, bool_op
  3. Geometry — PATENT-aligned placement (external shell + internal structure)
  4. Polish / Verify / Export
"""
import bpy, bmesh, math, os

PRODUCT = "VMan"
COMPONENT = "Chassis"
MATERIAL = "S355J2_Steel"
OUT_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT_FILE = f"{PRODUCT}_{COMPONENT}.glb"

# ISO 40' HC external dimensions (meters) — from PATENT 6.2
LENGTH_EXT = 12.192
WIDTH_EXT  = 2.438
HEIGHT_EXT = 2.896

# Internal working dimensions (from PATENT)
LENGTH_INT = 12.0
WIDTH_INT  = 2.2
HEIGHT_INT = 2.69

# Wall thickness (corten steel)
WALL = 0.002

# Key heights from PATENT side view
CONVEYOR_HEIGHT = 0.85      # center of belt surface
UTILITIES_HEIGHT = 0.35     # under-conveyor utilities (PDU, compressor, UPS, GPU)
VIBRATION_MOUNTS_H = 0.05   # base isolation pads

# Corner castings (ISO 1161)
CORNER_CASTING = 0.178

# Structural elements
FLOOR_THICKNESS = 0.005
CROSS_MEMBER_SECTION = 0.040

PBR = {
    "base_color": (0.55, 0.56, 0.58, 1.0),
    "metallic": 1.0,
    "roughness": 0.45,
    "alpha": 1.0,
    "emission": (0.0, 0.0, 0.0, 1.0),
    "emission_strength": 0.0,
}

BEVEL_WIDTH = 0.003
BEVEL_SEGMENTS = 2


def clean_scene():
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete(use_global=False)
    for block in bpy.data.meshes:
        if block.users == 0:
            bpy.data.meshes.remove(block)
    for block in bpy.data.materials:
        if block.users == 0:
            bpy.data.materials.remove(block)

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

def add_box(w, h, d, loc=(0, 0, 0)):
    """Create box with FULL dimensions w×h×d centered at loc."""
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=loc)
    obj = bpy.context.active_object
    obj.scale = (w, h, d)
    bpy.ops.object.transform_apply(scale=True)
    return obj

def add_cyl(radius, depth, vertices=32, loc=(0, 0, 0), rot=(0, 0, 0)):
    bpy.ops.mesh.primitive_cylinder_add(
        vertices=vertices, radius=radius, depth=depth,
        location=loc, rotation=rot,
    )
    return bpy.context.active_object

def bool_op(target, cutter, operation='UNION'):
    mod = target.modifiers.new(operation, 'BOOLEAN')
    mod.operation = operation
    mod.object = cutter
    mod.solver = 'EXACT'
    bpy.context.view_layer.objects.active = target
    bpy.ops.object.modifier_apply(modifier=operation)
    bpy.data.objects.remove(cutter, do_unlink=True)


def create_geometry():
    """Build ISO 40' HC container chassis per PATENT section 6.2.

    Coordinate system (Y-up, centered at container centroid):
        X: width   (-WIDTH_EXT/2  .. +WIDTH_EXT/2)
        Y: height  (0 .. HEIGHT_EXT)  [vibration mounts at Y=0]
        Z: length  (-LENGTH_EXT/2 .. +LENGTH_EXT/2)

    Key heights (from PATENT side view):
        Y=0.00 .. 0.05:  Vibration damping mounts
        Y=0.05 .. 0.40:  Under-conveyor utilities (PDU, compressor, UPS, GPU)
        Y=0.40 .. 1.25:  Conveyor belt surface at Y=0.85
        Y=1.25 .. 2.69:  Arm reach envelope + overhead cable tray
    """
    # ── Outer shell AABB ──
    outer_min_x = -WIDTH_EXT / 2
    outer_max_x =  WIDTH_EXT / 2
    outer_min_y = VIBRATION_MOUNTS_H  # shell sits on vibration mounts
    outer_max_y = outer_min_y + HEIGHT_INT
    outer_min_z = -LENGTH_EXT / 2
    outer_max_z =  LENGTH_EXT / 2

    # Main container box — hollow shell via solidify
    outer_center_y = (outer_min_y + outer_max_y) / 2.0
    outer = add_box(WIDTH_EXT, HEIGHT_INT, LENGTH_EXT,
                    loc=(0, outer_center_y, 0))
    sol = outer.modifiers.new("Hollow", 'SOLIDIFY')
    sol.thickness = WALL
    sol.offset = -1  # solidify inward
    bpy.context.view_layer.objects.active = outer
    bpy.ops.object.modifier_apply(modifier="Hollow")

    # ── Floor plate (inside bottom of shell) ──
    floor_min_y = outer_min_y + WALL
    floor_max_y = floor_min_y + FLOOR_THICKNESS
    floor_center_y = (floor_min_y + floor_max_y) / 2.0
    floor_w = WIDTH_EXT - 2 * WALL
    floor_d = LENGTH_EXT - 2 * WALL
    floor = add_box(floor_w, FLOOR_THICKNESS, floor_d,
                    loc=(0, floor_center_y, 0))
    bool_op(outer, floor, 'UNION')

    # ── Corner castings (8 corners, ISO 1161) ──
    cc = CORNER_CASTING
    for x_sign in (-1, 1):
        for y_sign in (-1, 1):
            for z_sign in (-1, 1):
                # Casting center: outer face flush with container edge
                cx = x_sign * (WIDTH_EXT / 2 - cc / 2)
                cy_base = outer_min_y if y_sign == -1 else outer_max_y
                cy = cy_base + y_sign * (cc / 2)
                cz = z_sign * (LENGTH_EXT / 2 - cc / 2)
                casting = add_box(cc, cc, cc, loc=(cx, cy, cz))
                bool_op(outer, casting, 'UNION')

    # ── Vibration damping mounts (4 corners at base) ──
    mount_h = VIBRATION_MOUNTS_H
    mount_w = 0.200
    mount_d = 0.200
    mount_center_y = mount_h / 2
    mount_inset_x = WIDTH_EXT / 2 - mount_w / 2 - 0.050
    mount_inset_z = LENGTH_EXT / 2 - mount_d / 2 - 0.050
    for x_sign in (-1, 1):
        for z_sign in (-1, 1):
            mx = x_sign * mount_inset_x
            mz = z_sign * mount_inset_z
            mount = add_box(mount_w, mount_h, mount_d,
                            loc=(mx, mount_center_y, mz))
            bool_op(outer, mount, 'UNION')

    # ── Structural cross-members (under conveyor, for utilities support) ──
    # 5 longitudinal beams along the length, supporting utilities
    utilities_top_y = UTILITIES_HEIGHT
    beam_h = 0.060
    beam_center_y = utilities_top_y - beam_h / 2
    beam_w = WIDTH_EXT - 0.100
    beam_d = CROSS_MEMBER_SECTION
    for i in range(5):
        z_pos = outer_min_z + 1.5 + i * ((LENGTH_EXT - 3.0) / 4.0)
        beam = add_box(beam_w, beam_h, beam_d,
                       loc=(0, beam_center_y, z_pos))
        bool_op(outer, beam, 'UNION')

    # ── Overhead cable tray (top interior, for EtherCAT) ──
    tray_h = 0.040
    tray_w = WIDTH_EXT - 0.150
    tray_d = LENGTH_EXT - 0.300
    tray_top_y = outer_max_y - 0.100
    tray_center_y = tray_top_y - tray_h / 2
    tray = add_box(tray_w, tray_h, tray_d,
                   loc=(0, tray_center_y, 0))
    bool_op(outer, tray, 'UNION')

    # ── Fork pockets (2x, bottom face for container handling) ──
    pocket_w = 0.160
    pocket_h = 0.120
    pocket_d = 0.400
    pocket_center_y = outer_min_y
    for x_offset in (-0.6, 0.6):
        pocket = add_box(pocket_w, pocket_h, pocket_d,
                         loc=(x_offset, pocket_center_y, outer_min_z + 1.0))
        bool_op(outer, pocket, 'DIFFERENCE')

    # ── Ventilation grille cutouts (4x: 2 intake left, 2 exhaust right) ──
    grille_w = WALL * 4
    grille_h = 0.300
    grille_d = 0.600
    grille_top_y = outer_max_y - 0.100
    grille_center_y = grille_top_y - grille_h / 2
    # Left side intakes
    for z_pos in (-3.0, -1.0):
        grille = add_box(grille_w, grille_h, grille_d,
                         loc=(outer_min_x, grille_center_y, z_pos))
        bool_op(outer, grille, 'DIFFERENCE')
    # Right side exhausts
    for z_pos in (1.0, 3.0):
        grille = add_box(grille_w, grille_h, grille_d,
                         loc=(outer_max_x, grille_center_y, z_pos))
        bool_op(outer, grille, 'DIFFERENCE')

    # ── Cable gland holes (4x through floor, for external connections) ──
    gland_r = 0.040
    gland_depth = FLOOR_THICKNESS + WALL * 2 + 0.010
    gland_center_y = outer_min_y
    for z_pos in (-4.0, -2.0, 2.0, 4.0):
        gland = add_cyl(gland_r, gland_depth, 16,
                        loc=(0.0, gland_center_y, z_pos))
        bool_op(outer, gland, 'DIFFERENCE')

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
    verts = len(bm.verts)
    edges = len(bm.edges)
    faces = len(bm.faces)
    quads = sum(1 for f in bm.faces if len(f.verts) == 4)
    non_manifold = sum(1 for e in bm.edges if not e.is_manifold)
    xs = [v.co.x for v in bm.verts]
    ys = [v.co.y for v in bm.verts]
    zs = [v.co.z for v in bm.verts]
    print(f"\n  MESH: {obj.name}")
    print(f"  Verts: {verts}  Edges: {edges}  Faces: {faces}")
    print(f"  Quads: {quads}/{faces} ({100 * quads / max(faces, 1):.0f}%)")
    print(f"  Non-manifold edges: {non_manifold}  Watertight: {'YES' if non_manifold == 0 else 'FIX'}")
    print(f"  AABB min: ({min(xs):.4f}, {min(ys):.4f}, {min(zs):.4f})")
    print(f"  AABB max: ({max(xs):.4f}, {max(ys):.4f}, {max(zs):.4f})")
    print(f"  AABB size: ({max(xs)-min(xs):.4f}, {max(ys)-min(ys):.4f}, {max(zs)-min(zs):.4f})")
    print(f"  PATENT alignment: Conveyor at Y=0.85m, utilities Y=0.0-0.40m, arms Y=0.40-2.69m")
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
    print(f"  EXPORTED: {path} ({os.path.getsize(path) / 1024:.1f} KB)\n")

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
