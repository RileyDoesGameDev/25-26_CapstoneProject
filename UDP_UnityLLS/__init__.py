bl_info = {
    "name": "Unity LLS",
    "author": "Riley Foster",
    "version": (1, 0),
    "blender": (3, 0, 0),
    "location": "View3D > Tool Shelf > Unity LLS",
    "description": "Send mesh data to Unity via a UDP Socket",
    "category": "Object",
}

import bpy
from . import UDP_Server
from.import mesh_sender


class UDP_OT_Start(bpy.types.Operator):
    """Start UDP Server"""
    bl_idname = "udp.start_server"
    bl_label = "Start UDP Server"

    def execute(self, context):
        UDP_Server.setup_sockets()
        mesh_sender.send_mesh_data()
        self.report({'INFO'}, "UDP Server started and mesh sent")
        return {'FINISHED'}


class UDP_OT_Stop(bpy.types.Operator):
    """Stop UDP Server"""
    bl_idname = "udp.stop_server"
    bl_label = "Stop UDP Server"

    def execute(self, context):
        UDP_Server.stop_communication()
        self.report({'INFO'}, "UDP Server stopped")
        return {'FINISHED'}


class UDP_PT_Panel(bpy.types.Panel):
    bl_label = "Unity LLS"
    bl_idname = "UDP_PT_Panel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "UDP Tools"

    def draw(self, context):
        layout = self.layout
        layout.operator("udp.start_server", icon="PLAY")
        layout.operator("udp.stop_server", icon="PAUSE")


# Registration
classes = (UDP_OT_Start, UDP_OT_Stop, UDP_PT_Panel)

def register():
    for cls in classes:
        bpy.utils.register_class(cls)

def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)

if __name__ == "__main__":
    register()