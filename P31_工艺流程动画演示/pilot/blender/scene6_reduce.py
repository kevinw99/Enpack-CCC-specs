"""
P30 Scene 6 — Boat Reduction Comparison (10s, 300 frames @30fps)

Split-screen: left = 36 boats (hot, red), right = 18 boats (cooler, green).
Animated defect count bar chart appears at bottom.
Shows that reducing boats reduces thermal radiation → fewer defects.

Layout:
  Left panel:  36 boats (6×6 grid), red glow, defect count ~45
  Right panel: 18 boats (6×3 grid), blue-green glow, defect count ~12
  Bottom: animated bar chart comparing defect counts
"""

import bpy
import math
import sys

TOTAL_FRAMES = 300
FPS = 30


def cleanup():
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete(use_global=False)
    for block in [bpy.data.materials, bpy.data.meshes, bpy.data.fonts]:
        for item in block:
            block.remove(item)


def make_mat(name, color, metallic=0.0, roughness=0.5, alpha=1.0,
             emission_color=None, emission_strength=0.0):
    mat = bpy.data.materials.new(name)
    mat.use_nodes = True
    bsdf = mat.node_tree.nodes["Principled BSDF"]
    bsdf.inputs["Base Color"].default_value = color
    bsdf.inputs["Metallic"].default_value = metallic
    bsdf.inputs["Roughness"].default_value = roughness
    if alpha < 1.0:
        bsdf.inputs["Alpha"].default_value = alpha
        mat.surface_render_method = 'BLENDED'
    if emission_color and emission_strength > 0:
        bsdf.inputs["Emission Color"].default_value = emission_color
        bsdf.inputs["Emission Strength"].default_value = emission_strength
    return mat


def kf_loc(obj, frame, loc):
    obj.location = loc
    obj.keyframe_insert(data_path="location", frame=frame)


def kf_scale(obj, frame, sc):
    obj.scale = sc
    obj.keyframe_insert(data_path="scale", frame=frame)


def setup():
    sc = bpy.context.scene
    sc.frame_start = 1
    sc.frame_end = TOTAL_FRAMES
    sc.render.fps = FPS
    sc.render.resolution_x = 1920
    sc.render.resolution_y = 1080
    sc.render.film_transparent = False

    world = bpy.data.worlds.get("World") or bpy.data.worlds.new("World")
    sc.world = world
    world.use_nodes = True
    bg = world.node_tree.nodes["Background"]
    bg.inputs["Color"].default_value = (0.06, 0.06, 0.10, 1.0)
    bg.inputs["Strength"].default_value = 1.0


def setup_camera():
    bpy.ops.object.camera_add(location=(0, -8, 4))
    cam = bpy.context.active_object
    cam.name = "Camera"
    cam.rotation_euler = (math.radians(65), 0, 0)
    cam.data.lens = 32
    bpy.context.scene.camera = cam


def setup_lights():
    bpy.ops.object.light_add(type='AREA', location=(0, -3, 6))
    key = bpy.context.active_object
    key.name = "Key"
    key.data.energy = 400
    key.data.size = 8
    key.data.color = (1.0, 0.98, 0.95)

    bpy.ops.object.light_add(type='AREA', location=(-3, 0, 3))
    fill_l = bpy.context.active_object
    fill_l.name = "FillLeft"
    fill_l.data.energy = 60
    fill_l.data.size = 4
    fill_l.data.color = (1.0, 0.7, 0.5)

    bpy.ops.object.light_add(type='AREA', location=(3, 0, 3))
    fill_r = bpy.context.active_object
    fill_r.name = "FillRight"
    fill_r.data.energy = 60
    fill_r.data.size = 4
    fill_r.data.color = (0.5, 0.9, 0.7)


def create_boat_grid(cx, rows, cols, spacing, color, emission_color, emission_str, prefix):
    """Create a grid of boats centered at cx."""
    mat = make_mat(f"Boat_{prefix}", color, roughness=0.6,
                   emission_color=emission_color,
                   emission_strength=emission_str)

    boats = []
    for r in range(rows):
        for c in range(cols):
            x = cx + (c - (cols - 1) / 2) * spacing
            y = (r - (rows - 1) / 2) * (spacing * 0.6)

            bpy.ops.mesh.primitive_cube_add(size=1, location=(x, y, 0))
            boat = bpy.context.active_object
            boat.name = f"{prefix}_boat_{r}_{c}"
            boat.scale = (0.18, 0.06, 0.03)
            boat.data.materials.append(mat)

            heat_frame = 20 + (r * cols + c) * 3
            kf_scale(boat, 1, (0.01, 0.01, 0.01))
            kf_scale(boat, heat_frame, (0.01, 0.01, 0.01))
            kf_scale(boat, heat_frame + 10, (0.18, 0.06, 0.03))

            boats.append(boat)

    return boats


def create_bar_chart():
    """Animated bar chart at bottom: 36舟=45 defects vs 18舟=12 defects."""
    mat_red = make_mat("BarRed", (0.9, 0.2, 0.15, 1.0),
                       emission_color=(1.0, 0.3, 0.1, 1.0),
                       emission_strength=2.0)
    mat_green = make_mat("BarGreen", (0.15, 0.8, 0.4, 1.0),
                         emission_color=(0.2, 0.9, 0.4, 1.0),
                         emission_strength=2.0)
    mat_label = make_mat("BarLabel", (1.0, 1.0, 1.0, 1.0),
                         emission_color=(1.0, 1.0, 1.0, 1.0),
                         emission_strength=3.0)

    chart_y = -3.0
    chart_z = 0
    bar_appear = 160

    bar_height_36 = 1.8
    bar_height_18 = 0.5

    bpy.ops.mesh.primitive_cube_add(size=1, location=(-1.2, chart_y, chart_z))
    bar36 = bpy.context.active_object
    bar36.name = "Bar_36"
    bar36.data.materials.append(mat_red)

    kf_scale(bar36, 1, (0.3, 0.15, 0.01))
    kf_scale(bar36, bar_appear, (0.3, 0.15, 0.01))
    kf_scale(bar36, bar_appear + 30, (0.3, 0.15, bar_height_36))
    kf_loc(bar36, bar_appear, (-1.2, chart_y, chart_z))
    kf_loc(bar36, bar_appear + 30, (-1.2, chart_y, chart_z + bar_height_36 / 2))

    bpy.ops.mesh.primitive_cube_add(size=1, location=(1.2, chart_y, chart_z))
    bar18 = bpy.context.active_object
    bar18.name = "Bar_18"
    bar18.data.materials.append(mat_green)

    kf_scale(bar18, 1, (0.3, 0.15, 0.01))
    kf_scale(bar18, bar_appear + 15, (0.3, 0.15, 0.01))
    kf_scale(bar18, bar_appear + 45, (0.3, 0.15, bar_height_18))
    kf_loc(bar18, bar_appear + 15, (1.2, chart_y, chart_z))
    kf_loc(bar18, bar_appear + 45, (1.2, chart_y, chart_z + bar_height_18 / 2))

    labels = [
        ("36舟", (-1.2, chart_y - 0.5, chart_z - 0.1), bar_appear),
        ("45个凹凸点", (-1.2, chart_y, chart_z + bar_height_36 + 0.3), bar_appear + 30),
        ("18舟", (1.2, chart_y - 0.5, chart_z - 0.1), bar_appear + 15),
        ("12个凹凸点", (1.2, chart_y, chart_z + bar_height_18 + 0.3), bar_appear + 45),
        ("↓ 73%", (0, chart_y, chart_z + 1.5), bar_appear + 60),
    ]

    for text, loc, appear in labels:
        bpy.ops.object.text_add(location=loc)
        obj = bpy.context.active_object
        obj.name = f"ChartLbl_{text[:4]}"
        obj.data.body = text
        obj.data.size = 0.2
        obj.data.align_x = 'CENTER'
        obj.rotation_euler = (math.radians(90), 0, 0)
        obj.data.materials.append(mat_label)

        kf_scale(obj, 1, (0.01, 0.01, 0.01))
        kf_scale(obj, appear, (0.01, 0.01, 0.01))
        kf_scale(obj, appear + 10, (1, 1, 1))


def create_panel_labels():
    mat_label = make_mat("PanelLabel", (1.0, 1.0, 1.0, 1.0),
                         emission_color=(1.0, 1.0, 1.0, 1.0),
                         emission_strength=3.0)

    for text, x, appear in [("原方案：36舟", -2.0, 20), ("优化方案：18舟", 2.0, 20)]:
        bpy.ops.object.text_add(location=(x, -4.5, 2.5))
        obj = bpy.context.active_object
        obj.name = f"PanelLbl_{text[:4]}"
        obj.data.body = text
        obj.data.size = 0.22
        obj.data.align_x = 'CENTER'
        obj.rotation_euler = (math.radians(65), 0, 0)
        obj.data.materials.append(mat_label)

        kf_scale(obj, 1, (0.01, 0.01, 0.01))
        kf_scale(obj, appear, (0.01, 0.01, 0.01))
        kf_scale(obj, appear + 10, (1, 1, 1))


def create_divider():
    mat_div = make_mat("Divider", (0.3, 0.3, 0.5, 0.5), alpha=0.5,
                       emission_color=(0.4, 0.4, 0.6, 1.0),
                       emission_strength=1.0)
    bpy.ops.mesh.primitive_cube_add(size=1, location=(0, -1, 1))
    div = bpy.context.active_object
    div.name = "Divider"
    div.scale = (0.005, 4, 2.5)
    div.data.materials.append(mat_div)


def main():
    cleanup()
    setup()
    setup_camera()
    setup_lights()

    create_boat_grid(cx=-2.5, rows=6, cols=6, spacing=0.45,
                     color=(0.9, 0.85, 0.75, 1.0),
                     emission_color=(1.0, 0.35, 0.1, 1.0),
                     emission_str=4.0, prefix="L36")

    create_boat_grid(cx=2.5, rows=3, cols=6, spacing=0.45,
                     color=(0.85, 0.9, 0.85, 1.0),
                     emission_color=(0.2, 0.8, 0.4, 1.0),
                     emission_str=3.0, prefix="R18")

    create_bar_chart()
    create_panel_labels()
    create_divider()

    should_render = "--render" in sys.argv
    if should_render:
        sc = bpy.context.scene
        sc.render.image_settings.file_format = 'PNG'
        sc.render.filepath = "//render6/frame_"
        bpy.ops.render.render(animation=True)
    else:
        print("Scene 6 built. Use --render to render.")

    bpy.ops.wm.save_as_mainfile(filepath=bpy.path.abspath("//scene6_reduce.blend"))
    print("Saved scene6_reduce.blend")


if __name__ == "__main__":
    main()
