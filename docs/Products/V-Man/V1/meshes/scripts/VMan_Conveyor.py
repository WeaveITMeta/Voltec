"""
Blender Headless Mesh Generator
Product: V-Man  |  Component: Conveyor
Run: blender --background --python this_script.py

Precision belt/roller conveyor module.
PATENT reference: Section 6.2 Side View — conveyor at 0.85m height

The conveyor is the central reference point for the U-cell layout.
Belt surface center at Y=0.85m (from PATENT).
Legs extend downward to Y=0.0 (floor level).
Sensor brackets extend upward to Y=1.25m (above belt).

Table of Contents:
  1. Constants — conveyor dims, PATENT-aligned heights, PBR
  2. Helpers  — add_box, add_cyl, bool_op
  3. Geometry — PATENT-precise placement (belt at Y=0.85m)
  4. Polish / Verify / Export
"""
import bpy, bmesh, math, os

PRODUCT = "VMan"
COMPONENT = "Conveyor"
MATERIAL = "S355J2_Steel"
OUT_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT_FILE = f"{PRODUCT}_{COMPONENT}.glb"

# Conveyor dimensions (meters)
CONV_LENGTH     = 10.000   # total length (Z)
CONV_WIDTH      = 0.600    # belt width (X)
BELT_HEIGHT     = 0.85     # center of belt surface (Y) — from PATENT 6.2
FRAME_SECTION   = 0.040    # frame rail cross-section (square)
BELT_THICKNESS  = 0.003    # belt surface thickness (Y)
ROLLER_RADIUS   = 0.040    # drive/idler roller radius
LEG_SECTION     = 0.050    # leg cross-section (square)
FOOT_W          = 0.080    # foot pad width
FOOT_H          = 0.010    # foot pad height
BRACE_SECTION   = 0.030    # cross-brace cross-section
GUIDE_W         = 0.010    # guide rail width (X)
GUIDE_H         = 0.040    # guide rail height (Y)
SENSOR_W        = 0.016    # sensor bracket square
SENSOR_H        = 0.060    # sensor bracket height (Y)
LEG_COUNT       = 4        # legs per side
SENSOR_COUNT    = 6        # sensors per side

PBR = {
    "base_color": (0.55, 0.56, 0.58, 1.0),
    "metallic": 1.0,
    "roughness": 0.40,
    "alpha": 1.0,
    "emission": (0.0, 0.0, 0.0, 1.0),
    "emission_strength": 0.0,
}

BEVEL_WIDTH = 0.002
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
    """Build conveyor per PATENT section 6.2.

    Belt surface center at Y=0.85m (from PATENT).
    Legs extend from Y=0.0 (floor) to frame rails.
    Frame rails at Y=0.80m (below belt center).
    Sensor brackets extend upward from frame rails.

    Layout:
        Y=0.0:      Floor level
        Y=0.01:     Foot pads
        Y=0.01-0.80: Legs
        Y=0.80:     Frame rails (left/right)
        Y=0.85:     Belt surface center
        Y=0.88:     Top of belt
        Y=0.88-1.25: Sensor brackets (extending upward)
    """
    # ── Key AABB edges ──
    foot_min_y   = 0.0
    foot_max_y   = FOOT_H
    leg_min_y    = foot_max_y
    leg_max_y    = BELT_HEIGHT - FRAME_SECTION / 2  # frame rails sit below belt center
    leg_height   = leg_max_y - leg_min_y
    frame_min_y  = leg_max_y
    frame_max_y  = frame_min_y + FRAME_SECTION
    frame_center_y = (frame_min_y + frame_max_y) / 2.0
    belt_min_y   = BELT_HEIGHT - BELT_THICKNESS / 2
    belt_max_y   = BELT_HEIGHT + BELT_THICKNESS / 2
    belt_center_y = BELT_HEIGHT
    guide_min_y  = belt_max_y
    guide_max_y  = guide_min_y + GUIDE_H
    guide_center_y = (guide_min_y + guide_max_y) / 2.0

    conv_min_z = -CONV_LENGTH / 2
    conv_max_z =  CONV_LENGTH / 2

    # Frame rail X positions: outside the belt width
    rail_left_center_x  = -(CONV_WIDTH / 2 + FRAME_SECTION / 2)
    rail_right_center_x =  (CONV_WIDTH / 2 + FRAME_SECTION / 2)

    # ── Left frame rail (first body) ──
    body = add_box(FRAME_SECTION, FRAME_SECTION, CONV_LENGTH,
                   loc=(rail_left_center_x, frame_center_y, 0))

    # ── Right frame rail ──
    rail_r = add_box(FRAME_SECTION, FRAME_SECTION, CONV_LENGTH,
                     loc=(rail_right_center_x, frame_center_y, 0))
    bool_op(body, rail_r, 'UNION')

    # ── Legs (LEG_COUNT per side) ──
    leg_center_y = (leg_min_y + leg_max_y) / 2.0
    leg_margin = 1.0
    leg_z_start = conv_min_z + leg_margin
    leg_z_step = (CONV_LENGTH - 2 * leg_margin) / (LEG_COUNT - 1) if LEG_COUNT > 1 else 0
    for x_center in (rail_left_center_x, rail_right_center_x):
        for i in range(LEG_COUNT):
            z_pos = leg_z_start + i * leg_z_step
            leg = add_box(LEG_SECTION, leg_height, LEG_SECTION,
                          loc=(x_center, leg_center_y, z_pos))
            bool_op(body, leg, 'UNION')

            # Foot pad: flush below leg bottom
            foot_center_y = (foot_min_y + foot_max_y) / 2.0
            foot = add_box(FOOT_W, FOOT_H, FOOT_W,
                           loc=(x_center, foot_center_y, z_pos))
            bool_op(body, foot, 'UNION')

    # ── Cross braces (connecting left and right legs) ──
    brace_center_y = leg_min_y + leg_height * 0.25
    brace_w = CONV_WIDTH + FRAME_SECTION * 2
    for i in range(LEG_COUNT):
        z_pos = leg_z_start + i * leg_z_step
        brace = add_box(brace_w, BRACE_SECTION, BRACE_SECTION,
                        loc=(0, brace_center_y, z_pos))
        bool_op(body, brace, 'UNION')

    # ── Belt surface ──
    belt_length = CONV_LENGTH - 2 * ROLLER_RADIUS
    belt = add_box(CONV_WIDTH, BELT_THICKNESS, belt_length,
                   loc=(0, belt_center_y, 0))
    bool_op(body, belt, 'UNION')

    # ── Drive roller (output end, +Z) ──
    roller_center_z = conv_max_z - ROLLER_RADIUS
    roller_length = CONV_WIDTH + FRAME_SECTION * 2
    drive = add_cyl(ROLLER_RADIUS, roller_length, 24,
                    loc=(0, frame_center_y, roller_center_z),
                    rot=(0, 0, math.pi / 2))
    bool_op(body, drive, 'UNION')

    # ── Idler roller (input end, -Z) ──
    idler_center_z = conv_min_z + ROLLER_RADIUS
    idler = add_cyl(ROLLER_RADIUS * 0.9, roller_length, 24,
                    loc=(0, frame_center_y, idler_center_z),
                    rot=(0, 0, math.pi / 2))
    bool_op(body, idler, 'UNION')

    # ── Guide rails (on top of belt, near belt edges) ──
    guide_inset = 0.005
    guide_left_x  = -(CONV_WIDTH / 2 - guide_inset - GUIDE_W / 2)
    guide_right_x =  (CONV_WIDTH / 2 - guide_inset - GUIDE_W / 2)
    guide_length = CONV_LENGTH - 0.200
    for gx in (guide_left_x, guide_right_x):
        guide = add_box(GUIDE_W, GUIDE_H, guide_length,
                        loc=(gx, guide_center_y, 0))
        bool_op(body, guide, 'UNION')

    # ── Sensor brackets (SENSOR_COUNT per side, mounted on outer face of frame rail) ──
    sensor_center_y = guide_max_y + SENSOR_H / 2
    sensor_z_start = conv_min_z + 1.5
    sensor_z_step = (CONV_LENGTH - 3.0) / (SENSOR_COUNT - 1) if SENSOR_COUNT > 1 else 0
    for x_sign in (-1, 1):
        sensor_x = x_sign * (CONV_WIDTH / 2 + FRAME_SECTION + SENSOR_W / 2)
        for i in range(SENSOR_COUNT):
            sz = sensor_z_start + i * sensor_z_step
            bracket = add_box(SENSOR_W, SENSOR_H, SENSOR_W,
                              loc=(sensor_x, sensor_center_y, sz))
            bool_op(body, bracket, 'UNION')

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
    print(f"  AABB size: ({max(xs)-min(xs):.4f}, {max(ys)-min(ys):.4f}, {max(zs)-min(zs):.4f})")
    print(f"  PATENT alignment: Belt at Y=0.85m, frame rails Y=0.80m, sensors Y=0.88-1.25m")
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
