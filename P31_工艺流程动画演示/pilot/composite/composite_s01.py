"""
P30 S01 Final Compositing — Combine all segments into one video.

Workflow:
  1. Convert Blender PNG sequences → MP4
  2. Concatenate segments in scene order
  3. Mix narration audio
  4. Output s01_final.mp4
"""
import os
import subprocess
import sys
import json

PILOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SEEDANCE_DIR = os.path.join(PILOT_DIR, "seedance")
BLENDER_DIR = os.path.join(PILOT_DIR, "blender")
AUDIO_DIR = os.path.join(PILOT_DIR, "audio")
OUT_DIR = os.path.dirname(os.path.abspath(__file__))

FPS = 30

SCENES = [
    {
        "id": "scene1",
        "title": "为什么需要集流体",
        "segments": [
            {"type": "seedance", "file": "s01_sc1_why_battery.mp4"},
        ],
        "narration": "scene1_narration.mp3",
    },
    {
        "id": "scene2",
        "title": "三明治结构",
        "segments": [
            {"type": "composite", "file": "scene2_final.mp4"},
        ],
        "narration": "scene2_narration.mp3",
    },
    {
        "id": "scene3",
        "title": "PVD蒸镀原理",
        "segments": [
            # s01_sc3a_equipment.mp4 excluded — was a reference video, not AI-generated
            {"type": "seedance", "file": "s01_sc3b_vacuum.mp4"},
            {"type": "seedance", "file": "s01_sc3c_boats_heat.mp4"},
            {"type": "seedance", "file": "s01_sc3d_deposition.mp4"},
            {"type": "blender", "render_dir": "render3e", "frames": 300},
            {"type": "seedance", "file": "s01_sc3f_output.mp4"},
        ],
        "narration": "scene3_narration.mp3",
    },
    {
        "id": "scene4",
        "title": "蒸发舟细节",
        "segments": [
            {"type": "seedance", "file": "s01_sc4_boat_detail.mp4"},
            {"type": "blender", "render_dir": "render4b", "frames": 300},
        ],
        "narration": "scene4_narration.mp3",
    },
    {
        "id": "scene5",
        "title": "凹凸点缺陷",
        "segments": [
            {"type": "seedance", "file": "s01_sc5_defect_splash.mp4"},
            {"type": "blender", "render_dir": "render5b", "frames": 300},
        ],
        "narration": "scene5_narration.mp3",
    },
    {
        "id": "scene6",
        "title": "改善方案",
        "segments": [
            {"type": "blender", "render_dir": "render6", "frames": 300},
            {"type": "seedance", "file": "s01_sc6b_tungsten_mesh.mp4"},
        ],
        "narration": "scene6_narration.mp3",
    },
    {
        "id": "scene7",
        "title": "质量验证",
        "segments": [
            {"type": "seedance", "file": "s01_sc7_quality.mp4"},
        ],
        "narration": "scene7_narration.mp3",
    },
]


def run(cmd, desc=""):
    print(f"  [{desc}] {cmd[:100]}...")
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"  ERROR: {result.stderr[:200]}")
        return False
    return True


def blender_to_mp4(render_dir, frames, output_path):
    """Convert Blender PNG sequence to MP4."""
    src = os.path.join(BLENDER_DIR, render_dir)
    if not os.path.isdir(src):
        print(f"  WARNING: render dir {src} not found, skipping")
        return False

    png_count = len([f for f in os.listdir(src) if f.endswith('.png')])
    print(f"  Found {png_count} frames in {render_dir}")

    cmd = (f'ffmpeg -y -framerate {FPS} -start_number 1 -i "{src}/frame_%04d.png" '
           f'-c:v libx264 -pix_fmt yuv420p -crf 18 '
           f'-vf "scale=1920:1080:force_original_aspect_ratio=decrease,'
           f'pad=1920:1080:(ow-iw)/2:(oh-ih)/2" '
           f'"{output_path}"')
    return run(cmd, f"PNG→MP4 {render_dir}")


def normalize_segment(input_path, output_path):
    """Normalize a video segment to 1080p 30fps."""
    cmd = (f'ffmpeg -y -i "{input_path}" '
           f'-c:v libx264 -pix_fmt yuv420p -crf 18 '
           f'-vf "scale=1920:1080:force_original_aspect_ratio=decrease,'
           f'pad=1920:1080:(ow-iw)/2:(oh-ih)/2,fps={FPS}" '
           f'-an "{output_path}"')
    return run(cmd, f"Normalize {os.path.basename(input_path)}")


def get_duration(path):
    result = subprocess.run(
        f'ffprobe -v error -show_entries format=duration -of csv=p=0 "{path}"',
        shell=True, capture_output=True, text=True)
    return float(result.stdout.strip())


def main():
    tmp_dir = os.path.join(OUT_DIR, "tmp_composite")
    os.makedirs(tmp_dir, exist_ok=True)

    all_scene_files = []
    total_duration = 0

    for scene in SCENES:
        print(f"\n{'='*50}")
        print(f"Scene: {scene['id']} — {scene['title']}")

        segment_files = []
        for i, seg in enumerate(scene["segments"]):
            if seg["type"] == "seedance":
                src = os.path.join(SEEDANCE_DIR, seg["file"])
                if not os.path.exists(src):
                    print(f"  WARNING: {src} not found, skipping")
                    continue
                norm_path = os.path.join(tmp_dir, f"{scene['id']}_seg{i}.mp4")
                normalize_segment(src, norm_path)
                segment_files.append(norm_path)

            elif seg["type"] == "blender":
                mp4_path = os.path.join(tmp_dir, f"{scene['id']}_seg{i}_blender.mp4")
                if blender_to_mp4(seg["render_dir"], seg["frames"], mp4_path):
                    segment_files.append(mp4_path)

            elif seg["type"] == "composite":
                src = os.path.join(OUT_DIR, seg["file"])
                if os.path.exists(src):
                    norm_path = os.path.join(tmp_dir, f"{scene['id']}_seg{i}.mp4")
                    normalize_segment(src, norm_path)
                    segment_files.append(norm_path)

        if not segment_files:
            print(f"  No segments for {scene['id']}, skipping")
            continue

        if len(segment_files) == 1:
            scene_video = segment_files[0]
        else:
            concat_list = os.path.join(tmp_dir, f"{scene['id']}_concat.txt")
            with open(concat_list, "w") as f:
                for sf in segment_files:
                    f.write(f"file '{sf}'\n")
            scene_video = os.path.join(tmp_dir, f"{scene['id']}_concat.mp4")
            run(f'ffmpeg -y -f concat -safe 0 -i "{concat_list}" -c copy "{scene_video}"',
                f"Concat {scene['id']}")

        narration_path = os.path.join(AUDIO_DIR, scene["narration"])
        scene_final = os.path.join(tmp_dir, f"{scene['id']}_final.mp4")

        if os.path.exists(narration_path):
            video_dur = get_duration(scene_video)
            audio_dur = get_duration(narration_path)
            target_dur = max(video_dur, audio_dur)

            cmd = (f'ffmpeg -y -i "{scene_video}" -i "{narration_path}" '
                   f'-c:v libx264 -crf 18 -c:a aac -b:a 128k '
                   f'-shortest -pix_fmt yuv420p "{scene_final}"')
            run(cmd, f"Mix audio {scene['id']}")
        else:
            scene_final = scene_video

        dur = get_duration(scene_final)
        total_duration += dur
        print(f"  Scene {scene['id']}: {dur:.1f}s")
        all_scene_files.append(scene_final)

    print(f"\n{'='*50}")
    print(f"Concatenating {len(all_scene_files)} scenes ({total_duration:.1f}s total)...")

    final_concat = os.path.join(tmp_dir, "final_concat.txt")
    with open(final_concat, "w") as f:
        for sf in all_scene_files:
            f.write(f"file '{sf}'\n")

    output_path = os.path.join(OUT_DIR, "s01_pvd_final.mp4")
    run(f'ffmpeg -y -f concat -safe 0 -i "{final_concat}" '
        f'-c:v libx264 -crf 18 -c:a aac -b:a 128k '
        f'-pix_fmt yuv420p "{output_path}"',
        "Final concat")

    if os.path.exists(output_path):
        size_mb = os.path.getsize(output_path) / 1024 / 1024
        dur = get_duration(output_path)
        print(f"\n✓ Final output: {output_path}")
        print(f"  Duration: {dur:.1f}s ({dur/60:.1f} min)")
        print(f"  Size: {size_mb:.1f} MB")
    else:
        print("\n✗ Final output not created")


if __name__ == "__main__":
    main()
