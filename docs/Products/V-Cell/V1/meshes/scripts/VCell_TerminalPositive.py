# ============================================================================
# VCell_TerminalPositive.py — Positive aluminum current collector terminal
# Multi-body assembly: flat rectangular terminal plate + raised bus-bar
# contact pad + bolt/weld hole + chamfered edges
# Patent ref: US20120171568A1 (prismatic cell terminal welding),
#             US20130115493A1 (positive polarity rigid container terminal)
# Material: Al 1100-H14 (high conductivity)
# ============================================================================
import bpy, bmesh, os

# --- Dimensions (meters) ---
PLATE_L  = 0.025    # Terminal plate length
PLATE_W  = 0.018    # Terminal plate width
PLATE_T  = 0.003    # Plate thickness 3mm
PAD_L    = 0.016    # Bus-bar contact pad length
PAD_W    = 0.012    # Pad width
PAD_T    = 0.0015   # Pad raised height
HOLE_R   = 0.0025   # Bolt hole radius
HOLE_OFF = 0.009    # Hole offset from center

# --- PBR Material: polished Al terminal ---
MAT_COLOR = (0.88, 0.89, 0.90, 1.0)
MAT_METAL = 1.0
MAT_ROUGH = 0.12

# --- Output ---
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
OUT_DIR    = os.path.normpath(os.path.join(SCRIPT_DIR, ".."))
OUT_FILE   = os.path.join(OUT_DIR, "VCell_TerminalPositive.glb")
OBJ_NAME   = "VCell_TerminalPositive"

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

def add_cylinder(name, r, depth, loc=(0,0,0), segs=24):
    bpy.ops.mesh.primitive_cylinder_add(
        radius=r, depth=depth, vertices=segs, location=loc)
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

def create_geometry(mat):
    # --- Base terminal plate ---
    plate = add_box("term_plate", PLATE_L, PLATE_W, PLATE_T, loc=(0, 0, 0))

    # --- Raised bus-bar contact pad ---
    pad = add_box("contact_pad", PAD_L, PAD_W, PAD_T,
                  loc=(0, 0, PLATE_T/2 + PAD_T/2))
    bool_op(plate, pad, "UNION")

    # --- Bolt hole through plate ---
    hole = add_cylinder("bolt_hole", HOLE_R, PLATE_T * 2,
                        loc=(0, HOLE_OFF, 0))
    bool_op(plate, hole, "DIFFERENCE")

    # --- Laser weld groove around base (cosmetic ridge) ---
    groove = add_box("weld_groove", PLATE_L + 0.001, 0.001, 0.0003,
                     loc=(0, PLATE_W/2, PLATE_T/2))
    bool_op(plate, groove, "DIFFERENCE")

    plate.name = OBJ_NAME
    plate.data.materials.append(mat)
    return plate

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
    mod.width    = 0.0003
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
    print(f"[VCell_TerminalPositive] Verts={verts} Faces={faces} "
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
    print(f"[VCell_TerminalPositive] Exported → {OUT_FILE} ({kb:.1f} KiB)")

# ============================================================================
if __name__ == "__main__":
    clean_scene()
    mat = make_material("MAT_VCell_TermPos", MAT_COLOR, MAT_METAL, MAT_ROUGH)
    obj = create_geometry(mat)
    polish(obj)
    verify(obj)
    export_glb(obj)
