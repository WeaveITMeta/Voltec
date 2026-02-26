# ============================================================================
# VCell_AlHexLattice.py — Standalone Al hexagonal lattice substrate display
# Multi-body assembly: flat Al slab + hexagonal honeycomb cell array punched
# through + peripheral frame + tab stub
# Patent ref: US9929432B2 (structured current collector)
# Dimensions: 150mm × 80mm × 0.1mm (100μm, display scale 10x Z)
# ============================================================================
import bpy, bmesh, math, os

# --- Dimensions (meters, Z scaled 10x for visual clarity) ---
L       = 0.150      # Display length (half cell)
W       = 0.080      # Display width
T       = 0.001      # Visual thickness (10x real 100μm)
FRAME_T = 0.003      # Peripheral frame thickness
TAB_L   = 0.010
TAB_W   = 0.006
TAB_T   = T

# Honeycomb parameters (visually accurate hex grid)
HEX_R    = 0.006     # Hex cell inner radius
HEX_WALL = 0.0008    # Wall between cells
HEX_SP_X = (HEX_R + HEX_WALL) * 2.0
HEX_SP_Y = (HEX_R + HEX_WALL) * math.sqrt(3)

# --- PBR Material: brushed aluminum lattice ---
MAT_COLOR = (0.78, 0.80, 0.82, 1.0)
MAT_METAL = 0.95
MAT_ROUGH = 0.22

# --- Output ---
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
OUT_DIR    = os.path.normpath(os.path.join(SCRIPT_DIR, ".."))
OUT_FILE   = os.path.join(OUT_DIR, "VCell_AlHexLattice.glb")
OBJ_NAME   = "VCell_AlHexLattice"

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

def create_geometry(mat):
    # --- Main slab ---
    slab = add_box("hex_slab", L, W, T, loc=(0, 0, 0))

    # --- Punch hexagonal array ---
    rows = int((W - FRAME_T * 2) / HEX_SP_Y) + 1
    cols = int((L - FRAME_T * 2) / HEX_SP_X) + 1
    cutters = []
    for row in range(rows):
        for col in range(cols):
            cx = -L/2 + FRAME_T + col * HEX_SP_X + (row % 2) * (HEX_SP_X / 2)
            cy = -W/2 + FRAME_T + row * HEX_SP_Y
            if (abs(cx) < L/2 - FRAME_T - HEX_R and
                    abs(cy) < W/2 - FRAME_T - HEX_R):
                cell = add_hex_prism(f"hex_{row}_{col}",
                                     HEX_R, T * 3,
                                     loc=(cx, cy, 0))
                # Rotate 30° so flat sides face up/down
                cell.rotation_euler[2] = math.radians(30)
                bpy.ops.object.transform_apply(rotation=True)
                cutters.append(cell)

    # Apply all boolean cuts
    for c in cutters:
        bool_op(slab, c, "DIFFERENCE")

    # --- Current collector tab ---
    tab = add_box("hex_tab", TAB_L, TAB_W, TAB_T,
                  loc=(L/2 - TAB_L/2, 0, 0))
    bool_op(slab, tab, "UNION")

    slab.name = OBJ_NAME
    slab.data.materials.append(mat)
    return slab

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
    print(f"[VCell_AlHexLattice] Verts={verts} Faces={faces} "
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
    print(f"[VCell_AlHexLattice] Exported → {OUT_FILE} ({kb:.1f} KiB)")

# ============================================================================
if __name__ == "__main__":
    clean_scene()
    mat = make_material("MAT_VCell_AlHexLattice", MAT_COLOR, MAT_METAL, MAT_ROUGH)
    obj = create_geometry(mat)
    polish(obj)
    verify(obj)
    export_glb(obj)
