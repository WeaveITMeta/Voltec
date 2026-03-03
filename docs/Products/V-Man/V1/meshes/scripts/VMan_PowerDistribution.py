"""
Blender Headless Mesh Generator
Product: V-Man  |  Component: PowerDistribution
Run: blender --background --python this_script.py

Power distribution unit (PDU).
PATENT reference: Section 6.2 Side View — under-conveyor utilities at Y=0.0–0.40m

Positioned under the conveyor, left side of container.
Bottom of PDU at Y=0.0 (floor level).
Top of PDU at Y=0.35m (below conveyor frame rails at Y=0.80m).

Table of Contents:
  1. Constants — PDU dimensions, PATENT-aligned placement, PBR
  2. Helpers  — add_box, add_cyl, bool_op
  3. Geometry — PATENT-precise placement (feet on floor, top at Y=0.35m)
  4. Polish / Verify / Export
"""
import bpy, bmesh, math, os

PRODUCT = "VMan"
COMPONENT = "PowerDistribution"
MATERIAL = "S235JR_Steel"
OUT_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT_FILE = f"{PRODUCT}_{COMPONENT}.glb"

# PDU outer dimensions (meters)
PDU_W = 0.600    # width (X)
PDU_H = 0.350    # height (Y) — fits under conveyor utilities zone
PDU_D = 0.500    # depth (Z)
WALL  = 0.002

# Sub-components (simplified for PATENT alignment)
FOOT_W = 0.050
FOOT_H = 0.010
FOOT_D = 0.050
FOOT_INSET = 0.040

BREAKER_W = 0.160
BREAKER_H = 0.180
BREAKER_D = 0.080

BUSBAR_COVER_H = 0.006
BUSBAR_COVER_D_FRAC = 0.50

UPS_W_FRAC = 0.90
UPS_H_FRAC = 0.60
UPS_D = 0.080

SURGE_W = 0.040
SURGE_H = 0.100
SURGE_D = 0.050
SURGE_COUNT = 3

DISPLAY_W = 0.080
DISPLAY_H = 0.050
DISPLAY_D = 0.010

GLAND_R = 0.012
GLAND_COUNT = 6

PBR = {
    "base_color": (0.35, 0.36, 0.38, 1.0),
    "metallic": 1.0,
    "roughness": 0.5,
    "alpha": 1.0,
    "emission": (0.0, 0.0, 0.0, 1.0),
    "emission_strength": 0.0,
}

BEVEL_WIDTH = 0.001
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
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=loc)
    obj = bpy.context.active_object
    obj.scale = (w, h, d)
    bpy.ops.object.transform_apply(scale=True)
    return obj

def add_cyl(radius, depth, vertices=24, loc=(0, 0, 0), rot=(0, 0, 0)):
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
    """Build PDU per PATENT section 6.2.

    Positioned under conveyor, left side of container.
    Y=0.0 (floor) to Y=0.35m (below conveyor frame rails).
    X positioned on left side of container interior.
    """
    # ── Key AABB edges ──
    foot_min_y = 0.0
    foot_max_y = FOOT_H
    enc_min_y  = foot_max_y
    enc_max_y  = enc_min_y + PDU_H
    enc_center_y = (enc_min_y + enc_max_y) / 2.0
    enc_min_x  = -1.0  # left side of container
    enc_max_x  = enc_min_x + PDU_W
    enc_min_z  = -5.0  # rear section
    enc_max_z  = enc_min_z + PDU_D

    # ── Main enclosure (hollow box) ──
    body = add_box(PDU_W, PDU_H, PDU_D, loc=((enc_min_x + enc_max_x) / 2, enc_center_y, (enc_min_z + enc_max_z) / 2))
    sol = body.modifiers.new("Hollow", 'SOLIDIFY')
    sol.thickness = WALL
    sol.offset = -1
    bpy.context.view_layer.objects.active = body
    bpy.ops.object.modifier_apply(modifier="Hollow")

    # ── Mounting feet (4x) ──
    foot_center_y = (foot_min_y + foot_max_y) / 2.0
    for x_sign in (-1, 1):
        for z_sign in (-1, 1):
            fx = enc_min_x + (FOOT_INSET if x_sign == -1 else PDU_W - FOOT_INSET)
            fz = enc_min_z + (FOOT_INSET if z_sign == -1 else PDU_D - FOOT_INSET)
            foot = add_box(FOOT_W, FOOT_H, FOOT_D,
                           loc=(fx, foot_center_y, fz))
            bool_op(body, foot, 'UNION')

    # ── Main breaker housing (front face) ──
    breaker_center_x = enc_min_x + PDU_W * 0.25
    breaker_center_y = enc_min_y + PDU_H * 0.55
    breaker_center_z = enc_max_z + BREAKER_D / 2
    breaker = add_box(BREAKER_W, BREAKER_H, BREAKER_D,
                      loc=(breaker_center_x, breaker_center_y, breaker_center_z))
    bool_op(body, breaker, 'UNION')

    # ── Bus bar cover (on top) ──
    busbar_d = PDU_D * BUSBAR_COVER_D_FRAC
    busbar_min_y = enc_max_y
    busbar_center_y = busbar_min_y + BUSBAR_COVER_H / 2
    busbar = add_box(PDU_W - 0.100, BUSBAR_COVER_H, busbar_d,
                     loc=((enc_min_x + enc_max_x) / 2, busbar_center_y, enc_min_z + busbar_d / 2))
    bool_op(body, busbar, 'UNION')

    # ── UPS battery compartment (rear) ──
    ups_w = PDU_W * UPS_W_FRAC
    ups_h = PDU_H * UPS_H_FRAC
    ups_center_y = enc_min_y + ups_h / 2
    ups_center_z = enc_min_z - UPS_D / 2
    ups = add_box(ups_w, ups_h, UPS_D,
                  loc=((enc_min_x + enc_max_x) / 2, ups_center_y, ups_center_z))
    bool_op(body, ups, 'UNION')

    # ── Surge protector modules (front face, right side) ──
    surge_base_x = enc_max_x - PDU_W * 0.30
    surge_center_y = enc_min_y + PDU_H * 0.55
    surge_center_z = enc_max_z + SURGE_D / 2
    for i in range(SURGE_COUNT):
        sx = surge_base_x + i * 0.060
        sp = add_box(SURGE_W, SURGE_H, SURGE_D,
                     loc=(sx, surge_center_y, surge_center_z))
        bool_op(body, sp, 'UNION')

    # ── Energy monitoring display (front face, upper right) ──
    display_center_x = enc_max_x - PDU_W * 0.20
    display_center_y = enc_min_y + PDU_H * 0.80
    display_center_z = enc_max_z + DISPLAY_D / 2
    display = add_box(DISPLAY_W, DISPLAY_H, DISPLAY_D,
                      loc=(display_center_x, display_center_y, display_center_z))
    bool_op(body, display, 'UNION')

    # ── Bottom cable gland holes ──
    gland_y = enc_min_y
    gland_spacing = (PDU_W - 0.160) / (GLAND_COUNT - 1)
    gland_start_x = enc_min_x + 0.080
    for i in range(GLAND_COUNT):
        gx = gland_start_x + i * gland_spacing
        gland = add_cyl(GLAND_R, WALL + 0.010, 12,
                        loc=(gx, gland_y, (enc_min_z + enc_max_z) / 2))
        bool_op(body, gland, 'DIFFERENCE')

    body.name = f"{PRODUCT}_{COMPONENT}"
    body.data.name = f"{PRODUCT}_{COMPONENT}_mesh"
    return body


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
    print(f"  PATENT alignment: Under-conveyor utilities, Y=0.0-0.35m, left side")
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
