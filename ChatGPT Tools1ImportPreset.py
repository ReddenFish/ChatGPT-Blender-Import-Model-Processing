bl_info = {
    "name": "ChatGPT Tools:修复导入物体",
    "blender": (3, 6, 0),
    "category": "Object",
    "author": "ChatGPT",
    "description": "一组常用的物体操作工具，包括清空父级、删除空物体、缩放物体和合并物体功能。",
    "version": (1, 0, 0),
    "support": "COMMUNITY",
    "tracker_url": "https://github.com/your-repo-url",
    "license": "GPL-3.0",
}
import bpy
import math
import mathutils

class ChatGPTToolsPanel(bpy.types.Panel):
    bl_label = "导入模型预处理"
    bl_idname = "OBJECT_PT_chatgpt_tools"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'ChatGPT 工具'

    def draw(self, context):
        layout = self.layout

        # 添加一键操作按钮，清空父级并删除空物体
        layout.operator("object.clear_parent_and_remove_empty", text="清空父级 & 删除空物体", icon='TRASH')

        # 创建第一行，放置前两个按钮
        row = layout.row(align=True)
        row.operator("object.clear_parent_keep_transform", text="清空父级 & 保持变换")
        row.operator("object.remove_empty_objects", text="删除空物体")
        
        # 创建第二行，放置后两个按钮
        row = layout.row(align=True)
        row.operator("object.scale_objects_small", text="缩放物体至 0.1x")
        row.operator("object.scale_objects_large", text="缩放物体至 10x")

class ClearParentAndRemoveEmptyOperator(bpy.types.Operator):
    bl_idname = "object.clear_parent_and_remove_empty"
    bl_label = "清空父级 & 删除空物体"
    
    def execute(self, context):
        # 清空父级并保持变换
        for obj in context.selected_objects:
            if obj.parent:
                world_matrix = obj.matrix_world
                obj.parent = None
                obj.matrix_world = world_matrix
        
        # 删除所有空物体
        for obj in context.selected_objects:
            if obj.type == 'EMPTY':
                bpy.data.objects.remove(obj)
        
        return {'FINISHED'}

class ClearParentKeepTransformOperator(bpy.types.Operator):
    bl_idname = "object.clear_parent_keep_transform"
    bl_label = "清空父级 & 保持变换"
    
    def execute(self, context):
        for obj in context.selected_objects:
            if obj.parent:
                # 获取物体的当前世界矩阵
                world_matrix = obj.matrix_world
                # 清除父物体并保留世界坐标
                obj.parent = None
                # 设置物体的局部矩阵为其世界矩阵，使其保持相同的空间位置
                obj.matrix_world = world_matrix
        return {'FINISHED'}

class RemoveEmptyObjectsOperator(bpy.types.Operator):
    bl_idname = "object.remove_empty_objects"
    bl_label = "删除空物体"
    
    def execute(self, context):
        for obj in context.selected_objects:
            if obj.type == 'EMPTY':
                bpy.data.objects.remove(obj)
        return {'FINISHED'}

class ScaleObjectsSmallOperator(bpy.types.Operator):
    bl_idname = "object.scale_objects_small"
    bl_label = "缩放物体至 0.1x"
    
    def execute(self, context):
        # 确保选中的物体已经激活
        for obj in context.selected_objects:
            obj.select_set(True)
        context.view_layer.objects.active = context.selected_objects[0]  # 激活第一个物体

        # 使用 bpy.ops.transform.resize 操作来缩小所有选中的物体
        bpy.ops.transform.resize(value=(0.1, 0.1, 0.1))
        
        return {'FINISHED'}

class ScaleObjectsLargeOperator(bpy.types.Operator):
    bl_idname = "object.scale_objects_large"
    bl_label = "缩放物体至 10x"
    
    def execute(self, context):
        # 确保选中的物体已经激活
        for obj in context.selected_objects:
            obj.select_set(True)
        context.view_layer.objects.active = context.selected_objects[0]  # 激活第一个物体

        # 使用 bpy.ops.transform.resize 操作来放大所有选中的物体
        bpy.ops.transform.resize(value=(10.0, 10.0, 10.0))
        
        return {'FINISHED'}

def register():
    bpy.utils.register_class(ChatGPTToolsPanel)
    bpy.utils.register_class(ClearParentAndRemoveEmptyOperator)
    bpy.utils.register_class(ClearParentKeepTransformOperator)
    bpy.utils.register_class(RemoveEmptyObjectsOperator)
    bpy.utils.register_class(ScaleObjectsSmallOperator)
    bpy.utils.register_class(ScaleObjectsLargeOperator)

def unregister():
    bpy.utils.unregister_class(ChatGPTToolsPanel)
    bpy.utils.unregister_class(ClearParentAndRemoveEmptyOperator)
    bpy.utils.unregister_class(ClearParentKeepTransformOperator)
    bpy.utils.unregister_class(RemoveEmptyObjectsOperator)
    bpy.utils.unregister_class(ScaleObjectsSmallOperator)
    bpy.utils.unregister_class(ScaleObjectsLargeOperator)

if __name__ == "__main__":
    register()
