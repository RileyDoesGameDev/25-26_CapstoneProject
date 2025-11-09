import bpy
import os
import sys
import json

#Add Button to run
#Add Button to Stop

script_dir = r"C:\Users\rfoster\Documents\2025NeumontClasses\Capstone\25-26_CapstoneProject\UDP_UnityLLS"
if script_dir not in sys.path:
    sys.path.append(script_dir)
#import Object_Move_Detection
import UDP_Server

#previoius_ObjData = []


#def Compare_Prev_ObjData():
    


def get_meshes():
    meshes = []
    for obj in bpy.context.scene.objects:
        if obj.type == 'MESH':
            meshes.append(obj.data)
    return meshes
   

mesh = get_meshes()
data = []
if mesh:
    for obj in mesh:
        obj.update()
        # Get vertices in world space 
        verts = [{"x": v.co.x, "y": v.co.z, "z": v.co.y} for v in obj.vertices]
    
        # Get triangles - Blender uses polygons, so we need to triangulate
        # Ensure mesh has triangulated faces
        obj.calc_loop_triangles()
        triangles = []
        for tri in obj.loop_triangles:
            triangles.extend([tri.vertices[0], tri.vertices[1], tri.vertices[2]])
    
        # Get normals per vertex
        normals = [{"x": v.normal.x, "y": v.normal.z, "z": v.normal.y} for v in obj.vertices]    
        
        
        
        # Convert to JSON string
        
        
        chunk_data = []

        chunk_data.append({
            "chunk": 1,
            "total": 3,
            "type": "vertices",
            "data": verts
        })

        chunk_data.append({
            "chunk": 2,
            "total": 3,
            "type": "triangles",
            "data": triangles
        })

        chunk_data.append({
            "chunk": 3,
            "total": 3,
            "type": "normals",
            "data": normals
        })
        
for item in chunk_data:              
    print(item)


UDP_Server.setup_sockets()
for item in chunk_data: 
    json_string = json.dumps(item)             
    UDP_Server.send_data(json_string)
    
UDP_Server.stop_communication()





