"""
P30 Scene 5B — Defect Micro Mechanisms (10s, 300 frames @30fps)

Three-panel split showing the three splash/defect mechanisms:
  Left:   气泡核化 — bubble nucleation in aluminum pool
  Center: 送丝冲击 — wire feed impact on liquid surface
  Right:  舟间热辐射 — inter-boat thermal radiation causing edge boiling

Each panel shows the mechanism + flying droplets hitting the film above.
"""

import bpy
import math
import sys
import random

TOTAL_FRAMES = 300
FPS = 30

PANEL_WIDTH = 2.0
PANEL_GAP = 0.3
PANEL_CENTERS = [
    -(PANEL_WIDTH + PANEL_GAP),
    0,
    (PANEL_WIDTH + PANEL_GAP),
]


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
    bg.inputs["Color"].default_value = (0.05, 0.05, 0.08, 1.0)
    bg.inputs["Strength"].default_value = 1.0


def setup_camera():
    bpy.ops.object.camera_add(location=(0, -7, 1.5))
    cam = bpy.context.active_object
    cam.name = "Camera"
    cam.rotation_euler = (math.radians(82), 0, 0)
    cam.data.lens = 28
    bpy.context.scene.camera = cam


def setup_lights():
    bpy.ops.object.light_add(type='AREA', location=(0, -4, 5))
    key = bpy.context.active_object
    key.name = "Key"
    key.data.energy = 400
    key.data.size = 8
    key.data.color = (1.0, 0.98, 0.95)

    for i, cx in enumerate(PANEL_CENTERS):
        bpy.ops.object.light_add(type='POINT', location=(cx, 0, -1.5))
        warm = bpy.context.active_object
        warm.name = f"WarmLight_{i}"
        warm.data.energy = 50
        warm.data.color = (1.0, 0.6, 0.3)


def create_panel_base(cx, panel_name):
    """Create boat (bottom) and film (top) for one panel."""
    mat_boat = make_mat(f"Boat_{panel_name}", (0.85, 0.82, 0.75, 1.0),
                        roughness=0.6,
                        emission_color=(1.0, 0.5, 0.2, 1.0),
                        emission_strength=3.0)
    mat_al = make_mat(f"Al_{panel_name}", (0.85, 0.87, 0.90, 1.0),
                      metallic=0.95, roughness=0.08,
                      emission_color=(1.0, 0.7, 0.3, 1.0),
                      emission_strength=1.0)
    mat_film = make_mat(f"Film_{panel_name}", (0.5, 0.45, 0.7, 0.5),
                        alpha=0.5, roughness=0.15,
                        emission_color=(0.4, 0.4, 0.6, 1.0),
                        emission_strength=0.5)

    bpy.ops.mesh.primitive_cube_add(size=1, location=(cx, 0, -1.0))
    boat = bpy.context.active_object
    boat.name = f"Boat_{panel_name}"
    boat.scale = (0.8, 0.5, 0.15)
    boat.data.materials.append(mat_boat)

    bpy.ops.mesh.primitive_cube_add(size=1, location=(cx, 0, -0.8))
    pool = bpy.context.active_object
    pool.name = f"Pool_{panel_name}"
    pool.scale = (0.7, 0.4, 0.05)
    pool.data.materials.append(mat_al)

    bpy.ops.mesh.primitive_plane_add(size=2.0, location=(cx, 0, 2.0))
    film = bpy.context.active_object
    film.name = f"Film_{panel_name}"
    film.data.materials.append(mat_film)

    return boat, pool, film


def create_droplets(cx, panel_name, start_frame, count=8):
    """Animated droplets flying from pool up to film."""
    mat_drop = make_mat(f"Drop_{panel_name}", (0.9, 0.92, 0.95, 0.9),
                        metallic=0.9, roughness=0.05,
                        emission_color=(1.0, 0.8, 0.4, 1.0),
                        emission_strength=4.0)

    for i in range(count):
        launch = start_frame + i * 20 + random.randint(-5, 5)
        launch = max(10, min(260, launch))
        land = launch + random.randint(15, 30)

        sx = cx + random.uniform(-0.4, 0.4)
        sy = random.uniform(-0.3, 0.3)
        ex = sx + random.uniform(-0.3, 0.3)
        ey = sy + random.uniform(-0.2, 0.2)

        bpy.ops.mesh.primitive_uv_sphere_add(
            segments=10, ring_count=6,
            radius=0.04, location=(sx, sy, -0.75))
        drop = bpy.context.active_object
        drop.name = f"Drop_{panel_name}_{i}"
        drop.data.materials.append(mat_drop)

        kf_scale(drop, 1, (0.01, 0.01, 0.01))
        kf_scale(drop, launch - 1, (0.01, 0.01, 0.01))
        kf_scale(drop, launch, (1, 1, 1))
        kf_loc(drop, launch, (sx, sy, -0.75))
        kf_loc(drop, land, (ex, ey, 1.95))
        kf_scale(drop, land, (1, 1, 1))
        kf_scale(drop, land + 5, (1.5, 1.5, 0.3))


def create_bubble_mechanism(cx):
    """Panel 1: bubble nucleation — bubbles rise and burst."""
    mat_bubble = make_mat("Bubble", (0.7, 0.75, 0.85, 0.3),
                          alpha=0.3, roughness=0.05,
                          emission_color=(1.0, 0.9, 0.7, 1.0),
                          emission_strength=2.0)

    for i in range(6):
        start = 40 + i * 35
        bx = cx + random.uniform(-0.3, 0.3)
        by = random.uniform(-0.2, 0.2)

        bpy.ops.mesh.primitive_uv_sphere_add(
            segments=16, ring_count=10,
            radius=0.08, location=(bx, by, -0.9))
        bubble = bpy.context.active_object
        bubble.name = f"Bubble_{i}"
        bubble.data.materials.append(mat_bubble)

        kf_scale(bubble, 1, (0.01, 0.01, 0.01))
        kf_scale(bubble, start, (0.01, 0.01, 0.01))
        kf_scale(bubble, start + 10, (1, 1, 1))
        kf_loc(bubble, start, (bx, by, -0.9))
        kf_loc(bubble, start + 20, (bx, by, -0.7))
        kf_scale(bubble, start + 20, (1.3, 1.3, 1.3))
        kf_scale(bubble, start + 25, (2.0, 2.0, 0.1))

    create_droplets(cx, "bubble", start_frame=60, count=8)


def create_wire_mechanism(cx):
    """Panel 2: wire feed impact — wire enters pool, causes splash."""
    mat_wire = make_mat("Wire", (0.8, 0.82, 0.85, 1.0),
                        metallic=0.9, roughness=0.2)

    bpy.ops.mesh.primitive_cylinder_add(
        radius=0.015, depth=3.0,
        location=(cx, 0, 0.5))
    wire = bpy.context.active_object
    wire.name = "AlWire"
    wire.data.materials.append(mat_wire)

    kf_loc(wire, 1, (cx, 0, 1.5))
    kf_loc(wire, 80, (cx, 0, 0.5))
    kf_loc(wire, 150, (cx, 0, -0.2))
    kf_loc(wire, 220, (cx, 0, -0.5))

    create_droplets(cx, "wire", start_frame=80, count=10)


def create_radiation_mechanism(cx):
    """Panel 3: inter-boat thermal radiation — neighboring boat heats edge."""
    mat_neighbor = make_mat("NeighborBoat", (0.85, 0.82, 0.75, 1.0),
                            roughness=0.6,
                            emission_color=(1.0, 0.4, 0.1, 1.0),
                            emission_strength=6.0)

    bpy.ops.mesh.primitive_cube_add(size=1, location=(cx + 1.2, 0, -1.0))
    neighbor = bpy.context.active_object
    neighbor.name = "NeighborBoat"
    neighbor.scale = (0.3, 0.5, 0.15)
    neighbor.data.materials.append(mat_neighbor)

    mat_arrow = make_mat("RadArrow", (1.0, 0.3, 0.1, 0.7),
                         alpha=0.7,
                         emission_color=(1.0, 0.3, 0.1, 1.0),
                         emission_strength=5.0)

    for i in range(3):
        y_off = (i - 1) * 0.2
        bpy.ops.mesh.primitive_cube_add(size=1,
                                         location=(cx + 0.7, y_off, -0.95))
        arrow = bpy.context.active_object
        arrow.name = f"RadArrow_{i}"
        arrow.scale = (0.3, 0.02, 0.02)
        arrow.data.materials.append(mat_arrow)

        kf_scale(arrow, 1, (0.01, 0.01, 0.01))
        kf_scale(arrow, 60, (0.01, 0.01, 0.01))
        kf_scale(arrow, 80, (0.3, 0.02, 0.02))

    create_droplets(cx, "radiation", start_frame=90, count=6)


def create_panel_labels():
    mat_label = make_mat("LabelMat", (1.0, 1.0, 1.0, 1.0),
                         emission_color=(1.0, 1.0, 1.0, 1.0),
                         emission_strength=3.0)

    labels = [
        ("气泡核化", PANEL_CENTERS[0], 30),
        ("送丝冲击", PANEL_CENTERS[1], 30),
        ("舟间热辐射", PANEL_CENTERS[2], 30),
    ]

    for text, cx, appear in labels:
        bpy.ops.object.text_add(location=(cx, -1.5, 2.8))
        obj = bpy.context.active_object
        obj.name = f"Lbl_{text}"
        obj.data.body = text
        obj.data.size = 0.25
        obj.data.align_x = 'CENTER'
        obj.rotation_euler = (math.radians(90), 0, 0)
        obj.data.materials.append(mat_label)

        kf_scale(obj, 1, (0.01, 0.01, 0.01))
        kf_scale(obj, appear, (0.01, 0.01, 0.01))
        kf_scale(obj, appear + 10, (1, 1, 1))


def create_dividers():
    """Vertical dividing lines between panels."""
    mat_div = make_mat("Divider", (0.3, 0.3, 0.4, 0.5), alpha=0.5,
                       emission_color=(0.3, 0.3, 0.5, 1.0),
                       emission_strength=1.0)

    for x_off in [-PANEL_GAP / 2 - PANEL_WIDTH / 2, PANEL_GAP / 2 + PANEL_WIDTH / 2]:
        bpy.ops.mesh.primitive_cube_add(size=1, location=(x_off, -3, 1.0))
        div = bpy.context.active_object
        div.name = f"Div_{x_off:.1f}"
        div.scale = (0.005, 0.005, 2.5)
        div.data.materials.append(mat_div)


def main():
    cleanup()
    setup()
    setup_camera()
    setup_lights()

    for cx in PANEL_CENTERS:
        create_panel_base(cx, f"P{PANEL_CENTERS.index(cx)}")

    create_bubble_mechanism(PANEL_CENTERS[0])
    create_wire_mechanism(PANEL_CENTERS[1])
    create_radiation_mechanism(PANEL_CENTERS[2])
    create_panel_labels()
    create_dividers()

    should_render = "--render" in sys.argv
    if should_render:
        sc = bpy.context.scene
        sc.render.image_settings.file_format = 'PNG'
        sc.render.filepath = "//render5b/frame_"
        bpy.ops.render.render(animation=True)
    else:
        print("Scene 5B built. Use --render to render.")

    bpy.ops.wm.save_as_mainfile(filepath=bpy.path.abspath("//scene5b_defect_micro.blend"))
    print("Saved scene5b_defect_micro.blend")


if __name__ == "__main__":
    main()
