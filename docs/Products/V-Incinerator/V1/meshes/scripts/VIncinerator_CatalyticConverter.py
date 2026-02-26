"""
V-Incinerator — Catalytic Converter  (Blender 4.4 headless)
============================================================
Pt-Pd on γ-alumina honeycomb monolith in Inconel 625 housing.
400 cpsi cordierite substrate. Rectangular housing with flanged
inlet/outlet ducts, access inspection port, thermocouple ports,
mounting brackets, external stiffener ribs.

Run: blender --background --python this_script.py
"""
import bpy, bmesh, math, os

PRODUCT   = "VIncinerator"
COMPONENT = "CatalyticConverter"
MATERIAL  = "Inconel_625"
OUT_DIR   = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT_FILE  = f"{PRODUCT}_{COMPONENT}.glb"

# ── Dimensions ────────────────────────────────────────────────────────
WIDTH  = 1.20       # housing X
DEPTH  = 0.80       # housing Y
HEIGHT = 0.60       # housing Z
WALL   = 0.008
DUCT_W = 0.50       # duct opening
DUCT_H = 0.40
DUCT_L = 0.20       # stub length
TC_R   = 0.015      # thermocouple port radius
TC_L   = 0.06
BRACKET_W = 0.08
BRACKET_D = 0.06
BRACKET_H = 0.12
RIB_W  = 0.012
RIB_D  = 0.006

PBR = {
    "base_color": (0.58, 0.60, 0.56, 1.0),  # Inconel 625 grey
    "metallic": 1.0,
    "roughness": 0.40,
    "alpha": 1.0,
    "emission": (0.0, 0.0, 0.0, 1.0),
    "emission_strength": 0.0,
}

def clean_scene():
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete(use_global=False)
    for b in bpy.data.meshes:
        if b.users == 0: bpy.data.meshes.remove(b)
    for b in bpy.data.materials:
        if b.users == 0: bpy.data.materials.remove(b)

def setup_scene():
    bpy.context.scene.name = "Scene0"
    bpy.context.scene.unit_settings.system = 'METRIC'
    bpy.context.scene.unit_settings.scale_length = 1.0

def create_material():
    mat = bpy.data.materials.new(name=f"MAT_{PRODUCT}_{MATERIAL}")
    mat.use_nodes = True; mat.use_backface_culling = True
    nodes = mat.node_tree.nodes; links = mat.node_tree.links; nodes.clear()
    bsdf = nodes.new('ShaderNodeBsdfPrincipled')
    bsdf.inputs['Base Color'].default_value = PBR["base_color"]
    bsdf.inputs['Metallic'].default_value = PBR["metallic"]
    bsdf.inputs['Roughness'].default_value = PBR["roughness"]
    bsdf.inputs['Alpha'].default_value = PBR["alpha"]
    bsdf.inputs['Emission Color'].default_value = PBR["emission"]
    bsdf.inputs['Emission Strength'].default_value = PBR["emission_strength"]
    out = nodes.new('ShaderNodeOutputMaterial'); out.location = (300, 0)
    links.new(bsdf.outputs['BSDF'], out.inputs['Surface'])
    return mat

def add_cube(sx, sy, sz, loc=(0,0,0)):
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=loc)
    obj = bpy.context.active_object; obj.scale = (sx, sy, sz)
    bpy.ops.object.transform_apply(scale=True)
    return obj

def add_cyl(r, d, v=24, loc=(0,0,0), rot=(0,0,0)):
    bpy.ops.mesh.primitive_cylinder_add(vertices=v, radius=r, depth=d,
                                        location=loc, rotation=rot)
    return bpy.context.active_object

def bool_op(target, cutter, op='UNION'):
    mod = target.modifiers.new(op, 'BOOLEAN')
    mod.operation = op; mod.object = cutter; mod.solver = 'EXACT'
    bpy.context.view_layer.objects.active = target
    bpy.ops.object.modifier_apply(modifier=op)
    bpy.data.objects.remove(cutter, do_unlink=True)

def create_geometry():
    """Catalytic converter housing with ducts, TC ports, brackets, ribs."""

    # 1) Main housing — hollow box
    box = add_cube(WIDTH, DEPTH, HEIGHT)
    sol = box.modifiers.new("Hollow", 'SOLIDIFY')
    sol.thickness = WALL; sol.offset = -1
    bpy.context.view_layer.objects.active = box
    bpy.ops.object.modifier_apply(modifier="Hollow")

    # 2) Inlet duct (left, -X) with transition taper
    duct_in = add_cube(DUCT_L, DUCT_W, DUCT_H, (-WIDTH/2 - DUCT_L/2, 0, 0))
    # Flange at end
    fl_in = add_cube(0.02, DUCT_W + 0.05, DUCT_H + 0.05, (-WIDTH/2 - DUCT_L, 0, 0))
    bool_op(duct_in, fl_in, 'UNION')
    bool_op(box, duct_in, 'UNION')

    # 3) Outlet duct (right, +X)
    duct_out = add_cube(DUCT_L, DUCT_W, DUCT_H, (WIDTH/2 + DUCT_L/2, 0, 0))
    fl_out = add_cube(0.02, DUCT_W + 0.05, DUCT_H + 0.05, (WIDTH/2 + DUCT_L, 0, 0))
    bool_op(duct_out, fl_out, 'UNION')
    bool_op(box, duct_out, 'UNION')

    # 4) Thermocouple ports (3 on top, evenly spaced)
    for i in range(3):
        x = -WIDTH/3 + i * WIDTH/3
        tc = add_cyl(TC_R, TC_L, 12, (x, 0, HEIGHT/2 + TC_L/2))
        tc_col = add_cyl(TC_R + 0.008, 0.01, 12, (x, 0, HEIGHT/2 + TC_L))
        bool_op(tc, tc_col, 'UNION')
        bool_op(box, tc, 'UNION')

    # 5) Inspection port (front face, +Y)
    insp = add_cyl(0.08, 0.06, 24, (0, DEPTH/2 + 0.03, 0), (math.pi/2, 0, 0))
    insp_col = add_cyl(0.11, 0.015, 24, (0, DEPTH/2 + 0.06, 0), (math.pi/2, 0, 0))
    bool_op(insp, insp_col, 'UNION')
    bool_op(box, insp, 'UNION')

    # 6) External stiffener ribs (vertical, on long sides)
    for y_sign in [1, -1]:
        for x_off in [-WIDTH/3, 0, WIDTH/3]:
            rib = add_cube(RIB_W, RIB_D, HEIGHT * 0.8,
                           (x_off, y_sign * (DEPTH/2 + RIB_D/2), 0))
            bool_op(box, rib, 'UNION')

    # 7) Mounting brackets (4 at bottom corners)
    for cx in [-WIDTH/2 + 0.10, WIDTH/2 - 0.10]:
        for cy in [-DEPTH/2 + 0.08, DEPTH/2 - 0.08]:
            bracket = add_cube(BRACKET_W, BRACKET_D, BRACKET_H,
                               (cx, cy, -HEIGHT/2 - BRACKET_H/2))
            bool_op(box, bracket, 'UNION')

    box.name = f"{PRODUCT}_{COMPONENT}"
    box.data.name = f"{PRODUCT}_{COMPONENT}_mesh"
    return box

def polish(obj):
    bpy.context.view_layer.objects.active = obj
    bpy.ops.object.shade_auto_smooth()
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.mesh.select_all(action='SELECT')
    bpy.ops.uv.smart_project(angle_limit=math.radians(66), island_margin=0.02)
    bpy.ops.mesh.normals_make_consistent(inside=False)
    bpy.ops.mesh.remove_doubles(threshold=0.0001)
    bpy.ops.object.mode_set(mode='OBJECT')
    bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
    bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY', center='BOUNDS')

def verify(obj):
    bm = bmesh.new(); bm.from_mesh(obj.data)
    f = len(bm.faces); q = sum(1 for face in bm.faces if len(face.verts) == 4)
    nm = sum(1 for e in bm.edges if not e.is_manifold)
    print(f"\n  MESH: {obj.name}  |  V:{len(bm.verts)} E:{len(bm.edges)} F:{f}")
    print(f"  Quads: {q}/{f} ({100*q/max(f,1):.0f}%)  |  Non-manifold: {nm}  |  Watertight: {'YES' if nm==0 else 'NO'}")
    bm.free()

def export(obj):
    os.makedirs(OUT_DIR, exist_ok=True)
    path = os.path.join(OUT_DIR, OUT_FILE)
    bpy.ops.object.select_all(action='DESELECT')
    obj.select_set(True); bpy.context.view_layer.objects.active = obj
    bpy.ops.export_scene.gltf(
        filepath=path, export_format='GLB', use_selection=True,
        export_apply=True, export_normals=True, export_materials='EXPORT',
        export_cameras=False, export_lights=False,
        export_animations=False, export_yup=True,
        export_draco_mesh_compression_enable=True,
        export_draco_mesh_compression_level=6)
    print(f"  EXPORTED: {path} ({os.path.getsize(path)/1024:.1f} KB)\n")

def main():
    clean_scene(); setup_scene()
    mat = create_material()
    obj = create_geometry()
    obj.data.materials.append(mat)
    polish(obj); verify(obj); export(obj)
    print(f"DONE: {PRODUCT}_{COMPONENT}")

if __name__ == "__main__":
    main()
