"""
Batch runner — executes all VCore Blender scripts sequentially.
Run: blender --background --python run_all.py
"""
import bpy, os, sys, importlib

SCRIPTS_DIR = os.path.dirname(os.path.abspath(__file__))

SCRIPTS = [
    "VCore_OuterCasing",
    "VCore_ReactorVessel",
    "VCore_FuelAssembly",
    "VCore_ReflectorAssembly",
    "VCore_ControlDrums",
    "VCore_HeatPipeBundle",
    "VCore_StirlingEngines",
    "VCore_HotSideHX",
    "VCore_ColdRadiator",
    "VCore_BioShield",
    "VCore_VCellBuffer",
    "VCore_ControlModule",
    "VCore_ElectricalConverter",
    "VCore_StatusArray",
]

if SCRIPTS_DIR not in sys.path:
    sys.path.insert(0, SCRIPTS_DIR)

for name in SCRIPTS:
    print(f"\n{'='*60}")
    print(f"  RUNNING: {name}.py")
    print(f"{'='*60}")
    try:
        mod = importlib.import_module(name)
        importlib.reload(mod)
        mod.main()
        print(f"  OK: {name}")
    except Exception as e:
        print(f"  FAIL: {name} — {e}")

print(f"\n{'='*60}")
print(f"  ALL DONE — {len(SCRIPTS)} scripts executed")
print(f"{'='*60}")
