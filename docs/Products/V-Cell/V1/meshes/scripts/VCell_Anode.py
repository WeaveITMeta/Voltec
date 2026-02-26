# ============================================================================
# VCell_Anode.py — Sodium metal anode on Al hexagonal lattice substrate
# Multi-body assembly: thin prismatic Na metal layer + Al hex lattice base +
# peripheral contact tabs
# Patent ref: US9929432B2 (Na metal anode), US20090068548A1 (tab geometry)
# Dimensions: 296mm × 96mm × 0.15mm (Na 50μm + Al hex lattice 100μm)
# ============================================================================
import bpy, bmesh, math, os

# --- Dimensions (meters) ---
L      = 0.296      # Active area length (housing minus wall*2)
W      = 0.096      # Active area width
NA_T   = 0.00005    # Sodium layer thickness 50μm
AL_T   = 0.00010    # Al hex lattice thickness 100μm
TAB_L  = 0.012      # Current collector tab length
TAB_W  = 0.008      # Tab width
TAB_T  = 0.0002     # Tab thickness
HEX_A  = 0.00005    # Hex cell edge 50μm (visual representation)

# --- PBR Materials ---
NA_COLOR   = (0.85, 0.88, 0.90, 1.0)   # Silvery sodium metal
NA_METAL   = 0.98
NA_ROUGH   = 0.15
AL_COLOR   = (0.72, 0.74, 0.76, 1.0)   # Al honeycomb lattice
AL_METAL   = 0.95
AL_ROUGH   = 0.20

# --- Output ---
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
OUT_DIR    = os.path.normpath(os.path.join(SCRIPT_DIR, ".."))
OUT_FILE   = os.path.join(OUT_DIR, "VCell_Anode.glb")
OBJ_NAME   = "VCell_Anode"

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

def create_geometry(mat_na, mat_al):
    base_z = 0.0

    # --- Al hex lattice substrate ---
    al_base = add_box("al_lattice", L, W, AL_T,
                      loc=(0, 0, base_z + AL_T/2))

    # --- Honeycomb texture: punch rows of hexagonal cutouts ---
    # Represent hex cells as closely-packed cylinders removed from the slab
    # 5 rows × 8 cols at coarse visual scale (50μm scaled to visible geometry)
    HEX_R = 0.008   # Visual hex cell radius (scaled for mesh detail)
    HEX_SP_X = HEX_R * 2.1
    HEX_SP_Y = HEX_R * 1.82
    cutters = []
    rows, cols = 5, 10
    for row in range(rows):
        for col in range(cols):
            cx = -L/2 + 0.02 + col * HEX_SP_X + (row % 2) * HEX_R
            cy = -W/2 + 0.02 + row * HEX_SP_Y
            if abs(cx) < L/2 - 0.01 and abs(cy) < W/2 - 0.01:
                c = add_box(f"hc_{row}_{col}",
                            HEX_R * 1.2, HEX_R * 1.2, AL_T * 2,
                            loc=(cx, cy, base_z + AL_T/2))
                cutters.append(c)
    for c in cutters:
        bool_op(al_base, c, "DIFFERENCE")
    al_base.data.materials.append(mat_al)

    # --- Sodium metal layer on top of lattice ---
    na_layer = add_box("na_layer", L - 0.002, W - 0.002, NA_T,
                       loc=(0, 0, base_z + AL_T + NA_T/2))
    na_layer.data.materials.append(mat_na)

    # --- Current collector tab (positive lead, Al) ---
    tab = add_box("anode_tab", TAB_L, TAB_W, TAB_T,
                  loc=(L/2 - TAB_L/2, 0, base_z + AL_T/2))
    tab.data.materials.append(mat_al)

    # --- Join all into single mesh ---
    assembled = join_objects([al_base, na_layer, tab])
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

def verify(obj):
    bm = bmesh.new()
    bm.from_mesh(obj.data)
    bm.verts.ensure_lookup_table()
    verts = len(bm.verts)
    faces = len(bm.faces)
    quads = sum(1 for f in bm.faces if len(f.verts) == 4)
    nm    = [e for e in bm.edges if not e.is_manifold]
    bm.free()
    print(f"[VCell_Anode] Verts={verts} Faces={faces} "
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
    print(f"[VCell_Anode] Exported → {OUT_FILE} ({kb:.1f} KiB)")

# ============================================================================
if __name__ == "__main__":
    clean_scene()
    mat_na = make_material("MAT_VCell_Na", NA_COLOR, NA_METAL, NA_ROUGH)
    mat_al = make_material("MAT_VCell_AlHex", AL_COLOR, AL_METAL, AL_ROUGH)
    obj = create_geometry(mat_na, mat_al)
    polish(obj)
    verify(obj)
    export_glb(obj)
