"""
Quick viewport render of scene3_pvd.blend — outputs OpenGL preview frames.
Much faster than full EEVEE render (~100x).
"""
import bpy

sc = bpy.context.scene
sc.render.filepath = "//render3_viewport/frame_"
sc.render.image_settings.file_format = 'PNG'
sc.render.resolution_x = 1920
sc.render.resolution_y = 1080

# Use solid/material preview shading for viewport render
for area in bpy.context.screen.areas if hasattr(bpy.context, 'screen') and bpy.context.screen else []:
    if area.type == 'VIEW_3D':
        area.spaces[0].shading.type = 'MATERIAL'

bpy.ops.render.opengl(animation=True)
print("Viewport render complete.")
