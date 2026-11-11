#!/usr/bin/env python3
"""Build the preliminary Volume I manuscript as a navigable PDF."""
from pathlib import Path
from xml.sax.saxutils import escape
import re
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.platypus import (BaseDocTemplate, PageTemplate, Frame, Paragraph,
    Spacer, PageBreak, Preformatted, KeepTogether)
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
 'h2': ParagraphStyle('h2', fontName='SansBold', fontSize=11, leading=15, textColor=BLUE, spaceBefore=13, spaceAfter=7, keepWithNext=True),
 'toc': ParagraphStyle('toc', fontName='Book', fontSize=10, leading=19, leftIndent=0, firstLineIndent=0, textColor=INK, rightIndent=24),
 'code': ParagraphStyle('code', fontName='Mono', fontSize=7, leading=10, textColor=INK, leftIndent=8, backColor=colors.HexColor('#f2f5f6'), borderPadding=7, spaceBefore=4, spaceAfter=12),
 'coverlabel': ParagraphStyle('coverlabel', fontName='SansBold', fontSize=9, leading=15, textColor=colors.HexColor('#ddc99b'), alignment=TA_LEFT),
 'covertitle': ParagraphStyle('covertitle', fontName='BookBold', fontSize=26, leading=33, textColor=colors.white),
 'coversub': ParagraphStyle('coversub', fontName='Book', fontSize=11, leading=17, textColor=colors.HexColor('#e7ebef')),
}
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
    if line.startswith('```'):
        i+=1; code=[]
        while i < len(lines) and not lines[i].startswith('```'):
            code.append(lines[i]); i+=1
        story.append(Preformatted('\n'.join(code), styles['code'])); i+=1; continue
    acc=[]
    while i < len(lines) and lines[i].strip() and not lines[i].startswith(('# ', '## ', '```')):
        acc.append(lines[i].strip()); i+=1
    s=' '.join(acc)
    story.append(Paragraph(inline(s),styles['body']))
doc.multiBuild(story)
print(OUT)
