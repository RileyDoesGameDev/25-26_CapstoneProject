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


def get_meshes():
    meshes = []
    for obj in bpy.context.scene.objects:
        if obj.type == 'MESH':
            meshes.append(obj.data)
    return meshes
   


# dynamic chunking

## take list of each type devide each into groups off 100s put in json chunk
def set_chunks(chunk_data):
    for group in chunk_data:
        vert_list = []
        trig_list = []
        norms_list = []
        
        
        
        
        
        


'''
        
def make_json(chunk_data): 
    total_chunks = len(chunk_data) * 3
    current_count = 0  
    json_list = []      
    for group in chunk_data:
        current_count += 1
        json_list.append({
            "chunk": current_count,
            "total": total_chunks,
            "type": "vertices",
            "data": group[0],

        })
        current_count += 1
        json_list.append({
            "chunk": current_count,
            "total": total_chunks,
            "type": "triangles",
            "trigData": group[1]
        })
        current_count += 1
        json_list.append({
            "chunk": current_count,
            "total": total_chunks,
            "type": "normals",
            "data": group[2],
          
        })
        

    return json_list    
        
'''

mesh = get_meshes()
chunk_data = []

if mesh:
    for obj in mesh:
        obj.update()
      
        print(obj.name)
        # Get vertices in world space 
        
        verts = [{ "x": v.co.x, "y": v.co.z, "z": v.co.y} for v in obj.vertices]
    
        # Get triangles - Blender uses polygons, so we need to triangulate
        # Ensure mesh has triangulated faces
        obj.calc_loop_triangles()
        trigs = []
        for tri in obj.loop_triangles:
            trigs.extend([tri.vertices[0], tri.vertices[1], tri.vertices[2]])
    
        # Get normals per vertex
        norms = [{"x": v.normal.x, "y": v.normal.z, "z": v.normal.y} for v in obj.vertices] 
        
           
        
        chunk_data.append([verts, trigs, normals])
   

chunks = set_chunks(chunk_data) 

UDP_Server.setup_sockets()

for item in chunks: 
    print(item)
   # json_string = json.dumps(item)             
   # UDP_Server.send_data(json_string)
    
UDP_Server.stop_communication()





       
