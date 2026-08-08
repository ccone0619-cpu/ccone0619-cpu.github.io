from pathlib import Path

from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

from build_resume import (
    ACCENT,
    EMAIL,
    INK,
    LINE,
    MUTED,
    PORTFOLIO_URL,
    QUIET,
    SOFT,
    WHITE,
    FONT_LIGHT,
    FONT_MEDIUM,
    draw_bullet,
    draw_labeled_item,
    draw_section_title,
    draw_text_block,
    register_fonts,
)


ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "assets"


RESUMES = [
    {
        "path": ASSETS / "zhao-zhouyu-director-resume.pdf",
        "role": "编导 / 内容制作",
        "subject": "影视飓风编导岗位定制简历",
        "profile": (
            "AIGC 内容创作者，参与多部红果上线短剧。能够从剧情拆解和分镜规划出发，"
            "组织角色、场景与画面资产，推进视频生成、后期剪辑和成片交付；参与制作的一部 AI 漫剧进入红果漫剧新剧榜第 4 名。"
        ),
        "strengths": [
            ("结构化拆解", "把剧情拆成镜头、角色、场景和可执行的制作任务。"),
            ("执行落地", "独立推进所分配剧集，从前期规划到最终成片。"),
            ("视觉叙事", "关注人物情绪、镜头衔接和画面统一，让素材服务剧情。"),
        ],
        "skills": [
            ("内容制作", "剧情拆解 / 分镜规划 / 叙事节奏"),
            ("视觉组织", "角色资产 / 场景资产 / 画面统一"),
            ("AIGC 图像", "Midjourney / Nano Banana"),
            ("视频生成", "Seedance / AI 视频生成"),
            ("后期交付", "Premiere Pro / After Effects / 成片输出"),
        ],
        "bullets": [
            "独立负责所分配剧集，从剧情拆解、分镜规划推进到视频生成、后期剪辑和成片交付。",
            "组织角色、场景和画面资产，控制人物与镜头的一致性，保证生成素材能服务剧情表达。",
            "围绕人物情绪、镜头衔接和叙事节奏做制作判断，串联前期规划与后期输出。",
            "参与多部红果上线短剧制作，其中一部 AI 漫剧进入红果漫剧新剧榜第 4 名。",
        ],
        "works": [
            ("《镇北王》· 红果上榜短剧", "分镜、视觉资产、视频生成、剪辑与交付。"),
            ("《寒假》· 微电影风格短片", "视觉组织、镜头生成、AE 合成与情绪节奏。"),
            ("仿实拍风格短片", "人物关系、镜头节奏与成片质感处理。"),
        ],
        "closing": "从内容拆解到成片交付，适合承担需要结构判断与执行推进的编导工作。",
    },
    {
        "path": ASSETS / "zhao-zhouyu-editor-resume.pdf",
        "role": "视频剪辑师 / 后期制作",
        "subject": "影视飓风视频剪辑师岗位定制简历",
        "profile": (
            "AIGC 内容创作者 / 视频剪辑师，参与多部红果上线短剧。能够独立完成素材筛选、"
            "粗剪、精剪、声音配合、画面合成和成片输出；参与制作的一部 AI 漫剧进入红果漫剧新剧榜第 4 名。"
        ),
        "strengths": [
            ("素材筛选", "依据人物关系、情绪变化和叙事目标筛选有效镜头。"),
            ("节奏剪辑", "通过镜头衔接、动作匹配和音乐节奏组织完整表达。"),
            ("稳定交付", "独立推进剪辑全流程，完成后期处理与成片输出。"),
        ],
        "skills": [
            ("剪辑软件", "Premiere Pro / After Effects"),
            ("剪辑流程", "素材筛选 / 粗剪 / 精剪 / 成片输出"),
            ("画面与声音", "镜头衔接 / 音画配合 / 合成处理"),
            ("素材来源", "AI 视频生成 / 影视与动漫素材整理"),
        ],
        "bullets": [
            "独立负责剪辑全流程，完成素材筛选、粗剪、精剪、声音配合、画面合成和成片输出。",
            "围绕人物情绪与叙事节奏重新组织镜头，处理动作衔接、情绪落点和音乐卡点。",
            "使用 Premiere Pro 和 After Effects 完成剪辑、合成、后期处理及最终交付。",
            "参与多部红果上线短剧制作，其中一部 AI 漫剧进入红果漫剧新剧榜第 4 名。",
        ],
        "works": [
            ("仿实拍风格短片", "人物关系、镜头节奏与成片质感处理。"),
            ("影视与动漫混剪", "镜头筛选、音乐卡点、动作衔接与情绪节奏。"),
            ("《寒假》· 微电影风格短片", "素材筛选、AE 合成、声音配合与成片输出。"),
        ],
        "closing": "可直接承担从素材整理到粗剪、精剪及成片输出的完整剪辑流程。",
    },
]


def build_pdf(spec):
    width, height = A4
    margin = 42
    pdf = canvas.Canvas(str(spec["path"]), pagesize=A4, pageCompression=1)
    pdf.setTitle(f"赵洲钰 - {spec['role']}")
    pdf.setAuthor("赵洲钰")
    pdf.setSubject(spec["subject"])

    pdf.setFillColor(WHITE)
    pdf.rect(0, 0, width, height, stroke=0, fill=1)
    pdf.setFillColor(ACCENT)
    pdf.roundRect(margin, height - 83, 4, 37, 2, stroke=0, fill=1)

    pdf.setFillColor(INK)
    pdf.setFont(FONT_MEDIUM, 30)
    pdf.drawString(margin + 15, height - 64, "赵洲钰")
    pdf.setFont(FONT_MEDIUM, 11.5)
    pdf.drawString(margin + 15, height - 86, spec["role"])

    pdf.setFillColor(MUTED)
    pdf.setFont(FONT_LIGHT, 8.8)
    pdf.drawString(margin, height - 112, "20 岁    |    18570252625    |    微信 Cc1_0619")
    pdf.drawString(margin, height - 129, f"邮箱  {EMAIL}")
    pdf.linkURL(f"mailto:{EMAIL}", (margin, height - 134, margin + 155, height - 120), relative=0)
    pdf.setFillColor(ACCENT)
    pdf.drawRightString(width - margin, height - 129, f"个人作品集  {PORTFOLIO_URL}")
    pdf.linkURL(PORTFOLIO_URL, (width - margin - 230, height - 134, width - margin, height - 120), relative=0)

    pdf.setStrokeColor(INK)
    pdf.setLineWidth(1)
    pdf.line(margin, height - 148, width - margin, height - 148)

    y = height - 171
    y = draw_section_title(pdf, "个人简介", margin, y, width - margin * 2)
    y = draw_text_block(pdf, spec["profile"], margin, y, width - margin * 2, FONT_LIGHT, 9.7, INK, 15)
    y = draw_text_block(pdf, f"联系邮箱：{EMAIL}", margin, y - 2, width - margin * 2, FONT_LIGHT, 8.8, MUTED, 14)
    y -= 12

    left_x = margin
    left_width = 165
    gap = 27
    right_x = left_x + left_width + gap
    right_width = width - margin - right_x
    column_top = y

    left_y = draw_section_title(pdf, "核心优势", left_x, column_top, left_width)
    for title, body in spec["strengths"]:
        left_y = draw_labeled_item(pdf, title, body, left_x, left_y, left_width)

    left_y -= 2
    left_y = draw_section_title(pdf, "专业技能", left_x, left_y, left_width)
    for title, value in spec["skills"]:
        left_y = draw_labeled_item(pdf, title, value, left_x, left_y, left_width)

    left_y -= 2
    left_y = draw_section_title(pdf, "可直接承担", left_x, left_y, left_width)
    draw_text_block(pdf, spec["closing"], left_x, left_y, left_width, FONT_LIGHT, 8.7, INK, 13)

    right_y = draw_section_title(pdf, "项目经历", right_x, column_top, right_width)
    pdf.setFillColor(INK)
    pdf.setFont(FONT_MEDIUM, 16)
    pdf.drawString(right_x, right_y, "红果 AI 漫剧制作")
    right_y -= 17
    pdf.setFillColor(MUTED)
    pdf.setFont(FONT_MEDIUM, 8.5)
    pdf.drawString(right_x, right_y, "分配剧集独立交付  |  多部平台上线项目")
    right_y -= 21
    for bullet in spec["bullets"]:
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
    for title, body in spec["works"]:
        right_y = draw_labeled_item(pdf, title, body, right_x, right_y, right_width)

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
    register_fonts()
    for resume in RESUMES:
        build_pdf(resume)
        print(resume["path"])
