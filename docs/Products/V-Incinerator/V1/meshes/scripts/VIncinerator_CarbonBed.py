"""
V-Incinerator — Activated Carbon Bed  (Blender 4.4 headless)
=============================================================
Packed-bed column in 304SS vessel. 0.5 m bed depth, 4.0 m² cross-section.
Vertical cylindrical vessel with inlet/outlet nozzles, access manway,
carbon loading hatch on top, drain valve at bottom, support legs,
external stiffener rings, differential pressure taps.

Run: blender --background --python this_script.py
"""
import bpy, bmesh, math, os

PRODUCT   = "VIncinerator"
COMPONENT = "CarbonBed"
MATERIAL  = "304SS"
OUT_DIR   = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT_FILE  = f"{PRODUCT}_{COMPONENT}.glb"

SHELL_R   = 0.56        # ~4.0 m² cross-section → r ≈ 1.13/2
WALL      = 0.008
OUTER_R   = SHELL_R + WALL
HEIGHT    = 1.40         # vessel height (bed 0.5m + headspace)
FLANGE_R  = OUTER_R + 0.05
FLANGE_H  = 0.03
GAS_IN_R  = 0.10
GAS_IN_L  = 0.15
GAS_OUT_R = 0.10
GAS_OUT_L = 0.15
HATCH_R   = 0.18        # loading hatch
HATCH_H   = 0.06
DRAIN_R   = 0.04
DRAIN_L   = 0.08
MANWAY_R  = 0.16
MANWAY_L  = 0.08
LEG_R     = 0.03
LEG_H     = 0.30
RING_R    = OUTER_R + 0.012
RING_H    = 0.020

PBR = {
    "base_color": (0.65, 0.67, 0.68, 1.0),  # 304SS light grey
    "metallic": 1.0,
    "roughness": 0.32,
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

def add_cyl(r, d, v=48, loc=(0,0,0), rot=(0,0,0)):
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
    """Activated carbon bed vessel with nozzles, hatch, manway, legs, rings."""

    # 1) Main vessel — hollow vertical cylinder
    vessel = add_cyl(OUTER_R, HEIGHT, 48)
    sol = vessel.modifiers.new("Hollow", 'SOLIDIFY')
    sol.thickness = WALL; sol.offset = -1
    bpy.context.view_layer.objects.active = vessel
    bpy.ops.object.modifier_apply(modifier="Hollow")

    # 2) Top and bottom flanges
    for z in [HEIGHT/2 + FLANGE_H/2, -HEIGHT/2 - FLANGE_H/2]:
        fl = add_cyl(FLANGE_R, FLANGE_H, 48, (0, 0, z))
        hole = add_cyl(SHELL_R, FLANGE_H + 0.01, 48, (0, 0, z))
        bool_op(fl, hole, 'DIFFERENCE')
        bool_op(vessel, fl, 'UNION')

    # 3) External stiffener rings (2)
    for z in [-HEIGHT/4, HEIGHT/4]:
        ring = add_cyl(RING_R, RING_H, 48, (0, 0, z))
        rh = add_cyl(OUTER_R - 0.001, RING_H + 0.01, 48, (0, 0, z))
        bool_op(ring, rh, 'DIFFERENCE')
        bool_op(vessel, ring, 'UNION')

    # 4) Gas inlet (side, horizontal, lower section)
    gi = add_cyl(GAS_IN_R, GAS_IN_L, 32,
                 (OUTER_R + GAS_IN_L/2, 0, -HEIGHT/4),
                 (0, math.pi/2, 0))
    gi_col = add_cyl(GAS_IN_R + 0.025, 0.015, 32,
                     (OUTER_R + GAS_IN_L, 0, -HEIGHT/4),
                     (0, math.pi/2, 0))
    bool_op(gi, gi_col, 'UNION')
    bool_op(vessel, gi, 'UNION')

    # 5) Gas outlet (side, horizontal, upper section, 180° opposite)
    go = add_cyl(GAS_OUT_R, GAS_OUT_L, 32,
                 (-(OUTER_R + GAS_OUT_L/2), 0, HEIGHT/4),
                 (0, math.pi/2, 0))
    go_col = add_cyl(GAS_OUT_R + 0.025, 0.015, 32,
                     (-(OUTER_R + GAS_OUT_L), 0, HEIGHT/4),
                     (0, math.pi/2, 0))
    bool_op(go, go_col, 'UNION')
    bool_op(vessel, go, 'UNION')

    # 6) Carbon loading hatch (top center)
    hatch = add_cyl(HATCH_R, HATCH_H, 32, (0, 0, HEIGHT/2 + FLANGE_H + HATCH_H/2))
    hatch_col = add_cyl(HATCH_R + 0.03, 0.02, 32,
                         (0, 0, HEIGHT/2 + FLANGE_H + HATCH_H))
    bool_op(hatch, hatch_col, 'UNION')
    bool_op(vessel, hatch, 'UNION')

    # 7) Drain valve (bottom center)
    dr = add_cyl(DRAIN_R, DRAIN_L, 24, (0, 0, -HEIGHT/2 - FLANGE_H - DRAIN_L/2))
    dr_col = add_cyl(DRAIN_R + 0.015, 0.012, 24,
                      (0, 0, -HEIGHT/2 - FLANGE_H - DRAIN_L))
    bool_op(dr, dr_col, 'UNION')
    bool_op(vessel, dr, 'UNION')

    # 8) Access manway (side, mid-height)
    mw = add_cyl(MANWAY_R, MANWAY_L, 32,
                 (0, OUTER_R + MANWAY_L/2, 0),
                 (math.pi/2, 0, 0))
    mw_col = add_cyl(MANWAY_R + 0.035, 0.02, 32,
                     (0, OUTER_R + MANWAY_L, 0),
                     (math.pi/2, 0, 0))
    bool_op(mw, mw_col, 'UNION')
    bool_op(vessel, mw, 'UNION')

    # 9) Support legs (4)
    for angle in [math.pi/4, 3*math.pi/4, 5*math.pi/4, 7*math.pi/4]:
        lx = (OUTER_R - 0.05) * math.cos(angle)
        ly = (OUTER_R - 0.05) * math.sin(angle)
        leg = add_cyl(LEG_R, LEG_H, 12,
                       (lx, ly, -HEIGHT/2 - FLANGE_H - DRAIN_L - LEG_H/2))
        # Foot pad
        pad = add_cyl(LEG_R + 0.02, 0.01, 12,
                       (lx, ly, -HEIGHT/2 - FLANGE_H - DRAIN_L - LEG_H))
        bool_op(leg, pad, 'UNION')
        bool_op(vessel, leg, 'UNION')

    # 10) DP taps (2 small ports on opposite sides)
    for angle, z in [(0, -HEIGHT/3), (math.pi, HEIGHT/6)]:
        tx = (OUTER_R + 0.03) * math.cos(angle)
        ty = (OUTER_R + 0.03) * math.sin(angle)
        tap = add_cyl(0.012, 0.06, 12, (tx, ty, z), (0, math.pi/2, angle))
        bool_op(vessel, tap, 'UNION')

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
