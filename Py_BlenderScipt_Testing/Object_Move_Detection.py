import bpy



def run_script_one():
    print("Executing Script")
    # Example: Create a new cube
    bpy.ops.mesh.primitive_cube_add(size=2, enter_editmode=False, align='WORLD', location=(0, 0, 5))