bl_info = {
    "name": "Empty Generator",
    "description": "Empty object generator",
    "author": "Dwi Rizki Irawan",
    "version": (0, 0, 1),
    "blender": (2, 79, 0),
    "category": "Object"
}

import bpy

from bpy.props import (StringProperty, 
                        BoolProperty, 
                        IntProperty, 
                        FloatProperty, 
                        FloatVectorProperty, 
                        EnumProperty, 
                        PointerProperty)

from bpy.types import (Panel, 
                        Operator, 
                        AddonPreferences, 
                        PropertyGroup)


class EmptyGeneratorSettings(PropertyGroup):
    parent = EnumProperty(
                    # (identifier, name, descripion)
        items = [
                    ('0','None', 'Don\'t parent empty'),
                    ('1','Object', 'Parent empty to object'),
                    ('2','Empty', 'Parent object to empty'),
                ],
        name="Parent",
        default="0",
        )
        
    prefix = StringProperty(
        name="Prefix",
        description="Empty prefix",
        default=""
    )

    copy_location = BoolProperty(
        name="Copy location",
        description="Copy location from selected object(s)",
        default=True
    )
        

class EmptyGeneratorPanel(Panel):
    bl_idname = "empyy_generator_panel"
    bl_label = "Empty Generator"
    bl_space_type = "VIEW_3D"
    bl_region_type = "TOOLS"
    bl_category = "Tools"

    def draw(self, context):
        layout = self.layout
        scene = context.scene
        settings = scene.settings
        
        layout.prop(settings, "parent", "Parent")
        layout.prop(settings, "prefix", "Prefix")
        layout.prop(settings, "copy_location", "Copy location")
        self.layout.operator("object.generate_empty_plain_axis", icon="OUTLINER_OB_EMPTY", text="Generate")

class GenerateEmptyPlainAxis(Operator):
    """Create empty for selected object(s)"""
    bl_idname = "object.generate_empty_plain_axis"
    bl_label = "Create null object"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        scene = context.scene
        settings = scene.settings
        
        for obj in context.selected_objects:
            if (settings.prefix != ""):
                o = bpy.data.objects.new(settings.prefix +'_Empty', None) 
            else:
                o = bpy.data.objects.new(obj.name +'_Empty', None)
            
            scene.objects.link(o)
                
            if (settings.copy_location == True):
                o.location = obj.location
            
            # Object as parent
            if (settings.parent == "1"):
                o.parent = obj
                o.matrix_parent_inverse = obj.matrix_world.inverted()
                scene.update()
                
            # Empty as parent
            if (settings.parent == "2"):
                obj.parent = o
                obj.matrix_local = o.matrix_world.inverted()
                scene.update()
                    
        return {'FINISHED'}

def register():
    bpy.utils.register_module(__name__)
    bpy.types.Scene.settings = PointerProperty(type=EmptyGeneratorSettings)

def unregister():
    bpy.utils.unregister_module(__name__)
    del bpy.types.Scene.settings
    
if __name__ == "__main__":
    register()