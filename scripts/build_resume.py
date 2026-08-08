from pathlib import Path

from reportlab.lib.colors import HexColor
from reportlab.lib.pagesizes import A4
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas


ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "assets"
PDF_PATH = ASSETS / "zhao-zhouyu-resume.pdf"
PORTFOLIO_URL = "https://ccone0619-cpu.github.io/"

INK = HexColor("#1D1D1F")
MUTED = HexColor("#6E6E73")
QUIET = HexColor("#86868B")
LINE = HexColor("#D2D2D7")
ACCENT = HexColor("#0071E3")
SOFT = HexColor("#F5F5F7")
WHITE = HexColor("#FFFFFF")

FONT_LIGHT = "ResumeLight"
FONT_MEDIUM = "ResumeMedium"


PROFILE = (
    "熟悉 AI 漫剧完整制作流程及主流 AIGC 创作工具，拥有个人创作工作流。"
    "参与多部红果上线短剧，能够独立完成所分配剧集的分镜、视觉资产、视频生成、剪辑及成片输出。"
)

STRENGTHS = [
    ("独立推进", "接到分配剧集后，自主拆解任务并推进至最终成片。"),
    ("成片判断", "从人物情绪、镜头衔接和叙事节奏判断素材。"),
    ("上线经验", "参与多部红果上线项目，理解实际交付要求。"),
]

PROJECT_BULLETS = [
    "独立负责所分配剧集，从剧情拆解和分镜设计推进到最终成片。",
    "使用 Midjourney、Image 生成画面，以 Nano Banana 制作 4K 视觉资产，并通过 Seedance 生成视频。",
    "使用 After Effects 和 Premiere Pro 完成合成、节奏剪辑、声音配合与成片输出。",
    "参与制作的一部 AI 漫剧进入红果漫剧新剧榜第 4 名。",
]

WORKS = [
    ("《镇北王》· 红果上榜短剧", "负责分镜、视觉资产、视频生成、剪辑与交付。"),
    ("影视与动漫混剪", "展示镜头筛选、音乐卡点、动作衔接与情绪节奏。"),
    ("《寒假》· 微电影风格短片", "完成视觉组织、素材筛选、AE 合成与节奏剪辑。"),
]


def register_fonts():
    pdfmetrics.registerFont(TTFont(FONT_LIGHT, "/System/Library/Fonts/STHeiti Light.ttc"))
    pdfmetrics.registerFont(TTFont(FONT_MEDIUM, "/System/Library/Fonts/STHeiti Medium.ttc"))


def wrap_text(text, font_name, font_size, max_width):
    lines = []
    current = ""
    for char in text:
        candidate = current + char
        if current and pdfmetrics.stringWidth(candidate, font_name, font_size) > max_width:
            lines.append(current.rstrip())
            current = char.lstrip()
        else:
            current = candidate
    if current:
        lines.append(current.rstrip())
    return lines


def draw_text_block(pdf, text, x, y, width, font_name, font_size, color, leading):
    pdf.setFillColor(color)
    pdf.setFont(font_name, font_size)
    for line in wrap_text(text, font_name, font_size, width):
        pdf.drawString(x, y, line)
        y -= leading
    return y


def draw_section_title(pdf, title, x, y, width):
    pdf.setFillColor(ACCENT)
    pdf.roundRect(x, y - 1, 3, 13, 1.5, stroke=0, fill=1)
    pdf.setFillColor(INK)
    pdf.setFont(FONT_MEDIUM, 11)
    pdf.drawString(x + 10, y, title)
    pdf.setStrokeColor(LINE)
    pdf.setLineWidth(0.6)
    pdf.line(x, y - 9, x + width, y - 9)
    return y - 27


def draw_bullet(pdf, text, x, y, width, font_size=9, leading=14):
    pdf.setFillColor(ACCENT)
    pdf.circle(x + 2.5, y + 3.2, 1.5, stroke=0, fill=1)
    return draw_text_block(pdf, text, x + 12, y, width - 12, FONT_LIGHT, font_size, INK, leading) - 4


def draw_labeled_item(pdf, title, body, x, y, width):
    pdf.setFillColor(INK)
    pdf.setFont(FONT_MEDIUM, 9.7)
    pdf.drawString(x, y, title)
    y -= 15
    y = draw_text_block(pdf, body, x, y, width, FONT_LIGHT, 8.7, MUTED, 13.2)
    return y - 11


def build_pdf():
    register_fonts()
    width, height = A4
    margin = 42
    pdf = canvas.Canvas(str(PDF_PATH), pagesize=A4, pageCompression=1)
    pdf.setTitle("赵洲钰 - 个人简历")
    pdf.setAuthor("赵洲钰")
    pdf.setSubject("AIGC 内容创作者 / 视频剪辑师")

    pdf.setFillColor(WHITE)
    pdf.rect(0, 0, width, height, stroke=0, fill=1)
    pdf.setFillColor(ACCENT)
    pdf.roundRect(margin, height - 83, 4, 37, 2, stroke=0, fill=1)

    pdf.setFillColor(INK)
    pdf.setFont(FONT_MEDIUM, 30)
    pdf.drawString(margin + 15, height - 64, "赵洲钰")
    pdf.setFont(FONT_MEDIUM, 11.5)
    pdf.drawString(margin + 15, height - 86, "AIGC 内容创作者 / 视频剪辑师")

    pdf.setFillColor(MUTED)
    pdf.setFont(FONT_LIGHT, 8.8)
    pdf.drawString(margin, height - 112, "杭州 · 20 岁    |    18570252625    |    微信 Cc1_0619")
    pdf.setFillColor(ACCENT)
    pdf.drawString(margin, height - 129, f"个人作品集  {PORTFOLIO_URL}")
    pdf.linkURL(PORTFOLIO_URL, (margin, height - 134, margin + 230, height - 120), relative=0)

    pdf.setStrokeColor(INK)
    pdf.setLineWidth(1)
    pdf.line(margin, height - 148, width - margin, height - 148)

    y = height - 171
    y = draw_section_title(pdf, "个人简介", margin, y, width - margin * 2)
    y = draw_text_block(pdf, PROFILE, margin, y, width - margin * 2, FONT_LIGHT, 9.7, INK, 15)
    y -= 12

    left_x = margin
    left_width = 165
    gap = 27
    right_x = left_x + left_width + gap
    right_width = width - margin - right_x
    column_top = y

    left_y = draw_section_title(pdf, "核心优势", left_x, column_top, left_width)
    for title, body in STRENGTHS:
        left_y = draw_labeled_item(pdf, title, body, left_x, left_y, left_width)

    left_y -= 2
    left_y = draw_section_title(pdf, "专业技能", left_x, left_y, left_width)
    skill_groups = [
        ("剪辑与后期", "Premiere Pro / After Effects"),
        ("内容制作", "分镜制作 / 叙事节奏 / 视觉统一"),
        ("图像工具", "Midjourney / Nano Banana"),
        ("视频工具", "Seedance / AI 视频生成"),
        ("成片能力", "素材筛选 / 成片输出"),
    ]
    for title, value in skill_groups:
        left_y = draw_labeled_item(pdf, title, value, left_x, left_y, left_width)

    left_y -= 2
    left_y = draw_section_title(pdf, "求职方向", left_x, left_y, left_width)
    left_y = draw_text_block(
        pdf,
        "视频剪辑 / 内容制作 / AIGC 视频相关岗位",
        left_x,
        left_y,
        left_width,
        FONT_LIGHT,
        8.7,
        INK,
        13,
    )

    right_y = draw_section_title(pdf, "项目经历", right_x, column_top, right_width)
    pdf.setFillColor(INK)
    pdf.setFont(FONT_MEDIUM, 16)
    pdf.drawString(right_x, right_y, "红果 AI 漫剧制作")
    right_y -= 17
    pdf.setFillColor(MUTED)
    pdf.setFont(FONT_MEDIUM, 8.5)
    pdf.drawString(right_x, right_y, "分配剧集独立交付  |  多部平台上线项目")
    right_y -= 21
    for bullet in PROJECT_BULLETS:
        right_y = draw_bullet(pdf, bullet, right_x, right_y, right_width)

    box_height = 55
    right_y -= 2
    pdf.setFillColor(SOFT)
    pdf.roundRect(right_x, right_y - box_height + 8, right_width, box_height, 5, stroke=0, fill=1)
    pdf.setFillColor(ACCENT)
    pdf.setFont(FONT_MEDIUM, 8.3)
    pdf.drawString(right_x + 13, right_y - 7, "项目结果")
    pdf.setFillColor(INK)
    pdf.setFont(FONT_MEDIUM, 12.5)
    pdf.drawString(right_x + 13, right_y - 26, "红果漫剧新剧榜第 4 名")
    pdf.setFillColor(MUTED)
    pdf.setFont(FONT_LIGHT, 7.8)
    pdf.drawString(right_x + 13, right_y - 40, "参与制作项目获得可验证的上线榜单成绩")
    right_y -= box_height + 16

    right_y = draw_section_title(pdf, "代表作品", right_x, right_y, right_width)
    for title, body in WORKS:
        right_y = draw_labeled_item(pdf, title, body, right_x, right_y, right_width)

    workflow_y = 106
    workflow_height = 58
    pdf.setFillColor(SOFT)
    pdf.roundRect(margin, workflow_y, width - margin * 2, workflow_height, 6, stroke=0, fill=1)
    pdf.setFillColor(ACCENT)
    pdf.setFont(FONT_MEDIUM, 8.4)
    pdf.drawString(margin + 14, workflow_y + 36, "我的工作流")
    pdf.setFillColor(INK)
    pdf.setFont(FONT_MEDIUM, 9.1)
    pdf.drawString(
        margin + 14,
        workflow_y + 17,
        "剧情拆解  →  分镜设计  →  视觉资产  →  视频生成  →  后期剪辑  →  成片交付",
    )

    pdf.setStrokeColor(LINE)
    pdf.setLineWidth(0.6)
    pdf.line(margin, 44, width - margin, 44)
    pdf.setFillColor(QUIET)
    pdf.setFont(FONT_LIGHT, 7.4)
    pdf.drawString(margin, 28, "更多成片、项目画布与制作过程请查看个人作品集")
    pdf.setFillColor(ACCENT)
    pdf.drawRightString(width - margin, 28, PORTFOLIO_URL)
    pdf.linkURL(PORTFOLIO_URL, (width - margin - 150, 22, width - margin, 35), relative=0)

    pdf.showPage()
    pdf.save()


if __name__ == "__main__":
    ASSETS.mkdir(parents=True, exist_ok=True)
    build_pdf()
    print(PDF_PATH)
