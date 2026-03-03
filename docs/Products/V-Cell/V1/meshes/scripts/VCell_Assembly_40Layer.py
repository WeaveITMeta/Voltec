# ============================================================================
# VCell_Assembly_40Layer.py — Complete 40-layer electrochemical stack assembly
# Anode-Electrolyte-Cathode sandwich repeated 40 times in parallel
# Patent ref: US9929432B2, EP3168914A1, US20100273062A1
# ============================================================================
import bpy, bmesh, math, os

# --- Dimensions (meters) ---
# Housing: 300mm × 100mm × 12mm
L_HOUSING = 0.300
W_HOUSING = 0.100
H_HOUSING = 0.012

# Single layer thicknesses
ANODE_T = 0.00015      # 50μm Na + 100μm Al hex lattice
ELECTROLYTE_T = 0.00003  # 30μm ceramic
CATHODE_T = 0.0003     # 200μm S/VACNT + 100μm Al hex lattice
THERMAL_PAD_T = 0.0002 # 200μm AlN

# Layer dimensions (slightly smaller than housing interior)
L_LAYER = 0.296
W_LAYER = 0.096

# Stack parameters
NUM_LAYERS = 40
SINGLE_CYCLE_HEIGHT = ANODE_T + ELECTROLYTE_T + CATHODE_T
TOTAL_STACK_HEIGHT = NUM_LAYERS * SINGLE_CYCLE_HEIGHT + THERMAL_PAD_T

# Visual scale multiplier (1:1 = actual size, no scaling)
VISUAL_SCALE = 1.0  # 1:1 scaling - actual dimensions

# --- PBR Materials ---
def make_material(name, color, metal, rough):
    mat = bpy.data.materials.new(name=name)
    mat.use_nodes = True
    bsdf = mat.node_tree.nodes.get("Principled BSDF")
    bsdf.inputs["Base Color"].default_value = color
    bsdf.inputs["Metallic"].default_value = metal
    bsdf.inputs["Roughness"].default_value = rough
    return mat

# --- Output ---
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
OUT_DIR = os.path.normpath(os.path.join(SCRIPT_DIR, ".."))
OUT_FILE = os.path.join(OUT_DIR, "VCell_Assembly_40Layer.glb")
OBJ_NAME = "VCell_Assembly_40Layer"

# ============================================================================
def clean_scene():
    bpy.ops.wm.read_factory_settings(use_empty=True)
    bpy.context.scene.name = "Scene0"

def add_box(name, sx, sy, sz, loc=(0,0,0)):
    bpy.ops.mesh.primitive_cube_add(size=1, location=loc)
    obj = bpy.context.active_object
    obj.name = name
    obj.scale = (sx, sy, sz)
    bpy.ops.object.transform_apply(scale=True)
    return obj

def join_objects(objs):
    bpy.ops.object.select_all(action="DESELECT")
    for o in objs:
        o.select_set(True)
    bpy.context.view_layer.objects.active = objs[0]
    bpy.ops.object.join()
    return bpy.context.active_object

def create_geometry(mat_na, mat_al, mat_elyte, mat_cnt, mat_s, mat_aln):
    # --- Center stack at Y=0 ---
    stack_bottom = -TOTAL_STACK_HEIGHT / 2
    
    all_components = []
    
    # --- Thermal pad (bottom, single instance) ---
    tp_y = stack_bottom + THERMAL_PAD_T / 2
    tp = add_box("thermal_pad", L_LAYER, W_LAYER, THERMAL_PAD_T, loc=(0, tp_y, 0))
    tp.data.materials.append(mat_aln)
    all_components.append(tp)
    
    # --- 40 repeated cycles of Anode-Electrolyte-Cathode ---
    for cycle_idx in range(NUM_LAYERS):
        cycle_bottom = stack_bottom + THERMAL_PAD_T + cycle_idx * SINGLE_CYCLE_HEIGHT
        
        # Anode (layer 1 of cycle)
        anode_y = cycle_bottom + ANODE_T / 2
        anode = add_box(f"anode_{cycle_idx}", L_LAYER, W_LAYER, ANODE_T, loc=(0, anode_y, 0))
        anode.data.materials.append(mat_na)
        all_components.append(anode)
        
        # Electrolyte (layer 2 of cycle)
        elyte_y = cycle_bottom + ANODE_T + ELECTROLYTE_T / 2
        elyte = add_box(f"electrolyte_{cycle_idx}", L_LAYER, W_LAYER, ELECTROLYTE_T, loc=(0, elyte_y, 0))
        elyte.data.materials.append(mat_elyte)
        all_components.append(elyte)
        
        # Cathode (layer 3 of cycle)
        cathode_y = cycle_bottom + ANODE_T + ELECTROLYTE_T + CATHODE_T / 2
        cathode = add_box(f"cathode_{cycle_idx}", L_LAYER, W_LAYER, CATHODE_T, loc=(0, cathode_y, 0))
        cathode.data.materials.append(mat_s)
        all_components.append(cathode)
    
    # --- Join all into single mesh ---
    assembled = join_objects(all_components)
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
    nm = [e for e in bm.edges if not e.is_manifold]
    bm.free()
    print(f"[VCell_Assembly_40Layer] Verts={verts} Faces={faces} "
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
    print(f"[VCell_Assembly_40Layer] Exported → {OUT_FILE} ({kb:.1f} KiB)")

# ============================================================================
if __name__ == "__main__":
    clean_scene()
    mat_na = make_material("MAT_VCell_Anode", (0.85, 0.88, 0.90, 1.0), 0.0, 0.70)
    mat_al = make_material("MAT_VCell_AlLattice", (0.78, 0.80, 0.82, 1.0), 0.0, 0.70)
    mat_elyte = make_material("MAT_VCell_Electrolyte", (0.90, 0.88, 0.85, 1.0), 0.0, 0.80)
    mat_cnt = make_material("MAT_VCell_CNT", (0.05, 0.05, 0.05, 1.0), 0.0, 0.90)
    mat_s = make_material("MAT_VCell_Sulfur", (0.30, 0.25, 0.20, 1.0), 0.0, 0.85)
    mat_aln = make_material("MAT_VCell_ThermalPad", (0.92, 0.90, 0.85, 1.0), 0.0, 0.70)
    obj = create_geometry(mat_na, mat_al, mat_elyte, mat_cnt, mat_s, mat_aln)
    polish(obj)
    verify(obj)
    export_glb(obj)
