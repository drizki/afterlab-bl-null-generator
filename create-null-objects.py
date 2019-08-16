bl_info = {
    "name": "Null Generator",
    "category": "Object",
}

import bpy

class CreateNullObjectPanel(bpy.types.Panel):
    bl_idname = "create_null_object_panel"
    bl_label = "Null Object Generator"
    bl_space_type = "VIEW_3D"
    bl_region_type = "TOOLS"
    bl_category = "Tools"
    
    def draw(self, context):
        self.layout.operator("object.create_null_objects", text="Create")

class CreateNullObject(bpy.types.Operator):
    """Create null objects for selected objects"""
    bl_idname = "object.create_null_objects"
    bl_label = "Create null object"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        scene = context.scene
        for obj in context.selected_objects:
            o = bpy.data.objects.new('empty', None)
            o.location.x = obj.location.x
            o.location.y = obj.location.y
            o.location.z = obj.location.z
            scene.objects.link(o)
        return {'FINISHED'}

def register():
    bpy.utils.register_class(CreateNullObject)
    bpy.utils.register_class(CreateNullObjectPanel)

def unregister():
    bpy.utils.unregister_class(CreateNullObject)
    bpy.utils.unregister_class(CreateNullObjectPanel)

if __name__ == "__main__":
    register()