import bpy
import json
from . import UDP_Server


import bpy
import json
from . import UDP_Server

def get_mesh():
    obj = bpy.data.objects
    if obj and obj.type == 'MESH':
        return obj.data
    return None


def send_mesh_data():
    mesh = get_mesh()
    if not mesh:
        print("No mesh found.")
        return

    mesh.calc_loop_triangles()
    verts = [{"x": v.co.x, "y": v.co.z, "z": v.co.y} for v in mesh.vertices]
    triangles = [i for tri in mesh.loop_triangles for i in tri.vertices]
    normals = [{"x": v.normal.x, "y": v.normal.z, "z": v.normal.y} for v in mesh.vertices]

    message = json.dumps({
        "name": mesh.name,
        "vertices": verts,
        "triangles": triangles,
        "normals": normals,
    })

    print("Sending mesh:", message[:120], "...")
    UDP_Server.send_data(message)
