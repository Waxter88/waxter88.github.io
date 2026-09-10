#!/usr/bin/env python3
"""Build Jackson Pipe's one-page resume. Requires ReportLab (see README.md)."""

from io import BytesIO
from pathlib import Path
from xml.sax.saxutils import escape, quoteattr

from reportlab.lib import colors
from reportlab.lib.enums import TA_RIGHT
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (
    BaseDocTemplate, Frame, HRFlowable, PageTemplate,
    Paragraph, Spacer, Table, TableStyle,
)


ROOT = Path(__file__).resolve().parent
DEFAULT_OUTPUT = ROOT / 'Resume_Jackson-Pipe.pdf'
PAGE_W, PAGE_H = letter
MARGIN = 36
BODY_W = PAGE_W - 2 * MARGIN
LABEL_W = 100
CONTENT_W = BODY_W - LABEL_W
PORTFOLIO_URL = 'https://jacksonpipe.dev/'
CERTIFICATE_URL = (
    'https://www.credly.com/badges/8b1faf23-3fe2-46e0-8b53-8ba530f416db/public_url'
)

# Typography and colours follow the portfolio's visual identity.
INK = colors.HexColor('#242922')
BODY = colors.HexColor('#41483f')
MUTED = colors.HexColor('#62695d')
ACCENT = colors.HexColor('#aa422c')
RULE = colors.HexColor('#d4d7cc')


# Edit the content here, then rebuild the downloadable PDF.
# Dates follow index.html and the corrected Niagara dates in this repository.
SUMMARY = (
    'Software developer with full-stack experience and graduate training in cybersecurity.'
)

SKILLS = [
    ('Development',
     'TypeScript, JavaScript, Python, C#, React, Next.js, Node.js, REST APIs'),
    ('Data & tools',
     'SQL, SQLite, MySQL, Microsoft Azure, Docker, Git / GitHub, Linux'),
    ('Security training',
     'Incident response, SIEM/log analysis, vulnerability assessment, network security, '
     'IAM, secure software development'),
]

# Program context: Mohawk's 2025 Program of Studies and official overview.
# https://myssb.mohawkcollege.ca/mcprod/psecrsdes.P_POSGet?pos_prg=557&prg_ver=25-A
# https://www.mohawkcollege.ca/programs/graduate-studies/cyber-security-analytics-557
# Jackson confirmed the tabletop exercise and attack-response simulations.
# Program outcomes support training descriptions, not employment or tool claims.
SECURITY_EXERCISE = (
    'Completed a cyberattack tabletop exercise and simulated attack-response labs, '
    'practising incident response in a controlled training environment.'
)

# Broad credential topics, checked against the official descriptions:
# https://learn.microsoft.com/en-us/credentials/certifications/azure-fundamentals/
# https://www.niagaracollege.ca/media/program/programming/
AZURE_DESCRIPTION = (
    'Validated foundational knowledge of Azure services, cloud security, and governance.'
)
NIAGARA_DESCRIPTION = (
    'Studied software development, database design, and web application programming.'
)

EXPERIENCE = [
    {
        'title': 'Software Developer',
        'context': 'Niagara College · Academic client project',
        'dates': 'Sep 2020 – Apr 2022',
        'description': (
            'Led a five-person student team to build a React, Node.js, and MySQL '
            'business-management platform for a local client. Developed point-of-sale, '
            'inventory, ordering, authentication, payment, and invoicing features, '
            'refining the application through client feedback.'
        ),
    },
    {
        'title': 'Programming Instructor',
        'context': 'Code Ninjas · Code Sensei',
        'dates': 'Oct 2023 – Present',
        'description': (
            'Teach JavaScript, C#, and Lua through game and app development. Adapt lessons '
            'to each student and help them debug code and break down programming problems.'
        ),
    },
    {
        'title': 'Coding Instructor',
        'context': 'Self-employed',
        'dates': 'Jun – Aug 2019',
        'description': (
            'Designed and taught introductory Scratch, Python, and Java lessons for youth, '
            'adapting exercises to different skill levels.'
        ),
    },
]


def register_fonts():
    """Embed the static Manrope instances supplied alongside their OFL licence."""
    font_dir = ROOT / 'assets' / 'fonts'
    for name, filename in (
        ('Resume', 'manrope-regular.ttf'),
        ('Resume-Bold', 'manrope-semibold.ttf'),
    ):
        pdfmetrics.registerFont(TTFont(name, str(font_dir / filename)))
    pdfmetrics.registerFontFamily(
        'Resume', normal='Resume', bold='Resume-Bold',
        italic='Resume', boldItalic='Resume-Bold',
    )


def style(name, **overrides):
    settings = dict(
        fontName='Resume', fontSize=11, leading=15.5, textColor=BODY,
        spaceAfter=0, spaceBefore=0, splitLongWords=False,
    )
    settings.update(overrides)
    return ParagraphStyle(name, **settings)


def link(label, url):
    return f'<link href={quoteattr(url)}>{escape(label)}</link>'


def table(rows, widths, commands=()):
    result = Table(rows, colWidths=widths)
    result.setStyle(TableStyle([
        ('FONTNAME', (0, 0), (-1, -1), 'Resume'),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('LEFTPADDING', (0, 0), (-1, -1), 0),
        ('RIGHTPADDING', (0, 0), (-1, -1), 0),
        ('TOPPADDING', (0, 0), (-1, -1), 0),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 0),
        *commands,
    ]))
    return result


def dated_line(label, dates, width=CONTENT_W, font_size=12.2):
    return table([[
        Paragraph(label, style(
            'entry', fontSize=font_size, leading=16.5, textColor=INK,
        )),
        Paragraph(escape(dates), style(
            'date', fontSize=8.8, leading=16.5, textColor=MUTED, alignment=TA_RIGHT,
        )),
    ]], [width - 100, 100], [
        ('RIGHTPADDING', (0, 0), (0, 0), 8),
    ])


def section(title, content):
    # A narrow label rail introduces one continuous stream of body text.
    return [
        Spacer(1, 12),
        HRFlowable(width='100%', thickness=0.6, color=RULE),
        Spacer(1, 12),
        table([[
            Paragraph(escape(title).replace('\n', '<br/>'), style(
                'section', fontName='Resume-Bold', fontSize=12.5,
                leading=16, textColor=ACCENT,
            )),
            content,
        ]], [LABEL_W, CONTENT_W], [
            ('RIGHTPADDING', (0, 0), (0, 0), 14),
        ]),
    ]


def experience():
    content = []
    for index, item in enumerate(EXPERIENCE):
        if index:
            content.append(Spacer(1, 10))
        content.extend([
            dated_line(f'<b>{escape(item["title"])}</b>', item['dates']),
            Paragraph(escape(item['context']), style(
                'context', fontSize=9.8, leading=14, textColor=MUTED, spaceAfter=4,
            )),
            Paragraph(escape(item['description']), style('experience')),
        ])
    return content


def education():
    meta_style = style('school', fontSize=9.8, leading=14, textColor=MUTED)
    return [
        dated_line('<b>Cyber Security Analytics</b>', '2025 – Apr 2026'),
        Paragraph('Graduate Certificate · Mohawk College', meta_style),
        Spacer(1, 4),
        Paragraph(escape(SECURITY_EXERCISE), style('training')),
        Spacer(1, 10),
        dated_line('<b>' + link('Azure Fundamentals (AZ-900)', CERTIFICATE_URL) + '</b>', '2025'),
        Paragraph('Microsoft Certified', meta_style),
        Spacer(1, 4),
        Paragraph(escape(AZURE_DESCRIPTION), style('certification')),
        Spacer(1, 8),
        dated_line('<b>Computer Programming</b>', '2020 – 2022'),
        Paragraph('Diploma · Niagara College', meta_style),
        Spacer(1, 4),
        Paragraph(escape(NIAGARA_DESCRIPTION), style('diploma')),
    ]


def header():
    contact_style = style('contact', fontSize=9.2, leading=13, textColor=MUTED)
    web_style = style('web-link', fontSize=9.3, leading=13, textColor=MUTED)
    contacts = table([
        [
            Paragraph('Hamilton, Ontario', contact_style),
            Paragraph(link('jackbpipe@gmail.com', 'mailto:jackbpipe@gmail.com'), contact_style),
            Paragraph(link('(289) 776-5958', 'tel:+12897765958'), contact_style),
        ],
        [
            Paragraph('<b><u>' + link('jacksonpipe.dev', PORTFOLIO_URL) + '</u></b>', style(
                'portfolio-link', fontSize=9.8, leading=13, textColor=ACCENT,
            )),
            Paragraph(link('github.com/Waxter88', 'https://github.com/Waxter88'), web_style),
            Paragraph(link(
                'linkedin.com/in/jackson-pipe', 'https://www.linkedin.com/in/jackson-pipe/',
            ), web_style),
        ],
    ], [152, 172, BODY_W - 324], [
        ('BOTTOMPADDING', (0, 0), (-1, 0), 4),
    ])
    return [
        Paragraph('Jackson Pipe', style(
            'name', fontName='Resume-Bold', fontSize=42, leading=47,
            textColor=INK, spaceAfter=5,
        )),
        Paragraph('Software Development &amp; Cybersecurity', style(
            'headline', fontSize=12.2, leading=17, textColor=ACCENT,
        )),
        Spacer(1, 11),
        contacts,
        Spacer(1, 10),
        Paragraph(escape(SUMMARY), style('summary', fontSize=11.2, leading=16)),
    ]


def build(output=DEFAULT_OUTPUT):
    register_fonts()
    # An overflowing edit must not replace the reviewed PDF.
    buffer = BytesIO()
    doc = BaseDocTemplate(
        buffer, pagesize=letter, leftMargin=MARGIN, rightMargin=MARGIN,
        topMargin=MARGIN, bottomMargin=MARGIN, initialFontName='Resume',
        title='Jackson Pipe | Software Development & Cybersecurity',
        author='Jackson Pipe', subject='Resume', lang='en-CA',
        creator='build_resume.py', displayDocTitle=True,
    )
    frame = Frame(
        MARGIN, MARGIN, BODY_W, PAGE_H - 2 * MARGIN,
        leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0,
    )
    doc.addPageTemplates(PageTemplate(id='resume', frames=[frame]))
    story = header()
    story += section('Relevant\nexperience', experience())
    story += section('Education &\ncertification', education())
    story += section('Technical\nskills', [
        Paragraph(f'<b>{escape(label)}:</b> {escape(value)}', style('skills', spaceAfter=5))
        for label, value in SKILLS
    ])
    doc.build(story)
    if doc.page != 1:
        raise ValueError(f'Resume must fit one page; this edit produces {doc.page} pages.')
    output = Path(output)
    output.write_bytes(buffer.getvalue())
    print(f'Written: {output} (1 page)')


if __name__ == '__main__':
    build()
