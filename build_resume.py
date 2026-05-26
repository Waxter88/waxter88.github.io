#!/usr/bin/env python3
"""
Polished, professional résumé — Jackson Pipe
Design: DejaVu Sans typeface, dark-navy header, blue accent, clean single-column body.
"""

import os
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib.enums import TA_RIGHT
from reportlab.platypus import (
    BaseDocTemplate, Frame, PageTemplate,
    Paragraph, Spacer, Table, TableStyle, KeepTogether,
)
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

# ── Register DejaVu Sans (clean open-source sans-serif, fully embedded) ────────
FONT_DIR = '/usr/share/fonts/truetype/dejavu'
pdfmetrics.registerFont(TTFont('DV',   os.path.join(FONT_DIR, 'DejaVuSans.ttf')))
pdfmetrics.registerFont(TTFont('DV-B', os.path.join(FONT_DIR, 'DejaVuSans-Bold.ttf')))
pdfmetrics.registerFontFamily('DV', normal='DV', bold='DV-B', italic='DV', boldItalic='DV-B')

PAGE_W, PAGE_H = letter
MARGIN   = 0.50 * inch
BODY_W   = PAGE_W - 2 * MARGIN   # 7.50 inch
HEADER_H = 1.22 * inch
GAP      = 0.10 * inch
BOT_MAR  = 0.35 * inch

# ── Colour palette ─────────────────────────────────────────────────────────────
C_NAVY    = colors.HexColor('#0f172a')
C_ACCENT  = colors.HexColor('#1d4ed8')
C_BODY    = colors.HexColor('#334155')
C_MUTED   = colors.HexColor('#64748b')
C_TINT    = colors.HexColor('#f8fafc')
C_BLUE_LT = colors.HexColor('#93c5fd')
C_CONTACT = colors.HexColor('#94a3b8')
C_HDR_SEP = colors.HexColor('#1e3a5f')
C_ROW_SEP = colors.HexColor('#e2e8f0')


# ══════════════════════════════════════════════════════════════════════════════
# Header — drawn directly on the canvas each page
# ══════════════════════════════════════════════════════════════════════════════
def draw_header(canvas, doc):
    canvas.saveState()

    canvas.setFillColor(C_NAVY)
    canvas.rect(0, PAGE_H - HEADER_H, PAGE_W, HEADER_H, fill=1, stroke=0)

    canvas.setFillColor(C_ACCENT)
    canvas.rect(0, PAGE_H - HEADER_H, 5, HEADER_H, fill=1, stroke=0)

    canvas.setStrokeColor(C_ACCENT)
    canvas.setLineWidth(1.8)
    canvas.line(0, PAGE_H - HEADER_H, PAGE_W, PAGE_H - HEADER_H)

    x = 0.38 * inch

    canvas.setFillColor(colors.white)
    canvas.setFont('DV-B', 23)
    canvas.drawString(x, PAGE_H - 0.49 * inch, 'JACKSON  PIPE')

    canvas.setStrokeColor(C_HDR_SEP)
    canvas.setLineWidth(0.5)
    canvas.line(x, PAGE_H - 0.61 * inch, PAGE_W * 0.52, PAGE_H - 0.61 * inch)

    canvas.setFillColor(C_BLUE_LT)
    canvas.setFont('DV', 10.5)
    canvas.drawString(x, PAGE_H - 0.78 * inch,
                      'Software Developer   \u00b7   Cybersecurity Analyst')

    canvas.setStrokeColor(C_HDR_SEP)
    canvas.setLineWidth(0.3)
    canvas.line(x, PAGE_H - 0.90 * inch, PAGE_W - x, PAGE_H - 0.90 * inch)

    canvas.setFillColor(C_CONTACT)
    canvas.setFont('DV', 8.0)
    sep = '   \u00b7   '
    line1 = sep.join(['jackbpipe@gmail.com', '(289) 776-5958', 'Hamilton, ON, Canada'])
    line2 = sep.join(['github.com/Waxter88', 'linkedin.com/in/jackson-pipe', 'waxter88.github.io'])
    canvas.drawString(x, PAGE_H - 1.04 * inch, line1)
    canvas.drawString(x, PAGE_H - 1.17 * inch, line2)

    canvas.restoreState()


# ══════════════════════════════════════════════════════════════════════════════
# Style helpers
# ══════════════════════════════════════════════════════════════════════════════
def ps(name, **kw):
    base = dict(fontName='DV', fontSize=9.2, leading=13.2,
                textColor=C_BODY, spaceAfter=0, spaceBefore=0)
    base.update(kw)
    return ParagraphStyle(name, **base)


def section(title):
    sty = ps('_sh', fontName='DV-B', fontSize=8.0, textColor=C_NAVY)
    tbl = Table([[Paragraph(title.upper(), sty)]], colWidths=[BODY_W])
    tbl.setStyle(TableStyle([
        ('BACKGROUND',    (0, 0), (0, 0), C_TINT),
        ('TOPPADDING',    (0, 0), (0, 0), 4),
        ('BOTTOMPADDING', (0, 0), (0, 0), 4),
        ('LEFTPADDING',   (0, 0), (0, 0), 7),
        ('RIGHTPADDING',  (0, 0), (0, 0), 0),
        ('LINEBEFORE',    (0, 0), (0, 0), 3.5, C_ACCENT),
        ('LINEBELOW',     (0, 0), (0, 0), 0.75, C_ACCENT),
    ]))
    return [Spacer(1, 3), tbl, Spacer(1, 1)]


def job_entry(title, company, location, date_str):
    t_sty = ps('_jt', fontName='DV-B', fontSize=9.6, textColor=C_NAVY,
               spaceBefore=4, spaceAfter=0)
    d_sty = ps('_jd', fontName='DV', fontSize=8.2, textColor=C_MUTED,
               alignment=TA_RIGHT, spaceBefore=4, spaceAfter=0)
    m_sty = ps('_jm', fontName='DV', fontSize=8.4, textColor=C_MUTED, spaceAfter=3)

    D1, D2 = BODY_W * 0.67, BODY_W * 0.33
    title_row = Table(
        [[Paragraph(title, t_sty), Paragraph(date_str, d_sty)]],
        colWidths=[D1, D2],
    )
    title_row.setStyle(TableStyle([
        ('VALIGN',        (0, 0), (-1, -1), 'BOTTOM'),
        ('TOPPADDING',    (0, 0), (-1, -1), 0),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 1),
        ('LEFTPADDING',   (0, 0), (-1, -1), 0),
        ('RIGHTPADDING',  (0, 0), (-1, -1), 0),
    ]))
    meta = Paragraph(f'{company}  \u00b7  {location}', m_sty)
    return [title_row, meta]


def b(text):
    sty = ps('_b', leftIndent=13, firstLineIndent=0, spaceAfter=1, leading=12.8)
    return Paragraph(f'\u2013\u2002{text}', sty)


def skills_two_col(rows):
    """Render 6 skill rows as a 2-column 3-row table to save vertical space."""
    lbl = ps('_sl', fontName='DV-B', fontSize=8.0, textColor=C_NAVY, leading=12.5)
    val = ps('_sv', fontSize=8.0, textColor=C_BODY, leading=12.5)

    GAP_COL = 0.22 * inch
    HALF    = (BODY_W - GAP_COL) / 2
    L_W     = 1.18 * inch
    V_W     = HALF - L_W

    # Pair rows: left=[0,1,2], right=[3,4,5]
    pairs = [(rows[i], rows[i + 3]) for i in range(3)]

    tbl_rows = []
    for (l1, v1), (l2, v2) in pairs:
        tbl_rows.append([
            Paragraph(l1, lbl), Paragraph(v1, val),
            Paragraph('', val),   # spacer column
            Paragraph(l2, lbl), Paragraph(v2, val),
        ])

    tbl = Table(tbl_rows, colWidths=[L_W, V_W, GAP_COL, L_W, V_W])
    tbl.setStyle(TableStyle([
        ('VALIGN',        (0, 0), (-1, -1), 'TOP'),
        ('TOPPADDING',    (0, 0), (-1, -1), 3),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
        ('LEFTPADDING',   (0, 0), (-1, -1), 0),
        ('RIGHTPADDING',  (0, 0), (0, -1),  4),
        ('RIGHTPADDING',  (1, 0), (1, -1),  0),
        ('RIGHTPADDING',  (3, 0), (3, -1),  4),
        ('RIGHTPADDING',  (4, 0), (4, -1),  0),
        # Alternating row tints
        ('BACKGROUND',    (0, 0), (1, 0),   C_TINT),
        ('BACKGROUND',    (3, 0), (4, 0),   C_TINT),
        ('BACKGROUND',    (0, 2), (1, 2),   C_TINT),
        ('BACKGROUND',    (3, 2), (4, 2),   C_TINT),
        # Hair-line row separators
        ('LINEBELOW',     (0, 0), (1, 1),   0.3, C_ROW_SEP),
        ('LINEBELOW',     (3, 0), (4, 1),   0.3, C_ROW_SEP),
        # Vertical centre divider
        ('LINEAFTER',     (1, 0), (1, -1),  0.4, C_ROW_SEP),
    ]))
    return tbl


# ══════════════════════════════════════════════════════════════════════════════
# Document assembly
# ══════════════════════════════════════════════════════════════════════════════
def build(output='Resume_Jackson-Pipe.pdf'):
    frame = Frame(
        MARGIN, BOT_MAR, BODY_W,
        PAGE_H - HEADER_H - GAP - BOT_MAR,
        id='main', showBoundary=0,
        leftPadding=0, rightPadding=0,
        topPadding=0, bottomPadding=0,
    )
    doc = BaseDocTemplate(
        output, pagesize=letter,
        leftMargin=MARGIN, rightMargin=MARGIN,
        topMargin=HEADER_H + GAP, bottomMargin=BOT_MAR,
    )
    doc.addPageTemplates([
        PageTemplate(id='main', frames=[frame], onPage=draw_header)
    ])

    story = []

    # ── Professional Summary ───────────────────────────────────────────────────
    story += section('Professional Summary')
    story.append(Paragraph(
        'Results-driven Software Developer and Cybersecurity Analyst with 3+ years of full-stack '
        'development experience and a Graduate Certificate in Cyber Security Analytics (Mohawk '
        'College, 2024\u20132025). Adept at architecting scalable web applications while applying '
        'security-first principles \u2014 penetration testing, threat detection, SIEM log analysis, '
        'and Azure cloud security. Holds the <b>Microsoft Certified: Azure Fundamentals (AZ-900)</b> '
        'credential. Bridges software engineering and cybersecurity to deliver products that are '
        'performant, maintainable, and resilient against modern threats.',
        ps('_sum', leading=13.5, spaceAfter=0),
    ))

    # ── Experience ────────────────────────────────────────────────────────────
    story += section('Experience')

    story.append(KeepTogether([
        *job_entry('Code Sensei', 'Code Ninjas',
                   'Hamilton, ON', 'Oct 2023 \u2013 Present'),
        b('Mentor students through a self-paced, game-based curriculum, teaching programming '
          'fundamentals in JavaScript, C#, and Lua as they build their own games and apps.'),
        b('Break down complex programming concepts into accessible, hands-on lessons tailored to '
          'each student\u2019s skill level, reinforcing problem-solving and debugging as they advance '
          'through belt-based skill tiers.'),
    ]))

    story.append(KeepTogether([
        *job_entry('Software Developer', 'Niagara College Canada',
                   'Welland, ON', 'Sep 2021 \u2013 Apr 2023'),
        b('Led a cross-functional team of 5 in Agile/Scrum to architect and deliver a full-stack '
          'business-management platform for a local small-business client, on time and within scope.'),
        b('Designed and built core modules: POS system, inventory and supply-chain management, '
          'order processing, user authentication, payment-gateway integration, and automated '
          'invoice/receipt generation.'),
        b('Iterated on prototypes via user-feedback loops; final product exceeded all client '
          'requirements and received top marks from the academic evaluation panel.'),
        b('Stack: React \u00b7 Node.js \u00b7 MySQL \u00b7 Bootstrap \u00b7 RESTful APIs.'),
    ]))

    story.append(KeepTogether([
        *job_entry('Coding Instructor', 'Self-Employed',
                   'Hamilton, ON', 'Jun \u2013 Aug 2019'),
        b('Designed and delivered introductory programming curricula for youth using Scratch, Python, '
          'and Java, adapting lessons to diverse skill levels.'),
        b('Translated complex technical concepts into accessible material \u2014 directly applicable '
          'to code reviews, documentation, and team mentoring.'),
    ]))


    # ── Education & Certifications ──────────────────────────────────────────
    story += section('Education & Certifications')

    story.append(KeepTogether([
        *job_entry('Graduate Certificate \u2014 Cyber Security Analytics',
                   'Mohawk College', 'Hamilton, ON', '2025 \u2013 2026'),
        Paragraph(
            '\u2013\u2002<b>Microsoft Certified: Azure Fundamentals (AZ-900)</b>'
            '  \u2014  Microsoft  \u00b7  2024',
            ps('_cert', leftIndent=13, leading=13, spaceBefore=4, spaceAfter=0),
        ),
    ]))

    story.append(KeepTogether(job_entry(
        'Diploma \u2014 Computer Programming',
        'Niagara College', 'Welland, ON', '2020 \u2013 2022')))

    # ── Technical Skills ──────────────────────────────────────────────────────
    story += section('Technical Skills')

    skill_rows = [
        ('Languages',      'JavaScript / TypeScript,  Python,  C#,  C++,  SQL'),
        ('Front-End',      'React,  HTML5,  CSS3,  Bootstrap'),
        ('Back-End',       'Node.js,  Express,  ASP.NET Core,  RESTful APIs'),
        ('Databases',      'MySQL,  Microsoft SQL Server,  MongoDB'),
        ('Cloud\u00a0&\u00a0DevOps', 'Microsoft Azure,  Docker,  Git / GitHub,  Linux'),
        ('Security',
         'Pen Testing,  Network Security,  SIEM & Log Analysis,  '
         'Threat Detection & Response,  Vuln. Assessment,  '
         'Incident Response,  Digital Forensics,  Compliance & Governance'),
    ]

    story.append(skills_two_col(skill_rows))

    doc.build(story)
    print(f'\u2713  {output}  written.')


if __name__ == '__main__':
    build()
