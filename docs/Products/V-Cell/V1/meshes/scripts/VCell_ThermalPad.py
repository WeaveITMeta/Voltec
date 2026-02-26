# ============================================================================
# VCell_ThermalPad.py — AlN ceramic thermal interface pad
# Multi-body assembly: thin ceramic slab + registration notches (locating
# features for stack assembly) + surface texture (lapped ceramic finish)
# Patent ref: US20090068548A1 (prismatic cell thermal management)
# Dimensions: 300mm × 100mm × 0.2mm (AlN 170 W/(m·K))
# ============================================================================
import bpy, bmesh, os

# --- Dimensions (meters) ---
L       = 0.300      # Full housing footprint
W       = 0.100
T       = 0.0002     # 0.2mm AlN pad
NOTCH_W = 0.005      # Registration notch width
NOTCH_D = 0.001      # Notch depth

# --- PBR Material: AlN ceramic (pale beige, matte) ---
MAT_COLOR = (0.92, 0.90, 0.85, 1.0)
MAT_METAL = 0.0
MAT_ROUGH = 0.45

# --- Output ---
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
OUT_DIR    = os.path.normpath(os.path.join(SCRIPT_DIR, ".."))
OUT_FILE   = os.path.join(OUT_DIR, "VCell_ThermalPad.glb")
OBJ_NAME   = "VCell_ThermalPad"

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

def create_geometry(mat):
    # --- Main AlN slab ---
    slab = add_box("aln_slab", L, W, T, loc=(0, 0, 0))

    # --- Registration notches on each long edge (2 per side) ---
    for sign in [+1, -1]:
        for offset in [-0.08, +0.08]:
            notch = add_box(
                f"notch_{sign}_{offset}",
                NOTCH_W, NOTCH_D * 2, T * 2,
                loc=(offset, sign * (W/2), 0))
            bool_op(slab, notch, "DIFFERENCE")

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
    mod.width    = T * 0.2
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
    print(f"[VCell_ThermalPad] Verts={verts} Faces={faces} "
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
    print(f"[VCell_ThermalPad] Exported → {OUT_FILE} ({kb:.1f} KiB)")

# ============================================================================
if __name__ == "__main__":
    clean_scene()
    mat = make_material("MAT_VCell_AlN", MAT_COLOR, MAT_METAL, MAT_ROUGH)
    obj = create_geometry(mat)
    polish(obj)
    verify(obj)
    export_glb(obj)
