"""Generate comparison report PDF with embedded frame screenshots."""

import os
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm, cm
from reportlab.lib.colors import HexColor, black, white, grey
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image,
    PageBreak, KeepTogether
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_CENTER
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.cidfonts import UnicodeCIDFont

pdfmetrics.registerFont(UnicodeCIDFont("STSong-Light"))

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
OUT_PDF = os.path.join(SCRIPT_DIR, "comparison_report.pdf")

BLUE = HexColor("#1a5276")
LIGHT_BLUE = HexColor("#d6eaf8")
LIGHT_GREY = HexColor("#f2f3f4")
GREEN = HexColor("#27ae60")
ORANGE = HexColor("#e67e22")

styles = getSampleStyleSheet()

zh = ParagraphStyle("ZH", parent=styles["Normal"], fontName="STSong-Light",
                     fontSize=10, leading=14)
zh_small = ParagraphStyle("ZH_SM", parent=zh, fontSize=8, leading=11)
zh_bold = ParagraphStyle("ZH_B", parent=zh, fontSize=10, leading=14,
                          textColor=BLUE)
h1 = ParagraphStyle("H1_ZH", parent=zh, fontSize=18, leading=24,
                      textColor=BLUE, spaceAfter=6*mm)
h2 = ParagraphStyle("H2_ZH", parent=zh, fontSize=14, leading=18,
                      textColor=BLUE, spaceBefore=6*mm, spaceAfter=3*mm)
h3 = ParagraphStyle("H3_ZH", parent=zh, fontSize=11, leading=15,
                      textColor=BLUE, spaceBefore=4*mm, spaceAfter=2*mm)
caption = ParagraphStyle("CAP", parent=zh, fontSize=8, leading=10,
                          textColor=grey, alignment=TA_CENTER)

def p(text, style=zh):
    return Paragraph(text, style)

def header_table(data, col_widths=None):
    t = Table(data, colWidths=col_widths, repeatRows=1)
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), BLUE),
        ("TEXTCOLOR", (0, 0), (-1, 0), white),
        ("FONTNAME", (0, 0), (-1, -1), "STSong-Light"),
        ("FONTSIZE", (0, 0), (-1, -1), 9),
        ("LEADING", (0, 0), (-1, -1), 13),
        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("GRID", (0, 0), (-1, -1), 0.5, HexColor("#bdc3c7")),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [white, LIGHT_GREY]),
        ("TOPPADDING", (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
    ]))
    return t

def img(filename, w=70*mm):
    path = os.path.join(SCRIPT_DIR, filename)
    if not os.path.exists(path):
        return p(f"[missing: {filename}]", zh_small)
    im = Image(path, width=w, height=w * 9 / 16)
    return im

def build():
    doc = SimpleDocTemplate(OUT_PDF, pagesize=A4,
                            topMargin=15*mm, bottomMargin=15*mm,
                            leftMargin=15*mm, rightMargin=15*mm)
    story = []
    pw = A4[0] - 30*mm

    # --- Title ---
    story.append(p("P30 — Kling v3 vs Seedance 2.0 对比报告", h1))
    story.append(p("日期: 2026-05-16 &nbsp;&nbsp;|&nbsp;&nbsp; "
                    "测试条件: 纯文本生成 (text-to-video)，无参考图，相同 prompt", zh_small))
    story.append(Spacer(1, 6*mm))

    # --- 1. Technical specs ---
    story.append(p("1. 技术参数对比", h2))
    spec_data = [
        [p("参数", zh_bold), p("Kling v3 (std)", zh_bold), p("Seedance 2.0", zh_bold)],
        ["分辨率", "1280×720 (720p)", "1920×1080 (1080p)"],
        ["帧率", "24 fps", "24 fps"],
        ["音频", "无", "有（环境音效）"],
        ["平均码率", "5,343 kbps", "4,082 kbps"],
        ["生成耗时", "~70s", "~250s"],
        ["API 单价", "~0.48 RMB/s", "~0.16 RMB/s"],
        ["10s 片段成本", "~4.8 RMB", "~1.6 RMB"],
        ["模型", "kling-v3", "doubao-seedance-2-0"],
    ]
    cw = [pw*0.3, pw*0.35, pw*0.35]
    story.append(header_table(spec_data, cw))
    story.append(Spacer(1, 2*mm))
    story.append(p("注: Kling std 模式仅输出 720p。升级到 1080p 需 pro 模式 (~0.96 RMB/s，成本翻倍)。", zh_small))

    # --- 2. Visual comparison ---
    story.append(PageBreak())
    story.append(p("2. 画面质量逐片段对比", h2))

    segments = [
        {
            "title": "片段 A — SC3A 设备全景（宏观场景）",
            "kling_img": "kling_sc3a_equipment_frame3s.png",
            "seedance_img": "seedance_sc3a_equipment_frame3s.png",
            "kling_size": "4.9 MB",
            "seedance_size": "4.5 MB",
            "rows": [
                ["Prompt 理解力", "放卷/收卷辊和穿腔体的薄膜清晰，结构正确", "大型设备全景+洁净室，但放卷辊不明显", "Kling"],
                ["画面真实感", "非常逼真，像实拍照片", "非常逼真，更\"高端大气\"", "平手"],
                ["工业准确度", "更接近真实 PVD 卷绕镀膜设备", "更像通用精密设备", "Kling"],
                ["细节清晰度", "720p 限制了细节", "1080p 细节更丰富", "Seedance"],
            ],
        },
        {
            "title": "片段 B — SC3C 蒸发舟加热（中景场景）",
            "kling_img": "kling_sc3c_boats_heat_frame3s.png",
            "seedance_img": "seedance_sc3c_boats_heat_frame3s.png",
            "kling_size": "6.1 MB",
            "seedance_size": "4.5 MB",
            "rows": [
                ["Prompt 理解力", "椭圆形陶瓷舟+铝丝送入，形状贴合实际", "圆柱形容器(偏离)，腔壁有凝结纹理", "Kling"],
                ["画面真实感", "高温发光效果自然", "发光效果好，腔体氛围感强", "平手"],
                ["工业准确度", "舟的形状更接近氮化硼蒸发舟", "容器形状不准确，更像坩埚", "Kling"],
                ["细节清晰度", "720p 但码率高，细节尚可", "1080p 细节更多", "Seedance"],
            ],
        },
        {
            "title": "片段 C — SC5 缺陷飞溅（微观场景）",
            "kling_img": "kling_sc5_defect_splash_frame3s.png",
            "seedance_img": "seedance_sc5_defect_splash_frame3s.png",
            "kling_size": "8.2 MB",
            "seedance_size": "5.7 MB",
            "rows": [
                ["Prompt 理解力", "圆形容器中银液沸腾飞溅，液滴向上", "方形容器+上方透明薄膜", "Seedance"],
                ["画面真实感", "极度逼真，高速摄影质感", "逼真，展示完整工艺关系", "Kling"],
                ["工业准确度", "容器偏圆(实际舟是长方形)", "容器形状更准确+展示薄膜", "Seedance"],
                ["细节清晰度", "飞溅液滴清晰可见", "气泡和沸腾纹理清晰", "平手"],
            ],
        },
    ]

    img_w = pw * 0.45

    for seg in segments:
        story.append(p(seg["title"], h3))

        img_table = Table(
            [[img(seg["kling_img"], img_w), img(seg["seedance_img"], img_w)],
             [p(f"Kling v3 ({seg['kling_size']})", caption),
              p(f"Seedance 2.0 ({seg['seedance_size']})", caption)]],
            colWidths=[pw*0.5, pw*0.5]
        )
        img_table.setStyle(TableStyle([
            ("ALIGN", (0, 0), (-1, -1), "CENTER"),
            ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
            ("TOPPADDING", (0, 0), (-1, -1), 2),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 2),
        ]))
        story.append(img_table)
        story.append(Spacer(1, 2*mm))

        eval_data = [[p("维度", zh_bold), p("Kling v3", zh_bold),
                       p("Seedance 2.0", zh_bold), p("胜出", zh_bold)]]
        for row in seg["rows"]:
            eval_data.append([row[0], row[1], row[2], row[3]])
        eval_cw = [pw*0.15, pw*0.32, pw*0.32, pw*0.12]
        story.append(header_table(eval_data, eval_cw))
        story.append(Spacer(1, 4*mm))

    # --- 3. Overall scores ---
    story.append(PageBreak())
    story.append(p("3. 综合评分", h2))
    score_data = [
        [p("维度", zh_bold), p("Kling v3", zh_bold), p("Seedance 2.0", zh_bold), p("说明", zh_bold)],
        ["Prompt 理解力", "★★★★", "★★★★", "两者对中文工业 prompt 理解都很好"],
        ["画面真实感", "★★★★★", "★★★★", "Kling 的\"实拍感\"更强"],
        ["工业准确度", "★★★★", "★★★", "Kling 对设备形态还原更准确"],
        ["分辨率/清晰度", "★★★", "★★★★★", "std 模式 Kling 只有 720p"],
        ["生成速度", "★★★★★", "★★★", "Kling 快 3.5 倍"],
        ["性价比", "★★★", "★★★★★", "Seedance 便宜 3 倍"],
        ["附加功能", "—", "环境音效", "Seedance 额外附送音频"],
    ]
    story.append(header_table(score_data, [pw*0.15, pw*0.15, pw*0.15, pw*0.46]))

    # --- 4. Cost ---
    story.append(p("4. 费用汇总", h2))
    cost_data = [
        [p("工具", zh_bold), p("任务数", zh_bold), p("总时长", zh_bold), p("总花费", zh_bold)],
        ["Seedance (全部历史)", "15 (13成功)", "140s", "~22.4 RMB"],
        ["Kling (全部历史)", "4", "35s", "21 units (~10-14 RMB)"],
        [p("合计", zh_bold), "19", "175s", p("~33-37 RMB", zh_bold)],
    ]
    story.append(header_table(cost_data, [pw*0.35, pw*0.15, pw*0.15, pw*0.26]))

    # --- 5. Conclusion ---
    story.append(p("5. 结论与建议", h2))

    story.append(p("<b>画质判断:</b> Kling 在画面真实感和工业准确度上略胜一筹，尤其是设备全景和蒸发舟场景。"
                    "但 std 模式的 720p 分辨率是硬伤——最终成品需要 1080p。", zh))
    story.append(Spacer(1, 3*mm))

    plan_data = [
        [p("方案", zh_bold), p("做法", zh_bold), p("10s成本", zh_bold), p("适用", zh_bold)],
        ["A: Kling pro", "升级到 pro 模式 1080p", "~9.6 RMB", "追求最高画质"],
        ["B: Seedance", "继续当前方案", "~1.6 RMB", "成本优先，1080p 开箱即用"],
        ["C: 混合", "关键场景 Kling，批量 Seedance", "~5 RMB 均", "平衡质量与成本"],
    ]
    story.append(header_table(plan_data, [pw*0.18, pw*0.32, pw*0.18, pw*0.24]))
    story.append(Spacer(1, 3*mm))

    story.append(p("S01 全片 (~100s AI 片段) 成本估算: 方案A ~96 RMB / 方案B ~16 RMB / 方案C ~50 RMB", zh_small))
    story.append(Spacer(1, 4*mm))

    story.append(p("<b>建议:</b> 使用 Seedance 作为主力工具。1080p 开箱即用，成本低 3 倍，"
                    "画质用于工艺教学动画完全够用。已有完整 API 流程和 9 段成品。"
                    "如果团队评审后认为 Kling 画质差距明显，可随时切换到 Kling pro 方案。", zh))

    doc.build(story)
    print(f"PDF saved: {OUT_PDF}")
    print(f"Size: {os.path.getsize(OUT_PDF) / 1024:.0f} KB")

if __name__ == "__main__":
    build()
