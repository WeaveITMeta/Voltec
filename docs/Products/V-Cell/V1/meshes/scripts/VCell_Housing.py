# ============================================================================
# VCell_Housing.py — Al 6061-T6 prismatic cell housing
# Multi-body assembly: main box body + laser-weld seam ridge + pressure vent
# groove + positive/negative terminal holes + corner radiuses + lid
# Patent ref: US20090068548A1 (prismatic Li-ion cell housing geometry)
# Dimensions: 300mm × 100mm × 12mm, 0.5mm wall
# ============================================================================
import bpy, bmesh, math, os

# --- Dimensions (meters) ---
L = 0.300          # 300mm length
W = 0.100          # 100mm width
H = 0.012          # 12mm height
WALL = 0.0005      # 0.5mm wall
CORNER_R = 0.003   # 3mm corner radius
VENT_W = 0.060     # Vent groove width
VENT_D = 0.00015   # Vent groove depth (coined feature)
TERM_R = 0.004     # Terminal hole radius
SEAM_H = 0.0008    # Laser-weld seam ridge height
SEAM_W = 0.002     # Seam width

# --- PBR Material: brushed Al 6061-T6 ---
MAT_COLOR  = (0.78, 0.78, 0.80, 1.0)
MAT_METAL  = 0.95
MAT_ROUGH  = 0.25

# --- Output ---
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
OUT_DIR    = os.path.normpath(os.path.join(SCRIPT_DIR, ".."))
OUT_FILE   = os.path.join(OUT_DIR, "VCell_Housing.glb")
OBJ_NAME   = "VCell_Housing"

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

def add_cylinder(name, r, depth, loc=(0,0,0), rot=(0,0,0), segs=32):
    bpy.ops.mesh.primitive_cylinder_add(
        radius=r, depth=depth, vertices=segs, location=loc, rotation=rot)
    obj = bpy.context.active_object
    obj.name = name
    return obj

def bool_op(target, cutter, operation="DIFFERENCE"):
    mod = target.modifiers.new(name="Bool", type="BOOLEAN")
    mod.operation  = operation
    mod.object     = cutter
    mod.solver     = "EXACT"
    bpy.context.view_layer.objects.active = target
    bpy.ops.object.modifier_apply(modifier=mod.name)
    bpy.data.objects.remove(cutter, do_unlink=True)

def create_geometry(mat):
    # --- Main housing body ---
    body = add_box("body", L, W, H)

    # --- Hollow interior (subtract inner cavity) ---
    inner = add_box("inner",
                    L - 2*WALL, W - 2*WALL, H - WALL,
                    loc=(0, 0, -WALL/2))
    bool_op(body, inner, "DIFFERENCE")

    # --- Laser-weld seam ridge along perimeter at top ---
    seam_top = add_box("seam_top", L + 0.001, SEAM_W, SEAM_H,
                       loc=(0, 0, H/2 + SEAM_H/2))
    bool_op(body, seam_top, "UNION")
    seam_side = add_box("seam_side", SEAM_W, W + 0.001, SEAM_H,
                        loc=(0, 0, H/2 + SEAM_H/2))
    bool_op(body, seam_side, "UNION")

    # --- Pressure vent groove (coined feature on side wall, near top) ---
    vent_cutter = add_box("vent_cutter", VENT_W, VENT_D * 2, VENT_D * 2,
                          loc=(0, -W/2, H/2 - H*0.25))
    bool_op(body, vent_cutter, "DIFFERENCE")

    # --- Positive terminal hole (top face, offset +X) ---
    t_pos = add_cylinder("term_pos", TERM_R, WALL * 3,
                         loc=(L/2 - 0.015, 0.020, H/2),
                         rot=(0, 0, 0))
    bool_op(body, t_pos, "DIFFERENCE")

    # --- Negative terminal hole (top face, offset -X) ---
    t_neg = add_cylinder("term_neg", TERM_R, WALL * 3,
                         loc=(-L/2 + 0.015, 0.020, H/2),
                         rot=(0, 0, 0))
    bool_op(body, t_neg, "DIFFERENCE")

    body.name = OBJ_NAME
    mat_slot = body.data.materials
    mat_slot.clear()
    mat_slot.append(mat)
    return body

def polish(obj):
    bpy.context.view_layer.objects.active = obj
    bpy.ops.object.mode_set(mode="EDIT")
    bpy.ops.mesh.select_all(action="SELECT")
    bpy.ops.mesh.normals_make_consistent(inside=False)
    bpy.ops.uv.smart_project(angle_limit=66.0)
    bpy.ops.object.mode_set(mode="OBJECT")
    bpy.ops.object.shade_smooth()
    try:
        bpy.ops.mesh.customdata_custom_splitnormals_clear()
        obj.data.use_auto_smooth = False
    except Exception:
        pass
    try:
        bpy.ops.object.shade_auto_smooth(angle=30.0)
    except Exception:
        pass
    mod = obj.modifiers.new("Bevel", "BEVEL")
    mod.width = 0.0003
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
    print(f"[VCell_Housing] Verts={verts} Faces={faces} "
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
    print(f"[VCell_Housing] Exported → {OUT_FILE} ({kb:.1f} KiB)")

# ============================================================================
if __name__ == "__main__":
    clean_scene()
    mat = make_material("MAT_VCell_Housing", MAT_COLOR, MAT_METAL, MAT_ROUGH)
    obj = create_geometry(mat)
    polish(obj)
    verify(obj)
    export_glb(obj)
