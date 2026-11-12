#!/usr/bin/env python3
"""Build the preliminary Volume I manuscript as a navigable PDF."""
from pathlib import Path
from xml.sax.saxutils import escape
import re
import math
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.platypus import (BaseDocTemplate, PageTemplate, Frame, Paragraph,
    Spacer, PageBreak, Preformatted, KeepTogether, Flowable)
from reportlab.platypus.tableofcontents import TableOfContents
from reportlab.lib.utils import ImageReader

ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent
OUT = ROOT / 'output' / 'volume_i_incomplete_manuscript.pdf'
FONT = Path('/usr/share/fonts/truetype/dejavu')
for name, file in [('Book','DejaVuSerif.ttf'), ('BookBold','DejaVuSerif-Bold.ttf'),
                   ('BookItalic','DejaVuSerif.ttf'), ('Sans','DejaVuSans.ttf'),
                   ('SansBold','DejaVuSans-Bold.ttf'), ('Mono','DejaVuSansMono.ttf')]:
    pdfmetrics.registerFont(TTFont(name, str(FONT / file)))
pdfmetrics.registerFontFamily('Book', normal='Book', bold='BookBold', italic='BookItalic', boldItalic='BookBold')
W, H = 432, 648
INK=colors.HexColor('#172536'); BLUE=colors.HexColor('#253b50'); GOLD=colors.HexColor('#b3904b'); MUTED=colors.HexColor('#617181')
styles = {
 'body': ParagraphStyle('body', fontName='Book', fontSize=9.25, leading=14.4, textColor=INK, spaceAfter=8.3, allowWidows=0, allowOrphans=0),
 'h1': ParagraphStyle('h1', fontName='BookBold', fontSize=19, leading=25, textColor=BLUE, spaceBefore=6, spaceAfter=18, keepWithNext=True),
 'h2': ParagraphStyle('h2', fontName='SansBold', fontSize=11.5, leading=16, textColor=BLUE, spaceBefore=17, spaceAfter=9, keepWithNext=True),
 'h3': ParagraphStyle('h3', fontName='SansBold', fontSize=9.5, leading=13, textColor=BLUE, spaceBefore=10, spaceAfter=5, keepWithNext=True),
 'toc': ParagraphStyle('toc', fontName='Book', fontSize=10, leading=19, leftIndent=0, firstLineIndent=0, textColor=INK, rightIndent=24),
 'code': ParagraphStyle('code', fontName='Mono', fontSize=7, leading=10, textColor=INK, leftIndent=8, backColor=colors.HexColor('#f2f5f6'), borderPadding=7, spaceBefore=4, spaceAfter=12),
 'coverlabel': ParagraphStyle('coverlabel', fontName='SansBold', fontSize=9, leading=15, textColor=colors.HexColor('#ddc99b'), alignment=TA_LEFT),
 'covertitle': ParagraphStyle('covertitle', fontName='BookBold', fontSize=26, leading=33, textColor=colors.white),
 'coversub': ParagraphStyle('coversub', fontName='Book', fontSize=11, leading=17, textColor=colors.HexColor('#e7ebef')),
}
class Diagram(Flowable):
    """Original vector figures; labels and captions describe the model."""
    def __init__(self, kind):
        super().__init__()
        self.kind = kind
        self.width = 320
        self.height = 125 if kind == 'arm' else (112 if kind == 'graph' else 92)

    def arrow(self, x1, y1, x2, y2):
        c = self.canv
        c.line(x1, y1, x2, y2)
        a = math.atan2(y2-y1, x2-x1)
        for d in (-0.5, 0.5):
            c.line(x2, y2, x2-6*math.cos(a+d), y2-6*math.sin(a+d))

    def draw(self):
        c = self.canv
        c.setStrokeColor(BLUE)
        c.setFillColor(INK)
        c.setLineWidth(1)
        if self.kind == 'agent':
            for x, label in [(0,'SENSORS'), (122,'AGENT'), (240,'ACTUATORS')]:
                c.roundRect(x, 55, 80, 26, 4, stroke=1, fill=0)
                c.setFont('SansBold', 7)
                c.drawCentredString(x+40, 64, label)
            self.arrow(80, 68, 122, 68)
            self.arrow(202, 68, 240, 68)
            c.roundRect(110, 5, 100, 25, 4, stroke=1, fill=0)
            c.setFont('SansBold', 7)
            c.drawCentredString(160, 14, 'ENVIRONMENT')
            # Environment to sensors; actuators to environment.
            c.line(110, 17, 40, 17)
            self.arrow(40, 17, 40, 55)
            c.line(280, 55, 280, 17)
            self.arrow(280, 17, 210, 17)
            c.setFont('Sans', 6.5)
            c.drawCentredString(101, 74, 'observe')
            c.drawCentredString(221, 74, 'command')
        elif self.kind == 'arm':
            # Ideal two-link example: base (50, 25), elbow (190, 25),
            # tip (190, 95); link lengths are shown at a 2:1 scale.
            c.setStrokeColor(colors.HexColor('#9aa8b5'))
            c.setDash(3, 3)
            self.arrow(50, 25, 300, 25)
            self.arrow(50, 25, 50, 112)
            c.setDash()
            c.setFont('Sans', 7)
            c.drawString(302, 23, 'x')
            c.drawString(53, 110, 'y')
            c.setStrokeColor(BLUE)
            c.setLineWidth(3)
            c.line(50, 25, 190, 25)
            c.line(190, 25, 190, 95)
            c.setLineWidth(1)
            for x,y in [(50,25),(190,25),(190,95)]:
                c.setFillColor(colors.white)
                c.circle(x,y,4,stroke=1,fill=1)
            c.setFillColor(INK)
            c.setFont('SansBold', 7)
            c.drawCentredString(120, 33, 'L1 = 1 m')
            c.drawString(198, 58, 'L2 = 0.5 m')
            c.setFont('Sans', 7)
            c.drawString(196, 95, 'tool (1, 0.5) m')
            c.drawString(100, 12, 'θ1 = 0°')
            c.drawString(196, 34, 'θ2 = 90°')
        elif self.kind == 'graph':
            pts = {'S': (16,55), 'A': (135,95),
                   'B': (135,15), 'G': (304,55)}
            def edge(a, b, label, lx, ly):
                x1,y1=pts[a]; x2,y2=pts[b]
                angle=math.atan2(y2-y1,x2-x1)
                self.arrow(x1+12*math.cos(angle), y1+12*math.sin(angle),
                           x2-12*math.cos(angle), y2-12*math.sin(angle))
                c.setFont('SansBold', 8)
                c.drawCentredString(lx, ly, label)
            edge('S','A','1',70,83)
            edge('S','B','4',70,25)
            edge('A','G','10',220,86)
            edge('A','B','1',145,52)
            edge('B','G','1',220,22)
            for name,(x,y) in pts.items():
                c.setFillColor(colors.white)
                c.circle(x,y,11,stroke=1,fill=1)
                c.setFillColor(INK)
                c.setFont('SansBold',9)
                c.drawCentredString(x,y-3,name)
        else:
            raise ValueError('Unknown diagram: ' + self.kind)

class BookDoc(BaseDocTemplate):
    def afterFlowable(self, flowable):
        if isinstance(flowable, Paragraph) and getattr(flowable, '_toc_title', None):
            title = flowable._toc_title
            key = 'section-' + str(self.seq.nextf('heading'))
            self.canv.bookmarkPage(key)
            self.canv.addOutlineEntry(title, key, 0, False)
            self.notify('TOCEntry', (0, title, self.page, key))

def decorate(c, doc):
    c.saveState()
    if doc.page == 1:
        c.setFillColor(colors.HexColor('#101d2a')); c.rect(0,0,W,H,fill=1,stroke=0)
        img = ROOT / 'assets/images/hero_ai_robotics.png'
        if img.exists():
            c.drawImage(ImageReader(str(img)), 0, 0, width=W, height=H, preserveAspectRatio=True, anchor='c', mask='auto')
            c.setFillColor(colors.Color(0.035,0.075,0.12,alpha=.83)); c.rect(0,0,W,H,fill=1,stroke=0)
        c.setStrokeColor(GOLD); c.setLineWidth(1.2); c.line(56, H-83, 155, H-83)
        c.setFont('Sans',8); c.setFillColor(colors.HexColor('#cbd4db')); c.drawString(56, 45, 'PRELIMINARY MANUSCRIPT  ·  NOT FOR PUBLICATION')
    else:
        c.setStrokeColor(colors.HexColor('#d8dfe4')); c.setLineWidth(.45); c.line(56, 39, W-56, 39)
        c.setFillColor(MUTED); c.setFont('Sans',7)
        c.drawString(56, 27, 'FOUNDATIONS OF AI AND ROBOTICS')
        c.drawRightString(W-56, 27, str(doc.page))
    c.restoreState()

def inline(s):
    s=escape(s)
    s=re.sub(r'`([^`]+)`', r'<font name="Mono">\1</font>', s)
    s=re.sub(r'\*\*(.+?)\*\*',r'<b>\1</b>',s)
    s=re.sub(r'\*(.+?)\*',r'<i>\1</i>',s)
    return s

doc=BookDoc(str(OUT), pagesize=(W,H), leftMargin=56, rightMargin=56, topMargin=60, bottomMargin=55,
    title='Volume I: Foundations of Artificial Intelligence and Robotics — Preliminary Manuscript',
    author='Editorial manuscript', subject='Incomplete introductory volume; not a publication-ready book')
frame=Frame(56,55,W-112,H-115,leftPadding=0,rightPadding=0,topPadding=0,bottomPadding=0,id='body')
doc.addPageTemplates(PageTemplate(id='book', frames=frame, onPage=decorate))
story=[Spacer(1,24),Paragraph('THE COMPLETE ENCYCLOPEDIA OF',styles['coverlabel']), Spacer(1,19),
       Paragraph('Artificial Intelligence<br/>and Robotics<br/>Engineering',styles['covertitle']), Spacer(1,30),
       Paragraph('VOLUME I',styles['coverlabel']), Spacer(1,10),
       Paragraph('Foundations of Artificial Intelligence and Robotics',styles['coversub']),
       Spacer(1,20),Paragraph('Introductory manuscript',styles['coversub']),PageBreak(),
       Paragraph('Contents',styles['h1'])]
toc=TableOfContents(); toc.levelStyles=[styles['toc']]; story += [toc,PageBreak()]
text=(HERE/'manuscript.md').read_text().replace('K𝒹','K_d')
lines=text.splitlines(); i=0; first=True
while i < len(lines):
    line=lines[i]
    if not line.strip(): i+=1; continue
    if line.startswith('# '):
        if not first: story.append(PageBreak())
        first=False
        title=line[2:].strip(); p=Paragraph(inline(title),styles['h1']); p._toc_title=title; story.append(p); i+=1; continue
    if line.startswith('## '):
        story.append(Paragraph(inline(line[3:].strip()),styles['h2'])); i+=1; continue
    if line.startswith('### '):
        story.append(Paragraph(inline(line[4:].strip()),styles['h3'])); i+=1; continue
    if line.startswith('[FIGURE:'):
        match = re.fullmatch(r'\[FIGURE:(agent|graph|arm)\]', line)
        if not match:
            raise ValueError('Unknown figure marker: ' + line)
        i += 1
        while i < len(lines) and not lines[i].strip():
            i += 1
        if i >= len(lines) or not lines[i].startswith('Figure '):
            raise ValueError('Figure must be followed by a caption')
        story.append(KeepTogether([Diagram(match.group(1)),
                                   Paragraph(inline(lines[i]), styles['body'])]))
        i += 1
        continue
    if line.startswith('```'):
        i+=1; code=[]
        while i < len(lines) and not lines[i].startswith('```'):
            code.append(lines[i]); i+=1
        story.append(Preformatted('\n'.join(code), styles['code'])); i+=1; continue
    if re.match(r'^(?:\d+\.|-) ', line):
        story.append(Paragraph(inline(line), styles['body']))
        i += 1
        continue
    acc=[]
    while i < len(lines) and lines[i].strip() and not lines[i].startswith(('# ', '## ', '### ', '```', '[FIGURE:')):
        acc.append(lines[i].strip()); i+=1
    s=' '.join(acc)
    story.append(Paragraph(inline(s),styles['body']))
doc.multiBuild(story)
print(OUT)
