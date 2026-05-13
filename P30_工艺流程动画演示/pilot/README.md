# P30 Pilot — Scene 2: 三明治结构 (30s)

## 目录结构

```
pilot/
├── blender/
│   └── scene2_sandwich.py    # Blender Python 脚本（建模+动画）
├── audio/
│   ├── scene2_narration.mp3  # Edge TTS 旁白（晓晓，34.6s）
│   └── scene2_narration.vtt  # 字幕时间轴
├── render/                   # Blender 渲染输出（PNG 序列）
└── composite/                # DaVinci 最终合成
```

## 使用方法

### 1. Blender 建模 + 动画

```bash
# 安装 Blender: https://www.blender.org/download/
# macOS: brew install --cask blender

# 无头运行（生成 .blend 文件）
blender --background --python blender/scene2_sandwich.py

# 带渲染
blender --background --python blender/scene2_sandwich.py -- --render

# 或: 打开 Blender GUI → Scripting → 打开 scene2_sandwich.py → 运行
```

### 2. 旁白已生成

- `audio/scene2_narration.mp3` — 34.6s，晓晓语音，语速 -10%
- `audio/scene2_narration.vtt` — 6 段字幕，带时间戳

### 3. DaVinci Resolve 合成

1. 导入 `render/` PNG 序列 → 创建 30fps 时间线
2. 导入 `audio/scene2_narration.mp3`
3. 添加中文标注（参考 VTT 时间轴对齐）
4. 调色、输出 1080p MP4

## 动画时间轴

| 时段 | 帧 | 内容 |
|------|-----|------|
| 0-5s | 1-150 | 传统纯铝箔展示 |
| 5-10s | 150-300 | 过渡：分裂为三层 |
| 10-15s | 300-450 | 三层合拢组装 |
| 15-20s | 450-600 | 爆炸图 + 材质/厚度标注 |
| 20-25s | 600-750 | 传统 vs 复合尺寸对比 |
| 25-30s | 750-900 | 安全机制：短路→熔断→安全 |
