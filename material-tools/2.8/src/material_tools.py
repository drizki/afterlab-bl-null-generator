bl_info = {
    "name": "Material Tools",
    "description": "Material related tools",
    "author": "Dwi Rizki Irawan",
    "version": (0, 0, 1),
    "blender": (2, 80, 0),
    "category": "Material"
}

import bpy

from bpy.types import (Panel, Operator)

#===========================================================
# UI Panel
#===========================================================

class PANEL_PT_material_tools(Panel):
    """Material Tools Panel"""
    bl_label = "Material Tools"
    bl_idname = "PANEL_PT_material_tools"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "material"

    def draw(self, context):
        layout = self.layout
        row = layout.row()
        row.operator("material.reset_metallic_value", icon="MATERIAL_DATA", text="Reset Metallic")

#===========================================================
# Reset Material Metallic Operator (Principled BSDF)
#===========================================================
class MATERIAL_OT_reset_metallic_value(Operator):
    
    bl_idname="material.reset_metallic_value"
    bl_label="Reset metallic value to zero"
    bl_description="Reset metallic value to zero"
    
    def execute(self, context):
        scene = context.scene
        selected = context.selected_objects
        replaced = 0

        for obj in selected:
            materials = obj.data.materials
            for material in materials:
                shadder = material.node_tree.nodes['Principled BSDF']
                shadder.inputs[4].default_value = 0
                replaced += 1
        message = "Replaced " + str(replaced) + " values!"
        self.report({'INFO'}, message)
        return {'FINISHED'}


def register():
    bpy.utils.register_class(PANEL_PT_material_tools)
    bpy.utils.register_class(MATERIAL_OT_reset_metallic_value)


def unregister():
    bpy.utils.unregister_class(PANEL_PT_material_tools)
    bpy.utils.unregister_class(MATERIAL_OT_reset_metallic_value)

if __name__ == "__main__":
    register()
