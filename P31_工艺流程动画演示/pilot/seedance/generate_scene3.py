"""
P30 S01 — Generate video segments via Seedance 2.0 API

Usage:
  python3 generate_scene3.py                    # all seedance segments
  python3 generate_scene3.py s01_sc3c_boats_heat  # specific segment
  python3 generate_scene3.py --list             # list available segments
"""

import os
import sys
import time
import json
import base64

# Load API key from .env
env_path = os.path.expanduser("~/AI/.env")
with open(env_path) as f:
    for line in f:
        line = line.strip()
        if line and not line.startswith("#") and "=" in line:
            k, v = line.split("=", 1)
            os.environ.setdefault(k.strip(), v.strip())

from volcenginesdkarkruntime import Ark

client = Ark(api_key=os.environ["ARK_API_KEY"])

MODEL = "doubao-seedance-2-0-260128"
REF_DIR = "/tmp/ref_frames"
OUT_DIR = os.path.dirname(os.path.abspath(__file__))

def image_to_data_url(path):
    with open(path, "rb") as f:
        data = base64.b64encode(f.read()).decode()
    return f"data:image/png;base64,{data}"

# Load segments from JSON
PROMPTS_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "prompts_s01_all.json")
with open(PROMPTS_FILE) as f:
    ALL_DATA = json.load(f)

SEGMENTS = []
for seg in ALL_DATA["segments"]:
    if seg["tool"] != "seedance":
        continue
    ref_img = seg.get("ref_image")
    if ref_img and not os.path.exists(ref_img):
        ref_img = None
    SEGMENTS.append({
        "name": seg["name"],
        "duration": seg["duration"],
        "ref_image": ref_img,
        "prompt": seg["prompt"],
    })


def submit_task(seg):
    content = []

    if seg["ref_image"] and os.path.exists(seg["ref_image"]):
        content.append({
            "type": "image_url",
            "image_url": {"url": image_to_data_url(seg["ref_image"])}
        })
        print(f"  [+] Reference image: {os.path.basename(seg['ref_image'])}")

    content.append({"type": "text", "text": seg["prompt"]})

    print(f"  Submitting {seg['name']} ({seg['duration']}s)...")

    task = client.content_generation.tasks.create(
        model=MODEL,
        content=content,
        extra_body={
            "resolution": "1080p",
            "ratio": "16:9",
            "duration": seg["duration"],
            "watermark": False,
        }
    )
    task_id = task.id if hasattr(task, 'id') else task.task_id
    print(f"  Task ID: {task_id}")
    return task_id


def poll_task(task_id, name, timeout=600):
    start = time.time()
    while time.time() - start < timeout:
        result = client.content_generation.tasks.get(task_id=task_id)

        # Handle different response shapes
        status = getattr(result, 'status', None)
        if status is None:
            status = getattr(result, 'state', None)

        if status in ("succeeded", "success", "done"):
            # Try various paths to get the video URL
            video_url = None
            for attr_chain in [
                lambda r: r.content.video_url,
                lambda r: r.output.video_url,
                lambda r: r.result.video_url,
                lambda r: r.content[0].video_url if isinstance(r.content, list) else None,
            ]:
                try:
                    video_url = attr_chain(result)
                    if video_url:
                        break
                except:
                    continue

            if not video_url:
                # Dump the full result for debugging
                print(f"  ✓ {name} succeeded but can't find video URL")
                print(f"    Result attrs: {dir(result)}")
                try:
                    print(f"    Result dict: {result.model_dump()}")
                except:
                    print(f"    Result: {result}")
                return None

            print(f"  ✓ {name} succeeded: {video_url[:80]}...")
            return video_url

        elif status in ("failed", "error"):
            print(f"  ✗ {name} failed: {getattr(result, 'error', 'unknown')}")
            return None
        else:
            elapsed = int(time.time() - start)
            print(f"  ... {name} status: {status} ({elapsed}s)")
            time.sleep(15)

    print(f"  ✗ {name} timed out after {timeout}s")
    return None


def download_video(url, path):
    import urllib.request
    urllib.request.urlretrieve(url, path)
    size_mb = os.path.getsize(path) / 1024 / 1024
    print(f"  Downloaded: {path} ({size_mb:.1f} MB)")


def main():
    if "--list" in sys.argv:
        print("Available Seedance segments:")
        for s in SEGMENTS:
            ref = f" [ref: {os.path.basename(s['ref_image'])}]" if s['ref_image'] else ""
            print(f"  {s['name']} ({s['duration']}s){ref}")
        return

    # Select which segments to generate (default: all)
    names = sys.argv[1:] if len(sys.argv) > 1 else [s["name"] for s in SEGMENTS]

    tasks = {}
    for seg in SEGMENTS:
        if seg["name"] in names:
            print(f"\n{'='*50}")
            print(f"Segment: {seg['name']}")
            try:
                task_id = submit_task(seg)
                tasks[seg["name"]] = task_id
            except Exception as e:
                print(f"  ✗ Submit failed: {e}")

    if not tasks:
        print("No tasks submitted.")
        return

    print(f"\n{'='*50}")
    print(f"Submitted {len(tasks)} tasks. Polling for results...")
    print(f"{'='*50}\n")

    results = {}
    for name, task_id in tasks.items():
        url = poll_task(task_id, name)
        if url:
            out_path = os.path.join(OUT_DIR, f"{name}.mp4")
            download_video(url, out_path)
            results[name] = out_path

    print(f"\n{'='*50}")
    print(f"Done. {len(results)}/{len(tasks)} segments generated.")
    for name, path in results.items():
        print(f"  {name}: {path}")

    # Save results index
    with open(os.path.join(OUT_DIR, "results.json"), "w") as f:
        json.dump(results, f, indent=2)


if __name__ == "__main__":
    main()
