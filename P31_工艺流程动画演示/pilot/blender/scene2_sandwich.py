"""
P30 Pilot — Scene 2: Sandwich Structure (三明治结构)
Blender Python script: creates 3-layer composite current collector model + animation.

Usage:
  blender --background --python scene2_sandwich.py -- [--render]

Or open Blender GUI, go to Scripting tab, open this file, and run.
"""

import bpy
import sys
import math

# ---------------------------------------------------------------------------
# Config
# ---------------------------------------------------------------------------
TOTAL_FRAMES = 900  # 30s @ 30fps
FPS = 30

# Layer dimensions (meters in Blender, but we scale for visibility)
SCALE = 100  # 1 unit = 1 μm visually
LAYER_WIDTH = 8.0   # X
LAYER_DEPTH = 5.0   # Y

AL_THICKNESS = 1.0 * 0.01   # 1 μm → 0.01 Blender units (exaggerated for visibility)
PET_THICKNESS = 4.0 * 0.01  # 4 μm → 0.04

# We exaggerate thickness for animation clarity
AL_DISPLAY_THICKNESS = 0.15
PET_DISPLAY_THICKNESS = 0.4

GAP_EXPLODED = 1.5  # gap between layers in exploded view

# Colors (RGBA linear)
AL_COLOR = (0.85, 0.87, 0.9, 1.0)      # silver/aluminum
PET_COLOR = (0.2, 0.5, 0.8, 0.6)       # semi-transparent blue
TRAD_AL_COLOR = (0.75, 0.77, 0.8, 1.0)  # slightly darker aluminum

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def cleanup_scene():
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete(use_global=False)
    for mat in bpy.data.materials:
        bpy.data.materials.remove(mat)

def make_material(name, color, metallic=0.0, roughness=0.5, alpha=1.0):
    mat = bpy.data.materials.new(name)
    mat.use_nodes = True
    bsdf = mat.node_tree.nodes["Principled BSDF"]
    bsdf.inputs["Base Color"].default_value = color
    bsdf.inputs["Metallic"].default_value = metallic
    bsdf.inputs["Roughness"].default_value = roughness
    if alpha < 1.0:
        mat.blend_method = 'BLEND' if hasattr(mat, 'blend_method') else None
        bsdf.inputs["Alpha"].default_value = alpha
    return mat

def add_plate(name, location, thickness, width, depth, material):
    bpy.ops.mesh.primitive_cube_add(size=1, location=location)
    obj = bpy.context.active_object
    obj.name = name
    obj.scale = (width, depth, thickness)
    obj.data.materials.append(material)
    return obj

def keyframe_location(obj, frame, location):
    obj.location = location
    obj.keyframe_insert(data_path="location", frame=frame)

def keyframe_scale(obj, frame, scale):
    obj.scale = scale
    obj.keyframe_insert(data_path="scale", frame=frame)

def add_text(text, location, size=0.3, name="Text"):
    bpy.ops.object.text_add(location=location)
    obj = bpy.context.active_object
    obj.name = name
    obj.data.body = text
    obj.data.size = size
    obj.data.align_x = 'CENTER'
    obj.rotation_euler = (math.pi / 2, 0, 0)
    mat = make_material(f"mat_{name}", (0.1, 0.1, 0.1, 1.0))
    obj.data.materials.append(mat)
    return obj

# ---------------------------------------------------------------------------
# Scene Setup
# ---------------------------------------------------------------------------

def setup_scene():
    scene = bpy.context.scene
    scene.frame_start = 1
    scene.frame_end = TOTAL_FRAMES
    scene.render.fps = FPS
    scene.render.resolution_x = 1920
    scene.render.resolution_y = 1080
    scene.render.film_transparent = True

    # World background
    world = bpy.data.worlds.get("World") or bpy.data.worlds.new("World")
    scene.world = world
    world.use_nodes = True
    bg = world.node_tree.nodes["Background"]
    bg.inputs["Color"].default_value = (0.95, 0.95, 0.97, 1.0)
    bg.inputs["Strength"].default_value = 1.0

def setup_camera():
    bpy.ops.object.camera_add(location=(0, -12, 4), rotation=(math.radians(72), 0, 0))
    cam = bpy.context.active_object
    cam.name = "MainCamera"
    bpy.context.scene.camera = cam
    cam.data.lens = 50
    return cam

def setup_lighting():
    bpy.ops.object.light_add(type='AREA', location=(3, -3, 6))
    key = bpy.context.active_object
    key.name = "KeyLight"
    key.data.energy = 300
    key.data.size = 5

    bpy.ops.object.light_add(type='AREA', location=(-4, 2, 4))
    fill = bpy.context.active_object
    fill.name = "FillLight"
    fill.data.energy = 100
    fill.data.size = 4

# ---------------------------------------------------------------------------
# Materials
# ---------------------------------------------------------------------------

def create_materials():
    mats = {}
    mats['al'] = make_material("Aluminum", AL_COLOR, metallic=0.95, roughness=0.15)
    mats['pet'] = make_material("PET_Film", PET_COLOR, metallic=0.0, roughness=0.3, alpha=0.6)
    mats['trad'] = make_material("Traditional_Al", TRAD_AL_COLOR, metallic=0.9, roughness=0.25)
    mats['danger'] = make_material("Danger_Red", (0.9, 0.1, 0.1, 1.0), metallic=0.0, roughness=0.5)
    mats['safe'] = make_material("Safe_Green", (0.1, 0.8, 0.2, 1.0), metallic=0.0, roughness=0.5)
    return mats

# ---------------------------------------------------------------------------
# Animation Phases
# ---------------------------------------------------------------------------

def create_animation(mats):
    """
    Timeline:
      Frame 1-150   (0-5s):   Traditional foil displayed
      Frame 150-300 (5-10s):  Transition — foil splits into 3 layers
      Frame 300-450 (10-15s): Sandwich assembly — 3 layers merge
      Frame 450-600 (15-20s): Exploded view — layers separate with labels
      Frame 600-750 (20-25s): Size comparison
      Frame 750-900 (25-30s): Safety mechanism — short circuit → fuse → safe
    """

    # -- Phase 1: Traditional aluminum foil (0-5s) --
    trad_foil = add_plate("TradFoil", (0, 0, 0), 0.3, LAYER_WIDTH, LAYER_DEPTH, mats['trad'])
    keyframe_location(trad_foil, 1, (0, 0, 0))
    keyframe_scale(trad_foil, 1, (LAYER_WIDTH, LAYER_DEPTH, 0.3))

    label_trad = add_text("传统集流体\n6-15 μm 纯铝箔", (0, 0, 1.0), size=0.35, name="LabelTrad")
    keyframe_location(label_trad, 1, (0, 0, 1.0))

    # Fade out traditional foil at frame 150
    keyframe_scale(trad_foil, 130, (LAYER_WIDTH, LAYER_DEPTH, 0.3))
    keyframe_scale(trad_foil, 150, (0.01, 0.01, 0.01))
    keyframe_scale(label_trad, 130, label_trad.scale[:])
    keyframe_scale(label_trad, 150, (0.01, 0.01, 0.01))

    # -- Phase 2-3: Three layers appear and assemble (5-15s) --
    top_al = add_plate("TopAl", (0, 0, 3), AL_DISPLAY_THICKNESS, LAYER_WIDTH, LAYER_DEPTH, mats['al'])
    pet_film = add_plate("PET", (0, 0, 0), PET_DISPLAY_THICKNESS, LAYER_WIDTH, LAYER_DEPTH, mats['pet'])
    bot_al = add_plate("BotAl", (0, 0, -3), AL_DISPLAY_THICKNESS, LAYER_WIDTH, LAYER_DEPTH, mats['al'])

    # Start off-screen (hidden by scale)
    for obj, z in [(top_al, 3), (pet_film, 0), (bot_al, -3)]:
        keyframe_scale(obj, 1, (0.01, 0.01, 0.01))
        keyframe_location(obj, 1, (0, 0, z))

    # Appear at frame 150
    for obj, z in [(top_al, 3), (pet_film, 0), (bot_al, -3)]:
        keyframe_scale(obj, 150, (0.01, 0.01, 0.01))
        keyframe_scale(obj, 180, (LAYER_WIDTH, LAYER_DEPTH, AL_DISPLAY_THICKNESS if obj != pet_film else PET_DISPLAY_THICKNESS))
        keyframe_location(obj, 180, (0, 0, z))

    # Spread apart (exploded intro) frame 180-250
    spread = GAP_EXPLODED
    keyframe_location(top_al, 250, (0, 0, spread))
    keyframe_location(pet_film, 250, (0, 0, 0))
    keyframe_location(bot_al, 250, (0, 0, -spread))

    # Assemble (merge together) frame 300-450
    assembled_gap = 0.2
    keyframe_location(top_al, 300, (0, 0, spread))
    keyframe_location(pet_film, 300, (0, 0, 0))
    keyframe_location(bot_al, 300, (0, 0, -spread))

    keyframe_location(top_al, 420, (0, 0, PET_DISPLAY_THICKNESS / 2 + AL_DISPLAY_THICKNESS / 2 + 0.02))
    keyframe_location(pet_film, 420, (0, 0, 0))
    keyframe_location(bot_al, 420, (0, 0, -(PET_DISPLAY_THICKNESS / 2 + AL_DISPLAY_THICKNESS / 2 + 0.02)))

    # -- Phase 4: Exploded view with labels (15-20s) --
    explode_gap = 1.8
    keyframe_location(top_al, 450, (0, 0, PET_DISPLAY_THICKNESS / 2 + AL_DISPLAY_THICKNESS / 2 + 0.02))
    keyframe_location(pet_film, 450, (0, 0, 0))
    keyframe_location(bot_al, 450, (0, 0, -(PET_DISPLAY_THICKNESS / 2 + AL_DISPLAY_THICKNESS / 2 + 0.02)))

    keyframe_location(top_al, 500, (0, 0, explode_gap))
    keyframe_location(pet_film, 500, (0, 0, 0))
    keyframe_location(bot_al, 500, (0, 0, -explode_gap))

    # Labels for exploded view
    lbl_top = add_text("铝层 ~1 μm", (LAYER_WIDTH / 2 + 1.5, 0, explode_gap), size=0.25, name="LblTopAl")
    lbl_pet = add_text("PET/PP 基膜 ~4 μm", (LAYER_WIDTH / 2 + 1.5, 0, 0), size=0.25, name="LblPET")
    lbl_bot = add_text("铝层 ~1 μm", (LAYER_WIDTH / 2 + 1.5, 0, -explode_gap), size=0.25, name="LblBotAl")

    for lbl in [lbl_top, lbl_pet, lbl_bot]:
        keyframe_scale(lbl, 1, (0.01, 0.01, 0.01))
        keyframe_scale(lbl, 450, (0.01, 0.01, 0.01))
        keyframe_scale(lbl, 480, (1, 1, 1))

    # Keep labels visible until frame 600
    for lbl in [lbl_top, lbl_pet, lbl_bot]:
        keyframe_scale(lbl, 600, (1, 1, 1))
        keyframe_scale(lbl, 630, (0.01, 0.01, 0.01))

    # -- Phase 5: Size comparison (20-25s, frame 600-750) --
    # Reassemble layers
    keyframe_location(top_al, 600, (0, 0, explode_gap))
    keyframe_location(pet_film, 600, (0, 0, 0))
    keyframe_location(bot_al, 600, (0, 0, -explode_gap))

    # Move composite to right side
    offset_x = 2.5
    keyframe_location(top_al, 650, (offset_x, 0, PET_DISPLAY_THICKNESS / 2 + AL_DISPLAY_THICKNESS / 2 + 0.02))
    keyframe_location(pet_film, 650, (offset_x, 0, 0))
    keyframe_location(bot_al, 650, (offset_x, 0, -(PET_DISPLAY_THICKNESS / 2 + AL_DISPLAY_THICKNESS / 2 + 0.02)))

    # Traditional foil reappears on left for comparison
    trad_compare = add_plate("TradCompare", (-offset_x, 0, 0), 0.5, LAYER_WIDTH * 0.6, LAYER_DEPTH * 0.6, mats['trad'])
    keyframe_scale(trad_compare, 1, (0.01, 0.01, 0.01))
    keyframe_scale(trad_compare, 630, (0.01, 0.01, 0.01))
    keyframe_scale(trad_compare, 660, (LAYER_WIDTH * 0.6, LAYER_DEPTH * 0.6, 0.5))

    lbl_compare_trad = add_text("传统: 6-15 μm", (-offset_x, 0, 1.2), size=0.25, name="LblCompareTrad")
    lbl_compare_new = add_text("复合: ~6 μm\n(金属仅 2 μm)", (offset_x, 0, 1.2), size=0.25, name="LblCompareNew")

    for lbl in [lbl_compare_trad, lbl_compare_new]:
        keyframe_scale(lbl, 1, (0.01, 0.01, 0.01))
        keyframe_scale(lbl, 650, (0.01, 0.01, 0.01))
        keyframe_scale(lbl, 680, (1, 1, 1))
        keyframe_scale(lbl, 740, (1, 1, 1))
        keyframe_scale(lbl, 750, (0.01, 0.01, 0.01))

    keyframe_scale(trad_compare, 740, (LAYER_WIDTH * 0.6, LAYER_DEPTH * 0.6, 0.5))
    keyframe_scale(trad_compare, 750, (0.01, 0.01, 0.01))

    # -- Phase 6: Safety mechanism (25-30s, frame 750-900) --
    # Move composite back to center
    keyframe_location(top_al, 750, (offset_x, 0, PET_DISPLAY_THICKNESS / 2 + AL_DISPLAY_THICKNESS / 2 + 0.02))
    keyframe_location(pet_film, 750, (offset_x, 0, 0))
    keyframe_location(bot_al, 750, (offset_x, 0, -(PET_DISPLAY_THICKNESS / 2 + AL_DISPLAY_THICKNESS / 2 + 0.02)))

    keyframe_location(top_al, 780, (0, 0, PET_DISPLAY_THICKNESS / 2 + AL_DISPLAY_THICKNESS / 2 + 0.02))
    keyframe_location(pet_film, 780, (0, 0, 0))
    keyframe_location(bot_al, 780, (0, 0, -(PET_DISPLAY_THICKNESS / 2 + AL_DISPLAY_THICKNESS / 2 + 0.02)))

    # Short circuit indicator (red flash)
    lbl_danger = add_text("⚡ 短路!", (0, 0, 2.0), size=0.4, name="LblDanger")
    lbl_danger.data.materials.clear()
    lbl_danger.data.materials.append(mats['danger'])
    keyframe_scale(lbl_danger, 1, (0.01, 0.01, 0.01))
    keyframe_scale(lbl_danger, 790, (0.01, 0.01, 0.01))
    keyframe_scale(lbl_danger, 810, (1, 1, 1))

    # PET melts (fuse) — shrink PET layer
    keyframe_scale(pet_film, 820, (LAYER_WIDTH, LAYER_DEPTH, PET_DISPLAY_THICKNESS))
    keyframe_scale(pet_film, 850, (LAYER_WIDTH, LAYER_DEPTH, 0.01))

    # Danger label fades, safe label appears
    keyframe_scale(lbl_danger, 840, (1, 1, 1))
    keyframe_scale(lbl_danger, 860, (0.01, 0.01, 0.01))

    lbl_safe = add_text("✓ 电流切断\n防止起火", (0, 0, 2.0), size=0.35, name="LblSafe")
    lbl_safe.data.materials.clear()
    lbl_safe.data.materials.append(mats['safe'])
    keyframe_scale(lbl_safe, 1, (0.01, 0.01, 0.01))
    keyframe_scale(lbl_safe, 850, (0.01, 0.01, 0.01))
    keyframe_scale(lbl_safe, 870, (1, 1, 1))
    keyframe_scale(lbl_safe, 900, (1, 1, 1))

    # Layers drift apart (circuit broken)
    keyframe_location(top_al, 850, (0, 0, PET_DISPLAY_THICKNESS / 2 + AL_DISPLAY_THICKNESS / 2 + 0.02))
    keyframe_location(bot_al, 850, (0, 0, -(PET_DISPLAY_THICKNESS / 2 + AL_DISPLAY_THICKNESS / 2 + 0.02)))
    keyframe_location(top_al, 890, (0, 0, 1.0))
    keyframe_location(bot_al, 890, (0, 0, -1.0))


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    cleanup_scene()
    setup_scene()
    setup_camera()
    setup_lighting()
    mats = create_materials()
    create_animation(mats)

    should_render = "--render" in sys.argv
    if should_render:
        scene = bpy.context.scene
        scene.render.image_settings.file_format = 'PNG'
        scene.render.filepath = "//render/frame_"
        bpy.ops.render.render(animation=True)
        print(f"Rendered {TOTAL_FRAMES} frames to render/ directory")
    else:
        print("Scene built successfully. Open in Blender to preview.")
        print("To render: blender --background --python scene2_sandwich.py -- --render")

    # Save .blend file
    blend_path = bpy.path.abspath("//scene2_sandwich.blend")
    bpy.ops.wm.save_as_mainfile(filepath=blend_path)
    print(f"Saved: {blend_path}")

if __name__ == "__main__":
    main()
