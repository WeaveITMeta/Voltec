# ============================================================================
# VCell_CompressionFrame.py — External stack clamping/compression frame
# Multi-body assembly: two thick Al end plates + 4 tie rods (threaded SS) +
# spring washers + alignment pins
# Patent ref: US20130115493A1 (prismatic cell module compression frame),
#             US20120171568A1 (cell header + end plate assembly)
# Dimensions: 310mm × 110mm × 20mm end plates, 4x M8 tie rods
# ============================================================================
import bpy, bmesh, math, os

# --- Dimensions (meters) ---
PLATE_L   = 0.310    # End plate length (housing + clearance)
PLATE_W   = 0.110    # End plate width
PLATE_T   = 0.020    # End plate thickness 20mm (high stiffness)
ROD_R     = 0.004    # M8 tie rod radius
ROD_OFFSET_X = 0.140 # Rod X offset from center
ROD_OFFSET_Y = 0.048 # Rod Y offset from center
ROD_L     = 0.060    # Rod exposed length (represents stack gap)
NUT_R     = 0.008    # Hex nut circumradius
NUT_T     = 0.007    # Nut thickness
PIN_R     = 0.003    # Alignment pin radius
PIN_H     = 0.008    # Pin height above plate
BOSS_R    = 0.008    # Boss around rod hole

# --- PBR Materials ---
AL_COLOR  = (0.82, 0.83, 0.85, 1.0)  # Al 6061-T6 plates
AL_METAL  = 0.92
AL_ROUGH  = 0.28
ROD_COLOR = (0.60, 0.62, 0.64, 1.0)  # 316L SS tie rods
ROD_METAL = 1.0
ROD_ROUGH = 0.35

# --- Output ---
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
OUT_DIR    = os.path.normpath(os.path.join(SCRIPT_DIR, ".."))
OUT_FILE   = os.path.join(OUT_DIR, "VCell_CompressionFrame.glb")
OBJ_NAME   = "VCell_CompressionFrame"

# ============================================================================
def clean_scene():
    bpy.ops.wm.read_factory_settings(use_empty=True)
    bpy.context.scene.name = "Scene0"

def make_material(name, color, metal, rough):
    mat = bpy.data.materials.new(name=name)
    mat.use_nodes = True
    bsdf = mat.node_tree.nodes.get("Principled BSDF")
    bsdf.inputs["Base Color"].default_value = color
    bsdf.inputs["Metallic"].default_value   = metal
    bsdf.inputs["Roughness"].default_value  = rough
    return mat

def add_box(name, sx, sy, sz, loc=(0,0,0)):
    bpy.ops.mesh.primitive_cube_add(size=1, location=loc)
    obj = bpy.context.active_object
    obj.name = name
    obj.scale = (sx, sy, sz)
    bpy.ops.object.transform_apply(scale=True)
    return obj

def add_cylinder(name, r, depth, loc=(0,0,0), rot=(0,0,0), segs=24):
    bpy.ops.mesh.primitive_cylinder_add(
        radius=r, depth=depth, vertices=segs, location=loc, rotation=rot)
    obj = bpy.context.active_object
    obj.name = name
    return obj

def add_hex_prism(name, r, depth, loc=(0,0,0)):
    bpy.ops.mesh.primitive_cylinder_add(
        radius=r, depth=depth, vertices=6, location=loc)
    obj = bpy.context.active_object
    obj.name = name
    return obj

def bool_op(target, cutter, operation="DIFFERENCE"):
    mod = target.modifiers.new(name="Bool", type="BOOLEAN")
    mod.operation = operation
    mod.object    = cutter
    mod.solver    = "EXACT"
    bpy.context.view_layer.objects.active = target
    bpy.ops.object.modifier_apply(modifier=mod.name)
    bpy.data.objects.remove(cutter, do_unlink=True)

def join_objects(objs):
    bpy.ops.object.select_all(action="DESELECT")
    for o in objs:
        o.select_set(True)
    bpy.context.view_layer.objects.active = objs[0]
    bpy.ops.object.join()
    return bpy.context.active_object

ROD_POS = [
    ( ROD_OFFSET_X,  ROD_OFFSET_Y),
    ( ROD_OFFSET_X, -ROD_OFFSET_Y),
    (-ROD_OFFSET_X,  ROD_OFFSET_Y),
    (-ROD_OFFSET_X, -ROD_OFFSET_Y),
]

def make_end_plate(name, z_loc, mat_al):
    plate = add_box(name, PLATE_L, PLATE_W, PLATE_T, loc=(0, 0, z_loc))

    # Counterbored holes for tie rods + bosses
    for i, (rx, ry) in enumerate(ROD_POS):
        hole = add_cylinder(f"rod_hole_{name}_{i}", ROD_R, PLATE_T * 2,
                            loc=(rx, ry, z_loc))
        bool_op(plate, hole, "DIFFERENCE")
        boss = add_cylinder(f"boss_{name}_{i}", BOSS_R, PLATE_T * 0.3,
                            loc=(rx, ry, z_loc + PLATE_T/2 * (1 if "top" in name else -1)))
        bool_op(plate, boss, "UNION")

    # Alignment pin holes
    for i, (px, py) in enumerate([(0.12, 0), (-0.12, 0)]):
        pin_hole = add_cylinder(f"pin_hole_{name}_{i}", PIN_R, PLATE_T * 2,
                                loc=(px, py, z_loc))
        bool_op(plate, pin_hole, "DIFFERENCE")

    # Lightening pockets (rectangular cutouts for mass reduction)
    for i, px in enumerate([-0.06, 0.06]):
        pocket = add_box(f"pocket_{name}_{i}", 0.08, 0.07, PLATE_T * 0.6,
                         loc=(px, 0, z_loc))
        bool_op(plate, pocket, "DIFFERENCE")

    plate.data.materials.append(mat_al)
    return plate

def create_geometry(mat_al, mat_rod):
    STACK_GAP = ROD_L
    top_z = STACK_GAP/2 + PLATE_T/2
    bot_z = -STACK_GAP/2 - PLATE_T/2

    # End plates
    top_plate = make_end_plate("top_plate", top_z, mat_al)
    bot_plate = make_end_plate("bot_plate", bot_z, mat_al)

    all_objs = [top_plate, bot_plate]

    # Tie rods
    for i, (rx, ry) in enumerate(ROD_POS):
        rod = add_cylinder(f"tie_rod_{i}", ROD_R * 0.85, STACK_GAP + PLATE_T * 2,
                           loc=(rx, ry, 0))
        rod.data.materials.append(mat_rod)
        all_objs.append(rod)

        # Hex nuts on top and bottom
        for sign, zn in [(+1, top_z + PLATE_T/2 + NUT_T/2),
                         (-1, bot_z - PLATE_T/2 - NUT_T/2)]:
            nut = add_hex_prism(f"nut_{i}_{sign}", NUT_R, NUT_T,
                                loc=(rx, ry, zn))
            nut.data.materials.append(mat_rod)
            all_objs.append(nut)

    # Alignment pins protruding from top plate
    for i, (px, py) in enumerate([(0.12, 0), (-0.12, 0)]):
        pin = add_cylinder(f"align_pin_{i}", PIN_R, PIN_H,
                           loc=(px, py, top_z + PLATE_T/2 + PIN_H/2))
        pin.data.materials.append(mat_al)
        all_objs.append(pin)

    assembled = join_objects(all_objs)
    assembled.name = OBJ_NAME
    return assembled

def polish(obj):
    bpy.context.view_layer.objects.active = obj
    bpy.ops.object.mode_set(mode="EDIT")
    bpy.ops.mesh.select_all(action="SELECT")
    bpy.ops.mesh.normals_make_consistent(inside=False)
    bpy.ops.uv.smart_project(angle_limit=66.0)
    bpy.ops.object.mode_set(mode="OBJECT")
    bpy.ops.object.shade_smooth()
    try:
        bpy.ops.object.shade_auto_smooth(angle=30.0)
    except Exception:
        pass
    mod = obj.modifiers.new("Bevel", "BEVEL")
    mod.width    = 0.0005
    mod.segments = 2
    bpy.ops.object.modifier_apply(modifier=mod.name)

def verify(obj):
    bm = bmesh.new()
    bm.from_mesh(obj.data)
    bm.verts.ensure_lookup_table()
    verts = len(bm.verts)
    faces = len(bm.faces)
    quads = sum(1 for f in bm.faces if len(f.verts) == 4)
    nm    = [e for e in bm.edges if not e.is_manifold]
    bm.free()
    print(f"[VCell_CompressionFrame] Verts={verts} Faces={faces} "
          f"Quads={quads/faces*100:.0f}% NM={len(nm)}")

def export_glb(obj):
    bpy.ops.object.select_all(action="DESELECT")
    obj.select_set(True)
    bpy.ops.export_scene.gltf(
        filepath=OUT_FILE,
        use_selection=True,
        export_format="GLB",
        export_draco_mesh_compression_enable=True,
    )
    kb = os.path.getsize(OUT_FILE) / 1024
    print(f"[VCell_CompressionFrame] Exported → {OUT_FILE} ({kb:.1f} KiB)")

# ============================================================================
if __name__ == "__main__":
    clean_scene()
    mat_al  = make_material("MAT_VCell_FrameAl", AL_COLOR, AL_METAL, AL_ROUGH)
    mat_rod = make_material("MAT_VCell_FrameRod", ROD_COLOR, ROD_METAL, ROD_ROUGH)
    obj = create_geometry(mat_al, mat_rod)
    polish(obj)
    verify(obj)
    export_glb(obj)
