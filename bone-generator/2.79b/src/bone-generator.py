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
        
        self.layout.operator("object.generate_bone_action", icon="OUTLINER_OB_ARMATURE", text="Generate")

class GenerateBoneAction(Operator):
    """Run generate bone action"""
    bl_idname = "object.generate_bone_action"
    bl_label = "Generate bone"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        scene = context.scene
        ops = bpy.ops
        
        selected = context.selected_objects
        
        ops.object.armature_add()
        
        scene.cursor_location = (0.0, 0.0, 0.0)
        
        bpy.ops.view3d.cursor3d('INVOKE_DEFAULT')
        
        armature = context.active_object
        
        bpy.ops.object.mode_set(mode='EDIT')
        
        armature.data.bones['Bone'].name = 'root'
        
        
        for obj in selected:
            
            armature.select = True
            
            scene.objects.active = armature
            
            bpy.ops.object.mode_set(mode='EDIT')
            
            edit_bones = armature.data.edit_bones
            
            obj_bone = edit_bones.new(obj.name + '_bone')
            
            obj_bone.head = (obj.location.x, obj.location.y, obj.location.z)
            
            obj_bone.tail = (obj.location.x, obj.location.y, obj.location.z + 1.0)
            
            armature.data.edit_bones.active = armature.data.edit_bones[obj_bone.name]
            
            obj_bone.parent = edit_bones['root']
            
            bpy.ops.object.mode_set(mode='OBJECT')
            
            bpy.ops.object.select_all(action='DESELECT')
            
            obj.select = True
            
            armature.select = True
            
            scene.objects.active = armature
            
            bpy.ops.object.parent_set(type="BONE", keep_transform=True)
        
        
        
        for obj in selected:
            
            scene.objects.active = obj
            
            
            
            # print(edit_bones)
                
        return {'FINISHED'}

def register():
    bpy.utils.register_module(__name__)
    
def unregister():
    bpy.utils.unregister_module(__name__)
    
if __name__ == "__main__":
    register()