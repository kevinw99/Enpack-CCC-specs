import bpy
sc = bpy.context.scene
sc.render.image_settings.file_format = 'PNG'
sc.render.resolution_x = 960
sc.render.resolution_y = 540
for frame in [1, 75, 150, 225, 300]:
    sc.frame_set(frame)
    sc.render.filepath = f"//spot_check3e/frame_{frame:04d}.png"
    bpy.ops.render.render(write_still=True)
    print(f"Rendered frame {frame}")
print("Done.")
