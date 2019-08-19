bl_info = {
    "name": "Bone Generator",
    "description": "Generate bone for selected object(s)",
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

# ------------------------------------------------------
# Settings
# ------------------------------------------------------
# class BoneGeneratorSettings(PropertyGroup):

# ------------------------------------------------------
# UI Class
# ------------------------------------------------------
class UIPanel(Panel):
    bl_idname = "bone_generator_panel"
    bl_label = "Bone Generator"
    bl_space_type = "VIEW_3D"
    bl_region_type = "TOOLS"
    bl_category = "Tools"

    # ------------------------------------------------------
    # Draw UI
    # ------------------------------------------------------
    def draw(self, context):
        layout = self.layout
        scene = context.scene
        # settings = scene.bone_generator_settings
        
        self.layout.operator("object.generate_bone_action", icon="OUTLINER_OB_ARMATURE", text="Generate")

class GenerateBoneAction(Operator):
    """Run generate bone action"""
    bl_idname = "object.generate_bone_action"
    bl_label = "Generate bone"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        scene = context.scene
        ops = bpy.ops
        # settings = scene.bone_generator_settings
        
        selected = context.selected_objects
        ops.object.armature_add()
        
        
        armature = context.active_object
        
        
        bpy.ops.object.mode_set(mode='EDIT')
        
        edit = armature.data.edit_bones
        
        for bone in edit:
            edit.remove(bone)
            
            for obj in selected:
                edit.new(obj.name + '_bone')
                
                obj.parent = armature
                
        return {'FINISHED'}

def register():
    bpy.utils.register_module(__name__)
    # bpy.types.Scene.bone_generator_settings = PointerProperty(type=BoneGeneratorSettings)

def unregister():
    bpy.utils.unregister_module(__name__)
    # del bpy.types.Scene.bone_generator_settings
    
if __name__ == "__main__":
    register()