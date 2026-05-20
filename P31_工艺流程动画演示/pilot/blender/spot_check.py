"""Render a few specific frames in EEVEE to verify composition."""
import bpy

sc = bpy.context.scene
sc.render.filepath = "//spot_check/frame_"
sc.render.image_settings.file_format = 'PNG'
sc.render.resolution_x = 960
sc.render.resolution_y = 540

for frame in [1, 300, 600, 900, 1200, 1500, 1800]:
    sc.frame_set(frame)
    sc.render.filepath = f"//spot_check/frame_{frame:04d}.png"
    bpy.ops.render.render(write_still=True)
    print(f"Rendered frame {frame}")

print("Spot check done.")
