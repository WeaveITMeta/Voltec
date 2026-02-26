"""
V-Incinerator — Primary Combustion Chamber  (Blender 4.4 headless)
==================================================================
Inconel 718 secondary burn chamber. ID 1.8 m × L 3.6 m, horizontal.
25 mm wall + refractory lining. 6 secondary air nozzle stubs,
inlet/outlet flanges, viewport port, support saddles.

Run: blender --background --python this_script.py
"""
import bpy, bmesh, math, os

PRODUCT   = "VIncinerator"
COMPONENT = "CombustionChamber"
MATERIAL  = "Inconel_718"
OUT_DIR   = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT_FILE  = f"{PRODUCT}_{COMPONENT}.glb"

# ── Dimensions (meters, from PATENT.md) ───────────────────────────────
INNER_R   = 0.90          # ID 1.8 m
WALL      = 0.025 + 0.04  # 25mm Inconel + 40mm refractory modeled as single wall
OUTER_R   = INNER_R + WALL
LENGTH    = 3.60
FLANGE_R  = OUTER_R + 0.10
FLANGE_H  = 0.05
NOZZLE_R  = 0.05          # secondary air nozzle radius
NOZZLE_L  = 0.15          # stub protrusion
SADDLE_W  = 0.20
SADDLE_H  = 0.25
SADDLE_D  = 0.60

PBR = {
    "base_color": (0.62, 0.60, 0.55, 1.0),  # Inconel grey-tan
    "metallic": 1.0,
    "roughness": 0.38,
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

def add_cyl(r, d, v=64, loc=(0,0,0), rot=(0,0,0)):
    bpy.ops.mesh.primitive_cylinder_add(vertices=v, radius=r, depth=d,
                                        location=loc, rotation=rot)
    return bpy.context.active_object

def add_cube(sx, sy, sz, loc=(0,0,0)):
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=loc)
    obj = bpy.context.active_object; obj.scale = (sx, sy, sz)
    bpy.ops.object.transform_apply(scale=True)
    return obj

def bool_op(target, cutter, op='UNION'):
    mod = target.modifiers.new(op, 'BOOLEAN')
    mod.operation = op; mod.object = cutter; mod.solver = 'EXACT'
    bpy.context.view_layer.objects.active = target
    bpy.ops.object.modifier_apply(modifier=op)
    bpy.data.objects.remove(cutter, do_unlink=True)

def create_geometry():
    """Horizontal combustion chamber with nozzles, flanges, saddles."""

    # 1) Main vessel — horizontal thick-walled cylinder (along X axis)
    vessel = add_cyl(OUTER_R, LENGTH, 64, (0,0,0), (0, math.pi/2, 0))
    sol = vessel.modifiers.new("Hollow", 'SOLIDIFY')
    sol.thickness = WALL; sol.offset = -1
    bpy.context.view_layer.objects.active = vessel
    bpy.ops.object.modifier_apply(modifier="Hollow")

    # 2) Inlet flange (left end, -X)
    fl_in = add_cyl(FLANGE_R, FLANGE_H, 64, (-LENGTH/2 - FLANGE_H/2, 0, 0), (0, math.pi/2, 0))
    hole = add_cyl(INNER_R, FLANGE_H+0.01, 64, (-LENGTH/2 - FLANGE_H/2, 0, 0), (0, math.pi/2, 0))
    bool_op(fl_in, hole, 'DIFFERENCE')
    bool_op(vessel, fl_in, 'UNION')

    # 3) Outlet flange (right end, +X)
    fl_out = add_cyl(FLANGE_R, FLANGE_H, 64, (LENGTH/2 + FLANGE_H/2, 0, 0), (0, math.pi/2, 0))
    hole2 = add_cyl(INNER_R, FLANGE_H+0.01, 64, (LENGTH/2 + FLANGE_H/2, 0, 0), (0, math.pi/2, 0))
    bool_op(fl_out, hole2, 'DIFFERENCE')
    bool_op(vessel, fl_out, 'UNION')

    # 4) Six secondary air nozzle stubs along top (3 per side, spaced along length)
    for i in range(6):
        x_pos = -LENGTH/3 + (i % 3) * LENGTH/3
        angle = math.radians(30 if i < 3 else -30)  # angled slightly
        ny = (OUTER_R + NOZZLE_L/2) * math.sin(math.pi/2 + angle)
        nz = (OUTER_R + NOZZLE_L/2) * math.cos(math.pi/2 + angle)
        stub = add_cyl(NOZZLE_R, NOZZLE_L, 24, (x_pos, ny * (1 if i<3 else -1), nz))
        # Collar at end
        cny = (OUTER_R + NOZZLE_L) * math.sin(math.pi/2 + angle)
        cnz = (OUTER_R + NOZZLE_L) * math.cos(math.pi/2 + angle)
        collar = add_cyl(NOZZLE_R + 0.02, 0.015, 24, (x_pos, cny * (1 if i<3 else -1), cnz))
        bool_op(stub, collar, 'UNION')
        bool_op(vessel, stub, 'UNION')

    # 5) Viewport port (top center) — small cylinder + flange
    vp = add_cyl(0.06, 0.10, 24, (0, 0, OUTER_R + 0.05))
    vp_col = add_cyl(0.09, 0.02, 24, (0, 0, OUTER_R + 0.10))
    bool_op(vp, vp_col, 'UNION')
    bool_op(vessel, vp, 'UNION')

    # 6) Two support saddles (bottom)
    for x_off in [-LENGTH/3, LENGTH/3]:
        saddle = add_cube(SADDLE_D, SADDLE_W, SADDLE_H,
                          (x_off, 0, -(OUTER_R + SADDLE_H/2)))
        bool_op(vessel, saddle, 'UNION')

    vessel.name = f"{PRODUCT}_{COMPONENT}"
    vessel.data.name = f"{PRODUCT}_{COMPONENT}_mesh"
    return vessel

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
