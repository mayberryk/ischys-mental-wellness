"""Extract client-owned content from the Word package without changing the source."""
import json, re, sys, zipfile, xml.etree.ElementTree as ET
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
NS={'w':'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}
with zipfile.ZipFile(sys.argv[1]) as z:
 root=ET.fromstring(z.read('word/document.xml'))
 lines=[''.join(t.text or '' for t in p.findall('.//w:t',NS)).strip() for p in root.findall('.//w:p',NS)]
lines=[x for x in lines if x]
(ROOT/'content/source-package.txt').write_text('\n'.join(lines)+'\n')
sections=[
('welcome','Welcome to Ischys Integrative Mental Wellness'),
('starting-point','My Starting Point'),
('hobbies','Hobbies That Support Mental Health: Finding Something That Helps Your Brain Recharge'),
('caffeine','Caffeine: More Than Just a Morning Pick-Me-Up'),
('sleep','Sleep: Your Brain Needs It More Than You Think'),
('movement','Movement & Your Mental Health'),
('nutrition','Food, Hydration & Your Brain'),
('fermented','Fermented Foods & Your Gut Microbiome'),
('connection','Connection: Your Brain Needs People Too'),
('regulation','Stress & Your Nervous System'),
('substances','Substances & Your Mental Health'),
('medication','Getting the Most From Your Medication'),
('wellness-plan','My Mental Wellness Plan'),
('hard-day','When I\'m Having a Hard Day'),
('resources','Resources & Staying Connected'),
('end','Welcome to Ischys — patient welcome module')]
start=lines.index('PART 6 — PATIENT RESOURCE LIBRARY')
# Titles also occur in the library inventory; locate the actual bodies sequentially.
positions=[]
for key,title in sections:
 idx=lines.index(title,start)
 if key=='wellness-plan' and idx<500: raise ValueError('Matched inventory instead of body')
 positions.append(idx);start=idx+1
stopwords={'a','an','and','or','the','to','for','of','in','on','with','your','you','at','from','it','is','as','than','my','by','when','but','be','that','into','do','can','if','what','how','why','does','not','are','have','our','more','too','before','after','through','without','about','up'}
def heading(s):
 if len(s)>105 or '_' in s or s.endswith(('.',':',';')) or s.startswith(('"','“')): return False
 words=re.findall(r"[A-Za-z]+(?:['’][A-Za-z]+)?",s)
 return len(words)>1 and all(w[0].isupper() or w.lower() in stopwords for w in words)
def clean(s):
 s=s.replace('evidenceinformed','evidence-informed').replace('substanceuse','substance-use')
 if s=='Notice Understand Experiment Track Discuss → → → →': return 'Notice → Understand → Experiment → Track → Discuss'
 if s=='Choose Start Observe Measure Adjust → → → →':return 'Choose → Start → Observe → Measure → Adjust'
 return s
out={}
for i,(key,title) in enumerate(sections[:-1]):
 raw=lines[positions[i]+1:positions[i+1]]
 blocks=[];buffer=''
 def flush():
  global buffer
  if buffer: blocks.append({'type':'p','text':clean(buffer)});buffer=''
 for line in raw:
  if heading(line):
   flush();blocks.append({'type':'h2','text':line});continue
  if buffer: buffer+=' '+line
  else:buffer=line
  # Restore paragraphs broken into fixed-width lines in the supplied document.
  if line.endswith(('.', '?','!',':','”','"')) or len(line)<65 or '_' in line or '•' in line:flush()
 flush()
 out[key]={'source_title':title,'blocks':blocks,'source_lines':raw}
(ROOT/'content/source-sections.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n')
print('Extracted',len(out),'full content sections;',sum(len(v['source_lines']) for v in out.values()),'source paragraphs preserved.')
