from pathlib import Path

from reportlab.graphics import renderPDF
from reportlab.graphics.barcode.qr import QrCodeWidget
from reportlab.graphics.shapes import Drawing
from reportlab.lib.colors import HexColor
from reportlab.lib.pagesizes import A4
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas


ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "assets"
PDF_PATH = ASSETS / "zhao-zhouyu-resume.pdf"
PORTFOLIO_URL = "https://ccone0619-cpu.github.io/"
EMAIL = "ccone0619@gmail.com"

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
    "AIGC 内容创作者与视频剪辑师，参与多部红果上线短剧。"
    "能够独立推进所分配剧集，从剧情拆解、分镜与视觉资产制作，到视频生成、"
    "后期剪辑和成片交付。"
)

STRENGTHS = [
    ("独立推进", "接到分配剧集后，自主拆解任务并推进至最终成片。"),
    ("成片判断", "从人物情绪、镜头衔接和叙事节奏判断素材。"),
    ("上线经验", "参与多部红果上线项目，理解实际交付要求。"),
]

PROJECT_BULLETS = [
    "参与多部红果上线短剧，独立负责所分配剧集并推进至成片交付。",
    "使用 Midjourney、Image 与 Nano Banana 制作角色、场景及 4K 视觉资产。",
    "通过 Seedance 生成视频；使用 After Effects、Premiere Pro 完成素材筛选、剪辑、合成、声音配合与成片输出。",
    "参与多部红果上线项目，其中一部 AI 漫剧进入红果漫剧新剧榜第 4 名。",
]

WORKS = [
    ("仿实拍风格短片", "人物关系、镜头节奏与成片质感处理。"),
    ("《镇北王》· 红果上榜短剧", "分镜、视觉资产、视频生成、剪辑与交付。"),
    ("《寒假》· 微电影风格短片", "视觉组织、素材筛选、AE 合成与节奏剪辑。"),
]

DIRECT_DELIVERY = (
    "剧情拆解、分镜与视觉资产制作、AI 视频生成、后期剪辑与成片输出；"
    "可独立推进所分配剧集的完整制作。"
)


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


def draw_editorial_title(pdf, index, title, x, y, width):
    pdf.setFillColor(ACCENT)
    pdf.setFont("Helvetica-Bold", 7.2)
    pdf.drawString(x, y + 1, index)
    pdf.setFillColor(INK)
    pdf.setFont(FONT_MEDIUM, 11.2)
    pdf.drawString(x + 24, y, title)
    pdf.setStrokeColor(LINE)
    pdf.setLineWidth(0.6)
    pdf.line(x, y - 9, x + width, y - 9)
    return y - 27


def draw_compact_item(pdf, title, body, x, y, width):
    pdf.setFillColor(INK)
    pdf.setFont(FONT_MEDIUM, 9.2)
    pdf.drawString(x, y, title)
    y = draw_text_block(pdf, body, x, y - 15, width, FONT_LIGHT, 8.2, MUTED, 12.2)
    return y - 9


def draw_contact_item(pdf, label, value, x, y, link=None):
    pdf.setFillColor(QUIET)
    pdf.setFont(FONT_MEDIUM, 7.2)
    pdf.drawString(x, y, label)
    pdf.setFillColor(INK)
    pdf.setFont(FONT_LIGHT, 8.7)
    pdf.drawString(x, y - 13, value)
    if link:
        link_width = pdfmetrics.stringWidth(value, FONT_LIGHT, 8.7)
        pdf.linkURL(link, (x, y - 16, x + link_width, y - 3), relative=0)


def draw_qr(pdf, value, x, y, size):
    qr = QrCodeWidget(value)
    x1, y1, x2, y2 = qr.getBounds()
    width = x2 - x1
    height = y2 - y1
    drawing = Drawing(size, size, transform=[size / width, 0, 0, size / height, 0, 0])
    drawing.add(qr)
    renderPDF.draw(drawing, pdf, x, y)
    pdf.linkURL(value, (x, y, x + size, y + size), relative=0)


def build_pdf():
    register_fonts()
    width, height = A4
    margin = 40
    pdf = canvas.Canvas(str(PDF_PATH), pagesize=A4, pageCompression=1)
    pdf.setTitle("赵洲钰 - 个人简历")
    pdf.setAuthor("赵洲钰")
    pdf.setSubject("AIGC 内容创作者 / 视频剪辑师")

    pdf.setFillColor(WHITE)
    pdf.rect(0, 0, width, height, stroke=0, fill=1)

    proof_width = 158
    proof_x = width - margin - proof_width
    proof_y = height - 156

    pdf.setFillColor(ACCENT)
    pdf.rect(margin, height - 143, 4, 92, stroke=0, fill=1)
    pdf.setFillColor(QUIET)
    pdf.setFont("Helvetica-Bold", 7.3)
    pdf.drawString(margin + 16, height - 50, "PERSONAL RESUME")
    pdf.setFillColor(INK)
    pdf.setFont(FONT_MEDIUM, 34)
    pdf.drawString(margin + 14, height - 91, "赵洲钰")
    pdf.setFillColor(MUTED)
    pdf.setFont("Helvetica-Bold", 8.2)
    pdf.drawString(margin + 16, height - 110, "ZHAO ZHOUYU")
    pdf.setFillColor(INK)
    pdf.setFont(FONT_MEDIUM, 11.3)
    pdf.drawString(margin + 14, height - 137, "AIGC 内容创作者 / 视频剪辑师")

    pdf.setFillColor(SOFT)
    pdf.roundRect(proof_x, proof_y, proof_width, 108, 7, stroke=0, fill=1)
    pdf.setFillColor(ACCENT)
    pdf.roundRect(proof_x + 16, proof_y + 91, 24, 3, 1.5, stroke=0, fill=1)
    pdf.setFillColor(QUIET)
    pdf.setFont("Helvetica-Bold", 7.2)
    pdf.drawString(proof_x + 16, proof_y + 79, "VERIFIED PROJECT RESULT")
    pdf.setFillColor(INK)
    pdf.setFont("Helvetica-Bold", 27)
    pdf.drawString(proof_x + 16, proof_y + 45, "TOP 4")
    pdf.setFont(FONT_MEDIUM, 9.1)
    pdf.drawString(proof_x + 16, proof_y + 25, "红果漫剧新剧榜")
    pdf.setFillColor(MUTED)
    pdf.setFont(FONT_LIGHT, 7.5)
    pdf.drawString(proof_x + 16, proof_y + 10, "参与制作项目获得上线成绩")

    contact_y = height - 178
    draw_contact_item(pdf, "PHONE", "18570252625", margin, contact_y, "tel:18570252625")
    draw_contact_item(pdf, "AGE", "20", margin + 112, contact_y)
    draw_contact_item(pdf, "WECHAT", "Cc1_0619", margin + 177, contact_y)
    draw_contact_item(pdf, "EMAIL", EMAIL, margin + 283, contact_y, f"mailto:{EMAIL}")
    pdf.setStrokeColor(INK)
    pdf.setLineWidth(1)
    pdf.line(margin, height - 204, width - margin, height - 204)

    left_x = margin
    left_width = 172
    gap = 24
    right_x = left_x + left_width + gap
    right_width = width - margin - right_x
    main_top = height - 230

    pdf.setFillColor(HexColor("#F7F7F8"))
    pdf.rect(left_x - 12, 62, left_width + 24, main_top - 48, stroke=0, fill=1)

    left_y = draw_editorial_title(pdf, "01", "核心能力", left_x, main_top, left_width)
    for title, body in STRENGTHS:
        left_y = draw_compact_item(pdf, title, body, left_x, left_y, left_width)

    left_y -= 4
    left_y = draw_editorial_title(pdf, "02", "工具与技能", left_x, left_y, left_width)
    skill_groups = [
        ("剪辑与后期", "Premiere Pro / After Effects"),
        ("内容制作", "分镜制作 / 叙事节奏 / 视觉统一"),
        ("视觉资产", "Midjourney / Image / Nano Banana"),
        ("视频生成", "Seedance / AI 视频生成 / 成片输出"),
    ]
    for title, value in skill_groups:
        left_y = draw_compact_item(pdf, title, value, left_x, left_y, left_width)

    qr_title_y = 173
    draw_editorial_title(pdf, "03", "作品集", left_x, qr_title_y, left_width)
    qr_size = 68
    draw_qr(pdf, PORTFOLIO_URL, left_x, 74, qr_size)
    pdf.setFillColor(INK)
    pdf.setFont(FONT_MEDIUM, 8.4)
    pdf.drawString(left_x + 80, 124, "扫码查看成片")
    pdf.setFillColor(MUTED)
    pdf.setFont(FONT_LIGHT, 7.6)
    pdf.drawString(left_x + 80, 109, "视频 / 项目画布")
    pdf.drawString(left_x + 80, 96, "制作过程证据")
    pdf.setFillColor(ACCENT)
    pdf.setFont("Helvetica-Bold", 6.8)
    pdf.drawString(left_x + 80, 78, "PORTFOLIO")

    right_y = draw_editorial_title(pdf, "01", "个人简介", right_x, main_top, right_width)
    right_y = draw_text_block(pdf, PROFILE, right_x, right_y, right_width, FONT_LIGHT, 9, INK, 14)
    right_y -= 10

    right_y = draw_editorial_title(pdf, "02", "工作经历", right_x, right_y, right_width)
    pdf.setFillColor(INK)
    pdf.setFont(FONT_MEDIUM, 15)
    pdf.drawString(right_x, right_y, "AI 漫剧内容制作")
    pdf.setFillColor(MUTED)
    pdf.setFont(FONT_MEDIUM, 8.1)
    pdf.drawRightString(right_x + right_width, right_y + 2, "2025.11 — 2026.07")
    right_y -= 18
    pdf.setFillColor(ACCENT)
    pdf.setFont("Helvetica-Bold", 7.2)
    pdf.drawString(right_x, right_y, "ROLE")
    pdf.setFillColor(MUTED)
    pdf.setFont(FONT_LIGHT, 8.2)
    pdf.drawString(right_x + 32, right_y, "AIGC 内容创作者 / 视频剪辑师")
    right_y -= 22
    for bullet in PROJECT_BULLETS:
        right_y = draw_bullet(pdf, bullet, right_x, right_y, right_width, font_size=8.6, leading=13)

    result_height = 58
    right_y -= 1
    pdf.setFillColor(SOFT)
    pdf.roundRect(right_x, right_y - result_height + 6, right_width, result_height, 5, stroke=0, fill=1)
    pdf.setFillColor(ACCENT)
    pdf.setFont("Helvetica-Bold", 7)
    pdf.drawString(right_x + 13, right_y - 8, "RESULT")
    pdf.setFillColor(INK)
    pdf.setFont(FONT_MEDIUM, 12.3)
    pdf.drawString(right_x + 13, right_y - 27, "红果漫剧新剧榜第 4 名")
    pdf.setFillColor(MUTED)
    pdf.setFont(FONT_LIGHT, 7.6)
    pdf.drawString(right_x + 13, right_y - 41, "参与制作项目获得可验证的上线榜单成绩")
    right_y -= result_height + 12

    right_y = draw_editorial_title(pdf, "03", "代表作品", right_x, right_y, right_width)
    for index, (title, body) in enumerate(WORKS, start=1):
        pdf.setFillColor(QUIET)
        pdf.setFont("Helvetica-Bold", 7)
        pdf.drawString(right_x, right_y + 1, f"0{index}")
        pdf.setFillColor(INK)
        pdf.setFont(FONT_MEDIUM, 9.4)
        pdf.drawString(right_x + 25, right_y, title)
        right_y = draw_text_block(pdf, body, right_x + 25, right_y - 14, right_width - 25, FONT_LIGHT, 8.1, MUTED, 12)
        right_y -= 8

    right_y = draw_editorial_title(pdf, "04", "可直接承担", right_x, right_y - 2, right_width)
    draw_text_block(pdf, DIRECT_DELIVERY, right_x, right_y, right_width, FONT_LIGHT, 8.4, INK, 13)

    pdf.setStrokeColor(LINE)
    pdf.setLineWidth(0.6)
    pdf.line(margin, 44, width - margin, 44)
    pdf.setFillColor(QUIET)
    pdf.setFont(FONT_LIGHT, 7.2)
    pdf.drawString(margin, 28, "完整成片、项目画布与制作过程请查看个人作品集")
    pdf.setFillColor(ACCENT)
    pdf.setFont("Helvetica", 7.2)
    pdf.drawRightString(width - margin, 28, PORTFOLIO_URL)
    pdf.linkURL(PORTFOLIO_URL, (width - margin - 155, 22, width - margin, 35), relative=0)

    pdf.showPage()
    pdf.save()


if __name__ == "__main__":
    ASSETS.mkdir(parents=True, exist_ok=True)
    build_pdf()
    print(PDF_PATH)
