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

    link_to_selected = BoolProperty(
        name="Link",
        description="Link to selected object(s)",
        default=False
    )
    
    parent_to_selected = BoolProperty(
        name="Parent",
        description="Parent to selected object(s)",
        default=False
    )
    
    copy_location = BoolProperty(
        name="Copy location",
        description="Copy location from selected object(s)",
        default=False
    )
    
    count = IntProperty(
        name="Count",
        description="Number of empty object to generate",
        default=1,
        min=1,
        max=1000
    )
        


class GeneratorPanel(Panel):
    
    bl_idname = "null_generator_panel"
    bl_label = "Empty Generator"
    bl_space_type = "VIEW_3D"
    bl_region_type = "TOOLS"
    bl_category = "Tools"
    
    
    
    def draw(self, context):
        layout = self.layout
        scene = context.scene
        settings = scene.settings
        
        layout.prop(settings, "link_to_selected", "Link")
        layout.prop(settings, "parent_to_selected", "Parent")
        layout.prop(settings, "copy_location", "Copy location")
        layout.prop(settings, "count", text="Count")
        self.layout.operator("object.generate_empty_plain_axis", icon="OUTLINER_OB_EMPTY", text="Generate")


class GenerateEmptyPlainAxis(Operator):
    """Create empty for selected object(s)"""
    bl_idname = "object.generate_empty_plain_axis"
    bl_label = "Create null object"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        
        scene = context.scene
        settings = scene.settings
        
        for x in range(0, settings.count):
            for obj in context.selected_objects:
                if (settings.link_to_selected == True):
                    o = bpy.data.objects.new('empty', obj.data)
                else:
                    o = bpy.data.objects.new('empty', None)
                    
                if (settings.parent_to_selected == True):
                    o.parent = obj
                    
                if (settings.copy_location == True):
                    o.location = obj.location
                
                scene.objects.link(o)
        
        
            
        return {'FINISHED'}


def register():
    bpy.utils.register_module(__name__)
    bpy.types.Scene.settings = PointerProperty(type=EmptyGeneratorSettings)

def unregister():
    bpy.utils.unregister_module(__name__)
    del bpy.types.Scene.settings
    
if __name__ == "__main__":
    register()