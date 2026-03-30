import bpy

import json 

from . import UDP_Server

MAX_CHUNK_SIZE = 200  # number of items per chunk (safe for UDP)


    

def chunk_list(lst, size):
    """Yield successive chunks from list."""
    for i in range(0, len(lst), size):
        yield lst[i:i + size]


def send_mesh(object):
    obj = object.data
    obj.update()

    # Vertices (swapped Y/Z for Unity)
    vertices = [{"x": v.co.x, "y": v.co.z, "z": v.co.y} for v in obj.vertices]

    # Triangles and per-triangle material index (triangle order via loop_triangles)
    obj.calc_loop_triangles()
    triangles = []
    material_indices = []
    for tri in obj.loop_triangles:
        triangles.extend([tri.vertices[0], tri.vertices[1], tri.vertices[2]])
        material_indices.append(object.data.polygons[tri.polygon_index].material_index)

    # Normals (swapped Y/Z to match vertex ordering)
    normals = [{"x": v.normal.x, "y": v.normal.z, "z": v.normal.y} for v in obj.vertices]

    # Materials (fix spelling and send useful fields)
    materials = []

    for mat_slot in object.material_slots:
        mat = mat_slot.material

        if mat is None:
            materials.append({"name": None, "diffuse_color": [1,1,1,1], "use_nodes": False})
            continue

        if mat.use_nodes:
            bsdf = mat.node_tree.nodes.get("Principled BSDF")
            if bsdf:
                col = list(bsdf.inputs["Base Color"].default_value)
            else:
                col = [1,1,1,1]
        else:
            col = list(mat.diffuse_color)
    
        materials.append({
            "name": mat.name,
            "diffuse_color": col,
            "use_nodes": mat.use_nodes,
        })

        
        #if mat is None:
         #   materials.append({"name": None, "diffuse_color": [1.0, 1.0, 1.0, 1.0], "use_nodes": False})
        #else:
            # ensure diffuse_color is serializable (RGBA)
         #   col = list(mat.diffuse_color) if hasattr(mat, "diffuse_color") else [1.0, 1.0, 1.0, 1.0]
            



    # chunk lists for UDP safety
    vert_chunks = list(chunk_list(vertices, MAX_CHUNK_SIZE))
    tri_chunks = list(chunk_list(triangles, MAX_CHUNK_SIZE * 3))
    norm_chunks = list(chunk_list(normals, MAX_CHUNK_SIZE))
    matInd_chunks = list(chunk_list(material_indices, MAX_CHUNK_SIZE))
    # Build packets list so we compute total correctly
    packets = []

    # Vertices packets
    for chunk in vert_chunks:
        packets.append({
            "type": "vertices",
            "data": chunk
        })

    # Triangle packets (intData)
    for chunk in tri_chunks:
        packets.append({
            "type": "triangles",
            "intData": chunk
        })

    # Normal packets
    for chunk in norm_chunks:
        packets.append({
            "type": "normals",
            "data": chunk
        })

    # Single materials packet (materials are usually few; send once)
    
    
    packets.append({
        "type": "materials",
        "materialData": materials
    })
    
    for chunk in matInd_chunks:
        packets.append({
            "type": "material_index",
            "intData": chunk
        })

    # Now send with correct chunk numbering and total
    total_chunks = len(packets)
    UDP_Server.setup_sockets()
    chunk_id = 1

    for pkt_body in packets:
        pkt = {
            "name": obj.name,
            "chunk": chunk_id,
            "total": total_chunks,
            "type": pkt_body["type"]
        }
        # copy appropriate fields
        if pkt_body["type"] == "vertices" or pkt_body["type"] == "normals":
            pkt["data"] = pkt_body["data"]
        elif pkt_body["type"] == "triangles" or pkt_body["type"] == "material_index":
            pkt["intData"] = pkt_body["intData"]
        elif pkt_body["type"] == "materials":
            pkt["materialData"] = pkt_body["materialData"]

        UDP_Server.send_data(json.dumps(pkt))
        chunk_id += 1

    UDP_Server.stop_communication()



def main():
    for obj in bpy.context.scene.objects:
        if obj.type == "MESH":
            send_mesh(obj)


if __name__ == "__main__":
    main()