"""
P30 Scene 3E — Atomic Deposition Micro View (10s, 300 frames @30fps)

Shows aluminum atoms depositing onto polymer film surface.
Reference: ref_0006.png / ref_0007.png from reference video.

Elements:
  - Film surface (top, semi-transparent blue/purple plane)
  - Aluminum atoms (silver spheres) flying up and attaching
  - Growing aluminum layer on film underside
  - Labels: 薄膜 / 原子层 / 铝膜
"""

import bpy
import math
import sys
import random

TOTAL_FRAMES = 300
FPS = 30

def cleanup():
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete(use_global=False)
    for block in [bpy.data.materials, bpy.data.meshes]:
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
    bg.inputs["Color"].default_value = (0.15, 0.12, 0.25, 1.0)
    bg.inputs["Strength"].default_value = 1.0

def setup_camera():
    # Target empty at the atom grid center
    bpy.ops.object.empty_add(type='PLAIN_AXES', location=(0, 0, 1.5))
    target = bpy.context.active_object
    target.name = "CamTarget"

    bpy.ops.object.camera_add(location=(4, -6, -1))
    cam = bpy.context.active_object
    cam.name = "Camera"
    bpy.context.scene.camera = cam
    cam.data.lens = 28

    # Track To constraint: camera always looks at target
    track = cam.constraints.new('TRACK_TO')
    track.target = target
    track.track_axis = 'TRACK_NEGATIVE_Z'
    track.up_axis = 'UP_Y'

    kf_loc(cam, 1, (4, -6, -1))
    kf_loc(cam, 300, (2, -6.5, 0.5))

def setup_lights():
    bpy.ops.object.light_add(type='AREA', location=(3, -5, 4))
    key = bpy.context.active_object
    key.name = "Key"
    key.data.energy = 400
    key.data.size = 6
    key.data.color = (1.0, 0.98, 0.95)

    bpy.ops.object.light_add(type='AREA', location=(-3, -3, -3))
    fill = bpy.context.active_object
    fill.name = "Fill"
    fill.data.energy = 150
    fill.data.size = 5
    fill.data.color = (0.85, 0.88, 1.0)

    # Warm light from below (simulating boat glow)
    bpy.ops.object.light_add(type='AREA', location=(0, 0, -5))
    warm = bpy.context.active_object
    warm.name = "WarmBelow"
    warm.data.energy = 100
    warm.data.size = 8
    warm.data.color = (1.0, 0.7, 0.4)

def create_film():
    """Semi-transparent film surface at the top."""
    mat = make_mat("Film", (0.6, 0.55, 0.85, 0.6), alpha=0.6, roughness=0.15,
                   emission_color=(0.5, 0.45, 0.7, 1.0), emission_strength=0.5)

    bpy.ops.mesh.primitive_plane_add(size=14, location=(0, 0, 2.0))
    film = bpy.context.active_object
    film.name = "Film"
    film.data.materials.append(mat)
    return film

def create_deposited_layer():
    """Aluminum layer growing on bottom of film."""
    mat = make_mat("AlLayer", (0.88, 0.9, 0.92, 1.0), metallic=0.95, roughness=0.08)

    bpy.ops.mesh.primitive_plane_add(size=14, location=(0, 0, 1.95))
    layer = bpy.context.active_object
    layer.name = "AlLayer"
    layer.data.materials.append(mat)

    # Grow from thin to visible thickness
    kf_scale(layer, 1, (1, 1, 0.01))
    kf_scale(layer, 300, (1, 1, 0.15))
    return layer

def create_deposited_atoms_grid():
    """Pre-placed atoms on the film surface that are already deposited."""
    mat = make_mat("DepositedAtom", (0.82, 0.84, 0.88, 1.0),
                   metallic=0.9, roughness=0.15)
    atoms = []

    grid_range = 5
    for ix in range(-grid_range, grid_range + 1):
        for iy in range(-grid_range, grid_range + 1):
            x = ix * 0.35 + random.uniform(-0.05, 0.05)
            y = iy * 0.35 + random.uniform(-0.05, 0.05)
            z = 1.85 + random.uniform(-0.02, 0.02)

            bpy.ops.mesh.primitive_uv_sphere_add(
                segments=12, ring_count=8,
                radius=0.12, location=(x, y, z))
            a = bpy.context.active_object
            a.name = f"DepAtom_{ix}_{iy}"
            a.data.materials.append(mat)
            atoms.append(a)

    return atoms

def create_flying_atoms():
    """Atoms that fly up from below and land on the film."""
    mat_fly = make_mat("FlyingAtom", (0.9, 0.92, 0.95, 0.9),
                       metallic=0.85, roughness=0.1,
                       emission_color=(1.0, 0.8, 0.5, 1.0),
                       emission_strength=2.0)

    atoms = []
    num_atoms = 40

    for i in range(num_atoms):
        landing_x = random.uniform(-4, 4)
        landing_y = random.uniform(-4, 4)
        landing_z = 1.85

        start_x = landing_x + random.uniform(-1.5, 1.5)
        start_y = landing_y + random.uniform(-1.0, 1.0)
        start_z = random.uniform(-4, -2)

        bpy.ops.mesh.primitive_uv_sphere_add(
            segments=12, ring_count=8,
            radius=0.12, location=(start_x, start_y, start_z))
        a = bpy.context.active_object
        a.name = f"FlyAtom_{i}"
        a.data.materials.append(mat_fly)

        # Stagger arrival times across the 10 seconds
        arrive_frame = int(20 + i * (250 / num_atoms)) + random.randint(-5, 5)
        arrive_frame = max(10, min(280, arrive_frame))

        flight_duration = random.randint(25, 50)
        depart_frame = arrive_frame - flight_duration

        # Hidden before departure
        kf_scale(a, 1, (0.01, 0.01, 0.01))
        kf_scale(a, max(1, depart_frame - 1), (0.01, 0.01, 0.01))
        kf_scale(a, max(2, depart_frame), (1, 1, 1))

        # Fly from below to film
        kf_loc(a, max(1, depart_frame), (start_x, start_y, start_z))
        kf_loc(a, arrive_frame, (landing_x, landing_y, landing_z))

        # Stay put after landing
        kf_loc(a, 300, (landing_x, landing_y, landing_z))
        kf_scale(a, arrive_frame, (1, 1, 1))
        kf_scale(a, 300, (1, 1, 1))

        atoms.append(a)

    return atoms

def create_labels():
    mat_dark = make_mat("LabelWhite", (1.0, 1.0, 1.0, 1.0),
                        emission_color=(1.0, 1.0, 1.0, 1.0), emission_strength=2.0)

    def add_label(text, loc, appear, disappear, size=0.35, name="Lbl"):
        bpy.ops.object.text_add(location=loc)
        obj = bpy.context.active_object
        obj.name = name
        obj.data.body = text
        obj.data.size = size
        obj.data.align_x = 'LEFT'
        obj.rotation_euler = (math.radians(90), 0, 0)
        obj.data.materials.append(mat_dark)

        kf_scale(obj, 1, (0.01, 0.01, 0.01))
        kf_scale(obj, appear, (0.01, 0.01, 0.01))
        kf_scale(obj, appear + 10, (1, 1, 1))
        kf_scale(obj, disappear - 10, (1, 1, 1))
        kf_scale(obj, disappear, (0.01, 0.01, 0.01))

    add_label("薄膜", (-6.5, -3, 2.5), 30, 290, size=0.4, name="Lbl_Film")
    add_label("原子层", (-6.5, -3, 1.5), 60, 290, size=0.4, name="Lbl_AtomLayer")
    add_label("铝膜", (-6.5, -3, 0.8), 150, 290, size=0.4, name="Lbl_AlFilm")

def main():
    cleanup()
    setup()
    setup_camera()
    setup_lights()
    create_film()
    create_deposited_layer()
    create_deposited_atoms_grid()
    create_flying_atoms()
    create_labels()

    should_render = "--render" in sys.argv
    if should_render:
        sc = bpy.context.scene
        sc.render.image_settings.file_format = 'PNG'
        sc.render.filepath = "//render3e/frame_"
        bpy.ops.render.render(animation=True)
    else:
        print("Scene 3E built. Spot check or render.")

    bpy.ops.wm.save_as_mainfile(filepath=bpy.path.abspath("//scene3e_atomic.blend"))
    print("Saved scene3e_atomic.blend")

if __name__ == "__main__":
    main()
