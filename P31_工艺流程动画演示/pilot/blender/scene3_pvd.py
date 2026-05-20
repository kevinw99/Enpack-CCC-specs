"""
P30 Scene 3 — PVD 蒸镀原理 (60s, 1800 frames @30fps)

Elements:
  - Vacuum chamber (cross-section)
  - Evaporation boats (row of 6) that glow hot
  - Aluminum vapor particles rising
  - Polymer film moving across the top (conveyor belt)
  - Deposition visualization
  - Camera: establishing shot → zoom to boats → pull back

Usage:
  blender --background --python scene3_pvd.py
  blender --background --python scene3_pvd.py -- --render
"""

import bpy
import bmesh
import math
import sys
import random

# ---------------------------------------------------------------------------
# Config
# ---------------------------------------------------------------------------
TOTAL_FRAMES = 1800
FPS = 30

# Chamber dimensions
CHAMBER_W = 12.0
CHAMBER_H = 8.0
CHAMBER_D = 6.0

# Boats
NUM_BOATS = 6
BOAT_W = 1.2
BOAT_D = 0.3
BOAT_H = 0.2
BOAT_Y = -CHAMBER_H / 2 + 0.5

# Film
FILM_Y = CHAMBER_H / 2 - 1.5
FILM_THICKNESS = 0.03
ROLLER_RADIUS = 0.4

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def cleanup():
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete(use_global=False)
    for block in [bpy.data.materials, bpy.data.meshes, bpy.data.particles]:
        for item in block:
            block.remove(item)

def make_mat(name, color, emission_color=None, emission_strength=0.0, alpha=1.0, metallic=0.0, roughness=0.5):
    mat = bpy.data.materials.new(name)
    mat.use_nodes = True
    nodes = mat.node_tree.nodes
    links = mat.node_tree.links
    bsdf = nodes["Principled BSDF"]
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

def kf_emission(mat, frame, strength):
    bsdf = mat.node_tree.nodes["Principled BSDF"]
    bsdf.inputs["Emission Strength"].default_value = strength
    bsdf.inputs["Emission Strength"].keyframe_insert("default_value", frame=frame)

def kf_loc(obj, frame, loc):
    obj.location = loc
    obj.keyframe_insert(data_path="location", frame=frame)

def kf_scale(obj, frame, sc):
    obj.scale = sc
    obj.keyframe_insert(data_path="scale", frame=frame)

def kf_rot(obj, frame, rot):
    obj.rotation_euler = rot
    obj.keyframe_insert(data_path="rotation_euler", frame=frame)

# ---------------------------------------------------------------------------
# Scene Setup
# ---------------------------------------------------------------------------

def setup_scene():
    sc = bpy.context.scene
    sc.frame_start = 1
    sc.frame_end = TOTAL_FRAMES
    sc.render.fps = FPS
    sc.render.resolution_x = 1920
    sc.render.resolution_y = 1080
    sc.render.film_transparent = True
    world = bpy.data.worlds.get("World") or bpy.data.worlds.new("World")
    sc.world = world
    world.use_nodes = True
    bg = world.node_tree.nodes["Background"]
    bg.inputs["Color"].default_value = (0.05, 0.06, 0.1, 1.0)
    bg.inputs["Strength"].default_value = 0.8

def setup_camera():
    bpy.ops.object.camera_add(location=(0, -20, 1), rotation=(math.radians(90), 0, 0))
    cam = bpy.context.active_object
    cam.name = "Camera"
    bpy.context.scene.camera = cam
    cam.data.lens = 24

    # Phase 1 (0-10s): Establishing - wide front view, see entire chamber
    kf_loc(cam, 1, (0, -20, 0))
    kf_rot(cam, 1, (math.radians(90), 0, 0))

    # Phase 2 (10-15s): Slightly closer
    kf_loc(cam, 300, (0, -18, 0))
    kf_rot(cam, 300, (math.radians(90), 0, 0))

    # Phase 3 (15-25s): Move down to show boats heating up, keep whole chamber visible
    kf_loc(cam, 450, (0, -18, 0))
    kf_loc(cam, 750, (0, -15, -1.0))
    kf_rot(cam, 450, (math.radians(90), 0, 0))
    kf_rot(cam, 750, (math.radians(88), 0, 0))

    # Phase 4 (25-45s): Pull back to see full vapor column from boats to film
    kf_loc(cam, 900, (0, -15, -1.0))
    kf_loc(cam, 1100, (0, -18, 0))
    kf_rot(cam, 900, (math.radians(88), 0, 0))
    kf_rot(cam, 1100, (math.radians(90), 0, 0))

    # Phase 5-6 (45-60s): Wide view
    kf_loc(cam, 1350, (0, -18, 0))
    kf_loc(cam, 1800, (0, -20, 0))
    kf_rot(cam, 1350, (math.radians(90), 0, 0))
    kf_rot(cam, 1800, (math.radians(90), 0, 0))

    return cam

def setup_lights():
    # Strong key light from above-front
    bpy.ops.object.light_add(type='AREA', location=(0, -10, 8))
    key = bpy.context.active_object
    key.name = "KeyLight"
    key.data.energy = 500
    key.data.size = 12
    key.data.color = (0.85, 0.9, 1.0)

    # Fill light from side
    bpy.ops.object.light_add(type='AREA', location=(6, -5, 3))
    fill = bpy.context.active_object
    fill.name = "FillLight"
    fill.data.energy = 200
    fill.data.size = 6
    fill.data.color = (0.7, 0.75, 1.0)

    # Bottom light to illuminate boats even before they glow
    bpy.ops.object.light_add(type='AREA', location=(0, -5, -3))
    bot = bpy.context.active_object
    bot.name = "BottomLight"
    bot.data.energy = 100
    bot.data.size = 10
    bot.data.color = (0.8, 0.8, 0.9)

# ---------------------------------------------------------------------------
# Chamber
# ---------------------------------------------------------------------------

def create_chamber():
    mat_chamber = make_mat("ChamberMetal", (0.25, 0.27, 0.3, 1.0),
                           metallic=0.9, roughness=0.4)
    mat_glass = make_mat("ChamberGlass", (0.4, 0.5, 0.6, 0.15),
                         alpha=0.15, roughness=0.05)

    # Back wall
    bpy.ops.mesh.primitive_cube_add(size=1, location=(0, CHAMBER_D / 2, 0))
    back = bpy.context.active_object
    back.name = "Chamber_Back"
    back.scale = (CHAMBER_W, 0.15, CHAMBER_H)
    back.data.materials.append(mat_chamber)

    # Floor
    bpy.ops.mesh.primitive_cube_add(size=1, location=(0, 0, -CHAMBER_H / 2))
    floor = bpy.context.active_object
    floor.name = "Chamber_Floor"
    floor.scale = (CHAMBER_W, CHAMBER_D, 0.15)
    floor.data.materials.append(mat_chamber)

    # Ceiling
    bpy.ops.mesh.primitive_cube_add(size=1, location=(0, 0, CHAMBER_H / 2))
    ceil = bpy.context.active_object
    ceil.name = "Chamber_Ceiling"
    ceil.scale = (CHAMBER_W, CHAMBER_D, 0.15)
    ceil.data.materials.append(mat_chamber)

    # Left wall
    bpy.ops.mesh.primitive_cube_add(size=1, location=(-CHAMBER_W / 2, 0, 0))
    lwall = bpy.context.active_object
    lwall.name = "Chamber_Left"
    lwall.scale = (0.15, CHAMBER_D, CHAMBER_H)
    lwall.data.materials.append(mat_chamber)

    # Right wall
    bpy.ops.mesh.primitive_cube_add(size=1, location=(CHAMBER_W / 2, 0, 0))
    rwall = bpy.context.active_object
    rwall.name = "Chamber_Right"
    rwall.scale = (0.15, CHAMBER_D, CHAMBER_H)
    rwall.data.materials.append(mat_chamber)

    # Front window (transparent)
    bpy.ops.mesh.primitive_cube_add(size=1, location=(0, -CHAMBER_D / 2, 0))
    front = bpy.context.active_object
    front.name = "Chamber_Front"
    front.scale = (CHAMBER_W, 0.05, CHAMBER_H)
    front.data.materials.append(mat_glass)

    return [back, floor, ceil, lwall, rwall, front]

# ---------------------------------------------------------------------------
# Evaporation Boats
# ---------------------------------------------------------------------------

def create_boats():
    boats = []
    boat_mats = []

    spacing = (CHAMBER_W - 2) / (NUM_BOATS - 1)
    start_x = -(CHAMBER_W - 2) / 2

    for i in range(NUM_BOATS):
        x = start_x + i * spacing

        mat = make_mat(f"BoatMat_{i}",
                       (0.3, 0.25, 0.2, 1.0),
                       emission_color=(1.0, 0.4, 0.05, 1.0),
                       emission_strength=0.0,
                       roughness=0.7)

        bpy.ops.mesh.primitive_cube_add(size=1, location=(x, 0, BOAT_Y))
        boat = bpy.context.active_object
        boat.name = f"Boat_{i}"
        boat.scale = (BOAT_W, BOAT_D, BOAT_H)
        boat.data.materials.append(mat)

        # Aluminum pool inside boat (smaller, slightly higher)
        mat_al = make_mat(f"AlPool_{i}",
                          (0.75, 0.77, 0.8, 1.0),
                          emission_color=(1.0, 0.6, 0.1, 1.0),
                          emission_strength=0.0,
                          metallic=0.95, roughness=0.1)

        bpy.ops.mesh.primitive_cube_add(size=1, location=(x, 0, BOAT_Y + BOAT_H * 0.3))
        pool = bpy.context.active_object
        pool.name = f"AlPool_{i}"
        pool.scale = (BOAT_W * 0.8, BOAT_D * 0.6, BOAT_H * 0.3)
        pool.data.materials.append(mat_al)

        boats.append((boat, pool, mat, mat_al))
        boat_mats.append((mat, mat_al))

    # Animate boat glow
    # Phase 1-2 (0-15s): boats cold
    # Phase 3 (15-25s): boats heat up progressively
    # Phase 4-6 (25-60s): boats at full glow
    for i, (mat_boat, mat_pool) in enumerate(boat_mats):
        delay = i * 8  # staggered ignition
        kf_emission(mat_boat, 1, 0.0)
        kf_emission(mat_pool, 1, 0.0)

        kf_emission(mat_boat, 400 + delay, 0.0)
        kf_emission(mat_boat, 550 + delay, 25.0)
        kf_emission(mat_boat, 750, 40.0)

        kf_emission(mat_pool, 450 + delay, 0.0)
        kf_emission(mat_pool, 600 + delay, 50.0)
        kf_emission(mat_pool, 750, 80.0)

        # Sustain glow
        kf_emission(mat_boat, 1800, 40.0)
        kf_emission(mat_pool, 1800, 80.0)

    return boats

# ---------------------------------------------------------------------------
# Film + Rollers
# ---------------------------------------------------------------------------

def create_film_system():
    mat_film = make_mat("FilmPET", (0.4, 0.65, 0.95, 0.75),
                        emission_color=(0.3, 0.5, 0.8, 1.0),
                        emission_strength=2.0,
                        alpha=0.75, roughness=0.2)
    mat_roller = make_mat("Roller", (0.6, 0.6, 0.65, 1.0),
                          metallic=0.8, roughness=0.3)

    # Left roller
    bpy.ops.mesh.primitive_cylinder_add(radius=ROLLER_RADIUS, depth=CHAMBER_D * 0.8,
                                        location=(-CHAMBER_W / 2 + 0.8, 0, FILM_Y))
    lr = bpy.context.active_object
    lr.name = "Roller_L"
    lr.rotation_euler = (math.radians(90), 0, 0)
    lr.data.materials.append(mat_roller)

    # Right roller
    bpy.ops.mesh.primitive_cylinder_add(radius=ROLLER_RADIUS, depth=CHAMBER_D * 0.8,
                                        location=(CHAMBER_W / 2 - 0.8, 0, FILM_Y))
    rr = bpy.context.active_object
    rr.name = "Roller_R"
    rr.rotation_euler = (math.radians(90), 0, 0)
    rr.data.materials.append(mat_roller)

    # Film plane (stretched between rollers)
    film_width = (CHAMBER_W - 1.6)
    bpy.ops.mesh.primitive_plane_add(size=1, location=(0, 0, FILM_Y - ROLLER_RADIUS * 0.3))
    film = bpy.context.active_object
    film.name = "Film"
    film.scale = (film_width / 2, CHAMBER_D * 0.35, 1)
    film.data.materials.append(mat_film)

    # Animate rollers spinning
    for roller in [lr, rr]:
        kf_rot(roller, 1, (math.radians(90), 0, 0))
        kf_rot(roller, 1800, (math.radians(90), math.radians(720), 0))

    # Deposition layer — a thin plane just below the film that grows from left to right
    mat_depo = make_mat("Deposition", (0.85, 0.87, 0.9, 1.0),
                        metallic=0.95, roughness=0.1)

    bpy.ops.mesh.primitive_plane_add(size=1,
                                      location=(-film_width / 2, 0, FILM_Y - ROLLER_RADIUS * 0.3 - 0.02))
    depo = bpy.context.active_object
    depo.name = "DepoLayer"
    depo.data.materials.append(mat_depo)

    # Start invisible, grow as deposition happens (from frame 750 onward)
    kf_scale(depo, 1, (0.01, CHAMBER_D * 0.35, 1))
    kf_scale(depo, 750, (0.01, CHAMBER_D * 0.35, 1))
    kf_scale(depo, 1500, (film_width / 2, CHAMBER_D * 0.35, 1))
    kf_scale(depo, 1800, (film_width / 2, CHAMBER_D * 0.35, 1))

    # Move depo layer origin to grow from left
    kf_loc(depo, 1, (-film_width / 4, 0, FILM_Y - ROLLER_RADIUS * 0.3 - 0.02))
    kf_loc(depo, 750, (-film_width / 4, 0, FILM_Y - ROLLER_RADIUS * 0.3 - 0.02))
    kf_loc(depo, 1500, (0, 0, FILM_Y - ROLLER_RADIUS * 0.3 - 0.02))
    kf_loc(depo, 1800, (0, 0, FILM_Y - ROLLER_RADIUS * 0.3 - 0.02))

    return lr, rr, film, depo

# ---------------------------------------------------------------------------
# Vapor Particles (simple sphere emitters)
# ---------------------------------------------------------------------------

def create_vapor_particles():
    particles = []
    spacing = (CHAMBER_W - 2) / (NUM_BOATS - 1)
    start_x = -(CHAMBER_W - 2) / 2

    mat_vapor = make_mat("Vapor", (0.9, 0.92, 0.95, 0.7),
                         emission_color=(1.0, 0.7, 0.3, 1.0),
                         emission_strength=3.0,
                         alpha=0.7)

    for bi in range(NUM_BOATS):
        bx = start_x + bi * spacing
        # Create a cluster of small spheres that rise from each boat
        for pi in range(15):
            bpy.ops.mesh.primitive_uv_sphere_add(radius=0.06, location=(bx, 0, BOAT_Y + 0.3))
            p = bpy.context.active_object
            p.name = f"Vapor_{bi}_{pi}"
            p.data.materials.append(mat_vapor)

            # Random offsets for natural look
            ox = random.uniform(-0.4, 0.4)
            oy = random.uniform(-0.1, 0.1)
            rise_speed = random.uniform(0.6, 1.0)
            cycle_offset = random.randint(0, 400)

            start_z = BOAT_Y + 0.3
            end_z = FILM_Y - 0.5

            # Each particle does a rising cycle, repeating
            cycle_len = int((end_z - start_z) / rise_speed * 30)
            if cycle_len < 60:
                cycle_len = 60

            # Before boats heat up: hidden
            kf_scale(p, 1, (0.01, 0.01, 0.01))
            kf_scale(p, 700 + cycle_offset % 200, (0.01, 0.01, 0.01))

            # Animate rising cycles from frame ~700 to 1800
            frame = 700 + (cycle_offset % 200)
            while frame < 1800:
                # Appear at boat
                kf_loc(p, frame, (bx + ox, oy, start_z))
                kf_scale(p, frame, (0.01, 0.01, 0.01))
                kf_scale(p, frame + 5, (1, 1, 1))

                # Rise to film
                kf_loc(p, frame + cycle_len, (bx + ox + random.uniform(-0.2, 0.2), oy, end_z))

                # Disappear at film (deposited)
                kf_scale(p, frame + cycle_len - 5, (1, 1, 1))
                kf_scale(p, frame + cycle_len, (0.01, 0.01, 0.01))

                frame += cycle_len + random.randint(10, 40)

            particles.append(p)

    return particles

# ---------------------------------------------------------------------------
# Labels
# ---------------------------------------------------------------------------

def create_labels():
    labels = []

    def add_label(text, loc, appear_frame, disappear_frame, size=0.3, name="Label"):
        bpy.ops.object.text_add(location=loc)
        obj = bpy.context.active_object
        obj.name = name
        obj.data.body = text
        obj.data.size = size
        obj.data.align_x = 'CENTER'
        obj.rotation_euler = (math.radians(90), 0, 0)
        mat = make_mat(f"mat_{name}", (1.0, 1.0, 1.0, 1.0))
        obj.data.materials.append(mat)

        kf_scale(obj, 1, (0.01, 0.01, 0.01))
        kf_scale(obj, appear_frame, (0.01, 0.01, 0.01))
        kf_scale(obj, appear_frame + 15, (1, 1, 1))
        kf_scale(obj, disappear_frame - 15, (1, 1, 1))
        kf_scale(obj, disappear_frame, (0.01, 0.01, 0.01))

        labels.append(obj)
        return obj

    label_y = -CHAMBER_D / 2 - 1.5

    # "真空腔体" label — top center
    add_label("真空腔体", (0, label_y, CHAMBER_H / 2 + 0.5),
              appear_frame=60, disappear_frame=350, size=0.5, name="Lbl_Chamber")

    # "蒸发舟 ×6" label — below boats
    add_label("蒸发舟 ×6\n1500°C", (0, label_y, BOAT_Y - 1.0),
              appear_frame=400, disappear_frame=800, size=0.35, name="Lbl_Boats")

    # "塑料薄膜 (PET)" label — above film
    add_label("塑料薄膜 (PET)", (0, label_y, FILM_Y + 1.0),
              appear_frame=300, disappear_frame=700, size=0.3, name="Lbl_Film")

    # "铝蒸汽 ↑" label — right side middle
    add_label("铝蒸汽 ↑↑↑", (CHAMBER_W / 2 + 1.0, label_y, 0),
              appear_frame=750, disappear_frame=1200, size=0.35, name="Lbl_Vapor")

    # "铝层沉积" label — near film
    add_label("铝层沉积", (0, label_y, FILM_Y - 0.5),
              appear_frame=1000, disappear_frame=1500, size=0.35, name="Lbl_Depo")

    # Analogy text — bottom center
    add_label("就像对冷玻璃哈气\n铝蒸汽→凝结成铝膜", (0, label_y, -CHAMBER_H / 2 + 0.5),
              appear_frame=1350, disappear_frame=1700, size=0.3, name="Lbl_Analogy")

    return labels

# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    cleanup()
    setup_scene()
    cam = setup_camera()
    setup_lights()

    create_chamber()
    create_boats()
    create_film_system()
    create_vapor_particles()
    create_labels()

    should_render = "--render" in sys.argv
    if should_render:
        sc = bpy.context.scene
        sc.render.image_settings.file_format = 'PNG'
        sc.render.filepath = "//render3/frame_"
        bpy.ops.render.render(animation=True)
        print(f"Rendered {TOTAL_FRAMES} frames")
    else:
        print("Scene 3 built. Open in Blender to preview (press Space to play).")
        print("Render: blender --background scene3_pvd.blend -o //render3/frame_ -F PNG -a")

    blend_path = bpy.path.abspath("//scene3_pvd.blend")
    bpy.ops.wm.save_as_mainfile(filepath=blend_path)
    print(f"Saved: {blend_path}")

if __name__ == "__main__":
    main()
