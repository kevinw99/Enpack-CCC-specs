"""
P30 Scene 4B — 36 Evaporation Boats Overhead Layout (10s, 300 frames @30fps)

Top-down view showing two rows of 18 boats each (36 total).
Camera slowly zooms in, boats light up sequentially, dimension labels appear.

Elements:
  - 36 ceramic boats (2 rows x 18) with aluminum pools
  - Dimension annotations: boat size, spacing, row gap
  - Sequential heating animation
  - Labels: 蒸发舟 x36 / 间距 / 排列方式
"""

import bpy
import math
import sys

TOTAL_FRAMES = 300
FPS = 30
BOAT_LENGTH = 0.5    # visual size in Blender units
BOAT_WIDTH = 0.18
BOAT_HEIGHT = 0.12
BOAT_SPACING = 0.65  # center-to-center along row
ROW_GAP = 0.6        # gap between two rows
ROWS = 2
BOATS_PER_ROW = 18


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


def kf_val(obj, data_path, frame, value):
    setattr(obj, data_path, value)
    obj.keyframe_insert(data_path=data_path, frame=frame)


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
    bg.inputs["Color"].default_value = (0.08, 0.08, 0.12, 1.0)
    bg.inputs["Strength"].default_value = 1.0


def setup_camera():
    total_width = BOATS_PER_ROW * BOAT_SPACING
    center_x = (BOATS_PER_ROW - 1) * BOAT_SPACING / 2

    bpy.ops.object.camera_add(location=(center_x, -6, 10))
    cam = bpy.context.active_object
    cam.name = "Camera"
    cam.rotation_euler = (math.radians(30), 0, 0)
    cam.data.lens = 28
    cam.data.type = 'PERSP'
    bpy.context.scene.camera = cam

    kf_loc(cam, 1, (center_x, -6, 10))
    kf_loc(cam, 300, (center_x, -4.5, 8))


def setup_lights():
    total_width = BOATS_PER_ROW * BOAT_SPACING
    center_x = (BOATS_PER_ROW - 1) * BOAT_SPACING / 2

    bpy.ops.object.light_add(type='AREA', location=(center_x, 0, 15))
    key = bpy.context.active_object
    key.name = "KeyOverhead"
    key.data.energy = 800
    key.data.size = 14
    key.data.color = (1.0, 0.98, 0.95)

    bpy.ops.object.light_add(type='AREA', location=(center_x, -3, 8))
    fill = bpy.context.active_object
    fill.name = "FillFront"
    fill.data.energy = 200
    fill.data.size = 10
    fill.data.color = (0.9, 0.92, 1.0)


def create_boat(index, row, col):
    """Create a single evaporation boat with aluminum pool inside."""
    x = col * BOAT_SPACING
    y = (row - 0.5) * (BOAT_WIDTH + ROW_GAP)

    mat_ceramic = make_mat(f"Ceramic_{index}", (0.92, 0.90, 0.85, 1.0),
                           roughness=0.7)
    mat_al = make_mat(f"AlPool_{index}", (0.85, 0.87, 0.90, 1.0),
                      metallic=0.95, roughness=0.1)
    mat_hot = make_mat(f"HotBoat_{index}", (1.0, 0.4, 0.1, 1.0),
                       emission_color=(1.0, 0.5, 0.15, 1.0),
                       emission_strength=0.0)

    bpy.ops.mesh.primitive_cube_add(size=1, location=(x, y, 0))
    boat = bpy.context.active_object
    boat.name = f"Boat_{index}"
    boat.scale = (BOAT_LENGTH / 2, BOAT_WIDTH / 2, BOAT_HEIGHT / 2)
    boat.data.materials.append(mat_ceramic)
    boat.data.materials.append(mat_hot)

    bpy.ops.mesh.primitive_cube_add(size=1, location=(x, y, BOAT_HEIGHT * 0.3))
    pool = bpy.context.active_object
    pool.name = f"Pool_{index}"
    pool.scale = (BOAT_LENGTH * 0.4, BOAT_WIDTH * 0.35, BOAT_HEIGHT * 0.1)
    pool.data.materials.append(mat_al)

    heat_start = 30 + index * 6
    heat_end = min(heat_start + 30, 280)

    emission_node = mat_hot.node_tree.nodes["Principled BSDF"]
    emission_input = emission_node.inputs["Emission Strength"]

    emission_input.default_value = 0.0
    emission_input.keyframe_insert(data_path="default_value", frame=1)
    emission_input.keyframe_insert(data_path="default_value", frame=max(1, heat_start - 1))

    emission_input.default_value = 8.0
    emission_input.keyframe_insert(data_path="default_value", frame=heat_start + 15)

    emission_input.default_value = 5.0
    emission_input.keyframe_insert(data_path="default_value", frame=300)

    return boat, pool


def create_all_boats():
    boats = []
    for row in range(ROWS):
        for col in range(BOATS_PER_ROW):
            index = row * BOATS_PER_ROW + col
            boat, pool = create_boat(index, row, col)
            boats.append(boat)
    return boats


def create_labels():
    mat_label = make_mat("LabelMat", (1.0, 1.0, 1.0, 1.0),
                         emission_color=(1.0, 1.0, 1.0, 1.0),
                         emission_strength=3.0)

    center_x = (BOATS_PER_ROW - 1) * BOAT_SPACING / 2
    labels_data = [
        ("蒸发舟 ×36", (center_x, -1.2, 0.1), 60, 290, 0.35),
        ("18舟/排 × 2排", (center_x, 1.0, 0.1), 90, 290, 0.25),
        ("间距 160mm", (1.5, -0.8, 0.1), 120, 290, 0.2),
    ]

    for text, loc, appear, disappear, size in labels_data:
        bpy.ops.object.text_add(location=loc)
        obj = bpy.context.active_object
        obj.name = f"Lbl_{text[:4]}"
        obj.data.body = text
        obj.data.size = size
        obj.data.align_x = 'CENTER'
        obj.rotation_euler = (0, 0, 0)
        obj.data.materials.append(mat_label)

        kf_scale(obj, 1, (0.01, 0.01, 0.01))
        kf_scale(obj, appear, (0.01, 0.01, 0.01))
        kf_scale(obj, appear + 10, (1, 1, 1))
        kf_scale(obj, disappear, (1, 1, 1))
        kf_scale(obj, min(disappear + 10, 300), (0.01, 0.01, 0.01))


def create_dimension_lines():
    """Add thin lines showing spacing between boats."""
    mat_line = make_mat("DimLine", (0.3, 0.8, 1.0, 1.0),
                        emission_color=(0.3, 0.8, 1.0, 1.0),
                        emission_strength=2.0)

    y_pos = -0.6
    x0 = 0
    x1 = BOAT_SPACING

    bpy.ops.mesh.primitive_cube_add(size=1, location=((x0 + x1) / 2, y_pos, 0.05))
    line = bpy.context.active_object
    line.name = "DimLine_Spacing"
    line.scale = (BOAT_SPACING / 2, 0.001, 0.001)
    line.data.materials.append(mat_line)

    kf_scale(line, 1, (0.01, 0.01, 0.01))
    kf_scale(line, 110, (0.01, 0.01, 0.01))
    kf_scale(line, 125, (BOAT_SPACING / 2, 0.001, 0.001))
    kf_scale(line, 290, (BOAT_SPACING / 2, 0.001, 0.001))
    kf_scale(line, 300, (0.01, 0.01, 0.01))


def main():
    cleanup()
    setup()
    setup_camera()
    setup_lights()
    create_all_boats()
    create_labels()
    create_dimension_lines()

    should_render = "--render" in sys.argv
    if should_render:
        sc = bpy.context.scene
        sc.render.image_settings.file_format = 'PNG'
        sc.render.filepath = "//render4b/frame_"
        bpy.ops.render.render(animation=True)
    else:
        print("Scene 4B built. Use --render to render.")

    bpy.ops.wm.save_as_mainfile(filepath=bpy.path.abspath("//scene4b_36boats.blend"))
    print("Saved scene4b_36boats.blend")


if __name__ == "__main__":
    main()
