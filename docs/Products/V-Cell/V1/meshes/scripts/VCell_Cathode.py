# ============================================================================
# VCell_Cathode.py — Sulfur@VACNT cathode on Al hexagonal lattice
# Multi-body assembly: Al hex lattice base + VACNT forest layer (dark carbon
# texture) + sulfur-infused top layer + current collector tab
# Patent ref: US9929432B2 (S-PAN composite cathode), US20100273062A1 (all-solid)
# Dimensions: 296mm × 96mm × 0.30mm (200μm S/VACNT + 100μm Al hex lattice)
# ============================================================================
import bpy, bmesh, math, os

# --- Dimensions (meters) ---
L       = 0.296      # Active length
W       = 0.096      # Active width
AL_T    = 0.00010    # Al hex lattice 100μm
VACNT_T = 0.00015    # VACNT forest 150μm
S_T     = 0.00005    # Sulfur infiltration cap 50μm
TAB_L   = 0.012
TAB_W   = 0.008
TAB_T   = 0.0002

# --- PBR Materials ---
AL_COLOR    = (0.72, 0.74, 0.76, 1.0)  # Al lattice
AL_METAL    = 0.95
AL_ROUGH    = 0.20
VACNT_COLOR = (0.05, 0.05, 0.05, 1.0)  # Carbon black VACNT
VACNT_METAL = 0.0
VACNT_ROUGH = 0.90
S_COLOR     = (0.95, 0.85, 0.20, 1.0)  # Sulfur yellow
S_METAL     = 0.0
S_ROUGH     = 0.60

# --- Output ---
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
OUT_DIR    = os.path.normpath(os.path.join(SCRIPT_DIR, ".."))
OUT_FILE   = os.path.join(OUT_DIR, "VCell_Cathode.glb")
OBJ_NAME   = "VCell_Cathode"

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

def create_geometry(mat_al, mat_cnt, mat_s):
    base_z = 0.0

    # --- Al hex lattice substrate ---
    al_base = add_box("al_lattice_c", L, W, AL_T,
                      loc=(0, 0, base_z + AL_T/2))
    # Honeycomb cutouts (same pattern as anode)
    HEX_R  = 0.008
    HEX_SP = HEX_R * 2.1
    HEX_SY = HEX_R * 1.82
    rows, cols = 4, 9
    for row in range(rows):
        for col in range(cols):
            cx = -L/2 + 0.025 + col * HEX_SP + (row % 2) * HEX_R
            cy = -W/2 + 0.025 + row * HEX_SY
            if abs(cx) < L/2 - 0.01 and abs(cy) < W/2 - 0.01:
                c = add_box(f"hc_c_{row}_{col}",
                            HEX_R * 1.1, HEX_R * 1.1, AL_T * 2,
                            loc=(cx, cy, base_z + AL_T/2))
                bool_op(al_base, c, "DIFFERENCE")
    al_base.data.materials.append(mat_al)

    # --- VACNT forest layer (dark carbon slab with surface texture) ---
    cnt_layer = add_box("vacnt_layer", L - 0.002, W - 0.002, VACNT_T,
                        loc=(0, 0, base_z + AL_T + VACNT_T/2))
    # Texture: small raised posts representing CNT bundle tops
    POST_R = 0.005
    POST_H = VACNT_T * 0.3
    n_posts = 24
    for i in range(n_posts):
        angle = (i / n_posts) * 2 * math.pi
        rx = math.cos(angle) * (L/2 - 0.03)
        ry = math.sin(angle) * (W/2 - 0.01)
        post = add_box(f"cnt_post_{i}", POST_R, POST_R, POST_H,
                       loc=(rx, ry, base_z + AL_T + VACNT_T + POST_H/2))
        mod = cnt_layer.modifiers.new("PostUnion", "BOOLEAN")
        mod.operation = "UNION"
        mod.object    = post
        mod.solver    = "EXACT"
        bpy.context.view_layer.objects.active = cnt_layer
        bpy.ops.object.modifier_apply(modifier=mod.name)
        bpy.data.objects.remove(post, do_unlink=True)
    cnt_layer.data.materials.append(mat_cnt)

    # --- Sulfur infiltration cap layer (yellow-tinted top) ---
    s_layer = add_box("s_layer", L - 0.004, W - 0.004, S_T,
                      loc=(0, 0, base_z + AL_T + VACNT_T + S_T/2))
    s_layer.data.materials.append(mat_s)

    # --- Current collector tab (Al, cathode side) ---
    tab = add_box("cathode_tab", TAB_L, TAB_W, TAB_T,
                  loc=(-L/2 + TAB_L/2, 0, base_z + AL_T/2))
    tab.data.materials.append(mat_al)

    assembled = join_objects([al_base, cnt_layer, s_layer, tab])
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
    print(f"[VCell_Cathode] Verts={verts} Faces={faces} "
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
    print(f"[VCell_Cathode] Exported → {OUT_FILE} ({kb:.1f} KiB)")

# ============================================================================
if __name__ == "__main__":
    clean_scene()
    mat_al  = make_material("MAT_VCell_AlHex_C", AL_COLOR, AL_METAL, AL_ROUGH)
    mat_cnt = make_material("MAT_VCell_VACNT", VACNT_COLOR, VACNT_METAL, VACNT_ROUGH)
    mat_s   = make_material("MAT_VCell_Sulfur", S_COLOR, S_METAL, S_ROUGH)
    obj = create_geometry(mat_al, mat_cnt, mat_s)
    polish(obj)
    verify(obj)
    export_glb(obj)
