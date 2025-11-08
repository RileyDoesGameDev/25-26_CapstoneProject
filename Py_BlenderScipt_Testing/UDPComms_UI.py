import bpy
import os
import sys
import json

#Add Button to run
#Add Button to Stop

script_dir = r"C:\Users\rfoster\Documents\2025NeumontClasses\Capstone\25-26_CapstoneProject\Py_BlenderScipt_Testing"
if script_dir not in sys.path:
    sys.path.append(script_dir)
#import Object_Move_Detection
import UDP_Server



def get_mesh():
    obj = bpy.data.objects['Cube']
    if obj and obj.type == 'MESH':
        mesh = obj.data
        return mesh
    return None


mesh = get_mesh()
if mesh:
    mesh.update()
    # Get vertices in world space 
    verts = [{"x": v.co.x, "y": v.co.z, "z": v.co.y} for v in mesh.vertices]
    
    # Get triangles - Blender uses polygons, so we need to triangulate
    # Ensure mesh has triangulated faces
    mesh.calc_loop_triangles()
    triangles = []
    for tri in mesh.loop_triangles:
        triangles.extend([tri.vertices[0], tri.vertices[1], tri.vertices[2]])
    
    # Get normals per vertex
    normals = [{"x": v.normal.x, "y": v.normal.z, "z": v.normal.y} for v in mesh.vertices]
    
        
        
        # Convert to JSON string
message = json.dumps({
    "name": mesh.name,
    "vertices": verts,
    "triangles": triangles,
    "normals": normals,
    
})
print(message)

UDP_Server.setup_sockets()
UDP_Server.send_data(message)
UDP_Server.stop_communication()





