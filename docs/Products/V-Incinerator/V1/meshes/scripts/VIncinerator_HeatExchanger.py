"""
V-Incinerator — Heat Exchanger  (Blender 4.4 headless)
======================================================
Shell-and-tube counter-flow heat exchanger. Cu-Ni C71500 tubes.
Shell: 1.2 m dia × 3.0 m long. 240 tubes (modeled as tube sheet discs).
Inlet/outlet nozzles on shell + end bonnets + support saddles.

Run: blender --background --python this_script.py
"""
import bpy, bmesh, math, os

PRODUCT   = "VIncinerator"
COMPONENT = "HeatExchanger"
MATERIAL  = "CuNi_C71500"
OUT_DIR   = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT_FILE  = f"{PRODUCT}_{COMPONENT}.glb"

# ── Dimensions (meters, from PATENT.md) ───────────────────────────────
SHELL_R   = 0.60          # shell OD/2 = 1.2m dia
WALL      = 0.020         # shell wall
INNER_R   = SHELL_R - WALL
LENGTH    = 3.00
FLANGE_R  = SHELL_R + 0.08
FLANGE_H  = 0.04
NOZZLE_R  = 0.10          # shell-side inlet/outlet
NOZZLE_L  = 0.20
BONNET_R  = SHELL_R       # end bonnets (hemisphere approximation)
BONNET_H  = 0.35
SADDLE_W  = 0.18
SADDLE_H  = 0.22
SADDLE_D  = 0.50
TUBE_SHEET_T = 0.03       # tube sheet thickness (visible disc)

PBR = {
    "base_color": (0.72, 0.55, 0.42, 1.0),  # copper-nickel warm tone
    "metallic": 1.0,
    "roughness": 0.30,
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
    """Shell-and-tube heat exchanger with nozzles, tube sheets, bonnets, saddles."""

    # 1) Main shell — horizontal thick-walled cylinder (along X)
    shell = add_cyl(SHELL_R, LENGTH, 64, (0,0,0), (0, math.pi/2, 0))
    sol = shell.modifiers.new("Hollow", 'SOLIDIFY')
    sol.thickness = WALL; sol.offset = -1
    bpy.context.view_layer.objects.active = shell
    bpy.ops.object.modifier_apply(modifier="Hollow")

    # 2) Tube sheets at each end (solid discs visible inside)
    for xoff in [-LENGTH/2 + TUBE_SHEET_T/2, LENGTH/2 - TUBE_SHEET_T/2]:
        ts = add_cyl(INNER_R - 0.002, TUBE_SHEET_T, 64, (xoff, 0, 0), (0, math.pi/2, 0))
        bool_op(shell, ts, 'UNION')

    # 3) End bonnets — semi-elliptical caps (approximated as short cylinders with domed look)
    for xoff, xdir in [(-LENGTH/2 - BONNET_H/2, -1), (LENGTH/2 + BONNET_H/2, 1)]:
        bonnet = add_cyl(SHELL_R, BONNET_H, 64, (xoff, 0, 0), (0, math.pi/2, 0))
        # Hollow the bonnet
        bh = bonnet.modifiers.new("Hollow", 'SOLIDIFY')
        bh.thickness = WALL; bh.offset = -1
        bpy.context.view_layer.objects.active = bonnet
        bpy.ops.object.modifier_apply(modifier="Hollow")
        # Flange ring between shell and bonnet
        fl = add_cyl(FLANGE_R, FLANGE_H, 64,
                     (xdir * (LENGTH/2 + FLANGE_H/2), 0, 0), (0, math.pi/2, 0))
        fl_hole = add_cyl(INNER_R, FLANGE_H+0.01, 64,
                          (xdir * (LENGTH/2 + FLANGE_H/2), 0, 0), (0, math.pi/2, 0))
        bool_op(fl, fl_hole, 'DIFFERENCE')
        bool_op(bonnet, fl, 'UNION')
        bool_op(shell, bonnet, 'UNION')

    # 4) Shell-side inlet nozzle (top, near left end)
    n_in = add_cyl(NOZZLE_R, NOZZLE_L, 32, (-LENGTH/4, 0, SHELL_R + NOZZLE_L/2))
    n_in_col = add_cyl(NOZZLE_R + 0.03, 0.02, 32, (-LENGTH/4, 0, SHELL_R + NOZZLE_L))
    bool_op(n_in, n_in_col, 'UNION')
    bool_op(shell, n_in, 'UNION')

    # 5) Shell-side outlet nozzle (bottom, near right end)
    n_out = add_cyl(NOZZLE_R, NOZZLE_L, 32, (LENGTH/4, 0, -(SHELL_R + NOZZLE_L/2)))
    n_out_col = add_cyl(NOZZLE_R + 0.03, 0.02, 32, (LENGTH/4, 0, -(SHELL_R + NOZZLE_L)))
    bool_op(n_out, n_out_col, 'UNION')
    bool_op(shell, n_out, 'UNION')

    # 6) Tube-side nozzles (on each bonnet end cap)
    for xoff in [-LENGTH/2 - BONNET_H, LENGTH/2 + BONNET_H]:
        tn = add_cyl(0.08, 0.14, 32, (xoff, 0, 0), (0, math.pi/2, 0))
        tn_col = add_cyl(0.11, 0.02, 32,
                         (xoff + (0.14 if xoff > 0 else -0.14)/2, 0, 0),
                         (0, math.pi/2, 0))
        bool_op(tn, tn_col, 'UNION')
        bool_op(shell, tn, 'UNION')

    # 7) Support saddles
    for xoff in [-LENGTH/3, LENGTH/3]:
        saddle = add_cube(SADDLE_D, SADDLE_W, SADDLE_H,
                          (xoff, 0, -(SHELL_R + SADDLE_H/2)))
        bool_op(shell, saddle, 'UNION')

    shell.name = f"{PRODUCT}_{COMPONENT}"
    shell.data.name = f"{PRODUCT}_{COMPONENT}_mesh"
    return shell

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
