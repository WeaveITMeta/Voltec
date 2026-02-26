# ============================================================================
# VCell_StatusLED.py — State-of-charge LED indicator on housing face
# Multi-body assembly: recessed bezel ring in housing face + dome lens +
# PCB substrate stub + solder pads
# Patent ref: US20090068548A1 (cell header components)
# ============================================================================
import bpy, bmesh, math, os

# --- Dimensions (meters) ---
BEZEL_R    = 0.004    # Bezel outer radius
BEZEL_T    = 0.0015   # Bezel depth in housing
LENS_R     = 0.003    # Dome lens radius
LENS_H     = 0.002    # Dome height
PCB_L      = 0.012    # PCB substrate length
PCB_W      = 0.010    # PCB width
PCB_T      = 0.001    # PCB thickness
PAD_R      = 0.0008   # Solder pad radius
PAD_T      = 0.0003   # Pad height

# --- PBR Materials ---
BEZEL_COLOR = (0.12, 0.12, 0.14, 1.0)  # Dark anodized Al bezel
BEZEL_METAL = 0.90
BEZEL_ROUGH = 0.30
LENS_COLOR  = (0.10, 0.60, 1.00, 1.0)  # Voltec status blue
LENS_METAL  = 0.0
LENS_ROUGH  = 0.05
PCB_COLOR   = (0.08, 0.25, 0.10, 1.0)  # PCB green
PCB_METAL   = 0.0
PCB_ROUGH   = 0.70
PAD_COLOR   = (0.90, 0.75, 0.30, 1.0)  # Solder gold
PAD_METAL   = 0.80
PAD_ROUGH   = 0.25

# --- Output ---
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
OUT_DIR    = os.path.normpath(os.path.join(SCRIPT_DIR, ".."))
OUT_FILE   = os.path.join(OUT_DIR, "VCell_StatusLED.glb")
OBJ_NAME   = "VCell_StatusLED"

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

def add_sphere(name, r, loc=(0,0,0), segs=16):
    bpy.ops.mesh.primitive_uv_sphere_add(
        radius=r, segments=segs, ring_count=segs//2, location=loc)
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

def create_geometry(mat_bezel, mat_lens, mat_pcb, mat_pad):
    # --- PCB substrate ---
    pcb = add_box("led_pcb", PCB_L, PCB_W, PCB_T, loc=(0, 0, 0))
    pcb.data.materials.append(mat_pcb)

    # --- Bezel ring (cylinder with hollow center) ---
    bezel_outer = add_cylinder("bezel_outer", BEZEL_R, BEZEL_T,
                               loc=(0, 0, PCB_T/2 + BEZEL_T/2))
    inner_cut = add_cylinder("bezel_inner_cut", LENS_R + 0.0002, BEZEL_T * 2,
                             loc=(0, 0, PCB_T/2 + BEZEL_T/2))
    bool_op(bezel_outer, inner_cut, "DIFFERENCE")
    bezel_outer.data.materials.append(mat_bezel)

    # --- Dome lens (half sphere clipped to flat base) ---
    dome = add_sphere("lens_dome", LENS_R, loc=(0, 0, PCB_T/2 + LENS_H/2))
    # Clip lower hemisphere
    clip = add_box("lens_clip", LENS_R * 3, LENS_R * 3, LENS_H,
                   loc=(0, 0, PCB_T/2 - LENS_H/2))
    bool_op(dome, clip, "DIFFERENCE")
    dome.data.materials.append(mat_lens)

    # --- 2 solder pads on PCB surface ---
    for sign in [-1, +1]:
        pad = add_cylinder(f"solder_pad_{sign}", PAD_R, PAD_T,
                           loc=(sign * 0.003, 0, PCB_T/2 + PAD_T/2))
        pad.data.materials.append(mat_pad)

    all_objs = [pcb, bezel_outer, dome] + [
        o for o in bpy.data.objects if o.name.startswith("solder_pad_")]
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

def verify(obj):
    bm = bmesh.new()
    bm.from_mesh(obj.data)
    bm.verts.ensure_lookup_table()
    verts = len(bm.verts)
    faces = len(bm.faces)
    quads = sum(1 for f in bm.faces if len(f.verts) == 4)
    nm    = [e for e in bm.edges if not e.is_manifold]
    bm.free()
    print(f"[VCell_StatusLED] Verts={verts} Faces={faces} "
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
    print(f"[VCell_StatusLED] Exported → {OUT_FILE} ({kb:.1f} KiB)")

# ============================================================================
if __name__ == "__main__":
    clean_scene()
    mat_bezel = make_material("MAT_VCell_Bezel", BEZEL_COLOR, BEZEL_METAL, BEZEL_ROUGH)
    mat_lens  = make_material("MAT_VCell_Lens",  LENS_COLOR,  LENS_METAL,  LENS_ROUGH)
    mat_pcb   = make_material("MAT_VCell_PCB",   PCB_COLOR,   PCB_METAL,   PCB_ROUGH)
    mat_pad   = make_material("MAT_VCell_Pad",   PAD_COLOR,   PAD_METAL,   PAD_ROUGH)
    obj = create_geometry(mat_bezel, mat_lens, mat_pcb, mat_pad)
    polish(obj)
    verify(obj)
    export_glb(obj)
