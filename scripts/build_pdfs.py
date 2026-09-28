"""Generate printable patient resources from client-owned content. Requires reportlab."""
import json,re
from pathlib import Path
from html import escape
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, KeepTogether
from reportlab.lib.styles import getSampleStyleSheet,ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'output/pdf';OUT.mkdir(parents=True,exist_ok=True)
FONT=Path('/home/keithmayberry/.cache/codex-runtimes/codex-primary-runtime/dependencies/native/libreoffice-headless/libreoffice/share/fonts/truetype')
# Font names are environment-configurable for use outside the bundled runtime.
import os
FONT=Path(os.environ.get('ISCHYS_FONT_DIR',str(FONT)))
for name,file in [('Body','DejaVuSans.ttf'),('Bold','DejaVuSans-Bold.ttf')]:pdfmetrics.registerFont(TTFont(name,str(FONT/file)))
styles=getSampleStyleSheet()
styles.add(ParagraphStyle(name='Copy',fontName='Body',fontSize=9.5,leading=14,spaceAfter=7,textColor=colors.HexColor('#243d3d')))
styles.add(ParagraphStyle(name='Section',fontName='Bold',fontSize=12,leading=17,spaceBefore=15,spaceAfter=8,keepWithNext=True,textColor=colors.HexColor('#0b4f54')))
styles.add(ParagraphStyle(name='PageTitle',fontName='Bold',fontSize=23,leading=29,spaceAfter=16,textColor=colors.HexColor('#0b4f54')))
styles.add(ParagraphStyle(name='Fine',fontName='Body',fontSize=8,leading=11,spaceAfter=8,textColor=colors.HexColor('#54605b')))
S=json.loads((ROOT/'content/source-sections.json').read_text());T=json.loads((ROOT/'content/trackers.json').read_text())
titles={'welcome':'Welcome to Ischys','starting-point':'My Starting Point','wellness-plan':'My Mental Wellness Plan','hard-day':'When I’m Having a Hard Day','resources':'Resources & Staying Connected'}
links={'PATIENT PORTAL':('Patient portal: call 801-796-2552 for the current secure link.',None),'ISCHYS LEARNING CENTER':('Ask the practice for the Learning Center website address.',None),'USARA':('USARA','https://myusara.com/locations/'),'ARP':('Faith-based Addiction Recovery Program','https://addictionrecovery.churchofjesuschrist.org/'),'SMART RECOVERY':('SMART Recovery meetings','https://support.smartrecovery.org/find-a-smart-meeting'),'LOCAL MEETING RESOURCES':('Alcoholics Anonymous meetings','https://www.aa.org/find-aa'),'FAMILY SUPPORT RESOURCES':('SMART Recovery Family & Friends','https://smartrecovery.org/family'),'NAMI UTAH':('NAMI Utah','https://namiut.org/')}
def p(s,style='Copy'):return Paragraph(escape(s).replace('\n','<br/>'),styles[style])
def footer(canvas,doc):
 canvas.saveState();canvas.setStrokeColor(colors.HexColor('#d9ddd4'));canvas.line(48,44,564,44);canvas.setFont('Body',7);canvas.setFillColor(colors.HexColor('#54605b'));canvas.drawString(48,31,'Ischys Integrative Mental Wellness | 801-796-2552 | September 2026');canvas.drawRightString(564,31,str(doc.page));canvas.restoreState()
def build(key,title,story):
 SimpleDocTemplate(str(OUT/(key+'.pdf')),pagesize=(612,792),leftMargin=48,rightMargin=48,topMargin=42,bottomMargin=58,title=title,author='Laura Jane Hyte-Garner, MSN, APRN, PMHNP-BC').build(story,onFirstPage=footer,onLaterPages=footer)
for key,title in titles.items():
 story=[p('ISCHYS INTEGRATIVE MENTAL WELLNESS','Fine'),p(title,'PageTitle'),p('By Laura Jane Hyte-Garner, MSN, APRN, PMHNP-BC','Fine')]
 skipratings=False
 for block in S[key]['blocks']:
  text=block['text'];typ=block['type']
  if key=='starting-point' and text=='How Am I Doing Right Now?':
   story.append(p(text,'Section'));story.append(p('Think about the past 1–2 weeks. 0 = Really struggling; 5 = Somewhere in the middle; 10 = Doing very well.'))
   rows=[[p('Area of my life','Fine'),p('Circle a rating','Fine')]]
   for label in ['Mood','Stress / Anxiety','Sleep','Energy','Focus','Motivation','Physical Well-Being','Connection','Enjoyment','Daily Functioning','Overall Mental Wellness']:
    rows.append([p(label),p('0  1  2  3  4  5  6  7  8  9  10')])
   table=Table(rows,colWidths=[205,311],repeatRows=1);table.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),colors.HexColor('#eef0e9')),('LINEBELOW',(0,0),(-1,-1),.4,colors.HexColor('#d9ddd4')),('VALIGN',(0,0),(-1,-1),'TOP'),('TOPPADDING',(0,0),(-1,-1),7),('BOTTOMPADDING',(0,0),(-1,-1),6)]));story.append(table);skipratings=True;continue
  if skipratings:
   if text=='Look at Your Numbers':skipratings=False
   else:continue
  if text.startswith('QR CODE:'):
   label,url=links.get(text[8:].strip(),('Contact the practice for resource information.',None))
   if url:story.append(Paragraph(f'<link href="{escape(url,quote=True)}" color="#0b4f54">{escape(label)}: {escape(url)}</link>',styles['Fine']))
   else:story.append(p(label,'Fine'))
   continue
  if typ=='h2':story.append(p(text,'Section'))
  else:
   story.append(p(text))
   if ('_' in text or text.endswith(':')) and len(text)<100:story.append(Spacer(1,10))
 build(key,title,story)
for key,t in T.items():
 story=[p('ISCHYS INTEGRATIVE MENTAL WELLNESS','Fine'),p(t['title'],'PageTitle'),p(t['description']),p('Name (optional): ____________________    Date: ____________________','Fine')]
 for field in t['fields']:
  story.append(KeepTogether([p(field,'Copy'),Spacer(1,6),Table([['']],colWidths=[516],style=[('LINEBELOW',(0,0),(-1,-1),.5,colors.HexColor('#b7c1b6'))]),Spacer(1,7)]))
 story.extend([Spacer(1,8),p(t['note'],'Fine'),p('Educational self-reflection only; not individualized treatment. For immediate danger, call 911. For crisis support in the U.S., call or text 988.','Fine')]);build(key,t['title'],story)
print('Generated',len(list(OUT.glob('*.pdf'))),'printable PDFs.')
