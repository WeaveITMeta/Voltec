# ============================================================================
# VCell_Electrolyte.py — Sc-doped NASICON solid electrolyte membrane
# Multi-body assembly: thin sintered ceramic slab + ALD interlayer surface +
# edge chamfer (tape-cast geometry)
# Patent ref: EP3168914A1 (solid-state battery tape-cast electrolyte)
# Dimensions: 296mm × 96mm × 0.030mm (30μm sintered ceramic)
# ============================================================================
import bpy, bmesh, math, os

# --- Dimensions (meters) ---
L      = 0.296       # Active length
W      = 0.096       # Active width
T      = 0.000030    # 30μm electrolyte thickness
EDGE_C = 0.0005      # Edge chamfer (tape-cast edge bead)

# --- PBR Material: pale ceramic, translucent-ish ---
MAT_COLOR = (0.90, 0.88, 0.85, 1.0)   # Off-white sintered ceramic
MAT_METAL = 0.0
MAT_ROUGH = 0.55

# --- Output ---
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
OUT_DIR    = os.path.normpath(os.path.join(SCRIPT_DIR, ".."))
OUT_FILE   = os.path.join(OUT_DIR, "VCell_Electrolyte.glb")
OBJ_NAME   = "VCell_Electrolyte"

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

def create_geometry(mat):
    # --- Main electrolyte slab ---
    slab = add_box("elyte_slab", L, W, T, loc=(0, 0, 0))

    # --- Edge bead (tape-cast edge is slightly thicker) ---
    # Add thin strips along all 4 edges representing edge bead
    bead_t = T * 1.5
    for i, (bx, by, bsx, bsy) in enumerate([
        (0,  W/2,  L,      EDGE_C),    # +Y edge
        (0, -W/2,  L,      EDGE_C),    # -Y edge
        (L/2,  0,  EDGE_C, W),         # +X edge
        (-L/2, 0,  EDGE_C, W),         # -X edge
    ]):
        bead = add_box(f"bead_{i}", bsx, bsy, bead_t, loc=(bx, by, 0))
        mod = slab.modifiers.new("BoolBead", "BOOLEAN")
        mod.operation = "UNION"
        mod.object    = bead
        mod.solver    = "EXACT"
        bpy.context.view_layer.objects.active = slab
        bpy.ops.object.modifier_apply(modifier=mod.name)
        bpy.data.objects.remove(bead, do_unlink=True)

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
    mod = obj.modifiers.new("Bevel", "BEVEL")
    mod.width    = T * 0.3
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
    print(f"[VCell_Electrolyte] Verts={verts} Faces={faces} "
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
    print(f"[VCell_Electrolyte] Exported → {OUT_FILE} ({kb:.1f} KiB)")

# ============================================================================
if __name__ == "__main__":
    clean_scene()
    mat = make_material("MAT_VCell_ScNASICON", MAT_COLOR, MAT_METAL, MAT_ROUGH)
    obj = create_geometry(mat)
    polish(obj)
    verify(obj)
    export_glb(obj)
