"""
V-Supreme Assembly Position Baker
Imports all 23 component GLBs, translates each to its assembly position
(Y-up, meters, origin at feet center), and re-exports each GLB in-place.

Also exports a combined VSupreme_Assembly.glb with all parts positioned.

Run: blender --background --python assemble_all.py
"""
import bpy, bmesh, os, math

MESH_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
ASSEMBLY_FILE = os.path.join(MESH_DIR, "VSupreme_Assembly.glb")

# Assembly positions: component_name -> (x, y, z) in meters, Y-up
# Origin at ground contact center (feet midpoint), Y=0 is ground
POSITIONS = {
    "VSupreme_Helmet":          ( 0.000,  2.050,  0.000),
    "VSupreme_TorsoChest":      ( 0.000,  1.450,  0.080),
    "VSupreme_TorsoBack":       ( 0.000,  1.450, -0.080),
    "VSupreme_FusionReactor":   ( 0.000,  1.500,  0.000),
    "VSupreme_VCellArray":      ( 0.000,  1.300,  0.000),
    "VSupreme_PauldronL":       (-0.350,  1.700,  0.000),
    "VSupreme_PauldronR":       ( 0.350,  1.700,  0.000),
    "VSupreme_UpperArmL":       (-0.400,  1.450,  0.000),
    "VSupreme_UpperArmR":       ( 0.400,  1.450,  0.000),
    "VSupreme_ForearmL":        (-0.420,  1.100,  0.050),
    "VSupreme_ForearmR":        ( 0.420,  1.100,  0.050),
    "VSupreme_GauntletL":       (-0.430,  0.820,  0.050),
    "VSupreme_GauntletR":       ( 0.430,  0.820,  0.050),
    "VSupreme_HipAssembly":     ( 0.000,  0.950,  0.000),
    "VSupreme_ThighL":          (-0.150,  0.680,  0.000),
    "VSupreme_ThighR":          ( 0.150,  0.680,  0.000),
    "VSupreme_ShinL":           (-0.150,  0.300,  0.000),
    "VSupreme_ShinR":           ( 0.150,  0.300,  0.000),
    "VSupreme_BootL":           (-0.150,  0.060,  0.020),
    "VSupreme_BootR":           ( 0.150,  0.060,  0.020),
    "VSupreme_Spine":           ( 0.000,  1.350, -0.050),
    "VSupreme_IonThrusterPack": ( 0.000,  1.550, -0.200),
    "VSupreme_StatusArray":     ( 0.000,  2.080,  0.100),
}

def clean_scene():
    """Remove all objects from scene"""
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete(use_global=False)
    for block in bpy.data.meshes:
        if block.users == 0:
            bpy.data.meshes.remove(block)
    for block in bpy.data.materials:
        if block.users == 0:
            bpy.data.materials.remove(block)

def main():
    clean_scene()
    bpy.context.scene.unit_settings.system = 'METRIC'
    bpy.context.scene.unit_settings.scale_length = 1.0

    imported_objects = []
    missing = []

    for comp_name, (px, py, pz) in POSITIONS.items():
        glb_path = os.path.join(MESH_DIR, f"{comp_name}.glb")
        if not os.path.exists(glb_path):
            missing.append(comp_name)
            print(f"  MISSING: {glb_path}")
            continue

        # Import GLB
        bpy.ops.import_scene.gltf(filepath=glb_path)
        # Get newly imported objects
        new_objs = [o for o in bpy.context.selected_objects if o.type == 'MESH']
        if not new_objs:
            print(f"  WARNING: No mesh objects imported from {comp_name}")
            continue

        for obj in new_objs:
            # Translate to assembly position
            obj.location = (px, py, pz)
            # Apply transform so position is baked into vertices
            bpy.context.view_layer.objects.active = obj
            obj.select_set(True)
            bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
            # Reset origin to geometry center for clean export
            bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY', center='BOUNDS')
            obj.name = comp_name
            imported_objects.append(obj)
            print(f"  PLACED: {comp_name} at ({px:.3f}, {py:.3f}, {pz:.3f})")

        bpy.ops.object.select_all(action='DESELECT')

    if missing:
        print(f"\n  WARNING: {len(missing)} components missing: {missing}")

    # Re-export each component individually with baked position
    print("\n--- Re-exporting individual GLBs with baked positions ---")
    for obj in imported_objects:
        comp_name = obj.name
        out_path = os.path.join(MESH_DIR, f"{comp_name}.glb")
        bpy.ops.object.select_all(action='DESELECT')
        obj.select_set(True)
        bpy.context.view_layer.objects.active = obj
        bpy.ops.export_scene.gltf(
            filepath=out_path,
            export_format='GLB',
            use_selection=True,
            export_apply=True,
            export_normals=True,
            export_materials='EXPORT',
            export_cameras=False,
            export_lights=False,
            export_animations=False,
            export_yup=True,
            export_draco_mesh_compression_enable=True,
            export_draco_mesh_compression_level=6,
        )
        size_kb = os.path.getsize(out_path) / 1024
        print(f"  EXPORTED: {comp_name}.glb ({size_kb:.1f} KB)")

    # Export combined assembly
    print("\n--- Exporting combined assembly ---")
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.export_scene.gltf(
        filepath=ASSEMBLY_FILE,
        export_format='GLB',
        use_selection=True,
        export_apply=True,
        export_normals=True,
        export_materials='EXPORT',
        export_cameras=False,
        export_lights=False,
        export_animations=False,
        export_yup=True,
        export_draco_mesh_compression_enable=True,
        export_draco_mesh_compression_level=6,
    )
    size_kb = os.path.getsize(ASSEMBLY_FILE) / 1024
    print(f"  ASSEMBLY: VSupreme_Assembly.glb ({size_kb:.1f} KB)")
    print(f"\n  COMPLETE: {len(imported_objects)}/23 components positioned and exported")

if __name__ == "__main__":
    main()
