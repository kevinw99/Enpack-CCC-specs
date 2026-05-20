"""
Quick preview: 640x360, Workbench engine, every 3rd frame only.
1800 frames / 3 = 600 frames at low res → should take ~2 min.
"""
import bpy

sc = bpy.context.scene
sc.render.filepath = "//render3_preview/frame_"
sc.render.image_settings.file_format = 'PNG'
sc.render.resolution_x = 640
sc.render.resolution_y = 360
sc.render.resolution_percentage = 100
sc.frame_step = 3

sc.render.engine = 'BLENDER_WORKBENCH'

bpy.ops.render.render(animation=True)
print("Quick preview done.")
