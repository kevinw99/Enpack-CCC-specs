"""Generate Edge TTS narrations for all S01 scenes."""
import asyncio
import edge_tts

VOICE = "zh-CN-XiaoxiaoNeural"
RATE = "-10%"
OUTPUT_DIR = "."

NARRATIONS = {
    "scene1": {
        "text": "你的手机、电动车里都有锂电池。锂电池内部有正极和负极，中间靠锂离子移动来充放电。但锂离子在正负极材料里产生的电流，需要被收集起来，导出到外部电路。承担这个角色的薄片，叫做集流体。",
        "duration": 10,
    },
    "scene4": {
        "text": "蒸发舟是PVD镀膜的核心部件。它是一个12厘米长、3厘米宽的氮化硼陶瓷容器。铝丝从上方送入舟内，接触高温舟面后瞬间熔化，形成银色的铝液池。一台设备通常配置36个蒸发舟，分两排各18个排列，确保薄膜表面获得均匀的铝层。",
        "duration": 25,
    },
    "scene5": {
        "text": "然而在蒸镀过程中，铝液的飞溅会产生凹凸点缺陷。飞溅主要有三个来源：第一，铝液内部气泡核化后破裂；第二，送丝时铝丝冲击液面；第三，相邻蒸发舟之间的热辐射导致局部过热沸腾。飞溅的铝液滴撞击薄膜，就形成了凹凸点。",
        "duration": 25,
    },
    "scene6": {
        "text": "我们有两个改善方案。第一，减舟方案：将36个蒸发舟减至18个，增大舟间距，热辐射降低，凹凸点从45个降至12个，减少了73%。第二，钨网方案：在铝液面上铺设200目钨丝网，利用毛细效应让铝液均匀铺展，抑制局部沸腾和飞溅。",
        "duration": 25,
    },
    "scene7": {
        "text": "成品薄膜通过CCD在线检测，确认凹凸点数量达标后，卷绕收卷，完成蒸镀工序。",
        "duration": 10,
    },
}

async def generate_one(name, text):
    communicate = edge_tts.Communicate(text, VOICE, rate=RATE)
    mp3_path = f"{OUTPUT_DIR}/{name}_narration.mp3"
    vtt_path = f"{OUTPUT_DIR}/{name}_narration.vtt"
    await communicate.save(mp3_path)
    print(f"  Generated: {mp3_path}")

    with open(vtt_path, "w") as f:
        f.write("WEBVTT\n\n")
        f.write(f"00:00:00.000 --> 00:00:{NARRATIONS[name]['duration']:02d}.000\n")
        f.write(text + "\n")
    print(f"  Generated: {vtt_path}")

async def main():
    for name, info in NARRATIONS.items():
        print(f"Generating {name}...")
        await generate_one(name, info["text"])
    print("All narrations generated.")

asyncio.run(main())
