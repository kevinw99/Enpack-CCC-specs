import bpy
import sys
import os

prefix = sys.argv[sys.argv.index("--") + 1] if "--" in sys.argv else "spot"
out_dir = f"//{prefix}"

sc = bpy.context.scene
sc.render.image_settings.file_format = 'PNG'
sc.render.resolution_x = 960
sc.render.resolution_y = 540

for frame in [1, 60, 150, 225, 300]:
    sc.frame_set(frame)
    sc.render.filepath = f"{out_dir}/frame_{frame:04d}.png"
    bpy.ops.render.render(write_still=True)
    print(f"Rendered frame {frame}")
print("Done.")
