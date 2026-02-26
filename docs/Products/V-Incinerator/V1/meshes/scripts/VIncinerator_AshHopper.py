"""
V-Incinerator — Ash Collection Hopper  (Blender 4.4 headless)
==============================================================
A36 Carbon Steel + refractory-lined hopper for vitrified slag collection.
Rectangular top opening transitioning to a tapered conical discharge.
Inlet flange at top, slide gate valve at bottom, vibrator motor bracket,
access inspection port, support frame legs.

Run: blender --background --python this_script.py
"""
import bpy, bmesh, math, os

PRODUCT   = "VIncinerator"
COMPONENT = "AshHopper"
MATERIAL  = "A36_Steel"
OUT_DIR   = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT_FILE  = f"{PRODUCT}_{COMPONENT}.glb"

TOP_W     = 1.40        # top opening width
TOP_D     = 1.00        # top opening depth
TOP_H     = 0.50        # vertical section height
BOT_R     = 0.15        # discharge opening radius
TAPER_H   = 0.80        # tapered section height
WALL      = 0.010
FLANGE_W  = TOP_W + 0.10
FLANGE_D  = TOP_D + 0.10
FLANGE_H  = 0.04
GATE_W    = 0.30        # slide gate housing
GATE_D    = 0.20
GATE_H    = 0.15
LEG_SZ    = 0.06        # square legs
LEG_H     = 0.50
VIBR_W    = 0.15        # vibrator bracket
VIBR_D    = 0.10
VIBR_H    = 0.08

PBR = {
    "base_color": (0.45, 0.42, 0.38, 1.0),  # A36 dark steel
    "metallic": 1.0,
    "roughness": 0.55,
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

def add_cyl(r, d, v=32, loc=(0,0,0), rot=(0,0,0)):
    bpy.ops.mesh.primitive_cylinder_add(vertices=v, radius=r, depth=d,
                                        location=loc, rotation=rot)
    return bpy.context.active_object

def add_cone(r1, r2, d, v=32, loc=(0,0,0)):
    bpy.ops.mesh.primitive_cone_add(vertices=v, radius1=r1, radius2=r2,
                                     depth=d, location=loc)
    return bpy.context.active_object

def bool_op(target, cutter, op='UNION'):
    mod = target.modifiers.new(op, 'BOOLEAN')
    mod.operation = op; mod.object = cutter; mod.solver = 'EXACT'
    bpy.context.view_layer.objects.active = target
    bpy.ops.object.modifier_apply(modifier=op)
    bpy.data.objects.remove(cutter, do_unlink=True)

def create_geometry():
    """Ash hopper with taper, gate valve, vibrator bracket, legs."""

    # 1) Upper rectangular section — hollow box
    upper = add_cube(TOP_W, TOP_D, TOP_H, (0, 0, TAPER_H/2 + TOP_H/2))
    sol = upper.modifiers.new("Hollow", 'SOLIDIFY')
    sol.thickness = WALL; sol.offset = -1
    bpy.context.view_layer.objects.active = upper
    bpy.ops.object.modifier_apply(modifier="Hollow")

    # 2) Tapered section — cone from rectangular-ish to circular discharge
    # Approximate with a cone (wider base → narrow top mapped to wider top → narrow bottom)
    taper = add_cone(max(TOP_W, TOP_D)/2, BOT_R, TAPER_H, 32, (0, 0, 0))
    sol2 = taper.modifiers.new("Hollow", 'SOLIDIFY')
    sol2.thickness = WALL; sol2.offset = -1
    bpy.context.view_layer.objects.active = taper
    bpy.ops.object.modifier_apply(modifier="Hollow")
    bool_op(upper, taper, 'UNION')

    # 3) Top flange
    flange = add_cube(FLANGE_W, FLANGE_D, FLANGE_H,
                       (0, 0, TAPER_H/2 + TOP_H + FLANGE_H/2))
    fl_hole = add_cube(TOP_W - 0.02, TOP_D - 0.02, FLANGE_H + 0.01,
                        (0, 0, TAPER_H/2 + TOP_H + FLANGE_H/2))
    bool_op(flange, fl_hole, 'DIFFERENCE')
    bool_op(upper, flange, 'UNION')

    # 4) Discharge nozzle at bottom
    discharge = add_cyl(BOT_R, 0.12, 24, (0, 0, -TAPER_H/2 - 0.06))
    d_col = add_cyl(BOT_R + 0.03, 0.02, 24, (0, 0, -TAPER_H/2 - 0.12))
    bool_op(discharge, d_col, 'UNION')
    bool_op(upper, discharge, 'UNION')

    # 5) Slide gate valve housing at discharge
    gate = add_cube(GATE_W, GATE_D, GATE_H,
                     (0, BOT_R + GATE_D/2, -TAPER_H/2 - 0.06))
    bool_op(upper, gate, 'UNION')

    # 6) Vibrator motor bracket (on taper wall)
    vibr = add_cube(VIBR_W, VIBR_D, VIBR_H,
                     (TOP_W/3, TOP_D/3 + VIBR_D/2, TAPER_H/4))
    bool_op(upper, vibr, 'UNION')

    # 7) Inspection port (side of upper section)
    insp = add_cyl(0.08, 0.06, 24,
                    (TOP_W/2 + 0.03, 0, TAPER_H/2 + TOP_H/2),
                    (0, math.pi/2, 0))
    insp_col = add_cyl(0.10, 0.015, 24,
                        (TOP_W/2 + 0.06, 0, TAPER_H/2 + TOP_H/2),
                        (0, math.pi/2, 0))
    bool_op(insp, insp_col, 'UNION')
    bool_op(upper, insp, 'UNION')

    # 8) Support frame legs (4 at corners)
    total_h = TAPER_H + TOP_H
    for cx in [-TOP_W/2 + LEG_SZ, TOP_W/2 - LEG_SZ]:
        for cy in [-TOP_D/2 + LEG_SZ, TOP_D/2 - LEG_SZ]:
            leg = add_cube(LEG_SZ, LEG_SZ, LEG_H,
                           (cx, cy, -TAPER_H/2 - 0.12 - LEG_H/2))
            # Foot pad
            pad = add_cube(LEG_SZ * 2, LEG_SZ * 2, 0.015,
                           (cx, cy, -TAPER_H/2 - 0.12 - LEG_H))
            bool_op(leg, pad, 'UNION')
            bool_op(upper, leg, 'UNION')

    # 9) Cross braces between legs
    brace_z = -TAPER_H/2 - 0.12 - LEG_H * 0.6
    for cy in [-TOP_D/2 + LEG_SZ, TOP_D/2 - LEG_SZ]:
        brace = add_cube(TOP_W - LEG_SZ * 2, 0.03, 0.03, (0, cy, brace_z))
        bool_op(upper, brace, 'UNION')

    upper.name = f"{PRODUCT}_{COMPONENT}"
    upper.data.name = f"{PRODUCT}_{COMPONENT}_mesh"
    return upper

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
