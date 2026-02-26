"""
V-Incinerator — Outer Housing  (Blender 4.4 headless)
=====================================================
316L Stainless Steel modular industrial enclosure.
6.0 m (L) × 3.0 m (W) × 4.0 m (H). Ships in 2 ISO containers.
Reinforced corner posts, panel seam lines (loop cuts),
ventilation louvers, access doors, lifting lugs at corners.

Run: blender --background --python this_script.py
"""
import bpy, bmesh, math, os

PRODUCT   = "VIncinerator"
COMPONENT = "Housing"
MATERIAL  = "316L_SS"
OUT_DIR   = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT_FILE  = f"{PRODUCT}_{COMPONENT}.glb"

# ── Dimensions (meters, from PATENT.md) ───────────────────────────────
LEN    = 6.0
WID    = 3.0
HGT    = 4.0
WALL   = 0.008       # 8 mm sheet
POST_W = 0.12        # corner post width
POST_D = 0.12
LUG_R  = 0.04        # lifting lug ring radius
LUG_T  = 0.015
LOUVER_W = 0.60
LOUVER_H = 0.30
LOUVER_D = 0.015
DOOR_W = 1.0
DOOR_H = 2.2
DOOR_D = 0.010

PBR = {
    "base_color": (0.55, 0.56, 0.58, 1.0),  # brushed 316L
    "metallic": 1.0,
    "roughness": 0.35,
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

def add_cyl(r, d, v=32, loc=(0,0,0), rot=(0,0,0)):
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
    """Modular industrial housing with corner posts, doors, louvers, lifting lugs."""

    # 1) Main shell — hollow box
    box = add_cube(LEN, WID, HGT)
    sol = box.modifiers.new("Hollow", 'SOLIDIFY')
    sol.thickness = WALL; sol.offset = -1
    bpy.context.view_layer.objects.active = box
    bpy.ops.object.modifier_apply(modifier="Hollow")

    # 2) Add panel seam lines via loop cuts (edit mode)
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.mesh.select_all(action='SELECT')
    # Horizontal seams
    bpy.ops.mesh.loopcut_slide(MESH_OT_loopcut={"number_cuts": 3, "smoothness": 0},
                                TRANSFORM_OT_edge_slide={"value": 0})
    bpy.ops.object.mode_set(mode='OBJECT')

    # 3) Corner reinforcement posts (8 vertical posts at corners)
    corners = [
        ( LEN/2 - POST_W/2,  WID/2 - POST_D/2),
        ( LEN/2 - POST_W/2, -WID/2 + POST_D/2),
        (-LEN/2 + POST_W/2,  WID/2 - POST_D/2),
        (-LEN/2 + POST_W/2, -WID/2 + POST_D/2),
    ]
    for cx, cy in corners:
        post = add_cube(POST_W, POST_D, HGT, (cx, cy, 0))
        bool_op(box, post, 'UNION')

    # 4) Lifting lugs at top corners (4 torus-like rings)
    for cx, cy in corners:
        lug = add_cyl(LUG_R, LUG_T, 16, (cx, cy, HGT/2 + LUG_T/2))
        # Hole in center
        lug_hole = add_cyl(LUG_R * 0.5, LUG_T + 0.01, 16, (cx, cy, HGT/2 + LUG_T/2))
        bool_op(lug, lug_hole, 'DIFFERENCE')
        bool_op(box, lug, 'UNION')

    # 5) Access door (front face, +Y side)
    door_frame = add_cube(DOOR_W + 0.04, DOOR_D, DOOR_H + 0.04,
                          (0, WID/2, -HGT/2 + DOOR_H/2 + 0.10))
    bool_op(box, door_frame, 'UNION')
    # Door panel (slightly recessed)
    door = add_cube(DOOR_W, DOOR_D * 0.5, DOOR_H,
                    (0, WID/2 + DOOR_D * 0.3, -HGT/2 + DOOR_H/2 + 0.10))
    bool_op(box, door, 'UNION')

    # 6) Ventilation louvers (2 per long side)
    for side_y in [WID/2, -WID/2]:
        for x_off in [-LEN/4, LEN/4]:
            louver = add_cube(LOUVER_W, LOUVER_D, LOUVER_H,
                              (x_off, side_y, HGT/2 - 0.50))
            bool_op(box, louver, 'UNION')

    # 7) Roof penetration opening (for exhaust stack passage)
    roof_collar = add_cyl(0.25, 0.03, 32, (LEN/4, 0, HGT/2 + 0.015))
    bool_op(box, roof_collar, 'UNION')

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
