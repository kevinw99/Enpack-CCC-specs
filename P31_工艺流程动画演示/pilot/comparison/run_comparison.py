"""
P30 — Kling vs Seedance A/B comparison test
Pure text-to-video, no reference images, same prompts for both tools.
3 representative segments: equipment overview, boat heating, defect splash.

Usage:
  python3 run_comparison.py              # run both
  python3 run_comparison.py --kling      # kling only
  python3 run_comparison.py --seedance   # seedance only
"""

import os
import sys
import time
import json
import jwt
import requests
import urllib.request
from datetime import datetime

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

env_path = os.path.expanduser("~/AI/.env")
with open(env_path) as f:
    for line in f:
        line = line.strip()
        if line and not line.startswith("#") and "=" in line:
            k, v = line.split("=", 1)
            os.environ.setdefault(k.strip(), v.strip())

TEST_SEGMENTS = [
    {
        "id": "sc3a_equipment",
        "title": "PVD设备全景 (宏观)",
        "duration": 10,
        "prompt": "工业级PVD真空镀膜设备全景，银白色不锈钢机身，大型真空腔体居中，"
                  "左右两侧有放卷和收卷辊，塑料薄膜从左侧辊展开穿过腔体再卷到右侧。"
                  "设备干净整洁，工厂背景，柔和的工业灯光。"
                  "镜头从设备右前方缓缓推进到腔体正面。电影级画质，工业宣传片风格。",
    },
    {
        "id": "sc3c_boats_heat",
        "title": "蒸发舟加热 (中景)",
        "duration": 10,
        "prompt": "真空腔体内部，一排6个陶瓷蒸发舟整齐排列在底部。从暗到亮："
                  "蒸发舟逐个通电加热，从灰色变为暗红、橙红、亮白色，发出强烈的热辐射光芒。"
                  "铝丝从上方自动送入每个舟中，接触高温舟面后迅速熔化成银色液体。"
                  "腔体内壁反射橙色光芒。镜头沿蒸发舟排列方向缓缓平移。",
    },
    {
        "id": "sc5_defect_splash",
        "title": "凹凸点缺陷 (微观)",
        "duration": 10,
        "prompt": "蒸发舟内的银色铝液在高温下剧烈沸腾，液面产生气泡，气泡破裂时弹射出微小的"
                  "银色液滴飞溅到上方。类似一锅沸腾的油溅出油花的效果。"
                  "液滴飞向上方的塑料薄膜，撞击薄膜表面形成微小的凸起。"
                  "高速摄影风格，慢动作，戏剧性灯光。",
    },
]

# --- Kling API ---

KLING_API_BASE = "https://api-beijing.klingai.com"

def kling_jwt_token():
    ak = os.environ["KLING_API_KEY"]
    sk = os.environ["KLING_SECRECT_Key"]
    now = int(time.time())
    payload = {"iss": ak, "exp": now + 1800, "nbf": now - 5}
    return jwt.encode(payload, sk, algorithm="HS256",
                      headers={"typ": "JWT", "alg": "HS256"})

def kling_submit(seg):
    token = kling_jwt_token()
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
    body = {
        "model_name": "kling-v3",
        "prompt": seg["prompt"],
        "duration": "10",
        "aspect_ratio": "16:9",
        "mode": "std",
    }
    print(f"  [Kling] Submitting {seg['id']}...")
    r = requests.post(f"{KLING_API_BASE}/v1/videos/text2video",
                      json=body, headers=headers, timeout=30)
    r.raise_for_status()
    data = r.json()
    if data.get("code") != 0:
        print(f"  [Kling] Error: {data}")
        return None
    task_id = data["data"]["task_id"]
    print(f"  [Kling] Task ID: {task_id}")
    return task_id

def kling_poll(task_id, name, timeout=600):
    start = time.time()
    while time.time() - start < timeout:
        token = kling_jwt_token()
        headers = {"Authorization": f"Bearer {token}"}
        r = requests.get(f"{KLING_API_BASE}/v1/videos/text2video/{task_id}",
                         headers=headers, timeout=30)
        r.raise_for_status()
        data = r.json()
        task_data = data.get("data", {})
        status = task_data.get("task_status", "")

        if status == "succeed":
            videos = task_data.get("task_result", {}).get("videos", [])
            if videos:
                url = videos[0].get("url", "")
                dur = videos[0].get("duration", "?")
                print(f"  [Kling] ✓ {name} succeeded ({dur}s)")
                return url
            print(f"  [Kling] ✓ {name} succeeded but no video URL in response")
            return None
        elif status == "failed":
            msg = task_data.get("task_status_msg", "unknown")
            print(f"  [Kling] ✗ {name} failed: {msg}")
            return None
        else:
            elapsed = int(time.time() - start)
            print(f"  [Kling] ... {name}: {status} ({elapsed}s)")
            time.sleep(15)

    print(f"  [Kling] ✗ {name} timed out")
    return None

# --- Seedance API ---

def seedance_submit(seg):
    from volcenginesdkarkruntime import Ark
    client = Ark(api_key=os.environ["ARK_API_KEY"])
    content = [{"type": "text", "text": seg["prompt"]}]
    print(f"  [Seedance] Submitting {seg['id']}...")
    task = client.content_generation.tasks.create(
        model="doubao-seedance-2-0-260128",
        content=content,
        extra_body={
            "resolution": "1080p",
            "ratio": "16:9",
            "duration": seg["duration"],
            "watermark": False,
        }
    )
    task_id = task.id if hasattr(task, "id") else task.task_id
    print(f"  [Seedance] Task ID: {task_id}")
    return task_id, client

def seedance_poll(client, task_id, name, timeout=600):
    start = time.time()
    while time.time() - start < timeout:
        result = client.content_generation.tasks.get(task_id=task_id)
        status = getattr(result, "status", None) or getattr(result, "state", None)

        if status in ("succeeded", "success", "done"):
            for getter in [
                lambda r: r.content.video_url,
                lambda r: r.output.video_url,
                lambda r: r.result.video_url,
                lambda r: r.content[0].video_url if isinstance(r.content, list) else None,
            ]:
                try:
                    url = getter(result)
                    if url:
                        print(f"  [Seedance] ✓ {name} succeeded")
                        return url
                except:
                    continue
            print(f"  [Seedance] ✓ {name} succeeded but can't extract URL")
            return None
        elif status in ("failed", "error"):
            print(f"  [Seedance] ✗ {name} failed")
            return None
        else:
            elapsed = int(time.time() - start)
            print(f"  [Seedance] ... {name}: {status} ({elapsed}s)")
            time.sleep(15)

    print(f"  [Seedance] ✗ {name} timed out")
    return None

# --- Download & Report ---

def download(url, path):
    urllib.request.urlretrieve(url, path)
    size_mb = os.path.getsize(path) / 1024 / 1024
    print(f"  Downloaded: {os.path.basename(path)} ({size_mb:.1f} MB)")
    return size_mb

def run_tool(tool, segments):
    results = {}
    if tool == "kling":
        tasks = {}
        for seg in segments:
            try:
                tid = kling_submit(seg)
                if tid:
                    tasks[seg["id"]] = tid
            except Exception as e:
                print(f"  [Kling] Submit error for {seg['id']}: {e}")

        for seg_id, tid in tasks.items():
            url = kling_poll(tid, seg_id)
            if url:
                path = os.path.join(SCRIPT_DIR, f"kling_{seg_id}.mp4")
                size = download(url, path)
                results[seg_id] = {"path": path, "size_mb": size, "task_id": tid}
            else:
                results[seg_id] = {"path": None, "task_id": tid, "error": "no video"}

    elif tool == "seedance":
        tasks = {}
        client = None
        for seg in segments:
            try:
                tid, client = seedance_submit(seg)
                tasks[seg["id"]] = tid
            except Exception as e:
                print(f"  [Seedance] Submit error for {seg['id']}: {e}")

        for seg_id, tid in tasks.items():
            url = seedance_poll(client, tid, seg_id)
            if url:
                path = os.path.join(SCRIPT_DIR, f"seedance_{seg_id}.mp4")
                size = download(url, path)
                results[seg_id] = {"path": path, "size_mb": size, "task_id": tid}
            else:
                results[seg_id] = {"path": None, "task_id": tid, "error": "no video"}

    return results

def main():
    run_kling = "--seedance" not in sys.argv or "--kling" in sys.argv
    run_seedance = "--kling" not in sys.argv or "--seedance" in sys.argv

    if not any(a in sys.argv for a in ("--kling", "--seedance")):
        run_kling = run_seedance = True

    all_results = {"timestamp": datetime.now().isoformat(), "segments": {}}

    for seg in TEST_SEGMENTS:
        all_results["segments"][seg["id"]] = {
            "title": seg["title"],
            "prompt": seg["prompt"],
            "duration": seg["duration"],
        }

    if run_kling:
        print("\n" + "=" * 60)
        print("KLING — Submitting 3 segments (text-only, no ref images)")
        print("=" * 60)
        kling_results = run_tool("kling", TEST_SEGMENTS)
        for seg_id, r in kling_results.items():
            all_results["segments"][seg_id]["kling"] = r

    if run_seedance:
        print("\n" + "=" * 60)
        print("SEEDANCE — Submitting 3 segments (text-only, no ref images)")
        print("=" * 60)
        seedance_results = run_tool("seedance", TEST_SEGMENTS)
        for seg_id, r in seedance_results.items():
            all_results["segments"][seg_id]["seedance"] = r

    results_path = os.path.join(SCRIPT_DIR, "comparison_results.json")
    with open(results_path, "w") as f:
        json.dump(all_results, f, indent=2, ensure_ascii=False, default=str)
    print(f"\nResults saved to: {results_path}")

    # Summary
    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)
    for seg_id, info in all_results["segments"].items():
        print(f"\n{seg_id} — {info['title']}")
        for tool in ("kling", "seedance"):
            r = info.get(tool, {})
            if not r:
                print(f"  {tool:>10}: (not run)")
            elif r.get("error"):
                print(f"  {tool:>10}: FAILED — {r['error']}")
            else:
                print(f"  {tool:>10}: ✓ {r.get('size_mb', 0):.1f} MB — {os.path.basename(r.get('path', ''))}")


if __name__ == "__main__":
    main()
